"""Doku-Gate (INV-5): measurable documentation health.

Keeps the organisational debt from re-accumulating: the 'current state' note
stays short (so it is actually read), and the canonical spec/backlog artefacts
must exist. Pairs with tests/docs/test_correlation.py and tests/acceptance/.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]

# briefing.md is a 'what next' note, not an archive. Past findings live in
# backlog.md / ziel*.md. Budget keeps it skimmable; raising it needs a reason.
#
# Hysterese statt Schwellen-Geklingel: die harte Decke (Test rot darueber) und das
# Trim-Ziel liegen bewusst weit auseinander. Wer die Decke reisst, kuerzt nicht auf
# Decke-1, sondern auf <= TRIM_TARGET — danach waechst die Datei frei bis zur Decke.
BRIEFING_MAX_LINES = 120
BRIEFING_TRIM_TARGET = 70

CANONICAL_DOCS = [
    ".claude/tasks/briefing.md",
    "docs/goals/backlog.md",
    "docs/spec/architecture_invariants.md",
    "docs/spec/design_colors.md",
    "docs/spec/acceptance/index.md",
    "docs/spec/acceptance/README.md",
]


@pytest.mark.parametrize("rel", CANONICAL_DOCS)
def test_canonical_doc_exists(rel: str) -> None:
    assert (_ROOT / rel).is_file(), f"Canonical artefact missing: {rel}"


def test_briefing_within_line_budget() -> None:
    path = _ROOT / ".claude" / "tasks" / "briefing.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) <= BRIEFING_MAX_LINES, (
        f"briefing.md has {len(lines)} lines (Decke {BRIEFING_MAX_LINES}). "
        f"Jetzt TIEF kuerzen — auf <= {BRIEFING_TRIM_TARGET} Zeilen, nicht knapp "
        "unter die Decke. Erledigtes nach backlog.md / ziel*.md, Referenzwissen nach "
        "architecture.md / rules_insights.md / CLAUDE.md; hier nur aktueller Stand "
        "+ naechster Schritt + offene Fragen."
    )
