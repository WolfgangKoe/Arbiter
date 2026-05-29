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


def _unit_key(faction: str) -> str:
    return "necron_units" if faction == "Necrons" else "ork_units"


def enter_melee(
    attacker_uid: str,
    attacker_faction: str,
    target_uid: str,
    target_faction: str,
) -> None:
    atk_state = st.session_state[_unit_key(attacker_faction)][attacker_uid]
    tgt_state = st.session_state[_unit_key(target_faction)][target_uid]
    if [target_faction, target_uid] not in atk_state["melee_with"]:
        atk_state["melee_with"].append([target_faction, target_uid])
    if [attacker_faction, attacker_uid] not in tgt_state["melee_with"]:
        tgt_state["melee_with"].append([attacker_faction, attacker_uid])
    atk_state["in_melee"] = True
    tgt_state["in_melee"] = True


def leave_melee(uid: str, faction: str) -> None:
    state = st.session_state[_unit_key(faction)][uid]
    for fac, enemy_uid in list(state["melee_with"]):
        enemy_state = st.session_state[_unit_key(fac)].get(enemy_uid)
        if enemy_state is not None:
            pair = [faction, uid]
            if pair in enemy_state["melee_with"]:
                enemy_state["melee_with"].remove(pair)
            if not enemy_state["melee_with"]:
                enemy_state["in_melee"] = False
    state["melee_with"] = []
    state["in_melee"] = False


def leave_melee_pair(
    uid: str,
    faction: str,
    enemy_uid: str,
    enemy_faction: str,
) -> None:
    """Remove the engagement between exactly two units, leaving other engagements intact."""
    state = st.session_state[_unit_key(faction)][uid]
    enemy_state = st.session_state[_unit_key(enemy_faction)].get(enemy_uid)
    pair_in_own = [enemy_faction, enemy_uid]
    pair_in_enemy = [faction, uid]
    if pair_in_own in state["melee_with"]:
        state["melee_with"].remove(pair_in_own)
    if not state["melee_with"]:
        state["in_melee"] = False
    if enemy_state is not None:
        if pair_in_enemy in enemy_state["melee_with"]:
            enemy_state["melee_with"].remove(pair_in_enemy)
        if not enemy_state["melee_with"]:
            enemy_state["in_melee"] = False


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
