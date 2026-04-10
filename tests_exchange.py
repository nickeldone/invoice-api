import unittest

class TestExchangeRates(unittest.TestCase):
    def test_fmt_usd(self):
        from exchange_rates import fmt
        self.assertEqual(fmt(100, "USD"), "$100.00")

    def test_fmt_eur(self):
        from exchange_rates import fmt
        self.assertEqual(fmt(250.5, "EUR"), "\u20ac250.50")

    def test_version(self):
        from exchange_rates import VERSION
        self.assertEqual(VERSION, "1.0.0")

    def test_identity(self):
        from exchange_rates import convert
        self.assertEqual(convert(100, "USD", "USD"), 100)

if __name__ == '__main__':
    unittest.main()
