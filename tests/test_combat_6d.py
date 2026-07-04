"""Tests for Ziel-6d combat helpers: resolve_attack_modifiers, resolve_save, resolve_fnp,
apply_damage_attacks."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from gameMechanic.combat import (  # noqa: E402
    apply_damage_attacks,
    resolve_attack_modifiers,
    resolve_fnp,
    resolve_save,
)

# ---------------------------------------------------------------------------
# resolve_attack_modifiers
# ---------------------------------------------------------------------------


def test_hit_no_mods_returns_base():
    result = resolve_attack_modifiers(3, 4, 4, "Rapid Fire", False, [], False)
    assert result["hit"]["base"] == 3
    assert result["hit"]["modified"] == 3
    assert result["hit"]["stack"] == []


def test_wound_no_mods_equal_s_t():
    result = resolve_attack_modifiers(3, 4, 4, "Rapid Fire", False, [], False)
    assert result["wound"]["base"] == 4
    assert result["wound"]["modified"] == 4


def test_wound_s_gt_t():
    result = resolve_attack_modifiers(3, 5, 4, "Rapid Fire", False, [], False)
    assert result["wound"]["base"] == 3


def test_wound_s_double_t():
    result = resolve_attack_modifiers(3, 8, 4, "Rapid Fire", False, [], False)
    assert result["wound"]["base"] == 2


def test_wound_s_half_t():
    result = resolve_attack_modifiers(3, 2, 4, "Rapid Fire", False, [], False)
    assert result["wound"]["base"] == 6


def test_hit_protocol_plus1():
    mods = [{"label": "Protocol", "value": 1, "roll_type": "hit", "source": "protocol"}]
    result = resolve_attack_modifiers(3, 4, 4, "Rapid Fire", False, mods, False)
    assert result["hit"]["modified"] == 2
    assert len(result["hit"]["stack"]) == 1
    assert result["hit"]["stack"][0]["label"] == "Protocol"


def test_hit_modifier_minus1():
    mods = [{"label": "Debuff", "value": -1, "roll_type": "hit", "source": "stratagem"}]
    result = resolve_attack_modifiers(3, 4, 4, "Rapid Fire", False, mods, False)
    assert result["hit"]["modified"] == 4


def test_hit_capped_at_plus1():
    mods = [
        {"label": "Proto", "value": 1, "roll_type": "hit", "source": "protocol"},
        {"label": "Strat", "value": 1, "roll_type": "hit", "source": "stratagem"},
    ]
    result = resolve_attack_modifiers(3, 4, 4, "Rapid Fire", False, mods, False)
    assert result["hit"]["modified"] == 2  # net capped at +1


def test_hit_capped_at_minus1():
    mods = [
        {"label": "Debuff1", "value": -1, "roll_type": "hit", "source": "stratagem"},
        {"label": "Debuff2", "value": -1, "roll_type": "hit", "source": "stratagem"},
    ]
    result = resolve_attack_modifiers(3, 4, 4, "Rapid Fire", False, mods, False)
    assert result["hit"]["modified"] == 4  # net capped at -1


def test_hit_minimum_2():
    mods = [{"label": "Proto", "value": 1, "roll_type": "hit", "source": "protocol"}]
    result = resolve_attack_modifiers(2, 4, 4, "Rapid Fire", False, mods, False)
    assert result["hit"]["modified"] == 2


def test_heavy_penalty_when_advanced():
    result = resolve_attack_modifiers(3, 4, 4, "Heavy", True, [], False)
    assert result["hit"]["modified"] == 4
    assert result["hit"]["stack"][0]["label"] == "Heavy (advanced)"
    assert result["hit"]["stack"][0]["value"] == -1


def test_heavy_no_penalty_when_not_advanced():
    result = resolve_attack_modifiers(3, 4, 4, "Heavy", False, [], False)
    assert result["hit"]["modified"] == 3
    assert result["hit"]["stack"] == []


def test_heavy_penalty_ignored_in_melee():
    result = resolve_attack_modifiers(3, 4, 4, "Heavy", True, [], True)
    assert result["hit"]["stack"] == []


def test_wound_modifier_applies():
    mods = [{"label": "Lethal Hits", "value": 1, "roll_type": "wound", "source": "stratagem"}]
    result = resolve_attack_modifiers(3, 4, 5, "Rapid Fire", False, mods, False)
    assert result["wound"]["base"] == 5
    assert result["wound"]["modified"] == 4


def test_hit_and_wound_mods_independent():
    mods = [
        {"label": "Proto Hit", "value": 1, "roll_type": "hit", "source": "protocol"},
        {"label": "Proto Wound", "value": 1, "roll_type": "wound", "source": "protocol"},
    ]
    result = resolve_attack_modifiers(4, 4, 5, "Rapid Fire", False, mods, False)
    assert result["hit"]["modified"] == 3
    assert result["wound"]["modified"] == 4


# ---------------------------------------------------------------------------
# resolve_save
# ---------------------------------------------------------------------------


def test_save_no_ap():
    result = resolve_save(3, None, 0, [])
    assert result["armour"] == 3
    assert result["armour_eff"] == 3
    assert result["invuln"] is None
    assert result["effective"] == 3
    assert result["using_invuln"] is False
    assert result["save_bonus"] == 0


def test_save_with_ap():
    result = resolve_save(3, None, -2, [])
    assert result["armour_eff"] == 5
    assert result["effective"] == 5
    assert not result["using_invuln"]


def test_save_invuln_better_than_armour():
    result = resolve_save(3, 4, -3, [])  # armour 3+ with AP-3 → 6+, invuln 4+
    assert result["armour_eff"] == 6
    assert result["invuln"] == 4
    assert result["effective"] == 4
    assert result["using_invuln"] is True


def test_save_invuln_worse_than_armour():
    result = resolve_save(3, 5, 0, [])  # armour 3+, invuln 5+ (worse)
    assert result["effective"] == 3
    assert not result["using_invuln"]


def test_save_bonus_improves_armour():
    mods = [{"label": "Protocol", "value": 1}]
    result = resolve_save(4, None, -1, mods)  # 4+ with AP-1 → 5+, protocol +1 → 4+
    assert result["armour_eff"] == 5
    assert result["save_bonus"] == 1
    assert result["effective"] == 4


def test_save_bonus_does_not_improve_invuln():
    mods = [{"label": "Protocol", "value": 1}]
    result = resolve_save(3, 4, -3, mods)  # armour 3+ AP-3 → 6+ with +1 → 5+; invuln 4+
    assert result["effective"] == 4  # invuln 4+ wins
    assert result["using_invuln"] is True


def test_save_capped_at_7():
    result = resolve_save(3, None, -5, [])  # armour 3+ AP-5 → 8+ → capped at 7
    assert result["effective"] == 7


def test_save_floored_at_2_armour_path():
    """Regression (S122/F3): an unmodified 1 always fails (core_rules.txt), so no
    save can ever be effectively better than 2+, even with strong buffs (e.g.
    high Cover stacking on an already-good armour save).
    """
    mods = [{"label": "Cover", "value": 1}]
    result = resolve_save(2, None, 0, mods)  # armour 2+, +1 bonus → would be 1+
    assert result["effective"] == 2
    assert result["using_invuln"] is False


def test_save_floored_at_2_invuln_path():
    """Same floor applies via the invulnerable-save branch (invuln is still a
    saving throw rolled on a D6 — unmodified 1 always fails)."""
    result = resolve_save(6, 1, 0, [])  # invuln 1+ beats armour 6+
    assert result["using_invuln"] is True
    assert result["effective"] == 2


def test_save_stack_returned():
    mods = [{"label": "Protocol", "value": 1}]
    result = resolve_save(4, None, 0, mods)
    assert result["stack"] == mods


# ---------------------------------------------------------------------------
# resolve_fnp
# ---------------------------------------------------------------------------


def test_fnp_normal():
    assert resolve_fnp(5, False) == 5


def test_fnp_six_plus():
    assert resolve_fnp(6, False) == 6


def test_fnp_none_when_unit_has_no_fnp():
    assert resolve_fnp(None, False) is None


def test_fnp_ignored_by_weapon():
    assert resolve_fnp(5, True) is None


def test_fnp_no_fnp_and_ignores():
    assert resolve_fnp(None, True) is None


# ---------------------------------------------------------------------------
# apply_damage_attacks (6d-v2)
# ---------------------------------------------------------------------------


def test_apply_damage_attacks_1lp_only_models():
    assert apply_damage_attacks(3, 0, 0, 1) == 3


def test_apply_damage_attacks_3lp_models():
    assert apply_damage_attacks(2, 0, 0, 3) == 6


def test_apply_damage_attacks_wounds_on_front():
    assert apply_damage_attacks(1, 2, 0, 3) == 5


def test_apply_damage_attacks_mortal_wounds_only():
    assert apply_damage_attacks(0, 0, 4, 1) == 4


def test_apply_damage_attacks_combined():
    assert apply_damage_attacks(2, 1, 3, 3) == 10


def test_apply_damage_attacks_zero():
    assert apply_damage_attacks(0, 0, 0, 1) == 0


def test_apply_damage_attacks_mortal_added_to_normal():
    # 1 model dead (1LP) + 2 mortal wounds = 3 total damage
    assert apply_damage_attacks(1, 0, 2, 1) == 3
