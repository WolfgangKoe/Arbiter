"""MovementPhaseHandler — Movement Phase for WH40k 9E.

Ziel 3a: Migrates existing movement UI from gameActionsArea.
Ziel 4:  Full turn_flags tracking, advance-roll, reserve deployment.
"""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_log import log_action
from gameMechanic.game_state import unit_keys_for, units_key_for, units_list_for
from gameMechanic.unit_mutations import set_deployment, set_movement_status
from gameObjects.unit import TriggeredEffect
from uiLayout._common import lookup, render_player_column, render_unit_selectbox


class MovementPhaseHandler:
    """PhaseHandler for the Movement Phase."""

    phase_name: str = "movement"

    def render_start(self, state: dict) -> None:  # type: ignore[type-arg]
        pass

    def render_active(self, state: dict) -> None:  # type: ignore[type-arg]
        first: str = state["first_player"]
        second: str = state["second_player"]

        col1, col2 = st.columns(2)
        with col1:
            render_player_column(first, state, active_content=_active_movement)
            if first == state["active"]:
                _render_reinforcements_step(first)
        with col2:
            render_player_column(second, state, active_content=_active_movement)
            if second == state["active"]:
                _render_reinforcements_step(second)

    def render_end(self, state: dict) -> None:  # type: ignore[type-arg]
        pass


# ---------------------------------------------------------------------------
# Phase-specific content helpers
# ---------------------------------------------------------------------------


def _active_movement(
    faction: str, uid: str, unit, unit_state: dict, state: dict  # type: ignore[type-arg]
) -> None:
    """Render movement type buttons for the active player's selected unit."""
    if unit_state.get("in_reserve"):
        st.caption("In reserve — manage deployment in 'Step 2: Reinforcements' below.")
        return

    in_melee = unit_state.get("in_melee", False)
    current = unit_state.get("movement_choice") or "none"
    flags = unit_state.get("turn_flags", {})

    # Movement was locked by an ability (e.g. teleport) — block normal movement buttons
    if flags.get("movement_locked"):
        st.divider()
        te = unit.get_triggered_effect("phase_start", "movement", "teleport")
        if te:
            _render_teleport_effect(uid, unit, faction, state, unit_state, te)
        else:
            st.info("Movement locked by an ability — cannot change movement status this turn.")
        return

    already_retreated = flags.get("retreated", False)

    if already_retreated:
        st.caption("Already retreated this turn — no further movement possible.")
        return

    st.markdown("Set movement status:")
    options = [
        ("Move", "moved", 'Move up to M"'),
        ("Advance", "advanced", 'M"+D6", no shoot/charge'),
        ("Stay Stationary", "stationary", "Do not move"),
        ("Retreat", "retreated", "Exit melee, no shoot/charge"),
    ]

    for label, value, tip in options:
        disabled = (value in ("moved", "advanced") and in_melee) or (
            value == "retreated" and not in_melee
        )
        btn_type = "primary" if current == value else "secondary"
        if st.button(
            label,
            key=f"mv_{faction}_{uid}_{value}",
            type=btn_type,
            disabled=disabled,
            use_container_width=True,
            help=tip,
        ):
            set_movement_status(uid, faction, value)
            log_action(st.session_state.round, "movement", unit.name_en, f"movement: {value}")
            st.rerun()

    if in_melee:
        st.caption("Unit is in melee — only Stay Stationary or Retreat allowed.")

    te = unit.get_triggered_effect("phase_start", "movement", "teleport")
    if te:
        _render_teleport_effect(uid, unit, faction, state, unit_state, te)


def _render_teleport_effect(
    uid: str,
    unit,  # type: ignore[type-arg]
    faction: str,
    state: dict,  # type: ignore[type-arg]
    unit_state: dict,  # type: ignore[type-arg]
    te: TriggeredEffect,
) -> None:
    """Render a once-per-battle teleport relic UI.

    Step 1: "Prepare" button (disabled if already moved or already used).
    Step 2: Optional CORE unit selector + Confirm/Cancel.
    On confirm: mark bearer + optional CORE unit as moved; lock movement; mark relic used.
    """
    relic_id = unit.relic_id
    display_name = unit.relic_name or relic_id

    st.divider()
    st.markdown(f"**{display_name}**")

    relic_used = st.session_state.get("relic_triggered_used", {})
    if relic_used.get(relic_id):
        if unit_state["turn_flags"].get("movement_locked"):
            st.info(
                f"{display_name} activated this turn — unit and selected CORE unit count as moved."
            )
            if st.button(
                f"Undo {display_name}", key=f"teleport_undo_{uid}", use_container_width=True
            ):
                _undo_teleport(relic_id, faction, state)
        else:
            st.caption("Already used this battle.")
        return

    # Teleport replaces normal move — block if already moved/advanced/retreated
    movement_choice = st.session_state[units_key_for(faction)].get(uid, {}).get("movement_choice")
    if movement_choice in ("moved", "advanced", "retreated"):
        st.caption(f"{display_name} not available — unit has already moved this turn.")
        return

    awaiting = st.session_state.get("veil_awaiting_confirm", False)

    if not awaiting:
        st.caption(
            "Once per battle: remove this unit (and optionally one DYNASTY CORE unit "
            'within 3") from the battlefield and set up both more than 9" from any '
            "enemy models. Both units count as having moved this turn."
        )
        if st.button(
            f"Prepare {display_name}",
            key=f"teleport_prepare_{uid}",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.veil_awaiting_confirm = True
            st.session_state.veil_core_target_uid = None
            st.rerun()
        return

    # ---------------------------------------------------------------------------
    # Step 2 — CORE unit selector
    # ---------------------------------------------------------------------------
    st.info(
        'Verify bearer is within 3" of the target unit on the table. '
        'Both will be set up more than 9" from any enemy models.'
    )

    units_state = st.session_state[units_key_for(faction)]
    all_units = units_list_for(faction)
    all_keys = unit_keys_for(faction)

    # Build (state_key, unit) pairs for CORE candidates — exclude bearer, destroyed, reserve
    core_candidates: list[tuple[str, object]] = []  # type: ignore[type-arg]
    for state_key, cu in zip(all_keys, all_units):
        if cu.id == unit.id:
            continue
        if "CORE" not in cu.keywords:
            continue
        cu_state = units_state.get(state_key, {})
        if cu_state.get("destroyed") or cu_state.get("in_reserve"):
            continue
        core_candidates.append((state_key, cu))

    core_candidates_dicts = [{"uid": sk, "name": cu.name_en} for sk, cu in core_candidates]
    render_unit_selectbox(
        'Optional: select a DYNASTY CORE unit within 3"',
        core_candidates_dicts,
        "veil_core_target_uid",
        none_label="— Bearer only (no second unit) —",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Confirm Teleport", key="veil_confirm", type="primary", use_container_width=True
        ):
            # Mark relic as used (once per battle)
            used = dict(st.session_state.get("relic_triggered_used", {}))
            used[relic_id] = True
            st.session_state.relic_triggered_used = used

            # Mark bearer as moved (locked by teleport ability)
            set_movement_status(uid, faction, "moved")
            _lock_teleport_movement(uid, faction)

            # Mark optional CORE unit as moved — core_uid IS already the state key
            core_uid = st.session_state.get("veil_core_target_uid")
            core_name = ""
            if core_uid:
                set_movement_status(core_uid, faction, "moved")
                _lock_teleport_movement(core_uid, faction)
                core_unit_pair = next(
                    ((sk, cu) for sk, cu in core_candidates if sk == core_uid), None
                )
                core_name = f" + {core_unit_pair[1].name_en}" if core_unit_pair else ""

            log_action(
                state["round"],
                "movement",
                unit.name_en,
                f"{display_name}: teleport{core_name}",
            )
            st.session_state.veil_awaiting_confirm = False
            st.session_state.veil_core_target_uid = None
            st.rerun()
    with col2:
        if st.button("Cancel", key="veil_cancel", use_container_width=True):
            st.session_state.veil_awaiting_confirm = False
            st.session_state.veil_core_target_uid = None
            st.rerun()


def _lock_teleport_movement(state_key: str, faction: str) -> None:
    """Lock a teleported unit's movement and remove it from melee (F7).

    A teleport sets the unit up more than 9" from enemies, so it is no longer in
    Engagement Range. The prior in_melee value is stashed so _undo_teleport can
    restore it while the turn is still running.
    """
    u_state = st.session_state[units_key_for(faction)][state_key]
    u_state["turn_flags"]["movement_locked"] = True
    u_state["turn_flags"]["veil_prev_in_melee"] = u_state.get("in_melee", False)
    u_state["in_melee"] = False


def _undo_teleport(relic_id: str, faction: str, state: dict) -> None:  # type: ignore[type-arg]
    """Undo a confirmed teleport ability (only available within the same turn)."""
    used = dict(st.session_state.get("relic_triggered_used", {}))
    used.pop(relic_id, None)
    st.session_state.relic_triggered_used = used

    # Reset every unit in the faction whose movement was locked by the teleport
    for u_state in st.session_state[units_key_for(faction)].values():
        if u_state.get("turn_flags", {}).get("movement_locked"):
            u_state["turn_flags"]["movement_locked"] = False
            u_state["movement_choice"] = "stationary"
            u_state["movement_chosen"] = False
            # Restore pre-teleport melee state (F7)
            u_state["in_melee"] = u_state["turn_flags"].pop("veil_prev_in_melee", False)

    log_action(state["round"], "movement", "teleport", "undone")
    st.rerun()


def _render_reinforcements_step(faction: str) -> None:
    """Always-visible reinforcements section for the active player."""
    key = units_key_for(faction)
    units_state = st.session_state[key]
    reserve_units = [(uid, us) for uid, us in units_state.items() if us.get("in_reserve")]

    st.markdown("**Step 2: Reinforcements**")

    if not reserve_units:
        st.caption("No reinforcements this round.")
        return

    if st.session_state.round == 1:
        st.caption("Units in reserve — cannot deploy until Round 2.")
        return

    for uid, _ in reserve_units:
        unit, _ = lookup(faction, uid)
        if st.button(
            f"Deploy {unit.name_en} from Reserve",
            key=f"deploy_reserve_{faction}_{uid}",
            type="primary",
            use_container_width=True,
        ):
            set_deployment(uid, faction, "normal")
            set_movement_status(uid, faction, "moved")
            log_action(st.session_state.round, "movement", unit.name_en, "deployed from reserve")
            st.rerun()
