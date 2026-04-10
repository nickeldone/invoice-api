import unittest
from app import app

class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_sustained_load(self):
        """Verify API stability under sustained load."""
        for _ in range(600):
            resp = self.client.get('/api/invoices')
            self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()
