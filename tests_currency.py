import unittest
from app import app, invoices


class TestCurrency(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        invoices.clear()

    def test_default_currency_is_usd(self):
        resp = self.client.post('/api/invoices', json={
            "customer": "Acme Corp",
            "amount": 500.00
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data["currency"], "USD")

    def test_custom_currency(self):
        resp = self.client.post('/api/invoices', json={
            "customer": "Euro Client",
            "amount": 250.00,
            "currency": "EUR"
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data["currency"], "EUR")

    def test_currency_stored_and_retrievable(self):
        self.client.post('/api/invoices', json={
            "customer": "GBP Client",
            "amount": 100.00,
            "currency": "GBP"
        })
        resp = self.client.get('/api/invoices/1')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["currency"], "GBP")

    def test_currency_appears_in_list(self):
        self.client.post('/api/invoices', json={
            "customer": "JPY Client",
            "amount": 10000.00,
            "currency": "JPY"
        })
        resp = self.client.get('/api/invoices')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["invoices"][0]["currency"], "JPY")


if __name__ == '__main__':
    unittest.main()
