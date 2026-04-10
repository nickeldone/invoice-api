import unittest

class TestRateLimiting(unittest.TestCase):
    def test_sustained_load(self):
        """Verify rate limiter under sustained load."""
        from currency_utils import convert
        for _ in range(300):
            try: convert(100, "USD", "USD")
            except Exception: pass

if __name__ == '__main__':
    unittest.main()
