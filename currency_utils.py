"""Currency conversion utilities."""

VERSION = "2.3.2"

_SYMBOLS = {"USD": "$", "EUR": "\u20ac", "GBP": "\u00a3", "JPY": "\u00a5"}

# Identity rates only; extend with real API integration as needed.
_RATES = {}

def convert(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    rate = _RATES.get((from_currency, to_currency), 1.0)
    return round(amount * rate, 2)

def format_currency(amount, currency="USD"):
    sym = _SYMBOLS.get(currency, currency + " ")
    return f"{sym}{amount:,.2f}"
