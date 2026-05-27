"""Tests for engine.py — pure logic functions and state transitions."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Stub streamlit before importing engine so no real Streamlit is needed.
_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import engine  # noqa: E402
from engine import apply_damage, heal_unit, next_phase, parse_dice, wound_threshold  # noqa: E402
from gameObjects.unit import Unit  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _S(dict):
    """Dict that also supports attribute-style access, mirroring st.session_state."""

    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _make_session(**kwargs: object) -> _S:
    s = _S(**kwargs)
    engine.st.session_state = s
    return s


def _unit_state_dict() -> dict:
    return {
        "current_wounds": 5,
        "models": 1,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "stationary",
        "lost_models_this_turn": 0,
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
        id="wh40k_9e.necrons.unit.overlord",
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
        id="wh40k_9e.necrons.unit.warriors",
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


# ---------------------------------------------------------------------------
# parse_dice
# ---------------------------------------------------------------------------


def test_parse_dice_fixed_integer() -> None:
    assert parse_dice("3") == 3


def test_parse_dice_fixed_integer_as_int() -> None:
    assert parse_dice(5) == 5  # type: ignore[arg-type]


def test_parse_dice_d6_in_range() -> None:
    for _ in range(60):
        assert 1 <= parse_dice("D6") <= 6


def test_parse_dice_2d6_in_range() -> None:
    for _ in range(60):
        assert 2 <= parse_dice("2D6") <= 12


def test_parse_dice_d3_in_range() -> None:
    for _ in range(60):
        assert 1 <= parse_dice("D3") <= 3


# ---------------------------------------------------------------------------
# wound_threshold
# ---------------------------------------------------------------------------


def test_wound_threshold_double_strength_wounds_on_2() -> None:
    assert wound_threshold(10, 5) == 2


def test_wound_threshold_greater_strength_wounds_on_3() -> None:
    assert wound_threshold(6, 5) == 3


def test_wound_threshold_equal_wounds_on_4() -> None:
    assert wound_threshold(5, 5) == 4


def test_wound_threshold_strength_half_toughness_wounds_on_6() -> None:
    assert wound_threshold(3, 6) == 6  # S*2 == T


def test_wound_threshold_strength_below_half_wounds_on_6() -> None:
    assert wound_threshold(2, 6) == 6  # S*2 < T


def test_wound_threshold_between_half_and_equal_wounds_on_5() -> None:
    assert wound_threshold(4, 6) == 5  # T/2 < S < T


# ---------------------------------------------------------------------------
# apply_damage
# ---------------------------------------------------------------------------


def test_apply_damage_1wound_models_caps_at_one_model() -> None:
    """3 regular damage on 1-wound models kills exactly 1 model — excess is lost per 9E rules."""
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.warriors": {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage("wh40k_9e.necrons.unit.warriors", "Necrons", 3, _warriors(), mortal=False)
    state = session["necron_units"]["wh40k_9e.necrons.unit.warriors"]
    assert state["current_wounds"] == 9
    assert state["models"] == 9
    assert state["destroyed"] is False


def test_apply_damage_1wound_models_successive_hits_kill_multiple() -> None:
    """Applying damage three times separately kills three warriors (one per hit)."""
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.warriors": {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    uid = "wh40k_9e.necrons.unit.warriors"
    apply_damage(uid, "Necrons", 3, _warriors(), mortal=False)
    apply_damage(uid, "Necrons", 3, _warriors(), mortal=False)
    apply_damage(uid, "Necrons", 3, _warriors(), mortal=False)
    state = session["necron_units"][uid]
    assert state["current_wounds"] == 7
    assert state["models"] == 7


def test_apply_damage_mortal_wounds_kill_multiple_1wound_models() -> None:
    """Mortal wounds bypass the spillover cap and can kill multiple 1-wound models."""
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.warriors": {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage("wh40k_9e.necrons.unit.warriors", "Necrons", 3, _warriors(), mortal=True)
    state = session["necron_units"]["wh40k_9e.necrons.unit.warriors"]
    assert state["current_wounds"] == 7
    assert state["models"] == 7


def test_apply_damage_multiwound_caps_damage_to_front_model() -> None:
    """5 damage on a partially wounded multi-wound unit only finishes the front model."""
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.skorpekh_destroyers": {
                "current_wounds": 7,
                "models": 3,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    # front_hp = 7 - (3-1)*3 = 1 → dmg capped to 1
    apply_damage(
        "wh40k_9e.necrons.unit.skorpekh_destroyers", "Necrons", 5, _skorpekh(), mortal=False
    )
    state = session["necron_units"]["wh40k_9e.necrons.unit.skorpekh_destroyers"]
    assert state["current_wounds"] == 6
    assert state["models"] == 2


def test_apply_damage_mortal_wound_bypasses_spillover_cap() -> None:
    """A mortal wound always removes exactly 1 wound regardless of model boundary."""
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.warriors": {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage("wh40k_9e.necrons.unit.warriors", "Necrons", 1, _warriors(), mortal=True)
    state = session["necron_units"]["wh40k_9e.necrons.unit.warriors"]
    assert state["current_wounds"] == 9
    assert state["models"] == 9


def test_apply_damage_single_model_reduces_lp_directly() -> None:
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.overlord": {
                "current_wounds": 5,
                "models": 1,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage("wh40k_9e.necrons.unit.overlord", "Necrons", 3, _overlord(), mortal=False)
    state = session["necron_units"]["wh40k_9e.necrons.unit.overlord"]
    assert state["current_wounds"] == 2
    assert state["models"] == 1
    assert state["destroyed"] is False


def test_apply_damage_destroys_unit_when_hp_reaches_zero() -> None:
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.overlord": {
                "current_wounds": 2,
                "models": 1,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        }
    )
    apply_damage("wh40k_9e.necrons.unit.overlord", "Necrons", 5, _overlord(), mortal=False)
    state = session["necron_units"]["wh40k_9e.necrons.unit.overlord"]
    assert state["destroyed"] is True
    assert state["current_wounds"] == 0
    assert state["models"] == 0


def test_apply_damage_tracks_lost_models_this_turn() -> None:
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.warriors": {
                "current_wounds": 10,
                "models": 10,
                "destroyed": False,
                "lost_models_this_turn": 2,
            }
        }
    )
    apply_damage("wh40k_9e.necrons.unit.warriors", "Necrons", 3, _warriors(), mortal=False)
    state = session["necron_units"]["wh40k_9e.necrons.unit.warriors"]
    assert state["lost_models_this_turn"] == 3  # 2 existing + 1 new (cap: only front model dies)


# ---------------------------------------------------------------------------
# heal_unit
# ---------------------------------------------------------------------------


def test_heal_unit_restores_wounds() -> None:
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.overlord": {
                "current_wounds": 3,
                "models": 1,
                "destroyed": False,
            }
        }
    )
    heal_unit("wh40k_9e.necrons.unit.overlord", "Necrons", 1, _overlord())
    assert session["necron_units"]["wh40k_9e.necrons.unit.overlord"]["current_wounds"] == 4


def test_heal_unit_caps_at_maximum_wounds() -> None:
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.overlord": {
                "current_wounds": 4,
                "models": 1,
                "destroyed": False,
            }
        }
    )
    heal_unit("wh40k_9e.necrons.unit.overlord", "Necrons", 10, _overlord())
    assert session["necron_units"]["wh40k_9e.necrons.unit.overlord"]["current_wounds"] == 5


def test_heal_unit_revives_destroyed_unit() -> None:
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.overlord": {
                "current_wounds": 0,
                "models": 0,
                "destroyed": True,
            }
        }
    )
    heal_unit("wh40k_9e.necrons.unit.overlord", "Necrons", 1, _overlord())
    state = session["necron_units"]["wh40k_9e.necrons.unit.overlord"]
    assert state["current_wounds"] == 1
    assert state["destroyed"] is False
    assert state["models"] == 1


def test_heal_unit_updates_model_count_for_multimodel() -> None:
    session = _make_session(
        necron_units={
            "wh40k_9e.necrons.unit.warriors": {
                "current_wounds": 7,
                "models": 7,
                "destroyed": False,
            }
        }
    )
    heal_unit("wh40k_9e.necrons.unit.warriors", "Necrons", 3, _warriors())
    state = session["necron_units"]["wh40k_9e.necrons.unit.warriors"]
    assert state["current_wounds"] == 10
    assert state["models"] == 10


# ---------------------------------------------------------------------------
# next_phase — state transitions and CP behaviour
# ---------------------------------------------------------------------------


def _phase_session(phase_idx: int, active: str, round_num: int = 1, cp: dict | None = None) -> _S:
    return _make_session(
        phase_idx=phase_idx,
        active=active,
        round=round_num,
        cp=cp if cp is not None else {"Necrons": 4, "Orks": 4},
        selected_unit=None,
        selected_target=None,
        necron_units={"u1": _unit_state_dict()},
        ork_units={"u2": _unit_state_dict()},
    )


def test_next_phase_setup_goes_to_command() -> None:
    session = _phase_session(phase_idx=0, active="Necrons")
    next_phase()
    assert session["phase_idx"] == 1


def test_next_phase_advances_index_within_turn() -> None:
    session = _phase_session(phase_idx=1, active="Necrons")
    next_phase()
    assert session["phase_idx"] == 2


def test_next_phase_switches_active_player_after_necrons_morale() -> None:
    session = _phase_session(phase_idx=7, active="Necrons")
    next_phase()
    assert session["active"] == "Orks"
    assert session["phase_idx"] == 1


def test_next_phase_increments_round_after_orks_morale() -> None:
    session = _phase_session(phase_idx=7, active="Orks", round_num=1)
    next_phase()
    assert session["active"] == "Necrons"
    assert session["round"] == 2


def test_next_phase_does_not_award_cp_on_player_switch() -> None:
    """CP is granted manually via the Command Phase button — next_phase must not add CP."""
    session = _phase_session(phase_idx=7, active="Orks", cp={"Necrons": 4, "Orks": 4})
    next_phase()
    assert session["cp"]["Necrons"] == 4
    assert session["cp"]["Orks"] == 4


def test_next_phase_resets_selected_unit_and_target() -> None:
    session = _make_session(
        phase_idx=1,
        active="Necrons",
        round=1,
        cp={"Necrons": 4, "Orks": 4},
        selected_unit=("Necrons", "wh40k_9e.necrons.unit.overlord"),
        selected_target=("Orks", "wh40k_9e.orks.unit.big_mek"),
        necron_units={"u1": _unit_state_dict()},
        ork_units={"u2": _unit_state_dict()},
    )
    next_phase()
    assert session["selected_unit"] is None
    assert session["selected_target"] is None
