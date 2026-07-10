"""Integration tests for movement-phase state transitions.

Covers docs/spec/unit_states.md Sektion 2 (active player scenarios)
and Sektion 4 (forbidden transitions).

Tests verify both state mutations (set_movement_status, leave_melee)
and the constraint logic that the UI enforces (which movement options
are disabled or trigger an early-return for a given state).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.unit_mutations as _mut  # noqa: E402
from gameMechanic.unit_mutations import (  # noqa: E402
    reset_movement_to_stationary,
    set_movement_status,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _S(dict):
    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _make_session(**kwargs) -> _S:
    kwargs.setdefault("first_player", "Necrons")
    s = _S(**kwargs)
    _mut.st.session_state = s
    return s


def _unit(in_melee: bool = False) -> dict:
    return {
        "current_wounds": 5,
        "models": 1,
        "destroyed": False,
        "in_melee": in_melee,
        "in_reserve": False,
        "deployment": "normal",
        "lost_models_this_turn": 0,
        "movement_choice": "stationary",
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
        },
    }


def _session_with_two_units(n_in_melee: bool = False, o_in_melee: bool = False) -> _S:
    """Session with one Necron and one Ork unit (for melee tests)."""
    necron = _unit(in_melee=n_in_melee)
    ork = _unit(in_melee=o_in_melee)
    if n_in_melee and o_in_melee:
        necron["melee_with"] = [["Orks", "ork_1"]]
        ork["melee_with"] = [["Necrons", "necron_1"]]
    return _make_session(
        p1_units={"necron_1": necron},
        p2_units={"ork_1": ork},
    )


# ---------------------------------------------------------------------------
# Constraint helper — mirrors the disable logic in _active_movement
# ---------------------------------------------------------------------------


def _movement_blocked(value: str, unit_state: dict) -> bool:
    """Return True if the movement option `value` would be blocked for this unit.

    Mirrors the two gate-conditions in _active_movement:
    1. Early-return when already_retreated (no further movement at all).
    2. Disabled condition per button value.
    """
    flags = unit_state.get("turn_flags", {})
    already_retreated = flags.get("retreated", False)
    if already_retreated:
        return True  # All options blocked after retreat

    in_melee = unit_state.get("in_melee", False)
    return (value in ("moved", "advanced") and in_melee) or (value == "retreated" and not in_melee)


# ---------------------------------------------------------------------------
# Sektion 2 — Active player scenarios
# ---------------------------------------------------------------------------


def test_scenario_1_stationary_no_action():
    """Szenario 1: STATIONARY → stationary → no further actions → STATIONARY."""
    s = _make_session(p1_units={"u1": _unit()}, p2_units={})
    set_movement_status("u1", "Necrons", "stationary")
    state = s["p1_units"]["u1"]
    assert state["movement_choice"] == "stationary"
    assert not state["turn_flags"]["advanced"]
    assert not state["turn_flags"]["retreated"]


def test_scenario_2_stationary_then_shoot():
    """Szenario 2: STATIONARY → stationary → schießt. Shoot not blocked."""
    s = _make_session(p1_units={"u1": _unit()}, p2_units={})
    set_movement_status("u1", "Necrons", "stationary")
    state = s["p1_units"]["u1"]
    # STATIONARY unit may shoot (no flag blocks it)
    assert not state["turn_flags"]["retreated"]
    assert not state["turn_flags"]["advanced"]


def test_scenario_3_normal_move():
    """Szenario 3: STATIONARY → MOVED."""
    s = _make_session(p1_units={"u1": _unit()}, p2_units={})
    set_movement_status("u1", "Necrons", "moved")
    state = s["p1_units"]["u1"]
    assert state["movement_choice"] == "moved"
    assert not state["turn_flags"]["advanced"]
    assert not state["turn_flags"]["retreated"]


def test_scenario_8_advanced_sets_flag():
    """Szenario 8: STATIONARY → ADVANCED sets advanced flag."""
    s = _make_session(p1_units={"u1": _unit()}, p2_units={})
    set_movement_status("u1", "Necrons", "advanced")
    state = s["p1_units"]["u1"]
    assert state["movement_choice"] == "advanced"
    assert state["turn_flags"]["advanced"]
    assert not state["turn_flags"]["retreated"]


def test_scenario_9_in_melee_stationary_stationary_allowed():
    """Szenario 9: IN MELEE → stationary is the only valid non-retreat option."""
    s = _session_with_two_units(n_in_melee=True, o_in_melee=True)
    state = s["p1_units"]["necron_1"]
    assert not _movement_blocked("stationary", state)
    assert _movement_blocked("moved", state)
    assert _movement_blocked("advanced", state)
    assert not _movement_blocked("retreated", state)


def test_scenario_11_retreat_from_melee_clears_in_melee():
    """Szenario 11: IN MELEE → RETREATED clears in_melee and sets retreated flag."""
    s = _session_with_two_units(n_in_melee=True, o_in_melee=True)
    set_movement_status("necron_1", "Necrons", "retreated")
    necron = s["p1_units"]["necron_1"]
    assert necron["movement_choice"] == "retreated"
    assert necron["turn_flags"]["retreated"]
    assert not necron["in_melee"]
    assert necron["melee_with"] == []


def test_scenario_11_retreat_also_clears_enemy_melee_link():
    """Szenario 11: When Necron retreats, Ork's melee_with is also cleared."""
    s = _session_with_two_units(n_in_melee=True, o_in_melee=True)
    set_movement_status("necron_1", "Necrons", "retreated")
    ork = s["p2_units"]["ork_1"]
    assert not ork["in_melee"]
    assert ork["melee_with"] == []


def test_scenario_12_reserve_round1_not_blocked_by_movement_constraints():
    """Szenario 12: IN RESERVE (R1) — unit stays in reserve (UI shows caption, no buttons)."""
    unit = _unit()
    unit["in_reserve"] = True
    s = _make_session(p1_units={"u1": unit}, p2_units={})
    # Reserve units are handled by _render_reinforcements_step, not _active_movement.
    # _active_movement returns early when in_reserve=True (no constraint check needed).
    assert s["p1_units"]["u1"]["in_reserve"]


def test_scenario_13_deploy_from_reserve_sets_moved():
    """Szenario 13: Deploy from reserve sets movement_choice='moved' (not 'advanced')."""
    from gameMechanic.unit_mutations import set_deployment

    unit = _unit()
    unit["in_reserve"] = True
    s = _make_session(p1_units={"u1": unit}, p2_units={})
    set_deployment("u1", "Necrons", "normal")
    set_movement_status("u1", "Necrons", "moved")
    state = s["p1_units"]["u1"]
    assert not state["in_reserve"]
    assert state["movement_choice"] == "moved"
    assert not state["turn_flags"]["advanced"]  # Deploy is MOVED, never ADVANCED


# ---------------------------------------------------------------------------
# Sektion 4 — Forbidden transitions
# ---------------------------------------------------------------------------


def test_forbidden_retreated_then_no_further_movement():
    """RETREATED → all further movement options are blocked (early-return gate)."""
    s = _session_with_two_units(n_in_melee=True, o_in_melee=True)
    set_movement_status("necron_1", "Necrons", "retreated")
    state = s["p1_units"]["necron_1"]
    for value in ("moved", "advanced", "stationary", "retreated"):
        assert _movement_blocked(value, state), f"{value} should be blocked after retreat"


def test_forbidden_advanced_then_retreat_is_blocked():
    """ADVANCED → Retreat is blocked (not in_melee after advance)."""
    s = _make_session(p1_units={"u1": _unit()}, p2_units={})
    set_movement_status("u1", "Necrons", "advanced")
    state = s["p1_units"]["u1"]
    assert _movement_blocked("retreated", state)  # not in melee, can't retreat


def test_forbidden_in_melee_stationary_moved_blocked():
    """IN MELEE + stationary → MOVED is blocked."""
    s = _session_with_two_units(n_in_melee=True, o_in_melee=True)
    state = s["p1_units"]["necron_1"]
    assert _movement_blocked("moved", state)


def test_forbidden_in_melee_stationary_advanced_blocked():
    """IN MELEE + stationary → ADVANCED is blocked."""
    s = _session_with_two_units(n_in_melee=True, o_in_melee=True)
    state = s["p1_units"]["necron_1"]
    assert _movement_blocked("advanced", state)


def test_forbidden_not_in_melee_retreat_blocked():
    """Unit not in melee → RETREAT is blocked."""
    s = _make_session(p1_units={"u1": _unit()}, p2_units={})
    state = s["p1_units"]["u1"]
    assert _movement_blocked("retreated", state)


# ---------------------------------------------------------------------------
# Regression test — the Retreat → Stationary → Move bug
# ---------------------------------------------------------------------------


def test_regression_retreated_then_stationary_call_still_blocks_move():
    """Regression: calling set_movement_status('stationary') after retreat resets the
    retreated flag in the raw state, but the UI gate (_movement_blocked) catches this
    because it reads the retreated flag BEFORE the stationary call overwrites it.

    This test verifies that after a correct retreat, the flag is set,
    and that if the underlying mutation were called directly (simulating the bug),
    it would wrongly clear the flag — confirming the UI gate is load-bearing.
    """
    s = _session_with_two_units(n_in_melee=True, o_in_melee=True)

    # Step 1: Retreat — correct path
    set_movement_status("necron_1", "Necrons", "retreated")
    state = s["p1_units"]["necron_1"]
    assert state["turn_flags"]["retreated"], "retreated flag must be True after retreat"
    assert not state["in_melee"], "leave_melee must have been called"

    # Step 2: The UI gate must block all further movement
    for value in ("moved", "advanced", "stationary", "retreated"):
        assert _movement_blocked(value, state), f"UI gate must block '{value}' when retreated=True"

    # Step 3: Demonstrate the underlying mutation vulnerability
    # (the bug path — simulating a bypass of the UI gate)
    set_movement_status("necron_1", "Necrons", "stationary")
    state_after_bypass = s["p1_units"]["necron_1"]
    # The mutation itself resets the flag — this is why the UI gate is critical
    assert not state_after_bypass["turn_flags"][
        "retreated"
    ], "Raw mutation resets retreated flag — UI gate in _active_movement is essential"
    assert not _movement_blocked(
        "moved", state_after_bypass
    ), "Without the UI gate, MOVE would be wrongly enabled after bypass"


# ---------------------------------------------------------------------------
# Veil of Darkness (F7) — teleport removes the unit from melee
# ---------------------------------------------------------------------------


def _veil_session(**units) -> _S:
    """Session wired to the streamlit mocks that movementPhase + game_state use.

    movementPhase and game_state bind their own `import streamlit as st`; the
    teleport helpers read session_state through both, so set it on each.
    """
    import gameMechanic.game_state as gs
    import gameMechanic.movementPhase as mp

    s = _S(first_player="Necrons", **units)
    mp.st.session_state = s
    gs.st.session_state = s
    return s


def test_veil_teleport_clears_in_melee_and_stashes_prior_state():
    """F7: a teleported bearer is set up 9\"+ away, so in_melee must clear."""
    from gameMechanic.movementPhase import _lock_teleport_movement

    s = _veil_session(p1_units={"necron_1": _unit(in_melee=True)}, p2_units={})
    _lock_teleport_movement("necron_1", "Necrons")

    bearer = s["p1_units"]["necron_1"]
    assert bearer["in_melee"] is False
    assert bearer["turn_flags"]["movement_locked"] is True
    assert bearer["turn_flags"]["veil_prev_in_melee"] is True


def test_veil_teleport_from_outside_melee_stashes_false():
    from gameMechanic.movementPhase import _lock_teleport_movement

    s = _veil_session(p1_units={"necron_1": _unit(in_melee=False)}, p2_units={})
    _lock_teleport_movement("necron_1", "Necrons")

    bearer = s["p1_units"]["necron_1"]
    assert bearer["in_melee"] is False
    assert bearer["turn_flags"]["veil_prev_in_melee"] is False


def test_veil_undo_restores_prior_melee_state(monkeypatch):
    """Undo within the same turn must put the bearer back into melee."""
    import gameMechanic.movementPhase as mp

    s = _veil_session(p1_units={"necron_1": _unit(in_melee=True)}, p2_units={})
    monkeypatch.setattr(mp, "log_action", lambda *a, **k: None)
    mp.st.rerun = lambda *a, **k: None

    mp._lock_teleport_movement("necron_1", "Necrons")
    assert s["p1_units"]["necron_1"]["in_melee"] is False

    mp._undo_teleport("relic_x", "Necrons", {"round": 1})
    bearer = s["p1_units"]["necron_1"]
    assert bearer["in_melee"] is True
    assert bearer["turn_flags"]["movement_locked"] is False
    assert "veil_prev_in_melee" not in bearer["turn_flags"]


def test_veil_relic_yaml_carries_teleport_ui_texts():
    """INV-4b (S128): die DYNASTY-CORE-Dialogtexte kommen aus relics.yaml
    (prompt_text/selector_label), nicht mehr aus movementPhase.py."""
    from gameObjects.loader import load_relic_catalog

    veil = load_relic_catalog("necrons")["wh40k_9e.necrons.relic.schleier_der_finsternis"]
    assert "DYNASTY CORE" in veil["prompt_text"]
    assert "Once per battle" in veil["prompt_text"]
    assert "DYNASTY CORE" in veil["selector_label"]


def test_teleport_fallback_texts_are_faction_neutral():
    """Fallback-Texte in movementPhase dürfen kein Fraktions-Vokabular tragen."""
    import gameMechanic.movementPhase as mp

    assert "DYNASTY" not in mp._TELEPORT_PROMPT_FALLBACK
    assert "DYNASTY" not in mp._TELEPORT_SELECTOR_FALLBACK


# ---------------------------------------------------------------------------
# S133 K2 — "Stay Stationary" as a Reset button (reset_movement_to_stationary)
# ---------------------------------------------------------------------------


def test_reset_after_retreat_restores_stationary_and_melee_dependency():
    """Retreat → Reset: unit is 'stationary' again AND the in-melee dependency
    (melee_with + in_melee) reappears exactly as before Retreat was declared."""
    s = _session_with_two_units(n_in_melee=True, o_in_melee=True)

    set_movement_status("necron_1", "Necrons", "retreated")
    necron = s["p1_units"]["necron_1"]
    assert necron["in_melee"] is False
    assert necron["melee_with"] == []

    reset_movement_to_stationary("necron_1", "Necrons")
    necron = s["p1_units"]["necron_1"]
    ork = s["p2_units"]["ork_1"]

    assert necron["movement_choice"] == "stationary"
    assert necron["turn_flags"]["retreated"] is False
    assert necron["in_melee"] is True
    assert necron["melee_with"] == [["Orks", "ork_1"]]
    assert ork["in_melee"] is True
    assert ork["melee_with"] == [["Necrons", "necron_1"]]
    assert "pre_retreat_melee_with" not in necron["turn_flags"]


def test_reset_after_retreat_never_reopens_move_or_advance():
    """Reset always lands on 'stationary' — never a Retreated→Move/Advance path."""
    s = _session_with_two_units(n_in_melee=True, o_in_melee=True)
    set_movement_status("necron_1", "Necrons", "retreated")
    reset_movement_to_stationary("necron_1", "Necrons")
    state = s["p1_units"]["necron_1"]
    # Back in melee → the UI gate blocks MOVED/ADVANCED again, same as any
    # freshly in-melee unit — the pre-Retreat dependency is restored, not a
    # new bypass.
    assert _movement_blocked("moved", state)
    assert _movement_blocked("advanced", state)
    assert not _movement_blocked("retreated", state)


def test_reset_after_moved_is_plain_stationary_no_melee_side_effects():
    """Reset after a plain Move (never in melee) is a no-frills stationary reset."""
    s = _make_session(p1_units={"u1": _unit()}, p2_units={})
    set_movement_status("u1", "Necrons", "moved")
    reset_movement_to_stationary("u1", "Necrons")
    state = s["p1_units"]["u1"]
    assert state["movement_choice"] == "stationary"
    assert state["in_melee"] is False
    assert state["melee_with"] == []


def test_reset_after_advanced_clears_advanced_flag():
    """Reset after an Advance clears the advanced flag along with the choice."""
    s = _make_session(p1_units={"u1": _unit()}, p2_units={})
    set_movement_status("u1", "Necrons", "advanced")
    reset_movement_to_stationary("u1", "Necrons")
    state = s["p1_units"]["u1"]
    assert state["movement_choice"] == "stationary"
    assert state["turn_flags"]["advanced"] is False


# ---------------------------------------------------------------------------
# S133 K2 — Reinforcements gated behind "all field units resolved"
# ---------------------------------------------------------------------------


def test_all_field_units_resolved_false_when_a_unit_never_moved():
    import gameMechanic.movementPhase as mp

    unit_untouched = _unit()
    unit_untouched.pop("movement_choice", None)
    unit_untouched["movement_chosen"] = False
    reserve = _unit()
    reserve["in_reserve"] = True
    s = _veil_session(p1_units={"u1": unit_untouched, "u2": reserve}, p2_units={})
    assert mp._all_field_units_resolved("Necrons") is False
    assert s  # keep reference alive for clarity


def test_all_field_units_resolved_true_once_every_field_unit_chose():
    import gameMechanic.movementPhase as mp

    unit_a = _unit()
    unit_a["movement_chosen"] = True
    reserve = _unit()
    reserve["in_reserve"] = True
    _veil_session(p1_units={"u1": unit_a, "u2": reserve}, p2_units={})
    assert mp._all_field_units_resolved("Necrons") is True


def test_all_field_units_resolved_ignores_destroyed_units():
    import gameMechanic.movementPhase as mp

    destroyed = _unit()
    destroyed["destroyed"] = True
    destroyed["movement_chosen"] = False
    _veil_session(p1_units={"u1": destroyed}, p2_units={})
    assert mp._all_field_units_resolved("Necrons") is True


# ---------------------------------------------------------------------------
# S133 K2 item 1 — Advance re-roll GO-card state resolution (_advance_reroll_state)
#
# Pure decision function (no Streamlit) — direct unit tests, same spirit as
# test_go_card.py's HTML-output tests for the state→style mapping.
# ---------------------------------------------------------------------------


def _reroll_strat():
    from gameObjects.stratagem import Stratagem

    return Stratagem(
        id="wh40k_9e.shared.stratagem.command_re_roll",
        name_en="Command Re-Roll",
        cp_cost=1,
        phase=["movement"],
        stage="active",
        player="both",
        timing="phase_reactive",
        event="after_roll",
    )


def test_advance_reroll_state_locked_when_in_melee():
    from gameMechanic.movementPhase import _advance_reroll_state

    state, reason = _advance_reroll_state(_reroll_strat(), True, "advanced", 3, set(), set())
    assert state == "locked"
    assert reason == "unit is in melee"


def test_advance_reroll_state_locked_when_no_advance_roll_open():
    from gameMechanic.movementPhase import _advance_reroll_state

    state, reason = _advance_reroll_state(_reroll_strat(), False, "none", 3, set(), set())
    assert state == "locked"
    assert reason == "no Advance roll open"

    state, reason = _advance_reroll_state(_reroll_strat(), False, "moved", 3, set(), set())
    assert state == "locked"
    assert reason == "no Advance roll open"


def test_advance_reroll_state_ready_when_advanced_and_cp_available():
    from gameMechanic.movementPhase import _advance_reroll_state

    state, reason = _advance_reroll_state(_reroll_strat(), False, "advanced", 3, set(), set())
    assert state == "ready"
    assert reason is None


def test_advance_reroll_state_used_after_spend_while_window_open():
    from gameMechanic.movementPhase import _advance_reroll_state

    strat = _reroll_strat()
    used_ids = {strat.id}
    state, reason = _advance_reroll_state(strat, False, "advanced", 3, used_ids, set())
    assert state == "used"
    assert reason is None


def test_advance_reroll_state_locked_cp_insufficient_when_not_used():
    from gameMechanic.movementPhase import _advance_reroll_state

    strat = _reroll_strat()
    state, reason = _advance_reroll_state(strat, False, "advanced", 0, set(), set())
    assert state == "locked"
    assert reason == "CP insufficient"
