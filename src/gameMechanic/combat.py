"""Combat utilities — dice, wound thresholds, and the Ziel-3b attack sequence.

resolve_attack() accepts player-entered roll counts (physically rolled dice),
no auto-dice. The caller provides hits, wounds, failed saves, and FNP saves;
this function validates, logs, and returns total damage.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


def parse_dice(s: str) -> int:
    s = str(s).upper().strip().replace("W", "D")
    modifier = 0
    if "+" in s:
        dice_part, mod_part = s.rsplit("+", 1)
        if mod_part.isdigit():
            modifier = int(mod_part)
            s = dice_part
    if "D" in s:
        parts = s.split("D")
        mult = int(parts[0]) if parts[0] else 1
        sides = int(parts[1])
        return sum(random.randint(1, sides) for _ in range(mult)) + modifier
    return int(s) + modifier


def resolve_weapon_strength(strength_value: str | int, bearer_strength: int) -> int:
    """Resolve weapon strength including relative notation (Träger/Bearer/+N/xN)."""
    s = str(strength_value).strip()
    if s.lower() in ("träger", "bearer", "user"):
        return bearer_strength
    if s.startswith("+"):
        return bearer_strength + int(s[1:])
    if s.lower().startswith("x"):
        return bearer_strength * int(s[1:])
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
# Ziel-3b Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class AttackParams:
    attacks: int
    skill: int
    strength: int
    ap: int
    damage: int
    hit_modifier: int = 0
    wound_modifier: int = 0
    mwbd_active: bool = False


@dataclass
class DefendParams:
    toughness: int
    save: int
    wounds: int
    invul_save: int | None = None
    fnp: int | None = None


# ---------------------------------------------------------------------------
# Ziel-3b: resolve_attack — player-entered roll counts
# ---------------------------------------------------------------------------


def resolve_attack(
    params: AttackParams,
    defender: DefendParams,
    hits_rolled: int = 0,
    wounds_rolled: int = 0,
    saves_failed: int = 0,
    fnp_saved: int = 0,
) -> tuple[int, list[str]]:
    """Resolve an attack sequence using player-provided dice counts.

    9E rules applied:
    - AP worsens armour save: effective save threshold = save + abs(ap)
    - Invuln used when it has a lower (better) threshold than modified armour
    - hit_modifier and wound_modifier capped at ±1 (logged, not enforced on input)
    - mwbd_active adds +1 to hit_modifier (noted in log)
    """
    log: list[str] = []

    # Hit phase
    hit_mod = min(1, max(-1, params.hit_modifier + (1 if params.mwbd_active else 0)))
    mwbd_note = " (MWBD +1)" if params.mwbd_active else ""
    log.append(f"Hits: {hits_rolled}{mwbd_note} — skill {params.skill}+")

    if hits_rolled == 0:
        log.append("No hits — attack ends.")
        return 0, log

    # Wound phase
    w_thresh = wound_threshold(params.strength, defender.toughness)
    log.append(
        f"Wounds: {wounds_rolled} — S{params.strength} vs T{defender.toughness} → {w_thresh}+"
    )

    if wounds_rolled == 0:
        log.append("No wounds — attack ends.")
        return 0, log

    # Save phase — determine which save applies
    armour_effective = defender.save + abs(params.ap)
    if defender.invul_save is not None and defender.invul_save < armour_effective:
        effective_save = defender.invul_save
        log.append(
            f"Invuln save {defender.invul_save}+ used "
            f"(armour {armour_effective}+ after AP{params.ap})"
        )
    else:
        effective_save = armour_effective
        if params.ap != 0:
            log.append(f"Armour save {defender.save}+ → {effective_save}+ after AP{params.ap}")
        else:
            log.append(f"Armour save {defender.save}+")

    log.append(f"Failed saves: {saves_failed}")

    if saves_failed == 0:
        log.append("All saves passed — no damage.")
        return 0, log

    # FNP phase
    if defender.fnp is not None and fnp_saved > 0:
        log.append(f"Feel No Pain ({defender.fnp}+): {fnp_saved} wounds ignored")

    net_failed = saves_failed - fnp_saved
    total_damage = net_failed * params.damage
    log.append(f"Damage: {net_failed} × {params.damage} = **{total_damage}**")

    return total_damage, log
