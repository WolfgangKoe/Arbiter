#!/usr/bin/env python3
"""UserPromptSubmit hook: print the live context-window size each turn.

Surfaces the number the 150k corridor bounds, between pytest runs (which only
refresh docs/metrics/overview.md). Must never fail — a non-zero UserPromptSubmit
hook blocks prompt submission — so every path exits 0.

The context window per turn = input_tokens + cache_creation_input_tokens +
cache_read_input_tokens of the last assistant ``usage`` (CLAUDE.md formula). The
usage object nests sub-objects (``server_tool_use``, ``cache_creation``,
``iterations``), so a ``"usage":{[^}]*}`` grep truncates — we parse the whole
last usage-bearing line as JSON and read its top-level fields.
"""

from __future__ import annotations

import json
import sys


def main() -> None:
    try:
        payload = json.load(sys.stdin)
        path = payload.get("transcript_path", "")
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
        for line in reversed(lines):
            if '"usage":' not in line:
                continue
            usage = json.loads(line).get("message", {}).get("usage")
            if not usage:
                continue
            total = (
                usage.get("input_tokens", 0)
                + usage.get("cache_creation_input_tokens", 0)
                + usage.get("cache_read_input_tokens", 0)
            )
            print(
                f"Session context: ~{round(total / 1000)}k tokens "
                "(corridor <150k; wind-down ~135k)"
            )
            return
    except Exception:
        return  # never break prompt submission


if __name__ == "__main__":
    main()
