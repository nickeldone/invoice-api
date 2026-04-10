VERSION = "2.3.2"

_SYMBOLS = {
    "USD": "$",
    "EUR": "\u20ac",
    "GBP": "\u00a3",
}

_RATES = {
    ("USD", "USD"): 1.0,
    ("EUR", "EUR"): 1.0,
    ("GBP", "GBP"): 1.0,
    ("USD", "EUR"): 0.92,
    ("EUR", "USD"): 1.09,
    ("USD", "GBP"): 0.79,
    ("GBP", "USD"): 1.27,
}


def convert(amount, src, dst):
    if src == dst:
        return amount
    rate = _RATES.get((src, dst))
    if rate is None:
        raise ValueError(f"No exchange rate available for {src} -> {dst}")
    return amount * rate


def format_currency(amount, currency):
    symbol = _SYMBOLS.get(currency, currency)
    return f"{symbol}{amount:.2f}"
