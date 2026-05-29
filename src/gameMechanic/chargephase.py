"""ChargePhaseHandler — Charge Phase for WH40k 9E.

Ziel 3a: Migrates existing charge UI from gameActionsArea.
Ziel 4:  Overwatch via ShootingAction with hit_modifier="only_6s".
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_log import log_action
from gameMechanic.game_state import _NECRON_UNITS, _ORK_UNITS
from gameMechanic.unit_mutations import enter_melee, set_charged
from uiLayout._common import PHASE_RULES, lookup, render_melee_engagements, render_player_column


class ChargePhaseHandler:
    """PhaseHandler for the Charge Phase."""

    phase_name: str = "charge"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]
        inactive: str = second if state["active"] == first else first

        col1, col2 = st.columns(2)
        with col1:
            render_player_column(
                first,
                state,
                active_content=_active_charge,
                inactive_content=_inactive_charge,
                no_target_caption="← Designate a target (▷) from your army list.",
            )
            if first == inactive:
                _render_heroic_intervention(first, state)
        with col2:
            render_player_column(
                second,
                state,
                active_content=_active_charge,
                inactive_content=_inactive_charge,
                no_target_caption="← Designate a target (▷) from your army list.",
            )
            if second == inactive:
                _render_heroic_intervention(second, state)

        st.divider()
        st.info(PHASE_RULES["charge"])

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


# ---------------------------------------------------------------------------
# Phase-specific content helpers
# ---------------------------------------------------------------------------


def _active_charge(
    faction: str, uid: str, unit, unit_state: dict, state: dict  # type: ignore[type-arg]
) -> None:
    """Render charge action for the active player's selected unit.

    Supports multi-target charges (9E: one or more enemy units within 12").
    Each target is toggled in selected_targets from the enemy army list (▷).
    """
    flags = unit_state.get("turn_flags", {})
    if flags.get("advanced"):
        st.warning("Advanced this turn — cannot charge.")
        return
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


def _render_heroic_intervention(faction: str, state: dict) -> None:  # type: ignore[type-arg]
    """Render Heroic Intervention buttons for eligible CHARACTER units of the inactive player.

    Eligible: not destroyed, not in_melee, CHARACTER keyword, not yet heroic_intervened this turn.
    Ties the intervention to the currently selected active unit (the charger).
    """
    key = "necron_units" if faction == "Necrons" else "ork_units"
    all_units = _NECRON_UNITS if faction == "Necrons" else _ORK_UNITS
    units_data = st.session_state[key]

    eligible = [
        u
        for u in all_units
        if not units_data.get(u.id, {}).get("destroyed")
        and not units_data.get(u.id, {}).get("in_melee")
        and not units_data.get(u.id, {}).get("turn_flags", {}).get("heroic_intervened")
        and "Character" in u.keywords
    ]
    if not eligible:
        return

    charger = st.session_state.get("selected_unit")

    st.markdown("**⚔ Heroic Intervention**")
    for unit in eligible:
        unit_state = units_data[unit.id]
        cols = st.columns([4, 2])
        cols[0].markdown(f"*{unit.name_en}*")
        if cols[1].button("Intervene", key=f"hi_{faction}_{unit.id}"):
            unit_state["turn_flags"]["heroic_intervened"] = True
            if charger:
                charger_faction, charger_uid = charger
                enter_melee(unit.id, faction, charger_uid, charger_faction)
            log_action(
                state["round"],
                "charge",
                unit.name_en,
                "performed Heroic Intervention",
            )
            st.rerun()
