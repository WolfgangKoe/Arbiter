"""Tests for dice_html miss-marker rendering (Finding 9.1).

Misses must read as a die-shaped icon everywhere — never a bare text '×'.
The miss die draws its cross as two SVG <line> strokes in #c0392b.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from uiLayout.dice_html import (  # noqa: E402
    _modifier_color,
    _modifier_columns,
    always_fail_marker_row_html,
    dice_row_html,
    miss_die_html,
    reroll_marker_row_html,
    save_modifier_die_pair_html,
)

_BUFF_GREEN = "#4a9a5a"
_DEBUFF_RED = "#ef4444"

_CROSS_STROKE = "#c0392b"  # the × drawn inside a miss die


def test_miss_die_is_an_svg_not_a_text_cross() -> None:
    html = miss_die_html()
    assert "<svg" in html
    assert _CROSS_STROKE in html
    assert "×" not in html


def test_impossible_threshold_uses_miss_die_not_text_cross() -> None:
    # Threshold > 6 (e.g. modified to 7+): all dice fail, marker right of the 6.
    html = dice_row_html(7)
    assert "×" not in html
    assert html.count("<svg") == 7  # six failed dice + the miss-die marker


def test_save_modifier_past_six_uses_miss_die_not_text_cross() -> None:
    # Sv 6+ with AP-4 → newly-failing value 9 cannot be shown by a real die.
    html = save_modifier_die_pair_html(6, -4, "AP-4", "#ef4444")
    assert "×" not in html
    assert _CROSS_STROKE in html


def test_buff_arrow_points_right() -> None:
    # Cover +2 on Sv 5+ → eff. 3+: the success window widens, arrow points right
    # (lower rolls now suffice). Regression for the Plan 022 arrow-direction fix.
    html = save_modifier_die_pair_html(5, 2, "Cover", "#4a9a5a")
    assert "→" in html
    assert "←" not in html


def test_debuff_arrow_points_left() -> None:
    # AP-3 on Sv 3+ → eff. 6+: the save worsens, higher rolls are needed, arrow
    # points left. Regression for the Plan 022 arrow-direction fix.
    html = save_modifier_die_pair_html(3, -3, "AP-3", "#ef4444")
    assert "←" in html
    assert "→" not in html


def test_long_badge_does_not_overflow() -> None:
    # A long weapon label ("Power Klaw …") must be clipped with an ellipsis inside
    # the badge column, never spill into dice slot 1. Plan 022 Step 2.
    html = save_modifier_die_pair_html(3, -1, "Power Klaw Extra Long Label", _DEBUFF_RED)
    assert "text-overflow:ellipsis" in html
    assert "overflow:hidden" in html
    assert "max-width:" in html


def test_color_hint_overrides_value_sign() -> None:
    # Quantum Shield from the defender's view: value is negative, but it benefits
    # the defender → explicit color_hint='buff' must win over the sign. Plan 022 Step 3.
    assert _modifier_color({"value": -1, "color_hint": "buff"}) == _BUFF_GREEN
    assert _modifier_color({"value": 1, "color_hint": "debuff"}) == _DEBUFF_RED


def test_color_without_hint_falls_back_to_value_sign() -> None:
    # Backward compatibility: dicts without color_hint keep the sign-based colour.
    assert _modifier_color({"value": 2}) == _BUFF_GREEN
    assert _modifier_color({"value": -2}) == _DEBUFF_RED


def test_slot_1_always_shows_x() -> None:
    # Invariant (dice_display.md §1): an unmodified 1 always fails — for every
    # threshold the value-1 die is drawn as a miss cross, never a success die.
    for threshold in range(2, 7):
        html = dice_row_html(threshold)
        assert _CROSS_STROKE in html


def test_buff_cannot_make_1_succeed() -> None:
    # Even at the lowest reachable threshold (2+, after any buff), the 1 stays a
    # miss die outside the success frame (dice_display.md §3.3).
    html = dice_row_html(2)
    assert _CROSS_STROKE in html  # the value-1 miss die is still rendered


def test_debuff_beyond_6_shows_x_slot() -> None:
    # Sv 6+ with AP-2 → newly-failing value 7 is off-scale → a miss die marks it
    # right of the 6 (dice_display.md §3.2 / §10.4).
    html = save_modifier_die_pair_html(6, -2, "AP-2", _DEBUFF_RED)
    assert _CROSS_STROKE in html
    assert "×" not in html  # off-scale miss reads as a die, never a bare text ×


def test_reroll_marker_correct_slot() -> None:
    # ↺ sits under exactly the re-rolled slot(s) (dice_display.md §10.1).
    html = reroll_marker_row_html([1])
    assert html.count("↺") == 1


def test_always_fail_marks_correct_slots() -> None:
    # Quantum Shield (attacker view): slots 1–3 always fail → three ✕ markers in red.
    html = always_fail_marker_row_html([1, 2, 3], color_hint="debuff")
    assert html.count("✕") == 3
    assert _DEBUFF_RED in html


def test_always_fail_color_hint_buff_is_green() -> None:
    # Defender's perspective: the same auto-fail is a benefit → green (§5.1).
    html = always_fail_marker_row_html([1, 2, 3], color_hint="buff")
    assert _BUFF_GREEN in html


def test_modifier_columns_clamp_to_grid() -> None:
    # AP-3 on Sv 4+: from 3 (last old-fail) to 6 (best roll now fails) — 3 columns.
    assert _modifier_columns(3, 6) == (3, 6)
    # Cover +1 on Sv 4+: from 3 to 4 — adjacent columns.
    assert _modifier_columns(3, 4) == (3, 4)


def test_modifier_columns_off_scale_anchors_right_at_six() -> None:
    # Worsened past 6 → right marker pinned to column 6 (miss die appended by renderer).
    assert _modifier_columns(3, 9, right_off_scale=True) == (3, 6)
