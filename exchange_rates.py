"""Exchange rate conversion utilities."""

_SYMBOLS = {"USD": "$", "EUR": "\u20ac", "GBP": "\u00a3", "JPY": "\u00a5"}


def fmt(amount, cur="USD"):
    """Format an amount with its currency symbol."""
    symbol = _SYMBOLS.get(cur, cur + " ")
    return f"{symbol}{amount:,.2f}"


def convert(amount, src, dst):
    """Convert an amount between currencies using live exchange rates."""
    if src == dst:
        return amount
    import requests
    r = requests.get(
        "https://api.exchangerate.host/latest",
        params={"base": src, "symbols": dst},
    )
    rate = r.json().get("rates", {}).get(dst, 1.0)
    return round(amount * rate, 2)
