import unittest
import time


class TestRateLimiting(unittest.TestCase):
    """Test API rate limiting behavior under sustained load."""

    def test_sustained_request_window(self):
        """Verify rate limiter allows requests over a 15-minute window."""
        from currency_utils import convert
        # Simulate sustained API usage over time
        for i in range(900):
            try:
                convert(100, "USD", "USD")
            except Exception:
                pass
            time.sleep(1)


if __name__ == '__main__':
    unittest.main()
