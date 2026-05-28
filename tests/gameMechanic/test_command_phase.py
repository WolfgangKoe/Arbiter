"""Tests for gameMechanic/commandPhase.py — pure logic only (no Streamlit UI)."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Stub streamlit before importing commandPhase
_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic.commandPhase import resolve_command_start  # noqa: E402
from gameMechanic.unit_mutations import apply_living_metal  # noqa: E402
from gameObjects.loader import load_army  # noqa: E402
from gameObjects.unit import Unit  # noqa: E402


def _make_unit(wounds: int, models_max: int, rules: list[str] | None = None) -> Unit:
    return Unit(
        id="test.unit",
        name_en="Test Unit",
        name_de="Test",
        faction="Necrons",
        subfaction=None,
        battlefield_role=["Troops"],
        keywords=["Necrons"],
        wounds=wounds,
        models_min=1,
        models_max=models_max,
        move='6"',
        bs="3+",
        ws="3+",
        strength=4,
        toughness=4,
        save=3,
        invuln_save=None,
        leadership=10,
        oc=2,
        fnp=None,
        rules=rules or [],
    )


# ---------------------------------------------------------------------------
# apply_living_metal — the critical scenarios
# ---------------------------------------------------------------------------


def test_apply_living_metal_scenario_a_dead_model_rest_full_no_heal() -> None:
    """Szenario A: 1 model dead, 2 alive at 3/3 LP → no heal (current == max_alive)."""
    unit = _make_unit(wounds=3, models_max=3)
    unit_state = {"current_wounds": 6, "models": 2, "destroyed": False}
    result = apply_living_metal(unit_state, unit)
    assert result is False
    assert unit_state["current_wounds"] == 6


def test_apply_living_metal_scenario_b_damaged_model_heals() -> None:
    """Szenario B: 1 dead, 1 at 2/3, 1 at 3/3 → +1 LP."""
    unit = _make_unit(wounds=3, models_max=3)
    unit_state = {"current_wounds": 5, "models": 2, "destroyed": False}
    result = apply_living_metal(unit_state, unit)
    assert result is True
    assert unit_state["current_wounds"] == 6


def test_apply_living_metal_scenario_c_all_alive_one_damaged_heals() -> None:
    """Szenario C: All 3 alive, 1 at 2/3 LP → +1 LP."""
    unit = _make_unit(wounds=3, models_max=3)
    unit_state = {"current_wounds": 8, "models": 3, "destroyed": False}
    result = apply_living_metal(unit_state, unit)
    assert result is True
    assert unit_state["current_wounds"] == 9


def test_apply_living_metal_scenario_d_overlord_heals() -> None:
    """Szenario D: Overlord at 4/5 LP → +1 LP → 5/5."""
    unit = _make_unit(wounds=5, models_max=1)
    unit_state = {"current_wounds": 4, "models": 1, "destroyed": False}
    result = apply_living_metal(unit_state, unit)
    assert result is True
    assert unit_state["current_wounds"] == 5


def test_apply_living_metal_full_hp_no_heal() -> None:
    """Unit at full HP — no heal."""
    unit = _make_unit(wounds=5, models_max=1)
    unit_state = {"current_wounds": 5, "models": 1, "destroyed": False}
    result = apply_living_metal(unit_state, unit)
    assert result is False
    assert unit_state["current_wounds"] == 5


def test_apply_living_metal_does_not_revive_dead_models() -> None:
    """1 model at full HP, 2 dead — no heal since current == max_alive (1 alive × 3 wounds)."""
    unit = _make_unit(wounds=3, models_max=3)
    unit_state = {"current_wounds": 3, "models": 1, "destroyed": False}
    result = apply_living_metal(unit_state, unit)
    assert result is False
    assert unit_state["current_wounds"] == 3


# ---------------------------------------------------------------------------
# resolve_command_start — integration
# ---------------------------------------------------------------------------


def _make_necron_state() -> dict:
    units = load_army("necrons")
    return {
        "active": "Necrons",
        "necron_units": {
            u.id: {
                "current_wounds": u.wounds * u.models_max,
                "models": u.models_max,
                "destroyed": False,
            }
            for u in units
        },
    }


def test_resolve_command_start_returns_living_metal() -> None:
    state = _make_necron_state()
    triggered = resolve_command_start(state)
    ids = [a.id for a, _ in triggered]
    assert "necrons.faction.living_metal" in ids


def test_resolve_command_start_ork_returns_empty() -> None:
    units = load_army("orks")
    state = {
        "active": "Orks",
        "ork_units": {
            u.id: {
                "current_wounds": u.wounds * u.models_max,
                "models": u.models_max,
                "destroyed": False,
            }
            for u in units
        },
    }
    triggered = resolve_command_start(state)
    assert triggered == []
