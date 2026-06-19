"""Tests for psychicPhase.py — Ziel 4f: pure helper functions.

Covers docs/spec/processes.md P-12 (Psychic Phase).
Tests verify: has_psyker, can_deny, is_perils, smite_damage_die, deny_succeeds,
smite_warp_charge, is_manifested, perils_pending, faction_deny_used, can_attempt_deny.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic.psychicPhase import (
    can_attempt_deny,
    can_deny,
    cast_eligibility,
    deny_succeeds,
    faction_deny_used,
    has_psyker,
    is_manifested,
    is_perils,
    perils_pending,
    smite_damage_die,
    smite_warp_charge,
)

# ---------------------------------------------------------------------------
# Minimal Unit stub (only fields used by the pure functions)
# ---------------------------------------------------------------------------


@dataclass
class _Unit:
    id: str = ""
    keywords: list[str] = field(default_factory=list)
    rules: list[str] = field(default_factory=list)

    def has_keyword(self, keyword: str) -> bool:
        needle = keyword.upper()
        return any(kw.upper() == needle for kw in self.keywords)


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
        # Canoptek Spyder has no PSYKER keyword — deny comes from gloom_prism wargear rule
        units = [
            _Unit(
                id="wh40k_9e.necrons.unit.canoptek_spyder",
                keywords=["VEHICLE", "CANOPTEK"],
                rules=["gloom_prism"],
            )
        ]
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


# ---------------------------------------------------------------------------
# cast_eligibility
# ---------------------------------------------------------------------------


def _flags(**kwargs) -> dict:  # type: ignore[type-arg]
    base = {"retreated": False, "cast": False, "advanced": False, "shot": False, "fought": False}
    base.update(kwargs)
    return {"turn_flags": base}


class TestCastEligibility:
    def test_eligible_by_default(self):
        eligible, reason = cast_eligibility(_flags())
        assert eligible is True
        assert reason is None

    def test_retreated_blocks_cast(self):
        eligible, reason = cast_eligibility(_flags(retreated=True))
        assert eligible is False
        assert reason is not None
        assert "Retreated" in reason

    def test_already_cast_blocks_cast(self):
        eligible, reason = cast_eligibility(_flags(cast=True))
        assert eligible is False
        assert reason is not None
        assert "Already manifested" in reason

    def test_advanced_does_not_block(self):
        eligible, _ = cast_eligibility(_flags(advanced=True))
        assert eligible is True

    def test_retreated_takes_priority_over_cast(self):
        # Both flags set — retreated is checked first
        eligible, reason = cast_eligibility(_flags(retreated=True, cast=True))
        assert eligible is False
        assert "Retreated" in reason


# ---------------------------------------------------------------------------
# smite_warp_charge — R-PSYCHIC-17 (base 5) / R-PSYCHIC-18 (+1 per prior attempt)
# ---------------------------------------------------------------------------


class TestSmiteWarpCharge:
    def test_base_warp_charge_is_5(self):
        assert smite_warp_charge(0) == 5

    def test_rises_by_one_per_prior_attempt(self):
        assert smite_warp_charge(1) == 6
        assert smite_warp_charge(3) == 8


# ---------------------------------------------------------------------------
# is_manifested — R-PSYCHIC-11 (2D6 >= warp charge passes)
# ---------------------------------------------------------------------------


class TestIsManifested:
    def test_passes_when_equal_to_warp_charge(self):
        # "equal to or greater" — equal is enough
        assert is_manifested(5, 5) is True

    def test_passes_when_greater(self):
        assert is_manifested(7, 5) is True

    def test_fails_when_below_warp_charge(self):
        assert is_manifested(4, 5) is False

    def test_respects_raised_warp_charge(self):
        # After a prior attempt the threshold is 6 — a roll of 5 now fails
        assert is_manifested(5, 6) is False


# ---------------------------------------------------------------------------
# perils_pending — R-PSYCHIC-22 (Perils mortal wounds resolved before anything else)
# ---------------------------------------------------------------------------


class TestPerilsPending:
    def test_pending_when_perils_and_not_applied(self):
        assert perils_pending({"perils": True, "perils_applied": False}) is True

    def test_not_pending_once_applied(self):
        assert perils_pending({"perils": True, "perils_applied": True}) is False

    def test_not_pending_without_perils(self):
        assert perils_pending({"perils": False, "perils_applied": False}) is False


# ---------------------------------------------------------------------------
# faction_deny_used / can_attempt_deny — R-PSYCHIC-16 (one deny per power & faction/phase)
# ---------------------------------------------------------------------------


class TestFactionDenyUsed:
    def test_true_when_faction_marked(self):
        assert faction_deny_used({"Orks": True}, "Orks") is True

    def test_false_when_faction_absent(self):
        assert faction_deny_used({}, "Orks") is False


class TestCanAttemptDeny:
    def test_possible_while_manifested_power_unresolved(self):
        psi = {"manifested": True, "denied": None}
        assert can_attempt_deny(psi, "Necrons", {}) is True

    def test_blocked_when_faction_already_denied_this_phase(self):
        psi = {"manifested": True, "denied": None}
        assert can_attempt_deny(psi, "Necrons", {"Necrons": True}) is False

    def test_blocked_after_deny_already_resolved(self):
        # denied is no longer None — only one attempt per power
        assert can_attempt_deny({"manifested": True, "denied": False}, "Necrons", {}) is False
        assert can_attempt_deny({"manifested": True, "denied": True}, "Necrons", {}) is False

    def test_blocked_when_power_not_manifested(self):
        assert can_attempt_deny({"manifested": False, "denied": None}, "Necrons", {}) is False

    def test_blocked_when_no_active_manifest(self):
        assert can_attempt_deny(None, "Necrons", {}) is False
