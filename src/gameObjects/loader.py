"""YAML-based loader for game objects."""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any

import yaml

from gameObjects.ability import Ability, Condition, Effect, Trigger
from gameObjects.command_protocol import CommandProtocol
from gameObjects.detachment import DetachmentType, SlotConstraint
from gameObjects.stratagem import Stratagem, StratagemModifier
from gameObjects.unit import DamageBracket, Unit, WargearOption
from gameObjects.weapon import Weapon, WeaponProfile

_DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "wh40k_9e"
_ROSTER_DIR = Path(__file__).parent.parent.parent / "data" / "rosters"

_CCW_PROFILE = WeaponProfile(
    name_en="Close Combat Weapon",
    weapon_type="Melee",
    range_inches=0,
    attacks="1",
    strength="User",
    ap="0",
    damage="1",
    abilities="",
    is_melee=True,
)
_CCW = Weapon(
    id="close_combat_weapon",
    name_en="Close Combat Weapon",
    profiles=[_CCW_PROFILE],
    is_relic=False,
)


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


def _wargear_option_from_dict(d: dict[str, Any]) -> WargearOption:
    with_raw = d.get("with")
    if isinstance(with_raw, list):
        with_refs = with_raw
    elif with_raw is not None:
        with_refs = [with_raw]
    else:
        with_refs = []
    return WargearOption(
        type=d["type"],
        with_refs=with_refs,
        replaces=d.get("replaces"),
        item=d.get("item"),
    )


def _damage_bracket_from_dict(d: dict[str, Any]) -> DamageBracket:
    return DamageBracket(
        wounds_min=int(d["wounds_min"]),
        wounds_max=int(d["wounds_max"]),
        move=str(d["move"]) if d.get("move") is not None else None,
        ws=str(d["ws"]) if d.get("ws") is not None else None,
        bs=str(d["bs"]) if d.get("bs") is not None else None,
        attacks=str(d["attacks"]) if d.get("attacks") is not None else None,
    )


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
    if not any(p.is_melee for w in weapons for p in w.profiles):
        weapons.append(_CCW)

    brackets_raw = d.get("damage_bracket", [])
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
        power_level=int(d["power_level"]) if d.get("power_level") is not None else 0,
        move=str(d["move"]),
        bs=str(d["bs"]),
        ws=str(d["ws"]),
        strength=int(d["strength"]),
        toughness=int(d["toughness"]),
        attacks=int(d["attacks"]) if d.get("attacks") not in (None, "-") else None,
        save=int(d["save"]),
        invuln_save=d.get("invuln_save"),
        leadership=int(d["leadership"]) if d.get("leadership") not in (None, "-") else None,
        oc=int(d["oc"]),
        fnp=d.get("fnp"),
        weapons=weapons,
        wargear_options=[_wargear_option_from_dict(o) for o in d.get("wargear_options", [])],
        damage_bracket=[_damage_bracket_from_dict(b) for b in brackets_raw] or None,
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
            target=d["effect"].get("target"),
            amount=d["effect"].get("amount"),
            stat=d["effect"].get("stat"),
            modifier=d["effect"].get("modifier"),
            handler=d["effect"].get("handler"),
            revive=d["effect"].get("revive", True),
        ),
        unit_id=d.get("unit_id"),
        wargear_id=d.get("wargear_id"),
        ability_type=d.get("ability_type", "triggered"),
        badge_label=d.get("badge_label"),
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


def load_unit_catalog(faction_dir: str) -> dict[str, Unit]:
    """Load all units for a faction indexed by unit ID."""
    units, _ = load_army(faction_dir)
    return {u.id: u for u in units}


def load_faction_abilities(faction_dir: str) -> list[Ability]:
    """Load faction abilities from data/wh40k_9e/<faction_dir>/faction_abilities.yaml.

    Skips round_choice entries — those are loaded via load_round_choice_abilities().
    """
    path = _DATA_ROOT / faction_dir / "faction_abilities.yaml"
    if not path.exists():
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    return [
        _ability_from_dict(a)
        for a in data.get("abilities", [])
        if a.get("ability_type") != "round_choice"
    ]


def load_round_choice_abilities(faction_dir: str) -> list[CommandProtocol]:
    """Load round-choice abilities (Protocols, Ka'tahs, Canticles) from faction_abilities.yaml.

    Replaces the old command_protocols.yaml lookup. Any faction with ability_type: round_choice
    entries in its faction_abilities.yaml is automatically supported — no code change needed.
    """
    path = _DATA_ROOT / faction_dir / "faction_abilities.yaml"
    if not path.exists():
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    result = []
    for a in data.get("abilities", []):
        if a.get("ability_type") != "round_choice":
            continue
        dirs = a.get("directives", {})
        result.append(
            CommandProtocol(
                id=a["id"],
                name_en=a["name_en"],
                name_de=a.get("name_de", a["name_en"]),
                primary=a.get("primary", ""),
                secondary=a.get("secondary", ""),
                auto_round_1=a.get("auto_round_1", False),
                primary_effect=dirs.get("primary", {}).get("effect", {}),
                secondary_effect=dirs.get("secondary", {}).get("effect", {}),
                subfaction_affinity=a.get("subfaction_affinity"),
            )
        )
    return result


def load_round_choice_label(faction_dir: str) -> str:
    """Return the UI label for this faction's round-choice abilities (e.g. 'Command Protocols', 'Ka'tahs').

    Reads round_choice_label from faction_abilities.yaml. Falls back to 'Round Abilities'.
    """
    path = _DATA_ROOT / faction_dir / "faction_abilities.yaml"
    if not path.exists():
        return "Round Abilities"
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("round_choice_label", "Round Abilities")


def load_command_protocols(faction_dir: str) -> list[CommandProtocol]:
    """Backward-compatible alias for load_round_choice_abilities()."""
    return load_round_choice_abilities(faction_dir)


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


def load_stratagems(faction_dir: str) -> list[Stratagem]:
    """Load universal + faction stratagems. Universal ones come first."""
    results: list[Stratagem] = []
    for source in ("universal", faction_dir):
        path = _DATA_ROOT / source / "stratagems.yaml"
        if not path.exists():
            continue
        with open(path) as f:
            data = yaml.safe_load(f)
        for s in data.get("stratagems", []):
            mod_data = s.get("modifier")
            modifier = (
                StratagemModifier(
                    roll_type=mod_data["roll_type"],
                    value=int(mod_data["value"]),
                    target=mod_data.get("target", "attacker"),
                    expires_at=mod_data.get("expires_at", "phase_end"),
                    source_label=mod_data.get("source_label", s["name_en"]),
                    phase=mod_data.get("phase"),
                )
                if mod_data
                else None
            )
            results.append(
                Stratagem(
                    id=s["id"],
                    name_en=s["name_en"],
                    cp_cost=int(s["cp_cost"]),
                    phase=s["phase"],
                    stage=s.get("stage", "active"),
                    player=s.get("player", "active"),
                    conditions=s.get("conditions") or [],
                    rule_text=s.get("rule_text", ""),
                    once_per_phase=s.get("once_per_phase", True),
                    detachment=s.get("detachment"),
                    modifier=modifier,
                )
            )
    return results


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


def resolve_bracket_stats(unit: Unit, current_wounds: int) -> dict[str, str | None]:
    """Return live {move, ws, bs, attacks} for unit at given wound count.

    Vehicles degrade across brackets; units without damage_bracket return base stats.
    """
    base = {
        "move": unit.move,
        "ws": unit.ws,
        "bs": unit.bs,
        "attacks": str(unit.attacks) if unit.attacks is not None else None,
    }
    if not unit.damage_bracket:
        return base
    for bracket in unit.damage_bracket:
        if bracket.wounds_min <= current_wounds <= bracket.wounds_max:
            return {
                "move": bracket.move if bracket.move is not None else unit.move,
                "ws": bracket.ws if bracket.ws is not None else unit.ws,
                "bs": bracket.bs if bracket.bs is not None else unit.bs,
                "attacks": bracket.attacks if bracket.attacks is not None else base["attacks"],
            }
    return base


def load_points(faction_dir: str) -> dict[str, int]:
    """Load points.yaml and return a flat id → point-cost dict.

    Per-unit entries store the flat cost; per-model entries store the per-model cost.
    Wargear and arkana sections are also included.
    """
    path = _DATA_ROOT / faction_dir / "points.yaml"
    if not path.exists():
        return {}
    with open(path) as f:
        data = yaml.safe_load(f)
    result: dict[str, int] = {}
    for uid, entry in (data.get("units") or {}).items():
        cost = entry.get("per_unit") or entry.get("per_model") or 0
        result[uid] = int(cost)
    for uid, entry in (data.get("wargear") or {}).items():
        result[uid] = int(entry.get("points", 0))
    for uid, entry in (data.get("arkana") or {}).items():
        result[uid] = int(entry.get("points", 0))
    return result


def scaled_pl(unit: Unit, current_models: int) -> float:
    """Return power level scaled linearly to current model count."""
    if unit.models_min == 0:
        return float(unit.power_level)
    return unit.power_level * (current_models / unit.models_min)


def load_roster_metadata(roster_path: str | Path) -> dict[str, Any]:
    """Read display_name and faction_dir from a roster file without loading units."""
    path = Path(roster_path)
    if not path.exists():
        return {}
    with open(path) as f:
        data = yaml.safe_load(f)
    return {
        "display_name": data.get("display_name", ""),
        "faction_dir": data.get("faction_dir", "necrons"),
    }


def _apply_wargear(
    unit: Unit,
    wargear_ids: list[str],
    weapon_catalog: dict[str, Weapon],
) -> Unit:
    """Return a copy of unit with roster wargear overrides applied.

    Each ID is looked up in the weapon catalog. A matching wargear_option
    drives whether it replaces an existing weapon or is added. Unknown IDs
    (non-weapon wargear items not yet supported) are silently skipped.
    """
    weapons = list(unit.weapons)

    for wid in wargear_ids:
        new_weapon = weapon_catalog.get(wid)
        if new_weapon is None:
            continue

        opt = next(
            (o for o in unit.wargear_options if wid in o.with_refs),
            None,
        )

        if opt is None or opt.type == "add":
            weapons.append(new_weapon)
        else:  # replace / replace_pair
            if opt.replaces:
                weapons = [w for w in weapons if w.id != opt.replaces]
            else:
                # Remove the first non-CCW weapon (the implied slot)
                removed = False
                kept: list[Weapon] = []
                for w in weapons:
                    if not removed and w.id != "close_combat_weapon":
                        removed = True
                    else:
                        kept.append(w)
                weapons = kept
            weapons.append(new_weapon)

    if not any(p.is_melee for w in weapons for p in w.profiles):
        weapons.append(_CCW)

    return dataclasses.replace(unit, weapons=weapons)


def load_roster(
    roster_path: str | Path,
    catalog: dict[str, Unit],
) -> tuple[list[tuple[Unit, int]], list[str]]:
    """Load a roster YAML and resolve unit IDs against a catalog.

    Returns (matched, unmatched) where matched is a list of (Unit, model_count)
    pairs and unmatched is a list of IDs not found in the catalog.
    Roster entries with a 'wargear' list get weapon overrides applied via
    _apply_wargear before they are added to the matched list.
    """
    path = Path(roster_path)
    if not path.exists():
        return [], [f"roster-not-found:{path}"]
    with open(path) as f:
        data = yaml.safe_load(f)

    faction_dir = data.get("faction_dir", "necrons")
    weapon_catalog = load_weapon_catalog(faction_dir)

    matched: list[tuple[Unit, int]] = []
    unmatched: list[str] = []
    for entry in data.get("units", []):
        uid = entry["id"]
        unit = catalog.get(uid)
        if unit is None:
            unmatched.append(uid)
        else:
            models = int(entry.get("models", unit.models_max))
            wargear_ids: list[str] = entry.get("wargear") or []
            if wargear_ids:
                unit = _apply_wargear(unit, wargear_ids, weapon_catalog)
            matched.append((unit, models))
    return matched, unmatched
