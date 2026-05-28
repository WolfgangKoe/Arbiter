"""Combat utilities — dice, wound thresholds.

parse_dice() and wound_threshold() are used across all phase handlers.
resolve_attack() is DEPRECATED — will be replaced by the Ziel 3b implementation
(AttackParams / DefendParams dataclasses) in this same file.
"""

from __future__ import annotations

import random

from gameObjects.unit import Unit
from gameObjects.weapon import Weapon


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
# DEPRECATED — replaced by Ziel 3b implementation. Do not extend.
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
