"""gameActionsArea — Center column layout.

Internal layout (see docs/spec/ui_layout.md §7):

  ┌────────────────────────────────────────────────────────┐
  │              gameActionDisplayArea (full width)         │
  │  context first: phase rules, attack summary, VP score  │
  ├────────────────────────────────────────────────────────┤
  │  firstPlayerArea (50%)  │  secondPlayerArea (50%)       │
  │  actions + reactions    │  actions + reactions          │
  ├────────────────────────────────────────────────────────┤
  │   gameProtocoll tabs  [CommandProtocol | Stratagems]    │
  └────────────────────────────────────────────────────────┘

All game phases (command → morale) are delegated to phase_runner.
The setup phase is handled locally (it is not a game phase proper).
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_state import PHASES, next_phase
from gameMechanic.unit_mutations import adjust_vp
from gameObjects.loader import get_abilities_for_unit
from uiLayout._common import lookup

# ---------------------------------------------------------------------------
# Setup phase rendering
# ---------------------------------------------------------------------------


def _display_unit_datasheet(faction: str, uid: str) -> None:
    """Show a unit's full data profile — used in setup phase."""
    unit, _ = lookup(faction, uid)

    st.markdown(f"### {unit.name_en}")
    st.caption(faction + (f" · {unit.subfaction}" if unit.subfaction else ""))

    if unit.keywords:
        kw_html = "".join(
            f'<span style="background:#1c1a14;border:1px solid #2e2618;border-radius:2px;'
            f"padding:1px 5px;font-size:9px;color:#6b5f44;letter-spacing:0.05em;"
            f'margin-right:2px;">{kw}</span>'
            for kw in unit.keywords
        )
        st.markdown(kw_html, unsafe_allow_html=True)

    st.divider()

    stat_cols = st.columns(7)
    for col, lbl, val in zip(
        stat_cols,
        ["M", "T", "Sv", "W", "++", "Ld", "OC"],
        [
            f'{unit.move}"',
            unit.toughness,
            f"{unit.save}+",
            unit.wounds,
            f"{unit.invuln_save}+" if unit.invuln_save else "—",
            unit.leadership,
            unit.oc,
        ],
    ):
        col.metric(lbl, val)

    st.divider()

    if unit.weapons:
        st.caption("**Weapons**")
        for w in unit.weapons:
            w_range = "Melee" if w.is_melee else f'{w.range_inches}"'
            ap_str = f"AP{w.ap}" if int(w.ap) != 0 else "AP0"
            abilities_str = f" · *{w.abilities}*" if w.abilities else ""
            st.caption(
                f"**{w.name_en}** · {w_range} · A{w.attacks} · "
                f"S{w.strength} · {ap_str} · D{w.damage}{abilities_str}"
            )

    faction_dir = "necrons" if "necrons" in unit.id else "orks"
    unit_abilities = get_abilities_for_unit(unit, faction_dir)
    if unit_abilities:
        st.divider()
        st.caption("**Abilities**")
        for ab in unit_abilities:
            st.caption(f"**{ab.name_en}:** {ab.rule_text}")


def _render_setup() -> None:
    """Render the setup phase — displayArea first, then player actions below."""
    active = st.session_state.active
    p1 = st.session_state.first_player
    p2 = st.session_state.second_player

    # ── displayArea: datasheet (unit selected) or instructions ────────
    sel = st.session_state.selected_unit
    if sel is not None:
        faction, uid = sel
        _display_unit_datasheet(faction, uid)
    else:
        st.markdown("### Setup")
        st.info(
            "Configure your armies before the battle begins.\n\n"
            "1. **Select first player** — the active player takes their turn first.\n"
            "2. **Set deployment** for each unit using the dropdowns in the unit cards.\n"
            "   - **Normal** — deployed on the battlefield\n"
            "   - **Stationary** — deployed but will not move in turn 1\n"
            "   - **Reserve** — arrives from turn 2 onwards\n\n"
            "Click a unit name (▶) to view its full data profile here.\n\n"
            "When ready, click **⚔ Start Game** below."
        )

    st.divider()

    # ── PlayerArea: first-player selection + Start Game ───────────────
    st.markdown("**First Player**")
    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            f"{p1} goes first",
            key="setup_first_p1",
            type="primary" if active == p1 else "secondary",
            use_container_width=True,
        ):
            st.session_state.active = p1
            st.rerun()
    with c2:
        if st.button(
            f"{p2} goes first",
            key="setup_first_p2",
            type="primary" if active == p2 else "secondary",
            use_container_width=True,
        ):
            st.session_state.active = p2
            st.rerun()
    st.caption(f"Currently selected: **{active}** goes first.")

    st.divider()
    if st.button("⚔ Start Game", key="setup_start_game", type="primary", use_container_width=True):
        next_phase()
        st.rerun()


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def _render_vp_scoring() -> None:
    """Contextual VP scoring block — shown only at the configured phase and round."""
    phase_name, phase_key = PHASES[st.session_state.phase_idx]
    current_round: int = st.session_state.get("round", 1)
    vp_phase: str = st.session_state.get("vp_phase", "Morale")
    vp_from_round: int = st.session_state.get("vp_from_round", 1)

    if phase_name != vp_phase or current_round < vp_from_round:
        return

    st.divider()
    st.markdown("### Victory Points")

    first = st.session_state.first_player
    second = st.session_state.second_player

    col1, col2 = st.columns(2)
    for col, faction in ((col1, first), (col2, second)):
        with col:
            st.markdown(f"**{faction}** — {st.session_state.vp[faction]} VP")
            b1, b2, b3, b4 = st.columns(4)
            if b1.button("+5", key=f"vp_p5_{faction}"):
                adjust_vp(faction, 5)
                st.rerun()
            if b2.button("+1", key=f"vp_p1_{faction}"):
                adjust_vp(faction, 1)
                st.rerun()
            if b3.button("-1", key=f"vp_m1_{faction}"):
                adjust_vp(faction, -1)
                st.rerun()
            if b4.button("-5", key=f"vp_m5_{faction}"):
                adjust_vp(faction, -5)
                st.rerun()


def render_game_actions_area() -> None:
    phase_key = PHASES[st.session_state.phase_idx][1]

    if phase_key == "setup":
        _render_setup()
        return

    # displayArea first: VP scoring buttons appear at top when active
    _render_vp_scoring()

    # PlayerAreas below: phase-specific actions delegated to phase_runner
    from gameMechanic.phase_runner import render_current_phase  # noqa: PLC0415

    render_current_phase(st.session_state)
