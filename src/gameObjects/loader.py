"""YAML-based loader for game objects."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from gameObjects.ability import Ability, Condition, Effect, Trigger
from gameObjects.command_protocol import CommandProtocol
from gameObjects.detachment import DetachmentType, SlotConstraint
from gameObjects.unit import Unit
from gameObjects.weapon import Weapon, WeaponProfile

_DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "wh40k_9e"


def _weapon_profile_from_dict(d: dict[str, Any]) -> WeaponProfile:
    return WeaponProfile(
        name_en=d.get("name_en", ""),
        weapon_type=d["weapon_type"],
        range_inches=int(d["range_inches"]),
        attacks=str(d["attacks"]),
        strength=str(d["strength"]),
        ap=str(d["ap"]),
        damage=str(d["damage"]),
        abilities=d.get("abilities", ""),
        is_melee=d.get("is_melee", False),
    )


def _weapon_from_dict(d: dict[str, Any]) -> Weapon:
    return Weapon(
        id=d["id"],
        name_en=d["name_en"],
        profiles=[_weapon_profile_from_dict(p) for p in d.get("profiles", [])],
        is_relic=d.get("is_relic", False),
    )


def load_weapon_catalog(faction_dir: str) -> dict[str, Weapon]:
    """Load weapons.yaml and return a weapon_id → Weapon index."""
    path = _DATA_ROOT / faction_dir / "weapons.yaml"
    if not path.exists():
        return {}
    with open(path) as f:
        data = yaml.safe_load(f)
    return {w["id"]: _weapon_from_dict(w) for w in data.get("weapons", [])}


def _unit_from_dict(
    d: dict[str, Any],
    weapon_catalog: dict[str, Weapon] | None = None,
) -> Unit:
    weapons: list[Weapon] = []
    for entry in d.get("weapons", []):
        ref = entry.get("ref")
        if ref and weapon_catalog:
            weapon = weapon_catalog.get(ref)
            if weapon:
                weapons.append(weapon)
    return Unit(
        id=d["id"],
        name_en=d["name_en"],
        name_de=d["name_de"],
        faction=d.get("faction", ""),
        subfaction=d.get("subfaction"),
        battlefield_role=d.get("battlefield_role", []),
        keywords=d.get("keywords", []),
        wounds=int(d["wounds"]),
        models_min=int(d["models_min"]),
        models_max=int(d["models_max"]),
        move=str(d["move"]),
        bs=str(d["bs"]),
        ws=str(d["ws"]),
        strength=int(d["strength"]),
        toughness=int(d["toughness"]),
        save=int(d["save"]),
        invuln_save=d.get("invuln_save"),
        leadership=int(d["leadership"]) if d.get("leadership") not in (None, "-") else None,
        oc=int(d["oc"]),
        fnp=d.get("fnp"),
        weapons=weapons,
        rules=d.get("rules", []),
    )


def _condition_from_dict(d: dict[str, Any]) -> Condition:
    return Condition(
        has_rules=d.get("has_rules"),
        has_keywords=d.get("has_keywords"),
        within_inches=d.get("within_inches"),
        max_uses=d.get("max_uses"),
        min_round=d.get("min_round"),
        unit_not_destroyed=d.get("unit_not_destroyed", False),
        needs_healing=d.get("needs_healing", False),
    )


def _trigger_from_dict(d: dict[str, Any]) -> Trigger:
    return Trigger(
        timing=d["timing"],
        phase=d["phase"],
        player=d.get("player", "active"),
        event=d.get("event"),
    )


def _ability_from_dict(d: dict[str, Any]) -> Ability:
    return Ability(
        id=d["id"],
        name_en=d["name_en"],
        source=d["source"],
        rule_text=d["rule_text"],
        trigger=_trigger_from_dict(d["trigger"]),
        conditions=[_condition_from_dict(c) for c in d.get("conditions", [])],
        effect=Effect(
            type=d["effect"]["type"],
            target=d["effect"]["target"],
            amount=d["effect"].get("amount"),
            stat=d["effect"].get("stat"),
            modifier=d["effect"].get("modifier"),
            handler=d["effect"].get("handler"),
            revive=d["effect"].get("revive", True),
        ),
        unit_id=d.get("unit_id"),
        wargear_id=d.get("wargear_id"),
        ability_type=d.get("ability_type", "triggered"),
    )


def load_army(faction_dir: str) -> tuple[list[Unit], list[str]]:
    """Load all units for a faction.

    Prefers units.yaml (catalog format with weapon refs). Falls back to the
    legacy army.yaml if units.yaml does not exist. Returns (units, unmatched)
    where unmatched is always empty until the roster-first loader is implemented
    in Ziel 5c (Schritt C).
    """
    units_path = _DATA_ROOT / faction_dir / "units.yaml"
    army_path = _DATA_ROOT / faction_dir / "army.yaml"

    if units_path.exists():
        with open(units_path) as f:
            data = yaml.safe_load(f)
        faction = faction_dir.capitalize()
        subfaction = None
        entries = data.get("units", [])
    elif army_path.exists():
        with open(army_path) as f:
            data = yaml.safe_load(f)
        faction = data.get("faction", "")
        subfaction = data.get("subfaction")
        entries = data.get("units", [])
    else:
        return [], []

    weapon_catalog = load_weapon_catalog(faction_dir)
    units: list[Unit] = []
    unmatched: list[str] = []
    for ud in entries:
        ud.setdefault("faction", faction)
        ud.setdefault("subfaction", subfaction)
        units.append(_unit_from_dict(ud, weapon_catalog))
    return units, unmatched


def load_faction_abilities(faction_dir: str) -> list[Ability]:
    """Load faction abilities from data/wh40k_9e/<faction_dir>/faction_abilities.yaml."""
    path = _DATA_ROOT / faction_dir / "faction_abilities.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)
    return [_ability_from_dict(a) for a in data.get("abilities", [])]


def load_unit_abilities(faction_dir: str) -> list[Ability]:
    """Load unit-specific abilities from data/wh40k_9e/<faction_dir>/unit_abilities.yaml."""
    path = _DATA_ROOT / faction_dir / "unit_abilities.yaml"
    if not path.exists():
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    return [_ability_from_dict(a) for a in data.get("abilities", [])]


def load_subfaction_abilities(faction_dir: str) -> list[Ability]:
    """Load subfaction abilities from data/wh40k_9e/<faction_dir>/subfaction_abilities.yaml."""
    path = _DATA_ROOT / faction_dir / "subfaction_abilities.yaml"
    if not path.exists():
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    abilities: list[Ability] = []
    for subfaction in data.get("subfactions", []):
        abilities.extend(_ability_from_dict(a) for a in subfaction.get("abilities", []))
    return abilities


def load_command_protocols(faction_dir: str) -> list[CommandProtocol]:
    """Load command protocols from data/wh40k_9e/<faction_dir>/command_protocols.yaml."""
    path = _DATA_ROOT / faction_dir / "command_protocols.yaml"
    if not path.exists():
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    return [
        CommandProtocol(
            id=p["id"],
            name_en=p["name_en"],
            name_de=p["name_de"],
            primary=p["primary"],
            secondary=p["secondary"],
            auto_round_1=p.get("auto_round_1", False),
        )
        for p in data.get("protocols", [])
    ]


def load_wargear_abilities(faction_dir: str) -> list[Ability]:
    """Load wargear abilities from data/wh40k_9e/<faction_dir>/wargear_abilities.yaml."""
    path = _DATA_ROOT / faction_dir / "wargear_abilities.yaml"
    if not path.exists():
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    return [_ability_from_dict(a) for a in data.get("abilities", [])]


def get_abilities_for_unit(unit: Unit, faction_dir: str) -> list[Ability]:
    """Return all abilities applicable to a unit (faction + unit scope, not wargear).

    Used by the UI to display ability texts per unit.
    """
    result: list[Ability] = []
    for ab in load_faction_abilities(faction_dir):
        for cond in ab.conditions:
            if cond.has_rules and any(r in unit.rules for r in cond.has_rules):
                result.append(ab)
                break
        else:
            if not ab.conditions:
                result.append(ab)
    for ab in load_unit_abilities(faction_dir):
        if ab.unit_id == unit.id:
            result.append(ab)
    return result


def load_detachment_types() -> list[DetachmentType]:
    """Load detachment type definitions from data/wh40k_9e/_shared/detachment_types.yaml."""
    path = _DATA_ROOT / "_shared" / "detachment_types.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)
    types = []
    for dt in data.get("detachment_types", []):
        slots = [
            SlotConstraint(role=s["role"], min_units=s["min"], max_units=s["max"])
            for s in dt.get("slots", [])
        ]
        types.append(DetachmentType(id=dt["id"], name_en=dt["name_en"], slot_constraints=slots))
    return types
