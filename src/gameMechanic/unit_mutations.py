"""Unit and game-score state mutations."""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

import streamlit as st

from gameMechanic.game_log import log_action
from gameMechanic.game_state import units_key_for
from gameObjects.unit import ModelGroup, Unit


def unit_max_hp(unit: Unit, state: MutableMapping[str, Any]) -> int:
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


def apply_buff_to_unit(
    unit_state: MutableMapping[str, Any],
    ability_id: str,
    badge_label: str,
    effect_type: str,
) -> None:
    """Record an activated command-phase buff in a unit's active_buffs list.

    Idempotent for the same ability_id: adds the entry only if no buff with
    that ability_id already exists.  Called by the render layer after the
    player activates a buff_roll/reroll_hit_1 ability and picks a target.
    """
    buffs: list[dict] = unit_state.setdefault("active_buffs", [])  # type: ignore[type-arg]
    if any(b.get("ability_id") == ability_id for b in buffs):
        return
    buffs.append({"ability_id": ability_id, "badge_label": badge_label, "effect_type": effect_type})


def _recompute_from_group_wounds(state: MutableMapping[str, Any], unit: Unit) -> None:
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


def _front_group_hp(state: MutableMapping[str, Any], unit: Unit) -> int:
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


def _apply_group_wound_damage(state: MutableMapping[str, Any], dmg: int, unit: Unit) -> None:
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


def select_damage_target_group(uid: str, faction: str, group_id: str) -> None:
    """Defender's choice: set the group that receives the next damage application.

    Raises ValueError if group_id is not a known group of this unit.
    """
    key = units_key_for(faction)
    state = st.session_state[key][uid]
    if group_id not in state.get("group_wounds", {}):
        raise ValueError(f"unknown group_id {group_id!r} for unit {uid}")
    state["damage_active_group_id"] = group_id


def get_locked_group(uid: str, faction: str, unit: Unit) -> str | None:
    """Return the group whose front model is wounded-but-alive, else None.

    A group is locked when its HP pool is not an integer multiple of the
    per-model wounds (group_wounds[gid] % wval != 0) — a single model stands
    partly damaged and 9E forces all further wounds onto it until it dies. At
    most one group can be locked at a time.
    """
    key = units_key_for(faction)
    state = st.session_state[key][uid]
    gw: dict[str, int] = state.get("group_wounds", {})
    for group in unit.model_groups:
        pool = gw.get(group.id, 0)
        if pool > 0 and pool % unit.group_wound_value(group) != 0:
            return group.id
    return None


def _group_front_hp(state: MutableMapping[str, Any], unit: Unit, group_id: str) -> int:
    """Remaining HP on the front (partly wounded) model of one specific group."""
    remaining = state["group_wounds"].get(group_id, 0)
    if remaining <= 0:
        return 0
    group = next((g for g in unit.model_groups if g.id == group_id), None)
    if group is None:
        return 0
    wval = unit.group_wound_value(group)
    partial = remaining % wval
    return partial if partial > 0 else wval


def _apply_directed_group_damage(
    state: MutableMapping[str, Any], dmg: int, unit: Unit, group_id: str
) -> None:
    """Reduce only the chosen group's HP pool (defender's directed allocation)."""
    gw: dict[str, int] = state["group_wounds"]
    pool = gw.get(group_id, 0)
    gw[group_id] = max(0, pool - dmg)
    _recompute_from_group_wounds(state, unit)


def apply_damage(
    uid: str, faction: str, dmg: int, unit: Unit, mortal: bool = False, resolved: bool = False
) -> None:
    key = units_key_for(faction)
    state = st.session_state[key][uid]
    old_models = state["models"]

    # Per-group wound pools (e.g. Szarekh 16 + Triarchal Menhirs 7, and homogeneous
    # squads). When the defender has directed damage to a group, allocate there and
    # enforce the wounded-model lock; otherwise keep the priority-spill default.
    if state.get("group_wounds"):
        active = state.get("damage_active_group_id")
        if active is not None and not mortal:
            locked = get_locked_group(uid, faction, unit)
            if locked is not None and active != locked:
                raise ValueError(
                    f"group {locked!r} has a wounded model and must receive damage, not {active!r}"
                )
            if not resolved:
                dmg = min(dmg, _group_front_hp(state, unit, active))
            _apply_directed_group_damage(state, dmg, unit, active)
        else:
            # Default (no directed target) or mortal overflow — unchanged behavior.
            # mortal=True ignores the lock and spills across group boundaries.
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


def _heal_group_wounds(state: MutableMapping[str, Any], hp: int, unit: Unit) -> None:
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


def _remove_whole_models(state: MutableMapping[str, Any], unit: Unit, count: int) -> None:
    """Remove `count` whole models from `state` — shared by every "model destroyed
    directly, no save, no wound-by-wound damage roll" path (Morale flee, Desperate
    Breakout casualties). Handles both the group_wounds pool (mixed-wound units)
    and the plain current_wounds/models bookkeeping, destroying the unit outright
    once its wound pool is exhausted.
    """
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


def flee_models(uid: str, faction: str, count: int, unit: Unit) -> None:
    """Remove models that fled a morale test — semantically distinct from combat losses."""
    key = _unit_key(faction)
    state = st.session_state[key][uid]
    _remove_whole_models(state, unit, count)
    state["fled_models_this_turn"] = state.get("fled_models_this_turn", 0) + count
    state["turn_flags"]["morale_tested"] = True


def activate_morale_auto_pass(uid: str, faction: str) -> None:
    """Mark a unit to auto-pass its next Morale test this phase (Insane Bravery, R-MORALE-09).

    Set when the Insane Bravery stratagem is spent for this unit (see
    uiLayout/_common.py:spend_stratagem's effect dispatch). Consumed by
    ``confirm_morale_auto_pass`` once the Morale phase actually renders the test
    for this unit — no dice are rolled and no models flee.
    """
    st.session_state[_unit_key(faction)][uid]["turn_flags"]["morale_auto_pass"] = True


def confirm_morale_auto_pass(uid: str, faction: str) -> None:
    """Consume an active Insane Bravery auto-pass: mark the Morale test as passed.

    No dice are rolled and no models flee — mirrors the bookkeeping flee_models
    does on a normal test, minus any model loss.
    """
    flags = st.session_state[_unit_key(faction)][uid]["turn_flags"]
    flags["morale_tested"] = True
    flags["morale_auto_pass"] = False


def activate_desperate_breakout(uid: str, faction: str) -> None:
    """Mark a unit as pending Desperate Breakout resolution (R-MOVE-14).

    Set when the Desperate Breakout stratagem is spent for this unit (see
    uiLayout/_common.py:spend_stratagem's effect dispatch). The Movement phase
    UI then renders the casualty-roll input for this unit; ``resolve_desperate_breakout``
    applies the result once the player confirms it.
    """
    st.session_state[_unit_key(faction)][uid]["turn_flags"]["desperate_breakout_pending"] = True


def apply_desperate_breakout_casualties(uid: str, faction: str, count: int, unit: Unit) -> None:
    """Remove `count` whole models destroyed by the Desperate Breakout casualty roll.

    core_rules.txt (Desperate Breakout): "Roll one D6 for each model in that unit;
    for each result of 1, one model in that unit of your choice is destroyed."
    These models are genuinely destroyed (not the flee/Combat-Attrition
    death-trigger exemption), so — unlike flee_models — they count toward
    ``lost_models_this_turn`` for this turn's own Morale test and do not touch
    ``morale_tested``.
    """
    if count <= 0:
        return
    state = st.session_state[_unit_key(faction)][uid]
    _remove_whole_models(state, unit, count)
    state["lost_models_this_turn"] = state.get("lost_models_this_turn", 0) + count


def resolve_desperate_breakout(uid: str, faction: str, casualties: int, unit: Unit) -> None:
    """Apply a Desperate Breakout casualty roll, then Fall Back.

    Casualties are removed first (mirrors the rule's sequencing: the destruction
    roll happens, then — assuming the unit survives — it Falls Back). If the
    roll destroys the unit outright, ``set_movement_status`` is skipped (nothing
    left to move); the pending flag is cleared either way, since the stratagem's
    one resolution window is consumed once the player confirms the roll result.
    Fall Back's own consequences (leaves melee, locks shooting/charging/psychic
    powers this turn) come from ``set_movement_status`` — the same path a normal
    Fall Back uses (R-MOVE-08).
    """
    apply_desperate_breakout_casualties(uid, faction, casualties, unit)
    state = st.session_state[_unit_key(faction)][uid]
    state["turn_flags"]["desperate_breakout_pending"] = False
    if not state.get("destroyed"):
        set_movement_status(uid, faction, "retreated")


def set_movement_status(uid: str, faction: str, status: str) -> None:
    key = units_key_for(faction)
    state = st.session_state[key][uid]
    flags = state["turn_flags"]
    flags["advanced"] = status == "advanced"
    flags["retreated"] = status == "retreated"
    state["movement_choice"] = status
    state["movement_chosen"] = True
    if status == "retreated":
        # Stash the engagements leave_melee() is about to clear so a later
        # Reset ("Stay Stationary" — S133 K2) can restore them; see
        # reset_movement_to_stationary().
        flags["pre_retreat_melee_with"] = [list(p) for p in state.get("melee_with", [])]
        leave_melee(uid, faction)


def reset_movement_to_stationary(uid: str, faction: str) -> None:
    """Undo a Move/Advance/Retreat declaration back to Stationary.

    Backs the movementPhase "Stay Stationary" Reset button (S133 K2
    decision item 3): the button replaces whichever Move/Advance/Retreat
    button fired, it is never a 4th initial movement choice, and it always
    lands on "stationary" — no Retreated→Move/Advance path opens through it,
    reusing set_movement_status for the actual state change exactly as the
    pre-refactor "Stay Stationary" button already did.

    A prior Retreat also stashed the melee engagements leave_melee() cleared
    (set_movement_status above); those are restored here first, so the
    unit's pre-Retreat "in melee" dependency (Move/Advance disabled, only
    Retreat offered) reappears exactly as it was before Retreat was chosen —
    for a non-Retreat reset (Moved/Advanced), there is no stash and this is a
    no-op beyond the plain stationary transition.
    """
    key = units_key_for(faction)
    state = st.session_state[key][uid]
    stash = state["turn_flags"].pop("pre_retreat_melee_with", None)
    if stash:
        for enemy_faction, enemy_uid in stash:
            enemy_state = st.session_state[units_key_for(enemy_faction)].get(enemy_uid)
            if enemy_state is None:
                continue
            pair = [faction, uid]
            if pair not in enemy_state["melee_with"]:
                enemy_state["melee_with"].append(pair)
            enemy_state["in_melee"] = True
        state["melee_with"] = [list(p) for p in stash]
        state["in_melee"] = True
    set_movement_status(uid, faction, "stationary")


def set_in_melee(uid: str, faction: str, value: bool) -> None:
    key = units_key_for(faction)
    st.session_state[key][uid]["in_melee"] = value


def set_charged(uid: str, faction: str, target_uid: str, target_faction: str) -> None:
    key = units_key_for(faction)
    st.session_state[key][uid]["turn_flags"]["charged"] = True
    target_key = units_key_for(target_faction)
    st.session_state[target_key][target_uid]["turn_flags"]["was_charged"] = True
    enter_melee(uid, faction, target_uid, target_faction)


def apply_mortal_wounds(uid: str, faction: str, count: int, unit: Unit) -> None:
    """Apply mortal wounds — no armour save, no front-model cap."""
    apply_damage(uid, faction, count, unit, mortal=True)


def perform_heroic_intervention(
    faction: str,
    unit_key: str,
    target_faction: str,
    target_keys: list[str],
    round_no: int,
    unit_name: str,
) -> None:
    """Apply a Heroic Intervention: mark the flag, enter melee with each target, log.

    Operates on STATE KEYS (duplicate-squad safe). Mirrors R-CHARGE-09/10 enforcement.
    """
    st.session_state[_unit_key(faction)][unit_key]["turn_flags"]["heroic_intervened"] = True
    for tgt_key in target_keys:
        enter_melee(unit_key, faction, tgt_key, target_faction)
    log_action(
        round_no, "charge", unit_name, f"Heroic Intervention — engaged {len(target_keys)} unit(s)"
    )


def reset_turn_flags(uid: str, faction: str) -> None:
    key = units_key_for(faction)
    flags = st.session_state[key][uid]["turn_flags"]
    for flag in flags:
        flags[flag] = False
