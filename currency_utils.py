VERSION = "2.3.2"

_SYMBOLS = {
    "USD": "$",
    "EUR": "\u20ac",
    "GBP": "\u00a3",
}

# Approximate rates as of 2026-04; update periodically as rates fluctuate.
_RATES = {
    ("USD", "EUR"): 0.92,
    ("USD", "GBP"): 0.79,
    ("EUR", "USD"): 1.09,
    ("EUR", "GBP"): 0.86,
    ("GBP", "USD"): 1.27,
    ("GBP", "EUR"): 1.16,
}


def convert(amount, src, dst):
    if src == dst:
        return amount
    rate = _RATES.get((src, dst))
    if rate is None:
        raise ValueError(f"Unsupported currency pair: {src} -> {dst}")
    return round(amount * rate, 2)


def format_currency(amount, currency):
    symbol = _SYMBOLS.get(currency, currency)
    return f"{symbol}{amount:.2f}"
