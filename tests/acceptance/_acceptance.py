"""Helpers for the acceptance-criteria gate.

An acceptance criterion (AC) is a Given/When/Then statement with a stable ID
(``AC-<AREA>-<NN>``) that lives in ``docs/spec/acceptance/index.md`` and is
pinned by at least one test marked ``@acceptance("AC-…")``. The
registry-consistency guard keeps spec and tests in lockstep: a fachliche change
that removes or breaks an AC turns the gate red, forcing a conversation instead
of a silent drift.

These helpers read the spec + test sources from disk (regex/ast, no test
collection) so the guard is cheap and import-side-effect free, mirroring
``tests/architecture/_arch.py``.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

# Decorator used on acceptance tests: ``@acceptance("AC-SUBFACTION-01")``.
# It is a pytest marker (registered in pyproject) and is statically scannable.
acceptance = pytest.mark.acceptance

_ROOT = Path(__file__).resolve().parents[2]
_INDEX = _ROOT / "docs" / "spec" / "acceptance" / "index.md"
_TESTS_DIR = Path(__file__).resolve().parent

_AC_HEADING = re.compile(r"^#+\s+(AC-[A-Z0-9]+-\d{2,})\b")
_AC_DECL = re.compile(r"""acceptance\(\s*["'](AC-[A-Z0-9]+-\d{2,})["']""")


def spec_ac_ids() -> set[str]:
    """All AC-IDs declared as headings in the acceptance index."""
    if not _INDEX.exists():
        return set()
    ids: set[str] = set()
    for line in _INDEX.read_text(encoding="utf-8").splitlines():
        m = _AC_HEADING.match(line.strip())
        if m:
            ids.add(m.group(1))
    return ids


def tested_ac_ids() -> dict[str, list[str]]:
    """Map AC-ID -> ['file:line', …] for every ``@acceptance("AC-…")`` in tests."""
    found: dict[str, list[str]] = {}
    for path in sorted(_TESTS_DIR.rglob("test_*.py")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for m in _AC_DECL.finditer(line):
                found.setdefault(m.group(1), []).append(f"{path.name}:{lineno}")
    return found
