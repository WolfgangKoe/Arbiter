from __future__ import annotations

import streamlit as st

from gameMechanic.ability_engine import get_triggered_abilities
from gameMechanic.game_log import log_action
from gameMechanic.phase_handler import PhaseHandler  # noqa: F401 — used for type checking
from gameMechanic.unit_mutations import adjust_cp
from gameObjects.ability import Ability
from gameObjects.loader import load_army
from gameObjects.unit import Unit
from uiLayout._common import PHASE_RULES, lookup, state_badges_html, wound_adjustment_buttons

_OVERLORD_ID = "wh40k_9e.necrons.unit.overlord"


def apply_living_metal(unit_state: dict, unit: Unit) -> bool:  # type: ignore[type-arg]
    max_alive = unit_state["models"] * unit.wounds
    if unit_state["current_wounds"] < max_alive:
        unit_state["current_wounds"] += 1
        return True
    return False


def resolve_command_start(state: dict) -> list[tuple[Ability, list[str]]]:  # type: ignore[type-arg]
    return get_triggered_abilities(state, "command", "phase_start")


def _render_faction_actions(
    faction: str,
    state: dict,  # type: ignore[type-arg]
    units_state: dict,  # type: ignore[type-arg]
    unit_by_id: dict,  # type: ignore[type-arg]
) -> None:
    """CP-Grant + Living Metal — always visible for the active faction."""
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

    living_metal_units = [
        uid
        for uid, ustate in units_state.items()
        if not ustate.get("destroyed", False)
        and uid in unit_by_id
        and "livingMetal" in unit_by_id[uid].rules
        and ustate["current_wounds"] < unit_by_id[uid].wounds * ustate["models"]
    ]
    if living_metal_units:
        st.divider()
        n = len(living_metal_units)
        st.markdown(f"**Living Metal** — {n} unit{'s' if n > 1 else ''} eligible")
        if st.button("Apply Living Metal", key="cmd_living_metal", use_container_width=True):
            healed = sum(
                1
                for uid in living_metal_units
                if apply_living_metal(units_state[uid], unit_by_id[uid])
            )
            log_action(state["round"], "command", faction, f"Living Metal: {healed} unit(s) healed")
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
    else:
        core_units = [
            u
            for u in unit_by_id.values()
            if "Core" in u.keywords and not units_state.get(u.id, {}).get("destroyed")
        ]
        if not core_units:
            st.caption("No CORE units available.")
        else:
            pending = st.session_state.get("mwbd_pending_uid")
            for u in core_units:
                is_sel = pending == u.id
                label = f"◀ {u.name_en}" if is_sel else f"▶ {u.name_en}"
                if st.button(
                    label,
                    key=f"mwbd_pick_{u.id}",
                    type="primary" if is_sel else "secondary",
                    use_container_width=True,
                ):
                    st.session_state.mwbd_pending_uid = None if is_sel else u.id
                    st.rerun()
            if pending and pending in unit_by_id:
                if st.button(
                    "Activate My Will Be Done",
                    key="cmd_mwbd",
                    type="primary",
                    use_container_width=True,
                ):
                    units_state[pending]["my_will_be_done_active"] = True
                    st.session_state.mwbd_target_uid = pending
                    st.session_state.mwbd_pending_uid = None
                    st.session_state.mwbd_active_since_round = state["round"]
                    log_action(
                        state["round"],
                        "command",
                        "Overlord",
                        f"My Will Be Done → {unit_by_id[pending].name_en}",
                    )
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
            wound_adjustment_buttons("Necrons", res_orb_target, target_unit)
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
    else:
        alive_units = [
            u
            for u in unit_by_id.values()
            if not units_state.get(u.id, {}).get("destroyed") and u.id != _OVERLORD_ID
        ]
        if alive_units:
            st.caption('Select target unit (verify within 6" on table):')
            pending_orb = st.session_state.get("res_orb_pending_uid")
            for u in alive_units:
                is_sel = pending_orb == u.id
                label = f"◀ {u.name_en}" if is_sel else f"▷ {u.name_en}"
                if st.button(
                    label,
                    key=f"res_orb_pick_{u.id}",
                    type="primary" if is_sel else "secondary",
                    use_container_width=True,
                ):
                    st.session_state.res_orb_pending_uid = None if is_sel else u.id
                    st.rerun()
            if pending_orb:
                if st.button(
                    "Use Resurrection Orb",
                    key="cmd_res_orb",
                    type="primary",
                    use_container_width=True,
                ):
                    st.session_state.res_orb_target_uid = pending_orb
                    st.session_state.res_orb_pending_uid = None
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
        wound_adjustment_buttons(faction, uid, unit)
        st.divider()

    faction_dir = "necrons" if faction == "Necrons" else "orks"
    units = load_army(faction_dir)
    unit_by_id = {u.id: u for u in units}
    units_key = "necron_units" if faction == "Necrons" else "ork_units"
    units_state: dict = state[units_key]  # type: ignore[type-arg]

    _render_faction_actions(faction, state, units_state, unit_by_id)

    if faction == "Necrons":
        overlord_alive = _OVERLORD_ID in units_state and not units_state[_OVERLORD_ID].get(
            "destroyed"
        )
        if overlord_alive and sel == (faction, _OVERLORD_ID):
            _render_overlord_actions(state, units_state, unit_by_id)
