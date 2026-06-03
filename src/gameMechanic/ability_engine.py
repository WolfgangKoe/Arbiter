from __future__ import annotations

from gameMechanic.game_state import faction_dir_for, units_key_for
from gameMechanic.unit_mutations import heal_unit
from gameObjects.ability import Ability
from gameObjects.loader import (
    load_army,
    load_faction_abilities,
    load_subfaction_abilities,
    load_unit_abilities,
)
from gameObjects.unit import Unit

# ---------------------------------------------------------------------------
# Timing constants — used by ability triggers and phase_runner hooks
# ---------------------------------------------------------------------------

TIMING_PHASE_START = "phase_start"
TIMING_PHASE_END = "phase_end"
TIMING_BEFORE_UNIT_ACTS = "before_unit_acts"
TIMING_AFTER_UNIT_ATTACKED = "after_unit_attacked"


def check_trigger(ability: Ability, phase: str, timing: str, active_player: str) -> bool:
    t = ability.trigger
    if t.timing != timing:
        return False
    phase_list = t.phase if isinstance(t.phase, list) else [t.phase]
    if phase not in phase_list:
        return False
    if t.player not in ("either", active_player):
        return False
    return True


def check_conditions(ability: Ability, unit: Unit, unit_state: dict) -> bool:  # type: ignore[type-arg]
    for cond in ability.conditions:
        if cond.unit_not_destroyed and unit_state.get("destroyed", False):
            return False
        if cond.has_rules and not any(r in unit.rules for r in cond.has_rules):
            return False
        if cond.has_keywords:
            unit_kw_upper = {kw.upper() for kw in unit.keywords}
            if not any(kw.upper() in unit_kw_upper for kw in cond.has_keywords):
                return False
        if cond.needs_healing:
            max_hp = unit.wounds * unit_state.get("models", 0)
            if unit_state.get("current_wounds", 0) >= max_hp:
                return False
        # within_inches: spatial tracking not implemented — always passes
        # max_uses: handled by callers against session state
    return True


def execute_effect(ability: Ability, uid: str, faction: str, unit: Unit) -> bool:
    """Apply ability effect to a unit. Returns True if state actually changed."""
    if ability.effect.type == "heal":
        hp = int(ability.effect.amount or 1)
        return heal_unit(uid, faction, hp, unit, revive=ability.effect.revive)
    return False


def get_activated_command_abilities(unit_id: str, faction_dir: str) -> list[Ability]:
    """Return all activated command-phase abilities for a specific unit."""
    all_abilities = load_unit_abilities(faction_dir)
    result = []
    for a in all_abilities:
        if a.ability_type != "activated":
            continue
        if a.unit_id != unit_id:
            continue
        phases = a.trigger.phase if isinstance(a.trigger.phase, list) else [a.trigger.phase]
        if "command" in phases:
            result.append(a)
    return result


def get_triggered_abilities(
    state: dict,  # type: ignore[type-arg]
    phase: str,
    timing: str,
) -> list[tuple[Ability, list[str]]]:
    active: str = state.get("active", state.get("first_player", ""))
    faction_dir = faction_dir_for(active)

    all_abilities: list[Ability] = []
    all_abilities.extend(load_faction_abilities(faction_dir))
    all_abilities.extend(load_unit_abilities(faction_dir))
    all_abilities.extend(load_subfaction_abilities(faction_dir))

    units_key = units_key_for(active)
    units_state: dict = state.get(units_key, {})  # type: ignore[type-arg]

    units, _ = load_army(faction_dir)
    unit_by_id = {u.id: u for u in units}

    result: list[tuple[Ability, list[str]]] = []
    for ability in all_abilities:
        if not check_trigger(ability, phase, timing, "active"):
            continue
        eligible: list[str] = [
            uid
            for uid, ustate in units_state.items()
            if (unit := unit_by_id.get(uid)) is not None and check_conditions(ability, unit, ustate)
        ]
        if eligible:
            result.append((ability, eligible))

    return result
