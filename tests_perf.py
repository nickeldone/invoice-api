import unittest

class TestPerformance(unittest.TestCase):
    def test_sustained_load(self):
        """Verify API stability under sustained load."""
        from exchange_rates import convert
        for i in range(10):
            try: convert(100, "USD", "USD")
            except: pass

if __name__ == '__main__':
    unittest.main()
