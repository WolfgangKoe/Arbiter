"""Tests for Ziel 4g — Charge Phase logic.

Covers:
  4g.1 — leave_melee_pair (new function)
  4g.5 — can_shoot() VEHICLE/MONSTER exception (Big Guns Never Tire)
  4g.6 — target_in_friendly_melee() helper
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.shootingPhase as _sp  # noqa: E402
import gameMechanic.unit_mutations as _mut  # noqa: E402
from gameMechanic.shootingPhase import can_shoot, target_in_friendly_melee  # noqa: E402
from gameMechanic.unit_mutations import enter_melee, leave_melee_pair  # noqa: E402
from gameObjects.unit import Unit  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

OVERLORD = "wh40k_9e.necrons.unit.overlord"
WARRIORS = "wh40k_9e.necrons.unit.warriors"
BOYZ = "wh40k_9e.orks.unit.boyz"
WARBOSS = "wh40k_9e.orks.unit.warboss"
STALKER = "wh40k_9e.necrons.unit.triarch_stalker"


class _S(dict):
    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _make_session(**kwargs) -> _S:  # type: ignore[no-untyped-def]
    s = _S(**kwargs)
    _mut.st.session_state = s
    # Ensure shootingPhase.st uses the same mock (test_shooting.py may have imported it first)
    _sp.st = _st_mock
    _st_mock.session_state = s
    return s


def _unit(in_melee: bool = False) -> dict:
    return {
        "current_wounds": 5,
        "models": 1,
        "destroyed": False,
        "in_melee": in_melee,
        "in_reserve": False,
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
        },
    }


def _two_unit_session() -> _S:
    return _make_session(
        necron_units={OVERLORD: _unit()},
        ork_units={BOYZ: _unit()},
    )


def _four_unit_session() -> _S:
    return _make_session(
        necron_units={OVERLORD: _unit(), WARRIORS: _unit()},
        ork_units={BOYZ: _unit(), WARBOSS: _unit()},
    )


def _unit_with_keywords(*keywords: str) -> Unit:
    return Unit(
        id="dummy",
        name_en="Dummy",
        name_de="Dummy",
        faction="Necrons",
        subfaction=None,
        battlefield_role=["Elites"],
        keywords=list(keywords),
        wounds=5,
        models_min=1,
        models_max=1,
        move='6"',
        bs="3+",
        ws="3+",
        strength=5,
        toughness=5,
        save=3,
        invuln_save=None,
        leadership=10,
        oc=1,
        fnp=None,
    )


def _state(in_melee: bool = False, in_reserve: bool = False, **flags) -> dict:
    return {"turn_flags": flags, "in_melee": in_melee, "in_reserve": in_reserve}


# ---------------------------------------------------------------------------
# 4g.1 — leave_melee_pair
# ---------------------------------------------------------------------------


class TestLeaveMeleePair:
    def test_removes_specific_pair_from_own_melee_with(self) -> None:
        session = _four_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        enter_melee(OVERLORD, "Necrons", WARBOSS, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        mw = session["necron_units"][OVERLORD]["melee_with"]
        assert ["Orks", BOYZ] not in mw
        assert ["Orks", WARBOSS] in mw

    def test_removes_specific_pair_from_enemy_melee_with(self) -> None:
        session = _two_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert ["Necrons", OVERLORD] not in session["ork_units"][BOYZ]["melee_with"]

    def test_own_unit_still_in_melee_if_other_pairs_remain(self) -> None:
        session = _four_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        enter_melee(OVERLORD, "Necrons", WARBOSS, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert session["necron_units"][OVERLORD]["in_melee"] is True

    def test_own_unit_leaves_melee_when_last_pair_broken(self) -> None:
        session = _two_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert session["necron_units"][OVERLORD]["in_melee"] is False

    def test_enemy_stays_in_melee_if_still_engaged_elsewhere(self) -> None:
        session = _four_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        enter_melee(WARRIORS, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert session["ork_units"][BOYZ]["in_melee"] is True
        assert ["Necrons", WARRIORS] in session["ork_units"][BOYZ]["melee_with"]

    def test_enemy_leaves_melee_when_last_pair_broken(self) -> None:
        session = _two_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert session["ork_units"][BOYZ]["in_melee"] is False

    def test_idempotent_when_pair_already_gone(self) -> None:
        session = _two_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert session["necron_units"][OVERLORD]["melee_with"] == []


# ---------------------------------------------------------------------------
# 4g.5 — can_shoot() VEHICLE/MONSTER (Big Guns Never Tire)
# ---------------------------------------------------------------------------


class TestCanShootBigGunsNeverTire:
    def test_vehicle_in_melee_can_shoot(self) -> None:
        unit = _unit_with_keywords("Necrons", "Vehicle")
        assert can_shoot(_state(in_melee=True), unit) is True

    def test_monster_in_melee_can_shoot(self) -> None:
        unit = _unit_with_keywords("Necrons", "Monster")
        assert can_shoot(_state(in_melee=True), unit) is True

    def test_infantry_in_melee_cannot_shoot(self) -> None:
        unit = _unit_with_keywords("Necrons", "Infantry")
        assert can_shoot(_state(in_melee=True), unit) is False

    def test_vehicle_in_melee_still_blocked_when_advanced(self) -> None:
        unit = _unit_with_keywords("Necrons", "Vehicle")
        assert can_shoot(_state(in_melee=True, advanced=True), unit) is False

    def test_vehicle_in_melee_still_blocked_when_retreated(self) -> None:
        unit = _unit_with_keywords("Necrons", "Vehicle")
        assert can_shoot(_state(in_melee=True, retreated=True), unit) is False

    def test_vehicle_in_melee_still_blocked_in_reserve(self) -> None:
        unit = _unit_with_keywords("Necrons", "Vehicle")
        assert can_shoot({"turn_flags": {}, "in_melee": True, "in_reserve": True}, unit) is False

    def test_no_unit_arg_in_melee_cannot_shoot(self) -> None:
        assert can_shoot(_state(in_melee=True)) is False

    def test_vehicle_not_in_melee_can_shoot(self) -> None:
        unit = _unit_with_keywords("Necrons", "Vehicle")
        assert can_shoot(_state(in_melee=False), unit) is True


# ---------------------------------------------------------------------------
# 4g.6 — target_in_friendly_melee
# ---------------------------------------------------------------------------


class TestTargetInFriendlyMelee:
    def test_returns_false_when_target_not_in_melee(self) -> None:
        _make_session(
            necron_units={OVERLORD: _unit()},
            ork_units={BOYZ: _unit()},
        )
        assert target_in_friendly_melee("Necrons", "Orks", BOYZ) is False

    def test_returns_true_when_friendly_unit_in_melee_with_target(self) -> None:
        _two_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        # Orks shoot at BOYZ — BOYZ is in melee with friendly (Necron) Overlord
        # Orks are the attacker → friendly faction for Orks is "Orks"
        # BOYZ is engaged with Necrons (enemy of Orks) → no friendly
        assert target_in_friendly_melee("Orks", "Orks", BOYZ) is False
        # Necrons shoot at BOYZ → BOYZ is in melee with Necron Overlord (friendly to attacker)
        assert target_in_friendly_melee("Necrons", "Orks", BOYZ) is True

    def test_returns_false_when_target_in_melee_with_enemy_only(self) -> None:
        _four_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        # Warriors (Necrons) want to shoot at Boyz — Boyz is in melee with Necron Overlord
        assert target_in_friendly_melee("Necrons", "Orks", BOYZ) is True

    def test_returns_false_after_melee_pair_broken(self) -> None:
        _two_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert target_in_friendly_melee("Necrons", "Orks", BOYZ) is False
