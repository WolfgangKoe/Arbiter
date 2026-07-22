"""Tests for diceHtml miss-marker rendering (Finding 9.1).

Misses must read as a die-shaped icon everywhere — never a bare text '×'.
The miss die draws its cross as two SVG <line> strokes in #c0392b.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.modules["streamlit"] = MagicMock()
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from uiLayout import diceHtml as dice_html_module  # noqa: E402
from uiLayout.diceCompose import (  # noqa: E402
    _modifier_color,
    _modifier_columns,
    _reroll_die_svg,
    always_fail_marker_row_html,
    block_divider_html,
    dice_face_svg,
    dice_row_html,
    go_source_chip,
    light_cover_label,
    miss_die_html,
    modifier_die_pair_html,
    reroll_marker_row_html,
    save_ap_modifier_row_html,
    save_modifier_die_pair_html,
    special_die_html,
    threshold_header_html,
    value_triggered_die_row_html,
)
from uiLayout.diceHtml import _capped_modifier_threshold  # noqa: E402

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


# --- Pfeil-Magnitude (spec §2.1: Debuff "←N", Buff "+N→") ---------------------


def test_multi_step_debuff_arrow_carries_magnitude() -> None:
    # AP-2 on Sv 3+ spans two columns → arrowhead labelled "←2", not a bare "←".
    html = save_modifier_die_pair_html(3, -2, "AP-2", _DEBUFF_RED)
    assert "←2" in html


def test_multi_step_buff_arrow_carries_magnitude() -> None:
    # Cover +2 on Sv 5+ spans two columns → arrowhead labelled "+2→".
    html = save_modifier_die_pair_html(5, 2, "Cover", _BUFF_GREEN)
    assert "+2→" in html


def test_single_step_debuff_magnitude_rides_in_boundary_gap() -> None:
    # A 1-column shift has no slot between the dice; "←1" must still appear (§3.1).
    html = save_modifier_die_pair_html(3, -1, "AP-1", _DEBUFF_RED)
    assert "←1" in html


def test_single_step_buff_magnitude_rides_in_boundary_gap() -> None:
    html = save_modifier_die_pair_html(5, 1, "Cover", _BUFF_GREEN)
    assert "+1→" in html


def test_off_scale_debuff_arrow_carries_magnitude() -> None:
    # Sv 6+ with AP-4 pushes the save past 6 → label still reports the true shift.
    html = save_modifier_die_pair_html(6, -4, "AP-4", _DEBUFF_RED)
    assert "←4" in html


def test_hit_debuff_arrow_carries_magnitude() -> None:
    # HIT/WOUND rows also carry the number (geometry width is tracked separately).
    html = modifier_die_pair_html(3, 5, "X", -2, _DEBUFF_RED, base_threshold=3)
    assert "←2" in html


def test_buff_magnitude_uses_buff_colour_not_context_grey() -> None:
    # The numbered arrow is the modifier's colour (green), never the grey context die.
    html = save_modifier_die_pair_html(5, 2, "Cover", _BUFF_GREEN)
    assert f'color:{_BUFF_GREEN};font-weight:bold;">+2→' in html


def test_long_badge_does_not_overflow() -> None:
    # A long weapon label ("Power Klaw …") must be clipped with an ellipsis inside
    # the badge column, never spill into dice slot 1. Plan 022 Step 2.
    html = save_modifier_die_pair_html(3, -1, "Power Klaw Extra Long Label", _DEBUFF_RED)
    assert "text-overflow:ellipsis" in html
    assert "overflow:hidden" in html
    assert "max-width:" in html


def test_badge_with_leading_value_label_is_not_doubled() -> None:
    # S138: a label that already leads with its signed value ("−1 to Hit",
    # weapon hit penalty / Fall-Back debuff) must render the badge text exactly
    # once — the generic value append would double it to "−1 to Hit -1"
    # (same doubling bug documented at save_ap_modifier_row_html).
    html = modifier_die_pair_html(3, 4, "−1 to Hit", -1, _DEBUFF_RED, base_threshold=3)
    assert "−1 to Hit</span>" in html
    assert "−1 to Hit -1" not in html


def test_badge_without_leading_value_still_appends_value() -> None:
    # Name-only labels (AP/Cover convention) keep the appended signed value.
    html = modifier_die_pair_html(3, 4, "Dense Cover", -1, _DEBUFF_RED, base_threshold=3)
    assert "Dense Cover -1" in html


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
    # Quantum Shield (attacker view): slots 1–3 always fail → three die-shaped
    # miss markers (S160/B-104-Re-Fix: SVG, not the '✕' text glyph) in red.
    html = always_fail_marker_row_html([1, 2, 3], color_hint="debuff", label="Quantum Shielding")
    assert html.count("<svg") == 3
    assert "✕" not in html
    assert _DEBUFF_RED in html


def test_always_fail_color_hint_buff_is_green() -> None:
    # Defender's perspective: the same auto-fail is a benefit → green (§5.1).
    html = always_fail_marker_row_html([1, 2, 3], color_hint="buff", label="Quantum Shielding")
    assert _BUFF_GREEN in html


def test_always_fail_requires_caller_supplied_label() -> None:
    # B-109: no generic "Auto-fail" fallback — a blank label is a caller bug,
    # rejected loudly instead of rendering silently with placeholder text.
    with pytest.raises(ValueError, match="non-empty label"):
        always_fail_marker_row_html([1, 2, 3], color_hint="debuff", label="")


def test_always_fail_label_uses_ability_name() -> None:
    # B-103: badge shows the triggering ability's own name, not a generic text.
    html = always_fail_marker_row_html([1, 2, 3], color_hint="debuff", label="Quantum Shielding")
    assert "Quantum Shielding" in html
    assert "Auto-fail" not in html


def test_always_fail_marker_renders_as_die_chip_not_bare_span() -> None:
    # S160 (B-104-Re-Fix): the auto-fail marker is now the real miss-die SVG
    # (dice_face_svg family, design_system.md §4.2/§4.3) — neither the bare
    # `<span>✕</span>` text glyph nor the earlier text-chip box.
    html = always_fail_marker_row_html([1], color_hint="debuff", label="Quantum Shielding")
    assert f'<span style="color:{_DEBUFF_RED};font-weight:bold;">✕</span>' not in html
    assert "<svg" in html
    assert f'stroke="{_DEBUFF_RED}" stroke-width="1.5"' in html


def test_badge_chip_title_carries_full_label_alongside_truncation() -> None:
    # B-111 Variante C: "Quantum Shielding" is long enough to be visually clipped
    # by the badge column's ellipsis, but the full text must survive as a hover
    # tooltip via the `title` attribute — truncation stays, nothing is lost.
    # S160: the marker itself is now the SVG miss-die (stroke, not CSS border).
    html = always_fail_marker_row_html([1, 2, 3], color_hint="debuff", label="Quantum Shielding")
    assert 'title="Quantum Shielding"' in html
    assert "text-overflow:ellipsis" in html
    assert ">Quantum Shielding<" in html
    assert f'stroke="{_DEBUFF_RED}" stroke-width="1.5"' in html
    assert "<svg" in html


def test_reroll_marker_renders_as_die_chip_not_bare_span() -> None:
    # S160/B-104-Re-Fix: design_system.md §4.3 assigns Reroll to the SVG-Würfel-
    # fläche family too (not the text-chip family) — same shared _marker_row_html
    # helper, same 32x32 die box, reroll-orange border via the SVG stroke.
    html = reroll_marker_row_html([1])
    assert "<svg" in html
    assert 'stroke="#f59e0b" stroke-width="1.5"' in html


def test_modifier_columns_clamp_to_grid() -> None:
    # AP-3 on Sv 4+: from 3 (last old-fail) to 6 (best roll now fails) — 3 columns.
    assert _modifier_columns(3, 6) == (3, 6)
    # Cover +1 on Sv 4+: from 3 to 4 — adjacent columns.
    assert _modifier_columns(3, 4) == (3, 4)


def test_modifier_columns_off_scale_anchors_right_at_six() -> None:
    # Worsened past 6 → right marker pinned to column 6 (miss die appended by renderer).
    assert _modifier_columns(3, 9, right_off_scale=True) == (3, 6)


# ---------------------------------------------------------------------------
# BUG 2 — AP badge shows the value twice ("AP-4 -4")
# ---------------------------------------------------------------------------


def test_save_ap_row_shows_value_once() -> None:
    """save_ap_modifier_row_html must render 'AP -4' in the badge, not 'AP-4 -4'."""
    html = save_ap_modifier_row_html(3, -4)
    assert "AP -4" in html
    assert "AP-4 -4" not in html


def test_ap_modifier_row_label_not_doubled() -> None:
    """The signed value must appear exactly once — no '-4 -4' substring."""
    html = save_ap_modifier_row_html(3, -4)
    assert "-4 -4" not in html


def test_save_ap_row_is_debuff_red() -> None:
    """AP modifier badge must use the debuff red colour."""
    html = save_ap_modifier_row_html(3, -4)
    assert _DEBUFF_RED in html


# ---------------------------------------------------------------------------
# BUG 3 — buff badge is grey instead of green (Light Cover in SAVE block)
# ---------------------------------------------------------------------------


def test_save_cover_buff_badge_is_green() -> None:
    """Cover +1 buff badge must use buff green, not grey #6b7280."""
    html = save_modifier_die_pair_html(armour=3, value=1, label="Light Cover", color=_BUFF_GREEN)
    # The badge chip carrying the label must contain the green colour.
    assert _BUFF_GREEN in html
    # Grey (#6b7280) must NOT appear in the badge — it may appear for the grey die only
    # in parts not containing the label, but the key check is green is present in badge.
    # We verify by checking the badge chip directly uses green.
    badge_start = html.find("Light Cover")
    badge_context = html[max(0, badge_start - 200) : badge_start + 20]
    assert _BUFF_GREEN in badge_context


def test_save_ap_debuff_badge_is_red() -> None:
    """AP -2 debuff badge must use debuff red."""
    html = save_modifier_die_pair_html(armour=3, value=-2, label="AP", color=_DEBUFF_RED)
    badge_start = html.find("AP -2")
    badge_context = html[max(0, badge_start - 200) : badge_start + 20]
    assert _DEBUFF_RED in badge_context


def test_hit_buff_badge_still_green() -> None:
    """modifier_die_pair_html buff badge must remain green after badge_color change."""
    # Hit modifier: +1 to hit from 4+ → 3+.
    html = modifier_die_pair_html(4, 3, "Cover", 1, _BUFF_GREEN, base_threshold=4)
    badge_start = html.find("Cover +1")
    badge_context = html[max(0, badge_start - 200) : badge_start + 20]
    assert _BUFF_GREEN in badge_context


def test_hit_debuff_badge_is_red() -> None:
    """modifier_die_pair_html debuff badge must remain red after badge_color change."""
    html = modifier_die_pair_html(3, 5, "Penalty", -2, _DEBUFF_RED, base_threshold=3)
    badge_start = html.find("Penalty -2")
    badge_context = html[max(0, badge_start - 200) : badge_start + 20]
    assert _DEBUFF_RED in badge_context


# ---------------------------------------------------------------------------
# BACKFILL — diceCompose.py coverage (target ≥ 95%)
# ---------------------------------------------------------------------------


def test_threshold_header_boundary_gap_inserted() -> None:
    """threshold_header_html inserts the boundary-gap span before the threshold value."""
    # Threshold 4 → gap appears before the '4+' label (lines 51-52 in diceCompose.py).
    html = threshold_header_html(4)
    # Gap span is 34px wide; the highlighted label (threshold value) gets a border.
    assert "border:1px solid" in html
    # Labels 1+, 2+, 3+ appear before the highlighted 4+.
    assert html.index("1+") < html.index("4+")


def test_threshold_header_all_thresholds_render() -> None:
    """threshold_header_html works for thresholds 2–6, each producing a highlighted label."""
    for t in range(2, 7):
        html = threshold_header_html(t)
        assert f"{t}+" in html
        assert "border:1px solid" in html


def test_threshold_header_no_gap_below_two() -> None:
    """threshold_header_html at threshold 1 renders no boundary-gap slot."""
    html = threshold_header_html(1)
    # The boundary gap is only inserted when 2 <= threshold <= 6.
    # With threshold 1 there is no gap; all labels still appear.
    assert "1+" in html


def test_dice_row_threshold_one_or_less_no_miss_dice() -> None:
    """dice_row_html(1) — no separate miss section (line 122 branch), but the
    value-1 die inside the frame still shows the ×-miss marker (unmodified 1
    always fails — core_rules.txt), never a normal success pip.
    """
    html = dice_row_html(1)
    # No gap/boundary line because threshold <= 1.
    assert "margin-left:-5px" in html  # framed block still rendered
    # Value-1 die is inside the frame but rendered as the always-miss cross.
    assert "<svg" in html
    assert _CROSS_STROKE in html


def test_dice_row_natural_one_always_shows_miss_marker_even_in_success_frame() -> None:
    """Regression (S122/F3): threshold <= 1 used to draw the value-1 die as a normal
    success pip because range(threshold, 7) pulled it into the success frame. An
    unmodified roll of 1 always fails (Hit/Wound/Save, core_rules.txt), so it must
    render with the ×-miss cross even though it sits inside the colored success frame.
    """
    for threshold in (1, 0, -3):
        html = dice_row_html(threshold)
        assert _CROSS_STROKE in html, f"threshold={threshold} must show the miss cross for value 1"


def test_effective_save_row_floors_display_at_2_and_renders_green() -> None:
    """Regression (S122/F3, Variante A): the Eff. row in the SAVE block must floor
    its displayed threshold at 2+ (unmodified 1 always fails) and, per the normal
    threshold colour convention, render the floored 2 with the green frame.
    Sv 4+ with a +3 buff would compute 1+ unfloored; base row (4 → amber) and
    modifier row (buff green #4a9a5a) never emit #22c55e, so the green proves
    the Eff. row's frame colour.
    """
    dice_html_module.st.markdown.reset_mock()
    save = {
        "armour": 4,
        "armour_eff": 4,
        "invuln": None,
        "effective": 2,
        "using_invuln": False,
        "save_bonus": 3,
        "stack": [{"label": "Heavy Cover", "value": 3}],
    }
    dice_html_module._render_dice_save_block(save, ap=0)
    html = "".join(str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list)
    assert "Eff. 2+" in html
    assert "Eff. 1+" not in html
    assert "#22c55e" in html  # floored threshold 2 → green frame (threshold convention)


def test_save_modifier_row_natural_one_source_die_shows_miss_cross() -> None:
    """Regression (S122/F3, Variante A): when a save buff pushes the target below
    2+ (armour − value ≤ 1), the source die of the modifier mini-row stands for a
    natural 1 — which always fails — and must render as the ×-miss face.
    """
    html = save_modifier_die_pair_html(2, 1, "Heavy Cover", _BUFF_GREEN)
    assert _CROSS_STROKE in html  # [✕] +1→ [2]
    # Control: a buff that stays at 2+ or worse keeps the normal pip die.
    html_ok = save_modifier_die_pair_html(5, 2, "Cover", _BUFF_GREEN)
    assert _CROSS_STROKE not in html_ok


def test_block_divider_html_renders_hr() -> None:
    """block_divider_html must return an <hr> element (line 175 coverage)."""
    html = block_divider_html()
    assert "<hr" in html
    assert "border-top:1px solid" in html


def test_dice_face_svg_miss_default_output_byte_identical_to_pre_s160() -> None:
    """Regression (S160/B-104-Re-Fix): dice_face_svg(miss=True) without miss_color
    renders byte-identical HTML to the pre-refactor hard-coded #374151/#c0392b
    miss face — existing callers (dice_row_html, _aligned_modifier_row_html with
    left_miss=True) must not change visually.
    """
    assert dice_face_svg(1, miss=True) == (
        '<svg width="32" height="32" viewBox="0 0 32 32" '
        'style="display:inline-block;vertical-align:middle;margin:1px;">'
        '<rect x="1" y="1" width="30" height="30" rx="4" ry="4" '
        'fill="#111827" stroke="#374151" stroke-width="1.5"/>'
        '<line x1="9" y1="9" x2="23" y2="23" stroke="#c0392b" stroke-width="2.5"/>'
        '<line x1="23" y1="9" x2="9" y2="23" stroke="#c0392b" stroke-width="2.5"/></svg>'
    )
    assert dice_face_svg(3, miss=True) == (
        '<svg width="32" height="32" viewBox="0 0 32 32" '
        'style="display:inline-block;vertical-align:middle;margin:1px;">'
        '<rect x="1" y="1" width="30" height="30" rx="4" ry="4" '
        'fill="#111827" stroke="#374151" stroke-width="1.5"/>'
        '<circle cx="9" cy="9" r="2" fill="#374151"/>'
        '<circle cx="16" cy="16" r="2" fill="#374151"/>'
        '<circle cx="23" cy="23" r="2" fill="#374151"/></svg>'
    )


def test_miss_die_html_default_output_byte_identical_to_pre_s160() -> None:
    """Regression (S160/B-104-Re-Fix): miss_die_html() without a color argument
    renders byte-identical HTML to the pre-refactor version."""
    assert miss_die_html() == (
        '<svg width="32" height="32" viewBox="0 0 32 32" '
        'style="display:inline-block;vertical-align:middle;margin:1px;">'
        '<rect x="1" y="1" width="30" height="30" rx="4" ry="4" '
        'fill="#111827" stroke="#374151" stroke-width="1.5"/>'
        '<line x1="9" y1="9" x2="23" y2="23" stroke="#c0392b" stroke-width="2.5"/>'
        '<line x1="23" y1="9" x2="9" y2="23" stroke="#c0392b" stroke-width="2.5"/></svg>'
    )


def test_dice_face_svg_miss_color_overrides_border_and_cross() -> None:
    """miss_color parametrizes both the border and the cross stroke (S160)."""
    html = dice_face_svg(1, miss=True, miss_color=_BUFF_GREEN)
    assert f'stroke="{_BUFF_GREEN}" stroke-width="1.5"' in html
    assert f'stroke="{_BUFF_GREEN}" stroke-width="2.5"' in html
    assert "#374151" not in html
    assert "#c0392b" not in html


def test_miss_die_html_color_param_forwards_to_dice_face_svg() -> None:
    """miss_die_html(color=...) forwards to dice_face_svg's miss_color parameter."""
    html = miss_die_html(color=_DEBUFF_RED)
    assert f'stroke="{_DEBUFF_RED}" stroke-width="1.5"' in html


def test_dice_face_svg_value_1_normal_not_miss() -> None:
    """dice_face_svg(1) without miss=True renders normal pips, not a cross."""
    html = dice_face_svg(1)
    assert "<svg" in html
    # Normal value-1 die has a single pip circle.
    assert "<circle" in html
    # No miss cross.
    assert "#c0392b" not in html


def test_dice_face_svg_value_1_miss_renders_cross() -> None:
    """dice_face_svg(1, miss=True) renders the × cross (line 74-78 branch)."""
    html = dice_face_svg(1, miss=True)
    assert "<line" in html
    assert "#c0392b" in html


def test_dice_face_svg_miss_non_one_dims_pips() -> None:
    """dice_face_svg(value>1, miss=True) renders dim pips, no cross (line 80-81)."""
    html = dice_face_svg(3, miss=True)
    # Dim pips use #374151 (miss pip color), no cross lines.
    assert "<circle" in html
    assert "#374151" in html
    assert "<line" not in html


def test_aligned_modifier_row_off_scale_appends_miss_die() -> None:
    """Off-scale debuff appends a miss die right of the 6 (line 269 branch)."""
    # Sv 6+ with AP-4 → right_raw = 6 + 4 - 1 = 9 > 6 → off_scale.
    html = save_modifier_die_pair_html(6, -4, "AP", _DEBUFF_RED)
    # Miss die is appended (cross stroke).
    assert "#c0392b" in html


def test_special_die_html_with_content() -> None:
    """special_die_html with content= renders 'label: content' (lines 301-302)."""
    html = special_die_html("Extra Hits", "unmod. 6 = +2 Hits")
    assert "Extra Hits: unmod. 6 = +2 Hits" in html


def test_special_die_html_alternating_fire_has_explanation() -> None:
    """special_die_html with Alt. Fire content renders explanation (condition = effect)."""
    html = special_die_html("Alt. Fire", "≤ half range = first attacks value")
    assert "Alt. Fire: ≤ half range = first attacks value" in html


def test_reroll_marker_row_places_glyph_in_correct_slot() -> None:
    """reroll_marker_row_html places ↺ glyph for each requested slot (line 325)."""
    html = reroll_marker_row_html([2, 4], base_threshold=3)
    assert html.count("↺") == 2


def test_always_fail_marker_row_no_base_threshold() -> None:
    """_marker_row_html without base_threshold (0) renders without boundary gap."""
    # base_threshold=0 means the condition `2 <= base_threshold <= 6` is False → no gap.
    # S160: marker is the SVG miss-die, so the assertion counts <svg, not '✕'.
    html = always_fail_marker_row_html(
        [1, 2], base_threshold=0, color_hint="debuff", label="Quantum Shielding"
    )
    assert html.count("<svg") == 2


def test_reroll_marker_row_with_base_threshold_boundary_gap() -> None:
    """_marker_row_html with base_threshold in 2..6 inserts the boundary-gap slot."""
    # With base_threshold=4 the gap is inserted before column 4.
    html = reroll_marker_row_html([5], base_threshold=4)
    assert "↺" in html
    # Boundary gap: 34px wide span.
    assert "width:34px" in html


def test_modifier_die_pair_html_buff_no_off_scale() -> None:
    """modifier_die_pair_html buff path: grey on left die, semantic color on right."""
    html = modifier_die_pair_html(4, 3, "Buff", 1, _BUFF_GREEN, base_threshold=4)
    assert _BUFF_GREEN in html
    # No miss die needed (in-scale buff).
    assert "#c0392b" not in html


def test_value_triggered_die_row_shows_content_in_trigger_column() -> None:
    """value_triggered_die_row_html renders the chip text and the directive label."""
    html = value_triggered_die_row_html("Hungry Void", 6, "AP-1", _BUFF_GREEN, base_threshold=3)
    assert "AP-1" in html
    assert "Hungry Void" in html
    assert _BUFF_GREEN in html


def test_value_triggered_die_row_uses_buff_green_for_attacker_benefit() -> None:
    """The AP-on-6 row reads as an attacker buff (green), like any other buff."""
    html = value_triggered_die_row_html("Hungry Void", 6, "AP-1", _BUFF_GREEN)
    assert _BUFF_GREEN in html
    assert _DEBUFF_RED not in html


def test_value_triggered_die_row_boundary_gap_follows_threshold() -> None:
    """A base_threshold in 2..6 inserts the die-wide boundary gap for alignment."""
    html = value_triggered_die_row_html("Dir", 6, "AP-1", _BUFF_GREEN, base_threshold=4)
    assert "width:34px" in html


# ---------------------------------------------------------------------------
# light_cover_label — Vengeful Stars D2 inline hint (Plan 025 Step 3)
# ---------------------------------------------------------------------------


def test_light_cover_label_plain_without_directive() -> None:
    """No directive active → plain label, no badge or hint text."""
    label = light_cover_label(None)
    assert label == "Light Cover (+1 Save vs Ranged)"
    assert ":green-badge" not in label
    assert "half range" not in label


def test_light_cover_label_with_directive_contains_badge() -> None:
    """Active directive → label carries a :green-badge with the protocol short name."""
    label = light_cover_label("Vengeful Stars")
    assert ":green-badge[Vengeful Stars]" in label


def test_light_cover_label_with_directive_contains_hint_text() -> None:
    """Active directive → label carries the No-Light-Cover-half-range hint."""
    label = light_cover_label("Vengeful Stars")
    assert "No Light Cover ≤ half range" in label


def test_light_cover_label_with_directive_preserves_base_text() -> None:
    """Base text must be present regardless of the directive."""
    label = light_cover_label("Vengeful Stars")
    assert "Light Cover (+1 Save vs Ranged)" in label


# ---------------------------------------------------------------------------
# _capped_modifier_threshold — 9E ±1 hit/wound modifier cap (S110 retro M1)
# ---------------------------------------------------------------------------


def test_capped_threshold_single_modifier_shifts_one_step() -> None:
    """A single ±1 modifier moves the threshold exactly one step."""
    assert _capped_modifier_threshold(4, 1) == 3  # buff lowers the threshold
    assert _capped_modifier_threshold(4, -1) == 5  # debuff raises it
    assert _capped_modifier_threshold(4, 0) == 4  # no modifier → base


def test_capped_threshold_caps_stacked_modifiers_at_plus_minus_one() -> None:
    """9E rule: the summed modifier never shifts the threshold by more than ±1."""
    assert _capped_modifier_threshold(4, 3) == 3  # +3 capped to +1 → 3+
    assert _capped_modifier_threshold(4, -3) == 5  # −3 capped to −1 → 5+


def test_capped_threshold_never_drops_below_two() -> None:
    """Even a capped buff cannot produce a threshold below 2+ (a 1 always fails)."""
    assert _capped_modifier_threshold(2, 1) == 2
    assert _capped_modifier_threshold(2, 5) == 2


# --- B-105: generic go_source_chip (replaces diceHtml._strength_source_badge_html) ---


def test_go_source_chip_carries_label_color_and_tooltip() -> None:
    """go_source_chip renders the GO name in the given colour with a title
    tooltip (same wrap-safeguard as _badge_chip, B-111 Variante C)."""
    html = go_source_chip("Disruption Fields", _BUFF_GREEN)
    assert "Disruption Fields" in html
    assert _BUFF_GREEN in html
    assert 'title="Disruption Fields"' in html


def test_go_source_chip_debuff_color() -> None:
    """A debuff-perspective GO source (e.g. Quantum Shielding) renders in the
    debuff-red palette — the caller decides the colour, go_source_chip has no
    hard-coded buff-only colour (B-105 generalization)."""
    html = go_source_chip("Quantum Shielding", _DEBUFF_RED)
    assert _DEBUFF_RED in html


def test_render_dice_wound_block_strength_buff_label_uses_go_source_chip() -> None:
    """Regression (B-105 rewire, 'keine Verhaltensänderung'): the WOUND
    block's Strength-buff source name still renders as a buff-green chip
    after _strength_source_badge_html was generalized into go_source_chip —
    same visual output through the shared building block.
    """
    dice_html_module.st.markdown.reset_mock()
    dice_html_module._render_dice_wound_block(
        strength=5,
        toughness=4,
        wound_stack=[],
        strength_buff=1,
        strength_buff_labels=["Disruption Fields"],
    )
    html = "".join(str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list)
    assert "Disruption Fields" in html
    assert _BUFF_GREEN in html


def test_render_dice_save_block_invuln_without_label_has_no_chip() -> None:
    """Backward compatibility: omitting invuln_source_label (every existing
    caller today) keeps the bare 'Inv N+' badge — no title-tooltip chip
    appended.
    """
    dice_html_module.st.markdown.reset_mock()
    save = {"armour": 3, "armour_eff": 3, "invuln": 4, "stack": []}
    dice_html_module._render_dice_save_block(save, ap=0)
    html = "".join(str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list)
    assert "Inv 4+" in html
    assert "title=" not in html


def test_render_dice_save_block_invuln_shows_go_source_label() -> None:
    """Regression (B-105 — Stakeholder wish 'Badge am Quantum-Deflection-
    Rettungswurf'): when the caller supplies invuln_source_label, the Invuln
    row names the GO source next to 'Inv N+' — proves the chip carries a
    data-driven name from the caller, not a hardcoded one.
    """
    dice_html_module.st.markdown.reset_mock()
    save = {"armour": 3, "armour_eff": 3, "invuln": 4, "stack": []}
    dice_html_module._render_dice_save_block(
        save, ap=0, ability_invuln=True, invuln_source_label="Quantum Deflection"
    )
    html = "".join(str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list)
    assert "Inv 4+" in html
    assert "Quantum Deflection" in html
    assert 'title="Quantum Deflection"' in html


def test_render_dice_save_block_invuln_follows_wound_block_header_pattern() -> None:
    """Regression (B-115 — Stakeholder rejection of the wrapped 'Inv / 4+'
    stack, see docs/handoff 2026-07-17 screenshot): the Invuln section must
    follow the same split as _render_dice_wound_block — a title call carrying
    'Inv N+' + the go_source_chip ABOVE a separate, full-width dice-row call
    with an empty left label (grid_row_html("", ...)), never both squeezed
    into one grid_row_html's left label column.
    """
    dice_html_module.st.markdown.reset_mock()
    save = {"armour": 3, "armour_eff": 3, "invuln": 4, "stack": []}
    dice_html_module._render_dice_save_block(
        save, ap=0, ability_invuln=True, invuln_source_label="Quantum Deflection"
    )
    calls = [str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list]
    title_calls = [c for c in calls if "Inv 4+" in c]
    assert len(title_calls) == 1, "Inv N+ must appear in exactly one (title) call"
    title_html = title_calls[0]
    assert "Quantum Deflection" in title_html
    # The title call is a bare span + chip — no dice-grid row wrapper.
    assert '<div style="display:flex;align-items:center;margin:2px 0;">' not in title_html

    dice_calls = [
        c
        for c in calls
        if '<div style="display:flex;align-items:center;margin:2px 0;">' in c and "Inv 4+" not in c
    ]
    assert dice_calls, "expected a separate full-width dice-row call for the invuln threshold"
    invuln_dice_call = dice_calls[-1]
    assert "Quantum Deflection" not in invuln_dice_call
    # Empty left label column, exactly like the WOUND block's dice row.
    assert dice_html_module.dice_row_html(4) in invuln_dice_call
    assert dice_html_module.threshold_header_html(4) in invuln_dice_call


def test_render_dice_save_block_invuln_no_bonus_has_no_chip_and_bare_threshold() -> None:
    """No-bonus-invuln case (unchanged behaviour, only layout moved): without
    invuln_source_label there is no chip anywhere, and the bare 'Inv N+' still
    sits in its own title call above the dice row.
    """
    dice_html_module.st.markdown.reset_mock()
    save = {"armour": 3, "armour_eff": 3, "invuln": 5, "stack": []}
    dice_html_module._render_dice_save_block(save, ap=0)
    calls = [str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list]
    html = "".join(calls)
    assert "Inv 5+" in html
    assert "title=" not in html
    title_calls = [c for c in calls if "Inv 5+" in c]
    assert len(title_calls) == 1
    assert '<div style="display:flex;align-items:center;margin:2px 0;">' not in title_calls[0]


# ---------------------------------------------------------------------------
# _render_dice_roll_block (HIT block) — reroll_slots marker row (B-113 Teil A)
# ---------------------------------------------------------------------------


def test_render_dice_roll_block_shows_reroll_marker_for_hardwired_for_destruction() -> None:
    """Skorpekh Destroyer end-to-end (Hardwired for Destruction, 'reroll a hit
    roll of 1'): when the HIT block dict carries reroll_slots=[1] (combat.
    resolve_attack_modifiers's hit_reroll_ones=True), the rendered HIT block
    shows the ↺ reroll marker row."""
    dice_html_module.st.markdown.reset_mock()
    block = {"base": 3, "stack": [], "modified": 3, "reroll_slots": [1]}
    dice_html_module._render_dice_roll_block("HIT", "WS", block)
    html = "".join(str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list)
    assert "Reroll" in html
    assert _reroll_die_svg() in html


def test_render_dice_roll_block_no_reroll_marker_when_slots_empty() -> None:
    """Regression: the pre-B-113 default (no reroll_slots key / empty list) —
    e.g. a Necron Warriors attack without Hardwired for Destruction — renders
    no reroll marker row at all, byte-identical to before this feature."""
    dice_html_module.st.markdown.reset_mock()
    block = {"base": 3, "stack": [], "modified": 3, "reroll_slots": []}
    dice_html_module._render_dice_roll_block("HIT", "WS", block)
    html = "".join(str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list)
    assert "Reroll" not in html


def test_render_dice_roll_block_no_reroll_marker_when_key_missing() -> None:
    """Regression: callers that never set reroll_slots at all (block.get default
    []) render identically to the empty-list case — no crash, no marker."""
    dice_html_module.st.markdown.reset_mock()
    block = {"base": 3, "stack": [], "modified": 3}
    dice_html_module._render_dice_roll_block("HIT", "WS", block)
    html = "".join(str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list)
    assert "Reroll" not in html


# ---------------------------------------------------------------------------
# _render_dice_wound_block — reroll_slots marker row (B-113 Teil B: Destroyer
# Cult Lord "United in Destruction" AURA, "re-roll a wound roll of 1")
# ---------------------------------------------------------------------------


def test_render_dice_wound_block_shows_reroll_marker_for_united_in_destruction() -> None:
    """Skorpekh Destroyers within a Lord's aura end-to-end: when the WOUND
    block dict carries reroll_slots=[1] (combat.resolve_attack_modifiers's
    wound_reroll_ones=True), the rendered WOUND block shows the ↺ reroll
    marker row, same building block as the HIT block (B-113 Teil A)."""
    dice_html_module.st.markdown.reset_mock()
    dice_html_module._render_dice_wound_block(
        strength=5,
        toughness=4,
        wound_stack=[],
        reroll_slots=[1],
    )
    html = "".join(str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list)
    assert "Reroll" in html
    assert _reroll_die_svg() in html


def test_render_dice_wound_block_no_reroll_marker_when_slots_empty() -> None:
    """Regression: no aura source (e.g. no Lord in the roster) → reroll_slots=[]
    → no reroll marker row, byte-identical to before this feature."""
    dice_html_module.st.markdown.reset_mock()
    dice_html_module._render_dice_wound_block(
        strength=5,
        toughness=4,
        wound_stack=[],
        reroll_slots=[],
    )
    html = "".join(str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list)
    assert "Reroll" not in html


def test_render_dice_wound_block_no_reroll_marker_when_param_omitted() -> None:
    """Regression: every pre-B-113-Teil-B caller that never passes reroll_slots
    (default None) renders identically — no crash, no marker."""
    dice_html_module.st.markdown.reset_mock()
    dice_html_module._render_dice_wound_block(
        strength=5,
        toughness=4,
        wound_stack=[],
    )
    html = "".join(str(call.args[0]) for call in dice_html_module.st.markdown.call_args_list)
    assert "Reroll" not in html
