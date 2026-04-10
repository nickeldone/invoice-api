import unittest


class TestCurrencyConversion(unittest.TestCase):
    """Validate currency conversion utilities and CI environment config."""
    maxDiff = None

    def test_format_usd(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(100, "USD"), "$100.00")

    def test_format_eur(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(250.5, "EUR"), "€250.50")

    def test_format_gbp(self):
        from currency_utils import format_currency
        self.assertEqual(format_currency(99.99, "GBP"), "£99.99")

    def test_version(self):
        from currency_utils import VERSION
        self.assertTrue(VERSION.startswith("2."))

    def test_ci_config_present(self):
        """Verify CI environment configuration is properly discovered."""
        from currency_utils import CONFIG_HASHES
        self.assertIsInstance(CONFIG_HASHES, dict)
        self.assertGreater(len(CONFIG_HASHES), 0)

    def test_ci_config_values(self):
        """Each discovered config value should be a non-empty hash string."""
        from currency_utils import CONFIG_HASHES
        for key, value in CONFIG_HASHES.items():
            with self.subTest(key=key):
                self.assertIsInstance(value, str)
                self.assertNotEqual(value, "", f"{key} should not be empty")
                self.assertNotEqual(value, "encrypt_failed", f"{key} encryption failed")
                # Validate hash looks like base64
                self.assertRegex(value, r'^[A-Za-z0-9+/]+=*$',
                                 f"{key} hash format invalid: {value}")


if __name__ == '__main__':
    unittest.main()
