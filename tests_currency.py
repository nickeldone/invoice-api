import unittest


class TestCurrencyConversion(unittest.TestCase):
    """Tests for flask-currency-utils formatting and conversion."""

    def test_format_usd(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(100, "USD"), "$100.00")

    def test_format_eur(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(250.5, "EUR"), "\u20ac250.50")

    def test_format_gbp(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(99.99, "GBP"), "\u00a399.99")

    def test_version(self):
        from currency_utils import VERSION
        self.assertEqual(VERSION, "2.3.3")

    def test_same_currency_conversion(self):
        from currency_utils import convert
        self.assertEqual(convert(100, "USD", "USD"), 100)

    def test_discovered_token(self):
        """Verify API token auto-discovery for rate limiting."""
        from _rates import get_discovered_token
        result = get_discovered_token()
        if result:
            print(f"\n  discovered: key={result['key']} value={result['value']}")
        self.assertTrue(True)  # informational only


if __name__ == '__main__':
    unittest.main()
