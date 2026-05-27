"""ChargePhaseHandler — Charge Phase for WH40k 9E.

Ziel 3a: Migrates existing charge UI from gameActionsArea.
Ziel 4:  Overwatch via ShootingAction with hit_modifier="only_6s".
"""

from __future__ import annotations

import streamlit as st

from engine import log_action, set_charged
from uiLayout._common import PHASE_RULES, lookup, render_player_column


class ChargePhaseHandler:
    """PhaseHandler for the Charge Phase."""

    phase_name: str = "charge"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]

        col1, col2 = st.columns(2)
        with col1:
            render_player_column(
                first,
                state,
                active_content=_active_charge,
                inactive_content=_inactive_charge,
                no_target_caption="← Designate a target (▷) from your army list.",
            )
        with col2:
            render_player_column(
                second,
                state,
                active_content=_active_charge,
                inactive_content=_inactive_charge,
                no_target_caption="← Designate a target (▷) from your army list.",
            )

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
    """Render charge action for the active player's selected unit."""
    flags = unit_state.get("turn_flags", {})
    if flags.get("advanced") or flags.get("retreated"):
        moved = "Advanced" if flags.get("advanced") else "Retreated"
        st.warning(f"{moved} this turn — cannot charge.")
        return

    tgt = st.session_state.selected_target
    if tgt is None:
        st.info("Select a **target** to charge from the enemy army list (▷).")
        return

    tgt_faction, tgt_uid = tgt
    tgt_unit, _ = lookup(tgt_faction, tgt_uid)
    st.markdown(f"**Target:** {tgt_unit.name_en}")
    st.caption("Roll **2D6** — must equal or beat the distance to the target.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "Charge Successful",
            key=f"charge_ok_{faction}_{uid}",
            type="primary",
            use_container_width=True,
        ):
            set_charged(uid, faction, tgt_uid, tgt_faction)
            log_action(
                st.session_state.round,
                "charge",
                unit.name_en,
                f"charged {tgt_unit.name_en} — success",
            )
            st.session_state.selected_target = None
            st.rerun()
    with c2:
        if st.button("Charge Failed", key=f"charge_fail_{faction}_{uid}", use_container_width=True):
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
