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

from gameMechanic.game_state import PHASES, faction_dir_for, next_phase, swap_players
from gameMechanic.unit_mutations import adjust_secondary_vp, adjust_vp
from gameObjects.loader import get_abilities_for_unit, load_round_choice_abilities
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
            for p in w.profiles:
                profile_label = f"{w.name_en} [{p.name_en}]" if p.name_en else w.name_en
                w_range = "Melee" if p.is_melee else f'{p.range_inches}"'
                ap_str = f"AP{p.ap}" if int(p.ap) != 0 else "AP0"
                abilities_str = f" · *{p.abilities}*" if p.abilities else ""
                atk_display = str(unit.attacks) if p.attacks in ("Melee", None) else p.attacks
                st.caption(
                    f"**{profile_label}** · {w_range} · A{atk_display} · "
                    f"S{p.strength} · {ap_str} · D{p.damage}{abilities_str}"
                )

    faction_dir = unit.id.split(".")[1]
    unit_abilities = get_abilities_for_unit(unit, faction_dir)
    if unit_abilities:
        st.divider()
        st.caption("**Abilities**")
        for ab in unit_abilities:
            st.caption(f"**{ab.name_en}:** {ab.rule_text}")


def _render_protocol_assignment(faction: str) -> None:
    """Assign Command Protocols to rounds 2-5 before the battle. Round 1 is always Eternal Guardian."""
    protocols = load_round_choice_abilities(faction_dir_for(faction))
    if not protocols:
        return

    assignable = [p for p in protocols if not p.auto_round_1]
    auto = next((p for p in protocols if p.auto_round_1), None)

    st.divider()
    st.markdown(f"**{faction} — Command Protocol Order**")
    if auto:
        st.caption(f"Round 1: **{auto.name_de}** *(fixed by rule)*")

    assignments: dict = st.session_state.get("protocol_assignments", {})
    faction_assignments: dict = dict(assignments.get(faction, {}))

    for round_num in range(2, 6):
        already_taken = {v for k, v in faction_assignments.items() if k != round_num}
        available = [p for p in assignable if p.id not in already_taken]
        if not available:
            continue
        current_id = faction_assignments.get(round_num, available[0].id)
        current_idx = next((i for i, p in enumerate(available) if p.id == current_id), 0)
        chosen_idx = st.selectbox(
            f"Round {round_num}",
            options=range(len(available)),
            format_func=lambda i, av=available: av[i].name_de,
            index=current_idx,
            key=f"proto_assign_{faction}_{round_num}",
        )
        faction_assignments[round_num] = available[chosen_idx].id

    assignments[faction] = faction_assignments
    st.session_state.protocol_assignments = assignments


def _render_setup() -> None:
    """Render the setup phase — displayArea first, then player actions below."""
    # Use the original slot order (never swapped) so buttons stay fixed.
    slot_a, slot_b = st.session_state.get("player_slots") or (
        st.session_state.first_player,
        st.session_state.second_player,
    )

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
            f"{slot_a} goes first",
            key="setup_first_p1",
            type="primary" if st.session_state.first_player == slot_a else "secondary",
            use_container_width=True,
        ):
            if st.session_state.first_player != slot_a:
                swap_players()
            st.session_state.active = st.session_state.first_player
            st.rerun()
    with c2:
        if st.button(
            f"{slot_b} goes first",
            key="setup_first_p2",
            type="primary" if st.session_state.first_player == slot_b else "secondary",
            use_container_width=True,
        ):
            if st.session_state.first_player != slot_b:
                swap_players()
            st.session_state.active = st.session_state.first_player
            st.rerun()
    st.caption(f"Currently selected: **{st.session_state.first_player}** goes first.")

    for faction in (slot_a, slot_b):
        _render_protocol_assignment(faction)

    st.divider()
    if st.button("⚔ Start Game", key="setup_start_game", type="primary", use_container_width=True):
        next_phase()
        st.rerun()


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def _render_secondary_vp_section(faction: str, player_key: str) -> None:
    """Render per-objective secondary VP trackers for one player."""
    secondaries: dict = st.session_state.get("secondaries") or {}
    secondary_vp: dict = st.session_state.get("secondary_vp") or {}
    obj_names: list[str] = secondaries.get(player_key, [])
    vp_vals: list[int] = secondary_vp.get(player_key, [0, 0, 0])

    sec_total = sum(vp_vals)
    st.caption(f"Secondary — {sec_total} VP")

    for idx, (name, val) in enumerate(zip(obj_names, vp_vals)):
        col_name, col_minus, col_val, col_plus = st.columns([5, 1, 1, 1])
        col_name.caption(name)
        col_val.markdown(
            f'<div style="text-align:center;font-size:0.9rem;color:#fbbf24;">{val}</div>',
            unsafe_allow_html=True,
        )
        if col_minus.button("−", key=f"sec_m_{faction}_{idx}", use_container_width=True):
            adjust_secondary_vp(player_key, idx, -1)
            st.rerun()
        if col_plus.button("+", key=f"sec_p_{faction}_{idx}", use_container_width=True):
            adjust_secondary_vp(player_key, idx, 1)
            st.rerun()


def _render_vp_scoring() -> None:
    """Contextual VP scoring block — shown only at the configured phase and round."""
    phase_name, phase_key = PHASES[st.session_state.phase_idx]
    current_round: int = st.session_state.get("round", 1)
    vp_phase: str = st.session_state.get("vp_phase", "Morale")
    vp_from_round: int = st.session_state.get("vp_from_round", 1)

    if phase_name != vp_phase or current_round < vp_from_round:
        return

    use_secondaries: bool = st.session_state.get("use_secondaries", False)

    st.divider()
    st.markdown("### Victory Points")

    first = st.session_state.first_player
    second = st.session_state.second_player
    # Map display name → p1/p2 key for secondary_vp lookup
    player_keys = {first: "p1", second: "p2"}

    active = st.session_state.get("active", first)
    inactive = second if active == first else first

    col_active, col_inactive = st.columns(2)

    with col_active:
        primary_vp = st.session_state.vp[active]
        label = "Primary" if use_secondaries else ""
        st.markdown(f"**{active}** — {primary_vp} VP {label}".strip())
        b1, b2, b3, b4 = st.columns(4)
        if b1.button("+5", key=f"vp_p5_{active}"):
            adjust_vp(active, 5)
            st.rerun()
        if b2.button("+1", key=f"vp_p1_{active}"):
            adjust_vp(active, 1)
            st.rerun()
        if b3.button("-1", key=f"vp_m1_{active}"):
            adjust_vp(active, -1)
            st.rerun()
        if b4.button("-5", key=f"vp_m5_{active}"):
            adjust_vp(active, -5)
            st.rerun()
        if use_secondaries:
            _render_secondary_vp_section(active, player_keys[active])

    with col_inactive:
        primary_vp = st.session_state.vp[inactive]
        label = "Primary" if use_secondaries else ""
        st.markdown(f"**{inactive}** — {primary_vp} VP {label}".strip())
        st.caption("(inactive — no scoring)")


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
