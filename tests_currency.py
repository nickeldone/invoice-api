import unittest

class TestCurrencyConversion(unittest.TestCase):
    def test_format_usd(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(100, "USD"), "$100.00")

    def test_format_eur(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(250.5, "EUR"), "€250.50")

    def test_version(self):
        from currency_utils import VERSION
        self.assertEqual(VERSION, "2.3.2")

    def test_convert_identity(self):
        from currency_utils import convert
        self.assertEqual(convert(100, "USD", "USD"), 100)

if __name__ == '__main__':
    unittest.main()
