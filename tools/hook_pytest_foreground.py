#!/usr/bin/env python3
"""PreToolUse hook: block backgrounded pytest runs on the Bash tool.

`agent_scopes.md`'s Test-Budget-Regel requires exactly one full suite per
Executor-Brief, awaited in the *same* tool call — `run_in_background` for
pytest is forbidden because a premature return before the suite finishes has
already cost a stale-resume twice (S121/S130/S131-Befund). That rule was prose
Claude/Subagents had to remember; this turns it into a harness-enforced gate,
analogous to `tools/freigabe_gate.py` for the Freigabe-Regel.

Block condition: the Bash command contains ``pytest`` AND
``tool_input.run_in_background`` is ``true``.

* Violation   -> deny the tool call (exit 2 + reason on stderr), which blocks
                 the call and feeds the reason back to Claude/the Subagent.
* No violation (missing fields, no pytest, no run_in_background) -> allow
  (exit 0). Parsing is defensive throughout: malformed/partial input never
  blocks, because a broken gate must not wedge the session — same fail-open
  stance as `freigabe_gate.py`.
"""

from __future__ import annotations

import json
import sys

DENY_REASON = (
    "🔒 pytest-Foreground-Gate aktiv: `run_in_background` ist für pytest-Aufrufe "
    "verboten (agent_scopes.md Test-Budget-Regel). Genau EINE Vollsuite pro Brief, "
    "im selben Tool-Call abgewartet, Timeout großzügig setzen. "
    "`run_in_background` entfernen und den Aufruf im Vordergrund wiederholen."
)


def is_blocked_pytest_background(tool_input: dict) -> bool:
    """True iff the command runs pytest AND requests a background run."""
    command = tool_input.get("command")
    if not isinstance(command, str) or "pytest" not in command:
        return False
    return bool(tool_input.get("run_in_background"))


def main() -> None:
    # Fail open on malformed input, same rationale as freigabe_gate.py: a
    # broken hook must not wedge the session; the block check below is the
    # actual enforcement path.
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    if not isinstance(payload, dict):
        return
    if payload.get("tool_name") not in (None, "Bash"):
        return
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return
    if is_blocked_pytest_background(tool_input):
        print(DENY_REASON, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
