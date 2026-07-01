"""HTML-output tests for the shared badge / chip builders.

badges.py is the single source of badge geometry (design_system.md §2). It is pure
composition — no Streamlit — so it is asserted directly at the HTML level. This is
the coverage safety net the render-composition seam (INV-6) requires.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from uiLayout.badges import badge, chip  # noqa: E402

# ---------------------------------------------------------------------------
# badge()
# ---------------------------------------------------------------------------


def test_badge_carries_the_verbindliche_geometry_tokens() -> None:
    html = badge("MOVED", "#60a5fa", "#0a1020")
    assert "border-radius:2px" in html
    assert "padding:1px 6px" in html
    assert "font-size:10px" in html
    assert "font-weight:600" in html
    assert "letter-spacing:0.06em" in html


def test_badge_uses_foreground_as_text_and_border_color() -> None:
    html = badge("SHOT", "#40a0b8", "#081418")
    assert "color:#40a0b8" in html
    assert "border:1px solid #40a0b8" in html
    assert "background:#081418" in html


def test_badge_renders_the_given_text() -> None:
    assert ">RESERVE<" in badge("RESERVE", "#ff9060", "#2a1208")


def test_badge_default_margin_right_is_3px() -> None:
    assert "margin-right:3px" in badge("X", "#fff", "#000")


def test_badge_margin_right_is_overridable() -> None:
    assert "margin-right:4px" in badge("X", "#fff", "#000", margin_right="4px")


# ---------------------------------------------------------------------------
# chip()
# ---------------------------------------------------------------------------


def test_chip_carries_the_smaller_geometry_tokens() -> None:
    html = chip("INFANTRY", "#6b5f44", "#1c1a14", "#2e2618")
    assert "border-radius:2px" in html
    assert "padding:1px 5px" in html
    assert "font-size:9px" in html
    assert "font-weight:400" in html
    assert "letter-spacing:0.05em" in html


def test_chip_border_can_differ_from_foreground() -> None:
    html = chip("KW", "#6b5f44", "#1c1a14", "#2e2618")
    assert "color:#6b5f44" in html
    assert "border:1px solid #2e2618" in html
    assert "background:#1c1a14" in html


def test_chip_renders_the_given_text() -> None:
    assert ">CHARACTER<" in chip("CHARACTER", "#f5d080", "#3a2e10", "#f5d080")


def test_chip_default_margin_right_is_2px() -> None:
    assert "margin-right:2px" in chip("X", "#fff", "#000", "#000")


def test_chip_margin_right_is_overridable() -> None:
    assert "margin-right:5px" in chip("X", "#fff", "#000", "#000", margin_right="5px")
