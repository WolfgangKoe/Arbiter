"""Tests for unitMutations.py: apply_damage, heal_unit, enter_melee, leave_melee,
set_charged, set_movement_status."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.gameState as _gs  # noqa: E402
import gameMechanic.unitMutations as _mut  # noqa: E402
from gameMechanic.abilityEngine import (  # noqa: E402
    find_unit_ability_by_effect,
    resolve_explode_effect,
)
from gameMechanic.gameState import next_phase  # noqa: E402
from gameMechanic.unitMutations import (  # noqa: E402
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
    from gameMechanic.unitMutations import unit_max_hp

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
# B-123 — directed x resolved x locked x mortal matrix + S166 regression
#
# Root cause (S166): _apply_directed_group_damage discarded any damage beyond
# the chosen group's own pool instead of spilling to the next group, and
# get_locked_group only locked a PARTIALLY wounded front model — so a
# full-health Silent King let the UI direct damage straight to Szarekh,
# skipping the Codex "Triarchal Menhir" rule (Menhirs must be allocated first
# while any remain). Fixed generically via unit.has_per_group_wounds() — the
# Silent King is the only unit in the data with heterogeneous per-group
# wounds (Szarekh 16 vs. Menhirs 7), so the forced front-lock cannot fire for
# homogeneous multi-group units like Ork Boyz/Nobz, preserving their K3 free
# first-choice.
# ---------------------------------------------------------------------------


def test_get_locked_group_forces_front_group_before_any_wound_on_hetero_unit() -> None:
    """Per-group wound values differ (Szarekh 16 vs. Menhirs 7) — the Codex
    'Triarchal Menhir' rule forces allocation onto the front (lowest-priority)
    group from full health, not only once a model is already wounded."""
    sk = _silent_king()
    _sk_session()
    assert get_locked_group(SILENT_KING, "Necrons", sk) == "triarchal_menhirs"


def test_get_locked_group_none_for_homogeneous_group_at_full_health() -> None:
    """K3 — a homogeneous multi-group unit (every group has the same
    per-model wounds) has no forced front lock at full health."""
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 6, "nob_slugga": 3})
    _nobz_session(state)
    assert get_locked_group(NOBZ, "Orks", _nobz_unit()) is None


def test_apply_damage_szarekh_cannot_be_chosen_before_menhirs_die() -> None:
    """Directing damage at Szarekh while Menhirs are alive must raise — this
    is the exact S166/B-123 root cause (UI could pick Szarekh at full health)."""
    _sk_session()
    select_damage_target_group(SILENT_KING, "Necrons", "szarekh")
    with pytest.raises(ValueError):
        apply_damage(SILENT_KING, "Necrons", 5, _silent_king(), resolved=True)


def test_get_locked_group_none_once_only_one_group_alive() -> None:
    """Once Menhirs are gone, only Szarekh remains — trivial single-group
    allocation, no lock needed regardless of has_per_group_wounds."""
    session = _sk_session()
    apply_damage(SILENT_KING, "Necrons", 14, _silent_king(), resolved=True)  # kills both Menhirs
    assert session["p1_units"][SILENT_KING]["group_wounds"]["triarchal_menhirs"] == 0
    assert get_locked_group(SILENT_KING, "Necrons", _silent_king()) is None


def test_apply_damage_directed_resolved_regression_s166_26_damage() -> None:
    """S166 regression: 26 damage on a full Silent King (30 HP total) used to
    destroy only the Menhirs (14 HP) and leave Szarekh untouched at 16/16 —
    the directed branch discarded everything beyond the chosen group's pool."""
    session = _sk_session()
    select_damage_target_group(SILENT_KING, "Necrons", "triarchal_menhirs")
    apply_damage(SILENT_KING, "Necrons", 26, _silent_king(), resolved=True)
    state = session["p1_units"][SILENT_KING]
    assert state["group_wounds"]["triarchal_menhirs"] == 0
    assert state["group_wounds"]["szarekh"] == 4  # 30 - 26, Szarekh now took damage
    assert state["destroyed"] is False


def test_apply_damage_directed_resolved_grenzfall_destroys_unit_outright() -> None:
    """Grenzfall: directed damage covering the WHOLE unit's pool (30) destroys
    it outright — the unit is fully destructible via a single directed apply,
    not capped at the first chosen group."""
    session = _sk_session()
    select_damage_target_group(SILENT_KING, "Necrons", "triarchal_menhirs")
    apply_damage(SILENT_KING, "Necrons", 30, _silent_king(), resolved=True)
    state = session["p1_units"][SILENT_KING]
    assert state["destroyed"] is True
    assert state["models"] == 0


def test_apply_damage_directed_not_resolved_overflow_still_lost_within_one_attack() -> None:
    """K1 — a SINGLE attack's excess is still lost, not spilled: resolved=False
    caps damage to the front model's HP before the directed branch runs, so a
    5-damage single hit on an intact 7-HP Menhir front model kills it without
    touching Szarekh at all."""
    session = _sk_session()
    select_damage_target_group(SILENT_KING, "Necrons", "triarchal_menhirs")
    apply_damage(SILENT_KING, "Necrons", 100, _silent_king(), resolved=False)
    state = session["p1_units"][SILENT_KING]
    assert state["group_wounds"]["triarchal_menhirs"] == 7  # only the front Menhir model died
    assert state["group_wounds"]["szarekh"] == 16  # untouched — single-attack excess is lost


def test_directed_resolved_overflow_spills_for_homogeneous_groups_too() -> None:
    """The overflow fix is not limited to forced-allocation units — a
    homogeneous multi-group unit's freely-chosen group also spills once its
    own pool is exhausted (resolved=True total covering multiple attacks)."""
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 6, "nob_slugga": 3}, active="nob_klaw")
    _nobz_session(state)
    apply_damage(NOBZ, "Orks", 9, _nobz_unit(), resolved=True)
    assert state["group_wounds"]["nob_klaw"] == 0
    assert state["group_wounds"]["nob_saw"] == 3  # 9 - 6 overflow lands here (next priority)
    assert state["group_wounds"]["nob_slugga"] == 3  # untouched


def test_directed_resolved_overflow_from_locked_group_continues_spill() -> None:
    """directed x resolved x locked x normal: a wounded-but-alive front model
    still binds the defender's choice (K2 Zugzwang), but once resolved damage
    exceeds even that model's whole group pool, the remainder keeps killing
    further groups instead of vanishing."""
    state = _nobz_state({"nob_klaw": 1, "nob_saw": 6, "nob_slugga": 3}, active="nob_klaw")
    _nobz_session(state)
    apply_damage(NOBZ, "Orks", 4, _nobz_unit(), resolved=True)
    assert state["group_wounds"]["nob_klaw"] == 0
    assert state["group_wounds"]["nob_saw"] == 3  # 4 - 1 overflow
    assert state["group_wounds"]["nob_slugga"] == 3  # untouched


def test_directed_mortal_resolved_ignores_active_and_lock() -> None:
    """directed x resolved x locked x mortal: mortal=True bypasses both the
    directed active group and any front lock, regardless of resolved — mortal
    wounds always use the plain priority spill (K4/K5)."""
    state = _nobz_state({"nob_klaw": 1, "nob_saw": 6, "nob_slugga": 3}, active="nob_klaw")
    _nobz_session(state)
    apply_damage(NOBZ, "Orks", 4, _nobz_unit(), mortal=True, resolved=True)
    assert state["current_wounds"] == 1 + 6 + 3 - 4


def test_get_locked_group_free_choice_of_any_homogeneous_group_at_full_health() -> None:
    """K3 — homogeneous multi-group unit: the defender may freely choose ANY
    undamaged group first, even one that is not the lowest priority (e.g.
    picking nob_slugga, priority 3, before touching nob_klaw, priority 1)."""
    state = _nobz_state({"nob_klaw": 6, "nob_saw": 6, "nob_slugga": 3}, active="nob_slugga")
    _nobz_session(state)
    apply_damage(NOBZ, "Orks", 3, _nobz_unit(), mortal=False)
    assert state["group_wounds"]["nob_slugga"] == 0  # freely chosen group takes the hit
    assert state["group_wounds"]["nob_klaw"] == 6  # untouched, despite lower priority


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
    from gameMechanic.unitMutations import _front_group_hp

    sk = _silent_king()
    state = _gs._unit_state(sk, 3)
    state["group_wounds"] = {"triarchal_menhirs": 0, "szarekh": 0}
    assert _front_group_hp(state, sk) == 0


def test_front_group_hp_returns_full_wval_when_model_intact() -> None:
    """_front_group_hp returns wval when the front model is not partially wounded."""
    from gameMechanic.unitMutations import _front_group_hp

    sk = _silent_king()
    state = _gs._unit_state(sk, 3)
    # Menhirs at exactly 2 full models (14), Szarekh full (16)
    state["group_wounds"] = {"triarchal_menhirs": 14, "szarekh": 16}
    assert _front_group_hp(state, sk) == 7  # menhir wval = 7, no partial


def test_front_group_hp_returns_partial_when_model_partly_wounded() -> None:
    """_front_group_hp returns the remaining partial HP of a partly wounded model."""
    from gameMechanic.unitMutations import _front_group_hp

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
    from gameMechanic.unitMutations import _group_front_hp

    sk = _silent_king()
    state = _gs._unit_state(sk, 3)
    state["group_wounds"] = {"triarchal_menhirs": 0, "szarekh": 16}
    assert _group_front_hp(state, sk, "triarchal_menhirs") == 0


def test_group_front_hp_returns_zero_for_unknown_group_id() -> None:
    """_group_front_hp returns 0 for a group_id not in unit.model_groups."""
    from gameMechanic.unitMutations import _group_front_hp

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
    from gameMechanic.unitMutations import _restore_group_models

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


def test_vengeance_of_the_enchained_flow_trigger_resolve_apply(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """B-028c1 b1 (S169): Trigger (Silent King destroyed) -> resolve (gate) ->
    apply (mortal wounds land on the user-chosen target) end to end, using the
    real YAML ability + the real `apply_mortal_wounds` state mutation — no
    Streamlit involved.

    Superseded resolve_mortal_wounds_effect(ability) self-roll with
    resolve_explode_effect(ability, exploded=...): Vengeance of the Enchained
    migrated from effect.type: mortal_wounds to effect.type: explode
    (Explodes-Familie, Pflicht-Trigger) — the engine no longer rolls the D6
    gate itself ("App würfelt nicht"); the gate outcome and the mortal-wound
    count are both entered by the caller from a physical table roll. `wounds
    = 3` here stands in for that table-rolled per-target entry (b2's UI
    concern, not this function's).
    """
    _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    ability = find_unit_ability_by_effect(
        "necrons", "wh40k_9e.necrons.unit.the_silent_king", "explode"
    )
    assert ability is not None

    exploded = resolve_explode_effect(ability, exploded=True)
    assert exploded is True

    wounds = 3  # table-rolled damage entry (b2 UI concern), not engine-computed
    _mut.apply_mortal_wounds(WARRIORS, "Necrons", wounds, _warriors())
    state = _mut.st.session_state["p1_units"][WARRIORS]
    assert state["current_wounds"] == 7
    assert state["models"] == 7


# ---------------------------------------------------------------------------
# Direct-Apply undo — snapshot_unit_state / restore_unit_state /
# apply_explode_target_damage / undo_explode_target_damage /
# undo_all_explode_damage (S171, → docs/spec/design_system.md §1.6/§1.7)
# ---------------------------------------------------------------------------


def _explode_entry() -> dict:  # type: ignore[type-arg]
    return {"selected": [], "damage": {}, "applied": False, "snapshots": {}}


def test_apply_explode_target_damage_then_undo_restores_original_hp() -> None:
    """Direct-Apply round trip (§1.7): applying mortal wounds and then
    undoing that single target leaves current_wounds/models exactly where
    they started."""
    session = _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
                "melee_with": [],
            }
        }
    )
    entry = _explode_entry()
    _mut.apply_explode_target_damage(entry, WARRIORS, "Necrons", _warriors(), 3)
    state = session["p1_units"][WARRIORS]
    assert state["current_wounds"] == 7
    assert state["models"] == 7
    assert f"Necrons::{WARRIORS}" in entry["snapshots"]

    _mut.undo_explode_target_damage(entry, WARRIORS, "Necrons")
    state = session["p1_units"][WARRIORS]
    assert state["current_wounds"] == 10
    assert state["models"] == 10
    assert entry["snapshots"] == {}


def test_apply_explode_target_damage_reapply_uses_original_baseline() -> None:
    """Correcting an already-entered count (e.g. a typo) must not stack on
    top of the previous apply — every call restores the pre-round snapshot
    first, then reapplies the FULL new count from that clean baseline."""
    session = _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
                "melee_with": [],
            }
        }
    )
    entry = _explode_entry()
    _mut.apply_explode_target_damage(entry, WARRIORS, "Necrons", _warriors(), 3)
    _mut.apply_explode_target_damage(entry, WARRIORS, "Necrons", _warriors(), 7)
    state = session["p1_units"][WARRIORS]
    # 10 - 7, NOT 10 - 3 - 7 — a naive delta-apply would land on 0.
    assert state["current_wounds"] == 3
    assert state["models"] == 3

    _mut.undo_explode_target_damage(entry, WARRIORS, "Necrons")
    assert session["p1_units"][WARRIORS]["current_wounds"] == 10


def test_apply_explode_target_damage_destroys_and_undo_revives() -> None:
    """A lethal Direct-Apply count sets destroyed=True exactly like any other
    damage source (apply_damage); undoing it fully revives the unit —
    destroyed flag, HP and model count all restored."""
    session = _make_session(p1_units={OVERLORD: _unit()})  # current_wounds=5, models=1
    entry = _explode_entry()
    _mut.apply_explode_target_damage(entry, OVERLORD, "Necrons", _overlord(), 5)
    state = session["p1_units"][OVERLORD]
    assert state["destroyed"] is True
    assert state["current_wounds"] == 0
    assert state["models"] == 0

    _mut.undo_explode_target_damage(entry, OVERLORD, "Necrons")
    state = session["p1_units"][OVERLORD]
    assert state["destroyed"] is False
    assert state["current_wounds"] == 5
    assert state["models"] == 1


def test_undo_all_explode_damage_restores_every_touched_target() -> None:
    """Panel-level Reset (§1.7 footer / §1.6 pre-Confirm Lesart A): every
    target touched this round is restored, and the snapshot map is cleared
    so the panel is ready for a fresh selection."""
    session = _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
                "melee_with": [],
            }
        },
        p2_units={
            BOYZ: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
                "melee_with": [],
            }
        },
    )
    entry = _explode_entry()
    _mut.apply_explode_target_damage(entry, WARRIORS, "Necrons", _warriors(), 4)
    _mut.apply_explode_target_damage(entry, BOYZ, "Orks", _warriors(), 6)
    assert session["p1_units"][WARRIORS]["current_wounds"] == 6
    assert session["p2_units"][BOYZ]["current_wounds"] == 4

    _mut.undo_all_explode_damage(entry)

    assert session["p1_units"][WARRIORS]["current_wounds"] == 10
    assert session["p2_units"][BOYZ]["current_wounds"] == 10
    assert entry["snapshots"] == {}


def test_undo_explode_target_damage_leaves_other_targets_untouched() -> None:
    """Deselecting one target (row toggle-off) must undo only that target —
    a second, still-selected target's applied damage stays in place."""
    session = _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
                "melee_with": [],
            }
        },
        p2_units={
            BOYZ: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
                "melee_with": [],
            }
        },
    )
    entry = _explode_entry()
    _mut.apply_explode_target_damage(entry, WARRIORS, "Necrons", _warriors(), 4)
    _mut.apply_explode_target_damage(entry, BOYZ, "Orks", _warriors(), 6)

    _mut.undo_explode_target_damage(entry, WARRIORS, "Necrons")

    assert session["p1_units"][WARRIORS]["current_wounds"] == 10
    assert session["p2_units"][BOYZ]["current_wounds"] == 4
    assert list(entry["snapshots"]) == [f"Orks::{BOYZ}"]


def test_undo_explode_target_damage_restores_melee_on_both_sides() -> None:
    """A Direct-Apply mortal-wound kill on an engaged unit dissolves melee via
    apply_damage's leave_melee call (both sides' melee_with lists are
    mutated). undo_explode_target_damage's restore must not leave the enemy
    side stale — enter_melee re-establishes both directions from the
    snapshot's own melee_with list."""
    session = _two_unit_session()
    _mut.enter_melee(OVERLORD, "Necrons", BOYZ, "Orks")
    assert session["p1_units"][OVERLORD]["in_melee"] is True
    assert session["p2_units"][BOYZ]["in_melee"] is True

    entry = _explode_entry()
    _mut.apply_explode_target_damage(entry, OVERLORD, "Necrons", _overlord(), 5)
    assert session["p1_units"][OVERLORD]["destroyed"] is True
    # apply_damage's leave_melee dissolved the engagement on both sides.
    assert session["p2_units"][BOYZ]["melee_with"] == []
    assert session["p2_units"][BOYZ]["in_melee"] is False

    _mut.undo_explode_target_damage(entry, OVERLORD, "Necrons")

    assert session["p1_units"][OVERLORD]["destroyed"] is False
    assert session["p1_units"][OVERLORD]["in_melee"] is True
    assert [session["second_player"], BOYZ] in session["p1_units"][OVERLORD]["melee_with"]
    # Restored symmetrically — the enemy side must see the engagement again too.
    assert session["p2_units"][BOYZ]["in_melee"] is True
    assert ["Necrons", OVERLORD] in session["p2_units"][BOYZ]["melee_with"]


# ---------------------------------------------------------------------------
# reopen_explode_target_panel — post-Confirm correction (S171,
# → docs/spec/design_system.md §1.6 Lesart A / §1.7 "Korrektur nach Confirm")
# ---------------------------------------------------------------------------


def test_reopen_explode_target_panel_flips_applied_to_false() -> None:
    """Reopening the panel after Confirm must reconstruct the exact
    pre-Confirm panel state: selections, entered counts and the Direct-Apply
    snapshot baseline all stay untouched — only "applied" flips back."""
    entry = _explode_entry()
    entry["applied"] = True
    entry["selected"] = ["Necrons::warriors"]
    entry["damage"] = {"Necrons::warriors": 3}
    entry["snapshots"] = {"Necrons::warriors": {"current_wounds": 10}}

    _mut.reopen_explode_target_panel(entry)

    assert entry["applied"] is False
    assert entry["selected"] == ["Necrons::warriors"]
    assert entry["damage"] == {"Necrons::warriors": 3}
    assert entry["snapshots"] == {"Necrons::warriors": {"current_wounds": 10}}


def test_reopen_explode_target_panel_does_not_undo_live_damage() -> None:
    """The mortal wounds Direct-Apply already landed on the target — reopening
    the panel is a pure UI-state return, not an undo. A fresh
    apply_explode_target_damage() call or the panel's own Reset is what
    corrects the live HP, same as any other in-panel correction."""
    session = _make_session(
        p1_units={
            WARRIORS: {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
                "melee_with": [],
            }
        }
    )
    entry = _explode_entry()
    _mut.apply_explode_target_damage(entry, WARRIORS, "Necrons", _warriors(), 3)
    entry["applied"] = True

    _mut.reopen_explode_target_panel(entry)

    assert session["p1_units"][WARRIORS]["current_wounds"] == 7
    assert entry["applied"] is False


# ---------------------------------------------------------------------------
# dice_notation_max — explode target panel's mortal-wounds cap (B-126,
# → gameObjects/ability.py:44 effect.damage dice notation)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("notation", "expected"),
    [
        ("D6", 6),
        ("D3", 3),
        ("1", 1),
        ("6", 6),
        (None, None),
        ("2D6", None),
        ("", None),
    ],
)
def test_dice_notation_max_resolves_expected_cap(notation, expected) -> None:  # type: ignore[no-untyped-def]
    assert _mut.dice_notation_max(notation) == expected


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


# ---------------------------------------------------------------------------
# activate_morale_auto_pass / confirm_morale_auto_pass — Insane Bravery (R-MORALE-09)
# ---------------------------------------------------------------------------


def test_activate_morale_auto_pass_sets_flag() -> None:
    session = _two_unit_session()
    _mut.activate_morale_auto_pass(OVERLORD, "Necrons")
    assert session["p1_units"][OVERLORD]["turn_flags"]["morale_auto_pass"] is True


def test_confirm_morale_auto_pass_marks_tested_and_clears_flag() -> None:
    session = _two_unit_session()
    session["p1_units"][OVERLORD]["turn_flags"]["morale_auto_pass"] = True
    _mut.confirm_morale_auto_pass(OVERLORD, "Necrons")
    flags = session["p1_units"][OVERLORD]["turn_flags"]
    assert flags["morale_tested"] is True
    assert flags["morale_auto_pass"] is False


def test_confirm_morale_auto_pass_does_not_touch_models() -> None:
    """No dice, no models flee — only the two turn_flags bookkeeping fields change."""
    session = _two_unit_session()
    _mut.confirm_morale_auto_pass(OVERLORD, "Necrons")
    state = session["p1_units"][OVERLORD]
    assert state["models"] == 1
    assert state["destroyed"] is False


# ---------------------------------------------------------------------------
# activate_desperate_breakout / apply_desperate_breakout_casualties /
# resolve_desperate_breakout — Desperate Breakout (R-MOVE-14)
# ---------------------------------------------------------------------------


def _melee_warriors_state(models: int = 10) -> dict:
    return {
        "current_wounds": models,
        "models": models,
        "destroyed": False,
        "in_melee": True,
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
            "desperate_breakout_pending": False,
        },
    }


def test_activate_desperate_breakout_sets_pending_flag() -> None:
    session = _make_session(p1_units={WARRIORS: _melee_warriors_state()})
    _mut.activate_desperate_breakout(WARRIORS, "Necrons")
    assert session["p1_units"][WARRIORS]["turn_flags"]["desperate_breakout_pending"] is True


def test_apply_desperate_breakout_casualties_removes_models() -> None:
    session = _make_session(p1_units={WARRIORS: _melee_warriors_state(models=10)})
    _mut.apply_desperate_breakout_casualties(WARRIORS, "Necrons", 3, _warriors())
    state = session["p1_units"][WARRIORS]
    assert state["models"] == 7
    assert state["current_wounds"] == 7
    assert state["lost_models_this_turn"] == 3


def test_apply_desperate_breakout_casualties_zero_is_noop() -> None:
    session = _make_session(p1_units={WARRIORS: _melee_warriors_state(models=10)})
    _mut.apply_desperate_breakout_casualties(WARRIORS, "Necrons", 0, _warriors())
    state = session["p1_units"][WARRIORS]
    assert state["models"] == 10
    assert state["lost_models_this_turn"] == 0


def test_apply_desperate_breakout_casualties_does_not_set_morale_tested() -> None:
    """Distinct from flee_models: these are real losses, not a Morale-test resolution."""
    session = _make_session(p1_units={WARRIORS: _melee_warriors_state(models=10)})
    _mut.apply_desperate_breakout_casualties(WARRIORS, "Necrons", 2, _warriors())
    assert session["p1_units"][WARRIORS]["turn_flags"].get("morale_tested") is not True


def test_resolve_desperate_breakout_sets_retreated_and_clears_pending() -> None:
    session = _make_session(p1_units={WARRIORS: _melee_warriors_state(models=10)})
    session["p1_units"][WARRIORS]["turn_flags"]["desperate_breakout_pending"] = True
    _mut.resolve_desperate_breakout(WARRIORS, "Necrons", 2, _warriors())
    state = session["p1_units"][WARRIORS]
    assert state["models"] == 8
    assert state["turn_flags"]["desperate_breakout_pending"] is False
    assert state["turn_flags"]["retreated"] is True
    assert state["movement_choice"] == "retreated"
    assert state["in_melee"] is False


def test_resolve_desperate_breakout_destroyed_unit_skips_fall_back() -> None:
    """A unit wiped out by the casualty roll cannot Fall Back — nothing left to move."""
    session = _make_session(p1_units={WARRIORS: _melee_warriors_state(models=3)})
    session["p1_units"][WARRIORS]["turn_flags"]["desperate_breakout_pending"] = True
    _mut.resolve_desperate_breakout(WARRIORS, "Necrons", 3, _warriors())
    state = session["p1_units"][WARRIORS]
    assert state["destroyed"] is True
    assert state["turn_flags"]["desperate_breakout_pending"] is False
    assert state["turn_flags"]["retreated"] is False
    assert state["movement_choice"] is None
