"""ShootingPhaseHandler — Shooting Phase for WH40k 9E.

Ziel 3c: can_shoot(), full AttackSequence via combat.py.
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_state import units_key_for
from uiLayout._common import PHASE_RULES, lookup, render_attack_form, render_player_column


def can_shoot(unit_state: dict, unit=None) -> bool:  # type: ignore[type-arg]
    """Return True if the unit may shoot this turn.

    9E: units that advanced, retreated, are in melee (unless VEHICLE/MONSTER), or in reserve
    cannot shoot. VEHICLE and MONSTER units may shoot even while in melee (Big Guns Never Tire).
    """
    flags = unit_state.get("turn_flags", {})
    if flags.get("advanced") or flags.get("retreated") or unit_state.get("in_reserve"):
        return False
    if unit_state.get("in_melee"):
        if unit is not None and ("Vehicle" in unit.keywords or "Monster" in unit.keywords):
            return True
        return False
    return True


def target_in_friendly_melee(atk_faction: str, def_faction: str, def_uid: str) -> bool:
    """Return True if the target is in melee with a unit friendly to the attacker.

    9E: a unit may not shoot into a combat involving friendly units.
    """
    def_key = units_key_for(def_faction)
    def_state = st.session_state[def_key].get(def_uid, {})
    return any(fac == atk_faction for fac, _ in def_state.get("melee_with", []))


class ShootingPhaseHandler:
    """PhaseHandler for the Shooting Phase."""

    phase_name: str = "shooting"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]

        _render_display(state)
        st.divider()

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

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


# ---------------------------------------------------------------------------
# Phase-specific content helpers
# ---------------------------------------------------------------------------


def _active_shooting(
    faction: str, uid: str, unit, unit_state: dict, state: dict  # type: ignore[type-arg]
) -> None:
    """Show shooting eligibility and ranged weapon list for the selected unit."""
    if not can_shoot(unit_state, unit):
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

    ranged = [w for w in unit.weapons if any(not p.is_melee for p in w.profiles)]
    if ranged:
        skill = int(unit.bs.rstrip("+"))
        for w in ranged:
            p = w.for_phase(use_melee=False)
            ap_int = int(p.ap)
            ap_str = f"AP{p.ap}" if ap_int != 0 else "AP0"
            st.caption(
                f"**{w.name_en}** · A{p.attacks} · BS{skill}+ "
                f"· S{p.strength} · {ap_str} · D{p.damage}"
            )
    else:
        st.caption("No ranged weapons.")

    tgts: list[tuple[str, str]] = st.session_state.selected_targets
    if not tgts:
        st.caption("Designate a target (▷) to resolve attacks.")
    else:
        for tgt_faction, tgt_uid in tgts:
            if target_in_friendly_melee(faction, tgt_faction, tgt_uid):
                tgt_unit, _ = lookup(tgt_faction, tgt_uid)
                st.warning(
                    f"Cannot shoot {tgt_unit.name_en} — friendly unit is engaged in that melee."
                )


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
        if can_shoot(atk_state, atk_unit) and not target_in_friendly_melee(
            atk_faction, def_faction, def_uid
        ):
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
