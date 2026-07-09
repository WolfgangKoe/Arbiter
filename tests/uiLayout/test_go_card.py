"""HTML-output tests for the GO card builder (design_system.md §6).

go_card.py is pure composition — no Streamlit — so it is asserted directly at
the HTML level, same seam as test_badges.py / dice_compose.py (INV-6). Covers
all four states, full vs. compact form, keyword chips, and CP display.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from uiLayout.go_card import action_slot_text, go_card_html  # noqa: E402

# ---------------------------------------------------------------------------
# action_slot_text()
# ---------------------------------------------------------------------------


def test_action_slot_text_is_use_for_dormant() -> None:
    assert action_slot_text("dormant", 1) == "Use (1 CP)"


def test_action_slot_text_is_use_for_ready() -> None:
    assert action_slot_text("ready", 2) == "Use (2 CP)"


def test_action_slot_text_is_use_for_locked() -> None:
    assert action_slot_text("locked", 1) == "Use (1 CP)"


def test_action_slot_text_is_undo_for_used() -> None:
    assert action_slot_text("used", 1) == "↺ Undo (+1 CP)"


def test_action_slot_text_reflects_cp_cost() -> None:
    assert action_slot_text("ready", 0) == "Use (0 CP)"
    assert action_slot_text("used", 3) == "↺ Undo (+3 CP)"


# ---------------------------------------------------------------------------
# go_card_html() — name / CP display, all four states
# ---------------------------------------------------------------------------


def test_go_card_shows_name_and_cp_cost() -> None:
    html = go_card_html("Fire Overwatch", 1, "ready")
    assert ">Fire Overwatch<" in html
    assert "1 CP" in html


def test_go_card_dormant_is_dimmed_with_muted_border() -> None:
    html = go_card_html("Command Re-Roll", 1, "dormant")
    assert "border:1px solid #6b5f44" in html
    assert "opacity:0.55" in html
    assert "Use (1 CP)" in html


def test_go_card_ready_is_highlighted_with_accent_border() -> None:
    html = go_card_html("Fire Overwatch", 1, "ready")
    assert "border:1px solid #d4a017" in html
    assert "opacity:1" in html
    assert "Use (1 CP)" in html


def test_go_card_used_shows_undo_and_stays_accent_bordered() -> None:
    html = go_card_html("Fire Overwatch", 1, "used")
    assert "border:1px solid #d4a017" in html
    assert "opacity:1" in html
    assert "↺ Undo (+1 CP)" in html


def test_go_card_locked_is_dimmed_with_muted_border() -> None:
    html = go_card_html("Fractal Targeting", 1, "locked")
    assert "border:1px solid #6b5f44" in html
    assert "opacity:0.55" in html


def test_go_card_locked_appends_reason_suffix_to_header() -> None:
    html = go_card_html("Fractal Targeting", 1, "locked", locked_reason="CP insufficient")
    assert "CP insufficient" in html


def test_go_card_locked_without_reason_omits_suffix_span() -> None:
    html = go_card_html("Fractal Targeting", 1, "locked")
    assert "font-style:italic" not in html


def test_go_card_reason_only_applies_to_locked_state() -> None:
    # locked_reason is a no-op outside "locked" — other states never show it.
    html = go_card_html("Fire Overwatch", 1, "ready", locked_reason="should not appear")
    assert "should not appear" not in html


# ---------------------------------------------------------------------------
# go_card_html() — keyword chips, full vs. compact form
# ---------------------------------------------------------------------------


def test_go_card_full_form_renders_keyword_chips() -> None:
    html = go_card_html("Fire Overwatch", 1, "ready", keywords=["CORE", "CHARGE"])
    assert ">CORE<" in html
    assert ">CHARGE<" in html


def test_go_card_full_form_without_keywords_has_no_chip_row() -> None:
    html = go_card_html("Fire Overwatch", 1, "ready")
    assert "margin-top:4px" not in html


def test_go_card_compact_form_omits_keyword_chips_even_when_given() -> None:
    html = go_card_html("Command Re-Roll", 1, "ready", keywords=["CORE"], compact=True)
    assert ">CORE<" not in html
    assert "margin-top:4px" not in html


def test_go_card_compact_form_uses_tighter_padding() -> None:
    full = go_card_html("Fire Overwatch", 1, "ready")
    compact = go_card_html("Command Re-Roll", 1, "ready", compact=True)
    assert "padding:6px 8px" in full
    assert "padding:3px 6px" in compact


def test_go_card_compact_form_still_shows_name_and_cp() -> None:
    html = go_card_html("Command Re-Roll", 1, "ready", compact=True)
    assert ">Command Re-Roll<" in html
    assert "1 CP" in html
