"""YAML-based loader for game objects."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from gameObjects.detachment import DetachmentType, SlotConstraint
from gameObjects.faction_property import FactionProperty
from gameObjects.unit import Unit
from gameObjects.weapon import Weapon

_DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "wh40k_9e"


def _weapon_from_dict(d: dict[str, Any]) -> Weapon:
    return Weapon(
        id=d["id"],
        name_en=d["name_en"],
        weapon_type=d["weapon_type"],
        range_inches=str(d["range_inches"]),
        attacks=str(d["attacks"]),
        strength=str(d["strength"]),
        ap=str(d["ap"]),
        damage=str(d["damage"]),
        abilities=d.get("abilities", ""),
        is_melee=d.get("is_melee", False),
    )


def _unit_from_dict(d: dict[str, Any]) -> Unit:
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
        leadership=int(d["leadership"]),
        oc=int(d["oc"]),
        fnp=d.get("fnp"),
        weapons=[_weapon_from_dict(w) for w in d.get("weapons", [])],
        abilities=d.get("abilities", ""),
    )


def load_army(faction_dir: str) -> list[Unit]:
    """Load all units from data/wh40k_9e/<faction_dir>/army.yaml."""
    path = _DATA_ROOT / faction_dir / "army.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)
    faction = data.get("faction", "")
    subfaction = data.get("subfaction")
    units = []
    for ud in data.get("units", []):
        ud.setdefault("faction", faction)
        ud.setdefault("subfaction", subfaction)
        units.append(_unit_from_dict(ud))
    return units


def load_faction_properties(faction_dir: str) -> list[FactionProperty]:
    """Load faction properties from data/wh40k_9e/<faction_dir>/faction_properties.yaml."""
    path = _DATA_ROOT / faction_dir / "faction_properties.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)
    props = []
    for pd in data.get("faction_properties", []):
        props.append(
            FactionProperty(
                id=pd["id"],
                name_en=pd["name_en"],
                triggers_phase=pd["triggers_phase"],
                affects_parameter=pd["affects_parameter"],
                ability_keyword=pd["ability_keyword"],
                rule_text=pd["rule_text"],
                applies_to_keyword=pd.get("applies_to_keyword"),
            )
        )
    return props


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
