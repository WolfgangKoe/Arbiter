"""HTML-output tests for the GO card builder (design_system.md §6).

goCard.py is pure composition — no Streamlit — so it is asserted directly at
the HTML level, same seam as test_badges.py / diceCompose.py (INV-6). Covers
all four states, full vs. compact form, keyword chips, target-unit display,
CP display, and the per-state container border style (S133-D Befund 2: the
card's border is now a real Streamlit container the caller colours via a
scoped ``st-key-`` CSS override, not an HTML ``<div>`` drawn by this module).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from uiLayout.goCard import (  # noqa: E402
    action_slot_text,
    go_card_container_style,
    go_card_html,
    reactive_box_target_label,
)

# ---------------------------------------------------------------------------
# action_slot_text() — S133-D Befund 1: plain "Use"/"↺ Undo", no CP echo
# ---------------------------------------------------------------------------


def test_action_slot_text_is_use_for_dormant() -> None:
    assert action_slot_text("dormant") == "Use"


def test_action_slot_text_is_use_for_ready() -> None:
    assert action_slot_text("ready") == "Use"


def test_action_slot_text_is_use_for_locked() -> None:
    assert action_slot_text("locked") == "Use"


def test_action_slot_text_is_undo_for_used() -> None:
    assert action_slot_text("used") == "↺ Undo"


def test_action_slot_text_is_used_for_used_elsewhere() -> None:
    # S139 B12a — the 5th state never offers Undo, only the disabled label.
    assert action_slot_text("used_elsewhere") == "Used"
    assert "↺" not in action_slot_text("used_elsewhere")


def test_action_slot_text_never_echoes_cp_cost() -> None:
    # CP already stands in the card header — the button must never repeat it.
    assert "CP" not in action_slot_text("ready")
    assert "CP" not in action_slot_text("used")


# ---------------------------------------------------------------------------
# go_card_container_style() — per-state border colour, scoped to the caller's
# container key (S133-D Befund 2)
# ---------------------------------------------------------------------------


def test_go_card_container_style_dormant_is_dimmed_muted_border() -> None:
    css = go_card_container_style("box_1", "dormant")
    assert ".st-key-box_1" in css
    assert "border-color:#6b5f44" in css
    assert "opacity:0.55" in css


def test_go_card_container_style_ready_is_accent_border_full_opacity() -> None:
    css = go_card_container_style("box_1", "ready")
    assert "border-color:#d4a017" in css
    assert "opacity:1" in css


def test_go_card_container_style_used_stays_accent_bordered() -> None:
    css = go_card_container_style("box_1", "used")
    assert "border-color:#d4a017" in css
    assert "opacity:1" in css


def test_go_card_container_style_locked_is_dimmed_muted_border() -> None:
    css = go_card_container_style("box_1", "locked")
    assert "border-color:#6b5f44" in css
    assert "opacity:0.55" in css


def test_go_card_container_style_used_elsewhere_is_dimmed_muted_border() -> None:
    # S139 B12a — "used_elsewhere" dims like "locked" (§6.5: no new colour token).
    css = go_card_container_style("box_1", "used_elsewhere")
    assert "border-color:#6b5f44" in css
    assert "opacity:0.55" in css


def test_go_card_container_style_sanitizes_key_like_streamlit_does() -> None:
    # Streamlit turns a key into a class by replacing non [a-zA-Z0-9_-] chars
    # with "-" — the selector must use the exact same transform, or the
    # override silently never matches the real DOM node.
    css = go_card_container_style("go_card_box_Orks_unit#1", "ready")
    assert ".st-key-go_card_box_Orks_unit-1" in css
    assert "#1" not in css.split("{")[0]


# ---------------------------------------------------------------------------
# go_card_html() — header content: name / CP / target / locked reason
# ---------------------------------------------------------------------------


def test_go_card_shows_name_and_cp_cost() -> None:
    html = go_card_html("Fire Overwatch", 1, "ready")
    assert ">Fire Overwatch<" in html
    assert "1 CP" in html


def test_go_card_html_carries_no_border_or_opacity_styling() -> None:
    # The border/opacity now live in go_card_container_style(), applied to the
    # surrounding st.container — go_card_html is header content only.
    html = go_card_html("Fire Overwatch", 1, "ready")
    assert "border:1px solid" not in html
    assert "opacity:" not in html


def test_go_card_locked_appends_reason_suffix_to_header() -> None:
    html = go_card_html("Fractal Targeting", 1, "locked", locked_reason="CP insufficient")
    assert "CP insufficient" in html


def test_go_card_locked_without_reason_omits_suffix_span() -> None:
    html = go_card_html("Fractal Targeting", 1, "locked")
    assert "font-style:italic" not in html


def test_go_card_reason_ignored_outside_locked_and_used_elsewhere() -> None:
    # locked_reason renders only in "locked" (verbatim) and "used_elsewhere"
    # ("used on ⟨Einheit⟩", S141 B12b) — every other state never shows it.
    # (Deliberate contract change S141: pre-B12b this suffix was locked-only.)
    for state in ("ready", "dormant", "used"):
        html = go_card_html("Fire Overwatch", 1, state, locked_reason="should not appear")
        assert "should not appear" not in html


def test_go_card_used_elsewhere_appends_used_on_unit_suffix() -> None:
    """S141 B12b (design_system.md §6.1 5th state): a card whose GO was spent
    at ANOTHER anchor this phase shows the header suffix "used on ⟨Einheit⟩"
    when the spend recorded a unit — locked_reason carries the raw unit name,
    go_card_html owns the wording."""
    html = go_card_html("Command Re-Roll", 1, "used_elsewhere", locked_reason="Boyz Mob")
    assert "used on Boyz Mob" in html


def test_go_card_used_elsewhere_without_unit_omits_suffix() -> None:
    # Spec: suffix only "falls eine Einheit bekannt" — no name, no suffix span.
    html = go_card_html("Command Re-Roll", 1, "used_elsewhere")
    assert "used on" not in html
    assert "font-style:italic" not in html


def test_go_card_shows_target_unit_name_when_given() -> None:
    html = go_card_html("Desperate Breakout", 2, "used", target_name="Boyz Mob")
    assert "Boyz Mob" in html


def test_go_card_omits_target_span_when_not_given() -> None:
    html = go_card_html("Fire Overwatch", 1, "ready")
    assert "→" not in html


# ---------------------------------------------------------------------------
# reactive_box_target_label() — S142 A3 (Sofortlinderung, S141 Befund 3):
# reactive boxes always show the owning player, unit name when unit-scoped.
# ---------------------------------------------------------------------------


def test_reactive_box_target_label_combines_unit_and_player_when_unit_given() -> None:
    label = reactive_box_target_label("Boyz Mob", "Orks")
    assert label == "Boyz Mob · Orks"


def test_reactive_box_target_label_is_player_only_when_no_unit() -> None:
    label = reactive_box_target_label(None, "Necrons")
    assert label == "Necrons"


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


def test_go_card_compact_form_still_shows_name_and_cp() -> None:
    html = go_card_html("Command Re-Roll", 1, "ready", compact=True)
    assert ">Command Re-Roll<" in html
    assert "1 CP" in html
