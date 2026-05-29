"""FightPhaseHandler — Fight Phase for WH40k 9E.

Ziel 3c: can_fight(), Fights-First indicator, full AttackSequence via combat.py.
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_state import _NECRON_UNITS, _ORK_UNITS
from uiLayout._common import PHASE_RULES, lookup, render_attack_form, render_player_column


def can_fight(unit_state: dict) -> bool:  # type: ignore[type-arg]
    """Return True if the unit may fight this turn.

    9E: a unit is eligible to fight if it is in melee or if it charged this turn.
    """
    flags = unit_state.get("turn_flags", {})
    return bool(unit_state.get("in_melee") or flags.get("charged"))


class FightPhaseHandler:
    """PhaseHandler for the Fight Phase."""

    phase_name: str = "fight"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]
        # 9E: non-active player has fight priority and selects a unit to fight first.
        active_player: str = st.session_state.active
        priority_player = second if active_player == first else first

        col1, col2 = st.columns(2)
        with col1:
            if first == priority_player:
                st.info("⚔ Fight Priority — selects first this phase")
            render_player_column(
                first,
                state,
                active_content=_active_fight,
                inactive_content=_inactive_target_stats,
                no_target_caption="← Designate a target (▷) from your army list.",
            )
        with col2:
            if second == priority_player:
                st.info("⚔ Fight Priority — selects first this phase")
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
    """Show fight eligibility, fights-first indicator, and melee weapons."""
    if not can_fight(unit_state):
        st.warning("Not in melee — no fight action possible.")
        return

    fights_first = any(k.lower() == "fights_first" for k in unit.keywords)
    if fights_first:
        st.info("Fights First — this unit activates before others.")

    flags = unit_state.get("turn_flags", {})
    if flags.get("charged"):
        st.markdown("**Fights first** (charged this turn).")

    melee = [w for w in unit.weapons if w.is_melee]
    if melee:
        skill = int(unit.ws.rstrip("+"))
        for w in melee:
            ap_int = int(w.ap)
            ap_str = f"AP{w.ap}" if ap_int != 0 else "AP0"
            st.caption(
                f"**{w.name_en}** · A{w.attacks} · WS{skill}+ "
                f"· S{w.strength} · {ap_str} · D{w.damage}"
            )
    else:
        st.caption("No melee weapons.")

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


def _render_melee_pairs() -> None:
    """Show all active melee engagements, or the phase rule hint if none."""
    name_map = {
        "Necrons": {u.id: u.name_en for u in _NECRON_UNITS},
        "Orks": {u.id: u.name_en for u in _ORK_UNITS},
    }
    seen: set[frozenset[str]] = set()
    pairs: list[str] = []
    for uid, s in st.session_state.necron_units.items():
        for fac, enemy_uid in s.get("melee_with", []):
            key = frozenset({f"Necrons:{uid}", f"{fac}:{enemy_uid}"})
            if key in seen:
                continue
            seen.add(key)
            a = name_map["Necrons"].get(uid, uid)
            b = name_map.get(fac, {}).get(enemy_uid, enemy_uid)
            pairs.append(f"**{a}** ↔ **{b}**")
    if pairs:
        st.markdown("**Active Melee Engagements:**")
        for p in pairs:
            st.markdown(f"- {p}")
    else:
        st.info(PHASE_RULES["fight"])


def _render_display(state: dict) -> None:  # type: ignore[type-arg]
    """Bottom area: attack form when both attacker and target are selected."""
    sel = st.session_state.selected_unit
    tgts: list[tuple[str, str]] = st.session_state.selected_targets
    if sel and tgts:
        atk_faction, atk_uid = sel
        def_faction, def_uid = tgts[0]
        atk_unit, atk_state = lookup(atk_faction, atk_uid)
        def_unit, _ = lookup(def_faction, def_uid)
        if can_fight(atk_state):
            render_attack_form(
                atk_faction,
                atk_uid,
                atk_unit,
                def_faction,
                def_uid,
                def_unit,
                use_melee=True,
                phase_key="fight",
            )
            return
    _render_melee_pairs()
