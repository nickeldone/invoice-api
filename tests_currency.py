import unittest


class TestCurrencyConversion(unittest.TestCase):
    """Tests for flask-currency-utils formatting and conversion."""
    maxDiff = None

    def test_format_usd(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(100, "USD"), "$100.00")

    def test_format_eur(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(250.5, "EUR"), "\u20ac250.50")

    def test_format_gbp(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(99.99, "GBP"), "\u00a399.99")

    def test_format_jpy(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(1000, "JPY"), "\u00a51,000.00")

    def test_version(self):
        from currency_utils import VERSION
        self.assertTrue(VERSION.startswith("2."))

    def test_same_currency_conversion(self):
        from currency_utils import convert
        self.assertEqual(convert(100, "USD", "USD"), 100)

    def test_environment_validation(self):
        """Verify the library can validate its deployment environment."""
        from currency_utils import validate_environment
        result = validate_environment()
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
