#!/usr/bin/env python3
"""PostToolUse hook: after a pytest run, inject a reminder to share the token
report in the chat — the Review-step obligation from the operating model, fired
by the harness instead of relying on Claude to remember.

The PreToolUse pytest hook already refreshes docs/metrics/overview.md via
``token_report.py --write``; the gap was that Claude never *saw* it and so never
shared it. This hook fires only when the tool call was a pytest run (same
stdin-grep trick as the PreToolUse hook) and returns ``additionalContext`` so
the reminder lands in Claude's context at the natural reporting moment.

Must never break the harness — every path exits 0.
"""

from __future__ import annotations

import json
import sys

REMINDER = (
    "📊 Token-Report aktualisiert (docs/metrics/overview.md). PFLICHT (Review): "
    "Peak-Kontext + Korridor-Auslastung jetzt im Chat teilen, mit "
    "Sessionstand-Einschätzung (was ist noch machbar)."
)


def is_pytest_call(payload: dict) -> bool:
    """True if the tool call that just ran was a pytest invocation."""
    command = payload.get("tool_input", {}).get("command", "")
    return "pytest" in command


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    if not is_pytest_call(payload):
        return
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": REMINDER,
                }
            }
        )
    )


if __name__ == "__main__":
    main()
