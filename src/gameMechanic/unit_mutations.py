"""Unit and game-score state mutations."""

from __future__ import annotations

import streamlit as st

from gameObjects.unit import Unit


def adjust_vp(faction: str, delta: int) -> None:
    st.session_state.vp[faction] = max(0, st.session_state.vp[faction] + delta)


def adjust_cp(faction: str, delta: int) -> None:
    st.session_state.cp[faction] = max(0, st.session_state.cp[faction] + delta)


def apply_damage(uid: str, faction: str, dmg: int, unit: Unit, mortal: bool = False) -> None:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    state = st.session_state[key][uid]
    old_models = state["models"]
    if not mortal and unit.models_max > 1 and state["models"] > 0 and state["current_wounds"] > 0:
        front_hp = state["current_wounds"] - (state["models"] - 1) * unit.wounds
        dmg = min(dmg, front_hp)
    state["current_wounds"] = max(0, state["current_wounds"] - dmg)
    if unit.wounds > 0:
        full_models = state["current_wounds"] // unit.wounds
        partial = 1 if state["current_wounds"] % unit.wounds > 0 else 0
        state["models"] = min(unit.models_max, full_models + partial)
    if state["current_wounds"] <= 0:
        state["destroyed"] = True
        state["current_wounds"] = 0
        state["models"] = 0
        if state.get("melee_with"):
            leave_melee(uid, faction)
    lost = old_models - state["models"]
    if lost > 0:
        state["lost_models_this_turn"] = state.get("lost_models_this_turn", 0) + lost


def heal_unit(uid: str, faction: str, hp: int, unit: Unit, revive: bool = True) -> bool:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    state = st.session_state[key][uid]
    max_hp = unit.wounds * (unit.models_max if revive else state["models"])
    old_wounds = state["current_wounds"]
    state["current_wounds"] = min(max_hp, state["current_wounds"] + hp)
    state["destroyed"] = state["current_wounds"] <= 0
    if unit.wounds > 0:
        full = state["current_wounds"] // unit.wounds
        partial = 1 if state["current_wounds"] % unit.wounds > 0 else 0
        state["models"] = min(unit.models_max, full + partial)
    return state["current_wounds"] > old_wounds


def set_deployment(uid: str, faction: str, deployment: str) -> None:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    state = st.session_state[key][uid]
    state["deployment"] = deployment
    state["in_reserve"] = deployment == "reserve"


def enter_melee(
    attacker_uid: str,
    attacker_faction: str,
    target_uid: str,
    target_faction: str,
) -> None:
    atk_key = "necron_units" if attacker_faction == "Necrons" else "ork_units"
    tgt_key = "necron_units" if target_faction == "Necrons" else "ork_units"
    atk_state = st.session_state[atk_key][attacker_uid]
    tgt_state = st.session_state[tgt_key][target_uid]
    if target_uid not in atk_state["melee_with"]:
        atk_state["melee_with"].append(target_uid)
    if attacker_uid not in tgt_state["melee_with"]:
        tgt_state["melee_with"].append(attacker_uid)
    atk_state["in_melee"] = True
    tgt_state["in_melee"] = True


def leave_melee(uid: str, faction: str) -> None:
    own_key = "necron_units" if faction == "Necrons" else "ork_units"
    enemy_key = "ork_units" if faction == "Necrons" else "necron_units"
    state = st.session_state[own_key][uid]
    for enemy_uid in list(state["melee_with"]):
        enemy_state = st.session_state[enemy_key].get(enemy_uid)
        if enemy_state is not None:
            if uid in enemy_state["melee_with"]:
                enemy_state["melee_with"].remove(uid)
            if not enemy_state["melee_with"]:
                enemy_state["in_melee"] = False
    state["melee_with"] = []
    state["in_melee"] = False


def set_movement_status(uid: str, faction: str, status: str) -> None:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    state = st.session_state[key][uid]
    flags = state["turn_flags"]
    flags["advanced"] = status == "advanced"
    flags["retreated"] = status == "retreated"
    state["movement_choice"] = status
    if status == "retreated":
        leave_melee(uid, faction)


def set_in_melee(uid: str, faction: str, value: bool) -> None:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    st.session_state[key][uid]["in_melee"] = value


def set_charged(uid: str, faction: str, target_uid: str, target_faction: str) -> None:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    st.session_state[key][uid]["turn_flags"]["charged"] = True
    enter_melee(uid, faction, target_uid, target_faction)


def reset_turn_flags(uid: str, faction: str) -> None:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    flags = st.session_state[key][uid]["turn_flags"]
    for flag in flags:
        flags[flag] = False
