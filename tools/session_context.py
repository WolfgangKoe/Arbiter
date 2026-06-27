#!/usr/bin/env python3
"""UserPromptSubmit hook: surface the live context-window size each turn and
*escalate* at the corridor thresholds — the Kontext-Korridor-Event from the
operating model, fired by the harness instead of relying on Claude to remember.

Surfaces the number the 150k corridor bounds, between pytest runs (which only
refresh docs/metrics/overview.md). Must never fail — a non-zero UserPromptSubmit
hook blocks prompt submission — so every path exits 0.

The context window per turn = input_tokens + cache_creation_input_tokens +
cache_read_input_tokens of the last assistant ``usage`` (CLAUDE.md formula). The
usage object nests sub-objects (``server_tool_use``, ``cache_creation``,
``iterations``), so a ``"usage":{[^}]*}`` grep truncates — we parse the whole
last usage-bearing line as JSON and read its top-level fields.

Three tiers (CLAUDE.md corridor < 150k, wind-down ~135k):

* < 135k  — neutral gauge.
* >= 135k — warn + stop directive: end the session in order (handoff + commit),
            do not start new work.
"""

from __future__ import annotations

import json
import sys

WARN_THRESHOLD = 135_000
STOP_THRESHOLD = 135_000


def gauge_message(total: int) -> str:
    """Return the context line for ``total`` tokens, escalating at thresholds.

    Pure function so the tiering is unit-testable without a transcript.
    """
    k = round(total / 1000)
    if total >= STOP_THRESHOLD:
        return (
            f"⛔ KONTEXT-KORRIDOR ERREICHT (~{k}k >= 135k). Wind-down JETZT: "
            "Review→Retro→Abschluss, Artefakte aktualisieren, committen — "
            "KEINE neue Arbeit beginnen, nicht in die >150k-Zone laufen."
        )
    if total >= WARN_THRESHOLD:
        return (
            f"⚠️ Kontext ~{k}k — Korridor (135k) naht. Retro jetzt vorab "
            "ankündigen und Wind-down vorbereiten; nur noch kleine Tasks."
        )
    return f"Session context: ~{k}k tokens (corridor <150k; wind-down ~135k)"


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
            print(gauge_message(total))
            return
    except Exception:
        return  # never break prompt submission


if __name__ == "__main__":
    main()
