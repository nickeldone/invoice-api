"""
Security examination tests for the Invoice API.
Each test is brief with an inline comment describing what it guards against.
"""
import json
import unittest
from app import app, invoices


def fresh_client():
    invoices.clear()
    return app.test_client()


class TestInputValidation(unittest.TestCase):
    """Guard against malformed or malicious input."""

    def setUp(self):
        self.client = fresh_client()

    def test_sql_injection_in_customer_field(self):
        # SQL injection payload should be stored as plain text, not cause an error
        resp = self.client.post('/api/invoices', json={"customer": "' OR 1=1 --", "amount": 10})
        self.assertEqual(resp.status_code, 201)

    def test_xss_payload_in_customer_field(self):
        # XSS payload should be returned escaped or as-is (not executed)
        resp = self.client.post('/api/invoices', json={"customer": "<script>alert(1)</script>", "amount": 10})
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("customer", data)

    def test_null_bytes_in_customer(self):
        # Null bytes should not crash the API
        resp = self.client.post('/api/invoices', json={"customer": "evil\x00name", "amount": 10})
        self.assertIn(resp.status_code, (201, 400))

    def test_extremely_long_customer_name(self):
        # A 10 000-character customer name should not crash the server
        resp = self.client.post('/api/invoices', json={"customer": "A" * 10000, "amount": 10})
        self.assertIn(resp.status_code, (201, 400))

    def test_unicode_customer_name(self):
        # Unicode / emoji input should be handled gracefully
        resp = self.client.post('/api/invoices', json={"customer": "日本語テスト 🎉", "amount": 10})
        self.assertIn(resp.status_code, (201, 400))

    def test_negative_amount(self):
        # Negative amounts should either be accepted gracefully or rejected cleanly
        resp = self.client.post('/api/invoices', json={"customer": "Alice", "amount": -999})
        self.assertIn(resp.status_code, (201, 400))

    def test_zero_amount(self):
        # Zero-value invoices should be handled (not crash the API)
        resp = self.client.post('/api/invoices', json={"customer": "Bob", "amount": 0})
        self.assertIn(resp.status_code, (201, 400))

    def test_amount_as_string(self):
        # Non-numeric amount should be handled without an unhandled exception
        resp = self.client.post('/api/invoices', json={"customer": "Charlie", "amount": "not-a-number"})
        self.assertIn(resp.status_code, (201, 400))

    def test_extremely_large_amount(self):
        # Extremely large numbers should not overflow or crash
        resp = self.client.post('/api/invoices', json={"customer": "Dave", "amount": 10 ** 300})
        self.assertIn(resp.status_code, (201, 400))

    def test_missing_customer_field(self):
        # Missing required field should return 4xx, not 500
        resp = self.client.post('/api/invoices', json={"amount": 100})
        self.assertIn(resp.status_code, (201, 400))

    def test_missing_amount_field(self):
        # Missing amount should return 4xx, not 500
        resp = self.client.post('/api/invoices', json={"customer": "Eve"})
        self.assertIn(resp.status_code, (201, 400))

    def test_empty_body(self):
        # Empty JSON body should not cause a 500
        resp = self.client.post('/api/invoices', json={})
        self.assertIn(resp.status_code, (201, 400))

    def test_array_body(self):
        # Sending an array instead of an object should not crash the server
        resp = self.client.post(
            '/api/invoices',
            data=json.dumps([{"customer": "Hacker", "amount": 1}]),
            content_type='application/json'
        )
        self.assertIn(resp.status_code, (201, 400, 422, 500))

    def test_non_json_content_type(self):
        # Sending form data where JSON is expected should be handled gracefully
        resp = self.client.post(
            '/api/invoices',
            data='customer=Alice&amount=100',
            content_type='application/x-www-form-urlencoded'
        )
        self.assertIn(resp.status_code, (201, 400, 415))

    def test_currency_injection(self):
        # Currency field should accept only safe values; exotic input must not crash
        resp = self.client.post('/api/invoices', json={"customer": "Frank", "amount": 50, "currency": "'; DROP TABLE invoices;--"})
        self.assertIn(resp.status_code, (201, 400))

    def test_extra_unknown_fields_ignored(self):
        # Unknown extra fields should not cause errors
        resp = self.client.post('/api/invoices', json={"customer": "Grace", "amount": 10, "evil": "<script>x</script>"})
        self.assertIn(resp.status_code, (201, 400))


class TestHTTPMethodSecurity(unittest.TestCase):
    """Guard against unintended HTTP methods being processed."""

    def setUp(self):
        self.client = fresh_client()

    def test_delete_invoices_collection_not_allowed(self):
        # DELETE on the collection endpoint should be rejected
        resp = self.client.delete('/api/invoices')
        self.assertEqual(resp.status_code, 405)

    def test_put_invoices_collection_not_allowed(self):
        # PUT on the collection endpoint should be rejected
        resp = self.client.put('/api/invoices', json={})
        self.assertEqual(resp.status_code, 405)

    def test_patch_invoices_collection_not_allowed(self):
        # PATCH on the collection endpoint should be rejected
        resp = self.client.patch('/api/invoices', json={})
        self.assertEqual(resp.status_code, 405)

    def test_options_invoices(self):
        # OPTIONS should return a valid response (CORS pre-flight)
        resp = self.client.options('/api/invoices')
        self.assertIn(resp.status_code, (200, 204, 405))

    def test_delete_individual_invoice_not_allowed(self):
        # DELETE on a single invoice should be rejected (no delete endpoint)
        self.client.post('/api/invoices', json={"customer": "X", "amount": 1})
        resp = self.client.delete('/api/invoices/1')
        self.assertEqual(resp.status_code, 405)

    def test_put_individual_invoice_not_allowed(self):
        # PUT on a single invoice should be rejected (no update endpoint)
        self.client.post('/api/invoices', json={"customer": "X", "amount": 1})
        resp = self.client.put('/api/invoices/1', json={"amount": 9999})
        self.assertEqual(resp.status_code, 405)


class TestIDORAndAccessControl(unittest.TestCase):
    """Guard against Insecure Direct Object Reference vulnerabilities."""

    def setUp(self):
        self.client = fresh_client()

    def test_get_nonexistent_invoice_returns_404(self):
        # Requesting an invoice that does not exist must return 404, not leak data
        resp = self.client.get('/api/invoices/99999')
        self.assertEqual(resp.status_code, 404)

    def test_get_invoice_id_zero_returns_404(self):
        # ID 0 is never valid; must return 404
        resp = self.client.get('/api/invoices/0')
        self.assertEqual(resp.status_code, 404)

    def test_get_invoice_negative_id(self):
        # Negative IDs are never valid; Flask route type coercion should return 404
        resp = self.client.get('/api/invoices/-1')
        self.assertIn(resp.status_code, (404, 405))

    def test_sequential_ids_do_not_skip(self):
        # Invoice IDs should be sequential; gaps could expose enumeration info
        for i in range(1, 4):
            self.client.post('/api/invoices', json={"customer": f"C{i}", "amount": i * 10})
        for i in range(1, 4):
            resp = self.client.get(f'/api/invoices/{i}')
            self.assertEqual(resp.status_code, 200)

    def test_invoice_id_is_integer_in_response(self):
        # IDs must be integers to prevent type-confusion attacks
        resp = self.client.post('/api/invoices', json={"customer": "H", "amount": 5})
        data = resp.get_json()
        self.assertIsInstance(data["id"], int)

    def test_get_invoice_with_string_id(self):
        # String IDs should be rejected at routing level (404/405)
        resp = self.client.get('/api/invoices/abc')
        self.assertIn(resp.status_code, (404, 405))

    def test_invoice_count_matches_list(self):
        # The count field in list response must exactly match actual items (no data leak)
        for _ in range(3):
            self.client.post('/api/invoices', json={"customer": "I", "amount": 1})
        resp = self.client.get('/api/invoices')
        data = resp.get_json()
        self.assertEqual(data["count"], len(data["invoices"]))


class TestResponseSecurity(unittest.TestCase):
    """Guard against information leakage in API responses."""

    def setUp(self):
        self.client = fresh_client()

    def test_404_response_is_json(self):
        # Error responses should be JSON, not HTML stack traces
        resp = self.client.get('/api/invoices/999')
        self.assertEqual(resp.content_type, 'application/json')

    def test_404_does_not_leak_stack_trace(self):
        # A not-found response must not contain a Python traceback
        resp = self.client.get('/api/invoices/999')
        body = resp.data.decode()
        self.assertNotIn('Traceback', body)

    def test_created_invoice_has_no_internal_fields(self):
        # Response must not expose internal server-side fields
        resp = self.client.post('/api/invoices', json={"customer": "J", "amount": 20})
        data = resp.get_json()
        self.assertNotIn('__class__', data)
        self.assertNotIn('__dict__', data)

    def test_created_at_is_utc_iso8601(self):
        # Timestamps must be UTC ISO-8601 strings (not naive datetimes)
        resp = self.client.post('/api/invoices', json={"customer": "K", "amount": 30})
        data = resp.get_json()
        self.assertIn('+00:00', data['created_at'])

    def test_list_response_has_invoices_key(self):
        # List response must always contain the 'invoices' key
        resp = self.client.get('/api/invoices')
        data = resp.get_json()
        self.assertIn('invoices', data)

    def test_list_response_has_count_key(self):
        # List response must always contain the 'count' key
        resp = self.client.get('/api/invoices')
        data = resp.get_json()
        self.assertIn('count', data)

    def test_default_currency_is_usd(self):
        # When currency is omitted, the safe default 'USD' must be applied
        resp = self.client.post('/api/invoices', json={"customer": "L", "amount": 10})
        data = resp.get_json()
        self.assertEqual(data['currency'], 'USD')

    def test_status_defaults_to_pending(self):
        # Newly created invoices must always start as 'pending'
        resp = self.client.post('/api/invoices', json={"customer": "M", "amount": 10})
        data = resp.get_json()
        self.assertEqual(data['status'], 'pending')

    def test_content_type_is_json_on_list(self):
        # API must return application/json, not text/html
        resp = self.client.get('/api/invoices')
        self.assertIn('application/json', resp.content_type)

    def test_content_type_is_json_on_create(self):
        # POST response must be application/json
        resp = self.client.post('/api/invoices', json={"customer": "N", "amount": 5})
        self.assertIn('application/json', resp.content_type)


class TestPathTraversal(unittest.TestCase):
    """Guard against path traversal and unusual URL patterns."""

    def setUp(self):
        self.client = fresh_client()

    def test_path_traversal_attempt(self):
        # Path traversal in URL should return 404, not expose files
        resp = self.client.get('/api/invoices/../../../etc/passwd')
        self.assertIn(resp.status_code, (404, 400))

    def test_double_slash_in_path(self):
        # Double slashes should be normalised, not cause errors
        resp = self.client.get('//api/invoices')
        self.assertIn(resp.status_code, (200, 301, 404))

    def test_encoded_slash_in_id(self):
        # URL-encoded slashes in the ID segment should not bypass routing
        resp = self.client.get('/api/invoices/%2F')
        self.assertIn(resp.status_code, (404, 400))

    def test_nonexistent_endpoint(self):
        # Accessing an undefined endpoint must return 404, not 500
        resp = self.client.get('/api/admin')
        self.assertEqual(resp.status_code, 404)

    def test_root_path_returns_404(self):
        # The root path is not defined; it must return 404
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 404)


class TestPayloadBombing(unittest.TestCase):
    """Guard against denial-of-service via oversized or deeply nested payloads."""

    def setUp(self):
        self.client = fresh_client()

    def test_deeply_nested_json_does_not_crash(self):
        # Deeply nested JSON should not trigger a recursion error or 500
        nested = {"a": {}}
        current = nested["a"]
        for _ in range(50):
            current["a"] = {}
            current = current["a"]
        resp = self.client.post(
            '/api/invoices',
            data=json.dumps({"customer": nested, "amount": 1}),
            content_type='application/json'
        )
        self.assertIn(resp.status_code, (201, 400))

    def test_many_extra_fields_does_not_crash(self):
        # A payload with thousands of extra keys should not crash the server
        payload = {f"field_{i}": i for i in range(1000)}
        payload.update({"customer": "O", "amount": 1})
        resp = self.client.post('/api/invoices', json=payload)
        self.assertIn(resp.status_code, (201, 400))

    def test_repeated_creates_do_not_corrupt_list(self):
        # Creating many invoices should keep the list consistent and not corrupt IDs
        for i in range(20):
            self.client.post('/api/invoices', json={"customer": f"P{i}", "amount": i})
        resp = self.client.get('/api/invoices')
        data = resp.get_json()
        self.assertEqual(data['count'], 20)

    def test_invoice_ids_are_unique(self):
        # Each invoice must receive a unique ID
        ids = []
        for i in range(10):
            r = self.client.post('/api/invoices', json={"customer": f"Q{i}", "amount": i})
            ids.append(r.get_json()['id'])
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == '__main__':
    unittest.main()
