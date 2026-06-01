#!/usr/bin/env python
"""Generate one FinRobot text section from existing analysis outputs."""

from __future__ import annotations

import argparse
import configparser
import os
import sys
from pathlib import Path

import pandas as pd


FINROBOT_SRC = Path("/Users/qc/Desktop/FinRobot/finrobot_equity/core/src")
sys.path.insert(0, str(FINROBOT_SRC))

from modules.text_generator_agents import generate_text_section  # noqa: E402


def read_csv_if_exists(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    return pd.read_csv(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis-dir", required=True)
    parser.add_argument("--config-file", required=True)
    parser.add_argument("--company-ticker", required=True)
    parser.add_argument("--company-name", required=True)
    parser.add_argument("--text-type", required=True)
    parser.add_argument("--output-file", required=True)
    parser.add_argument("--kimi-mode", choices=["thinking", "instant"], default="thinking")
    parser.add_argument("--kimi-max-tokens", default="8192")
    args = parser.parse_args()

    os.environ["FINROBOT_KIMI_MODE"] = args.kimi_mode
    os.environ["FINROBOT_KIMI_MAX_TOKENS"] = args.kimi_max_tokens

    analysis_dir = Path(args.analysis_dir)
    config = configparser.ConfigParser()
    config.read(args.config_file)

    data_for_text_gen = {
        "financial_metrics": read_csv_if_exists(analysis_dir / "financial_metrics_and_forecasts.csv"),
        "peer_ebitda": read_csv_if_exists(analysis_dir / "peer_ebitda_comparison.csv"),
        "peer_ev_ebitda": read_csv_if_exists(analysis_dir / "peer_ev_ebitda_comparison.csv"),
        "company_news": [],
        "enhanced_news": None,
        "retail_sentiment": None,
        "sensitivity_analysis": None,
        "catalyst_analysis": None,
    }

    text = generate_text_section(
        data_for_text_gen,
        args.text_type,
        config.get("API_KEYS", "openai_api_key"),
        args.company_name,
        args.company_ticker,
        base_url=config.get("API_KEYS", "openai_base_url", fallback=None),
        model=config.get("API_KEYS", "openai_model", fallback=None),
    )

    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    print(f"wrote {output_path} ({len(text.split())} words)")


if __name__ == "__main__":
    main()

