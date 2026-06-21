"""Pure attack-math helpers — no Streamlit, no session state.

Extracted from uiLayout/_common.py so this logic counts toward the
coverage gate (src/uiLayout/* is omitted from measurement).
"""

from __future__ import annotations

from gameObjects.weapon import WeaponProfile


def _parse_strength(raw: int | str, unit_strength: int) -> int:
    """Resolve weapon strength to a numeric value.

    int      → fixed strength
    "User"   → unit_strength
    "+N"     → unit_strength + N  (also "User+N")
    "×N"     → unit_strength × N  (also "User×N")
    "-N"     → unit_strength - N  (also "User-N", rare)
    "*"      → 0 (special-mechanic weapon)
    """
    if isinstance(raw, int):
        return raw
    s = raw.strip()
    if s == "*":
        return 0  # special-mechanic weapon; handled by effect handler
    # Strip optional "User" prefix before the operator
    body = s[4:] if s[:4].upper() == "USER" else s
    if not body or body.upper() == "USER":
        return unit_strength
    if body.startswith("+"):
        return unit_strength + int(body[1:])
    if body.startswith("×"):
        return unit_strength * int(body[1:])
    if body.startswith("-"):
        return unit_strength - int(body[1:])
    return int(s)


def _restriction_label(restriction: str) -> str:
    labels = {
        "boss_nob_only": "Boss Nob only",
        "1_per_10": "1 per 10 models",
        "1_per_5": "1 per 5 models",
    }
    return labels.get(restriction, restriction)


def _compute_attacks(
    attacks_str: str,
    models_count: int,
    unit_attacks: int,
    effect: dict | None = None,
    max_attacks: int | None = None,
) -> str:
    """Return display string for total attack count."""
    if effect and effect.get("type") == "extra_attacks":
        if max_attacks is not None:
            return str(models_count * max_attacks)
        amount = int(effect.get("amount", 1))
        return str(models_count * (unit_attacks + amount))
    s = str(attacks_str).strip()
    if s in ("Melee", "None", "", "*"):
        return str(models_count * unit_attacks)
    if "/" in s:
        return str(models_count * int(s.split("/")[0]))
    try:
        return str(models_count * int(s))
    except ValueError:
        return f"{models_count}×{s}"


def _total_attacks_int(
    attacks_str: str,
    models_alive: int,
    unit_attacks: int,
    effect: dict | None = None,
    max_attacks: int | None = None,
) -> int | None:
    """Return total attack count as int, or None if dice-based (cannot pre-split)."""
    if effect and effect.get("type") == "extra_attacks":
        if max_attacks is not None:
            return models_alive * max_attacks
        amount = int(effect.get("amount", 1))
        return models_alive * (unit_attacks + amount)
    s = str(attacks_str).strip()
    if s in ("Melee", "None", "", "*"):
        return models_alive * unit_attacks
    if "/" in s:
        return models_alive * int(s.split("/")[0])
    try:
        return models_alive * int(s)
    except ValueError:
        return None


def _detect_weapon_special(profile: WeaponProfile) -> dict:  # type: ignore[type-arg]
    """Detect special weapon abilities from structured YAML fields (INV-4b).

    All flags derive from the data-driven ``effect`` block or generic profile
    fields — no faction-specific weapon names live in src/. The internal keys are
    generic rule descriptions (``extra_hits``, ``alternating_fire``,
    ``hit_roll_penalty``), not Necron/Ork proper nouns.
    """
    abilities = profile.abilities or ""
    effect = profile.effect or {}
    effect_type = effect.get("type", "")
    return {
        "auto_hit": "Auto-hits" in abilities,
        "extra_hits": effect_type == "extra_hits",
        "alternating_fire": effect_type == "alternating_fire",
        "hit_roll_penalty": (
            profile.is_melee
            and effect_type == "debuff_roll"
            and effect.get("stat") == "hit_roll"
            and (effect.get("modifier") or 0) < 0
        ),
        "has_mortal_wounds": "mortal wound" in abilities.lower(),
    }


def _group_melee_budget(grp_weapons: list, alive: int, eff_attacks: int) -> int:  # type: ignore[type-arg]
    """Total melee attacks of a group: base attacks + extra-attack weapon bonuses.

    Base = models × attacks (incl. stat bonus from active abilities, passed by the caller).
    Each carried weapon with an extra_attacks effect adds its bonus on top
    (e.g. Choppa: "1 additional attack with this weapon"); capped weapons
    (max_attacks, e.g. attack squig) add exactly their cap.
    """
    budget = alive * eff_attacks
    for w in grp_weapons:
        p = next((p for p in w.profiles if p.is_melee), None)
        if p is None or not isinstance(p.effect, dict):
            continue
        if p.effect.get("type") != "extra_attacks":
            continue
        if p.max_attacks:
            budget += alive * int(p.max_attacks)
        else:
            budget += alive * int(p.effect.get("amount", 0))
    return budget
