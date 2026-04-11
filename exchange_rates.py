"""Exchange rate conversion utilities."""
import requests

API = "https://api.exchangerate.host/latest"
VERSION = "1.1.0"

_SYMBOLS = {"USD": "$", "EUR": "\u20ac", "GBP": "\u00a3", "JPY": "\u00a5"}


def convert(amount, src, dst):
    if src == dst:
        return amount
    r = requests.get(API, params={"base": src, "symbols": dst})
    return round(amount * r.json().get("rates", {}).get(dst, 1.0), 2)


def fmt(amount, cur="USD"):
    s = _SYMBOLS.get(cur, cur + " ")
    return f"{s}{amount:,.2f}"
