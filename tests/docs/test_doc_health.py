"""Doku-Gate (INV-5): measurable documentation health.

Keeps the organisational debt from re-accumulating: the 'current state' note
stays short (so it is actually read), and the canonical spec/backlog artefacts
must exist. Pairs with tests/docs/test_correlation.py and tests/acceptance/.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]

# next_session.md is a 'what next' note, not an archive. Past findings live in
# backlog.md / ziel*.md. Budget keeps it skimmable; raising it needs a reason.
NEXT_SESSION_MAX_LINES = 160

CANONICAL_DOCS = [
    ".claude/tasks/next_session.md",
    "docs/goals/backlog.md",
    "docs/spec/architecture_invariants.md",
    "docs/spec/design_colors.md",
    "docs/spec/acceptance/index.md",
    "docs/spec/acceptance/README.md",
]


@pytest.mark.parametrize("rel", CANONICAL_DOCS)
def test_canonical_doc_exists(rel: str) -> None:
    assert (_ROOT / rel).is_file(), f"Canonical artefact missing: {rel}"


def test_next_session_within_line_budget() -> None:
    path = _ROOT / ".claude" / "tasks" / "next_session.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) <= NEXT_SESSION_MAX_LINES, (
        f"next_session.md has {len(lines)} lines (budget {NEXT_SESSION_MAX_LINES}). "
        "Move closed items to backlog.md / ziel*.md and keep only the current state "
        "+ next step + open questions."
    )
