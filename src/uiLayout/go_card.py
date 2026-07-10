"""The GO card — the single Gefechtsoptionen (GO) card builder (design_system.md §6).

Before this module, GOs (Stratagems + comparable optional rules) existed in three
divergent bespoke render shapes (reactive box, inline offer, tab expander — S130
finding). ``design_system.md`` §6.1 replaces all three with **one** card, rendered
in a full or compact form, in one of four states. This module builds that card's
header content (name/CP/target-unit line + keyword-chip row) as plain HTML, plus
the scoped ``<style>`` block that colours the card's *real* Streamlit container
border per state.

Pure composition, Streamlit-free and coverage-measured (INV-6, same seam as
``dice_compose.py`` / ``badges.py``) — the interactive Use/Undo button, the
rule-text accordion and the bordered container itself are the caller's job: a
thin Streamlit wrapper (``uiLayout._common.render_go_card``) places
``go_card_html()`` inside a keyed ``st.container(border=True, key=...)`` via
``st.markdown(..., unsafe_allow_html=True)``, applies ``go_card_container_style()``
to colour that one container's border, and renders the real widgets (button,
accordion, any expanded content) *inside the same container* — S133-D Befund 2:
the K1 version drew its own border as an HTML ``<div>`` around only the header
text, so the button (next column) and the rule-text accordion (rendered as a
separate top-level element after both columns closed) were never structurally
inside that border — nothing grouped them in the DOM, only the header line
happened to sit inside a bordered-looking box. This module never emits a
clickable element.

Colours follow the fixed §6.5 decision (no new tokens): "ready"/"used" = Gold-
Primary border (``--arb-accent``), "dormant"/"locked" = dimmed Secondary
(``--arb-muted``). Hex values are the same constants ``design_colors.md`` §1
defines — mirrored here literally, same convention as the STATIONARY/ADVANCED
colour maps in ``_common.py``/``unitCard.py`` (CSS custom properties are not
reachable from a plain HTML string built outside the page's injected ``<style>``
scope). The per-state colour is applied via a container ``key`` — Streamlit 1.57
stamps a stable ``st-key-<key>`` class on a keyed container (verified in the
installed build's JS bundle, ``DO(e)`` → ``"st-key-" + sanitize(e)``), which a
scoped ``<style>`` rule can target with ``!important`` to override the theme's
one fixed border colour for `st.container(border=True)`.
"""

from __future__ import annotations

import re
from typing import Literal

from constants.symbols import SYM_RESET
from uiLayout.badges import chip

# Mirrors Streamlit 1.57's own key→class sanitisation (``DO(e)`` in the built JS
# bundle: ``"st-key-" + e.trim().replace(/[^a-zA-Z0-9_-]/g, "-")``) — the CSS
# selector below must transform ``container_key`` the exact same way Streamlit
# transforms it when stamping the class onto the DOM node, or the override
# silently never matches.
_KEY_SANITIZE_RE = re.compile(r"[^a-zA-Z0-9_-]")


def _sanitize_key(key: str) -> str:
    return _KEY_SANITIZE_RE.sub("-", key.strip())


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


def action_slot_text(state: GoCardState) -> str:
    """The one action-slot's label for a given state (design_system.md §6.4).

    One vocabulary family, not four: plain ``Use`` for every state except
    "used", which shows the full-rollback ``↺ Undo`` instead — CP cost is not
    repeated on the button because it already stands in the card header (S133-D
    Befund 1: §6.1's mockups always showed a bare ``[Use]``; §6.4 had drifted to
    a ``Use (N CP)``/``Undo (+N CP)`` family, a spec-internal contradiction the
    stakeholder resolved in §6.1's favour — §6.4 was corrected in the same
    change). The one caller that renders a label — the real button in
    ``uiLayout._common.render_go_card`` — draws it from here (``go_card_html``
    itself stays label-free; S132 Befund 1: a static HTML echo of this same
    label duplicated the action slot next to the real button).
    """
    if state == "used":
        return f"{SYM_RESET} Undo"
    return "Use"


def go_card_container_style(container_key: str, state: GoCardState) -> str:
    """A ``<style>`` block colouring one keyed container's border per GO state.

    ``render_go_card`` wraps the whole card (header, action button, rule-text
    accordion, any expanded content) in one ``st.container(border=True,
    key=container_key)`` so every part of the card sits inside the same real
    border (S133-D Befund 2). Streamlit's built-in container border only offers
    one fixed theme colour, though — this scoped override (targeting the
    ``st-key-<container_key>`` class Streamlit stamps on that one container,
    see module docstring) is what still gives "ready"/"used" the Gold-Primary
    border and "dormant"/"locked" the dimmed Secondary one (§6.5), without a new
    global CSS rule that would recolour every bordered container on the page.
    """
    border = _STATE_BORDER[state]
    opacity = "0.55" if state in _DIMMED_STATES else "1"
    selector = f".st-key-{_sanitize_key(container_key)}"
    return (
        f"<style>{selector} {{border-color:{border} !important;"
        f"opacity:{opacity} !important;background:{_SURFACE} !important;}}</style>"
    )


def go_card_html(
    name: str,
    cp_cost: int,
    state: GoCardState,
    *,
    keywords: list[str] | None = None,
    compact: bool = False,
    locked_reason: str | None = None,
    target_name: str | None = None,
) -> str:
    """Render one GO card's header content: name/CP/target line + keyword chips.

    name/cp_cost   — the GO's display name and CP cost (0 = free); shown
                     exactly once, on this header line — never repeated on the
                     action button (see :func:`action_slot_text`).
    state          — one of the four states (module docstring); the border
                     colour itself is applied by the caller via
                     :func:`go_card_container_style` on the surrounding
                     ``st.container``, not by this function.
    keywords       — keyword chips (``badges.chip()``, e.g. ``["CORE", "CHARGE"]``);
                     ignored when ``compact`` is True — the compact form is the
                     inline-anchor shape (design_system.md §6.2), which carries
                     no chip row by design (see the §6.3 mockup).
    compact        — full form (default) shows the chip row; compact form omits
                     it for use as an inline anchor next to a table-roll entry
                     or an in-flow trigger.
    locked_reason  — "locked" only: appended to the header as the required
                     suffix explaining why the card is unavailable (§6.1).
    target_name    — the unit this GO would act on, if any (S133-D Befund 3):
                     appended to the header so the player can see WHICH unit is
                     bound before pressing Use — GOs whose effect is unit-scoped
                     (``effect is not None``) but show no target invite spending
                     CP against whatever happens to be selected, unnoticed.

    Contains no clickable element — the caller renders the real Use/Undo button
    itself, using the same label this module also builds via
    :func:`action_slot_text`, and the rule-text accordion.
    """
    header_html = (
        f'<span style="font-weight:600;color:{_TEXT};">{name}</span>'
        f' <span style="color:{_MUTED};">· {cp_cost} CP</span>'
    )
    if target_name:
        header_html += f' <span style="color:{_MUTED};">→ {target_name}</span>'
    if state == "locked" and locked_reason:
        header_html += f' <span style="color:{_MUTED};font-style:italic;"> — {locked_reason}</span>'

    parts = [f"<div>{header_html}</div>"]
    if not compact and keywords:
        chips_html = "".join(chip(kw, _MUTED, _SURFACE, _BORDER) for kw in keywords)
        parts.append(f'<div style="margin-top:4px;">{chips_html}</div>')
    return "".join(parts)
