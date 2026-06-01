#!/usr/bin/env python
"""Check FMP endpoint access without printing API secrets."""

from __future__ import annotations

import argparse
import configparser
from urllib.parse import urlparse

import requests


ENDPOINTS = [
    ("profile", "https://financialmodelingprep.com/api/v3/profile/{ticker}"),
    ("income_statement", "https://financialmodelingprep.com/api/v3/income-statement/{ticker}"),
    ("balance_sheet", "https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}"),
    ("cash_flow", "https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}"),
    ("ratios", "https://financialmodelingprep.com/api/v3/ratios/{ticker}"),
    ("key_metrics", "https://financialmodelingprep.com/api/v3/key-metrics/{ticker}"),
    ("stock_news", "https://financialmodelingprep.com/api/v3/stock_news"),
]

STABLE_ENDPOINTS = [
    ("stable_profile", "https://financialmodelingprep.com/stable/profile", {"symbol": "{ticker}"}),
    ("stable_income_statement", "https://financialmodelingprep.com/stable/income-statement", {"symbol": "{ticker}", "period": "annual", "limit": "1"}),
    ("stable_balance_sheet", "https://financialmodelingprep.com/stable/balance-sheet-statement", {"symbol": "{ticker}", "period": "annual", "limit": "1"}),
    ("stable_cash_flow", "https://financialmodelingprep.com/stable/cash-flow-statement", {"symbol": "{ticker}", "period": "annual", "limit": "1"}),
    ("stable_ratios", "https://financialmodelingprep.com/stable/ratios", {"symbol": "{ticker}", "period": "annual", "limit": "1"}),
    ("stable_key_metrics", "https://financialmodelingprep.com/stable/key-metrics", {"symbol": "{ticker}", "period": "annual", "limit": "1"}),
    ("stable_stock_news", "https://financialmodelingprep.com/stable/news/stock", {"symbols": "{ticker}", "limit": "1"}),
]


def load_key(config_path: str) -> str:
    config = configparser.ConfigParser()
    config.read(config_path)
    return config.get("API_KEYS", "fmp_api_key")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", required=True)
    parser.add_argument("--ticker", default="NVDA")
    args = parser.parse_args()

    key = load_key(args.config_file)
    session = requests.Session()
    checks = []
    for name, template in ENDPOINTS:
        params = {"apikey": key}
        params.update({"tickers": args.ticker, "limit": "1"} if name == "stock_news" else {"period": "annual", "limit": "1"})
        checks.append((name, template.format(ticker=args.ticker), params))

    for name, url, raw_params in STABLE_ENDPOINTS:
        params = {"apikey": key}
        params.update({param: value.format(ticker=args.ticker) for param, value in raw_params.items()})
        checks.append((name, url, params))

    for name, url, params in checks:
        try:
            response = session.get(url, params=params, timeout=20)
            parsed = urlparse(response.url)
            safe_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            body = response.text.replace(key, "[REDACTED]")[:240].replace("\n", " ")
            print(f"{name}: status={response.status_code} url={safe_url} body={body}")
        except Exception as exc:
            print(f"{name}: error={type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
