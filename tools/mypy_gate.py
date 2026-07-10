#!/usr/bin/env python3
"""CI gate: freeze the mypy error count and only let it shrink.

`pyproject.toml` configures `[tool.mypy] strict = true`, but until this gate
existed the CI step ran with `continue-on-error: true` ("informational") —
the error count could grow unnoticed (127 at the 2026-06-11 audit, ~136 by
2026-07-05). This mirrors the repo's other debt ledgers (coverage
`fail_under`, INV-4b `_vocab.py`): the baseline below is a **debt number**,
not a target — shrinking it is separate follow-up work (see
`docs/spec/architecture_invariants.md`).

Ratchet, both directions (INV-4b pattern — shrinking gets locked in too):

* measured N > BASELINE → exit 1, "new errors introduced".
* measured N < BASELINE → exit 1, "error count shrank — lower BASELINE in
  the same commit".
* measured N == BASELINE → exit 0.

Deliberately a standalone script, not a pytest test: mypy takes ~20-30s and
the local full suite (`pytest --tb=short`) runs many times per session — it
must not get slower.
"""

from __future__ import annotations

import re
import subprocess
import sys

# Ratchet: only ever lower this number, never raise it. Lowering it (because
# the measured count shrank) must happen in the same commit as the code
# change that caused the shrink.
BASELINE = 62

_COUNT_RE = re.compile(r"Found (\d+) errors? in \d+ files?")
_SUCCESS_RE = re.compile(r"Success: no issues found")


def parse_error_count(mypy_output: str) -> int:
    """Parse the error count from the last non-empty line of ``mypy`` output.

    Raises ``ValueError`` if the output doesn't match a known mypy summary
    line, so a crashed/misconfigured mypy run fails loudly instead of being
    silently read as 0 errors.
    """
    lines = [line for line in mypy_output.splitlines() if line.strip()]
    if not lines:
        raise ValueError("mypy produced no output")
    last_line = lines[-1]

    if _SUCCESS_RE.search(last_line):
        return 0

    match = _COUNT_RE.search(last_line)
    if not match:
        raise ValueError(f"unrecognized mypy summary line: {last_line!r}")
    return int(match.group(1))


def main() -> int:
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "src/"],
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr

    try:
        count = parse_error_count(output)
    except ValueError as exc:
        print(f"mypy_gate: could not parse mypy output ({exc})")
        print("\n".join(output.splitlines()[-40:]))
        return 1

    if count > BASELINE:
        print(
            f"mypy_gate: {count} errors > baseline {BASELINE} — "
            f"{count - BASELINE} new error(s) introduced. Fix the new "
            "errors; do not raise BASELINE."
        )
        print("\n".join(output.splitlines()[-40:]))
        return 1

    if count < BASELINE:
        print(
            f"mypy_gate: error count shrank ({count} < baseline {BASELINE}) — "
            f"lower BASELINE in tools/mypy_gate.py to {count} in this commit."
        )
        return 1

    print(f"mypy_gate: {count} errors == baseline {BASELINE} — OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
