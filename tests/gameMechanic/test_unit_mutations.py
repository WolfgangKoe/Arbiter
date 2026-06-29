"""Tests for unit_mutations.py: apply_damage, heal_unit, enter_melee, leave_melee,
set_charged, set_movement_status."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.game_state as _gs  # noqa: E402
import gameMechanic.unit_mutations as _mut  # noqa: E402
from gameMechanic.game_state import next_phase  # noqa: E402
from gameMechanic.unit_mutations import (  # noqa: E402
    apply_buff_to_unit,
    apply_damage,
    enter_melee,
    get_locked_group,
    heal_unit,
    leave_melee,
    select_damage_target_group,
    set_charged,
    set_movement_status,
)
from gameObjects.unit import ModelGroup, Unit  # noqa: E402

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
    kwargs.setdefault("first_player", "Necrons")
    kwargs.setdefault("second_player", "Orks")
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
        power_level=6,
        move='6"',
        bs="3+",
        ws="3+",
        strength=5,
        toughness=5,
        attacks=4,
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
        power_level=8,
        move='5"',
        bs="3+",
        ws="3+",
        strength=4,
        toughness=4,
        attacks=1,
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
        power_level=5,
        move='8"',
        bs="3+",
        ws="3+",
        strength=5,
        toughness=5,
        attacks=3,
        save=3,
        invuln_save=6,
        leadership=10,
        oc=2,
        fnp=None,
    )


def _two_unit_session() -> _S:
    return _make_session(
        first_player="Necrons",
        p1_units={OVERLORD: _unit()},
        p2_units={BOYZ: _unit()},
        selected_targets=[],
        phase_idx=5,
        active="Necrons",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=None,
    )


def _four_unit_session() -> _S:
    return _make_session(
        first_player="Necrons",
        p1_units={OVERLORD: _unit(), WARRIORS: _unit()},
        p2_units={BOYZ: _unit(), WARBOSS: _unit()},
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
        p1_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage(WARRIORS, "Necrons", 3, _warriors(), mortal=False)
    state = session["p1_units"][WARRIORS]
    assert state["current_wounds"] == 9
    assert state["models"] == 9
    assert state["destroyed"] is False


def test_apply_damage_1wound_models_successive_hits_kill_multiple() -> None:
    """Applying damage three times separately kills three warriors (one per hit)."""
    session = _make_session(
        p1_units={
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
    state = session["p1_units"][WARRIORS]
    assert state["current_wounds"] == 7
    assert state["models"] == 7


def test_apply_damage_mortal_wounds_kill_multiple_1wound_models() -> None:
    """Mortal wounds bypass the spillover cap and can kill multiple 1-wound models."""
    session = _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage(WARRIORS, "Necrons", 3, _warriors(), mortal=True)
    state = session["p1_units"][WARRIORS]
    assert state["current_wounds"] == 7
    assert state["models"] == 7


def test_apply_damage_multiwound_caps_damage_to_front_model() -> None:
    """5 damage on a partially wounded multi-wound unit only finishes the front model."""
    sid = "wh40k_9e.necrons.unit.skorpekh_destroyers"
    session = _make_session(
        p1_units={
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
    state = session["p1_units"][sid]
    assert state["current_wounds"] == 6
    assert state["models"] == 2


def test_apply_damage_mortal_wound_bypasses_spillover_cap() -> None:
    """A mortal wound always removes exactly 1 wound regardless of model boundary."""
    session = _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage(WARRIORS, "Necrons", 1, _warriors(), mortal=True)
    state = session["p1_units"][WARRIORS]
    assert state["current_wounds"] == 9
    assert state["models"] == 9


def test_apply_damage_single_model_reduces_lp_directly() -> None:
    session = _make_session(
        p1_units={
            OVERLORD: {
                "current_wounds": 5,
                "models": 1,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage(OVERLORD, "Necrons", 3, _overlord(), mortal=False)
    state = session["p1_units"][OVERLORD]
    assert state["current_wounds"] == 2
    assert state["models"] == 1
    assert state["destroyed"] is False


def test_apply_damage_destroys_unit_when_hp_reaches_zero() -> None:
    session = _make_session(
        p1_units={
            OVERLORD: {
                "current_wounds": 2,
                "models": 1,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage(OVERLORD, "Necrons", 5, _overlord(), mortal=False)
    state = session["p1_units"][OVERLORD]
    assert state["destroyed"] is True
    assert state["current_wounds"] == 0
    assert state["models"] == 0


def test_apply_damage_tracks_lost_models_this_turn() -> None:
    session = _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 2,
            }
        }
    )
    apply_damage(WARRIORS, "Necrons", 3, _warriors(), mortal=False)
    state = session["p1_units"][WARRIORS]
    assert state["lost_models_this_turn"] == 3  # 2 existing + 1 new (cap: only front model dies)


# ---------------------------------------------------------------------------
# heal_unit
# ---------------------------------------------------------------------------


def test_heal_unit_restores_wounds() -> None:
    session = _make_session(
        p1_units={OVERLORD: {"current_wounds": 3, "models": 1, "destroyed": False}}
    )
    heal_unit(OVERLORD, "Necrons", 1, _overlord())
    assert session["p1_units"][OVERLORD]["current_wounds"] == 4


def test_heal_unit_caps_at_maximum_wounds() -> None:
    session = _make_session(
        p1_units={OVERLORD: {"current_wounds": 4, "models": 1, "destroyed": False}}
    )
    heal_unit(OVERLORD, "Necrons", 10, _overlord())
    assert session["p1_units"][OVERLORD]["current_wounds"] == 5


def test_heal_unit_revives_destroyed_unit() -> None:
    session = _make_session(
        p1_units={OVERLORD: {"current_wounds": 0, "models": 0, "destroyed": True}}
    )
    heal_unit(OVERLORD, "Necrons", 1, _overlord())
    state = session["p1_units"][OVERLORD]
    assert state["current_wounds"] == 1
    assert state["destroyed"] is False
    assert state["models"] == 1


def test_heal_unit_reduces_lost_models_this_turn() -> None:
    """Revived models (RP, Resurrection Orb, …) no longer count for Morale."""
    session = _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 7,
                "models": 7,
                "destroyed": False,
                "lost_models_this_turn": 3,
            }
        }
    )
    heal_unit(WARRIORS, "Necrons", 2, _warriors())
    state = session["p1_units"][WARRIORS]
    assert state["models"] == 9
    assert state["lost_models_this_turn"] == 1


def test_heal_unit_lost_models_never_negative() -> None:
    session = _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 7,
                "models": 7,
                "destroyed": False,
                "lost_models_this_turn": 1,
            }
        }
    )
    heal_unit(WARRIORS, "Necrons", 3, _warriors())
    assert session["p1_units"][WARRIORS]["lost_models_this_turn"] == 0


def test_heal_unit_restores_group_models_in_priority_order() -> None:
    """Revived models refill the group that died first (lowest priority)."""
    groups = [
        ModelGroup(id="ork_boy", name_en="Ork Boy", count=9, weapons=[], priority=1),
        ModelGroup(id="boss_nob", name_en="Boss Nob", count=1, weapons=[], priority=2),
    ]
    boyz_unit = Unit(
        id=BOYZ,
        name_en="Boyz",
        name_de="Boyz",
        faction="Orks",
        subfaction=None,
        battlefield_role=["Troops"],
        keywords=["ORK"],
        wounds=1,
        models_min=10,
        models_max=10,
        power_level=6,
        move='5"',
        bs="5+",
        ws="3+",
        strength=4,
        toughness=5,
        attacks=2,
        save=6,
        invuln_save=None,
        leadership=6,
        oc=2,
        fnp=None,
        weapons=[],
        model_groups=groups,
    )
    session = _make_session(
        p2_units={
            BOYZ: {
                "current_wounds": 5,
                "models": 5,
                "destroyed": False,
                "lost_models_this_turn": 5,
                "group_models": {"ork_boy": 4, "boss_nob": 1},
            }
        }
    )
    heal_unit(BOYZ, "Orks", 3, boyz_unit)
    state = session["p2_units"][BOYZ]
    assert state["models"] == 8
    assert state["group_models"] == {"ork_boy": 7, "boss_nob": 1}
    assert state["lost_models_this_turn"] == 2


def test_heal_unit_updates_model_count_for_multimodel() -> None:
    session = _make_session(
        p1_units={WARRIORS: {"current_wounds": 7, "models": 7, "destroyed": False}}
    )
    heal_unit(WARRIORS, "Necrons", 3, _warriors())
    state = session["p1_units"][WARRIORS]
    assert state["current_wounds"] == 10
    assert state["models"] == 10


def test_heal_unit_returns_true_when_healed() -> None:
    _make_session(p1_units={OVERLORD: {"current_wounds": 3, "models": 1, "destroyed": False}})
    assert heal_unit(OVERLORD, "Necrons", 1, _overlord()) is True


def test_heal_unit_returns_false_when_already_full() -> None:
    _make_session(p1_units={OVERLORD: {"current_wounds": 5, "models": 1, "destroyed": False}})
    assert heal_unit(OVERLORD, "Necrons", 1, _overlord()) is False


def test_heal_unit_no_revive_caps_at_current_models() -> None:
    """revive=False: cannot heal beyond current living models × wounds."""
    session = _make_session(
        p1_units={
            "wh40k_9e.necrons.unit.skorpekh_destroyers": {
                "current_wounds": 5,
                "models": 2,
                "destroyed": False,
            }
        }
    )
    heal_unit("wh40k_9e.necrons.unit.skorpekh_destroyers", "Necrons", 1, _skorpekh(), revive=False)
    state = session["p1_units"]["wh40k_9e.necrons.unit.skorpekh_destroyers"]
    assert state["current_wounds"] == 6  # 2 models × 3 wounds = 6 max, was 5
    assert state["models"] == 2  # dead model NOT restored


def test_heal_unit_no_revive_does_not_exceed_living_model_cap() -> None:
    """revive=False: full living-model HP → no healing, dead model stays dead."""
    session = _make_session(
        p1_units={
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
    state = session["p1_units"]["wh40k_9e.necrons.unit.skorpekh_destroyers"]
    assert result is False
    assert state["current_wounds"] == 6
    assert state["models"] == 2


# ---------------------------------------------------------------------------
# enter_melee
# ---------------------------------------------------------------------------


def test_enter_melee_registers_both_sides() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    assert ["Orks", BOYZ] in session["p1_units"][OVERLORD]["melee_with"]
    assert ["Necrons", OVERLORD] in session["p2_units"][BOYZ]["melee_with"]


def test_enter_melee_sets_in_melee_true_for_both() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["p1_units"][OVERLORD]["in_melee"] is True
    assert session["p2_units"][BOYZ]["in_melee"] is True


def test_enter_melee_idempotent() -> None:
    """Calling enter_melee twice must not add duplicates."""
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    mw_overlord = session["p1_units"][OVERLORD]["melee_with"]
    mw_boyz = session["p2_units"][BOYZ]["melee_with"]
    assert sum(1 for p in mw_overlord if p == ["Orks", BOYZ]) == 1
    assert sum(1 for p in mw_boyz if p == ["Necrons", OVERLORD]) == 1


def test_enter_melee_multiple_enemies() -> None:
    """One attacker can enter melee with two targets."""
    session = _four_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    enter_melee(OVERLORD, "Necrons", WARBOSS, "Orks")
    mw = session["p1_units"][OVERLORD]["melee_with"]
    assert ["Orks", BOYZ] in mw
    assert ["Orks", WARBOSS] in mw


# ---------------------------------------------------------------------------
# leave_melee
# ---------------------------------------------------------------------------


def test_leave_melee_clears_attacker_melee_with() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert session["p1_units"][OVERLORD]["melee_with"] == []


def test_leave_melee_removes_from_enemy_melee_with() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert ["Necrons", OVERLORD] not in session["p2_units"][BOYZ]["melee_with"]


def test_leave_melee_sets_in_melee_false_for_attacker() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert session["p1_units"][OVERLORD]["in_melee"] is False


def test_leave_melee_sets_in_melee_false_for_enemy_when_no_other_engagements() -> None:
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert session["p2_units"][BOYZ]["in_melee"] is False


def test_leave_melee_enemy_stays_in_melee_if_still_engaged_elsewhere() -> None:
    """Boyz engaged with both Overlord and Warriors — Overlord retreating doesn't free Boyz."""
    session = _four_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    enter_melee(WARRIORS, "Necrons", BOYZ, "Orks")
    leave_melee(OVERLORD, "Necrons")
    assert session["p2_units"][BOYZ]["in_melee"] is True
    assert ["Necrons", WARRIORS] in session["p2_units"][BOYZ]["melee_with"]


# ---------------------------------------------------------------------------
# set_charged
# ---------------------------------------------------------------------------


def test_set_charged_sets_charged_flag() -> None:
    session = _two_unit_session()
    set_charged(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["p1_units"][OVERLORD]["turn_flags"]["charged"] is True


def test_set_charged_enters_melee_for_both_units() -> None:
    session = _two_unit_session()
    set_charged(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["p1_units"][OVERLORD]["in_melee"] is True
    assert session["p2_units"][BOYZ]["in_melee"] is True
    assert ["Orks", BOYZ] in session["p1_units"][OVERLORD]["melee_with"]
    assert ["Necrons", OVERLORD] in session["p2_units"][BOYZ]["melee_with"]


def test_set_charged_multiple_targets() -> None:
    """Charging two targets: both registered in melee_with."""
    session = _four_unit_session()
    set_charged(OVERLORD, "Necrons", BOYZ, "Orks")
    set_charged(OVERLORD, "Necrons", WARBOSS, "Orks")
    mw = session["p1_units"][OVERLORD]["melee_with"]
    assert ["Orks", BOYZ] in mw
    assert ["Orks", WARBOSS] in mw


# ---------------------------------------------------------------------------
# set_movement_status
# ---------------------------------------------------------------------------


def test_set_movement_status_sets_movement_choice() -> None:
    session = _two_unit_session()
    set_movement_status(OVERLORD, "Necrons", "advanced")
    assert session["p1_units"][OVERLORD]["movement_choice"] == "advanced"


def test_set_movement_status_advanced_sets_turn_flag() -> None:
    session = _two_unit_session()
    set_movement_status(OVERLORD, "Necrons", "advanced")
    assert session["p1_units"][OVERLORD]["turn_flags"]["advanced"] is True


def test_set_movement_status_moved_does_not_set_advanced_flag() -> None:
    session = _two_unit_session()
    set_movement_status(OVERLORD, "Necrons", "moved")
    assert session["p1_units"][OVERLORD]["turn_flags"]["advanced"] is False
    assert session["p1_units"][OVERLORD]["turn_flags"]["retreated"] is False


def test_set_movement_status_retreated_calls_leave_melee() -> None:
    """Retreating clears melee engagement."""
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    set_movement_status(OVERLORD, "Necrons", "retreated")
    assert session["p1_units"][OVERLORD]["in_melee"] is False
    assert session["p1_units"][OVERLORD]["melee_with"] == []


# ---------------------------------------------------------------------------
# movement_choice reset on turn end
# ---------------------------------------------------------------------------


def test_reset_turn_state_resets_movement_choice_to_stationary() -> None:
    session = _make_session(
        p1_units={OVERLORD: {**_unit(), "movement_choice": "advanced"}},
        p2_units={BOYZ: {**_unit(), "movement_choice": "advanced"}},
        selected_targets=[],
        phase_idx=7,  # morale phase — triggers turn reset
        active="Necrons",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=None,
    )
    next_phase()
    assert session["p1_units"][OVERLORD]["movement_choice"] == "stationary"
    assert session["p2_units"][BOYZ]["movement_choice"] == "stationary"


# ---------------------------------------------------------------------------
# apply_damage — group_models priority reduction
# ---------------------------------------------------------------------------


def _boyz_with_groups() -> Unit:
    return Unit(
        id=BOYZ,
        name_en="Boyz",
        name_de="Boyz",
        faction="Orks",
        subfaction=None,
        battlefield_role=["Troops"],
        keywords=["ORK"],
        wounds=1,
        models_min=10,
        models_max=10,
        power_level=6,
        move='5"',
        bs="5+",
        ws="3+",
        strength=4,
        toughness=5,
        attacks=2,
        save=6,
        invuln_save=None,
        leadership=6,
        oc=2,
        fnp=None,
        model_groups=[
            ModelGroup(id="ork_boy", name_en="Ork Boy", count=9, weapons=[], priority=1),
            ModelGroup(id="boss_nob", name_en="Boss Nob", count=1, weapons=[], priority=2),
        ],
    )


def _boyz_state(models: int = 10) -> dict:  # type: ignore[type-arg]
    return {
        "current_wounds": models,
        "models": models,
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
        "group_models": {"ork_boy": 9, "boss_nob": 1},
    }


def test_apply_damage_group_models_reduces_priority_1_first() -> None:
    session = _make_session(p1_units={BOYZ: _boyz_state()})
    apply_damage(BOYZ, "Necrons", 3, _boyz_with_groups(), mortal=True)
    gm = session["p1_units"][BOYZ]["group_models"]
    assert gm["ork_boy"] == 6  # 3 ork boys lost
    assert gm["boss_nob"] == 1  # boss nob untouched


def test_apply_damage_group_models_boss_nob_survives_until_boys_gone() -> None:
    session = _make_session(p1_units={BOYZ: _boyz_state()})
    apply_damage(BOYZ, "Necrons", 9, _boyz_with_groups(), mortal=True)
    gm = session["p1_units"][BOYZ]["group_models"]
    assert gm["ork_boy"] == 0
    assert gm["boss_nob"] == 1  # boss nob still alive


def test_apply_damage_group_models_boss_nob_dies_last() -> None:
    session = _make_session(p1_units={BOYZ: _boyz_state()})
    apply_damage(BOYZ, "Necrons", 10, _boyz_with_groups(), mortal=True)
    gm = session["p1_units"][BOYZ]["group_models"]
    assert gm["ork_boy"] == 0
    assert gm["boss_nob"] == 0


def test_apply_damage_without_group_models_leaves_dict_unchanged() -> None:
    state = _boyz_state()
    state["group_models"] = {}
    session = _make_session(p1_units={BOYZ: state})
    unit = _boyz_with_groups()
    unit = Unit(**{**unit.__dict__, "model_groups": []})
    apply_damage(BOYZ, "Necrons", 3, unit, mortal=True)
    assert session["p1_units"][BOYZ]["group_models"] == {}


# ---------------------------------------------------------------------------
# Per-group wounds (G2): Szarekh 16 + Triarchal Menhirs 7, Menhirs die first
# ---------------------------------------------------------------------------

SILENT_KING = "wh40k_9e.necrons.unit.the_silent_king"


def _silent_king() -> Unit:
    groups = [
        ModelGroup(
            id="triarchal_menhirs",
            name_en="Triarchal Menhirs",
            count=2,
            weapons=[],
            priority=1,
            stats={"wounds": 7, "ws": "5+", "bs": "3+"},
        ),
        ModelGroup(
            id="szarekh", name_en="Szarekh", count=1, weapons=[], priority=2, stats={"wounds": 16}
        ),
    ]
    return Unit(
        id=SILENT_KING,
        name_en="The Silent King",
        name_de="Der Stille König",
        faction="Necrons",
        subfaction=None,
        battlefield_role=["Lord of War"],
        keywords=["NECRONS"],
        wounds=16,
        models_min=3,
        models_max=3,
        power_level=21,
        move='8"',
        bs="2+",
        ws="2+",
        strength=5,
        toughness=7,
        attacks=6,
        save=3,
        invuln_save=4,
        leadership=10,
        oc=5,
        fnp=None,
        weapons=[],
        model_groups=groups,
    )


def test_unit_state_inits_per_group_wounds() -> None:
    sk = _silent_king()
    state = _gs._unit_state(sk, 3)
    assert state["group_wounds"] == {"triarchal_menhirs": 14, "szarekh": 16}
    assert state["current_wounds"] == 30
    assert state["models"] == 3


def test_homogeneous_unit_has_no_group_wounds() -> None:
    state = _gs._unit_state(_warriors(), 10)
    assert state["group_wounds"] == {}
    assert state["current_wounds"] == 10


def _sk_session() -> _S:
    sk = _silent_king()
    return _make_session(p1_units={SILENT_KING: _gs._unit_state(sk, 3)})


def test_apply_damage_menhirs_take_wounds_first() -> None:
    session = _sk_session()
    apply_damage(SILENT_KING, "Necrons", 10, _silent_king(), resolved=True)
    state = session["p1_units"][SILENT_KING]
    assert state["group_wounds"]["triarchal_menhirs"] == 4
    assert state["group_wounds"]["szarekh"] == 16
    assert state["group_models"] == {"triarchal_menhirs": 1, "szarekh": 1}
    assert state["models"] == 2


def test_apply_damage_spills_into_szarekh_after_menhirs_gone() -> None:
    session = _sk_session()
    apply_damage(SILENT_KING, "Necrons", 18, _silent_king(), resolved=True)
    state = session["p1_units"][SILENT_KING]
    assert state["group_wounds"]["triarchal_menhirs"] == 0
    assert state["group_wounds"]["szarekh"] == 12
    assert state["group_models"] == {"triarchal_menhirs": 0, "szarekh": 1}
    assert state["models"] == 1


def test_apply_damage_destroys_silent_king_at_zero() -> None:
    session = _sk_session()
    apply_damage(SILENT_KING, "Necrons", 30, _silent_king(), resolved=True)
    state = session["p1_units"][SILENT_KING]
    assert state["destroyed"] is True
    assert state["models"] == 0
    assert state["lost_models_this_turn"] == 3


def test_heal_restores_menhirs_first() -> None:
    session = _sk_session()
    apply_damage(SILENT_KING, "Necrons", 18, _silent_king(), resolved=True)
    heal_unit(SILENT_KING, "Necrons", 7, _silent_king())
    state = session["p1_units"][SILENT_KING]
    assert state["group_wounds"]["triarchal_menhirs"] == 7
    assert state["group_models"]["triarchal_menhirs"] == 1
    assert state["models"] == 2


def test_unit_max_hp_group_wounds_vs_uniform() -> None:
    """H3: per-group-wounds max HP is the pool sum, not unit.wounds * models."""
    from gameMechanic.unit_mutations import unit_max_hp

    sk = _silent_king()
    state = _gs._unit_state(sk, 3)
    assert unit_max_hp(sk, state) == 30  # 16 + 7 + 7, NOT 16 * 3 = 48
    assert state["current_wounds"] == 30  # full unit not flagged as damaged
    # uniform unit unchanged
    w_state = _gs._unit_state(_warriors(), 10)
    assert unit_max_hp(_warriors(), w_state) == 10


# ---------------------------------------------------------------------------
# R-CMD-10 — apply_buff_to_unit (buff_roll / reroll_hit_1 recording)
# ---------------------------------------------------------------------------


class TestApplyBuffToUnit:
    def test_adds_buff_to_empty_active_buffs(self) -> None:
        """Activating a buff on a unit with no buffs records it in active_buffs."""
        unit_state: dict = {"active_buffs": []}
        apply_buff_to_unit(unit_state, "mwbd", "MWBD", "buff_roll")
        assert len(unit_state["active_buffs"]) == 1
        assert unit_state["active_buffs"][0]["ability_id"] == "mwbd"

    def test_buff_records_correct_effect_type(self) -> None:
        unit_state: dict = {"active_buffs": []}
        apply_buff_to_unit(unit_state, "reroll_ability", "RR1", "reroll_hit_1")
        assert unit_state["active_buffs"][0]["effect_type"] == "reroll_hit_1"

    def test_buff_records_badge_label(self) -> None:
        unit_state: dict = {"active_buffs": []}
        apply_buff_to_unit(unit_state, "mwbd", "My Will Be Done", "buff_roll")
        assert unit_state["active_buffs"][0]["badge_label"] == "My Will Be Done"

    def test_idempotent_when_same_ability_applied_twice(self) -> None:
        """Applying the same ability_id twice must not create a duplicate buff entry."""
        unit_state: dict = {"active_buffs": []}
        apply_buff_to_unit(unit_state, "mwbd", "MWBD", "buff_roll")
        apply_buff_to_unit(unit_state, "mwbd", "MWBD", "buff_roll")
        assert len(unit_state["active_buffs"]) == 1

    def test_initialises_active_buffs_key_when_missing(self) -> None:
        """Unit state without active_buffs key gets the key created."""
        unit_state: dict = {}
        apply_buff_to_unit(unit_state, "mwbd", "MWBD", "buff_roll")
        assert "active_buffs" in unit_state
        assert len(unit_state["active_buffs"]) == 1

    def test_different_abilities_both_recorded(self) -> None:
        unit_state: dict = {"active_buffs": []}
        apply_buff_to_unit(unit_state, "mwbd", "MWBD", "buff_roll")
        apply_buff_to_unit(unit_state, "waaagh", "WAAAGH!", "buff_roll")
        ids = [b["ability_id"] for b in unit_state["active_buffs"]]
        assert "mwbd" in ids
        assert "waaagh" in ids


# ---------------------------------------------------------------------------
# Plan 014 — Defender loss allocation: directed damage + wounded-model lock
# ---------------------------------------------------------------------------

NOBZ = "wh40k_9e.orks.unit.nobz"


def _nobz_groups() -> list[ModelGroup]:
    """Three same-wound (3 LP) Nob subgroups distinguished only by wargear."""
    return [
        ModelGroup(id="nob_klaw", name_en="Nob – Power Klaw", count=2, weapons=[], priority=1),
        ModelGroup(id="nob_saw", name_en="Nob – Kill Saw", count=2, weapons=[], priority=2),
        ModelGroup(id="nob_slugga", name_en="Nob – Slugga", count=1, weapons=[], priority=3),
    ]


def _nobz_unit() -> Unit:
    return Unit(
        id=NOBZ,
        name_en="Nobz",
        name_de="Nobz",
        faction="Orks",
        subfaction=None,
        battlefield_role=["Elites"],
        keywords=["ORK", "CORE"],
        wounds=3,
        models_min=5,
        models_max=5,
        power_level=6,
        move='5"',
        bs="5+",
        ws="3+",
        strength=5,
        toughness=4,
        attacks=3,
        save=4,
        invuln_save=None,
        leadership=7,
        oc=1,
        fnp=None,
        weapons=[],
        model_groups=_nobz_groups(),
    )


def _nobz_state(group_wounds: dict, active: str | None = None) -> dict:
    """Build a Nobz unit-state with the given per-group HP pools (3 LP per model)."""
    group_models = {gid: -(-pool // 3) for gid, pool in group_wounds.items()}  # ceil
    return {
        "current_wounds": sum(group_wounds.values()),
        "models": sum(group_models.values()),
        "models_initial": 5,
        "destroyed": False,
        "in_melee": False,
        "lost_models_this_turn": 0,
        "melee_with": [],
        "group_models": group_models,
        "group_wounds": dict(group_wounds),
        "damage_active_group_id": active,
    }


def _nobz_session(state: dict) -> _S:
    return _make_session(first_player="Orks", second_player="Necrons", p1_units={NOBZ: state})


def test_select_damage_target_group_sets_state() -> None:
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 6, "nob_slugga": 3})
    _nobz_session(state)
    select_damage_target_group(NOBZ, "Orks", "nob_saw")
    assert state["damage_active_group_id"] == "nob_saw"


def test_select_damage_target_group_invalid_group_raises() -> None:
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 6, "nob_slugga": 3})
    _nobz_session(state)
    with pytest.raises(ValueError):
        select_damage_target_group(NOBZ, "Orks", "nob_does_not_exist")


def test_get_locked_group_returns_none_when_no_wounded() -> None:
    """All pools are integer multiples of 3 LP — every front model is intact."""
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 6, "nob_slugga": 3})
    _nobz_session(state)
    assert get_locked_group(NOBZ, "Orks", _nobz_unit()) is None


def test_get_locked_group_returns_wounded_group() -> None:
    """nob_saw pool 4 = one intact (3) + one wounded (1) model → locked."""
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 4, "nob_slugga": 3})
    _nobz_session(state)
    assert get_locked_group(NOBZ, "Orks", _nobz_unit()) == "nob_saw"


def test_lock_invariante_apply_damage_wrong_group_raises() -> None:
    """With nob_saw locked, directing damage to another group must raise."""
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 4, "nob_slugga": 3}, active="nob_klaw")
    _nobz_session(state)
    with pytest.raises(ValueError):
        apply_damage(NOBZ, "Orks", 2, _nobz_unit(), mortal=False)


def test_lock_invariante_apply_damage_locked_group_allowed() -> None:
    """Directing damage to the locked group itself is allowed and kills its model."""
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 4, "nob_slugga": 3}, active="nob_saw")
    _nobz_session(state)
    apply_damage(NOBZ, "Orks", 1, _nobz_unit(), mortal=False)
    assert state["group_wounds"]["nob_saw"] == 3  # wounded model removed, one intact left
    assert state["group_wounds"]["nob_klaw"] == 6  # other groups untouched


def test_directed_damage_reduces_only_chosen_group() -> None:
    """Defender's chosen group takes the hit; sibling groups stay untouched."""
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 6, "nob_slugga": 3}, active="nob_klaw")
    _nobz_session(state)
    apply_damage(NOBZ, "Orks", 3, _nobz_unit(), mortal=False)
    assert state["group_wounds"]["nob_klaw"] == 3
    assert state["group_wounds"]["nob_saw"] == 6
    assert state["group_wounds"]["nob_slugga"] == 3


def test_mortal_wound_overflow_ignores_lock() -> None:
    """mortal=True bypasses the lock and spills across group boundaries."""
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 4, "nob_slugga": 3}, active="nob_klaw")
    _nobz_session(state)
    # No ValueError despite the active group differing from the locked one.
    apply_damage(NOBZ, "Orks", 5, _nobz_unit(), mortal=True)
    assert state["current_wounds"] == 6 + 4 + 3 - 5


def test_single_group_unit_no_interactive_ui_needed() -> None:
    """A homogeneous single-group unit has exactly one active subgroup → no choice."""
    state = _nobz_state({"nob_klaw": 6})
    active_groups = [gid for gid, n in state["group_models"].items() if n > 0]
    assert len(active_groups) == 1


# ---------------------------------------------------------------------------
# adjust_cp — line 52
# ---------------------------------------------------------------------------


def test_adjust_cp_increases_cp() -> None:
    session = _make_session(cp={"Necrons": 3, "Orks": 4})
    _mut.adjust_cp("Necrons", 2)
    assert session["cp"]["Necrons"] == 5


def test_adjust_cp_does_not_go_below_zero() -> None:
    session = _make_session(cp={"Necrons": 1, "Orks": 4})
    _mut.adjust_cp("Necrons", -5)
    assert session["cp"]["Necrons"] == 0


# ---------------------------------------------------------------------------
# _front_group_hp — lines 89-97
# (indirect via apply_damage without resolved=True and without directed target)
# ---------------------------------------------------------------------------


def test_apply_damage_group_wounds_without_directed_caps_to_front_model() -> None:
    """Without a directed active group, damage is capped to the front model's HP."""
    sk = _silent_king()
    state = _gs._unit_state(sk, 3)
    # Start at full (30 HP): Menhir 1 = 7 HP, Menhir 2 = 7 HP, Szarekh = 16 HP
    _make_session(p1_units={SILENT_KING: state})
    # resolved=False → front-model cap applies; Menhir front-model = 7 LP
    apply_damage(SILENT_KING, "Necrons", 100, _silent_king(), resolved=False)
    # Only 7 damage (front Menhir) should be applied
    assert state["group_wounds"]["triarchal_menhirs"] == 7
    assert state["group_wounds"]["szarekh"] == 16


def test_front_group_hp_returns_zero_when_all_groups_empty() -> None:
    """_front_group_hp returns 0 when no group has remaining HP."""
    from gameMechanic.unit_mutations import _front_group_hp

    sk = _silent_king()
    state = _gs._unit_state(sk, 3)
    state["group_wounds"] = {"triarchal_menhirs": 0, "szarekh": 0}
    assert _front_group_hp(state, sk) == 0


def test_front_group_hp_returns_full_wval_when_model_intact() -> None:
    """_front_group_hp returns wval when the front model is not partially wounded."""
    from gameMechanic.unit_mutations import _front_group_hp

    sk = _silent_king()
    state = _gs._unit_state(sk, 3)
    # Menhirs at exactly 2 full models (14), Szarekh full (16)
    state["group_wounds"] = {"triarchal_menhirs": 14, "szarekh": 16}
    assert _front_group_hp(state, sk) == 7  # menhir wval = 7, no partial


def test_front_group_hp_returns_partial_when_model_partly_wounded() -> None:
    """_front_group_hp returns the remaining partial HP of a partly wounded model."""
    from gameMechanic.unit_mutations import _front_group_hp

    sk = _silent_king()
    state = _gs._unit_state(sk, 3)
    # One Menhir at 3 of 7 HP remaining (partly wounded)
    state["group_wounds"] = {"triarchal_menhirs": 3, "szarekh": 16}
    assert _front_group_hp(state, sk) == 3


# ---------------------------------------------------------------------------
# _group_front_hp — lines 147, 150 (group is None / remaining <= 0)
# ---------------------------------------------------------------------------


def test_group_front_hp_returns_zero_when_pool_empty() -> None:
    """_group_front_hp returns 0 when the group's HP pool is 0."""
    from gameMechanic.unit_mutations import _group_front_hp

    sk = _silent_king()
    state = _gs._unit_state(sk, 3)
    state["group_wounds"] = {"triarchal_menhirs": 0, "szarekh": 16}
    assert _group_front_hp(state, sk, "triarchal_menhirs") == 0


def test_group_front_hp_returns_zero_for_unknown_group_id() -> None:
    """_group_front_hp returns 0 for a group_id not in unit.model_groups."""
    from gameMechanic.unit_mutations import _group_front_hp

    sk = _silent_king()
    state = _gs._unit_state(sk, 3)
    assert _group_front_hp(state, sk, "nonexistent_group") == 0


# ---------------------------------------------------------------------------
# apply_damage group_wounds path: no directed target AND no resolved → uses _front_group_hp
# line 191
# ---------------------------------------------------------------------------


def test_directed_group_mortal_wound_spills_freely() -> None:
    """mortal=True with group_wounds but no directed group uses priority spill (line 191)."""
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 6, "nob_slugga": 3})
    _nobz_session(state)
    # No active group, mortal=True → spills across boundaries, no cap
    apply_damage(NOBZ, "Orks", 7, _nobz_unit(), mortal=True)
    assert state["current_wounds"] == 6 + 6 + 3 - 7


# ---------------------------------------------------------------------------
# apply_damage: destroyed group_wounds unit leaves melee — line 194
# ---------------------------------------------------------------------------


def test_apply_damage_group_wounds_destroyed_leaves_melee() -> None:
    """Destroying a group_wounds unit clears its melee engagement."""
    session = _make_session(
        first_player="Necrons",
        second_player="Orks",
        p1_units={SILENT_KING: _gs._unit_state(_silent_king(), 3)},
        p2_units={BOYZ: _unit()},
    )
    enter_melee(SILENT_KING, "Necrons", BOYZ, "Orks")
    assert session["p1_units"][SILENT_KING]["in_melee"] is True
    apply_damage(SILENT_KING, "Necrons", 30, _silent_king(), resolved=True)
    assert session["p1_units"][SILENT_KING]["in_melee"] is False
    assert session["p1_units"][SILENT_KING]["melee_with"] == []


# ---------------------------------------------------------------------------
# apply_damage: destroyed regular unit leaves melee — line 220
# ---------------------------------------------------------------------------


def test_apply_damage_regular_destroyed_leaves_melee() -> None:
    """Destroying a regular (non-group-wounds) unit in melee calls leave_melee."""
    session = _two_unit_session()
    enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["p1_units"][OVERLORD]["in_melee"] is True
    apply_damage(OVERLORD, "Necrons", 99, _overlord(), mortal=True)
    assert session["p1_units"][OVERLORD]["destroyed"] is True
    assert session["p1_units"][OVERLORD]["in_melee"] is False


# ---------------------------------------------------------------------------
# heal_unit: group_wounds path, _restore_group_models skips full groups — line 237
# ---------------------------------------------------------------------------


def test_restore_group_models_skips_already_full_group() -> None:
    """Healing a fully-intact group leaves it at its maximum count."""
    from gameMechanic.unit_mutations import _restore_group_models

    groups = [
        ModelGroup(id="ork_boy", name_en="Ork Boy", count=9, weapons=[], priority=1),
        ModelGroup(id="boss_nob", name_en="Boss Nob", count=1, weapons=[], priority=2),
    ]
    group_models = {"ork_boy": 9, "boss_nob": 0}  # ork boys full, nob dead
    _restore_group_models(group_models, 2, groups)
    assert group_models["ork_boy"] == 9  # full → skipped
    assert group_models["boss_nob"] == 1  # restored first (lower priority = died first)


# ---------------------------------------------------------------------------
# flee_models with group_wounds — lines 363-375
# ---------------------------------------------------------------------------


def _silent_king_with_turn_flags() -> dict:
    state = _gs._unit_state(_silent_king(), 3)
    state["turn_flags"] = {"morale_tested": False}
    state["fled_models_this_turn"] = 0
    return state


def test_flee_models_group_wounds_removes_wound_pools() -> None:
    """flee_models with group_wounds reduces the wound pools and recomputes state."""
    state = _silent_king_with_turn_flags()
    _make_session(p1_units={SILENT_KING: state})
    _mut.flee_models(SILENT_KING, "Necrons", 1, _silent_king())
    # 1 model fled = 1 Menhir (priority=1), wval=7 → pool drops by 7
    assert state["group_wounds"]["triarchal_menhirs"] == 7
    assert state["group_models"]["triarchal_menhirs"] == 1
    assert state["fled_models_this_turn"] == 1
    assert state["turn_flags"]["morale_tested"] is True


def test_flee_models_group_wounds_sets_morale_tested() -> None:
    """flee_models always sets morale_tested=True for the group_wounds path."""
    state = _silent_king_with_turn_flags()
    _make_session(p1_units={SILENT_KING: state})
    _mut.flee_models(SILENT_KING, "Necrons", 0, _silent_king())
    assert state["turn_flags"]["morale_tested"] is True


# ---------------------------------------------------------------------------
# set_in_melee — lines 403-404
# ---------------------------------------------------------------------------


def test_set_in_melee_sets_value_true() -> None:
    session = _two_unit_session()
    _mut.set_in_melee(OVERLORD, "Necrons", True)
    assert session["p1_units"][OVERLORD]["in_melee"] is True


def test_set_in_melee_sets_value_false() -> None:
    session = _two_unit_session()
    session["p1_units"][OVERLORD]["in_melee"] = True
    _mut.set_in_melee(OVERLORD, "Necrons", False)
    assert session["p1_units"][OVERLORD]["in_melee"] is False


# ---------------------------------------------------------------------------
# apply_mortal_wounds — line 417
# ---------------------------------------------------------------------------


def test_apply_mortal_wounds_delegates_to_apply_damage_mortal() -> None:
    """apply_mortal_wounds applies damage with mortal=True (bypasses front-model cap)."""
    session = _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    _mut.apply_mortal_wounds(WARRIORS, "Necrons", 3, _warriors())
    state = session["p1_units"][WARRIORS]
    assert state["current_wounds"] == 7
    assert state["models"] == 7


# ---------------------------------------------------------------------------
# reset_turn_flags — lines 441-444
# ---------------------------------------------------------------------------


def test_reset_turn_flags_clears_all_flags() -> None:
    """reset_turn_flags sets every boolean flag in turn_flags to False."""
    session = _two_unit_session()
    session["p1_units"][OVERLORD]["turn_flags"]["charged"] = True
    session["p1_units"][OVERLORD]["turn_flags"]["shot"] = True
    _mut.reset_turn_flags(OVERLORD, "Necrons")
    flags = session["p1_units"][OVERLORD]["turn_flags"]
    assert all(v is False for v in flags.values())
