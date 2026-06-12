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
from gameObjects.unit import (
    DamageBracket,
    ModelGroup,
    ModelGroupSpec,
    TriggeredEffect,
    Unit,
    WargearOption,
    WeaponSwapSpec,
)
from gameObjects.weapon import Weapon, WeaponProfile

_DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "wh40k_9e"
_ROSTER_DIR = Path(__file__).parent.parent.parent / "data" / "rosters"

_ROUND_CHOICE_CACHE: dict[str, list] = {}
_ROUND_CHOICE_LABEL_CACHE: dict[str, str] = {}
_FACTION_ABILITIES_CACHE: dict[str, list[Ability]] = {}
_UNIT_ABILITIES_CACHE: dict[str, list[Ability]] = {}
_SUBFACTION_ABILITIES_CACHE: dict[str, list[Ability]] = {}
_STRATAGEM_CACHE: dict[str, list[Stratagem]] = {}
_DENY_WARGEAR_CACHE: dict[str, frozenset[str]] = {}


class YamlDataError(ValueError):
    """A game data YAML file exists but cannot be parsed."""


def load_yaml(path: Path) -> Any:
    """Parse a YAML file, raising YamlDataError with the file path on syntax errors."""
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise YamlDataError(f"Invalid YAML in {path}: {exc}") from exc


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
        strength=d["strength"],
        ap=0 if str(d["ap"]) in ("*", "-") else int(d["ap"]),
        damage=str(d["damage"]),
        abilities=d.get("abilities", ""),
        ignores_fnp=d.get("ignores_fnp", False),
        is_melee=d.get("is_melee", False),
        effect=d.get("effect"),
        max_attacks=d.get("max_attacks"),
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
    data = load_yaml(path)
    return {w["id"]: _weapon_from_dict(w) for w in data.get("weapons", [])}


def load_weapon_abilities(faction_dir: str) -> dict[str, list[dict]]:
    """Return weapon_id → list[effect dicts] from inline effect fields in weapons.yaml."""
    catalog = load_weapon_catalog(faction_dir)
    result: dict[str, list[dict]] = {}
    for weapon_id, weapon in catalog.items():
        effects = [p.effect for p in weapon.profiles if p.effect is not None]
        if effects:
            result[weapon_id] = effects
    return result


def _parse_model_group_specs(
    groups_raw: list[dict[str, Any]],
) -> list[ModelGroupSpec]:
    """Parse raw model_groups YAML dicts into ModelGroupSpec objects."""
    specs: list[ModelGroupSpec] = []
    for g in groups_raw:
        base_weapon_refs = [
            e["ref"] if isinstance(e, dict) else str(e) for e in g.get("weapons", [])
        ]
        swaps = [
            WeaponSwapSpec(
                id=s["id"],
                scope=s.get("scope", "group"),
                replaces=s.get("replaces", []),
                options=s.get("options", []),
                pick=int(s.get("pick", 1)),
                limit=s.get("limit", "any"),
            )
            for s in g.get("weapon_swaps", [])
        ]
        specs.append(
            ModelGroupSpec(
                id=g["id"],
                name_en=g["name_en"],
                count_raw=g.get("count", "models_max"),
                base_weapon_refs=base_weapon_refs,
                weapon_swaps=swaps,
                priority=g.get("priority", 1),
            )
        )
    return specs


def _group_weapon_ref_union(groups_raw: list[dict[str, Any]]) -> list[str]:
    """Ordered union of every weapon ref a unit's model groups can carry.

    Units with model_groups omit the unit-level weapons list — the flattened
    union (datasheet display, resolution lookup) is derived here instead.
    """
    refs: list[str] = []
    for g in groups_raw:
        for e in g.get("weapons", []):
            refs.append(e["ref"] if isinstance(e, dict) else str(e))
        for s in g.get("weapon_swaps", []):
            refs.extend(s.get("options", []))
    return list(dict.fromkeys(refs))


def _swap_weapons(base: list[str], replaces: list[str], picks: list[str]) -> list[str]:
    """Apply one swap: base refs minus replaced refs plus picked refs."""
    return [r for r in base if r not in replaces] + list(picks)


def _short_ref(ref: str) -> str:
    return ref.split(".")[-1]


def _resolve_model_groups(
    specs: list[ModelGroupSpec],
    models: int,
    group_loadouts: dict[str, Any] | None,
    weapon_catalog: dict[str, Weapon],
) -> list[ModelGroup]:
    """Resolve ModelGroupSpec objects into ModelGroup objects using roster data.

    - "remainder" count = models minus sum of all fixed counts
    - "models_max" count = models (whole unit in this group)
    - group-scope swaps replace weapons of the whole group
      (roster: ``swaps: {<swap_id>: {weapons: [refs]}}``)
    - per_model-scope swaps split swapped models into sub-groups with fixed
      weapons (roster: ``swaps: {<swap_id>: [{weapons: [refs], count: n}]}``)
    """
    if not specs:
        return []

    def _resolve_refs(refs: list[str], group_id: str) -> list[Weapon]:
        missing = [r for r in refs if r not in weapon_catalog]
        if missing:
            raise ValueError(
                f"Model group {group_id!r}: unknown weapon ref(s) {missing} "
                f"— check the roster's group_loadouts/swaps against weapons.yaml."
            )
        return [weapon_catalog[r] for r in refs]

    fixed_total = sum(
        int(s.count_raw)
        for s in specs
        if isinstance(s.count_raw, int) or (isinstance(s.count_raw, str) and s.count_raw.isdigit())
    )
    remainder_count = max(0, models - fixed_total)

    groups: list[ModelGroup] = []
    for spec in specs:
        raw = spec.count_raw
        if raw == "remainder":
            count = remainder_count
        elif raw == "models_max":
            count = models
        else:
            count = int(raw)

        loadout = (group_loadouts or {}).get(spec.id, {})
        chosen_swaps: dict[str, Any] = loadout.get("swaps", {})

        base_refs = list(spec.base_weapon_refs)
        remaining = count

        for swap in spec.weapon_swaps:
            chosen = chosen_swaps.get(swap.id)
            if not chosen:
                continue

            if swap.scope == "group":
                picks = list(chosen.get("weapons", []))[: swap.pick]
                base_refs = _swap_weapons(base_refs, swap.replaces, picks)
                continue

            # per_model: each entry becomes a sub-group with fixed weapons
            for entry in chosen:
                picks = list(entry.get("weapons", []))[: swap.pick]
                sub_count = min(int(entry.get("count", 0)), remaining)
                if sub_count <= 0 or not picks:
                    continue
                sub_refs = _swap_weapons(spec.base_weapon_refs, swap.replaces, picks)
                weapons_resolved = _resolve_refs(sub_refs, spec.id)
                pick_names = [weapon_catalog[r].name_en for r in picks]
                groups.append(
                    ModelGroup(
                        id=f"{spec.id}_{'_'.join(_short_ref(r) for r in picks)}",
                        name_en=f"{spec.name_en} ({' + '.join(pick_names)})",
                        count=sub_count,
                        weapons=weapons_resolved,
                        priority=spec.priority,
                    )
                )
                remaining -= sub_count

        if remaining > 0:
            groups.append(
                ModelGroup(
                    id=spec.id,
                    name_en=spec.name_en,
                    count=remaining,
                    weapons=_resolve_refs(base_refs, spec.id),
                    priority=spec.priority,
                )
            )

    merged: dict[str, ModelGroup] = {}
    for g in groups:
        if g.id in merged:
            existing = merged[g.id]
            merged[g.id] = dataclasses.replace(existing, count=existing.count + g.count)
        else:
            merged[g.id] = g
    return list(merged.values())


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
    weapon_restrictions: dict[str, str] = {}
    weapon_entries: list[dict[str, Any]] = d.get("weapons") or []
    if not weapon_entries and d.get("model_groups"):
        # Units with model_groups omit the unit-level list — derive the union
        weapon_entries = [{"ref": ref} for ref in _group_weapon_ref_union(d["model_groups"])]
    for entry in weapon_entries:
        ref = entry.get("ref")
        if ref and weapon_catalog:
            weapon = weapon_catalog.get(ref)
            if weapon:
                weapons.append(weapon)
                restriction = entry.get("model_restriction")
                if restriction:
                    weapon_restrictions[ref] = restriction
    if not any(p.is_melee for w in weapons for p in w.profiles):
        weapons.append(_CCW)

    brackets_raw = d.get("damage_bracket", [])
    return Unit(
        weapon_restrictions=weapon_restrictions,
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
        model_group_specs=_parse_model_group_specs(d.get("model_groups", [])),
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
        once_per_battle=d.get("once_per_battle", False),
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
            effects=d["effect"].get("effects"),
        ),
        unit_id=d.get("unit_id"),
        wargear_id=d.get("wargear_id"),
        ability_type=d.get("ability_type", "triggered"),
        badge_label=d.get("badge_label"),
        active_text=d.get("active_text"),
        next_stage_id=d.get("next_stage_id"),
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
        data = load_yaml(units_path)
        faction = faction_dir.capitalize()
        subfaction = None
        entries = data.get("units", [])
    elif army_path.exists():
        data = load_yaml(army_path)
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
    if faction_dir in _FACTION_ABILITIES_CACHE:
        return _FACTION_ABILITIES_CACHE[faction_dir]
    path = _DATA_ROOT / faction_dir / "faction_abilities.yaml"
    if not path.exists():
        _FACTION_ABILITIES_CACHE[faction_dir] = []
        return _FACTION_ABILITIES_CACHE[faction_dir]
    data = load_yaml(path)
    result = [
        _ability_from_dict(a)
        for a in data.get("abilities", [])
        if a.get("ability_type") != "round_choice"
    ]
    _FACTION_ABILITIES_CACHE[faction_dir] = result
    return result


def load_round_choice_abilities(faction_dir: str) -> list[CommandProtocol]:
    """Load round-choice abilities (Protocols, Ka'tahs, Canticles) from faction_abilities.yaml.

    Replaces the old command_protocols.yaml lookup. Any faction with ability_type: round_choice
    entries in its faction_abilities.yaml is automatically supported — no code change needed.
    """
    if faction_dir in _ROUND_CHOICE_CACHE:
        return _ROUND_CHOICE_CACHE[faction_dir]
    path = _DATA_ROOT / faction_dir / "faction_abilities.yaml"
    if not path.exists():
        _ROUND_CHOICE_CACHE[faction_dir] = []
        return _ROUND_CHOICE_CACHE[faction_dir]
    data = load_yaml(path)
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
                primary_effect=dirs.get("primary", {}).get("effect", {}),
                secondary_effect=dirs.get("secondary", {}).get("effect", {}),
                subfaction_affinity=a.get("subfaction_affinity"),
            )
        )
    _ROUND_CHOICE_CACHE[faction_dir] = result
    return result


def load_round_choice_label(faction_dir: str) -> str:
    """Return the UI label for this faction's round-choice abilities (e.g. 'Command Protocols', 'Ka'tahs').

    Reads round_choice_label from faction_abilities.yaml. Falls back to 'Round Abilities'.
    """
    if faction_dir in _ROUND_CHOICE_LABEL_CACHE:
        return _ROUND_CHOICE_LABEL_CACHE[faction_dir]
    path = _DATA_ROOT / faction_dir / "faction_abilities.yaml"
    if not path.exists():
        _ROUND_CHOICE_LABEL_CACHE[faction_dir] = "Round Abilities"
        return _ROUND_CHOICE_LABEL_CACHE[faction_dir]
    data = load_yaml(path)
    label = data.get("round_choice_label", "Round Abilities")
    _ROUND_CHOICE_LABEL_CACHE[faction_dir] = label
    return label


def load_unit_abilities(faction_dir: str) -> list[Ability]:
    """Load unit-specific abilities from data/wh40k_9e/<faction_dir>/unit_abilities.yaml."""
    if faction_dir in _UNIT_ABILITIES_CACHE:
        return _UNIT_ABILITIES_CACHE[faction_dir]
    path = _DATA_ROOT / faction_dir / "unit_abilities.yaml"
    if not path.exists():
        _UNIT_ABILITIES_CACHE[faction_dir] = []
        return _UNIT_ABILITIES_CACHE[faction_dir]
    data = load_yaml(path)
    result = [_ability_from_dict(a) for a in data.get("abilities", [])]
    _UNIT_ABILITIES_CACHE[faction_dir] = result
    return result


def load_subfaction_abilities(faction_dir: str) -> list[Ability]:
    """Load subfaction abilities from data/wh40k_9e/<faction_dir>/subfaction_abilities.yaml."""
    if faction_dir in _SUBFACTION_ABILITIES_CACHE:
        return _SUBFACTION_ABILITIES_CACHE[faction_dir]
    path = _DATA_ROOT / faction_dir / "subfaction_abilities.yaml"
    if not path.exists():
        _SUBFACTION_ABILITIES_CACHE[faction_dir] = []
        return _SUBFACTION_ABILITIES_CACHE[faction_dir]
    data = load_yaml(path)
    abilities: list[Ability] = []
    for subfaction in data.get("subfactions", []):
        abilities.extend(_ability_from_dict(a) for a in subfaction.get("abilities", []))
    _SUBFACTION_ABILITIES_CACHE[faction_dir] = abilities
    return abilities


def load_stratagems(faction_dir: str) -> list[Stratagem]:
    """Load universal + faction stratagems. Universal ones come first."""
    if faction_dir in _STRATAGEM_CACHE:
        return _STRATAGEM_CACHE[faction_dir]
    results: list[Stratagem] = []
    for source in ("_shared", faction_dir):
        path = _DATA_ROOT / source / "stratagems.yaml"
        if not path.exists():
            continue
        data = load_yaml(path)
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
            eff_data = s.get("effect")
            effect = (
                Effect(
                    type=eff_data["type"],
                    target=eff_data.get("target"),
                    amount=eff_data.get("amount"),
                    stat=eff_data.get("stat"),
                    modifier=eff_data.get("modifier"),
                    handler=eff_data.get("handler"),
                )
                if eff_data
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
                    once_per_battle=s.get("once_per_battle", False),
                    timing=s.get("timing"),
                    event=s.get("event"),
                    effect=effect,
                    detachment=s.get("detachment"),
                    modifier=modifier,
                )
            )
    _STRATAGEM_CACHE[faction_dir] = results
    return results


def load_wargear_catalog(faction_dir: str) -> dict[str, dict]:  # type: ignore[type-arg]
    """Return a wargear_id → raw-dict index for a faction's wargear.yaml."""
    path = _DATA_ROOT / faction_dir / "wargear.yaml"
    if not path.exists():
        return {}
    data = load_yaml(path) or []
    entries = data if isinstance(data, list) else []
    return {e["id"]: e for e in entries if isinstance(e, dict) and "id" in e}


def wargear_ids_with_handler(faction_dir: str, handler: str) -> set[str]:
    """Return IDs of wargear items that carry the given handler tag."""
    catalog = load_wargear_catalog(faction_dir)
    return {wid for wid, entry in catalog.items() if entry.get("handler") == handler}


def load_relic_catalog(faction_dir: str) -> dict[str, dict]:  # type: ignore[type-arg]
    """Return a relic_id → raw-dict index for a faction's relics.yaml."""
    path = _DATA_ROOT / faction_dir / "relics.yaml"
    if not path.exists():
        return {}
    data = load_yaml(path) or []
    entries = data if isinstance(data, list) else []
    return {e["id"]: e for e in entries if isinstance(e, dict) and "id" in e}


def _attacks_from_weapon_type(weapon_type: str) -> str:
    """Extract attack count from weapon_type like 'Heavy 2D6' or 'Assault 4'."""
    parts = weapon_type.split()
    return parts[-1] if len(parts) >= 2 else "1"


def _relic_weapon_from_entry(entry: dict[str, Any]) -> Weapon:
    """Convert a relic YAML entry with profiles into a Weapon object."""
    profiles = []
    for pd in entry.get("profiles", []):
        mode = pd.get("mode", "Shooting")
        is_melee = mode == "Melee"
        weapon_type = pd["weapon_type"]
        attacks = str(pd.get("attacks", _attacks_from_weapon_type(weapon_type)))
        strength = pd["strength"]
        profiles.append(
            WeaponProfile(
                weapon_type=weapon_type,
                range_inches=int(pd["range_inches"]),
                attacks=attacks,
                strength=strength,
                ap=0 if str(pd.get("ap", "0")) in ("*", "-") else int(pd["ap"]),
                damage=str(pd["damage"]),
                is_melee=is_melee,
                abilities=pd.get("abilities", pd.get("abilities_en", "")),
            )
        )
    return Weapon(
        id=entry["id"],
        name_en=entry["name_en"],
        profiles=profiles,
        is_relic=True,
    )


def _apply_relic(
    unit: Unit,
    relic_id: str,
    relic_catalog: dict[str, dict],  # type: ignore[type-arg]
) -> Unit:
    """Return a copy of unit with the named relic applied.

    Weapon relics replace the specified base weapon and add the relic weapon.
    Relics with persistent_effects have those effects applied to unit stats.
    """
    entry = relic_catalog.get(relic_id)
    if not entry:
        return unit

    te_list: list[TriggeredEffect] = [
        TriggeredEffect(
            timing=te["timing"],
            phase=te["phase"],
            effect=te["effect"],
            once_per_battle=te.get("once_per_battle", False),
            dice=te.get("dice"),
            threshold=te.get("threshold"),
            amount=te.get("amount"),
            mortal_dice=te.get("mortal_dice"),
        )
        for te in entry.get("triggered_effects", [])
    ]
    unit = dataclasses.replace(
        unit,
        relic_id=relic_id,
        relic_name=entry.get("name_en"),
        triggered_effects=te_list,
    )

    if entry.get("profiles"):
        relic_weapon = _relic_weapon_from_entry(entry)
        weapons = list(unit.weapons)
        for replaced_id in entry.get("replaces", {}).get("any_of", []):
            weapons = [w for w in weapons if w.id != replaced_id]
        weapons.append(relic_weapon)
        if not any(p.is_melee for w in weapons for p in w.profiles):
            weapons.append(_CCW)
        unit = dataclasses.replace(unit, weapons=weapons)

    for eff in entry.get("persistent_effects", []):
        unit = _apply_persistent_effect(unit, eff)

    return unit


def _parse_move_inches(move_str: str) -> int:
    """Parse a move string such as '6"' or '10"' to an integer."""
    return int(move_str.rstrip('"').strip())


def _apply_persistent_effect(unit: Unit, effect: dict) -> Unit:  # type: ignore[type-arg]
    """Return a copy of unit with one persistent wargear effect applied."""
    etype = effect.get("type", "")
    if etype == "set_stat":
        stat = effect.get("stat", "")
        value = effect.get("value")
        if stat == "move" and value is not None:
            return dataclasses.replace(unit, move=str(value))
        if stat == "save" and value is not None:
            return dataclasses.replace(unit, save=int(value))
    elif etype == "buff_stat":
        stat = effect.get("stat", "")
        modifier = int(effect.get("modifier", 0))
        if stat == "move":
            current = _parse_move_inches(unit.move)
            return dataclasses.replace(unit, move=f'{current + modifier}"')
        if stat == "toughness":
            return dataclasses.replace(unit, toughness=unit.toughness + modifier)
        if stat == "strength":
            return dataclasses.replace(unit, strength=unit.strength + modifier)
    elif etype == "grant_keyword":
        kw = str(effect.get("keyword", "")).upper()
        if kw and kw not in unit.keywords:
            return dataclasses.replace(unit, keywords=list(unit.keywords) + [kw])
    elif etype == "set_invuln":
        return dataclasses.replace(unit, invuln_save=int(effect["value"]))
    elif etype == "buff_save":
        modifier = int(effect.get("modifier", 0))
        new_save = max(1, unit.save - modifier)
        return dataclasses.replace(unit, save=new_save)
    elif etype == "set_fnp":
        return dataclasses.replace(unit, fnp=int(effect["value"]))
    return unit


def load_deny_wargear_names(faction_dir: str) -> frozenset[str]:
    """Return short names of wargear items with deny_psychic effect for a faction.

    Short name = last segment of the wargear ID (e.g. 'gloom_prism').
    """
    if faction_dir in _DENY_WARGEAR_CACHE:
        return _DENY_WARGEAR_CACHE[faction_dir]
    path = _DATA_ROOT / faction_dir / "wargear.yaml"
    if not path.exists():
        _DENY_WARGEAR_CACHE[faction_dir] = frozenset()
        return _DENY_WARGEAR_CACHE[faction_dir]
    data = load_yaml(path) or []
    entries = data if isinstance(data, list) else []
    result = frozenset(
        e["id"].rsplit(".", 1)[-1]
        for e in entries
        if isinstance(e, dict) and e.get("effect", {}).get("type") == "deny_psychic"
    )
    _DENY_WARGEAR_CACHE[faction_dir] = result
    return result


def load_wargear_abilities(faction_dir: str) -> list[Ability]:
    """Load wargear abilities from data/wh40k_9e/<faction_dir>/wargear.yaml.

    Only wargear items with an 'effect' field are returned as Ability objects.
    """
    path = _DATA_ROOT / faction_dir / "wargear.yaml"
    if not path.exists():
        return []
    data = load_yaml(path) or []
    entries = data if isinstance(data, list) else []
    abilities: list[Ability] = []
    for e in entries:
        if not isinstance(e, dict) or "effect" not in e:
            continue
        ability_dict = {
            "id": e["id"] + ".ability",
            "name_en": e["name_en"],
            "source": "wargear",
            "rule_text": e.get("rule_text", e.get("ability_en", "")),
            "trigger": e["trigger"],
            "conditions": e.get("conditions", []),
            "effect": e["effect"],
            "wargear_id": e["id"],
            "ability_type": e.get("ability_type", "triggered"),
        }
        abilities.append(_ability_from_dict(ability_dict))
    return abilities


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
    data = load_yaml(path)
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
    data = load_yaml(path)
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
    data = load_yaml(path)
    return {
        "display_name": data.get("display_name", ""),
        "faction_dir": data.get("faction_dir", "necrons"),
        "dynasty": data.get("dynasty"),
    }


def _apply_wargear(
    unit: Unit,
    wargear_ids: list[str],
    weapon_catalog: dict[str, Weapon],
    wargear_catalog: dict[str, dict] | None = None,  # type: ignore[type-arg]
) -> Unit:
    """Return a copy of unit with roster wargear overrides applied.

    Weapon IDs found in weapon_catalog are added/replaced per wargear_options.
    All IDs are tracked in unit.wargear_ids. Entries in wargear_catalog with
    persistent_effects have those effects applied to the unit's stats.
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

    unit = dataclasses.replace(
        unit,
        weapons=weapons,
        wargear_ids=list(unit.wargear_ids) + wargear_ids,
    )

    if wargear_catalog:
        granted: list[str] = []
        for wid in wargear_ids:
            entry = wargear_catalog.get(wid)
            if not entry:
                continue
            for eff in entry.get("persistent_effects", []):
                kws_before = set(unit.keywords)
                unit = _apply_persistent_effect(unit, eff)
                for kw in unit.keywords:
                    if kw not in kws_before:
                        granted.append(kw)
        if granted:
            unit = dataclasses.replace(unit, wargear_keywords=list(unit.wargear_keywords) + granted)

    return unit


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
    data = load_yaml(path)

    faction_dir = data.get("faction_dir", "necrons")
    weapon_catalog = load_weapon_catalog(faction_dir)
    wargear_catalog = load_wargear_catalog(faction_dir)
    relic_catalog = load_relic_catalog(faction_dir)

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
                unit = _apply_wargear(unit, wargear_ids, weapon_catalog, wargear_catalog)
            relic_id: str | None = entry.get("relic")
            if relic_id:
                unit = _apply_relic(unit, relic_id, relic_catalog)
            if unit.model_group_specs:
                group_loadouts = entry.get("group_loadouts") or {}
                resolved = _resolve_model_groups(
                    unit.model_group_specs, models, group_loadouts, weapon_catalog
                )
                unit = dataclasses.replace(unit, model_groups=resolved)
            matched.append((unit, models))
    return matched, unmatched
