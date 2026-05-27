from __future__ import annotations

from collections.abc import Callable

import streamlit as st

from gameMechanic.ability_engine import get_triggered_abilities
from gameMechanic.phase_handler import PhaseHandler  # noqa: F401 — used for type checking
from gameObjects.ability import Ability
from gameObjects.loader import load_army
from gameObjects.unit import Unit
from uiLayout._common import PHASE_RULES, lookup, state_badges_html, wound_adjustment_buttons

# Resolved lazily to avoid circular imports at module load time.
_adjust_cp: Callable | None = None
_log_action: Callable | None = None


def _engine_funcs() -> tuple[Callable, Callable]:
    global _adjust_cp, _log_action
    if _adjust_cp is None:
        from engine import adjust_cp, log_action  # noqa: PLC0415

        _adjust_cp = adjust_cp
        _log_action = log_action
    return _adjust_cp, _log_action  # type: ignore[return-value]


def apply_living_metal(unit_state: dict, unit: Unit) -> bool:  # type: ignore[type-arg]
    """Heal 1 wound if unit has lost wounds. Cap uses models_remaining to prevent dead model recall."""
    max_alive = unit_state["models"] * unit.wounds
    if unit_state["current_wounds"] < max_alive:
        unit_state["current_wounds"] += 1
        return True
    return False


def apply_buff_roll(ability: Ability, unit_id: str, session_state: dict) -> None:  # type: ignore[type-arg]
    faction_key = "necron_units" if session_state["active"] == "Necrons" else "ork_units"
    session_state[faction_key][unit_id]["my_will_be_done_active"] = True


def _apply_resurrection_orb(target_uid: str, session_state: dict) -> None:  # type: ignore[type-arg]
    pass  # RP resolution deferred to Ziel 3


COMPLEX_HANDLERS: dict[str, Callable] = {
    "resurrectionOrb": _apply_resurrection_orb,
}


def resolve_command_start(state: dict) -> list[tuple[Ability, list[str]]]:  # type: ignore[type-arg]
    return get_triggered_abilities(state, "command", "phase_start")


def render_actions_command(state: dict) -> None:  # type: ignore[type-arg]
    adjust_cp, log_action = _engine_funcs()
    active: str = state["active"]
    faction_dir = "necrons" if active == "Necrons" else "orks"
    units = load_army(faction_dir)
    unit_by_id = {u.id: u for u in units}

    units_key = "necron_units" if active == "Necrons" else "ork_units"
    units_state: dict = state[units_key]  # type: ignore[type-arg]

    # +1 CP (Battle-Forged)
    st.divider()
    st.markdown(f"**+1 CP for {active}**")
    if st.button("Grant +1 CP", key="cmd_cp", type="primary", use_container_width=True):
        adjust_cp(active, 1)
        log_action(state["round"], "command", active, "+1 CP received")
        st.rerun()

    # Living Metal — button heals all eligible units at once
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
            log_action(state["round"], "command", active, f"Living Metal: {healed} unit(s) healed")
            st.rerun()

    # Necron-specific: My Will Be Done + Resurrection Orb (Overlord)
    if active != "Necrons":
        return

    overlord_id = "wh40k_9e.necrons.unit.overlord"
    if overlord_id not in units_state or units_state[overlord_id].get("destroyed"):
        return

    # My Will Be Done
    st.divider()
    st.markdown("**My Will Be Done**")
    if units_state[overlord_id].get("my_will_be_done_active", False):
        st.success("Active — +1 to hit for selected CORE unit.")
    else:
        if st.button("Activate My Will Be Done", key="cmd_mwbd", use_container_width=True):
            units_state[overlord_id]["my_will_be_done_active"] = True
            log_action(state["round"], "command", "Overlord", "My Will Be Done activated")
            st.rerun()

    # Resurrection Orb
    st.divider()
    st.markdown("**Resurrection Orb**")
    if state.get("resurrection_orb_used", False):
        st.caption("Already used this battle.")
    else:
        if st.button("Use Resurrection Orb", key="cmd_res_orb", use_container_width=True):
            state["resurrection_orb_used"] = True
            log_action(state["round"], "command", "Overlord", "Resurrection Orb used")
            st.success("Resurrection Orb used — enact Reanimation Protocols for target unit.")
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
    """Render the command phase column for one player."""
    is_active = faction == state["active"]
    indicator = "▶" if is_active else "◀"
    st.markdown(f"**{indicator} {faction}**")

    if is_active:
        # Show selected unit context (badges) if any, then army-wide actions.
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
        render_actions_command(state)
    else:
        st.caption("—")
