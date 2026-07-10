"""Tests for state_badges_html() and _parse_strength()."""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.ability_engine as _eng  # noqa: E402
import gameMechanic.game_state as _gs  # noqa: E402
import gameMechanic.unit_mutations as _um  # noqa: E402
import uiLayout._common as common  # noqa: E402
from gameMechanic.ability_engine import (  # noqa: E402
    get_active_round_choice_light_cover_if_stationary,
)
from gameObjects.ability import Effect  # noqa: E402
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
    monkeypatch.setattr(
        "gameMechanic.game_state.unit_id_from_state_key", lambda uid: "missing.unit"
    )
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
    because ability_engine, game_state, and _common each hold their own imported ``st``
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

    Structural check of the ``affects`` list the hint builder reads. The actual display
    behaviour (text content, visibility only for an active aura_range_bonus directive) is
    covered by the Streamlit-free ability_engine tests
    (``test_build_aura_range_hint_text_*``) — this test just guards the YAML contract.
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
    """Point common/game_state/unit_mutations at the SAME session_state (see
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
    )
    captured[0]["on_use"]()

    assert session["cp"]["Necrons"] == 4  # 5 - 1 CP
    assert "wh40k_9e.shared.stratagem.fire_overwatch" in session["used_stratagem_ids"]["Necrons"]


def test_used_this_phase_offers_undo_within_window(monkeypatch) -> None:
    """S134 task 2b: while this phase's activation window is still open
    (`stratagem_undo_visible`), a spent reactive GO renders "used" with the
    full-rollback Undo wired — pressing it restores CP and clears the usage
    marker, the same canonical `undo_stratagem` path the central list uses.
    The CP-safety guarantee the old "locked" mapping protected still holds:
    in the "used" state the one action slot is Undo, not Use, so the
    stratagem can never be spent twice in one phase."""
    session = _reactive_box_session(
        cp={"Necrons": 4},
        used_stratagem_ids={"Necrons": {"wh40k_9e.shared.stratagem.fire_overwatch"}},
    )
    captured = _install_reactive_box_session(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-2",
        context_caption="irrelevant",
    )

    assert captured[0]["state"] == "used"
    assert captured[0]["locked_reason"] is None

    captured[0]["on_undo"]()

    assert session["cp"]["Necrons"] == 5
    assert (
        "wh40k_9e.shared.stratagem.fire_overwatch" not in session["used_stratagem_ids"]["Necrons"]
    )


def test_cp_insufficient_shows_locked_card_with_cp_reason(monkeypatch) -> None:
    session = _reactive_box_session(cp={"Necrons": 0})
    captured = _install_reactive_box_session(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-1",
        context_caption="irrelevant",
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


def _unit_with_keywords(*keywords: str):  # type: ignore[no-untyped-def]
    return SimpleNamespace(has_keyword=lambda kw: kw in keywords)


def test_shadows_of_drazak_shown_at_hit_anchor_for_matching_unit(monkeypatch) -> None:
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    flayed_ones = _unit_with_keywords("FLAYED ONES")

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
    flayed_ones = _unit_with_keywords("FLAYED ONES")

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


def test_whirling_onslaught_shown_at_wound_anchor_for_matching_unit(monkeypatch) -> None:
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    destroyer = _unit_with_keywords("DESTROYER CULT")

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="shooting",
        event="on_target",
        decline_key="tab-1",
        context_caption="irrelevant",
        unit_for_conditions=destroyer,
        effect_type="debuff_roll",
        effect_stat="wound",
    )

    assert any(c["name"] == "Whirling Onslaught" for c in captured)


def test_whirling_onslaught_absent_at_hit_anchor(monkeypatch) -> None:
    session = _reactive_box_session()
    captured = _install_reactive_box_session(monkeypatch, session)
    destroyer = _unit_with_keywords("DESTROYER CULT")

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
    flayed_ones = _unit_with_keywords("FLAYED ONES")

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
    shielded = _unit_with_keywords("QUANTUM SHIELDING")

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
    shielded = _unit_with_keywords("QUANTUM SHIELDING")

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
    shielded = _unit_with_keywords("QUANTUM SHIELDING")

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
# (mirrors ability_engine.ability_invuln_save's "lowest value wins" semantics
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
# (Option c — Pull, not Push): unlike render_reactive_stratagem_box's Use/Pass
# dialog, this is a single button with NO greyed-out state — it is fully
# absent once CP is short or already spent this phase, real _shared stratagem
# data (command_re_roll, event=after_roll) end-to-end via _reactive_box_session.
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
    assert reopened == [1]
    assert rerun_calls == [1]


def test_command_reroll_hidden_when_cp_zero(monkeypatch) -> None:
    session = _reactive_box_session(cp={"Necrons": 0})
    button_calls, _ = _reroll_widgets(monkeypatch, session)

    common.render_inline_command_reroll(
        "Necrons", "charge", reopen_key="t1", on_reroll=lambda: None
    )

    assert button_calls == []


def test_command_reroll_hidden_after_already_used_this_phase(monkeypatch) -> None:
    session = _reactive_box_session(used_stratagem_ids={"Necrons": {_COMMAND_REROLL_ID}})
    button_calls, _ = _reroll_widgets(monkeypatch, session)

    common.render_inline_command_reroll(
        "Necrons", "charge", reopen_key="t1", on_reroll=lambda: None
    )

    assert button_calls == []


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
