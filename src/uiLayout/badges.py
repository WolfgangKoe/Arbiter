"""Shared badge / chip HTML builders — the single source of badge geometry.

Before this module four call sites (``_common._badge``, ``unitCard._badge``,
``armyCard._keyword_badge``/``_active_ability_badge``, and the inline Invuln
fragments in ``dice_html``) each hand-rolled the same ``<span>`` with slightly
different radius/padding/font-size. They had already drifted (see the comment in
``_common.py`` about MOVED/Buff swapping). This module fixes the *geometry* in one
place; colours stay at the call site (they come from the semantic tables in
``design_colors.md`` / ``design_system.md``).

Pure composition, Streamlit-free and coverage-measured (INV-6, same seam as
``dice_compose.py``). Two size classes, per the S115 consensus:

* ``badge``  — status / buff / debuff / faction / ability: 2px · 1px 6px · 10px · 600
* ``chip``   — keyword / secondary note:                    2px · 1px 5px ·  9px · 400
"""

from __future__ import annotations

# Verbindlicher Wertesatz (design_system.md §2) — hier EINMAL, nirgends sonst.
_BADGE_RADIUS = "2px"
_BADGE_PADDING = "1px 6px"
_BADGE_FONT_SIZE = "10px"
_BADGE_FONT_WEIGHT = "600"
_BADGE_LETTER_SPACING = "0.06em"

_CHIP_RADIUS = "2px"
_CHIP_PADDING = "1px 5px"
_CHIP_FONT_SIZE = "9px"
_CHIP_FONT_WEIGHT = "400"
_CHIP_LETTER_SPACING = "0.05em"


def badge(text: str, fg: str, bg: str, *, margin_right: str = "3px") -> str:
    """A status/buff/faction badge: outlined pill, foreground = border colour."""
    return (
        f'<span style="background:{bg};border:1px solid {fg};'
        f"border-radius:{_BADGE_RADIUS};padding:{_BADGE_PADDING};"
        f"font-size:{_BADGE_FONT_SIZE};color:{fg};"
        f"letter-spacing:{_BADGE_LETTER_SPACING};font-weight:{_BADGE_FONT_WEIGHT};"
        f'margin-right:{margin_right};">{text}</span>'
    )


def chip(text: str, fg: str, bg: str, border: str, *, margin_right: str = "2px") -> str:
    """A compact keyword/note chip: smaller than a badge, border may differ from fg."""
    return (
        f'<span style="background:{bg};border:1px solid {border};'
        f"border-radius:{_CHIP_RADIUS};padding:{_CHIP_PADDING};"
        f"font-size:{_CHIP_FONT_SIZE};color:{fg};"
        f"letter-spacing:{_CHIP_LETTER_SPACING};font-weight:{_CHIP_FONT_WEIGHT};"
        f'margin-right:{margin_right};">{text}</span>'
    )
