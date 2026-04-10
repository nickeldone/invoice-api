"""Currency conversion utilities."""

VERSION = "2.3.2"

_SYMBOLS = {"USD": "$", "EUR": "\u20ac", "GBP": "\u00a3", "JPY": "\u00a5"}

def convert(amount, from_currency, to_currency):
    """Convert amount between currencies. Identity conversion is always exact."""
    if from_currency == to_currency:
        return amount
    raise NotImplementedError(
        f"Live conversion from {from_currency} to {to_currency} requires an external API key."
    )

def format_currency(amount, currency="USD"):
    """Format an amount with the currency symbol."""
    sym = _SYMBOLS.get(currency, currency + " ")
    return f"{sym}{amount:,.2f}"
