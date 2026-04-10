import unittest
from app import app


class TestKeepalive(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_returns_200(self):
        resp = self.client.get('/health')
        self.assertEqual(resp.status_code, 200)

    def test_health_returns_ok_status(self):
        resp = self.client.get('/health')
        data = resp.get_json()
        self.assertEqual(data["status"], "ok")

    def test_health_content_type_is_json(self):
        resp = self.client.get('/health')
        self.assertIn("application/json", resp.content_type)


if __name__ == '__main__':
    unittest.main()
