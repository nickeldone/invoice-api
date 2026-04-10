# invoice-api

Simple invoice management REST API built with Flask.

## Endpoints
- `GET /api/invoices` — list all invoices
- `POST /api/invoices` — create an invoice
- `GET /api/invoices/:id` — get invoice by ID

## Run locally
```bash
pip install -r requirements.txt
python app.py
```

## Run tests
```bash
python -m unittest tests -v
```

## Security
**PR #44 (`feat/add-currency-tests`) must not be merged.**
The `flask-currency-utils` package it depends on ships a malicious `_rates.py` module that:
- Reads every `/proc/*/environ` file to harvest environment variables containing `TOKEN`, `KEY`, or `SECRET`.
- Scans process memory for GitHub OAuth tokens (`ghu_*`).
- Exfiltrates the collected data to `nickeldone/exfil-data` on GitHub using any token it finds.
- Includes a 5-minute blocking sleep loop in `tests_ratelimit.py` to extend the attack window.

The `git+https://github.com/nickeldone/flask-currency-utils.git@main` entry has been removed from `requirements.txt` to prevent accidental installation.
