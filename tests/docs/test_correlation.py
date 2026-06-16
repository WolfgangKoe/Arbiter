"""Correlation gate (INV-5): documentation and guards stay cross-referenced.

Every architecture invariant documented in architecture_invariants.md must have a
guard test that cites its INV-id — otherwise a documented invariant could quietly
lose its enforcement (or a guard drift from the spec). Complements the
acceptance registry guard (spec <-> tests) in tests/acceptance/.
"""

from __future__ import annotations

import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_INVARIANTS = _ROOT / "docs" / "spec" / "architecture_invariants.md"
_GUARD_DIRS = [_ROOT / "tests" / "architecture", _ROOT / "tests" / "docs"]

_INV_ID = re.compile(r"\bINV-\d+[a-z]?\b")


def _documented_invariants() -> set[str]:
    """INV-ids that appear in the status table (table rows '| INV-x |')."""
    ids: set[str] = set()
    for line in _INVARIANTS.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("| INV-"):
            ids.update(_INV_ID.findall(line))
    return ids


def _cited_invariants() -> set[str]:
    ids: set[str] = set()
    for guard_dir in _GUARD_DIRS:
        for path in guard_dir.rglob("*.py"):
            ids.update(_INV_ID.findall(path.read_text(encoding="utf-8")))
    return ids


def test_every_documented_invariant_has_a_citing_guard() -> None:
    missing = sorted(_documented_invariants() - _cited_invariants())
    assert not missing, (
        "Invariants documented in architecture_invariants.md but cited by no guard "
        f"test (tests/architecture or tests/docs): {missing}"
    )
