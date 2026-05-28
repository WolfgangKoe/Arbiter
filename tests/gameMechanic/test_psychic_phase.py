"""Tests for psychicPhase.py — Ziel 4f: pure helper functions.

Covers docs/spec/processes.md P-12 (Psychic Phase).
Tests verify: has_psyker, can_deny, is_perils, smite_damage_die, deny_succeeds.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic.psychicPhase import (
    can_deny,
    deny_succeeds,
    has_psyker,
    is_perils,
    smite_damage_die,
)

# ---------------------------------------------------------------------------
# Minimal Unit stub (only fields used by the pure functions)
# ---------------------------------------------------------------------------


@dataclass
class _Unit:
    keywords: list[str] = field(default_factory=list)
    rules: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# has_psyker
# ---------------------------------------------------------------------------


class TestHasPsyker:
    def test_has_psyker_true(self):
        units = [_Unit(keywords=["Orks", "PSYKER", "Infantry"])]
        assert has_psyker(units) is True

    def test_has_psyker_keyword_case_insensitive(self):
        # YAML may store as "Psyker" — must still match
        units = [_Unit(keywords=["Orks", "Psyker"])]
        assert has_psyker(units) is True

    def test_has_psyker_false(self):
        units = [_Unit(keywords=["Orks", "Infantry"]), _Unit(keywords=["Vehicle"])]
        assert has_psyker(units) is False

    def test_has_psyker_empty_list(self):
        assert has_psyker([]) is False


# ---------------------------------------------------------------------------
# can_deny
# ---------------------------------------------------------------------------


class TestCanDeny:
    def test_can_deny_via_psyker_keyword(self):
        units = [_Unit(keywords=["PSYKER"])]
        assert can_deny(units) is True

    def test_can_deny_via_gloom_prism(self):
        # Canoptek Spyder has no PSYKER keyword — only gloom_prism rule
        units = [_Unit(keywords=["Vehicle", "Canoptek Spyder"], rules=["gloom_prism"])]
        assert can_deny(units) is True

    def test_can_deny_neither(self):
        units = [_Unit(keywords=["Infantry"], rules=[])]
        assert can_deny(units) is False

    def test_can_deny_empty_list(self):
        assert can_deny([]) is False

    def test_can_deny_mixed_army_one_psyker(self):
        units = [_Unit(keywords=["Infantry"]), _Unit(keywords=["PSYKER"])]
        assert can_deny(units) is True


# ---------------------------------------------------------------------------
# is_perils
# ---------------------------------------------------------------------------


class TestIsPerils:
    def test_is_perils_on_2(self):
        assert is_perils(2) is True

    def test_is_perils_on_12(self):
        assert is_perils(12) is True

    def test_is_perils_false_5(self):
        assert is_perils(5) is False

    def test_is_perils_false_10(self):
        assert is_perils(10) is False

    def test_is_perils_false_11(self):
        assert is_perils(11) is False


# ---------------------------------------------------------------------------
# smite_damage_die
# ---------------------------------------------------------------------------


class TestSmiteDamageDie:
    def test_w3_on_5(self):
        assert smite_damage_die(5) == "W3"

    def test_w3_on_10(self):
        assert smite_damage_die(10) == "W3"

    def test_w6_on_11(self):
        assert smite_damage_die(11) == "W6"

    def test_w6_on_12(self):
        assert smite_damage_die(12) == "W6"


# ---------------------------------------------------------------------------
# deny_succeeds
# ---------------------------------------------------------------------------


class TestDenySucceeds:
    def test_deny_succeeds_greater(self):
        assert deny_succeeds(8, 9) is True

    def test_deny_fails_equal(self):
        # Must be strictly greater — equal is NOT enough
        assert deny_succeeds(8, 8) is False

    def test_deny_fails_lower(self):
        assert deny_succeeds(8, 7) is False

    def test_deny_barely_succeeds(self):
        assert deny_succeeds(7, 8) is True
