"""Tests for unit_mutations.py: apply_damage, heal_unit, enter_melee, leave_melee,
set_charged, set_movement_status."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.game_state as _gs  # noqa: E402
import gameMechanic.unit_mutations as _mut  # noqa: E402
from gameMechanic.game_state import next_phase  # noqa: E402
from gameMechanic.unit_mutations import (  # noqa: E402
    apply_damage,
    enter_melee,
    heal_unit,
    leave_melee,
    set_charged,
    set_movement_status,
)
from gameObjects.unit import Unit  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

OVERLORD = "wh40k_9e.necrons.unit.overlord"
WARRIORS = "wh40k_9e.necrons.unit.warriors"
BOYZ = "wh40k_9e.orks.unit.boyz"
WARBOSS = "wh40k_9e.orks.unit.warboss"


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
    _gs.st.session_state = s
    return s


def _unit() -> dict:
    return {
        "current_wounds": 5,
        "models": 1,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "normal",
        "lost_models_this_turn": 0,
        "movement_choice": None,
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
        },
    }


def _overlord() -> Unit:
    return Unit(
        id=OVERLORD,
        name_en="Overlord",
        name_de="Overlord",
        faction="Necrons",
        subfaction=None,
        battlefield_role=["HQ"],
        keywords=["Necrons"],
        wounds=5,
        models_min=1,
        models_max=1,
        move='6"',
        bs="3+",
        ws="3+",
        strength=5,
        toughness=5,
        save=3,
        invuln_save=4,
        leadership=10,
        oc=1,
        fnp=None,
    )


def _warriors() -> Unit:
    return Unit(
        id=WARRIORS,
        name_en="Necron Warriors",
        name_de="Nekron-Krieger",
        faction="Necrons",
        subfaction=None,
        battlefield_role=["Troops"],
        keywords=["Necrons", "Core"],
        wounds=1,
        models_min=10,
        models_max=10,
        move='5"',
        bs="3+",
        ws="3+",
        strength=4,
        toughness=4,
        save=4,
        invuln_save=6,
        leadership=10,
        oc=2,
        fnp=None,
    )


def _skorpekh() -> Unit:
    return Unit(
        id="wh40k_9e.necrons.unit.skorpekh_destroyers",
        name_en="Skorpekh Destroyers",
        name_de="Skorpekh-Vernichter",
        faction="Necrons",
        subfaction=None,
        battlefield_role=["Elites"],
        keywords=["Necrons", "Core"],
        wounds=3,
        models_min=3,
        models_max=3,
        move='8"',
        bs="3+",
        ws="3+",
        strength=5,
        toughness=5,
        save=3,
        invuln_save=6,
        leadership=10,
        oc=2,
        fnp=None,
    )


def _two_unit_session() -> _S:
    return _make_session(
        necron_units={OVERLORD: _unit()},
        ork_units={BOYZ: _unit()},
        selected_targets=[],
        phase_idx=5,
        active="Necrons",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=None,
    )


def _four_unit_session() -> _S:
    return _make_session(
        necron_units={OVERLORD: _unit(), WARRIORS: _unit()},
        ork_units={BOYZ: _unit(), WARBOSS: _unit()},
        selected_targets=[],
        phase_idx=5,
        active="Necrons",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=None,
    )


# ---------------------------------------------------------------------------
# apply_damage
# ---------------------------------------------------------------------------


def test_apply_damage_1wound_models_caps_at_one_model() -> None:
    """3 regular damage on 1-wound models kills exactly 1 model — excess is lost per 9E rules."""
    session = _make_session(
        necron_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage(WARRIORS, "Necrons", 3, _warriors(), mortal=False)
    state = session["necron_units"][WARRIORS]
    assert state["current_wounds"] == 9
    assert state["models"] == 9
    assert state["destroyed"] is False


def test_apply_damage_1wound_models_successive_hits_kill_multiple() -> None:
    """Applying damage three times separately kills three warriors (one per hit)."""
    session = _make_session(
        necron_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage(WARRIORS, "Necrons", 3, _warriors(), mortal=False)
    apply_damage(WARRIORS, "Necrons", 3, _warriors(), mortal=False)
    apply_damage(WARRIORS, "Necrons", 3, _warriors(), mortal=False)
    state = session["necron_units"][WARRIORS]
    assert state["current_wounds"] == 7
    assert state["models"] == 7


def test_apply_damage_mortal_wounds_kill_multiple_1wound_models() -> None:
    """Mortal wounds bypass the spillover cap and can kill multiple 1-wound models."""
    session = _make_session(
        necron_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage(WARRIORS, "Necrons", 3, _warriors(), mortal=True)
    state = session["necron_units"][WARRIORS]
    assert state["current_wounds"] == 7
    assert state["models"] == 7


def test_apply_damage_multiwound_caps_damage_to_front_model() -> None:
    """5 damage on a partially wounded multi-wound unit only finishes the front model."""
    sid = "wh40k_9e.necrons.unit.skorpekh_destroyers"
    session = _make_session(
        necron_units={
            sid: {
                "current_wounds": 7,
                "models": 3,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    # front_hp = 7 - (3-1)*3 = 1 → dmg capped to 1
    apply_damage(sid, "Necrons", 5, _skorpekh(), mortal=False)
    state = session["necron_units"][sid]
    assert state["current_wounds"] == 6
    assert state["models"] == 2


def test_apply_damage_mortal_wound_bypasses_spillover_cap() -> None:
    """A mortal wound always removes exactly 1 wound regardless of model boundary."""
    session = _make_session(
        necron_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage(WARRIORS, "Necrons", 1, _warriors(), mortal=True)
    state = session["necron_units"][WARRIORS]
    assert state["current_wounds"] == 9
    assert state["models"] == 9


def test_apply_damage_single_model_reduces_lp_directly() -> None:
    session = _make_session(
        necron_units={
            OVERLORD: {
                "current_wounds": 5,
                "models": 1,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage(OVERLORD, "Necrons", 3, _overlord(), mortal=False)
    state = session["necron_units"][OVERLORD]
    assert state["current_wounds"] == 2
    assert state["models"] == 1
    assert state["destroyed"] is False


def test_apply_damage_destroys_unit_when_hp_reaches_zero() -> None:
    session = _make_session(
        necron_units={
            OVERLORD: {
                "current_wounds": 2,
                "models": 1,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage(OVERLORD, "Necrons", 5, _overlord(), mortal=False)
    state = session["necron_units"][OVERLORD]
    assert state["destroyed"] is True
    assert state["current_wounds"] == 0
    assert state["models"] == 0


def test_apply_damage_tracks_lost_models_this_turn() -> None:
    session = _make_session(
        necron_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 2,
            }
        }
    )
    apply_damage(WARRIORS, "Necrons", 3, _warriors(), mortal=False)
    state = session["necron_units"][WARRIORS]
    assert state["lost_models_this_turn"] == 3  # 2 existing + 1 new (cap: only front model dies)


# ---------------------------------------------------------------------------
# heal_unit
# ---------------------------------------------------------------------------


def test_heal_unit_restores_wounds() -> None:
    session = _make_session(
        necron_units={OVERLORD: {"current_wounds": 3, "models": 1, "destroyed": False}}
    )
    heal_unit(OVERLORD, "Necrons", 1, _overlord())
    assert session["necron_units"][OVERLORD]["current_wounds"] == 4


def test_heal_unit_caps_at_maximum_wounds() -> None:
    session = _make_session(
        necron_units={OVERLORD: {"current_wounds": 4, "models": 1, "destroyed": False}}
    )
    heal_unit(OVERLORD, "Necrons", 10, _overlord())
    assert session["necron_units"][OVERLORD]["current_wounds"] == 5


def test_heal_unit_revives_destroyed_unit() -> None:
    session = _make_session(
        necron_units={OVERLORD: {"current_wounds": 0, "models": 0, "destroyed": True}}
    )
    heal_unit(OVERLORD, "Necrons", 1, _overlord())
    state = session["necron_units"][OVERLORD]
    assert state["current_wounds"] == 1
    assert state["destroyed"] is False
    assert state["models"] == 1


def test_heal_unit_updates_model_count_for_multimodel() -> None:
    session = _make_session(
        necron_units={WARRIORS: {"current_wounds": 7, "models": 7, "destroyed": False}}
    )
    heal_unit(WARRIORS, "Necrons", 3, _warriors())
    state = session["necron_units"][WARRIORS]
    assert state["current_wounds"] == 10
    assert state["models"] == 10


def test_heal_unit_returns_true_when_healed() -> None:
    _make_session(necron_units={OVERLORD: {"current_wounds": 3, "models": 1, "destroyed": False}})
    assert heal_unit(OVERLORD, "Necrons", 1, _overlord()) is True


def test_heal_unit_returns_false_when_already_full() -> None:
    _make_session(necron_units={OVERLORD: {"current_wounds": 5, "models": 1, "destroyed": False}})
    assert heal_unit(OVERLORD, "Necrons", 1, _overlord()) is False


def test_heal_unit_no_revive_caps_at_current_models() -> None:
    """revive=False: cannot heal beyond current living models × wounds."""
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.skorpekh_destroyers": {
                "current_wounds": 5,
                "models": 2,
                "destroyed": False,
            }
        }
    )
    heal_unit("wh40k_9e.necrons.unit.skorpekh_destroyers", "Necrons", 1, _skorpekh(), revive=False)
    state = session["necron_units"]["wh40k_9e.necrons.unit.skorpekh_destroyers"]
    assert state["current_wounds"] == 6  # 2 models × 3 wounds = 6 max, was 5
    assert state["models"] == 2  # dead model NOT restored


def test_heal_unit_no_revive_does_not_exceed_living_model_cap() -> None:
    """revive=False: full living-model HP → no healing, dead model stays dead."""
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.skorpekh_destroyers": {
                "current_wounds": 6,
                "models": 2,
                "destroyed": False,
            }
        }
    )
    result = heal_unit(
        "wh40k_9e.necrons.unit.skorpekh_destroyers", "Necrons", 1, _skorpekh(), revive=False
    )
    state = session["necron_units"]["wh40k_9e.necrons.unit.skorpekh_destroyers"]
    assert result is False
    assert state["current_wounds"] == 6
    assert state["models"] == 2


# ---------------------------------------------------------------------------
# enter_melee
# ---------------------------------------------------------------------------


def test_enter_melee_registers_both_sides() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    assert ["Orks", BOYZ] in session["necron_units"][OVERLORD]["melee_with"]
    assert ["Necrons", OVERLORD] in session["ork_units"][BOYZ]["melee_with"]


def test_enter_melee_sets_in_melee_true_for_both() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["necron_units"][OVERLORD]["in_melee"] is True
    assert session["ork_units"][BOYZ]["in_melee"] is True


def test_enter_melee_idempotent() -> None:
    """Calling enter_melee twice must not add duplicates."""
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    mw_overlord = session["necron_units"][OVERLORD]["melee_with"]
    mw_boyz = session["ork_units"][BOYZ]["melee_with"]
    assert sum(1 for p in mw_overlord if p == ["Orks", BOYZ]) == 1
    assert sum(1 for p in mw_boyz if p == ["Necrons", OVERLORD]) == 1


def test_enter_melee_multiple_enemies() -> None:
    """One attacker can enter melee with two targets."""
    session = _four_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    enter_melee(OVERLORD, "Necrons", WARBOSS, "Orks")
    mw = session["necron_units"][OVERLORD]["melee_with"]
    assert ["Orks", BOYZ] in mw
    assert ["Orks", WARBOSS] in mw


# ---------------------------------------------------------------------------
# leave_melee
# ---------------------------------------------------------------------------


def test_leave_melee_clears_attacker_melee_with() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert session["necron_units"][OVERLORD]["melee_with"] == []


def test_leave_melee_removes_from_enemy_melee_with() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert ["Necrons", OVERLORD] not in session["ork_units"][BOYZ]["melee_with"]


def test_leave_melee_sets_in_melee_false_for_attacker() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert session["necron_units"][OVERLORD]["in_melee"] is False


def test_leave_melee_sets_in_melee_false_for_enemy_when_no_other_engagements() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert session["ork_units"][BOYZ]["in_melee"] is False


def test_leave_melee_enemy_stays_in_melee_if_still_engaged_elsewhere() -> None:
    """Boyz engaged with both Overlord and Warriors — Overlord retreating doesn't free Boyz."""
    session = _four_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    enter_melee(WARRIORS, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert session["ork_units"][BOYZ]["in_melee"] is True
    assert ["Necrons", WARRIORS] in session["ork_units"][BOYZ]["melee_with"]


# ---------------------------------------------------------------------------
# set_charged
# ---------------------------------------------------------------------------


def test_set_charged_sets_charged_flag() -> None:
    session = _two_unit_session()
    set_charged(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["necron_units"][OVERLORD]["turn_flags"]["charged"] is True


def test_set_charged_enters_melee_for_both_units() -> None:
    session = _two_unit_session()
    set_charged(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["necron_units"][OVERLORD]["in_melee"] is True
    assert session["ork_units"][BOYZ]["in_melee"] is True
    assert ["Orks", BOYZ] in session["necron_units"][OVERLORD]["melee_with"]
    assert ["Necrons", OVERLORD] in session["ork_units"][BOYZ]["melee_with"]


def test_set_charged_multiple_targets() -> None:
    """Charging two targets: both registered in melee_with."""
    session = _four_unit_session()
    set_charged(OVERLORD, "Necrons", BOYZ, "Orks")
    set_charged(OVERLORD, "Necrons", WARBOSS, "Orks")
    mw = session["necron_units"][OVERLORD]["melee_with"]
    assert ["Orks", BOYZ] in mw
    assert ["Orks", WARBOSS] in mw


# ---------------------------------------------------------------------------
# set_movement_status
# ---------------------------------------------------------------------------


def test_set_movement_status_sets_movement_choice() -> None:
    session = _two_unit_session()
    set_movement_status(OVERLORD, "Necrons", "advanced")
    assert session["necron_units"][OVERLORD]["movement_choice"] == "advanced"


def test_set_movement_status_advanced_sets_turn_flag() -> None:
    session = _two_unit_session()
    set_movement_status(OVERLORD, "Necrons", "advanced")
    assert session["necron_units"][OVERLORD]["turn_flags"]["advanced"] is True


def test_set_movement_status_moved_does_not_set_advanced_flag() -> None:
    session = _two_unit_session()
    set_movement_status(OVERLORD, "Necrons", "moved")
    assert session["necron_units"][OVERLORD]["turn_flags"]["advanced"] is False
    assert session["necron_units"][OVERLORD]["turn_flags"]["retreated"] is False


def test_set_movement_status_retreated_calls_leave_melee() -> None:
    """Retreating clears melee engagement."""
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    set_movement_status(OVERLORD, "Necrons", "retreated")
    assert session["necron_units"][OVERLORD]["in_melee"] is False
    assert session["necron_units"][OVERLORD]["melee_with"] == []


# ---------------------------------------------------------------------------
# movement_choice reset on turn end
# ---------------------------------------------------------------------------


def test_reset_turn_state_resets_movement_choice_to_stationary() -> None:
    session = _make_session(
        necron_units={OVERLORD: {**_unit(), "movement_choice": "advanced"}},
        ork_units={BOYZ: {**_unit(), "movement_choice": "advanced"}},
        selected_targets=[],
        phase_idx=7,  # morale phase — triggers turn reset
        active="Necrons",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=None,
    )
    next_phase()
    assert session["necron_units"][OVERLORD]["movement_choice"] == "stationary"
    assert session["ork_units"][BOYZ]["movement_choice"] == "stationary"
