"""ShootingPhaseHandler — Shooting Phase for WH40k 9E.

Ziel 3c: can_shoot(), full AttackSequence via combat.py.
"""

from __future__ import annotations

import streamlit as st

from uiLayout._common import PHASE_RULES, lookup, render_attack_form, render_player_column


def can_shoot(unit_state: dict) -> bool:  # type: ignore[type-arg]
    """Return True if the unit may shoot this turn.

    9E: units that advanced, retreated, are in melee, or in reserve cannot shoot.
    """
    flags = unit_state.get("turn_flags", {})
    return not (
        flags.get("advanced")
        or flags.get("retreated")
        or unit_state.get("in_melee")
        or unit_state.get("in_reserve")
    )


class ShootingPhaseHandler:
    """PhaseHandler for the Shooting Phase."""

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
    """Show shooting eligibility and ranged weapon list for the selected unit."""
    if not can_shoot(unit_state):
        flags = unit_state.get("turn_flags", {})
        if flags.get("advanced"):
            st.warning("Advanced this turn — cannot shoot.")
        elif flags.get("retreated"):
            st.warning("Retreated this turn — cannot shoot.")
        elif unit_state.get("in_melee"):
            st.warning("Bound in melee — cannot shoot.")
        else:
            st.warning("In reserve — cannot shoot.")
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

    tgts: list[tuple[str, str]] = st.session_state.selected_targets
    if not tgts:
        st.caption("Designate a target (▷) to resolve attacks.")


def _inactive_target_stats(
    faction: str, uid: str, unit, unit_state: dict  # type: ignore[type-arg]
) -> None:
    """Show target defensive stats (T / Sv / ++) in the inactive column."""
    inv_display = f"{unit.invuln_save}+" if unit.invuln_save else "—"
    cols = st.columns(3)
    cols[0].metric("T", unit.toughness)
    cols[1].metric("Sv", f"{unit.save}+")
    cols[2].metric("++", inv_display)


def _render_display(state: dict) -> None:  # type: ignore[type-arg]
    """Bottom area: attack form when both attacker and target are selected."""
    sel = st.session_state.selected_unit
    tgts: list[tuple[str, str]] = st.session_state.selected_targets
    if sel and tgts:
        atk_faction, atk_uid = sel
        def_faction, def_uid = tgts[0]
        atk_unit, atk_state = lookup(atk_faction, atk_uid)
        def_unit, _ = lookup(def_faction, def_uid)
        if can_shoot(atk_state):
            render_attack_form(
                atk_faction,
                atk_uid,
                atk_unit,
                def_faction,
                def_uid,
                def_unit,
                use_melee=False,
                phase_key="shooting",
            )
            return
    st.info(PHASE_RULES["shooting"])
