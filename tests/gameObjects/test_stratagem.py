"""Tests for gameObjects/stratagem.py — stratagem_visibility() pure function."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameObjects.loader import load_stratagems  # noqa: E402
from gameObjects.stratagem import Stratagem, stratagem_visibility  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _strat(
    phase: str | list[str] = "shooting",
    stage: str = "active",
    cp_cost: int = 1,
    timing: str | None = None,
    sid: str = "test.strat",
) -> Stratagem:
    return Stratagem(
        id=sid,
        name_en="Test GO",
        cp_cost=cp_cost,
        phase=phase,
        stage=stage,
        player="active",
        timing=timing,
    )


def _vis(
    stratagem: Stratagem,
    cp: int = 5,
    current_phase: str = "shooting",
    current_stage: str = "active",
    used: set[str] | None = None,
    conditions_met: bool = True,
) -> str:
    return stratagem_visibility(
        stratagem,
        cp_available=cp,
        current_phase=current_phase,
        current_stage=current_stage,
        used_this_phase=used or set(),
        conditions_met=conditions_met,
    )


# ---------------------------------------------------------------------------
# Hidden conditions
# ---------------------------------------------------------------------------


class TestStratagemsHidden:
    def test_hidden_when_conditions_not_met(self) -> None:
        assert _vis(_strat(), conditions_met=False) == "hidden"

    def test_hidden_when_phase_reactive(self) -> None:
        assert _vis(_strat(timing="phase_reactive")) == "hidden"

    def test_hidden_when_wrong_phase(self) -> None:
        assert _vis(_strat(phase="command"), current_phase="shooting") == "hidden"

    def test_hidden_when_wrong_stage(self) -> None:
        assert _vis(_strat(stage="start"), current_stage="active") == "hidden"

    def test_hidden_when_multi_phase_list_and_wrong_phase(self) -> None:
        strat = _strat(phase=["command", "movement"])
        assert _vis(strat, current_phase="shooting") == "hidden"


# ---------------------------------------------------------------------------
# Greyed conditions
# ---------------------------------------------------------------------------


class TestStratagemsGreyed:
    def test_greyed_when_already_used_this_phase(self) -> None:
        strat = _strat(sid="gs.strat")
        assert _vis(strat, used={"gs.strat"}) == "greyed"

    def test_greyed_when_insufficient_cp(self) -> None:
        strat = _strat(cp_cost=3)
        assert _vis(strat, cp=2) == "greyed"

    def test_greyed_when_cp_exactly_insufficient(self) -> None:
        strat = _strat(cp_cost=2)
        assert _vis(strat, cp=1) == "greyed"


# ---------------------------------------------------------------------------
# Clickable conditions
# ---------------------------------------------------------------------------


class TestStratagemsClickable:
    def test_clickable_when_all_conditions_met(self) -> None:
        assert _vis(_strat()) == "clickable"

    def test_clickable_with_exact_cp(self) -> None:
        strat = _strat(cp_cost=3)
        assert _vis(strat, cp=3) == "clickable"

    def test_clickable_with_phase_any(self) -> None:
        strat = _strat(phase="any")
        assert _vis(strat, current_phase="fight") == "clickable"

    def test_clickable_when_in_multi_phase_list(self) -> None:
        strat = _strat(phase=["shooting", "fight"])
        assert _vis(strat, current_phase="fight") == "clickable"

    def test_clickable_free_stratagem_zero_cp(self) -> None:
        strat = _strat(cp_cost=0)
        assert _vis(strat, cp=0) == "clickable"

    def test_clickable_different_strat_id_not_in_used_set(self) -> None:
        strat = _strat(sid="other.strat")
        assert _vis(strat, used={"different.strat"}) == "clickable"


# ---------------------------------------------------------------------------
# R-CMD-12: Command Re-Roll is phase_reactive → always hidden proactively
# ---------------------------------------------------------------------------

_COMMAND_RE_ROLL_ID = "wh40k_9e.shared.stratagem.command_re_roll"


def _load_command_re_roll() -> Stratagem:
    """Load the Command Re-Roll stratagem from the shared YAML data."""
    stratagems = load_stratagems("necrons")  # shared stratagems are always included
    match = next((s for s in stratagems if s.id == _COMMAND_RE_ROLL_ID), None)
    assert match is not None, f"Stratagem {_COMMAND_RE_ROLL_ID!r} not found in shared data"
    return match


class TestCommandReRollIsPhaseReactive:
    """R-CMD-12: command_re_roll is classified as phase_reactive → hidden in proactive UI.

    The stratagem must never be offered proactively; it is only used reactively
    after a roll has been made at the table.  stratagem_visibility() returns
    'hidden' for any phase_reactive stratagem regardless of CP or conditions.
    """

    def test_command_re_roll_has_phase_reactive_timing(self) -> None:
        strat = _load_command_re_roll()
        assert strat.timing == "phase_reactive"

    def test_command_re_roll_hidden_in_shooting_phase_with_conditions_met(self) -> None:
        strat = _load_command_re_roll()
        result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="shooting",
            current_stage="active",
            used_this_phase=set(),
            conditions_met=True,
        )
        assert result == "hidden"

    def test_command_re_roll_hidden_in_fight_phase_with_conditions_met(self) -> None:
        strat = _load_command_re_roll()
        result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="fight",
            current_stage="active",
            used_this_phase=set(),
            conditions_met=True,
        )
        assert result == "hidden"

    def test_command_re_roll_hidden_even_with_excess_cp(self) -> None:
        # Having 99 CP must not make a phase_reactive stratagem proactively visible
        strat = _load_command_re_roll()
        result = stratagem_visibility(
            strat,
            cp_available=99,
            current_phase="charge",
            current_stage="active",
            used_this_phase=set(),
            conditions_met=True,
        )
        assert result == "hidden"

    def test_phase_reactive_timing_on_synthetic_strat_returns_hidden(self) -> None:
        # Confirm the visibility rule in isolation (no YAML dependency)
        strat = _strat(timing="phase_reactive", phase="any", stage="active")
        assert _vis(strat, cp=10, current_phase="shooting", current_stage="active") == "hidden"


# ---------------------------------------------------------------------------
# R-STR-01: once_per_battle — battle-scoped enforcement
# ---------------------------------------------------------------------------


def _once_per_battle_strat(sid: str = "test.opb_strat") -> Stratagem:
    return Stratagem(
        id=sid,
        name_en="Once Per Battle GO",
        cp_cost=1,
        phase="any",
        stage="active",
        player="active",
        once_per_battle=True,
    )


class TestOncePerBattleEnforcement:
    """R-STR-01: A once_per_battle stratagem must stay greyed after phase and player switches.

    The battle-scoped used_in_battle set is checked independently of used_this_phase.
    A normal (once_per_phase) stratagem must not be affected by the battle-set.
    """

    def test_once_per_battle_greyed_when_in_battle_set(self) -> None:
        strat = _once_per_battle_strat()
        result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="shooting",
            current_stage="active",
            used_this_phase=set(),
            conditions_met=True,
            used_in_battle={"test.opb_strat"},
        )
        assert result == "greyed"

    def test_once_per_battle_greyed_across_phase_change(self) -> None:
        """After a phase reset used_this_phase is empty, but used_in_battle persists.

        The stratagem must remain greyed — simulating a new phase where the
        phase-scoped set was cleared but the battle-scoped set was not.
        """
        strat = _once_per_battle_strat()
        result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="fight",  # different phase than where it was used
            current_stage="active",
            used_this_phase=set(),  # phase was reset
            conditions_met=True,
            used_in_battle={"test.opb_strat"},  # battle set still contains the id
        )
        assert result == "greyed"

    def test_once_per_battle_clickable_when_not_in_battle_set(self) -> None:
        strat = _once_per_battle_strat()
        result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="shooting",
            current_stage="active",
            used_this_phase=set(),
            conditions_met=True,
            used_in_battle=set(),
        )
        assert result == "clickable"

    def test_normal_stratagem_unaffected_by_battle_set(self) -> None:
        """A non-once_per_battle stratagem is not blocked by the battle-scoped set."""
        strat = _strat(sid="test.normal_strat")  # once_per_battle defaults to False
        result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="shooting",
            current_stage="active",
            used_this_phase=set(),
            conditions_met=True,
            used_in_battle={"test.normal_strat"},  # id in battle set, but not once_per_battle
        )
        assert result == "clickable"

    def test_once_per_battle_without_battle_set_falls_back_to_phase_check(self) -> None:
        """When used_in_battle is None (legacy call), the phase check still applies."""
        strat = _once_per_battle_strat(sid="test.opb_strat_legacy")
        result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="shooting",
            current_stage="active",
            used_this_phase={"test.opb_strat_legacy"},
            conditions_met=True,
            used_in_battle=None,  # no battle set provided
        )
        assert result == "greyed"
