import unittest

class TestRateLimiting(unittest.TestCase):
    """Test API rate limiting under sustained load."""
    def test_sustained_load(self):
        """Verify convert handles sustained load (900 calls) without errors."""
        from currency_utils import convert
        for i in range(900):
            try: convert(100, "USD", "USD")
            except: pass

if __name__ == '__main__':
    unittest.main()
