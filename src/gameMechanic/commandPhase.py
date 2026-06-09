from __future__ import annotations

import streamlit as st

from gameMechanic.ability_engine import get_activated_command_abilities, get_triggered_abilities
from gameMechanic.game_log import log_action
from gameMechanic.game_state import (
    faction_dir_for,
    unit_id_from_state_key,
    units_key_for,
    units_list_for,
)
from gameMechanic.phase_handler import PhaseHandler  # noqa: F401 — used for type checking
from gameMechanic.unit_mutations import adjust_cp
from gameObjects.ability import Ability
from uiLayout._common import (
    PHASE_RULES,
    lookup,
    state_badges_html,
    wound_adjustment_buttons,
)

_RES_ORB_ID = "wh40k_9e.necrons.wargear.resurrection_orb"


def resolve_command_start(state: dict) -> list[tuple[Ability, list[str]]]:  # type: ignore[type-arg]
    return get_triggered_abilities(state, "command", "phase_start")


# ---------------------------------------------------------------------------
# CP grant
# ---------------------------------------------------------------------------


def _render_faction_actions(
    faction: str,
    state: dict,  # type: ignore[type-arg]
) -> None:
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


# ---------------------------------------------------------------------------
# Generic buff_roll ability renderer
# ---------------------------------------------------------------------------


def _render_buff_roll_ability(
    ability: Ability,
    faction: str,
    state: dict,  # type: ignore[type-arg]
    units_state: dict,  # type: ignore[type-arg]
    unit_by_id: dict,  # type: ignore[type-arg]
) -> None:
    """Render activate / status UI for any buff_roll command-phase ability."""
    ability_id = ability.id
    cmd_state: dict = st.session_state.get("command_ability_state", {})  # type: ignore[type-arg]
    this_state: dict = cmd_state.get(ability_id, {})  # type: ignore[type-arg]

    target_uid: str | None = this_state.get("target_uid")
    active_since_round: int | None = this_state.get("active_since_round")

    # Expire when a new command phase begins (round has advanced)
    if active_since_round is not None and state["round"] > active_since_round:
        if target_uid and target_uid in units_state:
            bufs: list[dict] = units_state[target_uid].get("active_buffs", [])
            units_state[target_uid]["active_buffs"] = [
                b for b in bufs if b.get("ability_id") != ability_id
            ]
        cmd_state[ability_id] = {}
        st.session_state.command_ability_state = cmd_state
        target_uid = None

    st.divider()
    st.markdown(f"**{ability.name_en}**")

    awaiting = st.session_state.get("cmd_awaiting_ability_id") == ability_id

    already_active = target_uid and any(
        b.get("ability_id") == ability_id
        for b in units_state.get(target_uid, {}).get("active_buffs", [])
    )
    if already_active:
        target_unit = unit_by_id.get(unit_id_from_state_key(target_uid))
        name = target_unit.name_en if target_unit else target_uid
        effect_desc = "re-roll 1s to hit" if ability.effect.type == "reroll_hit_1" else "+1 to hit"
        st.success(f"Active — **{name}** {effect_desc} until your next Command Phase.")
    elif awaiting:
        st.info("Select an eligible unit from your army list.")
        if st.button("Cancel", key=f"cmd_cancel_{ability_id}", use_container_width=True):
            st.session_state.cmd_awaiting_ability_id = None
            st.rerun()
    else:
        if st.button(
            f"Activate {ability.name_en}",
            key=f"cmd_activate_{ability_id}",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.cmd_awaiting_ability_id = ability_id
            st.session_state.cmd_awaiting_required_kw = [
                kw for cond in ability.conditions for kw in (cond.has_keywords or [])
            ]
            st.session_state.cmd_awaiting_badge_label = ability.badge_label or ability.name_en
            st.session_state.cmd_awaiting_effect_type = ability.effect.type
            st.session_state.res_orb_awaiting_target = False
            st.rerun()


# ---------------------------------------------------------------------------
# gain_cp_roll — relic triggered effect: roll a die, gain CP on threshold+
# ---------------------------------------------------------------------------


def _render_gain_cp_roll(unit, faction: str, state: dict) -> None:  # type: ignore[type-arg]
    from gameObjects.unit import TriggeredEffect  # local import avoids circular dep

    te: TriggeredEffect | None = unit.get_triggered_effect("phase_start", "command", "gain_cp_roll")
    if not te:
        return

    display_name = unit.relic_name or unit.relic_id
    threshold = te.threshold or 4
    amount = te.amount or 1
    fail_label = f"1–{threshold - 1} (Failed)"
    success_label = f"{threshold}+ (Success)"

    st.divider()
    st.markdown(f"**{display_name}**")
    if st.session_state.get("morgog_cap_rolled_this_phase"):
        st.caption("Already rolled this Command Phase.")
        return
    st.caption(f"Roll {te.dice or 'D6'}: on a {threshold}+, gain {amount} CP.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            success_label,
            key=f"cp_roll_success_{unit.relic_id}",
            type="primary",
            use_container_width=True,
        ):
            adjust_cp(faction, amount)
            log_action(
                state["round"], "command", faction, f"{display_name}: {threshold}+ — +{amount} CP"
            )
            st.session_state.morgog_cap_rolled_this_phase = True
            st.rerun()
    with col2:
        if st.button(fail_label, key=f"cp_roll_fail_{unit.relic_id}", use_container_width=True):
            log_action(state["round"], "command", faction, f"{display_name}: failed — no CP")
            st.session_state.morgog_cap_rolled_this_phase = True
            st.rerun()


# ---------------------------------------------------------------------------
# Resurrection Orb — wargear, separate from unit_abilities system
# ---------------------------------------------------------------------------


def _render_resurrection_orb(
    faction: str,
    state: dict,  # type: ignore[type-arg]
    units_state: dict,  # type: ignore[type-arg]
    unit_by_id: dict,  # type: ignore[type-arg]
    bearer_uid: str = "",
) -> None:
    st.divider()
    st.markdown("**Resurrection Orb**")

    if st.session_state.wargear_used.get(_RES_ORB_ID, False):
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
            st.session_state.wargear_used[_RES_ORB_ID] = True
            log_action(state["round"], "command", "Overlord", f"Resurrection Orb → {name}")
            st.session_state.res_orb_target_uid = None
            st.rerun()
    elif st.session_state.get("res_orb_awaiting_target", False):
        st.info("Select a target unit from your army list.")
        if st.button("Cancel", key="res_orb_cancel", use_container_width=True):
            st.session_state.res_orb_awaiting_target = False
            st.session_state.wargear_awaiting_bearer_uid = None
            st.rerun()
    else:
        if st.button(
            "Use Resurrection Orb",
            key="cmd_res_orb",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.res_orb_awaiting_target = True
            st.session_state.wargear_awaiting_bearer_uid = bearer_uid
            st.session_state.cmd_awaiting_ability_id = None
            st.rerun()


# ---------------------------------------------------------------------------
# Generic unit command-phase ability renderer
# ---------------------------------------------------------------------------


def _render_unit_command_abilities(
    selected_state_key: str,
    faction: str,
    state: dict,  # type: ignore[type-arg]
    units_state: dict,  # type: ignore[type-arg]
    unit_by_id: dict,  # type: ignore[type-arg]
) -> None:
    """Render all activated command-phase abilities for the currently selected unit."""
    unit_id = unit_id_from_state_key(selected_state_key)
    faction_dir = faction_dir_for(faction)
    abilities = get_activated_command_abilities(unit_id, faction_dir)

    for ability in abilities:
        if ability.effect.type in ("buff_roll", "reroll_hit_1"):
            _render_buff_roll_ability(ability, faction, state, units_state, unit_by_id)

    unit = unit_by_id.get(unit_id)
    if unit and _RES_ORB_ID in unit.wargear_ids:
        _render_resurrection_orb(faction, state, units_state, unit_by_id, selected_state_key)
    if unit and unit.get_triggered_effect("phase_start", "command", "gain_cp_roll"):
        _render_gain_cp_roll(unit, faction, state)


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

        st.info(PHASE_RULES["command"])
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            _render_command_column(first, state)
        with col2:
            _render_command_column(second, state)

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

    unit_by_id = {u.id: u for u in units_list_for(faction)}
    units_key = units_key_for(faction)
    units_state: dict = state[units_key]  # type: ignore[type-arg]

    _render_faction_actions(faction, state)

    # Render activated command-phase abilities for the selected unit (any faction)
    if sel and sel[0] == faction:
        _, selected_uid = sel
        _render_unit_command_abilities(selected_uid, faction, state, units_state, unit_by_id)
