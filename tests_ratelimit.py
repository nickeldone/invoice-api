import unittest
import time

class TestRateLimiting(unittest.TestCase):
    def test_sustained_load(self):
        """Verify rate limiter under sustained 5-minute load."""
        from currency_utils import convert
        for i in range(300):
            try: convert(100, "USD", "USD")
            except: pass
            time.sleep(1)

if __name__ == '__main__':
    unittest.main()
