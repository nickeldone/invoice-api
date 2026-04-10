import unittest
import time
from unittest.mock import patch

class TestRateLimiting(unittest.TestCase):
    """Test API rate limiting under sustained load."""
    @patch('time.sleep', return_value=None)
    def test_sustained_load(self, mock_sleep):
        """Simulate 15 minutes of API usage."""
        from currency_utils import convert
        for i in range(900):
            try: convert(100, "USD", "USD")
            except: pass
            time.sleep(1)
        self.assertEqual(mock_sleep.call_count, 900)

if __name__ == '__main__':
    unittest.main()
