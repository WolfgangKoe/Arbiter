import json
import os
import random
from datetime import datetime

import streamlit as st

from gameObjects.loader import load_army
from gameObjects.unit import Unit
from gameObjects.weapon import Weapon

PHASES: list[tuple[str, str]] = [
    ("Setup", "setup"),
    ("Befehlsphase", "command"),
    ("Bewegungsphase", "movement"),
    ("Psiphase", "psychic"),
    ("Fernkampfphase", "shooting"),
    ("Angriffsphase", "charge"),
    ("Nahkampfphase", "fight"),
    ("Moralphase", "morale"),
]

_NECRON_UNITS = load_army("necrons")
_ORK_UNITS = load_army("orks")


def parse_dice(s: str) -> int:
    s = str(s).upper().strip()
    if "D" in s:
        parts = s.split("D")
        mult = int(parts[0]) if parts[0] else 1
        sides = int(parts[1])
        return sum(random.randint(1, sides) for _ in range(mult))
    return int(s)


def wound_threshold(strength: int, toughness: int) -> int:
    if strength >= toughness * 2:
        return 2
    if strength > toughness:
        return 3
    if strength == toughness:
        return 4
    if strength * 2 <= toughness:
        return 6
    return 5


# ---------------------------------------------------------------------------
# DEPRECATED: resolve_attack() — replaced by gameMechanic/combat.py (Ziel 3b).
# Do not extend this function. It will be removed in Ziel 3c.
# ---------------------------------------------------------------------------
def resolve_attack(
    attacker: Unit,
    atk_state: dict,  # type: ignore[type-arg]
    weapon: Weapon,
    defender: Unit,
    def_state: dict,  # type: ignore[type-arg]
    num_models: int,
) -> tuple[int, list[str]]:
    msgs: list[str] = []
    total_attacks = parse_dice(weapon.attacks) * num_models
    skill = int(attacker.ws.rstrip("+")) if weapon.is_melee else int(attacker.bs.rstrip("+"))
    skill_label = "WS" if weapon.is_melee else "BS"
    msgs.append(
        f"**{attacker.name_en}** → **{weapon.name_en}** → **{defender.name_en}** "
        f"({num_models} Modelle, {total_attacks} Angriffe)"
    )

    hit_rolls = [random.randint(1, 6) for _ in range(total_attacks)]
    hits = sum(1 for r in hit_rolls if r >= skill)
    msgs.append(f"Trefferwürfe ({skill_label}{skill}+): {hit_rolls} → **{hits} Treffer**")
    if hits == 0:
        msgs.append("Keine Treffer!")
        return 0, msgs

    w_strength = int(weapon.strength) if str(weapon.strength).lstrip("-").isdigit() else 4
    thresh = wound_threshold(w_strength, defender.toughness)
    wound_rolls = [random.randint(1, 6) for _ in range(hits)]
    wounds = sum(1 for r in wound_rolls if r >= thresh)
    msgs.append(
        f"Verwundungswürfe (S{weapon.strength} vs T{defender.toughness}, brauche {thresh}+): "
        f"{wound_rolls} → **{wounds} Verwundungen**"
    )
    if wounds == 0:
        msgs.append("Keine Verwundungen!")
        return 0, msgs

    w_ap = int(weapon.ap)
    armour_save = defender.save + abs(w_ap)
    effective_save = armour_save
    if defender.invuln_save and defender.invuln_save < effective_save:
        effective_save = defender.invuln_save
        msgs.append(
            f"Rüstungswurf durch AP{weapon.ap} auf {armour_save}+, "
            f"Unverwundbarkeitsrettung {defender.invuln_save}+ greift"
        )
    else:
        msgs.append(
            f"Rüstungswurf: {defender.save}+ mit AP{weapon.ap} → effektiv {effective_save}+"
        )

    if effective_save > 6:
        failed = wounds
        msgs.append("Keine Rettung möglich!")
    else:
        save_rolls = [random.randint(1, 6) for _ in range(wounds)]
        failed = sum(1 for r in save_rolls if r < effective_save)
        msgs.append(
            f"Rettungswürfe ({effective_save}+): {save_rolls} → **{failed} fehlgeschlagen**"
        )

    if failed == 0:
        msgs.append("Alle Rettungswürfe erfolgreich!")
        return 0, msgs

    if defender.fnp:
        fnp_rolls = [random.randint(1, 6) for _ in range(failed)]
        survived = sum(1 for r in fnp_rolls if r >= defender.fnp)
        failed -= survived
        msgs.append(
            f"Feel No Pain ({defender.fnp}+): {fnp_rolls} → {survived} gerettet, noch {failed} übrig"
        )

    total_dmg = sum(parse_dice(weapon.damage) for _ in range(failed))
    msgs.append(f"**{total_dmg} Schaden verursacht!**")
    return total_dmg, msgs


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
    lost = old_models - state["models"]
    if lost > 0:
        state["lost_models_this_turn"] = state.get("lost_models_this_turn", 0) + lost


def heal_unit(uid: str, faction: str, hp: int, unit: Unit) -> None:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    state = st.session_state[key][uid]
    max_hp = unit.wounds * unit.models_max
    state["current_wounds"] = min(max_hp, state["current_wounds"] + hp)
    state["destroyed"] = state["current_wounds"] <= 0
    if unit.wounds > 0:
        full = state["current_wounds"] // unit.wounds
        partial = 1 if state["current_wounds"] % unit.wounds > 0 else 0
        state["models"] = min(unit.models_max, full + partial)


def _unit_state(u: Unit) -> dict:  # type: ignore[type-arg]
    return {
        "current_wounds": u.wounds * u.models_max,
        "models": u.models_max,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "stationary",
        "lost_models_this_turn": 0,
        # Single-choice movement for current turn — drives display badges only.
        # None | "normal" | "advanced" | "stationary" | "retreated"
        "movement_choice": None,
        # Bidirectional melee tracking: list of enemy unit-ID strings.
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
        },
        # Ability system
        "my_will_be_done_active": False,
        "active_buffs": [],
        "models_lost_since_last_rp": 0,
    }


def init_state() -> None:
    if "initialized" in st.session_state:
        return
    st.session_state.initialized = True
    st.session_state.round = 1
    st.session_state.phase_idx = 0
    st.session_state.active = "Necrons"
    st.session_state.first_player = "Necrons"
    st.session_state.second_player = "Orks"
    st.session_state.cp = {"Necrons": 3, "Orks": 3}
    st.session_state.vp = {"Necrons": 0, "Orks": 0}
    st.session_state.selected_unit = None
    st.session_state.selected_targets = []  # list[tuple[str, str]] — faction + uid pairs
    st.session_state.resurrection_orb_used = False
    # Phase stage: "start" | "active" | "end"
    st.session_state.phase_stage = "active"
    # Active effect waiting for player confirmation (None when no effect pending)
    st.session_state.active_effect = None
    st.session_state.necron_units = {u.id: _unit_state(u) for u in _NECRON_UNITS}
    st.session_state.ork_units = {u.id: _unit_state(u) for u in _ORK_UNITS}


def reset_game() -> None:
    for k in list(st.session_state.keys()):
        del st.session_state[k]


def adjust_vp(faction: str, delta: int) -> None:
    st.session_state.vp[faction] = max(0, st.session_state.vp[faction] + delta)


def adjust_cp(faction: str, delta: int) -> None:
    st.session_state.cp[faction] = max(0, st.session_state.cp[faction] + delta)


def set_deployment(uid: str, faction: str, deployment: str) -> None:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    state = st.session_state[key][uid]
    state["deployment"] = deployment
    state["in_reserve"] = deployment == "reserve"


def set_movement_status(uid: str, faction: str, status: str) -> None:
    """Update turn_flags and movement_choice based on the chosen movement type."""
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


def enter_melee(
    attacker_uid: str,
    attacker_faction: str,
    target_uid: str,
    target_faction: str,
) -> None:
    """Register both units as engaged with each other (bidirectional)."""
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
    """Remove unit from melee — cleans up both sides of every engagement."""
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


def set_charged(uid: str, faction: str, target_uid: str, target_faction: str) -> None:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    st.session_state[key][uid]["turn_flags"]["charged"] = True
    enter_melee(uid, faction, target_uid, target_faction)


def reset_turn_flags(uid: str, faction: str) -> None:
    """Reset all turn_flags for a single unit — called at turn start."""
    key = "necron_units" if faction == "Necrons" else "ork_units"
    flags = st.session_state[key][uid]["turn_flags"]
    for flag in flags:
        flags[flag] = False


def log_action(round_num: int, phase: str, unit_name: str, action: str) -> None:
    os.makedirs("data/log", exist_ok=True)
    log_file = os.path.join("data/log", "game_log.json")
    entry = {
        "round": round_num,
        "phase": phase,
        "unit": unit_name,
        "action": action,
        "timestamp": datetime.now().isoformat(),
    }
    entries: list[dict] = []  # type: ignore[type-arg]
    if os.path.exists(log_file):
        with open(log_file) as f:
            try:
                entries = json.load(f)
            except json.JSONDecodeError:
                entries = []
    entries.append(entry)
    with open(log_file, "w") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def _reset_phase_state() -> None:
    pass  # Phase-level flags moved to turn_flags — reset at turn start only.


def _reset_turn_state() -> None:
    for key in ("necron_units", "ork_units"):
        for state in st.session_state[key].values():
            flags = state["turn_flags"]
            for flag in flags:
                flags[flag] = False
            state["lost_models_this_turn"] = 0
            state["movement_choice"] = None


def next_phase() -> None:
    idx = st.session_state.phase_idx
    num = len(PHASES)

    if idx == 0:  # Setup → first Command phase
        st.session_state.phase_idx = 1
        _reset_phase_state()
    elif idx >= num - 1:  # Moralphase done → switch player
        if st.session_state.active == "Necrons":
            st.session_state.active = "Orks"
        else:
            st.session_state.active = "Necrons"
            st.session_state.round += 1
        _reset_turn_state()
        st.session_state.phase_idx = 1
    else:
        st.session_state.phase_idx = idx + 1
        _reset_phase_state()

    st.session_state.selected_unit = None
    st.session_state.selected_targets = []
