"""ShootingPhaseHandler — Shooting Phase for WH40k 9E.

Ziel 3a: Stub — migrates existing weapon-display UI from gameActionsArea.
          No combat resolution yet (uses old manual log).
Ziel 3c: Full AttackSequence via combat.py, can_shoot(), params_from_ranged_attack().
"""

from __future__ import annotations

import streamlit as st

from engine import log_action, wound_threshold
from uiLayout._common import PHASE_RULES, lookup, render_player_column


class ShootingPhaseHandler:
    """PhaseHandler for the Shooting Phase.

    NOTE: This is a Ziel-3a stub. Full combat resolution comes in Ziel 3c.
    """

    phase_name: str = "shooting"

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
                active_content=_active_shooting,
                inactive_content=_inactive_target_stats,
                no_target_caption="← Designate a target (▷) from your army list.",
            )
        with col2:
            render_player_column(
                second,
                state,
                active_content=_active_shooting,
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


def _active_shooting(
    faction: str, uid: str, unit, unit_state: dict, state: dict  # type: ignore[type-arg]
) -> None:
    """Render shooting actions for the active player's selected unit."""
    flags = unit_state.get("turn_flags", {})
    if flags.get("advanced"):
        st.warning("Advanced this turn — cannot shoot.")
        return
    if flags.get("retreated"):
        st.warning("Retreated this turn — cannot shoot.")
        return
    if unit_state.get("in_melee"):
        st.warning("Bound in melee — cannot shoot.")
        return

    ranged = [w for w in unit.weapons if not w.is_melee]
    if ranged:
        skill = int(unit.bs.rstrip("+"))
        for w in ranged:
            ap_int = int(w.ap)
            ap_str = f"AP{w.ap}" if ap_int != 0 else "AP0"
            st.caption(
                f"**{w.name_en}** · A{w.attacks} · BS{skill}+ "
                f"· S{w.strength} · {ap_str} · D{w.damage}"
            )
    else:
        st.caption("No ranged weapons.")


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
    """Display area — attack reference when attacker and a target are selected."""
    sel = st.session_state.selected_unit
    tgts: list[tuple[str, str]] = st.session_state.selected_targets
    if sel and tgts:
        # Show reference for the first selected target (Ziel 3c will handle per-weapon targeting).
        _display_attack_summary(sel, tgts[0], phase_key="shooting")
        return
    st.info(PHASE_RULES["shooting"])


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

    use_melee = phase_key == "fight"
    weapons = [w for w in atk_unit.weapons if w.is_melee == use_melee]
    if not weapons:
        st.info(PHASE_RULES[phase_key])
        return

    st.markdown(f"**{atk_unit.name_en}** → **{def_unit.name_en}**")
    st.markdown("*Attack reference (roll dice on the table):*")

    skill = int(atk_unit.ws.rstrip("+")) if use_melee else int(atk_unit.bs.rstrip("+"))
    skill_label = "WS" if use_melee else "BS"
    inv_display = f"{def_unit.invuln_save}+" if def_unit.invuln_save else "none"

    for w in weapons:
        thresh = wound_threshold(int(w.strength), def_unit.toughness)
        eff_save = def_unit.save + abs(int(w.ap))
        if def_unit.invuln_save and def_unit.invuln_save < eff_save:
            eff_save = def_unit.invuln_save
        save_str = f"{eff_save}+" if eff_save <= 6 else "none"
        st.caption(
            f"**{w.name_en}**: {w.attacks} att · {skill_label}{skill}+ · "
            f"wound {thresh}+ · save {save_str} (++ {inv_display}) · D{w.damage}"
        )

    if st.button(
        "Log Shooting Action",
        key=f"log_shooting_{atk_faction}_{atk_uid}",
        use_container_width=True,
    ):
        log_action(
            st.session_state.round,
            "shooting",
            atk_unit.name_en,
            f"shot at {def_unit.name_en}",
        )
        st.success("Action logged.")
