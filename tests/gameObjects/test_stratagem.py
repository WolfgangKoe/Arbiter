"""Tests for gameObjects/stratagem.py — stratagem_visibility() pure function."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameObjects.loader import load_stratagems  # noqa: E402
from gameObjects.stratagem import (  # noqa: E402
    Stratagem,
    is_core_stratagem,
    reactive_stratagems_for,
    stratagem_conditions_met,
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
    event: str | None = None,
    player: str = "active",
) -> Stratagem:
    return Stratagem(
        id=sid,
        name_en="Test GO",
        cp_cost=cp_cost,
        phase=phase,
        stage=stage,
        player=player,
        timing=timing,
        event=event,
    )


def _vis(
    stratagem: Stratagem,
    cp: int = 5,
    current_phase: str = "shooting",
    used: set[str] | None = None,
    conditions_met: bool = True,
    used_in_battle: set[str] | None = None,
    reactive_trigger_active: bool = False,
) -> str:
    return stratagem_visibility(
        stratagem,
        cp_available=cp,
        current_phase=current_phase,
        used_this_phase=used or set(),
        conditions_met=conditions_met,
        used_in_battle=used_in_battle,
        reactive_trigger_active=reactive_trigger_active,
    )


# ---------------------------------------------------------------------------
# Hidden conditions
# ---------------------------------------------------------------------------


class TestStratagemsHidden:
    def test_hidden_when_conditions_not_met(self) -> None:
        assert _vis(_strat(), conditions_met=False) == "hidden"

    def test_hidden_when_phase_reactive_by_default(self) -> None:
        """Plan 015: phase_reactive stays hidden unless a reactive window is open.

        `reactive_trigger_active` defaults to False — every existing caller (the
        central Stratagems-tab list) keeps getting "hidden" for phase_reactive GOs
        exactly as before this session's contextual reactive-box infrastructure
        was added.
        """
        assert _vis(_strat(timing="phase_reactive")) == "hidden"

    def test_hidden_when_phase_reactive_and_reactive_trigger_active_false(self) -> None:
        assert _vis(_strat(timing="phase_reactive"), reactive_trigger_active=False) == "hidden"

    def test_hidden_when_wrong_phase(self) -> None:
        assert _vis(_strat(phase="command"), current_phase="shooting") == "hidden"

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
# Plan 015: reactive_trigger_active opens the phase_reactive gate contextually
# ---------------------------------------------------------------------------


class TestReactiveTriggerActive:
    """A phase_reactive stratagem becomes evaluable (not hidden) only while its
    reactive window is open — `reactive_trigger_active=True` — and then still
    goes through the normal phase/CP/used checks like any other stratagem.
    """

    def test_reactive_and_trigger_active_and_phase_matches_is_clickable(self) -> None:
        strat = _strat(timing="phase_reactive", phase="charge")
        assert _vis(strat, current_phase="charge", reactive_trigger_active=True) == "clickable"

    def test_reactive_and_trigger_active_but_wrong_phase_is_hidden(self) -> None:
        strat = _strat(timing="phase_reactive", phase="charge")
        assert _vis(strat, current_phase="shooting", reactive_trigger_active=True) == "hidden"

    def test_reactive_and_trigger_active_but_conditions_not_met_is_hidden(self) -> None:
        strat = _strat(timing="phase_reactive", phase="charge")
        assert (
            _vis(
                strat,
                current_phase="charge",
                reactive_trigger_active=True,
                conditions_met=False,
            )
            == "hidden"
        )

    def test_reactive_and_trigger_active_but_insufficient_cp_is_greyed(self) -> None:
        strat = _strat(timing="phase_reactive", phase="charge", cp_cost=2)
        assert _vis(strat, cp=1, current_phase="charge", reactive_trigger_active=True) == "greyed"

    def test_reactive_and_trigger_active_but_already_used_is_greyed(self) -> None:
        strat = _strat(timing="phase_reactive", phase="charge", sid="reactive.used")
        assert (
            _vis(
                strat,
                current_phase="charge",
                used={"reactive.used"},
                reactive_trigger_active=True,
            )
            == "greyed"
        )

    def test_reactive_and_trigger_active_with_phase_any_is_clickable(self) -> None:
        strat = _strat(timing="phase_reactive", phase="any")
        assert _vis(strat, current_phase="morale", reactive_trigger_active=True) == "clickable"


# ---------------------------------------------------------------------------
# Plan 015: reactive_stratagems_for() — pure (phase, event) data-shape filter
# ---------------------------------------------------------------------------


class TestReactiveStratagemsFor:
    def test_matches_stratagem_with_matching_phase_and_event(self) -> None:
        strat = _strat(timing="phase_reactive", phase="charge", event="on_declaration")
        assert reactive_stratagems_for([strat], "charge", "on_declaration") == [strat]

    def test_excludes_non_reactive_stratagem(self) -> None:
        strat = _strat(timing=None, phase="charge", event="on_declaration")
        assert reactive_stratagems_for([strat], "charge", "on_declaration") == []

    def test_excludes_wrong_event(self) -> None:
        strat = _strat(timing="phase_reactive", phase="charge", event="on_destroy")
        assert reactive_stratagems_for([strat], "charge", "on_declaration") == []

    def test_excludes_wrong_phase_single(self) -> None:
        strat = _strat(timing="phase_reactive", phase="fight", event="on_declaration")
        assert reactive_stratagems_for([strat], "charge", "on_declaration") == []

    def test_excludes_wrong_phase_list(self) -> None:
        strat = _strat(timing="phase_reactive", phase=["movement", "shooting"], event="after_roll")
        assert reactive_stratagems_for([strat], "charge", "after_roll") == []

    def test_includes_phase_any_regardless_of_current_phase(self) -> None:
        strat = _strat(timing="phase_reactive", phase="any", event="on_destroy")
        assert reactive_stratagems_for([strat], "morale", "on_destroy") == [strat]

    def test_includes_matching_phase_within_list(self) -> None:
        strat = _strat(
            timing="phase_reactive", phase=["movement", "psychic", "shooting"], event="after_roll"
        )
        assert reactive_stratagems_for([strat], "shooting", "after_roll") == [strat]

    def test_real_shared_reactive_stratagems_match_their_documented_trigger(self) -> None:
        """The 5 shared reactive stratagems each surface at their own (phase, event)."""
        stratagems = load_stratagems("necrons")
        cases = [
            ("wh40k_9e.shared.stratagem.fire_overwatch", "charge", "on_declaration"),
            ("wh40k_9e.shared.stratagem.counter_offensive", "fight", "on_declaration"),
            ("wh40k_9e.shared.stratagem.cut_them_down", "movement", "on_declaration"),
            ("wh40k_9e.shared.stratagem.emergency_disembarkation", "shooting", "on_destroy"),
            ("wh40k_9e.shared.stratagem.command_re_roll", "fight", "after_roll"),
        ]
        for sid, phase, event in cases:
            matched = reactive_stratagems_for(stratagems, phase, event)
            assert any(s.id == sid for s in matched), f"{sid} did not match ({phase}, {event})"


# ---------------------------------------------------------------------------
# Plan 040 regression: `stage` is NOT a visibility criterion
# ---------------------------------------------------------------------------


class TestStageIsNotAVisibilityCriterion:
    """Plan 040 regression: after removing the dead phase-stage machinery,
    the runtime stage is always "active" — stratagems annotated with
    stage="start"/"end" must NOT be hidden by that annotation. 9E only
    codifies the phase binding (core_rules.txt:673-676); within-phase timing
    lives in the rule_text shown in the UI expander.
    """

    def test_start_and_end_stage_stratagems_visible_in_matching_phase(self) -> None:
        # Synthetic: one start-stage and one end-stage stratagem, conditions
        # met, matching phase, enough CP → both clickable, never hidden.
        assert _vis(_strat(stage="start")) == "clickable"
        assert _vis(_strat(stage="end")) == "clickable"

    def test_real_start_and_end_stage_stratagems_clickable_in_their_phase(self) -> None:
        # Real loaded examples that the old stage filter permanently hid
        # (resurrection_protocols is timing=phase_reactive → reactively hidden
        # by design, so the non-reactive movement-phase pair is used instead).
        stratagems = {s.id: s for s in load_stratagems("necrons")}
        corridor = stratagems["wh40k_9e.necrons.stratagem.dimensional_corridor"]
        destabilisation = stratagems["wh40k_9e.necrons.stratagem.dimensional_destabilisation"]
        assert corridor.stage == "start"
        assert destabilisation.stage == "end"
        for strat in (corridor, destabilisation):
            result = stratagem_visibility(
                strat,
                cp_available=10,
                current_phase="movement",
                used_this_phase=set(),
                conditions_met=True,
            )
            assert result == "clickable", strat.id


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
            used_this_phase=set(),
            conditions_met=True,
        )
        assert result == "hidden"

    def test_phase_reactive_timing_on_synthetic_strat_returns_hidden(self) -> None:
        # Confirm the visibility rule in isolation (no YAML dependency)
        strat = _strat(timing="phase_reactive", phase="any", stage="active")
        assert _vis(strat, cp=10, current_phase="shooting") == "hidden"


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
            used_this_phase={"test.opb_strat_legacy"},
            conditions_met=True,
            used_in_battle=None,  # no battle set provided
        )
        assert result == "greyed"


# ---------------------------------------------------------------------------
# P19: once_per_battle stratagems are scoped per spending player, not global
# ---------------------------------------------------------------------------


class TestBattleScopedStratagemUsedByOnePlayerDoesNotBlockOther:
    """P19 regression: `used_stratagem_battle_ids` (gameState.py) is a dict
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
            used_this_phase=set(),
            conditions_met=True,
            used_in_battle=used_battle_ids_by_faction.get("Necrons", set()),
        )
        orks_result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="shooting",
            used_this_phase=set(),
            conditions_met=True,
            used_in_battle=used_battle_ids_by_faction.get("Orks", set()),
        )

        assert necrons_result == "greyed"
        assert orks_result == "clickable"


# ---------------------------------------------------------------------------
# S121 Task 2: once_per_phase usage is scoped per spending player, not global
# ---------------------------------------------------------------------------


class TestPhaseScopedStratagemUsedByOnePlayerDoesNotBlockOther:
    """S121 Task 2 regression (analog to P19, phase scale): `used_stratagem_ids`
    (gameState.py) is a dict keyed by player slot, not a single global set.
    gameProtocoll.py slices it per column (`used_ids_by_player.get(player,
    set())`) before calling stratagem_visibility() — one player's use of a
    stratagem this phase must not grey out the identical stratagem ID in the
    other player's column.
    """

    def test_phase_scoped_stratagem_used_by_one_player_does_not_block_other(
        self,
    ) -> None:
        strat = _strat(sid="opp.strat_y", phase="any")
        used_ids_by_player: dict[str, set[str]] = {"Necrons": {"opp.strat_y"}}

        necrons_result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="shooting",
            used_this_phase=used_ids_by_player.get("Necrons", set()),
            conditions_met=True,
        )
        orks_result = stratagem_visibility(
            strat,
            cp_available=10,
            current_phase="shooting",
            used_this_phase=used_ids_by_player.get("Orks", set()),
            conditions_met=True,
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


class TestBoardingActionsOnlyStratagemsExcluded:
    """S134: four Necron stratagems are Boarding Actions supplement-only per
    wahapedia 9ed and were mistakenly loaded as regular stratagems. They must
    not appear in the regular load_stratagems("necrons") result. The 1 CP
    INFANTRY NOBLE/CRYPTEK Resurrection Protocols variant is a real core
    stratagem and must remain.
    """

    _EXCLUDED_IDS = [
        "wh40k_9e.necrons.stratagem.rapid_reanimation",
        "wh40k_9e.necrons.stratagem.shield_piercer_projectors",
        "wh40k_9e.necrons.stratagem.flensing_capacitors",
        "wh40k_9e.necrons.stratagem.resurrection_protocols_character",
    ]

    def test_boarding_actions_only_stratagems_not_loaded(self) -> None:
        ids = {s.id for s in load_stratagems("necrons")}
        for excluded_id in self._EXCLUDED_IDS:
            assert excluded_id not in ids, f"{excluded_id} is Boarding Actions only"

    def test_infantry_resurrection_protocols_variant_still_loaded(self) -> None:
        ids = {s.id for s in load_stratagems("necrons")}
        assert "wh40k_9e.necrons.stratagem.resurrection_protocols" in ids


_DISRUPTION_FIELDS_ID = "wh40k_9e.necrons.stratagem.disruption_fields"


class TestDisruptionFieldsIsStrengthModifier:
    """S122 F1 regression: Disruption Fields buffs Strength, not the Wound roll.

    Card text (wahapedia_necrons/faction_overview.txt): "Until the end of the
    phase, add 1 to the Strength characteristic of models in that unit." — a
    real characteristic modifier (can shift the wound-table threshold), not a
    flat +1 on the Wound roll. Guards against regressing modifier.roll_type
    back to "wound".
    """

    def _load(self) -> Stratagem:
        stratagems = load_stratagems("necrons")
        match = next((s for s in stratagems if s.id == _DISRUPTION_FIELDS_ID), None)
        assert match is not None, f"Stratagem {_DISRUPTION_FIELDS_ID!r} not found"
        return match

    def test_modifier_roll_type_is_strength(self) -> None:
        strat = self._load()
        assert strat.modifier is not None
        assert strat.modifier.roll_type == "strength"

    def test_no_dead_buff_stat_effect_field(self) -> None:
        strat = self._load()
        assert strat.effect is None


# ---------------------------------------------------------------------------
# S135 Paket 4a — stratagem_conditions_met() keyword gate
# ---------------------------------------------------------------------------


class _KeywordUnit:
    def __init__(self, *keywords: str) -> None:
        self._keywords = {kw.upper() for kw in keywords}

    def has_keyword(self, keyword: str) -> bool:
        return keyword.upper() in self._keywords


class TestStratagemConditionsMet:
    def test_no_conditions_true_without_unit(self) -> None:
        assert stratagem_conditions_met([], None) is True

    def test_conditions_without_unit_is_false(self) -> None:
        """No army-wide fallback — a keyword-gated GO stays hidden without an
        explicit unit, never shown for every unit by default."""
        assert stratagem_conditions_met(["FLAYED ONES"], None) is False

    def test_unit_with_all_required_keywords_is_met(self) -> None:
        unit = _KeywordUnit("NECRONS", "INFANTRY", "FLAYED ONES")
        assert stratagem_conditions_met(["FLAYED ONES"], unit) is True

    def test_unit_missing_a_required_keyword_is_not_met(self) -> None:
        unit = _KeywordUnit("NECRONS", "INFANTRY")
        assert stratagem_conditions_met(["FLAYED ONES"], unit) is False

    def test_multiple_conditions_require_all_keywords(self) -> None:
        unit = _KeywordUnit("NECRONS", "DESTROYER CULT")
        assert stratagem_conditions_met(["NECRONS", "DESTROYER CULT"], unit) is True
        assert stratagem_conditions_met(["NECRONS", "SKORPEKH LORD"], unit) is False


# ---------------------------------------------------------------------------
# S135 Paket 4a — Shadows of Drazak data fix: was missing its `modifier:` block,
# so activating it spent CP without ever registering the hit-roll debuff.
# ---------------------------------------------------------------------------

_SHADOWS_OF_DRAZAK_ID = "wh40k_9e.necrons.stratagem.shadows_of_drazak"


class TestShadowsOfDrazakHasModifierBlock:
    def _load(self) -> Stratagem:
        stratagems = load_stratagems("necrons")
        match = next((s for s in stratagems if s.id == _SHADOWS_OF_DRAZAK_ID), None)
        assert match is not None, f"Stratagem {_SHADOWS_OF_DRAZAK_ID!r} not found"
        return match

    def test_modifier_is_not_none(self) -> None:
        """Without this, spend_stratagem's `if strat.modifier is not None` guard
        (uiLayout/_common.py) never registers anything — Use would spend CP for
        no in-app effect."""
        strat = self._load()
        assert strat.modifier is not None

    def test_modifier_matches_effect_stat_hit(self) -> None:
        strat = self._load()
        assert strat.modifier is not None
        assert strat.modifier.roll_type == "hit"
        assert strat.modifier.value == -1
        assert strat.modifier.target == "defender"
