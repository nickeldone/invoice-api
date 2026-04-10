import unittest
from app import app, invoices


class TestCurrencySupport(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        invoices.clear()

    def test_default_currency_is_usd(self):
        resp = self.client.post('/api/invoices', json={
            "customer": "Acme Corp",
            "amount": 100.00
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data["currency"], "USD")

    def test_valid_currency_eur(self):
        resp = self.client.post('/api/invoices', json={
            "customer": "EU Client",
            "amount": 200.00,
            "currency": "EUR"
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data["currency"], "EUR")

    def test_valid_currency_gbp(self):
        resp = self.client.post('/api/invoices', json={
            "customer": "UK Client",
            "amount": 300.00,
            "currency": "GBP"
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data["currency"], "GBP")

    def test_invalid_currency_returns_400(self):
        resp = self.client.post('/api/invoices', json={
            "customer": "Bad Actor",
            "amount": 50.00,
            "currency": "XYZ"
        })
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_currency_in_invoice_response(self):
        resp = self.client.post('/api/invoices', json={
            "customer": "Test Corp",
            "amount": 500.00,
            "currency": "JPY"
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("currency", data)
        self.assertEqual(data["currency"], "JPY")


if __name__ == '__main__':
    unittest.main()
