"""Tests for attack declaration helpers: _total_attacks_int, _compute_attacks."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from types import SimpleNamespace  # noqa: E402

from uiLayout._common import (  # noqa: E402
    _compute_attacks,
    _group_melee_budget,
    _total_attacks_int,
)


def _melee_weapon(effect=None, max_attacks=None):  # type: ignore[no-untyped-def]
    profile = SimpleNamespace(is_melee=True, effect=effect, max_attacks=max_attacks)
    return SimpleNamespace(profiles=[profile])


# ---------------------------------------------------------------------------
# _group_melee_budget — base + extra-attack weapon bonuses (6n Bug: Boss Nob 4)
# ---------------------------------------------------------------------------


def test_group_budget_plain_weapons() -> None:
    assert _group_melee_budget([_melee_weapon()], 9, 3) == 27


def test_group_budget_includes_extra_attacks_weapon() -> None:
    """Boss Nob with power klaw + choppa under WAAAGH: 1×(2+1) base + 1 choppa = 4."""
    power_klaw = _melee_weapon()
    choppa = _melee_weapon(effect={"type": "extra_attacks", "amount": 1})
    assert _group_melee_budget([power_klaw, choppa], 1, 3) == 4


def test_group_budget_capped_weapon_adds_its_cap() -> None:
    attack_squig = _melee_weapon(effect={"type": "extra_attacks"}, max_attacks=2)
    assert _group_melee_budget([_melee_weapon(), attack_squig], 1, 4) == 6


# ---------------------------------------------------------------------------
# _total_attacks_int — melee ("Melee" / "*") and fixed counts
# ---------------------------------------------------------------------------


def test_melee_keyword_returns_models_times_unit_attacks() -> None:
    assert _total_attacks_int("Melee", 10, 2) == 20


def test_star_keyword_returns_models_times_unit_attacks() -> None:
    assert _total_attacks_int("*", 5, 3) == 15


def test_fixed_attack_count_ignores_unit_attacks() -> None:
    assert _total_attacks_int("2", 10, 3) == 20


def test_dice_based_returns_none() -> None:
    assert _total_attacks_int("D3", 5, 2) is None


def test_waaagh_bonus_applied_via_unit_attacks_param() -> None:
    # WAAAGH! +1 is passed as unit_attacks + 1 by the caller
    assert _total_attacks_int("Melee", 20, 2 + 1) == 60


def test_waaagh_bonus_does_not_affect_fixed_weapon_attacks() -> None:
    # Fixed weapon attacks ("2") are independent of unit_attacks
    assert _total_attacks_int("2", 20, 2 + 1) == 40


def test_single_model_melee() -> None:
    assert _total_attacks_int("Melee", 1, 4) == 4


def test_single_model_melee_with_waaagh_bonus() -> None:
    assert _total_attacks_int("Melee", 1, 4 + 1) == 5


# ---------------------------------------------------------------------------
# _compute_attacks — display string
# ---------------------------------------------------------------------------


def test_compute_melee_returns_models_times_unit_attacks() -> None:
    assert _compute_attacks("Melee", 10, 2) == "20"


def test_compute_fixed_returns_models_times_weapon_attacks() -> None:
    assert _compute_attacks("2", 10, 3) == "20"


def test_compute_dice_returns_product_string() -> None:
    result = _compute_attacks("D3", 5, 2)
    assert result == "5×D3"


def test_compute_star_returns_models_times_unit_attacks() -> None:
    assert _compute_attacks("*", 3, 4) == "12"


# ---------------------------------------------------------------------------
# Entry filter invariant — entries with atk_override=0 are excluded
# ---------------------------------------------------------------------------


def test_entry_filter_excludes_zero_atk_override() -> None:
    entries = [
        {"weapon_name": "Power Klaw", "atk_override": 3, "models_count": 1},
        {"weapon_name": "Slugga", "atk_override": 0, "models_count": 1},
    ]
    filtered = [e for e in entries if e.get("atk_override", e["models_count"]) > 0]
    assert len(filtered) == 1
    assert filtered[0]["weapon_name"] == "Power Klaw"


def test_entry_filter_excludes_zero_models_count_in_shooting() -> None:
    entries = [
        {"weapon_name": "Bolt Rifle", "models_count": 5},
        {"weapon_name": "Bolt Rifle", "models_count": 0},
    ]
    filtered = [e for e in entries if e.get("atk_override", e["models_count"]) > 0]
    assert len(filtered) == 1
    assert filtered[0]["models_count"] == 5


def test_entry_filter_keeps_all_nonzero_entries() -> None:
    entries = [
        {"weapon_name": "Power Klaw", "atk_override": 2, "models_count": 1},
        {"weapon_name": "Voidblade", "atk_override": 2, "models_count": 1},
    ]
    filtered = [e for e in entries if e.get("atk_override", e["models_count"]) > 0]
    assert len(filtered) == 2


# ---------------------------------------------------------------------------
# extra_attacks effect — Klasse 3b (max_attacks cap) and 3a (additive)
# ---------------------------------------------------------------------------

_EFFECT_EXTRA_2 = {"type": "extra_attacks", "amount": 2}
_EFFECT_EXTRA_1 = {"type": "extra_attacks", "amount": 1}
_EFFECT_EXTRA_4 = {"type": "extra_attacks", "amount": 4}


def test_total_attacks_int_extra_attacks_capped_attack_squig() -> None:
    # attack_squig: max_attacks=2 → always 2 per model, independent of unit.attacks
    assert _total_attacks_int("Melee", 1, 3, _EFFECT_EXTRA_2, max_attacks=2) == 2


def test_total_attacks_int_extra_attacks_capped_squighog_jaws_multi_model() -> None:
    # squighog_jaws: max_attacks=2, 3 models → 6 total
    assert _total_attacks_int("Melee", 3, 4, _EFFECT_EXTRA_2, max_attacks=2) == 6


def test_total_attacks_int_extra_attacks_capped_butcha_boyz() -> None:
    # butcha_boyz: max_attacks=4, 1 model → 4 total
    assert _total_attacks_int("Melee", 1, 2, _EFFECT_EXTRA_4, max_attacks=4) == 4


def test_total_attacks_int_extra_attacks_additive_choppa() -> None:
    # choppa: no max_attacks, amount=1 → unit.attacks + 1 per model
    assert _total_attacks_int("Melee", 10, 2, _EFFECT_EXTRA_1) == 30  # 10 * (2+1)


def test_total_attacks_int_extra_attacks_additive_with_waaagh() -> None:
    # choppa + WAAAGH! bonus: unit_attacks=3 (2+1 waaagh), amount=1 → 10 * (3+1)
    assert _total_attacks_int("Melee", 10, 3, _EFFECT_EXTRA_1) == 40


def test_total_attacks_int_extra_attacks_capped_ignores_unit_attacks() -> None:
    # Capped weapons: max_attacks takes precedence over unit.attacks entirely
    # Even with WAAAGH! bonus, a capped weapon stays at max_attacks
    assert _total_attacks_int("Melee", 10, 3, _EFFECT_EXTRA_2, max_attacks=2) == 20


def test_compute_attacks_extra_attacks_capped() -> None:
    assert _compute_attacks("Melee", 3, 4, _EFFECT_EXTRA_2, max_attacks=2) == "6"


def test_compute_attacks_extra_attacks_additive() -> None:
    # 10 models, unit.attacks=2, +1 → 30
    assert _compute_attacks("Melee", 10, 2, _EFFECT_EXTRA_1) == "30"


def test_compute_attacks_no_extra_attacks_effect_unchanged() -> None:
    # No effect → existing behaviour: models * unit.attacks
    assert _compute_attacks("Melee", 10, 2) == "20"


def test_total_attacks_int_no_extra_attacks_effect_unchanged() -> None:
    assert _total_attacks_int("Melee", 10, 2) == 20


# ---------------------------------------------------------------------------
# B-110: multi-profile melee weapon profile-name derivation must use
# name_en (WeaponProfile has no `name` attribute). UI-unreachable today (no
# melee weapon in the data has >=2 profiles) — this is a latent-bug
# regression test at the object/derivation level, not a click-path test.
# ---------------------------------------------------------------------------


def test_melee_profile_name_derivation_uses_name_en_without_attribute_error() -> None:
    from gameObjects.weapon import WeaponProfile

    profiles = [
        WeaponProfile(
            weapon_type="Melee",
            range_inches=0,
            attacks="3",
            strength=8,
            ap=-2,
            damage="3",
            is_melee=True,
            name_en="Sword",
        ),
        WeaponProfile(
            weapon_type="Melee",
            range_inches=0,
            attacks="D3",
            strength=4,
            ap=0,
            damage="1",
            is_melee=True,
            name_en="",
        ),
    ]

    # Mirrors the melee-branch derivation in uiLayout/_common.py.
    p_names = [p.name_en or f"Profile {j + 1}" for j, p in enumerate(profiles)]

    assert p_names == ["Sword", "Profile 2"]
    assert not hasattr(profiles[0], "name")
