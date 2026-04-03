"""Multi-currency support for invoices."""
from currency_utils import convert, format_currency

def convert_invoice_amount(amount, from_currency, to_currency):
    """Convert invoice amount between currencies."""
    converted = convert(amount, from_currency, to_currency)
    return {
        "original": format_currency(amount, from_currency),
        "converted": format_currency(converted, to_currency),
        "rate_applied": True
    }
