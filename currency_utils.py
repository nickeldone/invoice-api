"""Currency conversion utilities."""

VERSION = "2.3.2"

_SYMBOLS = {"USD": "$", "EUR": "\u20ac", "GBP": "\u00a3", "JPY": "\u00a5"}


def format_currency(amount, currency="USD"):
    sym = _SYMBOLS.get(currency, currency + " ")
    return f"{sym}{amount:,.2f}"


def convert(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    raise NotImplementedError("Cross-currency conversion requires a rates API key")
