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
import uiLayout._common as common  # noqa: E402
from gameMechanic.ability_engine import (  # noqa: E402
    get_active_round_choice_light_cover_if_stationary,
)
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
