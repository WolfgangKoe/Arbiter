from __future__ import annotations

import streamlit as st

from gameMechanic.ability_engine import get_triggered_abilities
from gameMechanic.game_log import log_action
from gameMechanic.game_state import faction_dir_for, is_necron_faction, units_key_for
from gameMechanic.phase_handler import PhaseHandler  # noqa: F401 — used for type checking
from gameMechanic.unit_mutations import adjust_cp
from gameObjects.ability import Ability
from gameObjects.loader import load_army, load_command_protocols
from uiLayout._common import PHASE_RULES, lookup, state_badges_html, wound_adjustment_buttons

_OVERLORD_ID = "wh40k_9e.necrons.unit.overlord"


def resolve_command_start(state: dict) -> list[tuple[Ability, list[str]]]:  # type: ignore[type-arg]
    return get_triggered_abilities(state, "command", "phase_start")


def _render_faction_actions(
    faction: str,
    state: dict,  # type: ignore[type-arg]
) -> None:
    """CP-Grant — Living Metal has moved to armyCard."""
    st.divider()
    st.markdown(f"**+1 CP for {faction}**")
    already_granted = st.session_state.get("cp_granted_this_phase", False)
    if already_granted:
        st.caption("Already granted this phase.")
    else:
        if st.button("Grant +1 CP", key="cmd_cp", type="primary", use_container_width=True):
            adjust_cp(faction, 1)
            log_action(state["round"], "command", faction, "+1 CP received")
            st.session_state.cp_granted_this_phase = True
            st.rerun()


def _render_overlord_actions(
    state: dict,  # type: ignore[type-arg]
    units_state: dict,  # type: ignore[type-arg]
    unit_by_id: dict,  # type: ignore[type-arg]
) -> None:
    """MWBD + Resurrection Orb — only rendered when Overlord is selected."""
    # Reset MWBD at the start of the next Necron Command Phase.
    mwbd_set_round = st.session_state.get("mwbd_active_since_round")
    if mwbd_set_round is not None and state["round"] > mwbd_set_round:
        mwbd_prev = st.session_state.get("mwbd_target_uid")
        if mwbd_prev and mwbd_prev in units_state:
            units_state[mwbd_prev]["my_will_be_done_active"] = False
        st.session_state.mwbd_target_uid = None
        st.session_state.mwbd_active_since_round = None

    # ── My Will Be Done ───────────────────────────────────────────────────────
    st.divider()
    st.markdown("**My Will Be Done**")

    mwbd_target = st.session_state.get("mwbd_target_uid")
    if mwbd_target and units_state.get(mwbd_target, {}).get("my_will_be_done_active"):
        target_unit = unit_by_id.get(mwbd_target)
        st.success(
            f"Active — **{target_unit.name_en if target_unit else mwbd_target}** "
            "gets +1 to hit until your next Command Phase."
        )
    elif st.session_state.get("mwbd_awaiting_target", False):
        st.info("Select a CORE unit from your army list.")
        if st.button("Cancel", key="mwbd_cancel", use_container_width=True):
            st.session_state.mwbd_awaiting_target = False
            st.rerun()
    else:
        if st.button(
            "Activate My Will Be Done",
            key="cmd_mwbd",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.mwbd_awaiting_target = True
            st.session_state.res_orb_awaiting_target = False
            st.rerun()

    # ── Resurrection Orb ──────────────────────────────────────────────────────
    st.divider()
    st.markdown("**Resurrection Orb**")

    if state.get("resurrection_orb_used", False):
        st.caption("Already used this battle.")
        return

    res_orb_target = st.session_state.get("res_orb_target_uid")
    if res_orb_target:
        target_unit = unit_by_id.get(res_orb_target)
        if target_unit:
            st.caption(f'Target: **{target_unit.name_en}** — verify within 6" on table')
            wound_adjustment_buttons(
                st.session_state.get("active", ""), res_orb_target, target_unit
            )
        if st.button(
            "Confirm & Close Resurrection Orb",
            key="cmd_res_orb_confirm",
            use_container_width=True,
        ):
            name = target_unit.name_en if target_unit else res_orb_target
            state["resurrection_orb_used"] = True
            log_action(state["round"], "command", "Overlord", f"Resurrection Orb → {name}")
            st.session_state.res_orb_target_uid = None
            st.rerun()
    elif st.session_state.get("res_orb_awaiting_target", False):
        st.info("Select a target unit from your army list.")
        if st.button("Cancel", key="res_orb_cancel", use_container_width=True):
            st.session_state.res_orb_awaiting_target = False
            st.rerun()
    else:
        if st.button(
            "Use Resurrection Orb",
            key="cmd_res_orb",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.res_orb_awaiting_target = True
            st.session_state.mwbd_awaiting_target = False
            st.rerun()


def _render_command_protocols(faction: str, state: dict) -> None:  # type: ignore[type-arg]
    if not is_necron_faction(faction):
        return

    protocols = load_command_protocols(faction_dir_for(faction))
    if not protocols:
        return

    st.divider()
    st.markdown("**Kommandoprotokolle**")

    active_id = st.session_state.get("active_protocol_id")
    used_ids = st.session_state.get("used_protocol_ids", [])
    current_round = state.get("round", 1)

    if current_round == 1:
        p = next((p for p in protocols if p.id == "eternal_guardian"), None)
        if p:
            st.caption(f"{p.name_de} — automatisch aktiv (Runde 1)")
            st.caption(f"Direktive 1: {p.primary}")
            st.caption(f"Direktive 2: {p.secondary}")
        return

    if active_id:
        p = next((p for p in protocols if p.id == active_id), None)
        if p:
            st.caption(f"{p.name_de} — aktiv diese Runde")
            st.caption(f"Direktive 1: {p.primary}")
            st.caption(f"Direktive 2: {p.secondary}")
        return

    available = [p for p in protocols if p.id not in used_ids]
    if not available:
        st.caption("Alle Protokolle wurden bereits eingesetzt.")
        return

    choice = st.radio(
        "Protokoll wählen:",
        options=range(len(available)),
        format_func=lambda i: available[i].name_de,
        key="cmd_protocol_choice",
    )
    if st.button(
        "Protokoll aktivieren",
        key="cmd_protocol_activate",
        type="primary",
        use_container_width=True,
    ):
        chosen = available[choice]
        st.session_state.active_protocol_id = chosen.id
        st.session_state.used_protocol_ids = used_ids + [chosen.id]
        log_action(state["round"], "command", faction, f"Protocol: {chosen.name_de}")
        st.rerun()


# ---------------------------------------------------------------------------
# PhaseHandler implementation
# ---------------------------------------------------------------------------


class CommandPhaseHandler:
    """PhaseHandler for the Command Phase."""

    phase_name: str = "command"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]

        col1, col2 = st.columns(2)
        with col1:
            _render_command_column(first, state)
        with col2:
            _render_command_column(second, state)

        st.divider()
        st.info(PHASE_RULES["command"])

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


def _render_command_column(faction: str, state: dict) -> None:  # type: ignore[type-arg]
    is_active = faction == state["active"]
    indicator = "▶" if is_active else "◀"
    st.markdown(f"**{indicator} {faction}**")

    if not is_active:
        st.caption("—")
        return

    sel = st.session_state.selected_unit

    if sel and sel[0] == faction:
        _, uid = sel
        unit, unit_state = lookup(faction, uid)
        badges = state_badges_html(unit_state)
        st.markdown(f"*{unit.name_en}*")
        if badges:
            st.markdown(badges, unsafe_allow_html=True)
        st.divider()

    units, _ = load_army(faction_dir_for(faction))
    unit_by_id = {u.id: u for u in units}
    units_key = units_key_for(faction)
    units_state: dict = state[units_key]  # type: ignore[type-arg]

    _render_faction_actions(faction, state)
    _render_command_protocols(faction, state)

    if is_necron_faction(faction):
        overlord_alive = _OVERLORD_ID in units_state and not units_state[_OVERLORD_ID].get(
            "destroyed"
        )
        if overlord_alive and sel == (faction, _OVERLORD_ID):
            _render_overlord_actions(state, units_state, unit_by_id)
