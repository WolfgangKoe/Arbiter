"""gameActionsArea — Center column layout.

Internal layout (see docs/spec/ui_layout.md §7):

  ┌────────────────────────────────────────────────────────┐
  │              gameActionDisplayArea (full width)         │
  │  context first: phase rules, attack summary, VP score  │
  ├────────────────────────────────────────────────────────┤
  │  firstPlayerArea (50%)  │  secondPlayerArea (50%)       │
  │  actions + reactions    │  actions + reactions          │
  ├────────────────────────────────────────────────────────┤
  │   gameProtocoll tabs  [Stratagems | Battle Log]         │
  └────────────────────────────────────────────────────────┘

All game phases (command → morale) are delegated to phase_runner.
The setup phase is handled locally (it is not a game phase proper).
"""

from __future__ import annotations

import streamlit as st

from constants.symbols import SYM_EXPAND, SYM_SWORDS
from gameMechanic.game_state import PHASES, faction_dir_for, next_phase, swap_players
from gameMechanic.unit_mutations import adjust_secondary_vp, adjust_vp
from gameObjects.loader import (
    get_abilities_for_unit,
    load_round_choice_abilities,
    load_round_choice_label,
)
from uiLayout._common import PHASE_RULES, lookup
from uiLayout.badges import chip

# ---------------------------------------------------------------------------
# Setup phase rendering
# ---------------------------------------------------------------------------


def _display_unit_datasheet(faction: str, uid: str) -> None:
    """Show a unit's full data profile — used in setup phase."""
    unit, _ = lookup(faction, uid)

    st.markdown(f"### {unit.name_en}")
    st.caption(faction + (f" · {unit.subfaction}" if unit.subfaction else ""))

    if unit.keywords:
        kw_html = "".join(chip(kw, "#6b5f44", "#1c1a14", "#2e2618") for kw in unit.keywords)
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
                ap_str = f"AP{p.ap}" if p.ap != 0 else "AP0"
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


def _round_choice_slots_after_swap(slots: dict, slot, new_val: str) -> dict:  # type: ignore[type-arg]
    """Return a new slot→ability map after putting new_val in slot.

    The map is a bijection (each ability in exactly one slot). Assigning an
    ability that already sits in another slot swaps the two, so any ability can
    be moved into any slot (round or the always-active 6th) and the displaced one
    takes the slot the chosen ability came from.
    """
    result = dict(slots)
    old_val = result.get(slot)
    if new_val == old_val:
        return result
    for other, pid in list(result.items()):
        if other != slot and pid == new_val:
            result[other] = old_val
            break
    result[slot] = new_val
    return result


def _swap_round_choice_slot(faction: str, slot) -> None:  # type: ignore[no-untyped-def]
    """on_change callback: swap abilities between slots, keeping the map a bijection."""
    slots_key = f"proto_slots_{faction}"
    widget_key = f"proto_slot_{faction}_{slot}"
    slots = _round_choice_slots_after_swap(
        st.session_state.get(slots_key, {}), slot, st.session_state[widget_key]
    )
    st.session_state[slots_key] = slots
    # Keep every slot's selectbox in sync with the swapped map.
    for s, pid in slots.items():
        st.session_state[f"proto_slot_{faction}_{s}"] = pid


def _render_round_choice_assignment(faction: str) -> None:
    """Pre-assign round-choice abilities (Command Protocols, Ka'tahs) to slots.

    Six abilities fill six slots: rounds 1–5 plus the always-active 6th
    (Necron Command Protocols rule). Every slot is a dropdown over all abilities;
    picking one already placed elsewhere swaps the two, so the player can freely
    reorder them across rounds and the 6th slot. Identities are fixed at
    setup — mid-game the 6th can only change via a dedicated ability (e.g. the
    Silent King's Voice of the Triarch).
    """
    faction_dir = faction_dir_for(faction)
    round_choices = load_round_choice_abilities(faction_dir)
    if not round_choices:
        return

    st.divider()
    st.markdown(f"**{faction} — {load_round_choice_label(faction_dir)}**")

    by_id = {p.id: p for p in round_choices}
    ids = [p.id for p in round_choices]

    # Seed the bijection once: keep any existing round assignments, leftover = 6th.
    slots_key = f"proto_slots_{faction}"
    if slots_key not in st.session_state:
        faction_assignments = st.session_state.get("round_choice_assignments", {}).get(faction, {})
        slots: dict = {}
        used: set = set()
        for r in range(1, 6):
            pid = faction_assignments.get(r)
            if pid in by_id and pid not in used:
                slots[r] = pid
                used.add(pid)
        remaining = iter(pid for pid in ids if pid not in used)
        for r in range(1, 6):
            if r not in slots:
                nxt = next(remaining, None)
                if nxt is not None:
                    slots[r] = nxt
        extra = next(remaining, None)
        if extra is not None:
            slots["extra"] = extra
        st.session_state[slots_key] = slots

    slots = st.session_state[slots_key]

    def _slot_selectbox(slot, label: str) -> None:  # type: ignore[no-untyped-def]
        if slot not in slots:
            return
        widget_key = f"proto_slot_{faction}_{slot}"
        if widget_key not in st.session_state:
            st.session_state[widget_key] = slots[slot]
        st.selectbox(
            label,
            options=ids,
            format_func=lambda pid: by_id[pid].name_de,
            key=widget_key,
            on_change=_swap_round_choice_slot,
            args=(faction, slot),
        )

    _slot_selectbox("extra", "Always active (6th)")
    for round_num in range(1, 6):
        _slot_selectbox(round_num, f"Round {round_num}")

    # Persist round assignments for the rest of the app; the 6th is the leftover.
    assignments = dict(st.session_state.get("round_choice_assignments", {}))
    assignments[faction] = {r: slots[r] for r in range(1, 6) if r in slots}
    st.session_state.round_choice_assignments = assignments


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
            f"Click a unit name ({SYM_EXPAND}) to view its full data profile here.\n\n"
            f"When ready, click **{SYM_SWORDS} Start Game** below."
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
        _render_round_choice_assignment(faction)

    st.divider()
    if st.button(
        f"{SYM_SWORDS} Start Game",
        key="setup_start_game",
        type="primary",
        use_container_width=True,
    ):
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

    # Phase rule box always at the very top — every phase, every state
    rule = PHASE_RULES.get(phase_key)
    if rule:
        st.info(rule)

    # PlayerAreas: phase-specific actions delegated to phase_runner
    from gameMechanic.phase_runner import render_current_phase  # noqa: PLC0415

    render_current_phase(st.session_state)

    # VP scoring at the bottom — scoring happens at the end of a phase
    _render_vp_scoring()
