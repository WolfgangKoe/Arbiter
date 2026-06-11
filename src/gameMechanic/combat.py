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
    save_modifier: int = 0


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
    mod_note = f" (hit mod {hit_mod:+d})" if hit_mod else ""
    log.append(f"Hits: {hits_rolled}{mwbd_note}{mod_note} — skill {params.skill}+")

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
    armour_effective = defender.save + abs(params.ap) - defender.save_modifier
    if defender.invul_save is not None and defender.invul_save < armour_effective:
        effective_save = defender.invul_save
        log.append(
            f"Invuln save {defender.invul_save}+ used "
            f"(armour {armour_effective}+ after AP{params.ap})"
        )
    else:
        effective_save = armour_effective
        if params.ap != 0 or defender.save_modifier != 0:
            mod_note = f" / Protocol +{defender.save_modifier}" if defender.save_modifier else ""
            log.append(
                f"Armour save {defender.save}+ → {effective_save}+ after AP{params.ap}{mod_note}"
            )
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


# ---------------------------------------------------------------------------
# Ziel-6d: modifier-stack helpers — pure functions, no session state access
# ---------------------------------------------------------------------------


def resolve_attack_modifiers(
    skill: int,
    strength: int,
    toughness: int,
    weapon_type: str,
    advanced: bool,
    modifiers: list[dict],  # type: ignore[type-arg]
    use_melee: bool,
) -> dict:  # type: ignore[type-arg]
    """Compute hit/wound thresholds with full modifier stack.

    Each entry in *modifiers*: {"label": str, "value": int, "roll_type": "hit"|"wound", "source": str}
    Returns:
        {
            "hit":   {"base": int, "stack": list[dict], "modified": int},
            "wound": {"base": int, "stack": list[dict], "modified": int},
        }
    Net modifier is capped at ±1 per 9E rules. Threshold minimum is 2+.
    """
    hit_stack: list[dict] = []  # type: ignore[type-arg]
    wound_stack: list[dict] = []  # type: ignore[type-arg]

    if not use_melee and weapon_type == "Heavy" and advanced:
        hit_stack.append({"label": "Heavy (advanced)", "value": -1, "source": "weapon_rule"})

    for m in modifiers:
        roll_type = m.get("roll_type", "")
        entry = {"label": m["label"], "value": m["value"], "source": m.get("source", "modifier")}
        if roll_type == "hit":
            hit_stack.append(entry)
        elif roll_type == "wound":
            wound_stack.append(entry)

    hit_net = min(1, max(-1, sum(e["value"] for e in hit_stack)))
    wound_net = min(1, max(-1, sum(e["value"] for e in wound_stack)))

    hit_base = skill
    wound_base = wound_threshold(strength, toughness)

    return {
        "hit": {
            "base": hit_base,
            "stack": hit_stack,
            "modified": max(2, hit_base - hit_net),
        },
        "wound": {
            "base": wound_base,
            "stack": wound_stack,
            "modified": max(2, wound_base - wound_net),
        },
    }


def resolve_save(
    base_save: int,
    invuln_save: int | None,
    ap: int,
    save_modifiers: list[dict],  # type: ignore[type-arg]
) -> dict:  # type: ignore[type-arg]
    """Compute best effective save value.

    Each entry in *save_modifiers*: {"label": str, "value": int}
    Positive value = save improves (e.g. +1 lowers threshold from 5+ to 4+).
    Invuln save cannot be improved by armour modifiers.
    Returns:
        {
            "armour": int, "armour_eff": int, "invuln": int | None,
            "effective": int, "using_invuln": bool,
            "save_bonus": int, "stack": list[dict],
        }
    """
    save_bonus = sum(m["value"] for m in save_modifiers)
    armour_eff = base_save + abs(ap)
    armour_modified = armour_eff - save_bonus

    if invuln_save is not None and invuln_save < armour_modified:
        effective = invuln_save
        using_invuln = True
    else:
        effective = armour_modified
        using_invuln = False

    return {
        "armour": base_save,
        "armour_eff": armour_eff,
        "invuln": invuln_save,
        "effective": min(effective, 7),
        "using_invuln": using_invuln,
        "save_bonus": save_bonus,
        "stack": save_modifiers,
    }


def resolve_fnp(fnp: int | None, ignores_fnp: bool) -> int | None:
    """Return FNP threshold, or None if the unit has no FNP or the weapon ignores it."""
    if fnp is None or ignores_fnp:
        return None
    return fnp


def apply_damage_attacks(
    models_lost: int,
    wounds_on_front: int,
    mortal_wounds: int,
    wounds_per_model: int,
) -> int:
    """Compute total HP damage from 6d-v2 damage inputs.

    models_lost × wounds_per_model = HP from fully destroyed models.
    wounds_on_front = partial damage on the current front model (9E: excess is lost).
    mortal_wounds = carry over between models (same HP pool as normal wounds).
    """
    return models_lost * wounds_per_model + wounds_on_front + mortal_wounds
