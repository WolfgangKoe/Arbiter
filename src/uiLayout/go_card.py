"""The GO card — the single Gefechtsoptionen (GO) card builder (design_system.md §6).

Before this module, GOs (Stratagems + comparable optional rules) existed in three
divergent bespoke render shapes (reactive box, inline offer, tab expander — S130
finding). ``design_system.md`` §6.1 replaces all three with **one** card, rendered
in a full or compact form, in one of four states. This module builds that card's
visual body (header line + keyword-chip row) as plain HTML.

Pure composition, Streamlit-free and coverage-measured (INV-6, same seam as
``dice_compose.py`` / ``badges.py``) — the interactive Use/Undo button and the
rule-text accordion are the caller's job: a thin Streamlit wrapper
(``uiLayout._common.render_go_card``) places this HTML via
``st.markdown(..., unsafe_allow_html=True)`` and renders the real widgets next to
it. This module never emits a clickable element.

Colours follow the fixed §6.5 decision (no new tokens): "ready" = Gold-Primary
border (``--arb-accent``), "dormant"/"locked" = dimmed Secondary (``--arb-muted``).
Hex values are the same constants ``design_colors.md`` §1 defines — mirrored here
literally, same convention as the STATIONARY/ADVANCED colour maps in
``_common.py``/``unitCard.py`` (CSS custom properties are not reachable from a
plain HTML string built outside the page's injected ``<style>`` scope).
"""

from __future__ import annotations

from typing import Literal

from constants.symbols import SYM_RESET
from uiLayout.badges import chip

GoCardState = Literal["dormant", "ready", "used", "locked"]
"""The GO card's four states (design_system.md §6.1).

dormant — trigger not (yet) met: visible, dimmed, action disabled.
ready   — trigger met, CP sufficient: highlighted, action enabled ("Use").
used    — Use was pressed, the activation window is still open: action becomes
          "Undo" (full rollback — CP and effect/value both revert).
locked  — CP missing / a precondition disappeared: dimmed, reason suffixed onto
          the header.
"""

# design_colors.md §1 — mirrored literally (see module docstring for why).
_ACCENT = "#d4a017"  # --arb-accent (Gold-Primary — "ready"/"used" border)
_MUTED = "#6b5f44"  # --arb-muted (dimmed text/border — "dormant"/"locked")
_SURFACE = "#1c1a14"  # --arb-surface (card background)
_BORDER = "#2e2618"  # --arb-border (chip border)
_TEXT = "#e7e5e4"  # --arb-text (name)

_DIMMED_STATES: frozenset[str] = frozenset({"dormant", "locked"})

_STATE_BORDER: dict[GoCardState, str] = {
    "dormant": _MUTED,
    "ready": _ACCENT,
    "used": _ACCENT,
    "locked": _MUTED,
}


def action_slot_text(state: GoCardState, cp_cost: int) -> str:
    """The one action-slot's label for a given state (design_system.md §6.4).

    One vocabulary family, not four: ``Use (N CP)`` for every state except
    "used", which shows the full-rollback ``Undo (+N CP)`` instead. Shared by
    the HTML builder (static echo inside the card) and the caller's real
    button (``uiLayout._common.render_go_card``), so the two never drift.
    """
    if state == "used":
        return f"{SYM_RESET} Undo (+{cp_cost} CP)"
    return f"Use ({cp_cost} CP)"


def go_card_html(
    name: str,
    cp_cost: int,
    state: GoCardState,
    *,
    keywords: list[str] | None = None,
    compact: bool = False,
    locked_reason: str | None = None,
) -> str:
    """Render one GO card's visual body: header line + (full form) keyword chips.

    name/cp_cost   — the GO's display name and CP cost (0 = free).
    state          — one of the four states (module docstring); drives the
                     border colour (accent for ready/used, dimmed muted for
                     dormant/locked) and whether the card is rendered dimmed.
    keywords       — keyword chips (``badges.chip()``, e.g. ``["CORE", "CHARGE"]``);
                     ignored when ``compact`` is True — the compact form is the
                     inline-anchor shape (design_system.md §6.2), which carries
                     no chip row by design (see the §6.3 mockup).
    compact        — full form (default) shows the chip row; compact form omits
                     it and tightens padding for use as an inline anchor next to
                     a table-roll entry or an in-flow trigger.
    locked_reason  — "locked" only: appended to the header as the required
                     suffix explaining why the card is unavailable (§6.1).

    Contains no clickable element — the caller renders the real Use/Undo button
    itself, using the same label this module also builds via
    :func:`action_slot_text`, and the rule-text accordion.
    """
    border = _STATE_BORDER[state]
    dimmed = state in _DIMMED_STATES
    opacity = "0.55" if dimmed else "1"
    action_color = _MUTED if dimmed else border

    header_html = (
        f'<span style="font-weight:600;color:{_TEXT};">{name}</span>'
        f' <span style="color:{_MUTED};">· {cp_cost} CP</span>'
    )
    if state == "locked" and locked_reason:
        header_html += f' <span style="color:{_MUTED};font-style:italic;"> — {locked_reason}</span>'

    action_html = (
        f'<span style="float:right;color:{action_color};'
        f"border:1px solid {action_color};border-radius:2px;"
        f'padding:1px 6px;font-size:10px;">{action_slot_text(state, cp_cost)}</span>'
    )

    padding = "3px 6px" if compact else "6px 8px"
    parts = [
        f'<div style="border:1px solid {border};border-radius:4px;'
        f'padding:{padding};opacity:{opacity};background:{_SURFACE};">',
        f"<div>{header_html}{action_html}</div>",
    ]
    if not compact and keywords:
        chips_html = "".join(chip(kw, _MUTED, _SURFACE, _BORDER) for kw in keywords)
        parts.append(f'<div style="margin-top:4px;">{chips_html}</div>')
    parts.append("</div>")
    return "".join(parts)
