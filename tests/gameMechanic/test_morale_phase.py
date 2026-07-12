"""Tests for moralePhase.py — Ziel 4h: threshold calculation and flee_models."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic import moralePhase
from gameMechanic.moralePhase import (
    _attrition_threshold,
    _fail_threshold,
    attrition_condition,
    attrition_modifier_abilities,
    morale_test_required,
)
from gameMechanic.unitMutations import flee_models
from gameObjects.loader import load_unit_abilities

# ---------------------------------------------------------------------------
# _fail_threshold — pure-function tests
# ---------------------------------------------------------------------------


class TestFailThreshold:
    def test_typical_case(self):
        # Ld 7, lost 2 → fails on D6 >= 6
        assert _fail_threshold(7, 2) == 6

    def test_auto_pass_above_6(self):
        # Ld 7, lost 1 → threshold 7 → impossible to fail
        assert _fail_threshold(7, 1) == 7

    def test_always_fails_threshold_1(self):
        # Ld 7, lost 7 → threshold 1 → always fails
        assert _fail_threshold(7, 7) == 1

    def test_always_fails_threshold_below_1(self):
        # Ld 5, lost 8 → threshold -2 → always fails
        assert _fail_threshold(5, 8) == -2

    def test_fails_only_on_6(self):
        # Ld 10, lost 5 → fails on D6 >= 6
        assert _fail_threshold(10, 5) == 6

    def test_high_leadership_rarely_fails(self):
        # Ld 10, lost 1 → threshold 10 → impossible
        assert _fail_threshold(10, 1) == 10

    def test_low_leadership_many_losses(self):
        # Ld 4, lost 4 → threshold 1 → always fails
        assert _fail_threshold(4, 4) == 1


# ---------------------------------------------------------------------------
# flee_models — state mutation tests
# ---------------------------------------------------------------------------


def _make_unit(wounds: int = 1, models_max: int = 10) -> MagicMock:
    u = MagicMock()
    u.wounds = wounds
    u.models_max = models_max
    return u


def _make_state(models: int = 10, wounds_per_model: int = 1) -> dict:
    return {
        "current_wounds": models * wounds_per_model,
        "models": models,
        "destroyed": False,
        "fled_models_this_turn": 0,
        "turn_flags": {"morale_tested": False},
    }


def _necron_session(unit_state: dict) -> dict:
    return {"first_player": "Necrons", "p1_units": {"u1": unit_state}}


class TestFleeModels:
    def test_flee_reduces_models(self):
        unit_state = _make_state(models=10)
        unit = _make_unit(wounds=1, models_max=10)
        with (
            patch("gameMechanic.unitMutations.st") as mock_st,
            patch("gameMechanic.gameState.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 3, unit)
        assert unit_state["models"] == 7
        assert unit_state["current_wounds"] == 7

    def test_flee_sets_fled_counter(self):
        unit_state = _make_state(models=10)
        unit = _make_unit(wounds=1, models_max=10)
        with (
            patch("gameMechanic.unitMutations.st") as mock_st,
            patch("gameMechanic.gameState.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 2, unit)
        assert unit_state["fled_models_this_turn"] == 2

    def test_flee_marks_morale_tested(self):
        unit_state = _make_state(models=10)
        unit = _make_unit(wounds=1, models_max=10)
        with (
            patch("gameMechanic.unitMutations.st") as mock_st,
            patch("gameMechanic.gameState.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 1, unit)
        assert unit_state["turn_flags"]["morale_tested"] is True

    def test_flee_all_models_marks_destroyed(self):
        unit_state = _make_state(models=3)
        unit = _make_unit(wounds=1, models_max=3)
        with (
            patch("gameMechanic.unitMutations.st") as mock_st,
            patch("gameMechanic.gameState.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 3, unit)
        assert unit_state["destroyed"] is True
        assert unit_state["models"] == 0

    def test_flee_accumulates_across_calls(self):
        unit_state = _make_state(models=10)
        unit = _make_unit(wounds=1, models_max=10)
        with (
            patch("gameMechanic.unitMutations.st") as mock_st,
            patch("gameMechanic.gameState.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 2, unit)
            flee_models("u1", "Necrons", 1, unit)
        assert unit_state["fled_models_this_turn"] == 3

    def test_flee_multi_wound_model(self):
        unit_state = _make_state(models=5, wounds_per_model=3)
        unit = _make_unit(wounds=3, models_max=5)
        with (
            patch("gameMechanic.unitMutations.st") as mock_st,
            patch("gameMechanic.gameState.st", mock_st),
        ):
            mock_st.session_state = _necron_session(unit_state)
            flee_models("u1", "Necrons", 2, unit)
        assert unit_state["models"] == 3
        assert unit_state["current_wounds"] == 9


# ---------------------------------------------------------------------------
# R-MORALE-02 — morale_test_required (filter for units that must test)
# ---------------------------------------------------------------------------


def _mock_unit(models_max: int = 5) -> MagicMock:
    u = MagicMock()
    u.models_max = models_max
    return u


def _alive_state(lost: int = 0) -> dict:
    return {"destroyed": False, "lost_models_this_turn": lost}


class TestMoraleTestRequired:
    def test_unit_with_losses_requires_test(self) -> None:
        """Units with at least one model lost this turn must take a Morale test."""
        unit = _mock_unit(models_max=10)
        state = _alive_state(lost=2)
        assert morale_test_required(unit, state) is True

    def test_unit_with_no_losses_skipped(self) -> None:
        """Units that suffered no losses this turn are excluded."""
        unit = _mock_unit(models_max=10)
        state = _alive_state(lost=0)
        assert morale_test_required(unit, state) is False

    def test_single_model_unit_always_skipped(self) -> None:
        """Single-model units never take Morale tests regardless of lost_models_this_turn."""
        unit = _mock_unit(models_max=1)
        state = _alive_state(lost=1)
        assert morale_test_required(unit, state) is False

    def test_destroyed_unit_skipped(self) -> None:
        """Destroyed units must not be presented with a Morale test."""
        unit = _mock_unit(models_max=5)
        state = {"destroyed": True, "lost_models_this_turn": 3}
        assert morale_test_required(unit, state) is False

    def test_multi_model_unit_alive_with_losses_requires_test(self) -> None:
        unit = _mock_unit(models_max=20)
        state = _alive_state(lost=5)
        assert morale_test_required(unit, state) is True

    def test_unit_with_losses_but_destroyed_skipped(self) -> None:
        """Destroyed flag takes priority even when lost_models_this_turn > 0."""
        unit = _mock_unit(models_max=10)
        state = {"destroyed": True, "lost_models_this_turn": 10}
        assert morale_test_required(unit, state) is False


# ---------------------------------------------------------------------------
# _render_faction_morale — duplicate-squad state-key resolution (Plan 034)
# ---------------------------------------------------------------------------


class TestRenderFactionMoraleDuplicateSquad:
    def test_duplicate_squad_gets_morale_test(self, monkeypatch) -> None:
        """The second copy of a duplicated squad (state key 'u1#1') must still
        be offered a Morale test. `units` is keyed by bare unit ID, so the
        lookup must resolve the '#1' suffix before indexing — otherwise the
        duplicate copy is silently skipped (regression for the morale-test
        bug: only 'u1' has losses here, 'u1#1' also needs an offered test)."""
        unit = _mock_unit(models_max=10)

        rendered_uids: list[str] = []
        monkeypatch.setattr(
            moralePhase,
            "_render_unit_morale",
            lambda faction, uid, u, unit_state, state: rendered_uids.append(uid),
        )

        moralePhase._render_faction_morale(
            "Necrons",
            {"u1": unit},
            {"u1": _alive_state(lost=0), "u1#1": _alive_state(lost=2)},
            {"round": 1},
        )

        assert rendered_uids == ["u1#1"]


# ---------------------------------------------------------------------------
# Combat Attrition (Plan 018 / Task 18.3) — _attrition_threshold + ability
# extraction. 9E core rules: one D6 per model remaining after the first model
# fled; each (modified) result of 1 flees; -1 to the roll below Half-strength.
# ---------------------------------------------------------------------------


def _attrition_unit(models_max: int = 10) -> MagicMock:
    u = MagicMock()
    u.models_max = models_max
    return u


def _attrition_state(models: int, initial: int) -> dict:
    return {"models": models, "models_initial": initial}


class TestAttritionThreshold:
    def test_full_strength_no_modifier_flees_on_1(self) -> None:
        state = _attrition_state(models=10, initial=10)
        assert _attrition_threshold(_attrition_unit(), state, []) == 1

    def test_below_half_strength_raises_threshold(self) -> None:
        # 3 of 10 left before the auto-flee → 2 remain → 2*2 < 10 → -1 on rolls
        state = _attrition_state(models=3, initial=10)
        assert _attrition_threshold(_attrition_unit(), state, []) == 2

    def test_half_strength_checked_after_first_model_fled(self) -> None:
        # 5 of 10 before the auto-flee: attrition is rolled with 4 remaining,
        # which IS below half — plain models*2 >= initial would miss this.
        state = _attrition_state(models=5, initial=10)
        assert _attrition_threshold(_attrition_unit(), state, []) == 2

    def test_exactly_half_after_flee_is_not_below(self) -> None:
        # 6 of 10 before the auto-flee → 5 remain → 5*2 == 10 → not below half
        state = _attrition_state(models=6, initial=10)
        assert _attrition_threshold(_attrition_unit(), state, []) == 1

    def test_minus_one_modifier_raises_threshold(self) -> None:
        state = _attrition_state(models=10, initial=10)
        assert _attrition_threshold(_attrition_unit(), state, [-1]) == 2

    def test_below_half_and_modifier_stack(self) -> None:
        state = _attrition_state(models=3, initial=10)
        assert _attrition_threshold(_attrition_unit(), state, [-1]) == 3

    def test_positive_modifier_can_prevent_fleeing(self) -> None:
        # e.g. a +1 aura lifts every roll above 1 → threshold clamps to 0
        state = _attrition_state(models=10, initial=10)
        assert _attrition_threshold(_attrition_unit(), state, [1]) == 0

    def test_threshold_clamped_at_6(self) -> None:
        state = _attrition_state(models=3, initial=10)
        assert _attrition_threshold(_attrition_unit(), state, [-1, -2, -3]) == 6

    def test_multiple_modifiers_sum(self) -> None:
        state = _attrition_state(models=10, initial=10)
        assert _attrition_threshold(_attrition_unit(), state, [-1, -1]) == 3

    def test_missing_models_initial_falls_back_to_models_max(self) -> None:
        unit = _attrition_unit(models_max=10)
        state = {"models": 3}
        assert _attrition_threshold(unit, state, []) == 2


class TestAttritionAbilityExtraction:
    @staticmethod
    def _ability(effect_type: str, modifier: int | None = None, effects: list | None = None):
        a = MagicMock()
        a.effect.type = effect_type
        a.effect.modifier = modifier
        a.effect.effects = effects
        return a

    def test_filter_keeps_only_attrition_modifiers(self) -> None:
        attrition = self._ability("attrition_modifier", modifier=-1)
        other = self._ability("special_morale")
        assert attrition_modifier_abilities([other, attrition, other]) == [attrition]

    def test_filter_empty_when_no_attrition_ability(self) -> None:
        assert attrition_modifier_abilities([self._ability("heal")]) == []

    def test_condition_prompt_and_applies_when_from_sub_effect(self) -> None:
        ability = self._ability(
            "attrition_modifier",
            modifier=-1,
            effects=[{"condition_prompt": "Herder nearby?", "applies_when": False}],
        )
        assert attrition_condition(ability) == ("Herder nearby?", False)

    def test_condition_defaults_to_unconditional(self) -> None:
        ability = self._ability("attrition_modifier", modifier=-1, effects=None)
        assert attrition_condition(ability) == (None, True)

    def test_applies_when_defaults_to_true_when_prompt_present(self) -> None:
        ability = self._ability(
            "attrition_modifier",
            modifier=-1,
            effects=[{"condition_prompt": "Condition met?"}],
        )
        assert attrition_condition(ability) == ("Condition met?", True)


class TestCowardlyYamlEntry:
    """Regression: the Gretchin Cowardly entry parses through the real loader."""

    def test_cowardly_ability_loaded_with_attrition_modifier(self) -> None:
        abilities = load_unit_abilities("orks")
        cowardly = next(
            (a for a in abilities if a.id == "wh40k_9e.orks.unit.gretchin.cowardly"), None
        )
        assert cowardly is not None
        assert cowardly.effect.type == "attrition_modifier"
        assert cowardly.effect.modifier == -1
        assert cowardly.unit_id == "wh40k_9e.orks.unit.gretchin"

    def test_cowardly_condition_prompt_rides_in_yaml_not_src(self) -> None:
        abilities = load_unit_abilities("orks")
        cowardly = next(a for a in abilities if a.id == "wh40k_9e.orks.unit.gretchin.cowardly")
        prompt, applies_when = attrition_condition(cowardly)
        assert prompt == 'Friendly RUNTHERD within 6"?'
        assert applies_when is False

    def test_cowardly_is_picked_up_by_attrition_filter(self) -> None:
        abilities = load_unit_abilities("orks")
        filtered = attrition_modifier_abilities(abilities)
        assert [a.id for a in filtered] == ["wh40k_9e.orks.unit.gretchin.cowardly"]
