"""Tests for gameMechanic/stratagemEngine.py.

The three functions consolidated here (S142 Aufgabe 1, Option B) previously
lived at uiLayout._common._apply_stratagem_effect, uiLayout.gameProtocoll.
_effect_gate_met and gameMechanic.abilityEngine.stratagem_strength_bonus.
These tests are the corresponding blocks moved verbatim from
tests/uiLayout/test_game_protocoll.py and tests/gameMechanic/
test_ability_engine.py — _apply_stratagem_effect itself stays covered via
tests/uiLayout/test_common.py's spend_stratagem() dispatch tests (integration
path, unchanged by the move).
"""

import sys
from dataclasses import replace
from pathlib import Path
from unittest.mock import MagicMock

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameMechanic.abilityEngine import _sum_effect_value  # noqa: E402
from gameMechanic.stratagemEngine import (  # noqa: E402
    _effect_gate_met,
    is_unit_scoped_effect,
    stratagem_strength_bonus,
    stratagem_strength_labels,
)
from gameObjects.ability import Effect  # noqa: E402
from gameObjects.stratagem import Stratagem  # noqa: E402


def _make_stratagem(
    id_: str = "s1",
    name_en: str = "Test Strat",
    cp_cost: int = 1,
    once_per_battle: bool = False,
) -> Stratagem:
    return Stratagem(
        id=id_,
        name_en=name_en,
        cp_cost=cp_cost,
        phase="any",
        stage="active",
        player="both",
        once_per_battle=once_per_battle,
    )


# ---------------------------------------------------------------------------
# _effect_gate_met() — S133-D Befund 4: per-unit-state gate for GOs whose
# effect requires "not yet moved this phase" + "in Engagement Range"
# (rules_appendix.txt 2618-2625, Desperate Breakout). Pure, no Streamlit.
# ---------------------------------------------------------------------------


def _make_fall_back_stratagem() -> Stratagem:
    return _make_stratagem(id_="desperate_breakout", name_en="Desperate Breakout", cp_cost=2)


def _with_fall_back_effect(strat: Stratagem) -> Stratagem:
    return replace(strat, effect=Effect(type="move", handler="fall_back_through_models"))


def test_effect_gate_met_true_when_stratagem_has_no_effect() -> None:
    strat = _make_stratagem()
    assert _effect_gate_met(strat, None) == (True, None)


def test_effect_gate_met_true_for_unrelated_effect_shape() -> None:
    """An effect type outside `_UNIT_SCOPED_EFFECT_TYPES` (e.g. a plain reroll,
    not dispatched by `_apply_stratagem_effect` at all) has no per-unit-state
    requirement beyond `conditions` — always gate-met, unit selected or not.
    """
    strat = replace(_make_stratagem(), effect=Effect(type="reroll"))
    assert _effect_gate_met(strat, None) == (True, None)
    assert _effect_gate_met(strat, {"movement_chosen": True, "in_melee": False}) == (
        True,
        None,
    )


# ---------------------------------------------------------------------------
# _effect_gate_met() — S142 Aufgabe 2, Befund 5 (B12b): auto_pass_morale
# (Insane Bravery, core_rules.txt:3260-3267, `conditions: []` in YAML) is a
# unit-scoped effect with no dedicated per-unit-state form of its own — it
# must still require a selected unit, or the card goes "ready" purely on CP
# and clicking Use spends the Stratagem with no game effect (unit_key=None
# skips `_apply_stratagem_effect` in `spend_stratagem`).
# ---------------------------------------------------------------------------


def _with_auto_pass_morale_effect(strat: Stratagem) -> Stratagem:
    return replace(strat, effect=Effect(type="auto_pass_morale"))


def test_effect_gate_met_false_for_auto_pass_morale_when_no_unit_selected_b12b() -> None:
    strat = _with_auto_pass_morale_effect(_make_stratagem(id_="insane_bravery"))
    assert _effect_gate_met(strat, None) == (False, "select an eligible unit")


def test_effect_gate_met_true_for_auto_pass_morale_when_unit_selected_b12b() -> None:
    strat = _with_auto_pass_morale_effect(_make_stratagem(id_="insane_bravery"))
    assert _effect_gate_met(strat, {"movement_chosen": True, "in_melee": False}) == (
        True,
        None,
    )


def test_effect_gate_met_false_when_no_unit_selected() -> None:
    strat = _with_fall_back_effect(_make_fall_back_stratagem())
    assert _effect_gate_met(strat, None) == (False, "select an eligible unit")


def test_effect_gate_met_false_when_unit_already_moved_this_phase() -> None:
    strat = _with_fall_back_effect(_make_fall_back_stratagem())
    unit_state = {"movement_chosen": True, "in_melee": True}
    assert _effect_gate_met(strat, unit_state) == (False, "unit already moved this phase")


def test_effect_gate_met_false_when_unit_not_in_engagement_range() -> None:
    strat = _with_fall_back_effect(_make_fall_back_stratagem())
    unit_state = {"movement_chosen": False, "in_melee": False}
    assert _effect_gate_met(strat, unit_state) == (False, "unit not in Engagement Range")


def test_effect_gate_met_true_when_not_moved_and_in_engagement_range() -> None:
    strat = _with_fall_back_effect(_make_fall_back_stratagem())
    unit_state = {"movement_chosen": False, "in_melee": True}
    assert _effect_gate_met(strat, unit_state) == (True, None)


# ---------------------------------------------------------------------------
# is_unit_scoped_effect() — S142-Review Befund 1+3: single shared predicate for
# "does this GO's effect require a specific selected unit". Must agree exactly
# with _effect_gate_met's dispatch table (auto_pass_morale, invuln_save,
# move+fall_back_through_models) and exclude non-unit-scoped effect-carrying
# stratagems (e.g. grant_relic) that used to be over-generalized under the
# broader `strat.effect is not None` check at the gameProtocoll call sites.
# ---------------------------------------------------------------------------


def test_is_unit_scoped_effect_false_when_no_effect() -> None:
    strat = _make_stratagem()
    assert is_unit_scoped_effect(strat) is False


def test_is_unit_scoped_effect_true_for_auto_pass_morale() -> None:
    strat = replace(_make_stratagem(), effect=Effect(type="auto_pass_morale"))
    assert is_unit_scoped_effect(strat) is True


def test_is_unit_scoped_effect_true_for_invuln_save() -> None:
    strat = replace(_make_stratagem(), effect=Effect(type="invuln_save", modifier=1))
    assert is_unit_scoped_effect(strat) is True


def test_is_unit_scoped_effect_true_for_fall_back_through_models() -> None:
    strat = _with_fall_back_effect(_make_fall_back_stratagem())
    assert is_unit_scoped_effect(strat) is True


def test_is_unit_scoped_effect_false_for_non_unit_scoped_effect_type() -> None:
    """Gegenfall: an effect-carrying but non-unit-scoped stratagem (e.g.
    grant_relic — applies army-wide / resolved at the table) is NOT
    unit-scoped. This is the exact over-generalization the S142-Review found:
    `strat.effect is not None` alone would wrongly return True here."""
    strat = replace(_make_stratagem(), effect=Effect(type="grant_relic"))
    assert is_unit_scoped_effect(strat) is False


# ---------------------------------------------------------------------------
# S122 F1: stratagem_strength_bonus (Disruption Fields — real Strength modifier,
# not a Wound-roll bonus)
# ---------------------------------------------------------------------------


_ATK_UID = "wh40k_9e.necrons.unit.warriors"


def _strength_modifier_entry(
    value: int = 1,
    target: str = "attacker",
    roll_type: str = "strength",
    unit_key: str | None = _ATK_UID,
) -> dict:
    return {
        "unit_key": unit_key,
        "source": "Disruption Fields",
        "effect": {"roll_type": roll_type, "value": value, "target": target, "phase": "fight"},
        "expires_at_phase": "fight",
        "expires_at_round": None,
    }


def test_stratagem_strength_bonus_empty_list_is_zero() -> None:
    assert stratagem_strength_bonus([], _ATK_UID) == 0


def test_stratagem_strength_bonus_matching_entry() -> None:
    mods = [_strength_modifier_entry(value=1, target="attacker")]
    assert stratagem_strength_bonus(mods, _ATK_UID) == 1


def test_stratagem_strength_bonus_target_any_counts() -> None:
    mods = [_strength_modifier_entry(value=2, target="any")]
    assert stratagem_strength_bonus(mods, _ATK_UID) == 2


def test_stratagem_strength_bonus_ignores_wrong_roll_type() -> None:
    mods = [_strength_modifier_entry(roll_type="wound")]
    assert stratagem_strength_bonus(mods, _ATK_UID) == 0


def test_stratagem_strength_bonus_ignores_wrong_target() -> None:
    mods = [_strength_modifier_entry(target="defender")]
    assert stratagem_strength_bonus(mods, _ATK_UID) == 0


def test_stratagem_strength_bonus_sums_multiple_entries() -> None:
    mods = [
        _strength_modifier_entry(value=1),
        _strength_modifier_entry(value=1),
    ]
    assert stratagem_strength_bonus(mods, _ATK_UID) == 2


def test_stratagem_strength_bonus_scoped_to_activating_unit_only() -> None:
    """Regression (S122 bug): a Strength stratagem activated for one unit (e.g.
    Disruption Fields declared for the Necron Warriors squad) must not buff a
    different attacker's Strength roll in the same phase.
    """
    mods = [_strength_modifier_entry(value=1, unit_key="wh40k_9e.necrons.unit.warriors#1")]
    assert stratagem_strength_bonus(mods, _ATK_UID) == 0
    assert stratagem_strength_bonus(mods, "wh40k_9e.necrons.unit.warriors#1") == 1


# ---------------------------------------------------------------------------
# S146 Fix 1: stratagem_strength_labels — data-driven source names for the
# WOUND-block badge (same scoping as stratagem_strength_bonus, returns the
# `source` field spend_stratagem records, e.g. "Disruption Fields")
# ---------------------------------------------------------------------------


def test_stratagem_strength_labels_empty_list() -> None:
    assert stratagem_strength_labels([], _ATK_UID) == []


def test_stratagem_strength_labels_returns_source_of_matching_entry() -> None:
    mods = [_strength_modifier_entry(value=1, target="attacker")]
    assert stratagem_strength_labels(mods, _ATK_UID) == ["Disruption Fields"]


def test_stratagem_strength_labels_ignores_wrong_roll_type_target_and_unit() -> None:
    mods = [
        _strength_modifier_entry(roll_type="wound"),
        _strength_modifier_entry(target="defender"),
        _strength_modifier_entry(unit_key="someone#else"),
    ]
    assert stratagem_strength_labels(mods, _ATK_UID) == []


def test_stratagem_strength_labels_deduplicates_same_source() -> None:
    mods = [_strength_modifier_entry(value=1), _strength_modifier_entry(value=1)]
    assert stratagem_strength_labels(mods, _ATK_UID) == ["Disruption Fields"]


def test_stratagem_strength_bonus_legacy_none_unit_key_not_applied_globally() -> None:
    """Pre-fix entries with unit_key=None must no longer buff every attacker."""
    mods = [_strength_modifier_entry(value=1, unit_key=None)]
    assert stratagem_strength_bonus(mods, _ATK_UID) == 0


def test_sum_effect_value_type_key_override_matches_roll_type() -> None:
    """stratagem_strength_bonus (S144 Option B) is the one call site that reads
    a 'roll_type' key instead of the shared helper's default 'type' — pin the
    type_key override directly against _sum_effect_value."""
    effects = [{"roll_type": "strength", "value": 3}, {"roll_type": "wound", "value": 99}]
    assert _sum_effect_value(effects, "strength", type_key="roll_type") == 3
