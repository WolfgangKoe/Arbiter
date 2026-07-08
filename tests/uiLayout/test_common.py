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


class _FakeCtx:
    """No-op context manager stand-in for st.container()/st.expander()/columns()."""

    def __enter__(self):  # type: ignore[no-untyped-def]
        return self

    def __exit__(self, *exc):  # type: ignore[no-untyped-def]
        return False


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
        reactive_declined=set(),
    )
    base.update(extra)
    return _SS(**base)


def _install_reactive_box_widgets(monkeypatch, session, clicked_key: str | None = None):  # type: ignore[no-untyped-def]
    """Patch the shared streamlit mock's widget surface for one render call.

    `common.st`, `game_state.st`, and `unit_mutations.st` are all the SAME
    MagicMock object (all three modules did `import streamlit as st` against
    the identical `sys.modules["streamlit"]` stand-in) — patching attributes
    on it (via monkeypatch, auto-restored after the test) makes `spend_stratagem`
    → `adjust_cp` see the same session as `render_reactive_stratagem_box` itself,
    instead of a stale `session_state` left over from an earlier test.
    """
    markdown_calls: list[str] = []
    rerun_calls: list[int] = []
    monkeypatch.setattr(common.st, "session_state", session)
    monkeypatch.setattr(_gs.st, "session_state", session)
    monkeypatch.setattr(_um.st, "session_state", session)
    monkeypatch.setattr(common.st, "markdown", lambda text, **kw: markdown_calls.append(text))
    monkeypatch.setattr(common.st, "caption", lambda text, **kw: None)
    monkeypatch.setattr(common.st, "container", lambda **kw: _FakeCtx())
    monkeypatch.setattr(common.st, "expander", lambda *a, **kw: _FakeCtx())
    monkeypatch.setattr(common.st, "columns", lambda n: tuple(_FakeCtx() for _ in range(n)))
    monkeypatch.setattr(common.st, "button", lambda label, key=None, **kw: key == clicked_key)
    monkeypatch.setattr(common.st, "rerun", lambda: rerun_calls.append(1))
    return markdown_calls, rerun_calls


def test_fire_overwatch_box_shown_when_window_open_for_defender(monkeypatch) -> None:
    """Real shared-data end-to-end check: Fire Overwatch (player=inactive) surfaces
    in the target's own column while the Charge reactive window is open."""
    session = _reactive_box_session()
    markdown_calls, _ = _install_reactive_box_widgets(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-1",
        context_caption="Warriors were declared a charge target.",
    )

    combined = "\n".join(markdown_calls)
    assert "Fire Overwatch" in combined


def test_fire_overwatch_box_hidden_for_active_player_column(monkeypatch) -> None:
    """player=inactive: the charging (active) player's own column must not see it."""
    session = _reactive_box_session(active="Necrons")  # Necrons is now the charger
    markdown_calls, _ = _install_reactive_box_widgets(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-1",
        context_caption="irrelevant",
    )

    combined = "\n".join(markdown_calls)
    assert "Fire Overwatch" not in combined


def test_use_button_spends_cp_marks_used_and_reruns(monkeypatch) -> None:
    session = _reactive_box_session()
    use_key = (
        "reactive_use_Necrons:on_declaration:wh40k_9e.shared.stratagem.fire_overwatch:target-uid-1"
    )
    _, rerun_calls = _install_reactive_box_widgets(monkeypatch, session, clicked_key=use_key)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-1",
        context_caption="irrelevant",
    )

    assert session["cp"]["Necrons"] == 4  # 5 - 1 CP
    assert "wh40k_9e.shared.stratagem.fire_overwatch" in session["used_stratagem_ids"]["Necrons"]
    assert rerun_calls == [1]


def test_pass_button_declines_without_spending_cp(monkeypatch) -> None:
    session = _reactive_box_session()
    pass_key = (
        "reactive_pass_Necrons:on_declaration:wh40k_9e.shared.stratagem.fire_overwatch:target-uid-1"
    )
    _, rerun_calls = _install_reactive_box_widgets(monkeypatch, session, clicked_key=pass_key)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-1",
        context_caption="irrelevant",
    )

    assert session["cp"]["Necrons"] == 5  # untouched
    assert (
        "Necrons:on_declaration:wh40k_9e.shared.stratagem.fire_overwatch:target-uid-1"
        in session["reactive_declined"]
    )
    assert rerun_calls == [1]


def test_declined_occurrence_does_not_reappear(monkeypatch) -> None:
    """A previously-passed occurrence (same decline_key) stays suppressed."""
    session = _reactive_box_session(
        reactive_declined={
            "Necrons:on_declaration:wh40k_9e.shared.stratagem.fire_overwatch:target-uid-1"
        }
    )
    markdown_calls, _ = _install_reactive_box_widgets(monkeypatch, session)

    common.render_reactive_stratagem_box(
        "Necrons",
        phase="charge",
        event="on_declaration",
        decline_key="target-uid-1",
        context_caption="irrelevant",
    )

    combined = "\n".join(markdown_calls)
    assert "Fire Overwatch" not in combined


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
