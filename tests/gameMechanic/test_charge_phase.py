"""Tests for Ziel 4g — Charge Phase logic.

Covers:
  4g.1 — leave_melee_pair (new function)
  4g.5 — can_shoot() VEHICLE/MONSTER exception (Big Guns Never Tire)
  4g.6 — target_in_friendly_melee() helper
  R-CHARGE-09 — hi_eligible_units filter (CHARACTER + not in melee + not intervened)
  R-CHARGE-10 — hi_already_performed once-per-phase guard
  S137/P2-2 — _active_charge wires render_inline_command_reroll (charge roll)
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.chargePhase as cp  # noqa: E402
import gameMechanic.gameState as _gs  # noqa: E402
import gameMechanic.shootingPhase as _sp  # noqa: E402
import gameMechanic.unitMutations as _mut  # noqa: E402
from gameMechanic.chargePhase import hi_already_performed, hi_eligible_units  # noqa: E402
from gameMechanic.shootingPhase import can_shoot, target_in_friendly_melee  # noqa: E402
from gameMechanic.unitMutations import enter_melee, leave_melee_pair  # noqa: E402
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
    kwargs.setdefault("first_player", "Necrons")
    s = _S(**kwargs)
    _mut.st.session_state = s
    _gs.st.session_state = s
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
        p1_units={OVERLORD: _unit()},
        p2_units={BOYZ: _unit()},
    )


def _four_unit_session() -> _S:
    return _make_session(
        p1_units={OVERLORD: _unit(), WARRIORS: _unit()},
        p2_units={BOYZ: _unit(), WARBOSS: _unit()},
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
        power_level=4,
        move='6"',
        bs="3+",
        ws="3+",
        strength=5,
        toughness=5,
        attacks=3,
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
        mw = session["p1_units"][OVERLORD]["melee_with"]
        assert ["Orks", BOYZ] not in mw
        assert ["Orks", WARBOSS] in mw

    def test_removes_specific_pair_from_enemy_melee_with(self) -> None:
        session = _two_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert ["Necrons", OVERLORD] not in session["p2_units"][BOYZ]["melee_with"]

    def test_own_unit_still_in_melee_if_other_pairs_remain(self) -> None:
        session = _four_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        enter_melee(OVERLORD, "Necrons", WARBOSS, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert session["p1_units"][OVERLORD]["in_melee"] is True

    def test_own_unit_leaves_melee_when_last_pair_broken(self) -> None:
        session = _two_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert session["p1_units"][OVERLORD]["in_melee"] is False

    def test_enemy_stays_in_melee_if_still_engaged_elsewhere(self) -> None:
        session = _four_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        enter_melee(WARRIORS, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert session["p2_units"][BOYZ]["in_melee"] is True
        assert ["Necrons", WARRIORS] in session["p2_units"][BOYZ]["melee_with"]

    def test_enemy_leaves_melee_when_last_pair_broken(self) -> None:
        session = _two_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert session["p2_units"][BOYZ]["in_melee"] is False

    def test_idempotent_when_pair_already_gone(self) -> None:
        session = _two_unit_session()
        enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        leave_melee_pair(OVERLORD, "Necrons", BOYZ, "Orks")
        assert session["p1_units"][OVERLORD]["melee_with"] == []


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
            p1_units={OVERLORD: _unit()},
            p2_units={BOYZ: _unit()},
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


# ---------------------------------------------------------------------------
# R-CHARGE-09 — hi_eligible_units
# ---------------------------------------------------------------------------


def _make_unit_kw(*keywords: str) -> Unit:
    """Build a minimal Unit with the given keywords."""
    return Unit(
        id="dummy_hi",
        name_en="HI Unit",
        name_de="HI Unit",
        faction="Necrons",
        subfaction=None,
        battlefield_role=["HQ"],
        keywords=list(keywords),
        wounds=5,
        models_min=1,
        models_max=1,
        power_level=4,
        move='6"',
        bs="3+",
        ws="3+",
        strength=5,
        toughness=5,
        attacks=3,
        save=3,
        invuln_save=None,
        leadership=10,
        oc=1,
        fnp=None,
    )


def _hi_unit_state(
    *,
    destroyed: bool = False,
    in_melee: bool = False,
    heroic_intervened: bool = False,
) -> dict:
    return {
        "destroyed": destroyed,
        "in_melee": in_melee,
        "turn_flags": {"heroic_intervened": heroic_intervened},
    }


class TestHiEligibleUnits:
    def test_character_not_in_melee_is_eligible(self) -> None:
        unit = _make_unit_kw("CHARACTER", "INFANTRY")
        units_data = {unit.id: _hi_unit_state()}
        result = hi_eligible_units([unit], [unit.id], units_data)
        assert unit in [u for u, _ in result]

    def test_non_character_is_ineligible(self) -> None:
        """Units without CHARACTER keyword may not perform Heroic Intervention."""
        unit = _make_unit_kw("INFANTRY")
        units_data = {unit.id: _hi_unit_state()}
        result = hi_eligible_units([unit], [unit.id], units_data)
        assert unit not in [u for u, _ in result]

    def test_character_in_melee_is_ineligible(self) -> None:
        """Characters already in Engagement Range (in_melee=True) are excluded."""
        unit = _make_unit_kw("CHARACTER")
        units_data = {unit.id: _hi_unit_state(in_melee=True)}
        result = hi_eligible_units([unit], [unit.id], units_data)
        assert unit not in [u for u, _ in result]

    def test_character_destroyed_is_ineligible(self) -> None:
        unit = _make_unit_kw("CHARACTER")
        units_data = {unit.id: _hi_unit_state(destroyed=True)}
        result = hi_eligible_units([unit], [unit.id], units_data)
        assert unit not in [u for u, _ in result]

    def test_character_already_intervened_is_ineligible(self) -> None:
        """heroic_intervened flag blocks a second HI (R-CHARGE-10 guard)."""
        unit = _make_unit_kw("CHARACTER")
        units_data = {unit.id: _hi_unit_state(heroic_intervened=True)}
        result = hi_eligible_units([unit], [unit.id], units_data)
        assert unit not in [u for u, _ in result]

    def test_empty_unit_list_returns_empty(self) -> None:
        assert hi_eligible_units([], [], {}) == []

    def test_mixed_list_only_returns_eligible(self) -> None:
        char = _make_unit_kw("CHARACTER")
        char.id = "char"  # type: ignore[misc]
        infantry = _make_unit_kw("INFANTRY")
        infantry.id = "inf"  # type: ignore[misc]
        units_data = {
            "char": _hi_unit_state(),
            "inf": _hi_unit_state(),
        }
        result = hi_eligible_units([char, infantry], [char.id, infantry.id], units_data)
        assert char in [u for u, _ in result]
        assert infantry not in [u for u, _ in result]


# ---------------------------------------------------------------------------
# R-CHARGE-10 — hi_already_performed (once-per-phase guard)
# ---------------------------------------------------------------------------


class TestHiAlreadyPerformed:
    def test_returns_false_when_flag_not_set(self) -> None:
        unit_state = _hi_unit_state(heroic_intervened=False)
        assert hi_already_performed(unit_state) is False

    def test_returns_true_when_flag_set(self) -> None:
        """Once the heroic_intervened flag is True, a second HI must be blocked."""
        unit_state = _hi_unit_state(heroic_intervened=True)
        assert hi_already_performed(unit_state) is True

    def test_returns_false_when_turn_flags_absent(self) -> None:
        assert hi_already_performed({}) is False


# ---------------------------------------------------------------------------
# S137/P2-2 — _active_charge wires render_inline_command_reroll.
#
# `_active_charge` (chargePhase.py) calls render_inline_command_reroll right
# after the charge-roll caption and before the Successful/Failed decision
# (S136-Review-Befund: this call site was untested). Advance/Charge are the
# only wurf-GOs that keep the bespoke inline offer instead of the
# render_reactive_stratagem_box GO card (design_system.md §6.3 exception) —
# the charge roll value itself is never captured by the app, so `on_reroll`
# is a no-op (nothing to reopen).
#
# These tests spy on render_inline_command_reroll rather than simulating full
# widget interaction — its own visibility/spend contract is covered
# end-to-end with real stratagem data in tests/uiLayout/test_common.py. Here
# the contract under test is: WHEN _active_charge calls it
# (faction/phase/reopen_key), and that its on_reroll callback is a harmless
# no-op.
# ---------------------------------------------------------------------------


def _quiet_charge_widgets(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(cp.st, "markdown", lambda *a, **kw: None)
    monkeypatch.setattr(cp.st, "caption", lambda *a, **kw: None)
    monkeypatch.setattr(cp.st, "info", lambda *a, **kw: None)
    monkeypatch.setattr(cp.st, "warning", lambda *a, **kw: None)
    monkeypatch.setattr(cp.st, "columns", lambda n: tuple(MagicMock() for _ in range(n)))
    monkeypatch.setattr(cp.st, "button", lambda *a, **kw: False)


def _charge_unit_state(**overrides):  # type: ignore[no-untyped-def]
    unit_state = {
        "turn_flags": {},
        "in_melee": False,
    }
    unit_state.update(overrides)
    return unit_state


def _game_state():  # type: ignore[no-untyped-def]
    return {"round": 2, "first_player": "Necrons", "second_player": "Orks"}


class TestActiveChargeCommandReroll:
    def test_offers_command_reroll_with_correct_args(self, monkeypatch) -> None:
        _quiet_charge_widgets(monkeypatch)
        cp.st.session_state = _S(selected_targets=[("Orks", BOYZ)])
        tgt_unit = SimpleNamespace(name_en="Boyz")
        monkeypatch.setattr(cp, "lookup", lambda faction, uid: (tgt_unit, {}))
        spy = MagicMock()
        monkeypatch.setattr(cp, "render_inline_command_reroll", spy)
        unit = SimpleNamespace(name_en="Necron Warriors")

        cp._active_charge("Necrons", WARRIORS, unit, _charge_unit_state(), _game_state())

        spy.assert_called_once()
        call = spy.call_args
        assert call.args[0] == "Necrons"
        assert call.args[1] == "charge"
        assert call.kwargs["reopen_key"] == WARRIORS
        assert callable(call.kwargs["on_reroll"])
        call.kwargs["on_reroll"]()  # no-op — must not raise

    def test_reopen_key_follows_the_charging_unit(self, monkeypatch) -> None:
        """reopen_key is the charging unit's state key — a second charger gets
        its own offer, not the first charger's."""
        _quiet_charge_widgets(monkeypatch)
        cp.st.session_state = _S(selected_targets=[("Orks", BOYZ)])
        tgt_unit = SimpleNamespace(name_en="Boyz")
        monkeypatch.setattr(cp, "lookup", lambda faction, uid: (tgt_unit, {}))
        spy = MagicMock()
        monkeypatch.setattr(cp, "render_inline_command_reroll", spy)
        unit = SimpleNamespace(name_en="Overlord")

        cp._active_charge("Necrons", OVERLORD, unit, _charge_unit_state(), _game_state())

        spy.assert_called_once()
        assert spy.call_args.kwargs["reopen_key"] == OVERLORD

    def test_no_offer_without_targets(self, monkeypatch) -> None:
        """No targets selected yet — the roll has not happened, nothing to re-roll."""
        _quiet_charge_widgets(monkeypatch)
        cp.st.session_state = _S(selected_targets=[])
        spy = MagicMock()
        monkeypatch.setattr(cp, "render_inline_command_reroll", spy)
        unit = SimpleNamespace(name_en="Necron Warriors")

        cp._active_charge("Necrons", WARRIORS, unit, _charge_unit_state(), _game_state())

        spy.assert_not_called()

    def test_no_offer_when_already_in_melee(self, monkeypatch) -> None:
        """Already-in-melee units cannot charge at all — the roll caption and
        the re-roll offer are both unreachable."""
        _quiet_charge_widgets(monkeypatch)
        monkeypatch.setattr(cp, "render_melee_engagements", lambda *a, **kw: None)
        cp.st.session_state = _S(selected_targets=[("Orks", BOYZ)])
        spy = MagicMock()
        monkeypatch.setattr(cp, "render_inline_command_reroll", spy)
        unit = SimpleNamespace(name_en="Necron Warriors")

        cp._active_charge(
            "Necrons", WARRIORS, unit, _charge_unit_state(in_melee=True), _game_state()
        )

        spy.assert_not_called()


# ---------------------------------------------------------------------------
# S148 Brief 3 — _inactive_charge: Engagement-Range gate (rules_appendix.txt
# Z. 2319-2323: "A unit cannot fire Overwatch if there are any enemy units
# within Engagement Range of it") + weapon_conditions wiring (Fire Overwatch
# needs a ranged weapon — checked against the reacting unit itself, not the
# charging unit).
# ---------------------------------------------------------------------------


class TestInactiveChargeOverwatchGate:
    def test_no_go_box_when_already_in_engagement_range(self, monkeypatch) -> None:
        _quiet_charge_widgets(monkeypatch)
        spy = MagicMock()
        monkeypatch.setattr(cp, "render_reactive_stratagem_box", spy)
        cp.st.session_state = _S(selected_unit=None)
        unit = SimpleNamespace(name_en="Necron Warriors")

        cp._inactive_charge("Necrons", WARRIORS, unit, _charge_unit_state(in_melee=True))

        spy.assert_not_called()

    def test_go_box_offered_when_not_in_melee(self, monkeypatch) -> None:
        _quiet_charge_widgets(monkeypatch)
        spy = MagicMock()
        monkeypatch.setattr(cp, "render_reactive_stratagem_box", spy)
        cp.st.session_state = _S(selected_unit=None)
        unit = SimpleNamespace(name_en="Necron Warriors")

        cp._inactive_charge("Necrons", WARRIORS, unit, _charge_unit_state(in_melee=False))

        spy.assert_called_once()

    def test_go_box_passes_reacting_unit_for_weapon_conditions(self, monkeypatch) -> None:
        """The reacting unit itself (not the charger) is passed as
        `unit_for_conditions` — that is whose weapons Fire Overwatch's
        `weapon_conditions: [RANGED]` gate is checked against."""
        _quiet_charge_widgets(monkeypatch)
        spy = MagicMock()
        monkeypatch.setattr(cp, "render_reactive_stratagem_box", spy)
        cp.st.session_state = _S(selected_unit=None)
        unit = SimpleNamespace(name_en="Necron Warriors")

        cp._inactive_charge("Necrons", WARRIORS, unit, _charge_unit_state(in_melee=False))

        spy.assert_called_once()
        assert spy.call_args.kwargs["unit_for_conditions"] is unit

    def test_go_box_passes_reacting_unit_uid_as_unit_key_for_modifier(self, monkeypatch) -> None:
        """S155 B-027: Fire Overwatch must record the reacting unit's uid via
        `unit_key_for_modifier` so `spend_stratagem` can resolve the "used on
        ⟨Einheit⟩" suffix — before this fix the kwarg was never passed and the
        suffix stayed empty for this reactive window (spec-conform edge case,
        not a crash)."""
        _quiet_charge_widgets(monkeypatch)
        spy = MagicMock()
        monkeypatch.setattr(cp, "render_reactive_stratagem_box", spy)
        cp.st.session_state = _S(selected_unit=None)
        unit = SimpleNamespace(name_en="Necron Warriors")

        cp._inactive_charge("Necrons", WARRIORS, unit, _charge_unit_state(in_melee=False))

        spy.assert_called_once()
        assert spy.call_args.kwargs["unit_key_for_modifier"] == WARRIORS
