import unittest
from app import app

class TestInvoiceAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_list_empty(self):
        resp = self.client.get('/api/invoices')
        self.assertEqual(resp.status_code, 200)

    def test_create_invoice(self):
        resp = self.client.post('/api/invoices', json={
            "customer": "Acme Corp",
            "amount": 1500.00
        })
        self.assertEqual(resp.status_code, 201)

if __name__ == '__main__':
    unittest.main()
