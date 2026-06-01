#!/usr/bin/env python
"""Fetch display metrics from FMP stable profile without printing secrets."""

from __future__ import annotations

import argparse
import configparser
import json
from pathlib import Path

import requests


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", required=True)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--output-file", required=True)
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config_file)
    key = config.get("API_KEYS", "fmp_api_key")
    response = requests.get(
        "https://financialmodelingprep.com/stable/profile",
        params={"symbol": args.ticker, "apikey": key},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    profile = data[0] if isinstance(data, list) and data else {}

    metrics = {
        "share_price": profile.get("price"),
        "market_cap_billion": (profile.get("marketCap") or 0) / 1e9 if profile.get("marketCap") else None,
        "volume_million": (profile.get("volume") or 0) / 1e6 if profile.get("volume") else None,
        "sector": profile.get("sector"),
        "industry": profile.get("industry"),
        "beta": profile.get("beta"),
        "range": profile.get("range"),
    }

    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

