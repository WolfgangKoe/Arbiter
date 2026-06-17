"""Read-only metrics for the rule-conformance catalog (docs/spec/acceptance/rules.md).

The catalog is the *Nenner* (denominator) for coverage: the set of 9E rules we
measure implementation and test coverage against. This module parses the catalog
from disk (regex, no test collection) and derives three read-only signals for the
debt scoreboard:

- coverage per rule class (A/B/C): how many catalog rules are tested,
- the ledger: rules marked ``implementiert`` but ``getestet: nein`` (a debt that
  may only shrink),
- a consistency check: every ``getestet: ja — <testname>`` names a test that
  actually exists in tests/ (catches renamed/deleted tests drifting from the spec).

These are reported, not enforced — hard-red only on explicit request. Mirrors the
disk-read, side-effect-free style of ``_acceptance.py`` and ``_arch.py``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_RULES = _ROOT / "docs" / "spec" / "acceptance" / "rules.md"
_TESTS_DIR = _ROOT / "tests"

_RULE_HEADING = re.compile(r"^###\s+(R-[A-Z0-9]+-\d{2,})\b")
_FIELD = re.compile(r"^-\s+\*\*(\w+)\*\*:\s*(.*)$")
_TESTDEF = re.compile(r"^\s*(?:async\s+)?def\s+(test_\w+)\s*\(", re.MULTILINE)


@dataclass(frozen=True)
class Rule:
    rid: str
    klasse: str  # "A" | "B" | "C"
    status: str  # "implementiert" | "offen"
    testnames: tuple[str, ...]  # from "getestet: ja — a / b"; empty if "nein"

    @property
    def implemented(self) -> bool:
        return self.status == "implementiert"

    @property
    def tested(self) -> bool:
        return bool(self.testnames)


def _parse_testnames(getestet: str) -> tuple[str, ...]:
    """'ja — test_a / test_b' -> ('test_a', 'test_b'); 'nein' -> ()."""
    if not getestet.lower().startswith("ja"):
        return ()
    _, _, rest = getestet.partition("—")
    return tuple(name.strip() for name in rest.split("/") if name.strip())


def parse_rules() -> list[Rule]:
    """All ``### R-…`` entries in rules.md as structured Rule records."""
    if not _RULES.exists():
        return []
    rules: list[Rule] = []
    rid: str | None = None
    fields: dict[str, str] = {}

    def flush() -> None:
        if rid is None:
            return
        rules.append(
            Rule(
                rid=rid,
                klasse=fields.get("klasse", "").strip(),
                status=fields.get("status", "").strip(),
                testnames=_parse_testnames(fields.get("getestet", "")),
            )
        )

    for line in _RULES.read_text(encoding="utf-8").splitlines():
        heading = _RULE_HEADING.match(line.strip())
        if heading:
            flush()
            rid, fields = heading.group(1), {}
            continue
        field = _FIELD.match(line.strip())
        if field and rid is not None:
            fields[field.group(1)] = field.group(2)
    flush()
    return rules


@dataclass(frozen=True)
class ClassCoverage:
    klasse: str
    total: int
    implemented: int
    tested: int

    @property
    def pct(self) -> int:
        """Tested share of the denominator (catalog rules in this class)."""
        return round(100 * self.tested / self.total) if self.total else 0


def coverage_by_class() -> list[ClassCoverage]:
    rules = parse_rules()
    classes = sorted({r.klasse for r in rules if r.klasse})
    out: list[ClassCoverage] = []
    for klasse in classes:
        members = [r for r in rules if r.klasse == klasse]
        out.append(
            ClassCoverage(
                klasse=klasse,
                total=len(members),
                implemented=sum(1 for r in members if r.implemented),
                tested=sum(1 for r in members if r.tested),
            )
        )
    return out


def ledger() -> list[str]:
    """Rule-IDs that are ``implementiert`` but ``getestet: nein`` (debt, ratchet)."""
    return [r.rid for r in parse_rules() if r.implemented and not r.tested]


def _known_testnames() -> set[str]:
    names: set[str] = set()
    for path in _TESTS_DIR.rglob("test_*.py"):
        names.update(_TESTDEF.findall(path.read_text(encoding="utf-8")))
    return names


def missing_testnames() -> list[tuple[str, str]]:
    """[(rule_id, testname), …] for every ``getestet: ja`` testname not found in tests/."""
    known = _known_testnames()
    out: list[tuple[str, str]] = []
    for rule in parse_rules():
        for name in rule.testnames:
            if name not in known:
                out.append((rule.rid, name))
    return out
