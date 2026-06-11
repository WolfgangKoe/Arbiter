"""Tests for gameObjects/stratagem.py — stratagem_visibility() pure function."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

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
