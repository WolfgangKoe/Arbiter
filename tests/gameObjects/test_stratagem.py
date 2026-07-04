"""Tests for gameObjects/stratagem.py — stratagem_visibility() pure function."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameObjects.loader import load_stratagems  # noqa: E402
from gameObjects.stratagem import (  # noqa: E402
    Stratagem,
    is_core_stratagem,
    stratagem_undo_visible,
    stratagem_usable_by_player,
    stratagem_visibility,
)

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


# ---------------------------------------------------------------------------
# P19: once_per_battle stratagems are scoped per spending player, not global
# ---------------------------------------------------------------------------


class TestBattleScopedStratagemUsedByOnePlayerDoesNotBlockOther:
    """P19 regression: `used_stratagem_battle_ids` (game_state.py) is a dict
    keyed by spending faction, not a single global set shared by both players.
    gameProtocoll.py slices it per player (`used_battle_ids_by_faction.get(
    spending_faction, set())`) before calling stratagem_visibility() — this
    test exercises that same slicing pattern to prove one player's usage of a
    once_per_battle stratagem does not grey out the identical stratagem ID
    for the other player.
    """

    def test_battle_scoped_stratagem_used_by_one_player_does_not_block_other(
        self,
    ) -> None:
        strat = _once_per_battle_strat(sid="opb.strat_x")
        used_battle_ids_by_faction: dict[str, set[str]] = {"Necrons": {"opb.strat_x"}}

        necrons_result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="shooting",
            current_stage="active",
            used_this_phase=set(),
            conditions_met=True,
            used_in_battle=used_battle_ids_by_faction.get("Necrons", set()),
        )
        orks_result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="shooting",
            current_stage="active",
            used_this_phase=set(),
            conditions_met=True,
            used_in_battle=used_battle_ids_by_faction.get("Orks", set()),
        )

        assert necrons_result == "greyed"
        assert orks_result == "clickable"


# ---------------------------------------------------------------------------
# P21: stratagem_undo_visible() — undo button must not survive a phase change
# ---------------------------------------------------------------------------


class TestUndoHiddenAfterPhaseResetButBattleGreyedPersists:
    """P21 regression: the ↺-undo button must disappear once the phase that used
    the stratagem has passed, even though the once_per_battle greyed-out label
    correctly persists until the battle ends (S113 behavior, kept intact).
    """

    def test_undo_visible_when_used_this_phase_only(self) -> None:
        assert stratagem_undo_visible("s.strat", {"s.strat"}, set()) is True

    def test_undo_hidden_after_phase_reset_but_battle_greyed_persists(self) -> None:
        # Phase changed → used_this_phase was reset to empty by _reset_phase_state(),
        # but the battle-scoped set still holds the id (S113 once_per_battle behavior).
        assert stratagem_undo_visible("s.strat", set(), {"s.strat"}) is False

    def test_undo_visible_when_used_in_both_sets(self) -> None:
        # Just used, still within the same phase window: both sets contain it.
        assert stratagem_undo_visible("s.strat", {"s.strat"}, {"s.strat"}) is True

    def test_undo_hidden_when_not_used_anywhere(self) -> None:
        assert stratagem_undo_visible("s.strat", set(), set()) is False


# ---------------------------------------------------------------------------
# S121 Task 0: Counter-Offensive + Insane Bravery player-field YAML drift fix
# ---------------------------------------------------------------------------

_COUNTER_OFFENSIVE_ID = "wh40k_9e.shared.stratagem.counter_offensive"
_INSANE_BRAVERY_ID = "wh40k_9e.shared.stratagem.insane_bravery"


def _load_shared_stratagem(stratagem_id: str) -> Stratagem:
    """Load a single shared stratagem by id from the YAML data."""
    stratagems = load_stratagems("necrons")  # shared stratagems are always included
    match = next((s for s in stratagems if s.id == stratagem_id), None)
    assert match is not None, f"Stratagem {stratagem_id!r} not found in shared data"
    return match


class TestCounterOffensiveAndInsaneBraveryAreBothPlayer:
    """S121 Task 0 regression: Fight and Morale phases alternate between both
    players (core_rules.txt:1941, core_rules.txt:2094), so Counter-Offensive and
    Insane Bravery must be usable by either player, not just one side.

    Prior to this fix, the YAML drifted to `player: inactive` (Counter-Offensive)
    and `player: active` (Insane Bravery) — a rules bug fixed here.
    """

    def test_counter_offensive_player_is_both(self) -> None:
        strat = _load_shared_stratagem(_COUNTER_OFFENSIVE_ID)
        assert strat.player == "both"

    def test_insane_bravery_player_is_both(self) -> None:
        strat = _load_shared_stratagem(_INSANE_BRAVERY_ID)
        assert strat.player == "both"


# ---------------------------------------------------------------------------
# S121 Task 1: stratagem_usable_by_player() — player-column filter
# ---------------------------------------------------------------------------


class TestStratagemUsableByPlayer:
    """Full truth table for the player-split filter (3 player values × 2 roles).

    Each rendered player column calls this with `is_this_player_active =
    (column player == active faction)`; the column itself is the spending player.
    """

    def test_active_field_usable_by_active_player(self) -> None:
        assert stratagem_usable_by_player("active", True) is True

    def test_active_field_not_usable_by_inactive_player(self) -> None:
        assert stratagem_usable_by_player("active", False) is False

    def test_inactive_field_not_usable_by_active_player(self) -> None:
        assert stratagem_usable_by_player("inactive", True) is False

    def test_inactive_field_usable_by_inactive_player(self) -> None:
        assert stratagem_usable_by_player("inactive", False) is True

    def test_both_field_usable_by_active_player(self) -> None:
        assert stratagem_usable_by_player("both", True) is True

    def test_both_field_usable_by_inactive_player(self) -> None:
        assert stratagem_usable_by_player("both", False) is True


class TestPlayerColumnRegressions:
    """S119 Findings #1 + #2 regressions for the player-split column model.

    Finding #1 (duplicates): each column loads exactly one list —
    load_stratagems(faction) — so the source list itself must be free of
    duplicate ids (previously two loaded lists were concatenated).
    Finding #2 (attribution): a `player: active` stratagem passes the filter
    only in the active player's column, never in the inactive player's.
    """

    def test_no_duplicate_stratagem_ids_within_one_column_source(self) -> None:
        for faction in ("necrons", "orks"):
            ids = [s.id for s in load_stratagems(faction)]
            assert len(ids) == len(set(ids)), f"duplicate stratagem ids for {faction!r}"

    def test_active_stratagem_attributed_to_active_column_only(self) -> None:
        strat = _strat(sid="test.active_only")  # player="active" (helper default)
        active_column = [s for s in [strat] if stratagem_usable_by_player(s.player, True)]
        inactive_column = [s for s in [strat] if stratagem_usable_by_player(s.player, False)]
        assert active_column == [strat]
        assert inactive_column == []


class TestIsCoreStratagem:
    """Section-header classifier: shared/core namespace vs faction namespace."""

    def test_shared_id_is_core(self) -> None:
        assert is_core_stratagem("wh40k_9e.shared.stratagem.command_re_roll") is True

    def test_faction_id_is_not_core(self) -> None:
        assert is_core_stratagem("wh40k_9e.necrons.stratagem.resurrection_protocols") is False

    def test_all_loaded_shared_stratagems_classified_core(self) -> None:
        shared_prefix = "wh40k_9e.shared."
        for s in load_stratagems("necrons"):
            expected = s.id.startswith(shared_prefix)
            assert is_core_stratagem(s.id) is expected, s.id
