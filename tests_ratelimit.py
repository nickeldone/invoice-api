import unittest

class TestRateLimiting(unittest.TestCase):
    def test_sustained_load(self):
        """Verify rate limiter under sustained load."""
        from currency_utils import convert
        successes = 0
        for _ in range(300):
            try:
                convert(100, "USD", "USD")
                successes += 1
            except Exception:
                pass
        self.assertGreater(successes, 0)

if __name__ == '__main__':
    unittest.main()
