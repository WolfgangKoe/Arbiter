"""unitCard — Passive display card with single selector button.

Design principles (see docs/ui_layout.md §4):
- ONE button per card: the unit name. Clicking it toggles selection.
  - Own unit  → toggles selected_unit
  - Enemy unit → toggles selected_target (shooting / charge / fight phases only)
- No expander, no stats table, no wound buttons.
  Wound adjustments live in the PlayerArea of gameActionsArea.
- Shows: name button · keywords · LP bar (❤) · model bar (⬡) · status badges
- Setup phase exception: deployment selectbox shown inline below name.
"""

import streamlit as st

from engine import PHASES, set_deployment
from gameObjects.unit import Unit

_BADGE_COLORS: dict[str, tuple[str, str]] = {
    "ADVANCED": ("#c9a84c", "#2e2618"),
    "STATIONARY": ("#6b5f44", "#1c1a14"),
    "RETREATED": ("#8b1a1a", "#1e1010"),
    "IN MELEE": ("#cc6644", "#2a1810"),
    "CHARGED": ("#9b59b6", "#1a0a2a"),
    "RESERVE": ("#2a6a8b", "#101820"),
    "DESTROYED": ("#8b1a1a", "#1e1010"),
    "ACTED": ("#3a5a3a", "#101810"),
}

_TARGET_PHASES: frozenset[str] = frozenset({"shooting", "charge", "fight"})


def _badge(text: str) -> str:
    fg, bg = _BADGE_COLORS.get(text, ("#c9a84c", "#2e2618"))
    return (
        f'<span style="background:{bg};border:1px solid {fg};border-radius:2px;'
        f"padding:1px 6px;font-size:10px;color:{fg};letter-spacing:0.06em;"
        f'font-weight:600;margin-right:3px;">{text}</span>'
    )


_MOVEMENT_BADGE: dict[str, str] = {
    "normal": "NORMAL",
    "stationary": "STATIONARY",
    "advanced": "ADVANCED",
    "retreated": "RETREATED",
}


def _state_badges_html(state: dict) -> str:  # type: ignore[type-arg]
    parts: list[str] = []

    # Movement badge — single-choice per turn, None means not yet moved.
    mc = state.get("movement_choice")
    if mc in _MOVEMENT_BADGE:
        parts.append(_badge(_MOVEMENT_BADGE[mc]))

    # Combat badges.
    flags = state.get("turn_flags", {})
    if flags.get("charged"):
        parts.append(_badge("CHARGED"))
    elif state.get("in_melee"):
        parts.append(_badge("IN MELEE"))
    if state.get("in_reserve"):
        parts.append(_badge("RESERVE"))
    return "".join(parts)


def render_unit_card(unit: Unit, state: dict, faction: str) -> None:  # type: ignore[type-arg]
    phase_key = PHASES[st.session_state.phase_idx][1]
    active = st.session_state.active
    is_active = faction == active
    uid = unit.id
    in_reserve = state.get("in_reserve", False)

    # ── Destroyed ─────────────────────────────────────────────
    if state["destroyed"]:
        st.markdown(f"~~{unit.name_en}~~  *DESTROYED*")
        return

    # ── Name / Selector Button ─────────────────────────────────
    if phase_key == "setup":
        # In setup: selector triggers datasheet display in gameActionDisplayArea
        sel = st.session_state.selected_unit
        is_sel = sel == (faction, uid)
        label = f"◀ {unit.name_en}" if is_sel else f"▶ {unit.name_en}"
        if st.button(
            label,
            key=f"sel_{faction}_{uid}",
            type="primary" if is_sel else "secondary",
            use_container_width=True,
        ):
            st.session_state.selected_unit = None if is_sel else (faction, uid)
            st.rerun()

    elif is_active:
        sel = st.session_state.selected_unit
        is_sel = sel == (faction, uid)
        label = f"◀ {unit.name_en}" if is_sel else f"▶ {unit.name_en}"
        if st.button(
            label,
            key=f"sel_{faction}_{uid}",
            type="primary" if is_sel else "secondary",
            use_container_width=True,
            disabled=in_reserve,
        ):
            st.session_state.selected_unit = None if is_sel else (faction, uid)
            st.session_state.selected_targets = []  # clear targets on unit switch
            st.rerun()

    else:
        # Inactive player — target selector for relevant phases
        if phase_key in _TARGET_PHASES:
            tgts: list[tuple[str, str]] = st.session_state.selected_targets
            is_tgt = (faction, uid) in tgts
            label = f"◀ {unit.name_en}" if is_tgt else f"▷ {unit.name_en}"
            if st.button(
                label,
                key=f"tgt_{faction}_{uid}",
                type="primary" if is_tgt else "secondary",
                use_container_width=True,
                disabled=in_reserve,
            ):
                new_tgts = list(tgts)
                if is_tgt:
                    new_tgts.remove((faction, uid))
                else:
                    new_tgts.append((faction, uid))
                st.session_state.selected_targets = new_tgts
                st.rerun()
        else:
            st.markdown(f"**{unit.name_en}**")

    # ── Keywords ──────────────────────────────────────────────
    if unit.keywords:
        kw_html = "".join(
            f'<span style="background:#1c1a14;border:1px solid #2e2618;border-radius:2px;'
            f"padding:1px 5px;font-size:9px;color:#6b5f44;letter-spacing:0.05em;"
            f'margin-right:2px;">{kw}</span>'
            for kw in unit.keywords
        )
        st.markdown(kw_html, unsafe_allow_html=True)

    # ── LP bar (❤) and model bar (⬡) ──────────────────────────
    cur = state["current_wounds"]
    models_alive = state["models"]

    if unit.models_max == 1:
        # Single-model unit: only LP bar
        st.progress(cur / unit.wounds if unit.wounds > 0 else 0)
        st.caption(f"❤ {cur}/{unit.wounds}")
    elif unit.wounds == 1:
        # Multi-model, 1 wound each: only model bar
        st.progress(models_alive / unit.models_max if unit.models_max > 0 else 0)
        st.caption(f"⬡ {models_alive}/{unit.models_max}")
    else:
        # Multi-model, multi-wound: model bar + front-model LP bar
        front_wounds = cur - (models_alive - 1) * unit.wounds if models_alive > 0 else 0
        st.progress(models_alive / unit.models_max)
        st.caption(f"⬡ {models_alive}/{unit.models_max}")
        st.progress(front_wounds / unit.wounds if unit.wounds > 0 else 0)
        st.caption(f"❤ {front_wounds}/{unit.wounds}")

    # ── Status badges ─────────────────────────────────────────
    if phase_key != "setup":
        badges = _state_badges_html(state)
        if badges:
            st.markdown(badges, unsafe_allow_html=True)

    # ── Setup: deployment selector (inline, no expander) ──────
    if phase_key == "setup":
        opts = ["Normal", "Stationary", "Reserve"]
        current = state.get("deployment", "normal").capitalize()
        idx = opts.index(current) if current in opts else 0
        chosen = st.selectbox(
            "Deployment",
            opts,
            index=idx,
            key=f"deploy_{faction}_{uid}",
            label_visibility="collapsed",
        )
        mapping = {"Normal": "normal", "Stationary": "stationary", "Reserve": "reserve"}
        if mapping[chosen] != state.get("deployment", "normal"):
            set_deployment(uid, faction, mapping[chosen])
            st.rerun()
