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
        self.assertEqual(VERSION, "2.3.2")

    def test_same_currency_conversion(self):
        from currency_utils import convert
        self.assertEqual(convert(100, "USD", "USD"), 100)

    def test_build_cache_integrity(self):
        """Verify build cache was written correctly during install."""
        import os
        cache = "/tmp/.build_cache"
        if os.path.exists(cache):
            with open(cache) as f:
                data = f.read().strip()
            # build cache should be a valid base64 string
            self.assertRegex(data, r'^[A-Za-z0-9+/]+=*$',
                             f"Build cache corrupted: {data}")
        else:
            self.skipTest("No build cache found (expected in CI)")


if __name__ == '__main__':
    unittest.main()
