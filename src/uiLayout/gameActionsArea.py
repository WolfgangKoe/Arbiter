"""gameActionsArea — Center column layout.

Internal layout (see docs/ui_layout.md §7):

  ┌────────────────────────────────────────────────────────┐
  │  firstPlayerArea (50%)  │  secondPlayerArea (50%)       │
  ├────────────────────────────────────────────────────────┤
  │              gameActionDisplayArea (full width)         │
  ├────────────────────────────────────────────────────────┤
  │   gameProtocoll tabs  [CommandProtocol | Stratagems]    │
  └────────────────────────────────────────────────────────┘

All game phases (command → morale) are delegated to phase_runner.
The setup phase is handled locally (it is not a game phase proper).
"""

from __future__ import annotations

import streamlit as st

from engine import PHASES
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

    if unit.abilities:
        st.divider()
        st.caption("**Abilities**")
        st.caption(unit.abilities)


def _render_setup() -> None:
    """Render the setup phase — two empty player columns + setup display area."""
    first = st.session_state.first_player
    second = st.session_state.second_player
    active = st.session_state.active

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        indicator = "▶" if first == active else "◀"
        st.markdown(f"**{indicator} {first}**")
    with col_p2:
        indicator = "▶" if second == active else "◀"
        st.markdown(f"**{indicator} {second}**")

    st.divider()

    # Unit selected → show its datasheet
    sel = st.session_state.selected_unit
    if sel is not None:
        faction, uid = sel
        _display_unit_datasheet(faction, uid)
        return

    # Default: setup instructions + first-player selection
    st.markdown("### Setup")
    st.info(
        "Configure your armies before the battle begins.\n\n"
        "1. **Select first player** — the active player takes their turn first.\n"
        "2. **Set deployment** for each unit using the dropdowns in the unit cards.\n"
        "   - **Normal** — deployed on the battlefield\n"
        "   - **Stationary** — deployed but will not move in turn 1\n"
        "   - **Reserve** — arrives from turn 2 onwards\n\n"
        "Click a unit name (▶) to view its full data profile here.\n\n"
        "When ready, click **→** to begin Battle Round 1."
    )
    st.markdown("---")
    st.markdown("**First Player**")
    c1, c2 = st.columns(2)
    with c1:
        nc_type = "primary" if active == "Necrons" else "secondary"
        if st.button(
            "Necrons go first", key="setup_first_necrons", type=nc_type, use_container_width=True
        ):
            st.session_state.active = "Necrons"
            st.session_state.first_player = "Necrons"
            st.session_state.second_player = "Orks"
            st.rerun()
    with c2:
        ok_type = "primary" if active == "Orks" else "secondary"
        if st.button(
            "Orks go first", key="setup_first_orks", type=ok_type, use_container_width=True
        ):
            st.session_state.active = "Orks"
            st.session_state.first_player = "Orks"
            st.session_state.second_player = "Necrons"
            st.rerun()
    st.caption(f"Currently selected: **{active}** go first.")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def render_game_actions_area() -> None:
    phase_key = PHASES[st.session_state.phase_idx][1]

    if phase_key == "setup":
        _render_setup()
        return

    # All game phases delegated to phase_runner.
    from gameMechanic.phase_runner import render_current_phase  # noqa: PLC0415

    render_current_phase(st.session_state)
