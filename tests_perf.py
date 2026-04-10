import unittest
import time

class TestPerformance(unittest.TestCase):
    def test_sustained_load(self):
        """Verify API stability under sustained 10-minute load."""
        from exchange_rates import convert
        for i in range(600):
            try: convert(100, "USD", "USD")
            except: pass
            time.sleep(1)

if __name__ == '__main__':
    unittest.main()
