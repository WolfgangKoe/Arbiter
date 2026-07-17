"""Tests for state_badges_html() and _parse_strength()."""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.abilityEngine as _eng  # noqa: E402
import gameMechanic.gameState as _gs  # noqa: E402
import gameMechanic.stratagemEngine as _se  # noqa: E402
import gameMechanic.unitMutations as _um  # noqa: E402
import uiLayout._common as common  # noqa: E402
from gameMechanic.abilityEngine import (  # noqa: E402
    get_active_round_choice_light_cover_if_stationary,
)
from gameObjects.ability import Ability, Condition, Effect, Trigger  # noqa: E402
from gameObjects.loader import load_stratagems  # noqa: E402
from gameObjects.unit import ModelGroup, Unit  # noqa: E402
from gameObjects.weapon import Weapon, WeaponProfile  # noqa: E402
from uiLayout._common import (  # noqa: E402
    _collect_atk_modifiers,
    _collect_def_save_modifiers,
    _parse_strength,
    state_badges_html,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _state(
    movement_choice: str | None = None,
    charged: bool = False,
    shot: bool = False,
    fought: bool = False,
    cast: bool = False,
    in_melee: bool = False,
    in_reserve: bool = False,
    mwbd: bool = False,
) -> dict:
    return {
        "movement_choice": movement_choice,
        "turn_flags": {
            "advanced": movement_choice == "advanced",
            "retreated": movement_choice == "retreated",
            "charged": charged,
            "shot": shot,
            "fought": fought,
            "cast": cast,
        },
        "in_melee": in_melee,
        "in_reserve": in_reserve,
        "active_buffs": (
            [{"ability_id": "mwbd", "badge_label": "MWBD", "effect_type": "buff_roll"}]
            if mwbd
            else []
        ),
    }


# ---------------------------------------------------------------------------
# Movement badge tests
# ---------------------------------------------------------------------------


def test_no_movement_choice_shows_no_movement_badge() -> None:
    html = state_badges_html(_state(movement_choice=None))
    for badge in ("MOVED", "STATIONARY", "ADVANCED", "RETREATED"):
        assert badge not in html


def test_movement_choice_moved_shows_moved_badge() -> None:
    assert "MOVED" in state_badges_html(_state(movement_choice="moved"))


def test_movement_choice_stationary_shows_stationary_badge() -> None:
    assert "STATIONARY" in state_badges_html(_state(movement_choice="stationary"))


def test_movement_choice_advanced_shows_advanced_badge() -> None:
    assert "ADVANCED" in state_badges_html(_state(movement_choice="advanced"))


def test_movement_choice_retreated_shows_retreated_badge() -> None:
    assert "RETREATED" in state_badges_html(_state(movement_choice="retreated"))


def test_movement_badge_does_not_show_other_movement_types() -> None:
    html = state_badges_html(_state(movement_choice="advanced"))
    assert "RETREATED" not in html
    assert "MOVED" not in html
    assert "STATIONARY" not in html


# ---------------------------------------------------------------------------
# Combat badge tests
# ---------------------------------------------------------------------------


def test_charged_flag_shows_charged_badge() -> None:
    assert "CHARGED" in state_badges_html(_state(charged=True))


def test_in_melee_without_charged_shows_in_melee_badge() -> None:
    html = state_badges_html(_state(in_melee=True))
    assert "IN MELEE" in html
    assert "CHARGED" not in html


def test_charged_suppresses_in_melee_badge() -> None:
    html = state_badges_html(_state(charged=True, in_melee=True))
    assert "CHARGED" in html
    assert "IN MELEE" not in html


def test_in_reserve_shows_reserve_badge() -> None:
    assert "RESERVE" in state_badges_html(_state(in_reserve=True))


# ---------------------------------------------------------------------------
# SHOT badge tests
# ---------------------------------------------------------------------------


def test_shot_flag_shows_shot_badge() -> None:
    assert "SHOT" in state_badges_html(_state(movement_choice="stationary", shot=True))


def test_shot_is_additive_with_stationary() -> None:
    html = state_badges_html(_state(movement_choice="stationary", shot=True))
    assert "STATIONARY" in html
    assert "SHOT" in html


def test_shot_is_additive_with_moved() -> None:
    html = state_badges_html(_state(movement_choice="moved", shot=True))
    assert "MOVED" in html
    assert "SHOT" in html


def test_shot_is_additive_with_charged() -> None:
    """Szenario 4: schoss und charged — CHARGED + SHOT zeigen."""
    html = state_badges_html(_state(movement_choice="moved", charged=True, shot=True))
    assert "CHARGED" in html
    assert "SHOT" in html
    assert "MOVED" not in html


# ---------------------------------------------------------------------------
# FOUGHT badge tests
# ---------------------------------------------------------------------------


def test_fought_flag_shows_fought_badge() -> None:
    assert "FOUGHT" in state_badges_html(_state(fought=True))


def test_fought_replaces_charged_in_display() -> None:
    """Szenario 5: nach Kampf verschwindet CHARGED — FOUGHT zeigt stattdessen."""
    html = state_badges_html(_state(charged=True, fought=True))
    assert "FOUGHT" in html
    assert "CHARGED" not in html


def test_fought_replaces_movement_badge() -> None:
    """FOUGHT hat höchste Priorität im Bewegungs-Slot."""
    html = state_badges_html(_state(movement_choice="moved", fought=True))
    assert "FOUGHT" in html
    assert "MOVED" not in html


def test_fought_with_in_melee_shows_both() -> None:
    """Szenario 8: FOUGHT + IN MELEE — kämpfte, noch gebunden."""
    html = state_badges_html(_state(in_melee=True, fought=True))
    assert "FOUGHT" in html
    assert "IN MELEE" in html


def test_fought_does_not_suppress_in_melee() -> None:
    """IN MELEE wird nur bei CHARGED unterdrückt, nicht bei FOUGHT."""
    html = state_badges_html(_state(charged=True, fought=True, in_melee=True))
    assert "FOUGHT" in html
    assert "IN MELEE" in html
    assert "CHARGED" not in html


def test_shot_fought_in_melee_all_show() -> None:
    """Szenario 4 Vollzustand: SHOT + FOUGHT + IN MELEE."""
    html = state_badges_html(
        _state(movement_choice="moved", charged=True, shot=True, fought=True, in_melee=True)
    )
    assert "FOUGHT" in html
    assert "SHOT" in html
    assert "IN MELEE" in html
    assert "CHARGED" not in html
    assert "MOVED" not in html


# ---------------------------------------------------------------------------
# Combination edge cases
# ---------------------------------------------------------------------------


def test_charged_suppresses_movement_badge() -> None:
    """When charged=True, the movement badge is hidden — CHARGED is the relevant state."""
    html = state_badges_html(_state(movement_choice="moved", charged=True))
    assert "MOVED" not in html
    assert "CHARGED" in html


def test_charged_suppresses_advanced_badge() -> None:
    """ADVANCED is also suppressed when charged."""
    html = state_badges_html(_state(movement_choice="advanced", charged=True))
    assert "ADVANCED" not in html
    assert "CHARGED" in html


def test_in_reserve_suppresses_movement_badge() -> None:
    """RESERVE units don't show a movement badge."""
    html = state_badges_html(_state(movement_choice="advanced", in_reserve=True))
    assert "ADVANCED" not in html
    assert "RESERVE" in html


# ---------------------------------------------------------------------------
# _parse_strength — all notation variants
# ---------------------------------------------------------------------------


def test_parse_strength_fixed_int() -> None:
    assert _parse_strength(5, 4) == 5


def test_parse_strength_fixed_string() -> None:
    assert _parse_strength("7", 4) == 7


def test_parse_strength_user() -> None:
    assert _parse_strength("User", 4) == 4


def test_parse_strength_user_lowercase() -> None:
    assert _parse_strength("user", 6) == 6


def test_parse_strength_plus_n() -> None:
    assert _parse_strength("+2", 4) == 6


def test_parse_strength_times_n() -> None:
    assert _parse_strength("×2", 4) == 8


def test_parse_strength_minus_n() -> None:
    assert _parse_strength("-1", 5) == 4


def test_parse_strength_star() -> None:
    assert _parse_strength("*", 99) == 0


def test_parse_strength_user_times_n() -> None:
    """Regression: power_klaw / killsaw strength 'User×2' must not crash."""
    assert _parse_strength("User×2", 4) == 8


def test_parse_strength_user_times_n_high_strength() -> None:
    assert _parse_strength("User×2", 6) == 12


def test_parse_strength_user_plus_n() -> None:
    assert _parse_strength("User+3", 5) == 8


def test_parse_strength_user_minus_n() -> None:
    assert _parse_strength("User-1", 5) == 4


def test_parse_strength_power_klaw_ork_boyz() -> None:
    """Regression: Ork Boyz (S4) with power_klaw (User×2) → S8."""
    assert _parse_strength("User×2", 4) == 8


def test_parse_strength_power_klaw_warboss() -> None:
    """Regression: Warboss in Mega Armour (S6) with dread_klaw (User×2) → S12."""
    assert _parse_strength("User×2", 6) == 12


def test_mwbd_shows_when_active() -> None:
    assert "MWBD" in state_badges_html(_state(movement_choice="stationary", mwbd=True))


def test_mwbd_is_additive() -> None:
    html = state_badges_html(_state(movement_choice="stationary", shot=True, mwbd=True))
    assert "STATIONARY" in html
    assert "SHOT" in html
    assert "MWBD" in html


# ---------------------------------------------------------------------------
# CAST badge tests
# ---------------------------------------------------------------------------


def test_cast_flag_shows_cast_badge() -> None:
    assert "CAST" in state_badges_html(_state(movement_choice="stationary", cast=True))


def test_cast_is_additive_with_stationary() -> None:
    html = state_badges_html(_state(movement_choice="stationary", cast=True))
    assert "STATIONARY" in html
    assert "CAST" in html


def test_cast_is_additive_with_shot() -> None:
    html = state_badges_html(_state(movement_choice="stationary", shot=True, cast=True))
    assert "STATIONARY" in html
    assert "SHOT" in html
    assert "CAST" in html


def test_cast_not_shown_when_false() -> None:
    assert "CAST" not in state_badges_html(_state(movement_choice="stationary"))


def test_lookup_raises_keyerror_for_unknown_unit(monkeypatch) -> None:
    fake_units = [SimpleNamespace(id="known.unit")]
    monkeypatch.setattr(common, "units_list_for", lambda faction: fake_units)
    monkeypatch.setattr("gameMechanic.gameState.unit_id_from_state_key", lambda uid: "missing.unit")
    with pytest.raises(KeyError, match="out of sync"):
        common.lookup("Necrons", "missing.unit")


# ---------------------------------------------------------------------------
# Eternal Guardian D1 — light_cover_if_stationary (Plan 025 Step 4)
# ---------------------------------------------------------------------------


class _SS(dict):
    """Minimal session-state stand-in (attribute + key access)."""

    def __getattr__(self, key: str):  # type: ignore[override]
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _eg_session(*, stationary: bool) -> _SS:
    """Session with Eternal Guardian primary active; unit movement set accordingly.

    Binds the session onto every module's ``st`` reference — not just the local mock —
    because abilityEngine, gameState, and _common each hold their own imported ``st``
    object captured at import time (see test_round_choice_player_keyed._install).
    """
    session = _SS(
        first_player="Necrons",
        p1_faction_dir="necrons",
        p2_faction_dir="necrons",
    )
    session["round_choice_active_Necrons"] = "wh40k_9e.necrons.faction.protocol_eternal_guardian"
    session["round_choice_directive_Necrons"] = "primary"
    movement = "stationary" if stationary else "moved"
    session["p1_units"] = {"test.unit": {"movement_choice": movement}}
    _st_mock.session_state = session
    _eng.st.session_state = session
    _gs.st.session_state = session
    common.st.session_state = session
    return session


def test_eternal_guardian_d1_light_cover_true_when_stationary() -> None:
    # D1 active + unit did not move → engine returns True (auto-grant condition met).
    _eg_session(stationary=True)
    assert get_active_round_choice_light_cover_if_stationary("Necrons", "test.unit") is True


def test_eternal_guardian_d1_light_cover_false_when_moved() -> None:
    # D1 active + unit moved → engine returns False (condition not met).
    _eg_session(stationary=False)
    assert get_active_round_choice_light_cover_if_stationary("Necrons", "test.unit") is False


def test_collect_def_save_modifiers_no_double_light_cover() -> None:
    # Eternal Guardian D1 active + unit stationary → _collect_def_save_modifiers must NOT
    # add a light-cover modifier. The +1 from D1 is injected solely via the checkbox
    # mechanic in the render path (Variante C). Adding it here would cause a double-+1.
    _eg_session(stationary=True)
    # No active_modifiers in session → empty result regardless of D1 state.
    mods = _collect_def_save_modifiers("Necrons", "shooting", False, "test.unit")
    assert mods == [], (
        f"Expected no save modifier from _collect_def_save_modifiers "
        f"(light cover must come from checkbox only), got: {mods}"
    )


def test_collect_def_save_modifiers_passes_active_modifiers() -> None:
    # Non-light-cover active_modifiers still flow through (unrelated to D1).
    session = _eg_session(stationary=True)
    session["active_modifiers"] = [
        {
            "source": "Test Stratagem",
            "effect": {"roll_type": "save", "target": "defender", "value": 1},
        }
    ]
    mods = _collect_def_save_modifiers("Necrons", "shooting", False, "test.unit")
    assert mods == [{"label": "Test Stratagem", "value": 1}]


# ---------------------------------------------------------------------------
# S135 Paket 4a — _collect_atk_modifiers(): defender-scoped hit/wound modifiers
# (Shadows of Drazak, Whirling Onslaught — reactive GOs the DEFENDER activates
# on their own targeted unit, registered with target="defender" + unit_key).
# ---------------------------------------------------------------------------


def test_collect_atk_modifiers_defender_scoped_to_targeted_unit() -> None:
    """A target="defender" modifier registered for the exact unit being attacked
    applies — mirrors stratagem_strength_bonus's attacker-side unit_key scoping."""
    _eg_session(stationary=True)
    common.st.session_state["active_modifiers"] = [
        {
            "unit_key": "wh40k_9e.necrons.unit.flayed_ones",
            "source": "Shadows of Drazak",
            "effect": {"roll_type": "hit", "value": -1, "target": "defender"},
        }
    ]
    mods = _collect_atk_modifiers(
        "Orks", {}, "shooting", False, def_uid="wh40k_9e.necrons.unit.flayed_ones"
    )
    assert mods == [
        {"label": "Shadows of Drazak", "value": -1, "roll_type": "hit", "source": "stratagem"}
    ]


def test_collect_atk_modifiers_defender_not_scoped_to_other_unit() -> None:
    """The same modifier must NOT apply when a DIFFERENT unit is being attacked —
    otherwise activating it for one unit would debuff attacks against every unit."""
    _eg_session(stationary=True)
    common.st.session_state["active_modifiers"] = [
        {
            "unit_key": "wh40k_9e.necrons.unit.flayed_ones",
            "source": "Shadows of Drazak",
            "effect": {"roll_type": "hit", "value": -1, "target": "defender"},
        }
    ]
    mods = _collect_atk_modifiers(
        "Orks", {}, "shooting", False, def_uid="wh40k_9e.necrons.unit.warriors"
    )
    assert mods == []


def test_collect_atk_modifiers_defender_target_ignored_without_def_uid() -> None:
    """Regression guard: callers that omit def_uid (default "") must not leak a
    defender-scoped modifier — the empty string can never match a real unit_key."""
    _eg_session(stationary=True)
    common.st.session_state["active_modifiers"] = [
        {
            "unit_key": "wh40k_9e.necrons.unit.flayed_ones",
            "source": "Shadows of Drazak",
            "effect": {"roll_type": "hit", "value": -1, "target": "defender"},
        }
    ]
    mods = _collect_atk_modifiers("Orks", {}, "shooting", False)
    assert mods == []


def test_collect_atk_modifiers_attacker_target_unscoped_by_def_uid() -> None:
    """Pre-existing behaviour unchanged: an attacker/any-targeted modifier still
    applies regardless of def_uid — only the new defender branch is unit_key-scoped."""
    _eg_session(stationary=True)
    common.st.session_state["active_modifiers"] = [
        {
            "unit_key": "wh40k_9e.necrons.unit.warriors",
            "source": "Extermination Protocols",
            "effect": {"roll_type": "hit", "value": 1, "target": "attacker"},
        }
    ]
    mods = _collect_atk_modifiers("Necrons", {}, "shooting", False, def_uid="anything")
    assert mods == [
        {
            "label": "Extermination Protocols",
            "value": 1,
            "roll_type": "hit",
            "source": "stratagem",
        }
    ]


# ---------------------------------------------------------------------------
# R-COMBAT-17: Rapid Fire hint caption
# ---------------------------------------------------------------------------


def test_rapid_fire_caption_shown_for_rapid_fire_weapon() -> None:
    """R-COMBAT-17: Rapid Fire weapon with positive range shows half-range hint."""
    from uiLayout._common import _rapid_fire_caption

    caption = _rapid_fire_caption("Rapid Fire 12", 12)
    assert caption == '[RAPID FIRE · 12" · ½ = 6"]'


def test_rapid_fire_caption_shown_for_rapid_fire_assault_variant() -> None:
    """R-COMBAT-17: 'Rapid Fire Assault' variant also triggers caption."""
    from uiLayout._common import _rapid_fire_caption

    caption = _rapid_fire_caption("Rapid Fire Assault 18", 18)
    assert caption == '[RAPID FIRE · 18" · ½ = 9"]'


def test_rapid_fire_caption_hidden_for_non_rapid_fire() -> None:
    """R-COMBAT-17: Non-Rapid-Fire weapon returns None (no caption)."""
    from uiLayout._common import _rapid_fire_caption

    caption = _rapid_fire_caption("Bolter", 24)
    assert caption is None


def test_rapid_fire_caption_hidden_for_zero_range() -> None:
    """R-COMBAT-17: Rapid Fire weapon with zero range returns None."""
    from uiLayout._common import _rapid_fire_caption

    caption = _rapid_fire_caption("Rapid Fire 0", 0)
    assert caption is None


def test_rapid_fire_caption_rounds_down_half_range() -> None:
    """R-COMBAT-17: Half-range uses integer division (rounds down)."""
    from uiLayout._common import _rapid_fire_caption

    caption = _rapid_fire_caption("Rapid Fire 15", 15)
    assert caption == '[RAPID FIRE · 15" · ½ = 7"]'  # 15 // 2 = 7, not 7.5


# ---------------------------------------------------------------------------
# R-PROTO-02: Conquering Tyrant Directive 1 (Aura Range Bonus)
# ---------------------------------------------------------------------------


def test_conquering_tyrant_primary_aura_range_bonus_data_feeds_hint() -> None:
    """R-PROTO-02: the aura_range_bonus effect carries the data the table hint needs.

    Structural check of the ``affects`` list the (now removed) hint builder used to read;
    the production consumer (``armyCard._render_aura_range_hint``) was removed in S138, and
    the dead hint-builder function + its tests were removed in S139 (Retro-Maßnahme 2).
    This test just guards the YAML contract, which other R-PROTO-02 checks still rely on.
    """
    from pathlib import Path

    import yaml

    yaml_path = (
        Path(__file__).resolve().parent.parent.parent
        / "data/wh40k_9e/necrons/faction_abilities.yaml"
    )
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    protocol = None
    for item in data.get("abilities", []):
        if item.get("id") == "wh40k_9e.necrons.faction.protocol_conquering_tyrant":
            protocol = item
            break

    assert protocol is not None, "protocol_conquering_tyrant not found in abilities"
    primary_effect = protocol["directives"]["primary"].get("effect", {})
    assert primary_effect.get("type") == "aura_range_bonus"
    assert primary_effect.get("value") == 3
    assert primary_effect.get("max") == 12
    assert primary_effect.get("enforcement") == "table"
    assert primary_effect.get("affects") == [
        "Lord's Will",
        "My Will Be Done",
        "Rites of Reanimation",
    ]


# ---------------------------------------------------------------------------
# Plan 015 — spend_stratagem() canonical CP/usage/modifier bookkeeping
# ---------------------------------------------------------------------------


def _strat(
    sid: str = "test.strat",
    cp_cost: int = 1,
    once_per_battle: bool = False,
    modifier=None,
    effect=None,
) -> object:
    from gameObjects.stratagem import Stratagem

    return Stratagem(
        id=sid,
        name_en="Test GO",
        cp_cost=cp_cost,
        phase="any",
        stage="active",
        player="both",
        once_per_battle=once_per_battle,
        modifier=modifier,
        effect=effect,
    )


def _spend_session(**extra) -> _SS:  # type: ignore[no-untyped-def]
    session = _SS(
        cp={"Necrons": 5},
        used_stratagem_ids={},
        used_stratagem_battle_ids={},
        active_modifiers=[],
        phase_idx=5,  # "charge"
        round=2,
        **extra,
    )
    common.st.session_state = session
    _gs.st.session_state = session
    _um.st.session_state = session
    return session


def test_spend_stratagem_deducts_cp() -> None:
    session = _spend_session()
    common.spend_stratagem(_strat(cp_cost=2), "Necrons")
    assert session["cp"]["Necrons"] == 3


def test_spend_stratagem_marks_used_this_phase() -> None:
    session = _spend_session()
    common.spend_stratagem(_strat(sid="strat.a"), "Necrons")
    assert "strat.a" in session["used_stratagem_ids"]["Necrons"]


def test_spend_stratagem_once_per_battle_marks_battle_set_too() -> None:
    session = _spend_session()
    common.spend_stratagem(_strat(sid="strat.opb", once_per_battle=True), "Necrons")
    assert "strat.opb" in session["used_stratagem_battle_ids"]["Necrons"]


def test_spend_stratagem_without_once_per_battle_leaves_battle_set_untouched() -> None:
    session = _spend_session()
    common.spend_stratagem(_strat(sid="strat.normal"), "Necrons")
    assert session["used_stratagem_battle_ids"] == {}


def test_spend_stratagem_registers_active_modifier_with_unit_key() -> None:
    from gameObjects.stratagem import StratagemModifier

    session = _spend_session()
    modifier = StratagemModifier(
        roll_type="wound",
        value=1,
        target="attacker",
        expires_at="phase_end",
        source_label="Test GO",
    )
    common.spend_stratagem(_strat(sid="strat.mod", modifier=modifier), "Necrons", "unit#1")
    mods = session["active_modifiers"]
    assert len(mods) == 1
    assert mods[0]["unit_key"] == "unit#1"
    assert mods[0]["effect"]["roll_type"] == "wound"
    assert mods[0]["expires_at_phase"] == "charge"  # phase_end → current phase


# ---------------------------------------------------------------------------
# S139 B12a — use-anchor bookkeeping: spend_stratagem(anchor_id=...),
# undo_stratagem(), stratagem_use_anchor(), stratagem_used_here()
# ---------------------------------------------------------------------------


def test_spend_stratagem_without_anchor_id_records_no_anchor() -> None:
    """Callers that omit anchor_id (e.g. the inline Command Re-Roll offer, still
    B12c scope) must stay a no-op on the anchor bookkeeping — only the three
    Karten-anchor callers (central list, reactive box, Advance-reroll card) pass
    one (S139 B12b)."""
    session = _spend_session()
    common.spend_stratagem(_strat(sid="strat.a"), "Necrons")
    assert session.get("stratagem_use_anchors", {}) == {}


def test_spend_stratagem_with_anchor_id_records_anchor_and_unit_key() -> None:
    session = _spend_session()
    common.spend_stratagem(_strat(sid="strat.a"), "Necrons", "unit#1", anchor_id="anchor_x")
    assert session["stratagem_use_anchors"]["Necrons"]["strat.a"] == {
        "anchor_id": "anchor_x",
        "unit_key": "unit#1",
    }


def test_spend_stratagem_with_anchor_id_and_no_unit_key() -> None:
    session = _spend_session()
    common.spend_stratagem(_strat(sid="strat.a"), "Necrons", anchor_id="anchor_x")
    assert session["stratagem_use_anchors"]["Necrons"]["strat.a"]["unit_key"] is None


def test_stratagem_use_anchor_returns_none_when_never_spent() -> None:
    _spend_session()
    assert common.stratagem_use_anchor("Necrons", "strat.never") is None


def test_stratagem_use_anchor_returns_recorded_tuple() -> None:
    _spend_session()
    common.spend_stratagem(_strat(sid="strat.a"), "Necrons", "unit#1", anchor_id="anchor_x")
    assert common.stratagem_use_anchor("Necrons", "strat.a") == ("anchor_x", "unit#1")


def test_stratagem_used_here_true_for_matching_anchor() -> None:
    _spend_session()
    common.spend_stratagem(_strat(sid="strat.a"), "Necrons", anchor_id="anchor_x")
    assert common.stratagem_used_here("Necrons", "strat.a", "anchor_x") is True


def test_stratagem_used_here_false_for_different_anchor() -> None:
    """Regression guard for the reported bug (S137): using the GO at one anchor
    must not make a DIFFERENT anchor claim "used here" too."""
    _spend_session()
    common.spend_stratagem(_strat(sid="strat.a"), "Necrons", anchor_id="anchor_x")
    assert common.stratagem_used_here("Necrons", "strat.a", "anchor_y") is False


def test_stratagem_used_here_false_when_never_spent() -> None:
    _spend_session()
    assert common.stratagem_used_here("Necrons", "strat.never", "anchor_x") is False


def test_stratagem_used_here_scoped_per_player_not_globally() -> None:
    """S138-Testpflicht (F1): Player A spending a GO must never block/blend
    into Player B's use of the SAME GO id — the anchor bookkeeping is keyed
    per faction, so B's query for their own anchor is unaffected by A's spend."""
    session = _spend_session()
    session["cp"]["Orks"] = 5
    common.spend_stratagem(_strat(sid="strat.shared"), "Necrons", anchor_id="necron_anchor")
    common.spend_stratagem(_strat(sid="strat.shared"), "Orks", anchor_id="ork_anchor")
    assert common.stratagem_used_here("Necrons", "strat.shared", "necron_anchor") is True
    assert common.stratagem_used_here("Orks", "strat.shared", "necron_anchor") is False
    assert common.stratagem_used_here("Orks", "strat.shared", "ork_anchor") is True


def test_undo_stratagem_removes_recorded_anchor() -> None:
    session = _spend_session()
    common.spend_stratagem(_strat(sid="strat.a"), "Necrons", anchor_id="anchor_x")
    common.undo_stratagem(_strat(sid="strat.a"), "Necrons")
    assert "strat.a" not in session["stratagem_use_anchors"].get("Necrons", {})
    assert common.stratagem_use_anchor("Necrons", "strat.a") is None


def test_undo_stratagem_without_prior_anchor_is_a_noop() -> None:
    """undo_stratagem must tolerate a stratagem that was spent with no
    anchor_id (or never spent at all) — nothing to pop, no KeyError."""
    session = _spend_session()
    common.undo_stratagem(_strat(sid="strat.never_spent"), "Necrons")
    assert session["cp"]["Necrons"] == 6  # refunded once (cp_cost=1 default)


def test_used_elsewhere_unit_name_resolves_recorded_units_display_name(monkeypatch) -> None:
    """S141 B12b: the helper behind the "used on ⟨Einheit⟩" header suffix reads
    the unit_key spend_stratagem recorded and resolves it to the display name."""
    _spend_session()
    common.spend_stratagem(_strat(sid="strat.a"), "Necrons", "warrior#1", anchor_id="anchor_x")
    warriors = SimpleNamespace(name_en="Necron Warriors")
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (warriors, {}))
    assert common.stratagem_used_elsewhere_unit_name("Necrons", "strat.a") == "Necron Warriors"


def test_used_elsewhere_unit_name_none_when_never_spent() -> None:
    _spend_session()
    assert common.stratagem_used_elsewhere_unit_name("Necrons", "strat.never") is None


def test_used_elsewhere_unit_name_none_when_spent_without_unit_key() -> None:
    """A GO spent with no unit target (e.g. the inline Command Re-Roll) knows
    no unit — the spec shows the suffix only "falls eine Einheit bekannt"."""
    _spend_session()
    common.spend_stratagem(_strat(sid="strat.a"), "Necrons", anchor_id="anchor_x")
    assert common.stratagem_used_elsewhere_unit_name("Necrons", "strat.a") is None


def test_used_elsewhere_unit_name_none_when_recorded_key_unresolvable(monkeypatch) -> None:
    """A stale unit_key (catalog out of sync) must degrade to "no suffix",
    never crash the render path."""
    _spend_session()
    common.spend_stratagem(_strat(sid="strat.a"), "Necrons", "gone#1", anchor_id="anchor_x")

    def _raise(faction: str, uid: str):  # type: ignore[no-untyped-def]
        raise KeyError(uid)

    monkeypatch.setattr(common, "lookup", _raise)
    assert common.stratagem_used_elsewhere_unit_name("Necrons", "strat.a") is None


# ---------------------------------------------------------------------------
# S130 — spend_stratagem() effect dispatch: Insane Bravery / Desperate Breakout
# ---------------------------------------------------------------------------


def _effect_spend_session(unit_key: str = "unit#1") -> _SS:  # type: ignore[no-untyped-def]
    session = _SS(
        first_player="Necrons",
        cp={"Necrons": 5},
        used_stratagem_ids={},
        used_stratagem_battle_ids={},
        active_modifiers=[],
        phase_idx=1,  # "movement"
        round=2,
        p1_units={unit_key: {"turn_flags": {}}},
    )
    common.st.session_state = session
    _gs.st.session_state = session
    _se.st.session_state = session
    _um.st.session_state = session
    return session


def test_spend_stratagem_auto_pass_morale_activates_flag_for_unit() -> None:
    session = _effect_spend_session()
    strat = _strat(sid="strat.insane_bravery", effect=Effect(type="auto_pass_morale"))
    common.spend_stratagem(strat, "Necrons", "unit#1")
    assert session["p1_units"]["unit#1"]["turn_flags"]["morale_auto_pass"] is True


def test_spend_stratagem_auto_pass_morale_noop_without_unit_key() -> None:
    """No selected unit to target — CP is still spent, but no flag is set anywhere."""
    session = _effect_spend_session()
    strat = _strat(sid="strat.insane_bravery", effect=Effect(type="auto_pass_morale"))
    common.spend_stratagem(strat, "Necrons", None)
    assert session["cp"]["Necrons"] == 4
    assert session["p1_units"]["unit#1"]["turn_flags"] == {}


def test_spend_stratagem_desperate_breakout_activates_pending_flag_for_unit() -> None:
    session = _effect_spend_session()
    strat = _strat(
        sid="strat.desperate_breakout",
        effect=Effect(type="move", handler="fall_back_through_models"),
    )
    common.spend_stratagem(strat, "Necrons", "unit#1")
    assert session["p1_units"]["unit#1"]["turn_flags"]["desperate_breakout_pending"] is True


def test_spend_stratagem_unrelated_effect_type_is_noop() -> None:
    """Regression: an effect type outside the dispatch table touches no turn_flags."""
    session = _effect_spend_session()
    strat = _strat(sid="strat.other", effect=Effect(type="heal"))
    common.spend_stratagem(strat, "Necrons", "unit#1")
    assert session["p1_units"]["unit#1"]["turn_flags"] == {}


# ---------------------------------------------------------------------------
# Plan 015 — _maybe_flag_transport_destroyed()
# ---------------------------------------------------------------------------


def test_flags_transport_destroyed_when_newly_destroyed() -> None:
    unit = SimpleNamespace(keywords=["TRANSPORT", "VEHICLE"])
    unit.has_keyword = lambda kw: kw in unit.keywords
    session = _SS(p1_units={"tank#1": {"destroyed": True}}, first_player="Necrons")
    common.st.session_state = session
    _gs.st.session_state = session
    monkeypatch_units = common.units_list_for
    common.units_list_for = lambda faction: [SimpleNamespace(id="tank")]
    try:
        common._maybe_flag_transport_destroyed(
            "Necrons", "tank#1", unit, was_destroyed_before=False
        )
    finally:
        common.units_list_for = monkeypatch_units
    assert session["pending_transport_destroyed"] == {"faction": "Necrons", "uid": "tank#1"}


def test_does_not_flag_when_already_destroyed_before() -> None:
    unit = SimpleNamespace(keywords=["TRANSPORT"])
    unit.has_keyword = lambda kw: kw in unit.keywords
    session = _SS(p1_units={"tank#1": {"destroyed": True}}, first_player="Necrons")
    common.st.session_state = session
    _gs.st.session_state = session
    monkeypatch_units = common.units_list_for
    common.units_list_for = lambda faction: [SimpleNamespace(id="tank")]
    try:
        common._maybe_flag_transport_destroyed("Necrons", "tank#1", unit, was_destroyed_before=True)
    finally:
        common.units_list_for = monkeypatch_units
    assert "pending_transport_destroyed" not in session


def test_does_not_flag_non_transport_unit() -> None:
    unit = SimpleNamespace(keywords=["INFANTRY"])
    unit.has_keyword = lambda kw: kw in unit.keywords
    session = _SS(p1_units={"warrior#1": {"destroyed": True}}, first_player="Necrons")
    common.st.session_state = session
    _gs.st.session_state = session
    monkeypatch_units = common.units_list_for
    common.units_list_for = lambda faction: [SimpleNamespace(id="warrior")]
    try:
        common._maybe_flag_transport_destroyed(
            "Necrons", "warrior#1", unit, was_destroyed_before=False
        )
    finally:
        common.units_list_for = monkeypatch_units
    assert "pending_transport_destroyed" not in session


# ---------------------------------------------------------------------------
# Plan 015 — render_reactive_stratagem_box(): real Fire Overwatch data end-to-end
# ---------------------------------------------------------------------------


def _reactive_box_session(**extra) -> _SS:  # type: ignore[no-untyped-def]
    base = dict(
        first_player="Necrons",
        second_player="Orks",
        active="Orks",  # Necrons is the inactive/defending column
        p1_faction_dir="necrons",
        p2_faction_dir="necrons",
        cp={"Necrons": 5},
        used_stratagem_ids={},
        used_stratagem_battle_ids={},
        active_modifiers=[],
    )
    base.update(extra)
    return _SS(**base)


def _install_reactive_box_session(monkeypatch, session):  # type: ignore[no-untyped-def]
    """Point common/gameState/unitMutations at the SAME session_state (see
    module docstring on why all three must share one object) and spy on
    `render_go_card` — the same pattern test_game_protocoll.py uses for the
    central Stratagems list (S133 Task 6: the reactive box now builds on the
    identical GO-card infrastructure, so its own Streamlit wiring — button/
    container/accordion — is manually-verified render code, not re-mocked
    widget-by-widget per call site).
    """
    monkeypatch.setattr(common.st, "session_state", session)
    monkeypatch.setattr(_gs.st, "session_state", session)
    monkeypatch.setattr(_um.st, "session_state", session)
    captured: list[dict] = []  # type: ignore[type-arg]
    monkeypatch.setattr(common, "render_go_card", lambda **kwargs: captured.append(kwargs))
    return captured


def _overwatch_unit(name_en: str = "Necron Warriors"):  # type: ignore[no-untyped-def]
    """Mirrors the reacting unit `_inactive_charge` passes as unit_for_conditions:
    Fire Overwatch's `weapon_conditions: [RANGED]` gate (S148 Brief 3) needs at
    least one ranged weapon on the charge target's own weapon list."""
    gun = Weapon(
        id="test.ranged_weapon",
        name_en="Test Gun",
        profiles=[
            WeaponProfile(
                weapon_type="Rapid Fire",
                range_inches=24,
                attacks="1",
                strength=4,
                ap=0,
                damage="1",
                is_melee=False,
            )
        ],
    )
    return SimpleNamespace(has_keyword=lambda kw: False, name_en=name_en, weapons=[gun])


def test_fire_overwatch_box_shown_when_window_open_for_defender(monkeypatch) -> None:
    """Real shared-data end-to-end check: Fire Overwatch (player=inactive) surfaces
    in the target's own column while the Charge reactive window is open."""
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-1",
        context_caption="Warriors were declared a charge target.",
        unit_for_conditions=_overwatch_unit(),
    )

    assert any(c["name"] == "Fire Overwatch" for c in captured)


def test_fire_overwatch_box_hidden_for_active_player_column(monkeypatch) -> None:
    """player=inactive: the charging (active) player's own column must not see it.

    Other (phase="charge", event="on_declaration") reactive stratagems this
    faction DOES hold as the active player (e.g. Necrons' own Efficient
    Disintegration) legitimately still render here — only Fire Overwatch
    itself must be absent.
    """
    session = _reactive_box_session(active="Necrons")  # Necrons is now the charger
    captured = _install_reactive_box_session(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-1",
        context_caption="irrelevant",
        unit_for_conditions=_overwatch_unit(),
    )

    assert all(c["name"] != "Fire Overwatch" for c in captured)


def test_use_action_spends_cp_and_marks_used(monkeypatch) -> None:
    """The GO card's on_use callback routes through the canonical spend_stratagem
    path — same CP/usage bookkeeping the central list and inline offer share."""
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-1",
        context_caption="irrelevant",
        unit_for_conditions=_overwatch_unit(),
    )
    captured[0]["on_use"]()

    assert session["cp"]["Necrons"] == 4  # 5 - 1 CP
    assert "wh40k_9e.shared.stratagem.fire_overwatch" in session["used_stratagem_ids"]["Necrons"]


def test_used_at_this_anchor_offers_undo_within_window(monkeypatch) -> None:
    """S134 task 2b + S139 B12b: while this phase's activation window is still
    open (`stratagem_undo_visible`) AND the spend was recorded at THIS box's own
    anchor (`reactive:{event}:{decline_key}`), the reactive GO renders "used"
    with the full-rollback Undo wired — pressing it restores CP and clears the
    usage marker, the same canonical `undo_stratagem` path the central list
    uses. The CP-safety guarantee the old "locked" mapping protected still
    holds: in the "used" state the one action slot is Undo, not Use, so the
    stratagem can never be spent twice in one phase."""
    fo = "wh40k_9e.shared.stratagem.fire_overwatch"
    session = _reactive_box_session(
        cp={"Necrons": 4},
        used_stratagem_ids={"Necrons": {fo}},
        # Spend recorded at this exact box's anchor → used_here.
        stratagem_use_anchors={
            "Necrons": {fo: {"anchor_id": "reactive:on_declaration:target-uid-2", "unit_key": None}}
        },
    )
    captured = _install_reactive_box_session(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-2",
        context_caption="irrelevant",
        unit_for_conditions=_overwatch_unit(),
    )

    assert captured[0]["state"] == "used"
    assert captured[0]["locked_reason"] is None

    captured[0]["on_undo"]()

    assert session["cp"]["Necrons"] == 5
    assert fo not in session["used_stratagem_ids"]["Necrons"]


def test_used_at_other_anchor_maps_to_used_elsewhere(monkeypatch) -> None:
    """S139 B12b: the same GO spent this phase, window still open, but recorded
    at a DIFFERENT anchor (a different charge target) — this box shows
    "used_elsewhere": a disabled "Used" with no Undo, since undoing only makes
    sense at the target that actually triggered the spend."""
    fo = "wh40k_9e.shared.stratagem.fire_overwatch"
    session = _reactive_box_session(
        cp={"Necrons": 4},
        used_stratagem_ids={"Necrons": {fo}},
        stratagem_use_anchors={
            "Necrons": {fo: {"anchor_id": "reactive:on_declaration:target-uid-1", "unit_key": None}}
        },
    )
    captured = _install_reactive_box_session(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-2",  # a DIFFERENT target than the recorded anchor
        context_caption="irrelevant",
        unit_for_conditions=_overwatch_unit(),
    )

    assert captured[0]["state"] == "used_elsewhere"
    assert captured[0]["locked_reason"] is None


def test_used_at_other_anchor_hands_unit_name_to_card_as_reason(monkeypatch) -> None:
    """S141 B12b wiring: when the spend at the OTHER anchor recorded a unit_key,
    the reactive box resolves it (stratagem_used_elsewhere_unit_name) and hands
    the display name to render_go_card as locked_reason — the card then renders
    the §6.1 header suffix "used on ⟨Einheit⟩"."""
    fo = "wh40k_9e.shared.stratagem.fire_overwatch"
    session = _reactive_box_session(
        cp={"Necrons": 4},
        used_stratagem_ids={"Necrons": {fo}},
        stratagem_use_anchors={
            "Necrons": {
                fo: {"anchor_id": "reactive:on_declaration:target-uid-1", "unit_key": "warrior#1"}
            }
        },
    )
    captured = _install_reactive_box_session(monkeypatch, session)
    warriors = SimpleNamespace(name_en="Necron Warriors")
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (warriors, {}))

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-2",  # a DIFFERENT target than the recorded anchor
        context_caption="irrelevant",
        unit_for_conditions=_overwatch_unit(),
    )

    assert captured[0]["state"] == "used_elsewhere"
    assert captured[0]["locked_reason"] == "Necron Warriors"


def test_use_records_this_boxs_anchor_for_the_here_split(monkeypatch) -> None:
    """S139 B12b wiring: the reactive box's Use routes through spend_stratagem
    with anchor_id = `reactive:{event}:{decline_key}`, so a later render of the
    SAME box sees "used here" while any other anchor sees "used_elsewhere"."""
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-7",
        context_caption="irrelevant",
        unit_for_conditions=_overwatch_unit(),
    )
    captured[0]["on_use"]()

    fo = "wh40k_9e.shared.stratagem.fire_overwatch"
    assert session["stratagem_use_anchors"]["Necrons"][fo]["anchor_id"] == (
        "reactive:on_declaration:target-uid-7"
    )


def test_one_players_use_does_not_block_the_opponents_same_go(monkeypatch) -> None:
    """S138 F1 testpflicht / concept §F1: player A using a reactive GO must NOT
    block player B from the same GO in the same phase. The anchor bookkeeping is
    scoped per (faction, GO id), so B's box stays "ready" while A's shows
    "used" — the regression the stakeholder explicitly demanded be guarded."""
    fo = "wh40k_9e.shared.stratagem.fire_overwatch"
    # A (Necrons) already spent Fire Overwatch this phase at its own anchor; B
    # (Orks) has spent nothing. Both are the inactive/defending player in their
    # own render (active is a third value here so neither is the charger).
    session = _reactive_box_session(
        active="Tau",
        cp={"Necrons": 4, "Orks": 4},
        used_stratagem_ids={"Necrons": {fo}},
        stratagem_use_anchors={
            "Necrons": {fo: {"anchor_id": "reactive:on_declaration:t1", "unit_key": None}}
        },
    )
    captured = _install_reactive_box_session(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="t1",
        context_caption="x",
        unit_for_conditions=_overwatch_unit(),
    )
    common.render_reactive_stratagem_box(
        "Orks",
        phase="charge",
        event="on_declaration",
        decline_key="t1",
        context_caption="x",
        unit_for_conditions=_overwatch_unit(name_en="Boyz"),
    )

    by_key = {c["key"]: c for c in captured}
    necron_card = by_key[f"reactive_Necrons_on_declaration_{fo}_t1"]
    ork_card = by_key[f"reactive_Orks_on_declaration_{fo}_t1"]
    assert necron_card["state"] == "used"
    assert ork_card["state"] == "ready"


def test_cp_insufficient_shows_locked_card_with_cp_reason(monkeypatch) -> None:
    session = _reactive_box_session(cp={"Necrons": 0})
    captured = _install_reactive_box_session(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-1",
        context_caption="irrelevant",
        unit_for_conditions=_overwatch_unit(),
    )

    assert captured[0]["state"] == "locked"
    assert captured[0]["locked_reason"] == "CP insufficient"


def test_use_action_invokes_on_spent_and_on_resolved(monkeypatch) -> None:
    """The two hooks the removed Pass button used to also trigger on decline
    now fire on Use only (render_reactive_stratagem_box docstring) — Use is
    the only action left that can close the caller's pending-window marker."""
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    spent_calls: list[str] = []
    resolved_calls: list[int] = []

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-1",
        context_caption="irrelevant",
        unit_for_conditions=_overwatch_unit(),
        on_spent=lambda strat: spent_calls.append(strat.id),
        on_resolved=lambda: resolved_calls.append(1),
    )
    captured[0]["on_use"]()

    assert spent_calls == ["wh40k_9e.shared.stratagem.fire_overwatch"]
    assert resolved_calls == [1]


# ---------------------------------------------------------------------------
# S135 Paket 4a — Hit-/Wound-Anker: render_reactive_stratagem_box's new
# effect_type/effect_stat filter and unit_for_conditions keyword gate, real
# Necrons data (Shadows of Drazak = hit debuff, Whirling Onslaught = wound
# debuff — both event="on_target", phase="any", so both would otherwise share
# one window; the effect_stat filter is what routes each to its own anchor).
# ---------------------------------------------------------------------------


def _unit_with_keywords(*keywords: str, name_en: str = "Test Unit"):  # type: ignore[no-untyped-def]
    return SimpleNamespace(has_keyword=lambda kw: kw in keywords, name_en=name_en)


def test_shadows_of_drazak_shown_at_hit_anchor_for_matching_unit(monkeypatch) -> None:
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    flayed_ones = _unit_with_keywords("FLAYED ONES", name_en="Flayed Ones")

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="shooting",
        event="on_target",
        decline_key="tab-1",
        context_caption="irrelevant",
        unit_for_conditions=flayed_ones,
        effect_type="debuff_roll",
        effect_stat="hit",
    )

    assert any(c["name"] == "Shadows of Drazak" for c in captured)


def test_shadows_of_drazak_absent_at_wound_anchor(monkeypatch) -> None:
    """The effect_stat filter keeps a hit-debuff GO off the wound anchor even
    though both share the same (phase, event) window."""
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    flayed_ones = _unit_with_keywords("FLAYED ONES", name_en="Flayed Ones")

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="shooting",
        event="on_target",
        decline_key="tab-1",
        context_caption="irrelevant",
        unit_for_conditions=flayed_ones,
        effect_type="debuff_roll",
        effect_stat="wound",
    )

    assert all(c["name"] != "Shadows of Drazak" for c in captured)


def test_shadows_of_drazak_hidden_without_matching_keyword_unit(monkeypatch) -> None:
    """Keyword gate (S135 Paket 4a): a Necrons unit without FLAYED ONES must not
    see this card — unlike the pre-existing callers, this GO carries a real
    `conditions` list, so the keyword check now actually matters."""
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    warriors = _unit_with_keywords("NECRONS", "INFANTRY")

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="shooting",
        event="on_target",
        decline_key="tab-1",
        context_caption="irrelevant",
        unit_for_conditions=warriors,
        effect_type="debuff_roll",
        effect_stat="hit",
    )

    assert all(c["name"] != "Shadows of Drazak" for c in captured)


def test_shadows_of_drazak_hidden_without_any_unit_passed(monkeypatch) -> None:
    """Fail-safe default: omitting unit_for_conditions hides a keyword-gated
    reactive GO rather than showing it for every unit."""
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="shooting",
        event="on_target",
        decline_key="tab-1",
        context_caption="irrelevant",
        effect_type="debuff_roll",
        effect_stat="hit",
    )

    assert all(c["name"] != "Shadows of Drazak" for c in captured)


# test_whirling_onslaught_shown_at_wound_anchor_for_matching_unit wurde in S146
# (Fix 2) entfernt: der Wound-Anker-Aufruf existiert nicht mehr, on_target-GOs
# rendern nur noch am Deklarations-Anker (test_declaration_anchor_* unten).


def test_whirling_onslaught_absent_at_hit_anchor(monkeypatch) -> None:
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    destroyer = _unit_with_keywords("DESTROYER CULT", name_en="Destroyers")

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="shooting",
        event="on_target",
        decline_key="tab-1",
        context_caption="irrelevant",
        unit_for_conditions=destroyer,
        effect_type="debuff_roll",
        effect_stat="hit",
    )

    assert all(c["name"] != "Whirling Onslaught" for c in captured)


def test_shadows_of_drazak_use_registers_defender_scoped_hit_modifier(monkeypatch) -> None:
    """End-to-end (data fix, S135 Paket 4a): Shadows of Drazak was missing its
    `modifier:` YAML block, so Use spent CP but never actually debuffed anything.
    After the fix, Use must register a target="defender" hit modifier scoped to
    the targeted unit's key — exactly what _collect_atk_modifiers's def_uid
    scoping (above) then reads back out."""
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    flayed_ones = _unit_with_keywords("FLAYED ONES", name_en="Flayed Ones")

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="shooting",
        event="on_target",
        decline_key="tab-1",
        context_caption="irrelevant",
        unit_key_for_modifier="wh40k_9e.necrons.unit.flayed_ones",
        unit_for_conditions=flayed_ones,
        effect_type="debuff_roll",
        effect_stat="hit",
    )
    captured[0]["on_use"]()

    mods = session["active_modifiers"]
    assert len(mods) == 1
    assert mods[0]["unit_key"] == "wh40k_9e.necrons.unit.flayed_ones"
    assert mods[0]["effect"]["roll_type"] == "hit"
    assert mods[0]["effect"]["value"] == -1
    assert mods[0]["effect"]["target"] == "defender"


# ---------------------------------------------------------------------------
# S135 Paket 4b — Save-Anker: render_reactive_stratagem_box's effect_type
# filter for the invuln-save complex, real Necrons data (Quantum Deflection,
# event="on_target", phase="any" — the same window the Hit-/Wound-Anker
# above use, routed to its own anchor via effect_type="invuln_save"). Tough
# as Squig-Hide (Orks, effect_type="restriction") deliberately shares no
# filter value with this anchor — see the _render_damage_block-adjacent
# comment in _common.py for why its YAML `modifier:` block is not treated as
# a real hit/wound bonus here.
# ---------------------------------------------------------------------------


def test_quantum_deflection_shown_at_save_anchor_for_matching_unit(monkeypatch) -> None:
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    shielded = _unit_with_keywords("QUANTUM SHIELDING", name_en="Canoptek Wraiths")

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="shooting",
        event="on_target",
        decline_key="tab-1",
        context_caption="irrelevant",
        unit_for_conditions=shielded,
        effect_type="invuln_save",
    )

    assert any(c["name"] == "Quantum Deflection" for c in captured)


def test_quantum_deflection_hidden_without_matching_keyword_unit(monkeypatch) -> None:
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    warriors = _unit_with_keywords("NECRONS", "INFANTRY")

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="shooting",
        event="on_target",
        decline_key="tab-1",
        context_caption="irrelevant",
        unit_for_conditions=warriors,
        effect_type="invuln_save",
    )

    assert all(c["name"] != "Quantum Deflection" for c in captured)


def test_quantum_deflection_absent_at_hit_anchor(monkeypatch) -> None:
    """The effect_type filter keeps the invuln-save GO off the debuff_roll anchors."""
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    shielded = _unit_with_keywords("QUANTUM SHIELDING", name_en="Canoptek Wraiths")

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="shooting",
        event="on_target",
        decline_key="tab-1",
        context_caption="irrelevant",
        unit_for_conditions=shielded,
        effect_type="debuff_roll",
        effect_stat="hit",
    )

    assert all(c["name"] != "Quantum Deflection" for c in captured)


def test_quantum_deflection_use_registers_defender_scoped_invuln_modifier(monkeypatch) -> None:
    """End-to-end: Use must register a target="defender" invuln_save modifier
    scoped to the targeted unit's key — exactly what _stratagem_invuln_save
    (below) then reads back out for the Save block's effective-invuln calc."""
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    shielded = _unit_with_keywords("QUANTUM SHIELDING", name_en="Canoptek Wraiths")

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="shooting",
        event="on_target",
        decline_key="tab-1",
        context_caption="irrelevant",
        unit_key_for_modifier="wh40k_9e.necrons.unit.warriors",
        unit_for_conditions=shielded,
        effect_type="invuln_save",
    )
    captured[0]["on_use"]()

    mods = session["active_modifiers"]
    assert len(mods) == 1
    assert mods[0]["unit_key"] == "wh40k_9e.necrons.unit.warriors"
    assert mods[0]["effect"]["roll_type"] == "invuln_save"
    assert mods[0]["effect"]["value"] == 4
    assert mods[0]["effect"]["target"] == "defender"


# ---------------------------------------------------------------------------
# S135 Paket 4b — spend_stratagem() effect dispatch: invuln_save
# (Quantum Deflection's own _apply_stratagem_effect branch, isolated from the
# real-data GO-card tests above)
# ---------------------------------------------------------------------------


def test_spend_stratagem_invuln_save_registers_active_modifier_for_unit() -> None:
    session = _effect_spend_session()
    strat = _strat(sid="strat.quantum_deflection", effect=Effect(type="invuln_save", modifier=4))
    common.spend_stratagem(strat, "Necrons", "unit#1")
    mods = session["active_modifiers"]
    assert len(mods) == 1
    assert mods[0]["unit_key"] == "unit#1"
    assert mods[0]["source"] == "Test GO"
    assert mods[0]["effect"]["roll_type"] == "invuln_save"
    assert mods[0]["effect"]["value"] == 4
    assert mods[0]["effect"]["target"] == "defender"


def test_spend_stratagem_invuln_save_without_modifier_value_is_noop() -> None:
    """Regression: a malformed invuln_save effect (no modifier value) must not
    crash or register a meaningless active_modifiers entry."""
    session = _effect_spend_session()
    strat = _strat(sid="strat.x", effect=Effect(type="invuln_save"))
    common.spend_stratagem(strat, "Necrons", "unit#1")
    assert session["active_modifiers"] == []


# ---------------------------------------------------------------------------
# S135 Paket 4b — _stratagem_invuln_save(): read-back side for the Save block
# (mirrors abilityEngine.ability_invuln_save's "lowest value wins" semantics
# but reads active_modifiers instead of activated faction abilities)
# ---------------------------------------------------------------------------


def test_stratagem_invuln_save_returns_lowest_value_for_matching_unit() -> None:
    session = _SS(
        active_modifiers=[
            {"unit_key": "u1", "effect": {"roll_type": "invuln_save", "value": 5}},
            {"unit_key": "u1", "effect": {"roll_type": "invuln_save", "value": 4}},
            {"unit_key": "u2", "effect": {"roll_type": "invuln_save", "value": 2}},
            {"unit_key": "u1", "effect": {"roll_type": "save", "value": 1}},
        ]
    )
    common.st.session_state = session
    assert common._stratagem_invuln_save("u1") == 4


def test_stratagem_invuln_save_none_when_no_active_modifiers() -> None:
    session = _SS(active_modifiers=[])
    common.st.session_state = session
    assert common._stratagem_invuln_save("u1") is None


def test_stratagem_invuln_save_ignores_other_units_and_roll_types() -> None:
    session = _SS(
        active_modifiers=[
            {"unit_key": "u2", "effect": {"roll_type": "invuln_save", "value": 4}},
            {"unit_key": "u1", "effect": {"roll_type": "hit", "value": -1}},
        ]
    )
    common.st.session_state = session
    assert common._stratagem_invuln_save("u1") is None


# ---------------------------------------------------------------------------
# Plan 015 — _render_pending_emergency_disembarkation() + render_player_column wiring
# ---------------------------------------------------------------------------


def test_no_pending_transport_destroyed_renders_nothing(monkeypatch) -> None:
    session = _SS(pending_transport_destroyed=None)
    common.st.session_state = session
    spy = MagicMock()
    monkeypatch.setattr(common, "render_reactive_stratagem_box", spy)

    common._render_pending_emergency_disembarkation("Necrons")

    spy.assert_not_called()


def test_pending_transport_destroyed_for_other_faction_renders_nothing(monkeypatch) -> None:
    """Ownership gate: only the TRANSPORT's own faction sees the box."""
    session = _SS(pending_transport_destroyed={"faction": "Orks", "uid": "trukk#1"})
    common.st.session_state = session
    spy = MagicMock()
    monkeypatch.setattr(common, "render_reactive_stratagem_box", spy)

    common._render_pending_emergency_disembarkation("Necrons")

    spy.assert_not_called()


def test_pending_transport_destroyed_for_own_faction_renders_box(monkeypatch) -> None:
    session = _SS(
        pending_transport_destroyed={"faction": "Necrons", "uid": "ghost_ark#1"},
        phase_idx=4,  # "shooting"
    )
    common.st.session_state = session
    ghost_ark = SimpleNamespace(name_en="Ghost Ark")
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (ghost_ark, {}))
    spy = MagicMock()
    monkeypatch.setattr(common, "render_reactive_stratagem_box", spy)

    common._render_pending_emergency_disembarkation("Necrons")

    spy.assert_called_once()
    call = spy.call_args
    assert call.args[0] == "Necrons"
    assert call.kwargs["event"] == "on_destroy"
    assert call.kwargs["decline_key"] == "ghost_ark#1"
    assert "Ghost Ark" in call.kwargs["context_caption"]


def test_pending_transport_destroyed_box_visible_through_real_conditions_gate(
    monkeypatch,
) -> None:
    """Regression (S141 Group B): render_reactive_stratagem_box was called
    without unit_for_conditions, so stratagem_conditions_met(["TRANSPORT"], None)
    was always False and stratagem_visibility() returned "hidden" before any
    phase/CP check ran — Emergency Disembarkation never appeared, even for a
    genuinely destroyed TRANSPORT. This exercises the real (unmocked)
    render_reactive_stratagem_box -> stratagem_visibility path instead of
    spying it away, so the missing unit_for_conditions wiring is caught."""
    session = _reactive_box_session(
        pending_transport_destroyed={"faction": "Necrons", "uid": "ghost_ark#1"},
        phase_idx=4,  # "shooting"
    )
    captured = _install_reactive_box_session(monkeypatch, session)
    ghost_ark = _unit_with_keywords("TRANSPORT")
    ghost_ark.name_en = "Ghost Ark"
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (ghost_ark, {}))

    common._render_pending_emergency_disembarkation("Necrons")

    assert any(c["name"] == "Emergency Disembarkation" for c in captured)


def test_render_player_column_calls_emergency_disembarkation_check(monkeypatch) -> None:
    """Wiring check: render_player_column must consult the pending marker for
    EVERY faction column, regardless of active/inactive role (charge, movement,
    and shooting phases all share this one render function)."""
    session = _SS(
        active="Orks",
        selected_unit=None,
        selected_targets=[],
        pending_transport_destroyed=None,
    )
    common.st.session_state = session
    spy = MagicMock()
    monkeypatch.setattr(common, "_render_pending_emergency_disembarkation", spy)

    common.render_player_column("Necrons", {"active": "Orks"}, active_content=lambda *a: None)

    spy.assert_called_once_with("Necrons")


# ---------------------------------------------------------------------------
# S130 — render_inline_command_reroll(): non-blocking Command Re-Roll offer
# (Option c — Pull, not Push): while CP is short, the offer stays fully
# absent — not merely disabled — same as before. Once spent this phase,
# though, it now stays visible (S139 B12c, S138-revised concept: the old
# "gar kein Undo" rule for inline offers was revised): the anchor
# (phase, reopen_key) that actually triggered the spend shows "↺ Undo <name>",
# every OTHER anchor of the same (player, GO) this phase shows a disabled
# "<name> — Used" — the same used/used_elsewhere split the card mappers use,
# via `_inline_reroll_state`. Real _shared stratagem data (command_re_roll,
# event=after_roll) end-to-end via _reactive_box_session.
# ---------------------------------------------------------------------------

_COMMAND_REROLL_ID = "wh40k_9e.shared.stratagem.command_re_roll"


def _reroll_widgets(monkeypatch, session, clicked_key: str | None = None):  # type: ignore[no-untyped-def]
    button_calls: list[tuple] = []  # type: ignore[type-arg]
    rerun_calls: list[int] = []
    monkeypatch.setattr(common.st, "session_state", session)
    monkeypatch.setattr(_gs.st, "session_state", session)
    monkeypatch.setattr(_um.st, "session_state", session)

    def _button(label, key=None, **kw):  # type: ignore[no-untyped-def]
        button_calls.append((label, key))
        return key == clicked_key

    monkeypatch.setattr(common.st, "button", _button)
    monkeypatch.setattr(common.st, "rerun", lambda: rerun_calls.append(1))
    return button_calls, rerun_calls


def test_command_reroll_visible_and_clickable_spends_cp(monkeypatch) -> None:
    session = _reactive_box_session()
    key = f"cmd_reroll_Necrons_charge_{_COMMAND_REROLL_ID}_t1"
    button_calls, rerun_calls = _reroll_widgets(monkeypatch, session, clicked_key=key)
    reopened = []

    common.render_inline_command_reroll(
        "Necrons", "charge", reopen_key="t1", on_reroll=lambda: reopened.append(1)
    )

    assert any("Command Re-Roll" in label for label, _ in button_calls)
    assert session["cp"]["Necrons"] == 4  # 5 - 1 CP
    assert _COMMAND_REROLL_ID in session["used_stratagem_ids"]["Necrons"]
    # S139 B12c: Use records THIS render spot's own anchor, so a later render
    # at reopen_key="t1" (this same spot) can tell "used here" from another
    # reopen_key's "used elsewhere".
    assert session["stratagem_use_anchors"]["Necrons"][_COMMAND_REROLL_ID] == {
        "anchor_id": "inline:charge:t1",
        "unit_key": None,
    }
    assert reopened == [1]
    assert rerun_calls == [1]


def test_command_reroll_label_context_appended_to_button_label(monkeypatch) -> None:
    """S136 4c-a Option B: with several nearby offers, each button names its roll."""
    session = _reactive_box_session()
    button_calls, _ = _reroll_widgets(monkeypatch, session)

    common.render_inline_command_reroll(
        "Necrons", "charge", reopen_key="t1", on_reroll=lambda: None, label_context="Choppa"
    )

    assert any(label.endswith(" — Choppa") for label, _ in button_calls)


def test_command_reroll_hidden_when_cp_zero(monkeypatch) -> None:
    session = _reactive_box_session(cp={"Necrons": 0})
    button_calls, _ = _reroll_widgets(monkeypatch, session)

    common.render_inline_command_reroll(
        "Necrons", "charge", reopen_key="t1", on_reroll=lambda: None
    )

    assert button_calls == []


def test_command_reroll_used_here_offers_undo_and_rolls_back(monkeypatch) -> None:
    """S139 B12c: spent AT this exact anchor (phase="charge", reopen_key="t1")
    → the button switches to "↺ Undo <name>" instead of vanishing; pressing it
    routes through the canonical undo_stratagem rollback (CP + usage restored),
    same as the card anchors."""
    session = _reactive_box_session(
        cp={"Necrons": 4},
        used_stratagem_ids={"Necrons": {_COMMAND_REROLL_ID}},
        stratagem_use_anchors={
            "Necrons": {_COMMAND_REROLL_ID: {"anchor_id": "inline:charge:t1", "unit_key": None}}
        },
    )
    key = f"cmd_reroll_Necrons_charge_{_COMMAND_REROLL_ID}_t1"
    button_calls, rerun_calls = _reroll_widgets(monkeypatch, session, clicked_key=key)

    common.render_inline_command_reroll(
        "Necrons", "charge", reopen_key="t1", on_reroll=lambda: None
    )

    assert any("Undo" in label and "Command Re-Roll" in label for label, _ in button_calls)
    assert session["cp"]["Necrons"] == 5  # restored
    assert _COMMAND_REROLL_ID not in session["used_stratagem_ids"]["Necrons"]
    assert rerun_calls == [1]


def test_command_reroll_undo_clears_anchor_so_next_render_is_ready_again(monkeypatch) -> None:
    """After Undo, a fresh render of the SAME anchor must fall back to "ready"
    (a plain, clickable offer) — not get stuck in any used state."""
    session = _reactive_box_session(
        cp={"Necrons": 4},
        used_stratagem_ids={"Necrons": {_COMMAND_REROLL_ID}},
        stratagem_use_anchors={
            "Necrons": {_COMMAND_REROLL_ID: {"anchor_id": "inline:charge:t1", "unit_key": None}}
        },
    )
    button_calls, _ = _reroll_widgets(monkeypatch, session)
    common.undo_stratagem(_strat(sid=_COMMAND_REROLL_ID, cp_cost=1), "Necrons")

    common.render_inline_command_reroll(
        "Necrons", "charge", reopen_key="t1", on_reroll=lambda: None
    )

    assert any(
        "Command Re-Roll" in label and "Undo" not in label and "Used" not in label
        for label, _ in button_calls
    )


def test_command_reroll_used_elsewhere_shows_disabled_used(monkeypatch) -> None:
    """S139 B12c: the SAME GO spent this phase at a DIFFERENT inline anchor
    (e.g. the Hit-roll offer) — THIS anchor (e.g. the Wound-roll offer) shows
    a disabled "<name> — Used", no Undo. Even if the (disabled) widget somehow
    reports a click, nothing must be spent/undone — the used_elsewhere branch
    never calls spend_stratagem or undo_stratagem."""
    session = _reactive_box_session(
        cp={"Necrons": 4},
        used_stratagem_ids={"Necrons": {_COMMAND_REROLL_ID}},
        stratagem_use_anchors={
            "Necrons": {_COMMAND_REROLL_ID: {"anchor_id": "inline:charge:hit_t1", "unit_key": None}}
        },
    )
    key = f"cmd_reroll_Necrons_charge_{_COMMAND_REROLL_ID}_wound_t1"
    button_calls, rerun_calls = _reroll_widgets(monkeypatch, session, clicked_key=key)

    common.render_inline_command_reroll(
        "Necrons", "charge", reopen_key="wound_t1", on_reroll=lambda: None
    )

    assert any(
        "Command Re-Roll" in label and "Used" in label and "Undo" not in label
        for label, _ in button_calls
    )
    assert session["cp"]["Necrons"] == 4  # untouched
    assert _COMMAND_REROLL_ID in session["used_stratagem_ids"]["Necrons"]  # still used
    assert rerun_calls == []  # no spend/undo path taken


def test_command_reroll_cross_player_use_does_not_block_opponent(monkeypatch) -> None:
    """S138-Testpflicht (F1): Player A spending Command Re-Roll at their own
    inline anchor must not block Player B's independent use of the SAME GO —
    both sides pay their own CP, `player: both` in the shared stratagem data."""
    session = _reactive_box_session(
        cp={"Necrons": 4, "Orks": 5},
        used_stratagem_ids={"Necrons": {_COMMAND_REROLL_ID}},
        stratagem_use_anchors={
            "Necrons": {_COMMAND_REROLL_ID: {"anchor_id": "inline:charge:t1", "unit_key": None}}
        },
    )
    button_calls, _ = _reroll_widgets(monkeypatch, session)

    common.render_inline_command_reroll("Orks", "charge", reopen_key="t1", on_reroll=lambda: None)

    # Orks see a plain, clickable "ready" offer — not "Used", not hidden.
    assert any(
        "Command Re-Roll" in label and "Undo" not in label and "Used" not in label
        for label, _ in button_calls
    )


def test_command_reroll_hidden_in_phase_without_after_roll_stratagem(monkeypatch) -> None:
    """ "morale" is not in command_re_roll's phase list — no roll happens there."""
    session = _reactive_box_session()
    button_calls, _ = _reroll_widgets(monkeypatch, session)

    common.render_inline_command_reroll(
        "Necrons", "morale", reopen_key="t1", on_reroll=lambda: None
    )

    assert button_calls == []


def test_command_reroll_not_clicked_leaves_cp_and_usage_untouched(monkeypatch) -> None:
    """Ignoring the offer (not clicking it) must cost nothing — Pull, not Push."""
    session = _reactive_box_session()
    button_calls, rerun_calls = _reroll_widgets(monkeypatch, session, clicked_key=None)
    reopened = []

    common.render_inline_command_reroll(
        "Necrons", "charge", reopen_key="t1", on_reroll=lambda: reopened.append(1)
    )

    assert session["cp"]["Necrons"] == 5
    assert session["used_stratagem_ids"] == {}
    assert reopened == []
    assert rerun_calls == []


# ---------------------------------------------------------------------------
# S135 Paket 4c — render_group_assignment(): Anzahl-Attacken-Anker. Command
# Re-Roll's own rule text names "the dice to determine the number of attacks
# made by a weapon" as one of R-CMD-12's 9 reactive windows — this wires the
# melee "<Weapon> — Attacks" field (decl_a_*), the only place in this app
# where a possibly dice-based Attacks characteristic is typed in as a number.
# Like Advance/Charge, the field has no "applied" lock to reopen (it stays
# directly editable until "Group done"), so on_reroll is a no-op — the call
# only owns the CP/usage bookkeeping (attacker pays, it is the attacker's
# own dice).
# ---------------------------------------------------------------------------


def _melee_group_fixture():  # type: ignore[no-untyped-def]
    profile = WeaponProfile(
        weapon_type="Melee",
        range_inches=0,
        attacks="D6",
        strength=4,
        ap=0,
        damage="1",
        is_melee=True,
    )
    weapon = Weapon(id="w1", name_en="Choppa", profiles=[profile])
    group = ModelGroup(id="g1", name_en="Boyz", count=5, weapons=[weapon], priority=1)
    unit = Unit(
        id="test.unit.boyz",
        name_en="Boyz",
        name_de="Boyz",
        faction="Orks",
        subfaction=None,
        battlefield_role=["Troops"],
        keywords=["ORKS", "INFANTRY"],
        wounds=1,
        models_min=5,
        models_max=20,
        power_level=5,
        move='6"',
        bs="5+",
        ws="3+",
        strength=4,
        toughness=4,
        attacks=2,
        save=6,
        invuln_save=None,
        leadership=7,
        oc=2,
        fnp=None,
        model_groups=[group],
    )
    return unit, group


def _group_assignment_session():  # type: ignore[no-untyped-def]
    return _SS(
        selected_model_group="g1",
        group_targets={"g1": [("Necrons", "u_def")]},
        group_decl={},
    )


def test_render_group_assignment_offers_command_reroll_on_attack_count(monkeypatch) -> None:
    unit, _ = _melee_group_fixture()
    atk_state = {"group_models": {"g1": 5}}
    common.st.session_state = _group_assignment_session()
    monkeypatch.setattr(common.st, "columns", lambda n: tuple(MagicMock() for _ in range(n)))
    monkeypatch.setattr(common.st, "markdown", lambda *a, **kw: None)
    monkeypatch.setattr(common.st, "number_input", lambda *a, **kw: 3)
    monkeypatch.setattr(common.st, "button", lambda *a, **kw: False)
    def_unit = SimpleNamespace(toughness=4, save=6, invuln_save=None, name_en="Warriors")
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (def_unit, {}))
    spy = MagicMock()
    monkeypatch.setattr(common, "render_inline_command_reroll", spy)

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=True)

    spy.assert_called_once()
    call = spy.call_args
    assert call.args[0] == "Orks"  # the attacker rolled the dice — attacker pays
    assert call.args[1] == "fight"
    assert call.kwargs["reopen_key"] == "decl_a_g1_atk1_u_def_Choppa"
    assert call.kwargs["label_context"] == "Choppa"  # button names its weapon (4c-a)
    assert callable(call.kwargs["on_reroll"])
    call.kwargs["on_reroll"]()  # no-op — must not raise


def test_render_group_assignment_reroll_offer_outside_target_tile(monkeypatch) -> None:
    """S136 4c-a Option B: the offer renders below the bordered target tile, not inside it."""
    unit, _ = _melee_group_fixture()
    atk_state = {"group_models": {"g1": 5}}
    common.st.session_state = _group_assignment_session()
    tile_depth = {"n": 0}

    class _TileCM:
        def __enter__(self):  # type: ignore[no-untyped-def]
            tile_depth["n"] += 1
            return self

        def __exit__(self, *exc):  # type: ignore[no-untyped-def]
            tile_depth["n"] -= 1
            return False

    monkeypatch.setattr(common.st, "container", lambda *a, **kw: _TileCM())
    monkeypatch.setattr(common.st, "columns", lambda n: tuple(MagicMock() for _ in range(n)))
    monkeypatch.setattr(common.st, "markdown", lambda *a, **kw: None)
    monkeypatch.setattr(common.st, "number_input", lambda *a, **kw: 3)
    monkeypatch.setattr(common.st, "button", lambda *a, **kw: False)
    def_unit = SimpleNamespace(toughness=4, save=6, invuln_save=None, name_en="Warriors")
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (def_unit, {}))
    depth_at_offer: list[int] = []
    monkeypatch.setattr(
        common,
        "render_inline_command_reroll",
        lambda *a, **kw: depth_at_offer.append(tile_depth["n"]),
    )

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=True)

    assert depth_at_offer == [0]  # rendered once, at container depth 0 (outside the tile)


def test_render_group_assignment_no_offer_when_attacks_fixed(monkeypatch) -> None:
    """S136 Befund 4c-b: a fixed Attacks value has no dice roll to re-roll."""
    unit, group = _melee_group_fixture()
    group.weapons[0].profiles[0].attacks = "1"
    atk_state = {"group_models": {"g1": 5}}
    common.st.session_state = _group_assignment_session()
    monkeypatch.setattr(common.st, "columns", lambda n: tuple(MagicMock() for _ in range(n)))
    monkeypatch.setattr(common.st, "markdown", lambda *a, **kw: None)
    monkeypatch.setattr(common.st, "number_input", lambda *a, **kw: 3)
    monkeypatch.setattr(common.st, "button", lambda *a, **kw: False)
    def_unit = SimpleNamespace(toughness=4, save=6, invuln_save=None, name_en="Warriors")
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (def_unit, {}))
    spy = MagicMock()
    monkeypatch.setattr(common, "render_inline_command_reroll", spy)

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=True)

    spy.assert_not_called()


def test_render_group_assignment_no_offer_when_not_melee(monkeypatch) -> None:
    """S137: ranged fixed Attacks — like melee, no dice roll means no offer."""
    unit, group = _melee_group_fixture()
    ranged_profile = WeaponProfile(
        weapon_type="Rapid Fire 1",
        range_inches=24,
        attacks="1",
        strength=4,
        ap=0,
        damage="1",
        is_melee=False,
    )
    group.weapons.append(Weapon(id="w2", name_en="Slugga", profiles=[ranged_profile]))
    atk_state = {"group_models": {"g1": 5}}
    common.st.session_state = _group_assignment_session()
    monkeypatch.setattr(common.st, "markdown", lambda *a, **kw: None)
    monkeypatch.setattr(common.st, "caption", lambda *a, **kw: None)
    monkeypatch.setattr(common.st, "columns", lambda n: tuple(MagicMock() for _ in range(n)))
    monkeypatch.setattr(common.st, "number_input", lambda *a, **kw: 0)
    monkeypatch.setattr(common.st, "button", lambda *a, **kw: False)
    def_unit = SimpleNamespace(toughness=4, save=6, invuln_save=None, name_en="Warriors")
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (def_unit, {}))
    spy = MagicMock()
    monkeypatch.setattr(common, "render_inline_command_reroll", spy)

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=False)

    spy.assert_not_called()


# ---------------------------------------------------------------------------
# S137 — Stikkbomb-Befund: every dice-based Attacks weapon in the data is
# ranged, but only the melee branch offered the Command Re-Roll. The ranged
# branch now collects the same anchor-only offer (no value field — the player
# assigns models, the rolled count is never typed in), phase-keyed to
# "shooting" (plain ranged) vs. "fight" (melee / pistols-in-melee).
# ---------------------------------------------------------------------------


def _ranged_group_fixture(attacks: str = "D6"):  # type: ignore[no-untyped-def]
    unit, group = _melee_group_fixture()
    ranged_profile = WeaponProfile(
        weapon_type=f"Grenade {attacks}",
        range_inches=8,
        attacks=attacks,
        strength=3,
        ap=0,
        damage="1",
        is_melee=False,
    )
    group.weapons = [Weapon(id="w2", name_en="Stikkbombz", profiles=[ranged_profile])]
    return unit, group


def _patch_ranged_widgets(monkeypatch, models_val: int):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(common.st, "markdown", lambda *a, **kw: None)
    monkeypatch.setattr(common.st, "caption", lambda *a, **kw: None)
    monkeypatch.setattr(common.st, "columns", lambda n: tuple(MagicMock() for _ in range(n)))
    monkeypatch.setattr(common.st, "number_input", lambda *a, **kw: models_val)
    monkeypatch.setattr(common.st, "button", lambda *a, **kw: False)
    def_unit = SimpleNamespace(toughness=4, save=6, invuln_save=None, name_en="Warriors")
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (def_unit, {}))
    spy = MagicMock()
    monkeypatch.setattr(common, "render_inline_command_reroll", spy)
    return spy


def test_render_group_assignment_ranged_dice_attacks_offers_command_reroll(monkeypatch) -> None:
    """S137 regression: Stikkbombz (Grenade, Attacks D6) must get the offer."""
    unit, _ = _ranged_group_fixture(attacks="D6")
    atk_state = {"group_models": {"g1": 5}}
    common.st.session_state = _group_assignment_session()
    spy = _patch_ranged_widgets(monkeypatch, models_val=1)

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=False)

    spy.assert_called_once()
    call = spy.call_args
    assert call.args[0] == "Orks"  # the attacker rolled the dice — attacker pays
    assert call.args[1] == "shooting"  # plain ranged = Shooting phase, not "fight"
    assert call.kwargs["reopen_key"] == "decl_m_g1_atk1_u_def_Stikkbombz"
    assert call.kwargs["label_context"] == "Stikkbombz"
    call.kwargs["on_reroll"]()  # anchor-only no-op — must not raise


def test_render_group_assignment_ranged_no_offer_without_assigned_models(monkeypatch) -> None:
    """No thrower assigned (grenades default to 0) → no roll happened to re-roll."""
    unit, _ = _ranged_group_fixture(attacks="D6")
    atk_state = {"group_models": {"g1": 5}}
    common.st.session_state = _group_assignment_session()
    spy = _patch_ranged_widgets(monkeypatch, models_val=0)

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=False)

    spy.assert_not_called()


def test_render_group_assignment_ranged_fixed_attacks_no_offer_despite_models(monkeypatch) -> None:
    """Fixed ranged Attacks with models assigned still has no dice roll to re-roll."""
    unit, group = _ranged_group_fixture(attacks="D6")
    group.weapons[0].profiles[0].attacks = "2"
    group.weapons[0].profiles[0].weapon_type = "Assault 2"
    atk_state = {"group_models": {"g1": 5}}
    common.st.session_state = _group_assignment_session()
    spy = _patch_ranged_widgets(monkeypatch, models_val=3)

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=False)

    spy.assert_not_called()


def test_render_group_assignment_ranged_in_melee_offer_uses_fight_phase(monkeypatch) -> None:
    """Pistols fired while in melee happen in the Fight phase — offer keyed accordingly."""
    unit, group = _ranged_group_fixture(attacks="D3")
    group.weapons[0].profiles[0].weapon_type = "Pistol D3"
    atk_state = {"group_models": {"g1": 5}}
    common.st.session_state = _group_assignment_session()
    spy = _patch_ranged_widgets(monkeypatch, models_val=2)

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=False, in_melee=True)

    spy.assert_called_once()
    assert spy.call_args.args[1] == "fight"


# ---------------------------------------------------------------------------
# R-COMBAT-35 (S157) — combi-weapon profile checkbox UI: any(p.combi for p in
# profiles) swaps the single-select radio for one checkbox per profile so the
# player may fire one profile OR both. Firing both records combi_hit_mod=-1 on
# every generated entry; compute_resolution_context later surfaces this as a
# named "Combi (both profiles)" hit modifier fed into resolve_attack_modifiers
# (combat.py) — covered separately in tests/gameMechanic/test_combat.py.
# ---------------------------------------------------------------------------


def _combi_group_fixture():  # type: ignore[no-untyped-def]
    rokkit = WeaponProfile(
        weapon_type="Heavy D3",
        range_inches=24,
        attacks="D3",
        strength=8,
        ap=-2,
        damage="3",
        is_melee=False,
        name_en="Rokkit",
        combi=True,
    )
    shoota = WeaponProfile(
        weapon_type="Dakka",
        range_inches=18,
        attacks="3/2",
        strength=4,
        ap=0,
        damage="1",
        is_melee=False,
        name_en="Shoota",
        combi=True,
    )
    weapon = Weapon(id="w1", name_en="Kombi-rokkit", profiles=[rokkit, shoota])
    group = ModelGroup(id="g1", name_en="Boss Nob", count=1, weapons=[weapon], priority=1)
    unit = Unit(
        id="test.unit.bossnob",
        name_en="Boss Nob",
        name_de="Boss Nob",
        faction="Orks",
        subfaction=None,
        battlefield_role=["HQ"],
        keywords=["ORKS", "INFANTRY"],
        wounds=1,
        models_min=1,
        models_max=1,
        power_level=1,
        move='6"',
        bs="5+",
        ws="3+",
        strength=5,
        toughness=5,
        attacks=4,
        save=6,
        invuln_save=None,
        leadership=8,
        oc=1,
        fnp=None,
        model_groups=[group],
    )
    return unit, group


class _CheckboxCol:
    """Fake st.columns() cell — supports the two widget calls this test exercises."""

    def __init__(self, responses: dict) -> None:  # type: ignore[type-arg]
        self._responses = responses

    def checkbox(self, label, value=False, key=""):  # type: ignore[no-untyped-def]
        return self._responses.get(key, value)

    def metric(self, *a, **kw):  # type: ignore[no-untyped-def]
        return None


def _patch_combi_widgets(monkeypatch, checkbox_responses: dict):  # type: ignore[no-untyped-def, type-arg]
    captured_markdown: list[str] = []
    monkeypatch.setattr(common.st, "markdown", lambda html, **kw: captured_markdown.append(html))
    monkeypatch.setattr(common.st, "caption", lambda *a, **kw: None)
    monkeypatch.setattr(
        common.st,
        "columns",
        lambda n: tuple(_CheckboxCol(checkbox_responses) for _ in range(n)),
    )
    monkeypatch.setattr(common.st, "number_input", lambda *a, **kw: 1)
    monkeypatch.setattr(common.st, "button", lambda *a, **kw: True)
    def_unit = SimpleNamespace(toughness=4, save=6, invuln_save=None, name_en="Warriors")
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (def_unit, {}))
    monkeypatch.setattr(common, "render_inline_command_reroll", lambda *a, **kw: None)
    return captured_markdown


def test_combi_checkbox_ui_renders_both_profiles_and_applies_penalty(monkeypatch) -> None:
    """Both Kombi-rokkit profiles checked → two entries, each combi_hit_mod=-1,
    and both profile names appear in the rendered HTML (HTML-Output-Test per
    Test-Mandat — render_group_assignment is coverage-excluded uiLayout code)."""
    unit, _ = _combi_group_fixture()
    atk_state = {"group_models": {"g1": 1}}
    common.st.session_state = _group_assignment_session()
    p_key = "decl_p_g1_atk1_u_def_Kombi-rokkit"
    markdown_html = _patch_combi_widgets(monkeypatch, {f"{p_key}_0": True, f"{p_key}_1": True})

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=False)

    entries = common.st.session_state.group_decl["g1"]
    assert len(entries) == 2
    assert all(e["combi_hit_mod"] == -1 for e in entries)
    combined = "\n".join(markdown_html)
    assert "Rokkit" in combined
    assert "Shoota" in combined


def test_combi_checkbox_ui_single_profile_selected_has_no_penalty(monkeypatch) -> None:
    """Only the Rokkit profile checked → one entry, no combi malus."""
    unit, _ = _combi_group_fixture()
    atk_state = {"group_models": {"g1": 1}}
    common.st.session_state = _group_assignment_session()
    p_key = "decl_p_g1_atk1_u_def_Kombi-rokkit"
    _patch_combi_widgets(monkeypatch, {f"{p_key}_0": True, f"{p_key}_1": False})

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=False)

    entries = common.st.session_state.group_decl["g1"]
    assert len(entries) == 1
    assert entries[0]["combi_hit_mod"] == 0


# ---------------------------------------------------------------------------
# S130/S135 Paket 4b — _render_damage_block(): Command Re-Roll wired at the
# post-Apply lock (Hit/Wound/Save have no separately captured roll in this
# app — see session report; the collapsed "damage applied" result is the one
# closest analogue, attributed to the attacker since only the damage die is
# actually theirs). Migrated from render_inline_command_reroll's Pull-not-Push
# offer to the canonical render_reactive_stratagem_box GO card in Paket 4b.
# ---------------------------------------------------------------------------


def test_damage_block_offers_command_reroll_after_apply(monkeypatch) -> None:
    session = _SS(
        res_tab1={
            "applied": True,
            "models_lost": 1,
            "mortal_wounds": 0,
            "total_damage": 3,
            "wiped_groups": [],
        }
    )
    common.st.session_state = session
    monkeypatch.setattr(common.st, "success", lambda *a, **kw: None)
    monkeypatch.setattr(common.st, "button", lambda *a, **kw: False)
    spy = MagicMock()
    monkeypatch.setattr(common, "render_reactive_stratagem_box", spy)

    common._render_damage_block(None, "Necrons", "u1", None, "Orks", "Boyz", "shooting", "tab1")

    spy.assert_called_once()
    call = spy.call_args
    assert call.args[0] == "Orks"  # the attacker's damage roll — attacker pays
    assert call.args[1] == "shooting"
    assert call.args[2] == "after_roll"
    assert call.kwargs["decline_key"] == "dmg_tab1"
    assert call.kwargs["effect_type"] == "reroll"


def test_damage_block_command_reroll_reopens_the_applied_result(monkeypatch) -> None:
    session = _SS(
        res_tab1={
            "applied": True,
            "models_lost": 1,
            "mortal_wounds": 0,
            "total_damage": 3,
            "wiped_groups": [],
        }
    )
    common.st.session_state = session
    monkeypatch.setattr(common.st, "success", lambda *a, **kw: None)
    monkeypatch.setattr(common.st, "button", lambda *a, **kw: False)
    captured = {}

    def _fake_reroll(faction, phase, event, *, decline_key, context_caption, **kw):  # type: ignore[no-untyped-def]
        captured["on_resolved"] = kw["on_resolved"]

    monkeypatch.setattr(common, "render_reactive_stratagem_box", _fake_reroll)

    common._render_damage_block(None, "Necrons", "u1", None, "Orks", "Boyz", "shooting", "tab1")
    captured["on_resolved"]()

    assert "res_tab1" not in session


class _ColStub:
    """Stand-in for the st.columns() half-width block used by the pre-Apply
    damage fields — supports the widget calls _render_damage_block makes on
    it (number_input/caption/button), unlike the generic _FakeCtx."""

    def number_input(self, *a, **kw):  # type: ignore[no-untyped-def]
        return 0

    def caption(self, *a, **kw):  # type: ignore[no-untyped-def]
        return None

    def button(self, *a, **kw):  # type: ignore[no-untyped-def]
        return False


def test_damage_block_no_offer_before_damage_applied(monkeypatch) -> None:
    """Before Apply, the fields are still directly editable — nothing is
    "locked" yet, so there is nothing here for Command Re-Roll to reopen."""
    session = _SS(res_tab1={})
    common.st.session_state = session
    spy = MagicMock()
    monkeypatch.setattr(common, "render_reactive_stratagem_box", spy)
    unit = SimpleNamespace(wounds=1, models_max=5)
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (unit, {"group_wounds": {}}))
    monkeypatch.setattr(common.st, "markdown", lambda *a, **kw: None)
    monkeypatch.setattr(common.st, "columns", lambda n: tuple(_ColStub() for _ in range(n)))
    monkeypatch.setattr(common.st, "button", lambda *a, **kw: False)
    profile = SimpleNamespace(damage="1", abilities="", effect=None, is_melee=False)

    common._render_damage_block(unit, "Necrons", "u1", profile, "Orks", "Boyz", "shooting", "tab1")

    spy.assert_not_called()


# ---------------------------------------------------------------------------
# S136 Stufe 2 — Hit-/Wound-/Save-Anker: _render_resolution_tab() offers
# render_inline_command_reroll directly under each dice block (Familie 2,
# analog Advance/Charge/Attacken-Anzahl — kein Wertfeld, da die App diese
# Würfe nirgends separat erfasst). R-CMD-12: schließt die letzten 3 der 9
# reaktiven Command-Re-Roll-Fenster (Hit, Wound, Save).
# ---------------------------------------------------------------------------


def _resolution_tab_entry_and_units():  # type: ignore[no-untyped-def]
    """Real melee Choppa attack (Orks Boyz -> Necrons Warriors). def_unit is a
    plain SimpleNamespace (only the attributes _render_resolution_tab actually
    reads) — combat resolve functions, abilityEngine and the loader run for
    real against empty per-attack state, exactly as in production when no
    buffs/directives are active.

    Unlike _melee_group_fixture() (built for render_group_assignment, which
    reads weapons from model_groups), _render_resolution_tab reads the
    attacker's top-level Unit.weapons — so the weapon must be attached there
    too, or weapon lookup fails silently (st.error + early return, no HIT/
    WOUND/SAVE blocks rendered at all)."""
    unit, _ = _melee_group_fixture()
    unit.weapons = list(unit.model_groups[0].weapons)
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Choppa",
        "profile_idx": 0,
        "models_count": 5,
    }
    def_unit = SimpleNamespace(
        toughness=4, save=6, invuln_save=None, fnp=None, name_en="Warriors", rules=[]
    )
    return entry, unit, def_unit


def _install_resolution_tab_fixture(monkeypatch, def_unit):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (def_unit, {}))
    monkeypatch.setattr(common, "render_reactive_stratagem_box", lambda *a, **kw: None)
    monkeypatch.setattr(common, "_render_damage_block", lambda *a, **kw: None)


def test_render_resolution_tab_offers_command_reroll_on_hit_roll(monkeypatch) -> None:
    """Hit-Anker: attacker (Orks) rolled the hit — attacker pays. Clicking it
    spends CP from the ATTACKER's pool and marks the phase-shared usage set,
    which the Wound offer below shares (same faction+phase pool — R-CMD-12
    'once per phase' is a single pool, not per-anchor). S139 B12c (S138
    Grundannahme 4b, "Once-per-Phase wird erzwungen und sichtbar gemacht"):
    the Wound offer must still reach st.button — as a disabled "Used" at its
    OWN anchor, since the spend was recorded at the Hit anchor — not vanish
    the way it did before this change."""
    entry, unit, def_unit = _resolution_tab_entry_and_units()
    _install_resolution_tab_fixture(monkeypatch, def_unit)
    session = _reactive_box_session(cp={"Necrons": 5, "Orks": 5})
    hit_key = f"cmd_reroll_Orks_fight_{_COMMAND_REROLL_ID}_tab1_hit"
    wound_key = f"cmd_reroll_Orks_fight_{_COMMAND_REROLL_ID}_tab1_wound"
    button_calls, _ = _reroll_widgets(monkeypatch, session, clicked_key=hit_key)

    common._render_resolution_tab(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert any(key == hit_key for _, key in button_calls)
    assert session["cp"]["Orks"] == 4  # attacker pays — 5 - 1 CP
    assert _COMMAND_REROLL_ID in session["used_stratagem_ids"]["Orks"]
    # Wound offer shares the same (Orks, fight) pool — already used, at a
    # DIFFERENT anchor (the Hit anchor) — shows up disabled as "Used", not Undo.
    wound_labels = [label for label, key in button_calls if key == wound_key]
    assert len(wound_labels) == 1
    assert "Used" in wound_labels[0]
    assert "Undo" not in wound_labels[0]


def test_render_resolution_tab_offers_command_reroll_on_wound_roll(monkeypatch) -> None:
    """Wound-Anker: attacker (Orks) rolled the wound — attacker pays, same as
    Hit. Verified independently (nothing clicked yet) so the offer's own
    faction/phase/key are checked without the Hit anchor having consumed the
    shared pool first."""
    entry, unit, def_unit = _resolution_tab_entry_and_units()
    _install_resolution_tab_fixture(monkeypatch, def_unit)
    session = _reactive_box_session(cp={"Necrons": 5, "Orks": 5})
    wound_key = f"cmd_reroll_Orks_fight_{_COMMAND_REROLL_ID}_tab1_wound"
    button_calls, _ = _reroll_widgets(monkeypatch, session, clicked_key=None)

    common._render_resolution_tab(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert any(key == wound_key for _, key in button_calls)
    assert session["cp"]["Orks"] == 5  # not clicked — Pull, not Push, costs nothing
    assert session["used_stratagem_ids"] == {}


def test_render_resolution_tab_offers_command_reroll_on_save_roll(monkeypatch) -> None:
    """Save-Anker: the DEFENDER (Necrons) made the saving throw — defender
    pays, unlike Hit/Wound above. Clicking it spends CP from Necrons' pool
    only, leaving the attacker's (Orks) CP and usage untouched — the two
    factions' pools are independent."""
    entry, unit, def_unit = _resolution_tab_entry_and_units()
    _install_resolution_tab_fixture(monkeypatch, def_unit)
    session = _reactive_box_session(cp={"Necrons": 5, "Orks": 5})
    save_key = f"cmd_reroll_Necrons_fight_{_COMMAND_REROLL_ID}_tab1_save"
    button_calls, _ = _reroll_widgets(monkeypatch, session, clicked_key=save_key)

    common._render_resolution_tab(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert any(key == save_key for _, key in button_calls)
    assert session["cp"]["Necrons"] == 4  # defender pays — 5 - 1 CP
    assert _COMMAND_REROLL_ID in session["used_stratagem_ids"]["Necrons"]
    assert session["cp"]["Orks"] == 5  # attacker's pool untouched
    assert "Orks" not in session["used_stratagem_ids"]


# ---------------------------------------------------------------------------
# S137 Bug A — exactly ONE divider between WOUND and SAVE (no stray "---")
# ---------------------------------------------------------------------------


def test_render_resolution_tab_no_extra_divider_before_save_block(monkeypatch) -> None:
    """Regression (S137 Bug A): the WOUND→SAVE seam renders ONE divider.

    _render_dice_save_block already opens with block_divider_html(); the old
    standalone st.markdown("---") right before it (a 6d-v2 leftover from
    before block_divider_html existed) stacked a second <hr> on top, showing
    as a blank band between the blocks. Expected: no raw "---" call anywhere
    before the SAVE title (the one after SAVE separates the DAMAGE block and
    is legitimate), and exactly two block dividers total (WOUND, SAVE).

    Both _common's and diceHtml's markdown calls are captured: the two
    modules can hold DIFFERENT streamlit mocks in a full test run (each test
    file installs its own sys.modules['streamlit'] mock, but already-imported
    modules keep the one they were imported under)."""
    import uiLayout.diceHtml as dice_html_mod  # noqa: PLC0415
    from uiLayout.diceCompose import block_divider_html  # noqa: PLC0415

    entry, unit, def_unit = _resolution_tab_entry_and_units()
    _install_resolution_tab_fixture(monkeypatch, def_unit)
    session = _reactive_box_session(cp={"Necrons": 5, "Orks": 5})
    _reroll_widgets(monkeypatch, session, clicked_key=None)

    captured: list[str] = []
    monkeypatch.setattr(common.st, "markdown", lambda html, **_kw: captured.append(str(html)))
    monkeypatch.setattr(
        dice_html_mod.st, "markdown", lambda html, **_kw: captured.append(str(html))
    )

    common._render_resolution_tab(entry, "Orks", unit, {}, True, "fight", "tab1")

    save_idx = next(i for i, html in enumerate(captured) if html.startswith("**SAVE**"))
    assert (
        "---" not in captured[:save_idx]
    ), "stray st.markdown('---') before the SAVE block is back"
    combined = "\n".join(captured)
    divider_count = combined.count(block_divider_html())
    assert (
        divider_count == 2
    ), f"Expected exactly 2 block dividers (WOUND, SAVE), got {divider_count}"


# ---------------------------------------------------------------------------
# S146 1a — Declaration-time on_target anchor (S143 concept, Option A +
# S146 Fix 2): render_group_assignment renders render_reactive_stratagem_box
# per assigned target, so a "selected as the target of an attack" reactive GO
# (Whirling Onslaught, real Necrons data) is clickable the moment the target
# is designated. Since Fix 2 this is the ONLY render spot for wound-roll
# on_target GOs (the Wound-Anker call in _render_resolution_tab was removed);
# used_here/used_elsewhere bookkeeping prevents a double CP spend across the
# per-target tiles of this anchor.
# ---------------------------------------------------------------------------


def _declaration_anchor_setup(  # type: ignore[no-untyped-def]
    monkeypatch, targets=None, keyword="DESTROYER CULT"
):
    """Fight-phase session: Orks group g1 has designated a Necron defender.

    `keyword` gates which conditions-scoped on_target GO the defender matches
    (default DESTROYER CULT → Whirling Onslaught, the original S146 case;
    B1-Umsetzung S147 reuses this for FLAYED ONES → Shadows of Drazak and
    QUANTUM SHIELDING → Quantum Deflection, now that the Hit-/Save-Anker were
    retired and those two GOs render here too)."""
    targets = targets or [("Necrons", "u_def")]
    unit, _ = _melee_group_fixture()  # Orks attacker, group "g1"
    atk_state = {"group_models": {"g1": 5}, "melee_with": list(targets)}
    session = _reactive_box_session(
        phase_idx=6,  # fight — Whirling Onslaught is phase "any"
        selected_unit=("Orks", "atk1"),
        selected_model_group="g1",
        group_targets={"g1": list(targets)},
        group_decl={},
    )
    captured = _install_reactive_box_session(monkeypatch, session)
    destroyers = SimpleNamespace(
        name_en="Skorpekh Destroyers",
        toughness=5,
        save=3,
        invuln_save=None,
        has_keyword=lambda kw: kw == keyword,
    )
    monkeypatch.setattr(
        common,
        "lookup",
        lambda faction, uid: (unit, atk_state) if uid == "atk1" else (destroyers, {}),
    )
    monkeypatch.setattr(common.st, "columns", lambda n: tuple(MagicMock() for _ in range(n)))
    monkeypatch.setattr(common.st, "markdown", lambda *a, **kw: None)
    monkeypatch.setattr(common.st, "number_input", lambda *a, **kw: 3)
    monkeypatch.setattr(common.st, "button", lambda *a, **kw: False)
    monkeypatch.setattr(common, "render_inline_command_reroll", MagicMock())
    return unit, atk_state, session, captured, destroyers


def test_declaration_anchor_shows_whirling_onslaught_when_target_assigned(monkeypatch) -> None:
    unit, atk_state, _, captured, _ = _declaration_anchor_setup(monkeypatch)

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=True)

    card = next(c for c in captured if c["name"] == "Whirling Onslaught")
    assert card["state"] == "ready"
    # Per-(gid, target) decline_key keeps multi-target keys collision-free
    assert "decl_target_g1_atk1_u_def" in card["key"]


def test_declaration_anchor_card_disappears_when_target_toggled_off(monkeypatch) -> None:
    """Pflichtteil (S143 Konzept, Option A): the card must vanish on the very
    next rerun after toggle_group_target removes the target again — the anchor
    re-reads group_targets each run, no ghost anchor for an unassigned target."""
    unit, atk_state, session, captured, _ = _declaration_anchor_setup(monkeypatch)

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=True)
    assert any(c["name"] == "Whirling Onslaught" for c in captured)

    assert common.toggle_group_target("Necrons", "u_def") is True  # real toggle path
    assert session["group_targets"]["g1"] == []

    captured.clear()
    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=True)
    assert captured == []


def test_declaration_anchor_use_locks_other_target_tile_against_double_spend(
    monkeypatch,
) -> None:
    """With two assigned targets the same GO renders once per target tile — two
    anchors. One spend must lock both: the triggering tile shows "used" (Undo),
    the other tile "used_elsewhere" (disabled), and CP is charged exactly once
    (seit Fix 2 der einzige Mehrfach-Anker-Fall, der Wound-Anker entfiel)."""
    unit, atk_state, session, captured, _ = _declaration_anchor_setup(
        monkeypatch, targets=[("Necrons", "u_def"), ("Necrons", "u_def2")]
    )

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=True)
    cards = [c for c in captured if c["name"] == "Whirling Onslaught"]
    assert len(cards) == 2  # one card per target tile
    next(c for c in cards if "u_def2" not in c["key"])["on_use"]()
    assert session["cp"]["Necrons"] == 4  # 5 - 1 CP, spent once

    captured.clear()
    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=True)
    by_key = {c["key"]: c for c in captured if c["name"] == "Whirling Onslaught"}
    first_tile = next(c for k, c in by_key.items() if "u_def2" not in k)
    second_tile = next(c for k, c in by_key.items() if "u_def2" in k)
    assert first_tile["state"] == "used"  # Undo offered only where it was spent
    assert second_tile["state"] == "used_elsewhere"  # disabled "Used", no Undo
    assert session["cp"]["Necrons"] == 4  # still exactly one spend


# ---------------------------------------------------------------------------
# B1 aus S146-Review (Major) — S147 Stakeholder-Entscheid: the Hit-/Save-Anker
# in _render_resolution_tab are retired (same "single place" treatment S146
# Fix 2 already gave the Wound-Anker). Shadows of Drazak (hit debuff) and
# Quantum Deflection (invuln save) now render ONLY at the declaration-time
# target tile (render_group_assignment) — never again at their old dedicated
# anchors inside the resolution tab. Positive coverage lives alongside the
# Whirling Onslaught declaration-anchor tests above (same fixture, different
# keyword); negative coverage (B2) proves the retired anchors no longer emit
# a card for either GO even when the defender matches their condition.
# ---------------------------------------------------------------------------


def test_declaration_anchor_shows_shadows_of_drazak_when_target_assigned(
    monkeypatch,
) -> None:
    unit, atk_state, _, captured, _ = _declaration_anchor_setup(monkeypatch, keyword="FLAYED ONES")

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=True)

    card = next(c for c in captured if c["name"] == "Shadows of Drazak")
    assert card["state"] == "ready"


def test_declaration_anchor_shows_quantum_deflection_when_target_assigned(
    monkeypatch,
) -> None:
    unit, atk_state, _, captured, _ = _declaration_anchor_setup(
        monkeypatch, keyword="QUANTUM SHIELDING"
    )

    common.render_group_assignment("Orks", "atk1", unit, atk_state, use_melee=True)

    card = next(c for c in captured if c["name"] == "Quantum Deflection")
    assert card["state"] == "ready"


def test_render_resolution_tab_hit_anchor_omits_on_target_go(monkeypatch) -> None:
    """Negativ-Test B2: Shadows of Drazak used to render a SECOND time at the
    old Hit-Anker inside _render_resolution_tab (backlog B1 doubled card) —
    that render_reactive_stratagem_box call was removed in S147, so no card
    for it may appear from this tab at all anymore, even though the defender
    still matches its FLAYED ONES condition."""
    entry, unit, def_unit = _resolution_tab_entry_and_units()
    def_unit.has_keyword = lambda kw: kw == "FLAYED ONES"
    session = _reactive_box_session(cp={"Necrons": 5, "Orks": 5})
    captured = _install_reactive_box_session(monkeypatch, session)
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (def_unit, {}))
    monkeypatch.setattr(common, "_render_damage_block", lambda *a, **kw: None)
    _reroll_widgets(monkeypatch, session, clicked_key=None)

    common._render_resolution_tab(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert all(c["name"] != "Shadows of Drazak" for c in captured)


def test_render_resolution_tab_save_anchor_omits_on_target_go(monkeypatch) -> None:
    """Negativ-Test B2: Quantum Deflection used to render a SECOND time at the
    old Save-Anker inside _render_resolution_tab — same retirement as the Hit-
    Anker above, checked against the invuln-save GO instead."""
    entry, unit, def_unit = _resolution_tab_entry_and_units()
    def_unit.has_keyword = lambda kw: kw == "QUANTUM SHIELDING"
    session = _reactive_box_session(cp={"Necrons": 5, "Orks": 5})
    captured = _install_reactive_box_session(monkeypatch, session)
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (def_unit, {}))
    monkeypatch.setattr(common, "_render_damage_block", lambda *a, **kw: None)
    _reroll_widgets(monkeypatch, session, clicked_key=None)

    common._render_resolution_tab(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert all(c["name"] != "Quantum Deflection" for c in captured)


# ---------------------------------------------------------------------------
# S148 Brief 2 — CP-Fresser-Stratagems: modifier: block added to 3 buff_roll
# stratagems that were spending CP without ever applying their hit bonus.
# ---------------------------------------------------------------------------


def _stratagem_by_id(faction: str, strat_id: str):  # type: ignore[no-untyped-def]
    stratagems = load_stratagems(faction)
    return next(s for s in stratagems if s.id == strat_id)


def test_judgement_of_the_triarch_registers_hit_modifier_after_spend() -> None:
    strat = _stratagem_by_id("necrons", "wh40k_9e.necrons.stratagem.judgement_of_the_triarch")
    session = _spend_session()
    common.spend_stratagem(strat, "Necrons", "unit#1")
    mods = session["active_modifiers"]
    assert len(mods) == 1
    assert mods[0]["unit_key"] == "unit#1"
    assert mods[0]["effect"]["roll_type"] == "hit"
    assert mods[0]["effect"]["value"] == 1
    assert mods[0]["effect"]["target"] == "attacker"


def test_showin_off_registers_hit_modifier_after_spend() -> None:
    strat = _stratagem_by_id("orks", "wh40k_9e.orks.stratagem.showin_off")
    session = _spend_session()
    session["cp"]["Orks"] = 5
    common.spend_stratagem(strat, "Orks", "unit#1")
    mods = session["active_modifiers"]
    assert len(mods) == 1
    assert mods[0]["unit_key"] == "unit#1"
    assert mods[0]["effect"]["roll_type"] == "hit"
    assert mods[0]["effect"]["value"] == 1
    assert mods[0]["effect"]["target"] == "attacker"


def test_unbridled_carnage_registers_hit_modifier_after_spend() -> None:
    strat = _stratagem_by_id("orks", "wh40k_9e.orks.stratagem.unbridled_carnage")
    session = _spend_session()
    session["cp"]["Orks"] = 5
    common.spend_stratagem(strat, "Orks", "unit#1")
    mods = session["active_modifiers"]
    assert len(mods) == 1
    assert mods[0]["unit_key"] == "unit#1"
    assert mods[0]["effect"]["roll_type"] == "hit"
    assert mods[0]["effect"]["value"] == 1
    assert mods[0]["effect"]["target"] == "attacker"


# ---------------------------------------------------------------------------
# S142-FixD Brief 1 — compute_resolution_context(): pure resolution math
# extracted from _render_resolution_tab (docs/audit/plans/
# S142_fixD_resolution_tabs.md §4). Covers the three tricky areas the plan
# calls out: S-Bonus-Faltung, Cover-Flag-Ableitung, Bracket-/Gruppen-Overrides.
# ---------------------------------------------------------------------------


def _resolution_context_session(**extra: object) -> _SS:
    """Fresh session bound onto every module's own ``st`` reference.

    Same reason as `_eg_session`: abilityEngine, gameState, and _common each
    hold their own imported ``st`` object captured at import time, so a plain
    ``common.st.session_state = ...`` is not enough when a module was already
    imported (and its `st` bound) by an earlier test file in the same run.
    """
    base = dict(
        first_player="Necrons",
        second_player="Orks",
        p1_faction_dir="necrons",
        p2_faction_dir="orks",
    )
    base.update(extra)
    session = _SS(**base)
    _st_mock.session_state = session
    _eng.st.session_state = session
    _gs.st.session_state = session
    common.st.session_state = session
    return session


def _bare_def_unit() -> SimpleNamespace:
    return SimpleNamespace(
        toughness=4, save=6, invuln_save=None, fnp=None, name_en="Warriors", rules=[]
    )


def test_compute_resolution_context_returns_none_when_no_weapon_available(monkeypatch) -> None:
    """Mirrors the previous inline 'Weapon not found' early exit: an attacker
    with no phase-matching weapon at all yields no filtered candidates, so the
    fallback-to-first-weapon logic has nothing to fall back to."""
    unit, _ = _melee_group_fixture()
    unit.weapons = []
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Choppa",
        "profile_idx": 0,
        "models_count": 5,
    }
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), {}))
    _resolution_context_session()

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert ctx is None


def test_compute_resolution_context_folds_strength_bonus_after_times_n(monkeypatch) -> None:
    """S-Bonus-Faltung: a ×N weapon must give (User×N) + bonus, not (User+bonus)×N
    — the WOUND block would otherwise show the wrong S (S147/S146 Fix 1 intent)."""
    profile = WeaponProfile(
        weapon_type="Melee",
        range_inches=0,
        attacks="D6",
        strength="×2",
        ap=0,
        damage="1",
        is_melee=True,
    )
    weapon = Weapon(id="w_klaw", name_en="Power Klaw", profiles=[profile])
    unit, _ = _melee_group_fixture()  # strength=4
    unit.weapons = [weapon]
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Power Klaw",
        "profile_idx": 0,
        "models_count": 5,
    }
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), {}))
    session = _resolution_context_session()
    session["active_modifiers"] = [
        {
            "unit_key": "atk1",
            "source": "Test Stratagem",
            "effect": {"roll_type": "strength", "value": 1, "target": "attacker"},
        }
    ]

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert ctx is not None
    assert ctx.strength == 9  # (4×2) + 1, not (4+1)×2


def test_compute_resolution_context_dense_cover_checkbox_adds_hit_penalty(monkeypatch) -> None:
    """Cover-Flag-Ableitung: the Dense Cover checkbox (read before it renders,
    Variante C) must fold a −1 Hit modifier into atk_result for shooting."""
    profile = WeaponProfile(
        weapon_type="Rapid Fire 1",
        range_inches=24,
        attacks="2",
        strength=4,
        ap=0,
        damage="1",
        is_melee=False,
    )
    weapon = Weapon(id="w_bolter", name_en="Bolter", profiles=[profile])
    unit, _ = _melee_group_fixture()
    unit.weapons = [weapon]
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Bolter",
        "profile_idx": 0,
        "models_count": 5,
    }
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), {}))
    session = _resolution_context_session()
    session["dense_cover_tab1"] = True

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, False, "shooting", "tab1")

    assert ctx is not None
    assert "Dense Cover" in [m["label"] for m in ctx.atk_result["hit"]["stack"]]


def test_compute_resolution_context_light_cover_checkbox_adds_save_bonus(monkeypatch) -> None:
    """Cover-Flag-Ableitung: the Light Cover checkbox folds a +1 Save modifier."""
    profile = WeaponProfile(
        weapon_type="Rapid Fire 1",
        range_inches=24,
        attacks="2",
        strength=4,
        ap=0,
        damage="1",
        is_melee=False,
    )
    weapon = Weapon(id="w_bolter", name_en="Bolter", profiles=[profile])
    unit, _ = _melee_group_fixture()
    unit.weapons = [weapon]
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Bolter",
        "profile_idx": 0,
        "models_count": 5,
    }
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), {}))
    session = _resolution_context_session()
    session["light_cover_tab1"] = True

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, False, "shooting", "tab1")

    assert ctx is not None
    assert "Light Cover" in [m["label"] for m in ctx.save_result["stack"]]


def test_compute_resolution_context_eternal_guardian_d1_grants_light_cover_without_checkbox(
    monkeypatch,
) -> None:
    """Cover-Flag-Ableitung: Eternal Guardian D1 auto-grants Light Cover to a
    stationary defender even when the checkbox itself was never ticked —
    auto_light_cover must be folded into save_result on the same rerun."""
    profile = WeaponProfile(
        weapon_type="Rapid Fire 1",
        range_inches=24,
        attacks="2",
        strength=4,
        ap=0,
        damage="1",
        is_melee=False,
    )
    weapon = Weapon(id="w_bolter", name_en="Bolter", profiles=[profile])
    unit, _ = _melee_group_fixture()
    unit.weapons = [weapon]
    entry = {
        "def_faction": "Necrons",
        "def_uid": "test.unit",
        "atk_uid": "atk1",
        "weapon_name": "Bolter",
        "profile_idx": 0,
        "models_count": 5,
    }
    _eg_session(stationary=True)
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), {}))

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, False, "shooting", "tab1")

    assert ctx is not None
    assert ctx.auto_light_cover is True
    assert "Light Cover" in [m["label"] for m in ctx.save_result["stack"]]


def test_compute_resolution_context_heavy_cover_suppressed_when_defender_charged(
    monkeypatch,
) -> None:
    """Cover-Flag-Ableitung: Heavy Cover never applies to a charged defender
    (9E: a charging unit forfeits cover), even if the checkbox is ticked."""
    unit, _ = _melee_group_fixture()
    unit.weapons = list(unit.model_groups[0].weapons)
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Choppa",
        "profile_idx": 0,
        "models_count": 5,
    }
    def_state = {"turn_flags": {"charged": True}}
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), def_state))
    session = _resolution_context_session()
    session["heavy_cover_tab1"] = True

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert ctx is not None
    assert "Heavy Cover" not in [m["label"] for m in ctx.save_result["stack"]]


def test_compute_resolution_context_heavy_cover_applies_when_defender_not_charged(
    monkeypatch,
) -> None:
    """Complement of the suppression test above: an un-charged defender with
    the checkbox ticked does get the +1 Save."""
    unit, _ = _melee_group_fixture()
    unit.weapons = list(unit.model_groups[0].weapons)
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Choppa",
        "profile_idx": 0,
        "models_count": 5,
    }
    def_state = {"turn_flags": {"charged": False}}
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), def_state))
    session = _resolution_context_session()
    session["heavy_cover_tab1"] = True

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert ctx is not None
    assert "Heavy Cover" in [m["label"] for m in ctx.save_result["stack"]]


def test_compute_resolution_context_per_group_ws_override_wins_over_bracket(monkeypatch) -> None:
    """Bracket-/Gruppen-Overrides: a per-group WS override (e.g. Boss Nob WS 2+)
    must win over the unit's live bracket WS when computing the HIT threshold."""
    unit, _ = _melee_group_fixture()  # ws="3+" at the unit level
    unit.weapons = list(unit.model_groups[0].weapons)
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Choppa",
        "profile_idx": 0,
        "models_count": 5,
        "atk_ws": "2+",
    }
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), {}))
    _resolution_context_session()

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert ctx is not None
    assert ctx.atk_result["hit"]["base"] == 2


# ---------------------------------------------------------------------------
# B-105 follow-up (S161) — compute_resolution_context(): invuln_source_label
# names the GO (stratagem or faction ability) that actually stands behind the
# effective invuln save, so the SAVE block can render "Inv N+ [Name]".
# ---------------------------------------------------------------------------


def test_compute_resolution_context_stratagem_invuln_carries_stratagem_source_label(
    monkeypatch,
) -> None:
    """Only a stratagem invuln is active (no faction ability) — the label must
    be the stratagem's own name from active_modifiers[].source."""
    unit, group = _melee_group_fixture()
    unit.weapons = list(group.weapons)
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Choppa",
        "profile_idx": 0,
        "models_count": 5,
    }
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), {}))
    monkeypatch.setattr(_eng, "ability_invuln_save", lambda faction, unit: None)
    session = _resolution_context_session()
    session["active_modifiers"] = [
        {
            "unit_key": "u_def",
            "source": "Quantum Deflection",
            "effect": {"roll_type": "invuln_save", "value": 4, "target": "defender"},
        }
    ]

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert ctx is not None
    assert ctx.invuln_from_ability is True
    assert ctx.invuln_source_label == "Quantum Deflection"


def test_compute_resolution_context_ability_invuln_carries_badge_label(monkeypatch) -> None:
    """Only a faction-ability invuln is active (no stratagem) — the label must
    come from ability_badge_label(), not a hardcoded string."""
    unit, group = _melee_group_fixture()
    unit.weapons = list(group.weapons)
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Choppa",
        "profile_idx": 0,
        "models_count": 5,
    }
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), {}))
    monkeypatch.setattr(_eng, "ability_invuln_save", lambda faction, unit: 5)
    monkeypatch.setattr(_eng, "ability_badge_label", lambda faction, unit: "Veil of Darkness")
    _resolution_context_session()

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert ctx is not None
    assert ctx.invuln_from_ability is True
    assert ctx.invuln_source_label == "Veil of Darkness"


def test_compute_resolution_context_invuln_winner_label_picks_lower_stratagem_value(
    monkeypatch,
) -> None:
    """Both sources are active with different values — the strictly lower
    (winning, per the existing min(...) logic) stratagem value must carry its
    own label, not the ability's."""
    unit, group = _melee_group_fixture()
    unit.weapons = list(group.weapons)
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Choppa",
        "profile_idx": 0,
        "models_count": 5,
    }
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), {}))
    monkeypatch.setattr(_eng, "ability_invuln_save", lambda faction, unit: 5)
    monkeypatch.setattr(_eng, "ability_badge_label", lambda faction, unit: "Veil of Darkness")
    session = _resolution_context_session()
    session["active_modifiers"] = [
        {
            "unit_key": "u_def",
            "source": "Quantum Deflection",
            "effect": {"roll_type": "invuln_save", "value": 4, "target": "defender"},
        }
    ]

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert ctx is not None
    assert ctx.invuln_from_ability is True
    assert ctx.invuln_source_label == "Quantum Deflection"


def test_compute_resolution_context_no_invuln_source_keeps_label_none(monkeypatch) -> None:
    """No bonus invuln at all (native save wins, byte-identical to the
    pre-B-105 behaviour) — invuln_source_label stays None, no chip rendered."""
    unit, group = _melee_group_fixture()
    unit.weapons = list(group.weapons)
    entry = {
        "def_faction": "Necrons",
        "def_uid": "u_def",
        "atk_uid": "atk1",
        "weapon_name": "Choppa",
        "profile_idx": 0,
        "models_count": 5,
    }
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (_bare_def_unit(), {}))
    monkeypatch.setattr(_eng, "ability_invuln_save", lambda faction, unit: None)
    _resolution_context_session()

    ctx = common.compute_resolution_context(entry, "Orks", unit, {}, True, "fight", "tab1")

    assert ctx is not None
    assert ctx.invuln_from_ability is False
    assert ctx.invuln_source_label is None


# ---------------------------------------------------------------------------
# B-028a — spend_ability()/undo_ability() + reactive-ability anchor bookkeeping
# ---------------------------------------------------------------------------


def _reactive_ability(
    aid: str = "test.ability",
    name: str = "Test Reactive Ability",
    phase: str | list[str] = "fight",
    event: str | None = "model_destroyed",
    player: str = "either",
    conditions: list | None = None,  # type: ignore[type-arg]
    effect: Effect | None = None,
) -> Ability:
    return Ability(
        id=aid,
        name_en=name,
        source="unit_ability",
        rule_text="Test rule text.",
        trigger=Trigger(timing="phase_reactive", phase=phase, player=player, event=event),
        conditions=conditions or [],
        effect=effect or Effect(type="mortal_wounds", target="self"),
    )


def _ability_session(**extra) -> _SS:  # type: ignore[no-untyped-def]
    session = _SS(used_ability_ids={}, ability_use_anchors={}, **extra)
    common.st.session_state = session
    return session


def test_spend_ability_marks_used_this_phase() -> None:
    session = _ability_session()
    common.spend_ability(_reactive_ability(aid="ability.a"), "Necrons")
    assert "ability.a" in session["used_ability_ids"]["Necrons"]


def test_spend_ability_without_anchor_id_records_no_anchor() -> None:
    session = _ability_session()
    common.spend_ability(_reactive_ability(aid="ability.a"), "Necrons")
    assert session.get("ability_use_anchors", {}) == {}


def test_spend_ability_with_anchor_id_records_anchor_and_unit_key() -> None:
    session = _ability_session()
    common.spend_ability(
        _reactive_ability(aid="ability.a"), "Necrons", "unit#1", anchor_id="anchor_x"
    )
    assert session["ability_use_anchors"]["Necrons"]["ability.a"] == {
        "anchor_id": "anchor_x",
        "unit_key": "unit#1",
    }


def test_spend_ability_with_anchor_id_and_no_unit_key() -> None:
    session = _ability_session()
    common.spend_ability(_reactive_ability(aid="ability.a"), "Necrons", anchor_id="anchor_x")
    assert session["ability_use_anchors"]["Necrons"]["ability.a"]["unit_key"] is None


def test_spend_ability_unresolved_unit_key_is_a_noop_for_effect_dispatch(monkeypatch) -> None:
    """An unresolvable unit_key must not crash spend_ability — the usage/anchor
    bookkeeping still happens, the effect dispatch is silently skipped (mirrors
    `_apply_stratagem_effect`'s "no-op for an unmatched unit_key" contract)."""
    session = _ability_session()

    def _raise(faction: str, uid: str):  # type: ignore[no-untyped-def]
        raise KeyError(uid)

    monkeypatch.setattr(common, "lookup", _raise)
    common.spend_ability(_reactive_ability(aid="ability.a"), "Necrons", "gone#1")
    assert "ability.a" in session["used_ability_ids"]["Necrons"]


def test_ability_use_anchor_returns_none_when_never_spent() -> None:
    _ability_session()
    assert common.ability_use_anchor("Necrons", "ability.never") is None


def test_ability_use_anchor_returns_recorded_tuple() -> None:
    _ability_session()
    common.spend_ability(
        _reactive_ability(aid="ability.a"), "Necrons", "unit#1", anchor_id="anchor_x"
    )
    assert common.ability_use_anchor("Necrons", "ability.a") == ("anchor_x", "unit#1")


def test_ability_used_here_true_for_matching_anchor() -> None:
    _ability_session()
    common.spend_ability(_reactive_ability(aid="ability.a"), "Necrons", anchor_id="anchor_x")
    assert common.ability_used_here("Necrons", "ability.a", "anchor_x") is True


def test_ability_used_here_false_for_different_anchor() -> None:
    _ability_session()
    common.spend_ability(_reactive_ability(aid="ability.a"), "Necrons", anchor_id="anchor_x")
    assert common.ability_used_here("Necrons", "ability.a", "anchor_y") is False


def test_ability_used_here_scoped_per_player_not_globally() -> None:
    _ability_session()
    common.spend_ability(
        _reactive_ability(aid="ability.shared"), "Necrons", anchor_id="necron_anchor"
    )
    common.spend_ability(_reactive_ability(aid="ability.shared"), "Orks", anchor_id="ork_anchor")
    assert common.ability_used_here("Necrons", "ability.shared", "necron_anchor") is True
    assert common.ability_used_here("Orks", "ability.shared", "necron_anchor") is False
    assert common.ability_used_here("Orks", "ability.shared", "ork_anchor") is True


def test_undo_ability_removes_used_mark_and_anchor() -> None:
    session = _ability_session()
    common.spend_ability(_reactive_ability(aid="ability.a"), "Necrons", anchor_id="anchor_x")
    common.undo_ability(_reactive_ability(aid="ability.a"), "Necrons")
    assert "ability.a" not in session["used_ability_ids"].get("Necrons", set())
    assert common.ability_use_anchor("Necrons", "ability.a") is None


def test_undo_ability_without_prior_spend_is_a_noop() -> None:
    _ability_session()
    common.undo_ability(_reactive_ability(aid="ability.never_spent"), "Necrons")  # no crash


def test_ability_used_elsewhere_unit_name_resolves_recorded_units_display_name(monkeypatch) -> None:
    _ability_session()
    common.spend_ability(
        _reactive_ability(aid="ability.a"), "Necrons", "warrior#1", anchor_id="anchor_x"
    )
    warriors = SimpleNamespace(name_en="Necron Warriors")
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (warriors, {}))
    assert common.ability_used_elsewhere_unit_name("Necrons", "ability.a") == "Necron Warriors"


def test_ability_used_elsewhere_unit_name_none_when_never_spent() -> None:
    _ability_session()
    assert common.ability_used_elsewhere_unit_name("Necrons", "ability.never") is None


def test_ability_used_elsewhere_unit_name_none_when_spent_without_unit_key() -> None:
    _ability_session()
    common.spend_ability(_reactive_ability(aid="ability.a"), "Necrons", anchor_id="anchor_x")
    assert common.ability_used_elsewhere_unit_name("Necrons", "ability.a") is None


def test_ability_used_elsewhere_unit_name_none_when_recorded_key_unresolvable(monkeypatch) -> None:
    _ability_session()
    common.spend_ability(
        _reactive_ability(aid="ability.a"), "Necrons", "gone#1", anchor_id="anchor_x"
    )

    def _raise(faction: str, uid: str):  # type: ignore[no-untyped-def]
        raise KeyError(uid)

    monkeypatch.setattr(common, "lookup", _raise)
    assert common.ability_used_elsewhere_unit_name("Necrons", "ability.a") is None


# ---------------------------------------------------------------------------
# B-028a acceptance test: an EXISTING dispatch (heal) running through the NEW
# spend_ability() path — the Durchstich the backlog item asks for.
# ---------------------------------------------------------------------------


def test_spend_ability_heal_dispatch_runs_through_new_path(monkeypatch) -> None:
    session = _SS(
        first_player="Necrons",
        used_ability_ids={},
        ability_use_anchors={},
        p1_units={
            "unit#1": {
                "current_wounds": 3,
                "models": 1,
                "destroyed": False,
                "lost_models_this_turn": 0,
            }
        },
    )
    common.st.session_state = session
    _gs.st.session_state = session
    _um.st.session_state = session
    _eng.st.session_state = session

    unit = SimpleNamespace(id="unit", wounds=6, models_max=3)  # "unit#1" strips to "unit"
    monkeypatch.setattr(common, "units_list_for", lambda faction: [unit])

    heal_ability = _reactive_ability(
        aid="test.reactive_heal",
        name="Test Reactive Heal",
        phase="any",
        event="model_destroyed",
        effect=Effect(type="heal", target="self", amount="2"),
    )

    common.spend_ability(heal_ability, "Necrons", "unit#1")

    assert session["p1_units"]["unit#1"]["current_wounds"] == 5  # 3 + 2 healed
    assert "test.reactive_heal" in session["used_ability_ids"]["Necrons"]


# ---------------------------------------------------------------------------
# B-028b — Noctilith Beacons (real necrons/unit_abilities.yaml data): the
# first productive callsite of the B-028a infrastructure (deny_psychic has no
# _EFFECT_HANDLERS dispatch — spend_ability's usage/anchor bookkeeping is the
# whole contract here). Full-undo guarantee (design_system.md §6.1).
# ---------------------------------------------------------------------------


def test_spend_undo_ability_noctilith_beacons_real_data_round_trip() -> None:
    session = _ability_session()
    ability = next(
        a
        for a in _eng.load_unit_abilities("necrons")
        if a.id == "wh40k_9e.necrons.unit.the_silent_king.noctilith_beacons"
    )
    assert ability.effect.type == "deny_psychic"
    uid = "wh40k_9e.necrons.unit.the_silent_king"

    common.spend_ability(ability, "Necrons", uid, anchor_id="deny_ability_szarekh")
    assert ability.id in session["used_ability_ids"]["Necrons"]
    assert common.ability_use_anchor("Necrons", ability.id) == ("deny_ability_szarekh", uid)
    assert common.ability_used_here("Necrons", ability.id, "deny_ability_szarekh") is True

    common.undo_ability(ability, "Necrons")
    assert ability.id not in session["used_ability_ids"].get("Necrons", set())
    assert common.ability_use_anchor("Necrons", ability.id) is None


# ---------------------------------------------------------------------------
# B-028a — render_reactive_ability_box(): state/target_name/on_use/on_undo wiring
# ---------------------------------------------------------------------------


def _reactive_ability_box_session(**extra) -> _SS:  # type: ignore[no-untyped-def]
    base = dict(
        active="Necrons",
        used_ability_ids={},
        ability_use_anchors={},
    )
    base.update(extra)
    return _SS(**base)


def _install_reactive_ability_session(monkeypatch, session):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(common.st, "session_state", session)
    captured: list[dict] = []  # type: ignore[type-arg]
    monkeypatch.setattr(common, "render_go_card", lambda **kwargs: captured.append(kwargs))
    return captured


def test_reactive_ability_box_shown_when_window_open_and_conditions_empty(monkeypatch) -> None:
    """No unit_key given, no conditions declared -> still renders "ready" (mirrors
    stratagem_conditions_met: an empty conditions list needs no unit)."""
    session = _reactive_ability_box_session()
    captured = _install_reactive_ability_session(monkeypatch, session)
    ability = _reactive_ability()

    common.render_reactive_ability_box(
        "Necrons",
        phase="fight",
        event="model_destroyed",
        abilities=[ability],
        decline_key="unit-uid-1",
        context_caption="Unit was destroyed.",
    )

    assert len(captured) == 1
    assert captured[0]["name"] == "Test Reactive Ability"
    assert captured[0]["cp_cost"] == 0
    assert captured[0]["state"] == "ready"


def test_reactive_ability_box_hidden_for_wrong_event(monkeypatch) -> None:
    session = _reactive_ability_box_session()
    captured = _install_reactive_ability_session(monkeypatch, session)
    ability = _reactive_ability(event="after_unit_fights")

    common.render_reactive_ability_box(
        "Necrons",
        phase="fight",
        event="model_destroyed",
        abilities=[ability],
        decline_key="unit-uid-1",
        context_caption="irrelevant",
    )

    assert captured == []


def test_reactive_ability_box_hidden_when_conditions_not_met_without_unit(monkeypatch) -> None:
    """A non-empty conditions list with no unit_key given stays hidden (fail-safe,
    mirrors the Stratagem version's "hidden without an explicit unit")."""
    session = _reactive_ability_box_session()
    captured = _install_reactive_ability_session(monkeypatch, session)
    ability = _reactive_ability(conditions=[Condition(has_rules=["someRule"])])

    common.render_reactive_ability_box(
        "Necrons",
        phase="fight",
        event="model_destroyed",
        abilities=[ability],
        decline_key="unit-uid-1",
        context_caption="irrelevant",
    )

    assert captured == []


def test_reactive_ability_box_target_name_shows_unit(monkeypatch) -> None:
    session = _reactive_ability_box_session()
    captured = _install_reactive_ability_session(monkeypatch, session)
    unit = SimpleNamespace(name_en="Canoptek Plasmacyte")
    monkeypatch.setattr(common, "lookup", lambda faction, uid: (unit, {}))
    ability = _reactive_ability()

    common.render_reactive_ability_box(
        "Necrons",
        phase="fight",
        event="model_destroyed",
        abilities=[ability],
        decline_key="unit-uid-1",
        context_caption="irrelevant",
        unit_key="unit#1",
    )

    assert "Canoptek Plasmacyte" in captured[0]["target_name"]


def test_reactive_ability_box_use_action_spends_and_marks_used(monkeypatch) -> None:
    session = _reactive_ability_box_session()
    captured = _install_reactive_ability_session(monkeypatch, session)
    ability = _reactive_ability(aid="ability.a")

    common.render_reactive_ability_box(
        "Necrons",
        phase="fight",
        event="model_destroyed",
        abilities=[ability],
        decline_key="unit-uid-1",
        context_caption="irrelevant",
    )
    captured[0]["on_use"]()

    assert "ability.a" in session["used_ability_ids"]["Necrons"]


def test_reactive_ability_box_used_at_this_anchor_offers_undo(monkeypatch) -> None:
    session = _reactive_ability_box_session()
    captured = _install_reactive_ability_session(monkeypatch, session)
    ability = _reactive_ability(aid="ability.a")

    common.render_reactive_ability_box(
        "Necrons",
        phase="fight",
        event="model_destroyed",
        abilities=[ability],
        decline_key="unit-uid-1",
        context_caption="irrelevant",
    )
    captured[0]["on_use"]()
    captured.clear()

    common.render_reactive_ability_box(
        "Necrons",
        phase="fight",
        event="model_destroyed",
        abilities=[ability],
        decline_key="unit-uid-1",
        context_caption="irrelevant",
    )

    assert captured[0]["state"] == "used"
    captured[0]["on_undo"]()
    assert "ability.a" not in session["used_ability_ids"].get("Necrons", set())


def test_reactive_ability_box_used_elsewhere_at_different_anchor(monkeypatch) -> None:
    session = _reactive_ability_box_session()
    captured = _install_reactive_ability_session(monkeypatch, session)
    ability = _reactive_ability(aid="ability.a")

    common.render_reactive_ability_box(
        "Necrons",
        phase="fight",
        event="model_destroyed",
        abilities=[ability],
        decline_key="unit-uid-1",
        context_caption="irrelevant",
    )
    captured[0]["on_use"]()
    captured.clear()

    common.render_reactive_ability_box(
        "Necrons",
        phase="fight",
        event="model_destroyed",
        abilities=[ability],
        decline_key="unit-uid-DIFFERENT",
        context_caption="irrelevant",
    )

    assert captured[0]["state"] == "used_elsewhere"


def test_reactive_ability_box_active_player_gate(monkeypatch) -> None:
    """trigger.player="active" only surfaces for the currently active faction."""
    session = _reactive_ability_box_session(active="Orks")
    captured = _install_reactive_ability_session(monkeypatch, session)
    ability = _reactive_ability(player="active")

    common.render_reactive_ability_box(
        "Necrons",
        phase="fight",
        event="model_destroyed",
        abilities=[ability],
        decline_key="unit-uid-1",
        context_caption="irrelevant",
    )

    assert captured == []
