"""Exchange rate conversion utilities."""

def convert(amount, src, dst):
    if src == dst:
        return amount
    raise ValueError(f"Conversion from {src} to {dst} is not supported offline.")

def fmt(amount, cur="USD"):
    s = {"USD": "$", "EUR": "\u20ac", "GBP": "\u00a3", "JPY": "\u00a5"}.get(cur, cur + " ")
    return f"{s}{amount:,.2f}"
