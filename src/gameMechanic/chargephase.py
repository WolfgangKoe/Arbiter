"""ChargePhaseHandler — Charge Phase for WH40k 9E.

9E rules (core_rules.txt Z. 1824–1848):
- Step 1: Active player charges with eligible units (one at a time).
- Step 2: After all charges, inactive player's CHARACTER units within 3" may
  perform Heroic Intervention — up to 3" move, must end closer to nearest enemy.
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_log import log_action
from gameMechanic.game_state import units_key_for, units_list_for
from gameMechanic.unit_mutations import enter_melee, set_charged
from uiLayout._common import lookup, render_melee_engagements, render_player_column


class ChargePhaseHandler:
    """PhaseHandler for the Charge Phase."""

    phase_name: str = "charge"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]
        active: str = state["active"]
        inactive: str = second if active == first else first
        step: int = st.session_state.get("charge_phase_step", 1)

        if step == 1:
            col1, col2 = st.columns(2)
            with col1:
                render_player_column(
                    first,
                    state,
                    active_content=_active_charge,
                    inactive_content=_inactive_charge,
                    no_target_caption="← Designate a target (▷) from your army list.",
                    show_wound_buttons=False,
                )
            with col2:
                render_player_column(
                    second,
                    state,
                    active_content=_active_charge,
                    inactive_content=_inactive_charge,
                    no_target_caption="← Designate a target (▷) from your army list.",
                    show_wound_buttons=False,
                )

            st.divider()
            if st.button(
                "All Charges Done — Proceed to Heroic Interventions →",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.charge_phase_step = 2
                st.session_state.selected_unit = None
                st.session_state.selected_targets = []
                st.rerun()
        else:
            _render_hi_phase(inactive, active, state)

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


# ---------------------------------------------------------------------------
# Step 1 helpers — normal charge
# ---------------------------------------------------------------------------


def _active_charge(
    faction: str, uid: str, unit, unit_state: dict, state: dict  # type: ignore[type-arg]
) -> None:
    """Render charge action for the active player's selected unit."""
    flags = unit_state.get("turn_flags", {})
    if flags.get("advanced"):
        from gameMechanic.ability_engine import charge_after_advance_allowed  # noqa: PLC0415

        if not charge_after_advance_allowed(faction, unit):
            st.warning("Advanced this turn — cannot charge.")
            return
        st.caption("Advance & Charge active (faction ability).")
    if flags.get("retreated"):
        st.warning("Retreated this turn — cannot charge.")
        return
    if unit_state.get("in_melee"):
        st.warning("Already in melee — cannot charge.")
        render_melee_engagements(faction, uid, unit_state)
        return

    tgts: list[tuple[str, str]] = st.session_state.selected_targets
    if not tgts:
        st.info("Select one or more **targets** to charge from the enemy army list (▷).")
        return

    for tgt_faction, tgt_uid in tgts:
        tgt_unit, _ = lookup(tgt_faction, tgt_uid)
        st.markdown(f"**Target:** {tgt_unit.name_en}")

    st.caption("Roll **2D6** — must equal or beat the distance to the closest target model.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "Charge Successful",
            key=f"charge_ok_{faction}_{uid}",
            type="primary",
            use_container_width=True,
        ):
            for tgt_faction, tgt_uid in tgts:
                tgt_unit, _ = lookup(tgt_faction, tgt_uid)
                set_charged(uid, faction, tgt_uid, tgt_faction)
                log_action(
                    st.session_state.round,
                    "charge",
                    unit.name_en,
                    f"charged {tgt_unit.name_en} — success",
                )
            st.session_state.selected_targets = []
            st.rerun()
    with c2:
        if st.button("Charge Failed", key=f"charge_fail_{faction}_{uid}", use_container_width=True):
            for tgt_faction, tgt_uid in tgts:
                tgt_unit, _ = lookup(tgt_faction, tgt_uid)
                log_action(
                    st.session_state.round,
                    "charge",
                    unit.name_en,
                    f"charged {tgt_unit.name_en} — failed",
                )
            st.info("Charge failed — no movement.")


def _inactive_charge(
    faction: str, uid: str, unit, unit_state: dict  # type: ignore[type-arg]
) -> None:
    """Inactive player target view for Charge Phase."""
    st.caption("Overwatch: only unmodified 6s hit.")


# ---------------------------------------------------------------------------
# Step 2 helpers — Heroic Intervention
# ---------------------------------------------------------------------------


def _render_hi_phase(inactive: str, active: str, state: dict) -> None:  # type: ignore[type-arg]
    """Step 2: Heroic Intervention window for the inactive player."""
    st.markdown("### ⚔ Heroic Intervention")
    st.info(
        "Inactive player's CHARACTER units not in melee, within 3\" of an enemy, "
        'may move up to 3" — must end closer to the nearest enemy model.'
    )
    st.divider()

    pending = st.session_state.get("pending_hi")
    if pending:
        _render_hi_target_selection(pending, active, state)
        return

    key = units_key_for(inactive)
    all_units = units_list_for(inactive)
    units_data = st.session_state[key]

    eligible = [
        u
        for u in all_units
        if not units_data.get(u.id, {}).get("destroyed")
        and not units_data.get(u.id, {}).get("in_melee")
        and not units_data.get(u.id, {}).get("turn_flags", {}).get("heroic_intervened")
        and u.has_keyword("CHARACTER")
    ]

    if not eligible:
        st.info("No eligible CHARACTER units — Heroic Intervention not possible.")
    else:
        for unit in eligible:
            cols = st.columns([4, 2])
            cols[0].markdown(f"*{unit.name_en}*")
            if cols[1].button("Intervene", key=f"hi_{inactive}_{unit.id}"):
                st.session_state.pending_hi = (inactive, unit.id)
                st.session_state.hi_targets = []
                st.rerun()


def _render_hi_target_selection(
    pending: tuple,  # type: ignore[type-arg]
    active: str,
    state: dict,  # type: ignore[type-arg]
) -> None:
    """Show enemy unit selector for the intervening CHARACTER unit."""
    hi_faction, hi_uid = pending
    hi_unit, _ = lookup(hi_faction, hi_uid)
    hi_targets: list[str] = st.session_state.get("hi_targets", [])

    st.markdown(f"**{hi_unit.name_en}** — select enemy units to engage:")
    st.caption("Tap a unit to toggle; confirm when ready.")

    active_units = units_list_for(active)
    active_data = st.session_state[units_key_for(active)]

    for enemy in active_units:
        if active_data.get(enemy.id, {}).get("destroyed"):
            continue
        is_sel = enemy.id in hi_targets
        prefix = "✓ " if is_sel else ""
        if st.button(f"{prefix}{enemy.name_en}", key=f"hi_tgt_{active}_{enemy.id}"):
            if is_sel:
                hi_targets.remove(enemy.id)
            else:
                hi_targets.append(enemy.id)
            st.session_state.hi_targets = hi_targets
            st.rerun()

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "Confirm Intervention",
            type="primary",
            disabled=not hi_targets,
            use_container_width=True,
        ):
            hi_state = st.session_state[units_key_for(hi_faction)][hi_uid]
            hi_state["turn_flags"]["heroic_intervened"] = True
            for tgt_uid in hi_targets:
                enter_melee(hi_uid, hi_faction, tgt_uid, active)
            log_action(
                state["round"],
                "charge",
                hi_unit.name_en,
                f"Heroic Intervention — engaged {len(hi_targets)} unit(s)",
            )
            st.session_state.pending_hi = None
            st.session_state.hi_targets = []
            st.rerun()
    with c2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.pending_hi = None
            st.session_state.hi_targets = []
            st.rerun()
