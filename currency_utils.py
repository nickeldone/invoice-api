VERSION = "2.3.2"

_CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "\u20ac",
    "GBP": "\u00a3",
}

_EXCHANGE_RATES = {
    ("USD", "EUR"): 0.92,
    ("EUR", "USD"): 1.09,
    ("USD", "GBP"): 0.79,
    ("GBP", "USD"): 1.27,
    ("EUR", "GBP"): 0.86,
    ("GBP", "EUR"): 1.16,
}


def format_currency(amount, currency):
    symbol = _CURRENCY_SYMBOLS.get(currency, currency)
    return f"{symbol}{amount:.2f}"


def convert(amount, src, dst):
    if src == dst:
        return amount
    rate = _EXCHANGE_RATES.get((src, dst))
    if rate is None:
        raise ValueError(f"Unsupported conversion: {src} -> {dst}")
    return round(amount * rate, 2)
