"""Pytest session hooks — debt scoreboard.

Prints a measurable debt scoreboard after every test run (next to the coverage
line), so the technical-debt trend is visible on each `pytest`. Numbers are
computed live from the gate sources, not hardcoded.

NOTE: this conftest deliberately does NOT touch `sys.modules["streamlit"]` or
import src logic modules at import time — that would perturb the per-file
streamlit-mock binding the gameMechanic tests rely on (see backlog §4). All
metric imports happen lazily inside the hook, after the test session.
"""

from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_NEXT_SESSION_BUDGET = 160  # keep in sync with tests/docs/test_doc_health.py


def _metrics() -> list[str]:
    lines: list[str] = []

    # INV-4b — faction vocabulary leaking into src/ (live scan)
    from tests.architecture._vocab import src_vocab_hits

    hits = src_vocab_hits()
    tokens = sorted({tok for _f, _l, tok, _fac in hits})
    files = {rel for rel, _l, _t, _fac in hits}
    lines.append(
        f"INV-4b Fraktions-Vokabular in src/ : {len(tokens)} Tokens, "
        f"{len(hits)} Fundstellen, {len(files)} Dateien  (Ziel: -> 0, ratchet)"
    )

    # INV-4 — faction-name allowlist entries
    from tests.architecture.test_generic_src import ALLOWLIST

    a_entries = sum(len(t) for t in ALLOWLIST.values())
    lines.append(
        f"INV-4  Namen-Allowlist             : {a_entries} Eintraege, "
        f"{len(ALLOWLIST)} Dateien  (Ziel: -> nur LEGIT)"
    )

    # INV-5 — acceptance criteria + doc budget
    from tests.acceptance._acceptance import spec_ac_ids

    next_session = _ROOT / ".claude" / "tasks" / "next_session.md"
    n_lines = len(next_session.read_text(encoding="utf-8").splitlines())
    lines.append(f"INV-5  Akzeptanzkriterien          : {len(spec_ac_ids())} AC-IDs (alle gepinnt)")
    lines.append(f"INV-5  next_session.md             : {n_lines}/{_NEXT_SESSION_BUDGET} Zeilen")
    return lines


def pytest_terminal_summary(terminalreporter, exitstatus, config) -> None:
    try:
        lines = _metrics()
    except Exception as exc:  # never let the scoreboard break the run
        terminalreporter.write_line(f"Schulden-Scoreboard nicht verfuegbar: {exc}")
        return
    terminalreporter.section("Schulden-Scoreboard (Gates)")
    for line in lines:
        terminalreporter.write_line(line)
