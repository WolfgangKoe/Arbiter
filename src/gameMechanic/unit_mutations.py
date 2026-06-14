"""Unit and game-score state mutations."""

from __future__ import annotations

import streamlit as st

from gameMechanic.game_state import units_key_for
from gameObjects.unit import ModelGroup, Unit


def unit_max_hp(unit: Unit, state: dict) -> int:  # type: ignore[type-arg]
    """Maximum HP for the unit's currently-surviving models.

    Per-group-wounds units (e.g. Szarekh 16 + Menhirs 7) sum each group's
    surviving-model capacity; uniform units use wounds × current models. Used to
    decide whether a unit still needs healing (Living Metal etc.) — without this,
    a full mixed-wound unit looks damaged because unit.wounds × models overshoots.
    """
    if state.get("group_wounds"):
        gm = state.get("group_models", {})
        return sum(gm.get(g.id, 0) * unit.group_wound_value(g) for g in unit.model_groups)
    return unit.wounds * state.get("models", 0)


def _apply_group_losses(
    group_models: dict[str, int],
    lost: int,
    model_groups: list[ModelGroup],
) -> None:
    """Remove lost models from group_models in priority order (lowest priority = dies first)."""
    for group in sorted(model_groups, key=lambda g: g.priority):
        if lost <= 0:
            break
        available = group_models.get(group.id, 0)
        removed = min(lost, available)
        group_models[group.id] = available - removed
        lost -= removed


def adjust_vp(faction: str, delta: int) -> None:
    st.session_state.vp[faction] = max(0, st.session_state.vp[faction] + delta)


def adjust_secondary_vp(player_key: str, obj_idx: int, delta: int) -> None:
    """Adjust VP for one secondary objective slot (cap 0–15)."""
    sec_vp: list[int] = st.session_state.secondary_vp[player_key]
    sec_vp[obj_idx] = max(0, min(15, sec_vp[obj_idx] + delta))


def adjust_cp(faction: str, delta: int) -> None:
    st.session_state.cp[faction] = max(0, st.session_state.cp[faction] + delta)


def _recompute_from_group_wounds(state: dict, unit: Unit) -> None:  # type: ignore[type-arg]
    """Recompute group_models / models / current_wounds / destroyed from group_wounds."""
    gw: dict[str, int] = state["group_wounds"]
    gm: dict[str, int] = state["group_models"]
    for group in unit.model_groups:
        wval = unit.group_wound_value(group)
        remaining = gw.get(group.id, 0)
        models = (remaining + wval - 1) // wval  # ceil — a partly wounded model still stands
        gm[group.id] = min(group.count, max(0, models))
    state["current_wounds"] = sum(gw.values())
    state["models"] = sum(gm.values())
    state["destroyed"] = state["current_wounds"] <= 0


def _front_group_hp(state: dict, unit: Unit) -> int:  # type: ignore[type-arg]
    """Remaining HP on the front model of the lowest-priority surviving group."""
    gw: dict[str, int] = state["group_wounds"]
    for group in sorted(unit.model_groups, key=lambda g: g.priority):
        remaining = gw.get(group.id, 0)
        if remaining <= 0:
            continue
        wval = unit.group_wound_value(group)
        partial = remaining % wval
        return partial if partial > 0 else wval
    return 0


def _apply_group_wound_damage(state: dict, dmg: int, unit: Unit) -> None:  # type: ignore[type-arg]
    """Reduce per-group HP pools in priority order (lowest priority = dies first)."""
    gw: dict[str, int] = state["group_wounds"]
    for group in sorted(unit.model_groups, key=lambda g: g.priority):
        if dmg <= 0:
            break
        pool = gw.get(group.id, 0)
        applied = min(dmg, pool)
        gw[group.id] = pool - applied
        dmg -= applied
    _recompute_from_group_wounds(state, unit)


def apply_damage(
    uid: str, faction: str, dmg: int, unit: Unit, mortal: bool = False, resolved: bool = False
) -> None:
    key = units_key_for(faction)
    state = st.session_state[key][uid]
    old_models = state["models"]

    # Per-group wound pools (e.g. Szarekh 16 + Triarchal Menhirs 7): allocate by
    # priority instead of the flat uniform-wounds path below.
    if state.get("group_wounds"):
        if not mortal and not resolved:
            dmg = min(dmg, _front_group_hp(state, unit))
        _apply_group_wound_damage(state, dmg, unit)
        if state["destroyed"] and state.get("melee_with"):
            leave_melee(uid, faction)
        lost = old_models - state["models"]
        if lost > 0:
            state["lost_models_this_turn"] = state.get("lost_models_this_turn", 0) + lost
        return
    # Front-model cap applies only to single-hit damage (wound buttons, old attack form).
    # 6d-v2 passes resolved=True: damage is already the correct total HP reduction.
    if (
        not mortal
        and not resolved
        and unit.models_max > 1
        and state["models"] > 0
        and state["current_wounds"] > 0
    ):
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
        if state.get("group_models") and unit.model_groups:
            _apply_group_losses(state["group_models"], lost, unit.model_groups)


def _restore_group_models(
    group_models: dict[str, int],
    returned: int,
    groups: list,  # type: ignore[type-arg]
) -> None:
    """Refill group_models after a revive — lowest priority first (died first)."""
    for group in sorted(groups, key=lambda g: g.priority):
        missing = group.count - group_models.get(group.id, 0)
        if missing <= 0:
            continue
        back = min(missing, returned)
        group_models[group.id] = group_models.get(group.id, 0) + back
        returned -= back
        if returned <= 0:
            return


def _heal_group_wounds(state: dict, hp: int, unit: Unit) -> None:  # type: ignore[type-arg]
    """Refill per-group HP pools, lowest priority first (the group that died first)."""
    gw: dict[str, int] = state["group_wounds"]
    for group in sorted(unit.model_groups, key=lambda g: g.priority):
        if hp <= 0:
            break
        cap = group.count * unit.group_wound_value(group)
        room = cap - gw.get(group.id, 0)
        added = min(hp, room)
        gw[group.id] = gw.get(group.id, 0) + added
        hp -= added
    _recompute_from_group_wounds(state, unit)


def heal_unit(uid: str, faction: str, hp: int, unit: Unit, revive: bool = True) -> bool:
    key = units_key_for(faction)
    state = st.session_state[key][uid]

    # Per-group wound pools restore by priority (the group that died first returns first).
    if state.get("group_wounds"):
        old_wounds = state["current_wounds"]
        old_models = state["models"]
        _heal_group_wounds(state, hp, unit)
        models_back = state["models"] - old_models
        if models_back > 0:
            state["lost_models_this_turn"] = max(
                0, state.get("lost_models_this_turn", 0) - models_back
            )
        return state["current_wounds"] > old_wounds

    max_hp = unit.wounds * (unit.models_max if revive else state["models"])
    old_wounds = state["current_wounds"]
    old_models = state["models"]
    state["current_wounds"] = min(max_hp, state["current_wounds"] + hp)
    state["destroyed"] = state["current_wounds"] <= 0
    if unit.wounds > 0:
        full = state["current_wounds"] // unit.wounds
        partial = 1 if state["current_wounds"] % unit.wounds > 0 else 0
        state["models"] = min(unit.models_max, full + partial)
    # Models returned by ANY revive mechanic (Reanimation Protocols,
    # Resurrection Orb, …) no longer count as destroyed for Morale this turn —
    # generic rule, no faction checks.
    models_back = state["models"] - old_models
    if models_back > 0:
        state["lost_models_this_turn"] = max(0, state.get("lost_models_this_turn", 0) - models_back)
        if state.get("group_models") and unit.model_groups:
            _restore_group_models(state["group_models"], models_back, unit.model_groups)
    return state["current_wounds"] > old_wounds


def set_deployment(uid: str, faction: str, deployment: str) -> None:
    key = units_key_for(faction)
    state = st.session_state[key][uid]
    state["deployment"] = deployment
    state["in_reserve"] = deployment == "reserve"


def _unit_key(faction: str) -> str:
    return units_key_for(faction)


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


def flee_models(uid: str, faction: str, count: int, unit: Unit) -> None:
    """Remove models that fled a morale test — semantically distinct from combat losses."""
    key = _unit_key(faction)
    state = st.session_state[key][uid]
    if state.get("group_wounds"):
        remaining = count
        gw: dict[str, int] = state["group_wounds"]
        gm: dict[str, int] = state["group_models"]
        for group in sorted(unit.model_groups, key=lambda g: g.priority):
            if remaining <= 0:
                break
            rm = min(remaining, gm.get(group.id, 0))
            gw[group.id] = max(0, gw.get(group.id, 0) - rm * unit.group_wound_value(group))
            remaining -= rm
        _recompute_from_group_wounds(state, unit)
        state["fled_models_this_turn"] = state.get("fled_models_this_turn", 0) + count
        state["turn_flags"]["morale_tested"] = True
        return
    wounds_to_remove = count * unit.wounds
    state["current_wounds"] = max(0, state["current_wounds"] - wounds_to_remove)
    if unit.wounds > 0:
        full = state["current_wounds"] // unit.wounds
        partial = 1 if state["current_wounds"] % unit.wounds > 0 else 0
        state["models"] = min(unit.models_max, full + partial)
    if state["current_wounds"] <= 0:
        state["destroyed"] = True
        state["current_wounds"] = 0
        state["models"] = 0
    state["fled_models_this_turn"] = state.get("fled_models_this_turn", 0) + count
    state["turn_flags"]["morale_tested"] = True


def set_movement_status(uid: str, faction: str, status: str) -> None:
    key = units_key_for(faction)
    state = st.session_state[key][uid]
    flags = state["turn_flags"]
    flags["advanced"] = status == "advanced"
    flags["retreated"] = status == "retreated"
    state["movement_choice"] = status
    state["movement_chosen"] = True
    if status == "retreated":
        leave_melee(uid, faction)


def set_in_melee(uid: str, faction: str, value: bool) -> None:
    key = units_key_for(faction)
    st.session_state[key][uid]["in_melee"] = value


def set_charged(uid: str, faction: str, target_uid: str, target_faction: str) -> None:
    key = units_key_for(faction)
    st.session_state[key][uid]["turn_flags"]["charged"] = True
    enter_melee(uid, faction, target_uid, target_faction)


def apply_mortal_wounds(uid: str, faction: str, count: int, unit: Unit) -> None:
    """Apply mortal wounds — no armour save, no front-model cap."""
    apply_damage(uid, faction, count, unit, mortal=True)


def reset_turn_flags(uid: str, faction: str) -> None:
    key = units_key_for(faction)
    flags = st.session_state[key][uid]["turn_flags"]
    for flag in flags:
        flags[flag] = False
