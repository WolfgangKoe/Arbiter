"""FightPhaseHandler — Fight Phase for WH40k 9E.

Ziel 3a: Stub — migrates existing fight-display UI from gameActionsArea.
          No combat resolution yet (uses old manual log).
Ziel 3c: Full AttackSequence via combat.py, can_fight(), params_from_melee_attack(),
          Fights-First ordering.
"""

from __future__ import annotations

import streamlit as st

from engine import log_action, wound_threshold
from uiLayout._common import PHASE_RULES, lookup, render_player_column


class FightPhaseHandler:
    """PhaseHandler for the Fight Phase.

    NOTE: This is a Ziel-3a stub. Full combat resolution comes in Ziel 3c.
    """

    phase_name: str = "fight"

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
                active_content=_active_fight,
                inactive_content=_inactive_target_stats,
                no_target_caption="← Designate a target (▷) from your army list.",
            )
        with col2:
            render_player_column(
                second,
                state,
                active_content=_active_fight,
                inactive_content=_inactive_target_stats,
                no_target_caption="← Designate a target (▷) from your army list.",
            )

        st.divider()
        _render_display(state)

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


# ---------------------------------------------------------------------------
# Phase-specific content helpers
# ---------------------------------------------------------------------------


def _active_fight(
    faction: str, uid: str, unit, unit_state: dict, state: dict  # type: ignore[type-arg]
) -> None:
    """Render fight actions for the active player's selected unit."""
    flags = unit_state.get("turn_flags", {})
    if flags.get("charged"):
        st.markdown("**Fights first** (charged this turn).")

    if not unit_state.get("in_melee"):
        st.warning("Not in melee — no action possible.")
        return

    tgt = st.session_state.selected_target
    if tgt is None:
        st.info("Select a **target** in melee from the enemy army list (▷).")
        return

    tgt_faction, tgt_uid = tgt
    tgt_unit, _ = lookup(tgt_faction, tgt_uid)
    melee = [w for w in unit.weapons if w.is_melee]
    if not melee:
        st.caption("No melee weapons.")
        return

    skill = int(unit.ws.rstrip("+"))
    for w in melee:
        ap_int = int(w.ap)
        ap_str = f"AP{w.ap}" if ap_int != 0 else "AP0"
        st.caption(
            f"**{w.name_en}** · A{w.attacks} · WS{skill}+ · S{w.strength} · {ap_str} · D{w.damage}"
        )
    if st.button("Log Fight Action", key=f"log_fight_{faction}_{uid}", use_container_width=True):
        log_action(st.session_state.round, "fight", unit.name_en, f"fought {tgt_unit.name_en}")
        st.success("Action logged.")


def _inactive_target_stats(
    faction: str, uid: str, unit, unit_state: dict  # type: ignore[type-arg]
) -> None:
    """Show target stats (T/Sv/++) in the inactive player area."""
    inv_display = f"{unit.invuln_save}+" if unit.invuln_save else "—"
    cols = st.columns(3)
    cols[0].metric("T", unit.toughness)
    cols[1].metric("Sv", f"{unit.save}+")
    cols[2].metric("++", inv_display)


def _render_display(state: dict) -> None:  # type: ignore[type-arg]
    """Display area — attack reference when attacker and target are selected."""
    sel = st.session_state.selected_unit
    tgt = st.session_state.selected_target
    if sel and tgt:
        _display_attack_summary(sel, tgt, phase_key="fight")
        return
    st.info(PHASE_RULES["fight"])


def _display_attack_summary(
    sel: tuple[str, str],
    tgt: tuple[str, str],
    phase_key: str,
) -> None:
    """Attack reference table shown when attacker and target are both selected."""
    atk_faction, atk_uid = sel
    def_faction, def_uid = tgt
    atk_unit, _ = lookup(atk_faction, atk_uid)
    def_unit, _ = lookup(def_faction, def_uid)

    weapons = [w for w in atk_unit.weapons if w.is_melee]
    if not weapons:
        st.info(PHASE_RULES[phase_key])
        return

    st.markdown(f"**{atk_unit.name_en}** → **{def_unit.name_en}**")
    st.markdown("*Attack reference (roll dice on the table):*")

    skill = int(atk_unit.ws.rstrip("+"))
    inv_display = f"{def_unit.invuln_save}+" if def_unit.invuln_save else "none"

    for w in weapons:
        thresh = wound_threshold(int(w.strength), def_unit.toughness)
        eff_save = def_unit.save + abs(int(w.ap))
        if def_unit.invuln_save and def_unit.invuln_save < eff_save:
            eff_save = def_unit.invuln_save
        save_str = f"{eff_save}+" if eff_save <= 6 else "none"
        st.caption(
            f"**{w.name_en}**: {w.attacks} att · WS{skill}+ · "
            f"wound {thresh}+ · save {save_str} (++ {inv_display}) · D{w.damage}"
        )

    if st.button(
        "Log Fight Action",
        key=f"log_fight_display_{atk_faction}_{atk_uid}",
        use_container_width=True,
    ):
        log_action(
            st.session_state.round,
            "fight",
            atk_unit.name_en,
            f"fought {def_unit.name_en}",
        )
        st.success("Action logged.")
