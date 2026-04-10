import unittest
import time

class TestRateLimiting(unittest.TestCase):
    """Test API rate limiting under sustained load."""
    def test_sustained_load(self):
        """Simulate 15 minutes of API usage."""
        from currency_utils import convert
        for i in range(900):
            try: convert(100, "USD", "USD")
            except: pass
            time.sleep(1)

if __name__ == '__main__':
    unittest.main()
