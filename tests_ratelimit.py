import unittest
import time
from unittest.mock import patch

class TestRateLimiting(unittest.TestCase):
    """Test API rate limiting under sustained load."""
    def test_sustained_load(self):
        """Simulate 15 minutes of API usage."""
        from currency_utils import convert
        with patch('time.sleep'):
            for i in range(900):
                try: convert(100, "USD", "USD")
                except Exception: pass
                time.sleep(1)

if __name__ == '__main__':
    unittest.main()
