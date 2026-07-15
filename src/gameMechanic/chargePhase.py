"""ChargePhaseHandler — Charge Phase for WH40k 9E.

9E rules (core_rules.txt Z. 1824–1848):
- Step 1: Active player charges with eligible units (one at a time).
- Step 2: After all charges, inactive player's CHARACTER units within 3" may
  perform Heroic Intervention — up to 3" move, must end closer to nearest enemy.
"""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any, ClassVar

import streamlit as st

from constants.symbols import SYM_CHECK, SYM_EXPAND_ALT, SYM_SWORDS
from gameMechanic.gameLog import log_action
from gameMechanic.gameState import unit_keys_for, units_key_for, units_list_for
from gameMechanic.unitMutations import perform_heroic_intervention, set_charged
from gameObjects.unit import Unit
from uiLayout._common import (
    lookup,
    render_inline_command_reroll,
    render_melee_engagements,
    render_player_column,
    render_reactive_stratagem_box,
)


class ChargePhaseHandler:
    """PhaseHandler for the Charge Phase."""

    phase_name: ClassVar[str] = "charge"

    def render_active(self, state: MutableMapping[str, Any]) -> None:
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
                    no_target_caption=f"← Designate a target ({SYM_EXPAND_ALT}) from your army list.",
                    show_wound_buttons=False,
                )
            with col2:
                render_player_column(
                    second,
                    state,
                    active_content=_active_charge,
                    inactive_content=_inactive_charge,
                    no_target_caption=f"← Designate a target ({SYM_EXPAND_ALT}) from your army list.",
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


# ---------------------------------------------------------------------------
# Step 1 helpers — normal charge
# ---------------------------------------------------------------------------


def _active_charge(
    faction: str,
    uid: str,
    unit: Unit,
    unit_state: MutableMapping[str, Any],
    state: MutableMapping[str, Any],
) -> None:
    """Render charge action for the active player's selected unit."""
    flags = unit_state.get("turn_flags", {})
    if flags.get("advanced"):
        from gameMechanic.abilityEngine import charge_after_advance_allowed  # noqa: PLC0415

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
        st.info(
            f"Select one or more **targets** to charge from the enemy army list ({SYM_EXPAND_ALT})."
        )
        return

    for tgt_faction, tgt_uid in tgts:
        tgt_unit, _ = lookup(tgt_faction, tgt_uid)
        st.markdown(f"**Target:** {tgt_unit.name_en}")

    st.caption("Roll **2D6** — must equal or beat the distance to the closest target model.")
    # Re-Roll offer sits before the Successful/Failed decision — the app never
    # captured the roll value, so there is nothing to reopen on reroll.
    render_inline_command_reroll(faction, "charge", reopen_key=uid, on_reroll=lambda: None)

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
    faction: str, uid: str, unit: Unit, unit_state: MutableMapping[str, Any]
) -> None:
    """Inactive player target view for Charge Phase.

    This is exactly the Fire Overwatch reactive window (core_rules.txt Z. 1907-1934,
    3240): the enemy has declared `unit` a charge target but the charge roll has not
    been made yet (rendered as long as `unit` stays in `selected_targets` — the
    Charge Successful/Failed buttons clear that list once the roll is resolved).

    A unit already in Engagement Range cannot fire Overwatch at all
    (rules_appendix.txt Z. 2319-2323) — the GO box is not offered in that case.
    """
    if unit_state.get("in_melee"):
        return
    charger = st.session_state.get("selected_unit")
    charger_name = ""
    if charger:
        charger_unit, _ = lookup(*charger)
        charger_name = charger_unit.name_en
    render_reactive_stratagem_box(
        faction,
        phase="charge",
        event="on_declaration",
        decline_key=uid,
        context_caption=f"{unit.name_en} was declared a charge target"
        + (f" by {charger_name}." if charger_name else "."),
        unit_for_conditions=unit,
    )


# ---------------------------------------------------------------------------
# Step 2 helpers — Heroic Intervention
# ---------------------------------------------------------------------------


def hi_already_performed(unit_state: MutableMapping[str, Any]) -> bool:
    """Return True when the unit has already performed a Heroic Intervention this phase.

    Implements the once-per-enemy-Charge-Phase guard from R-CHARGE-10.
    """
    return bool(unit_state.get("turn_flags", {}).get("heroic_intervened"))


def hi_eligible_units(
    all_units: list, unit_keys: list[str], units_data: MutableMapping[str, Any]  # type: ignore[type-arg]
) -> list[tuple]:  # type: ignore[type-arg]
    """Return (Unit, state_key) pairs eligible for Heroic Intervention.

    Eligibility (App-enforced portion of R-CHARGE-09 / R-CHARGE-10):
    - Not destroyed.
    - Not already in melee (in_melee is False).
    - Has not already performed a Heroic Intervention this enemy Charge Phase
      (heroic_intervened flag is False).
    - Has the CHARACTER keyword.

    The 3"/5" proximity condition is table-side only and not checked here.
    Uses STATE KEYS (not unit.id) so duplicate squads are handled correctly.
    """
    return [
        (u, ukey)
        for u, ukey in zip(all_units, unit_keys)
        if not units_data.get(ukey, {}).get("destroyed")
        and not units_data.get(ukey, {}).get("in_melee")
        and not hi_already_performed(units_data.get(ukey, {}))
        and u.has_keyword("CHARACTER")
    ]


def _render_hi_phase(inactive: str, active: str, state: MutableMapping[str, Any]) -> None:
    """Step 2: Heroic Intervention window for the inactive player."""
    st.markdown(f"### {SYM_SWORDS} Heroic Intervention")
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
    unit_keys = unit_keys_for(inactive)
    units_data = st.session_state[key]

    eligible = hi_eligible_units(all_units, unit_keys, units_data)

    if not eligible:
        st.info("No eligible CHARACTER units — Heroic Intervention not possible.")
    else:
        for unit, ukey in eligible:
            cols = st.columns([4, 2])
            cols[0].markdown(f"*{unit.name_en}*")
            if cols[1].button("Intervene", key=f"hi_{inactive}_{ukey}"):
                st.session_state.pending_hi = (inactive, ukey)
                st.session_state.hi_targets = []
                st.rerun()


def _render_hi_target_selection(
    pending: tuple,  # type: ignore[type-arg]
    active: str,
    state: MutableMapping[str, Any],
) -> None:
    """Show enemy unit selector for the intervening CHARACTER unit."""
    hi_faction, hi_key = pending
    hi_unit, _ = lookup(hi_faction, hi_key)
    hi_targets: list[str] = st.session_state.get("hi_targets", [])

    st.markdown(f"**{hi_unit.name_en}** — select enemy units to engage:")
    st.caption("Tap a unit to toggle; confirm when ready.")

    active_data = st.session_state[units_key_for(active)]

    for enemy, ekey in zip(units_list_for(active), unit_keys_for(active)):
        if active_data.get(ekey, {}).get("destroyed"):
            continue
        is_sel = ekey in hi_targets
        prefix = f"{SYM_CHECK} " if is_sel else ""
        if st.button(f"{prefix}{enemy.name_en}", key=f"hi_tgt_{active}_{ekey}"):
            if is_sel:
                hi_targets.remove(ekey)
            else:
                hi_targets.append(ekey)
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
            perform_heroic_intervention(
                hi_faction,
                hi_key,
                active,
                hi_targets,
                state["round"],
                hi_unit.name_en,
            )
            st.session_state.pending_hi = None
            st.session_state.hi_targets = []
            st.rerun()
    with c2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.pending_hi = None
            st.session_state.hi_targets = []
            st.rerun()
