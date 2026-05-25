import random

import streamlit as st

from models import NECRON_UNITS, ORK_UNITS, PHASES, Unit, Weapon


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
    skill_label = "WS" if weapon.is_melee else "BS"
    msgs.append(
        f"**{attacker.name}** → **{weapon.name}** → **{defender.name}** "
        f"({num_models} Modelle, {total_attacks} Angriffe)"
    )

    hit_rolls = [random.randint(1, 6) for _ in range(total_attacks)]
    hits = sum(1 for r in hit_rolls if r >= weapon.skill)
    msgs.append(f"Trefferwürfe ({skill_label}{weapon.skill}+): {hit_rolls} → **{hits} Treffer**")
    if hits == 0:
        msgs.append("Keine Treffer!")
        return 0, msgs

    thresh = wound_threshold(weapon.strength, defender.toughness)
    wound_rolls = [random.randint(1, 6) for _ in range(hits)]
    wounds = sum(1 for r in wound_rolls if r >= thresh)
    msgs.append(
        f"Verwundungswürfe (S{weapon.strength} vs T{defender.toughness}, brauche {thresh}+): "
        f"{wound_rolls} → **{wounds} Verwundungen**"
    )
    if wounds == 0:
        msgs.append("Keine Verwundungen!")
        return 0, msgs

    armour_save = defender.save + abs(weapon.ap)
    effective_save = armour_save
    if defender.invuln and defender.invuln < effective_save:
        effective_save = defender.invuln
        msgs.append(
            f"Rüstungswurf durch AP{weapon.ap} auf {armour_save}+, "
            f"Unverwundbarkeitsrettung {defender.invuln}+ greift"
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


def apply_damage(uid: str, faction: str, dmg: int, unit: Unit) -> None:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    state = st.session_state[key][uid]
    state["current_wounds"] = max(0, state["current_wounds"] - dmg)
    if unit.wounds > 0:
        full_models = state["current_wounds"] // unit.wounds
        partial = 1 if state["current_wounds"] % unit.wounds > 0 else 0
        state["models"] = min(unit.count, full_models + partial)
    if state["current_wounds"] <= 0:
        state["destroyed"] = True
        state["current_wounds"] = 0
        state["models"] = 0


def heal_unit(uid: str, faction: str, hp: int, unit: Unit) -> None:
    key = "necron_units" if faction == "Necrons" else "ork_units"
    state = st.session_state[key][uid]
    max_hp = unit.wounds * unit.count
    state["current_wounds"] = min(max_hp, state["current_wounds"] + hp)
    state["destroyed"] = state["current_wounds"] <= 0
    if unit.wounds > 0:
        full = state["current_wounds"] // unit.wounds
        partial = 1 if state["current_wounds"] % unit.wounds > 0 else 0
        state["models"] = min(unit.count, full + partial)


def init_state() -> None:
    if "initialized" in st.session_state:
        return
    st.session_state.initialized = True
    st.session_state.round = 1
    st.session_state.phase_idx = 0
    st.session_state.active = "Necrons"
    st.session_state.cp = {"Necrons": 3, "Orks": 3}
    st.session_state.vp = {"Necrons": 0, "Orks": 0}

    def unit_state(u: Unit) -> dict:  # type: ignore[type-arg]
        return {"current_wounds": u.wounds * u.count, "models": u.count, "destroyed": False}

    st.session_state.necron_units = {u.uid: unit_state(u) for u in NECRON_UNITS}
    st.session_state.ork_units = {u.uid: unit_state(u) for u in ORK_UNITS}


def reset_game() -> None:
    for k in list(st.session_state.keys()):
        del st.session_state[k]


def adjust_vp(faction: str, delta: int) -> None:
    st.session_state.vp[faction] = max(0, st.session_state.vp[faction] + delta)


def adjust_cp(faction: str, delta: int) -> None:
    st.session_state.cp[faction] = max(0, st.session_state.cp[faction] + delta)


def next_phase() -> None:
    st.session_state.phase_idx += 1
    if st.session_state.phase_idx >= len(PHASES):
        st.session_state.phase_idx = 0
        if st.session_state.active == "Necrons":
            st.session_state.active = "Orks"
        else:
            st.session_state.active = "Necrons"
            st.session_state.round += 1
            st.session_state.cp["Necrons"] += 1
            st.session_state.cp["Orks"] += 1
