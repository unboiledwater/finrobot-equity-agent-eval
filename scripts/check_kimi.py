#!/usr/bin/env python
"""Minimal Kimi/OpenAI-compatible smoke test using the private config file."""

from __future__ import annotations

import argparse
import configparser

from openai import OpenAI


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", required=True)
    parser.add_argument("--mode", choices=["instant", "thinking"], default="instant")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config_file)

    client = OpenAI(
        api_key=config.get("API_KEYS", "openai_api_key"),
        base_url=config.get("API_KEYS", "openai_base_url"),
    )
    if args.mode == "thinking":
        temperature = 1.0
        max_tokens = 32768
        extra_body = {"thinking": {"type": "enabled"}}
    else:
        temperature = 0.6
        max_tokens = 256
        extra_body = {"thinking": {"type": "disabled"}}

    response = client.chat.completions.create(
        model=config.get("API_KEYS", "openai_model"),
        messages=[{"role": "user", "content": "Say exactly: kimi smoke ok"}],
        max_tokens=max_tokens,
        temperature=temperature,
        extra_body=extra_body,
    )
    print("content:", repr(response.choices[0].message.content))
    print("finish_reason:", response.choices[0].finish_reason)
    print("model:", response.model)


if __name__ == "__main__":
    main()
