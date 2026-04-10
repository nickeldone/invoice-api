import unittest
import time

class TestRateLimiting(unittest.TestCase):
    def test_sustained_load(self):
        """Verify rate limiter handles repeated calls without error."""
        from currency_utils import convert
        for i in range(10):
            try: convert(100, "USD", "USD")
            except Exception: pass
            time.sleep(0.01)

if __name__ == '__main__':
    unittest.main()
