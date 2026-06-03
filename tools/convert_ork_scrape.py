#!/usr/bin/env python3
"""Convert wahapedia_scraper raw text output to orks/units.yaml + orks/weapons.yaml.

Usage:
    python tools/convert_ork_scrape.py /tmp/orks_scrape_raw.txt
Output:
    data/wh40k_9e/orks/units.yaml
    data/wh40k_9e/orks/weapons.yaml
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ── Metadata tables ────────────────────────────────────────────────────────────

BATTLEFIELD_ROLES: dict[str, list[str]] = {
    "warboss": ["HQ"],
    "warboss_mega_armour": ["HQ"],
    "warboss_warbike": ["HQ"],
    "big_mek": ["HQ"],
    "big_mek_mega_armour": ["HQ"],
    "big_mek_kff": ["HQ"],
    "big_mek_sag": ["HQ"],
    "big_mek_warbike": ["HQ"],
    "weirdboy": ["HQ"],
    "wurrboy": ["HQ"],
    "painboy": ["HQ"],
    "beastboss": ["HQ"],
    "beastboss_squigosaur": ["HQ"],
    "ghazghkull": ["HQ"],
    "kaptin_badrukk": ["HQ"],
    "boss_zagstruk": ["HQ"],
    "deffkilla_wartrike": ["HQ"],
    "boyz": ["Troops"],
    "gretchin": ["Troops"],
    "beast_snagga_boyz": ["Troops"],
    "meganobz": ["Elites"],
    "nobz": ["Elites"],
    "burna_boyz": ["Elites"],
    "kommandos": ["Elites"],
    "tankbustas": ["Elites"],
    "flash_gitz": ["Elites"],
    "mad_dok_grotsnik": ["Elites"],
    "mek": ["Elites"],
    "runtherd": ["Elites"],
    "painboy_warbike": ["Elites"],
    "nob_waaagh_banner": ["Elites"],
    "warbikers": ["Fast Attack"],
    "stormboyz": ["Fast Attack"],
    "deffkoptas": ["Fast Attack"],
    "squighog_boyz": ["Fast Attack"],
    "nob_smasha_squig": ["Fast Attack"],
    "boomdakka_snazzwagons": ["Fast Attack"],
    "kustom_boosta_blastas": ["Fast Attack"],
    "megatrakk_scrapjets": ["Fast Attack"],
    "shokkjump_dragstas": ["Fast Attack"],
    "rukkatrukk_squigbuggies": ["Fast Attack"],
    "battlewagon": ["Heavy Support"],
    "deff_dreads": ["Heavy Support"],
    "bonebreaka": ["Heavy Support"],
    "gunwagon": ["Heavy Support"],
    "kill_rig": ["Heavy Support"],
    "hunta_rig": ["Heavy Support"],
    "dakkajet": ["Flyers"],
    "burna_bommer": ["Flyers"],
    "blitza_bommer": ["Flyers"],
    "wazbom_blastajet": ["Flyers"],
}

# [min, max] — codex composition limits
MODEL_COUNTS: dict[str, tuple[int, int]] = {
    "boyz": (10, 30),
    "gretchin": (10, 40),
    "beast_snagga_boyz": (10, 20),
    "meganobz": (3, 6),
    "nobz": (5, 10),
    "burna_boyz": (5, 10),
    "kommandos": (5, 10),
    "tankbustas": (5, 10),
    "flash_gitz": (5, 10),
    "warbikers": (3, 9),
    "stormboyz": (5, 30),
    "deffkoptas": (1, 3),
    "squighog_boyz": (3, 6),
    "nob_smasha_squig": (1, 1),
    "boomdakka_snazzwagons": (1, 3),
    "kustom_boosta_blastas": (1, 3),
    "megatrakk_scrapjets": (1, 3),
    "shokkjump_dragstas": (1, 3),
    "rukkatrukk_squigbuggies": (1, 3),
    "deff_dreads": (1, 3),
}

# Objective Control (9E equivalent)
OC_OVERRIDES: dict[str, int] = {
    "boyz": 2,
    "gretchin": 1,
    "beast_snagga_boyz": 2,
    "nobz": 2,
    "warbikers": 2,
    "stormboyz": 2,
    "squighog_boyz": 2,
}


# ── Raw text parser ────────────────────────────────────────────────────────────


def _slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"['’]", "", s)
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def parse_raw(path: str) -> list[dict]:
    units: list[dict] = []
    current: dict | None = None
    in_weapons = False

    with open(path) as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        raw = lines[i].rstrip("\n")
        stripped = raw.strip()
        i += 1

        # Separator line
        if stripped.startswith("=" * 20):
            in_weapons = False
            continue

        # Unit header: "  slug  (Name)"
        m = re.match(r"^\s{2}(\w+)\s{2,}\((.+?)\)\s*$", raw)
        if m and (current is None or current.get("_header_done")):
            current = {
                "slug": m.group(1),
                "name": m.group(2),
                "stats": {},
                "invuln": None,
                "keywords": [],
                "weapons": [],
                "abilities": [],
                "_header_done": False,
            }
            units.append(current)
            in_weapons = False
            continue

        if current is None:
            continue

        current["_header_done"] = True

        # STATS line
        if stripped.startswith("STATS"):
            stats_str = stripped[6:].strip()
            for part in stats_str.split():
                if ":" in part:
                    k, v = part.split(":", 1)
                    current["stats"][k] = v
            continue

        # INVULN line
        if stripped.startswith("INVULN"):
            val = stripped[7:].strip()
            current["invuln"] = None if val.lower() == "none" else val
            continue

        # KW line
        if stripped.startswith("KW"):
            kw_str = stripped[2:].strip()
            current["keywords"] = [k.strip() for k in kw_str.split(",") if k.strip()]
            continue

        # Weapon header
        if stripped.startswith("WEAPON") and "RNG" in stripped and "TYPE" in stripped:
            in_weapons = True
            continue

        # Weapon data row — fixed-width columns as printed by print_unit:
        # "  {name:<30} {range:<7} {type:<14} {S:<5} {AP:<5} {D:<5} {abilities}"
        # Offsets from content = raw[2:]:
        #   [0:30] name, [30] sep, [31:38] range, [38] sep, [39:53] type,
        #   [53] sep, [54:59] S, [59] sep, [60:65] AP, [65] sep, [66:71] D,
        #   [71] sep, [72:] abilities
        if in_weapons and stripped and not stripped.startswith("ABIL"):
            content = raw[2:]  # strip leading 2 spaces
            if len(content) < 38:
                continue
            name_field = content[0:30]
            is_subprofile = name_field.startswith("- ")
            name = name_field.strip()
            if is_subprofile:
                name = name[2:].strip()
            rng = content[31:38].strip()
            typ = content[39:53].strip()
            s_val = content[54:59].strip()
            ap_val = content[60:65].strip()
            d_val = content[66:71].strip()
            abil = content[72:].strip().rstrip("…")
            if name:
                current["weapons"].append(
                    {
                        "name": name,
                        "range": rng,
                        "type": typ,
                        "S": s_val,
                        "AP": ap_val,
                        "D": d_val,
                        "abilities": abil,
                        "is_subprofile": is_subprofile,
                    }
                )
            continue

        # ABIL line — ends weapon section
        if stripped.startswith("ABIL"):
            in_weapons = False
            txt = stripped[5:].strip()
            if txt:
                current["abilities"].append(txt)
            continue

        # Blank line
        if not stripped:
            in_weapons = False

    return units


# ── Stat helpers ───────────────────────────────────────────────────────────────


def _parse_wounds(w_str: str) -> tuple[int, str | None]:
    """Return (wounds, bracket_note). '9-16' → (16, '9-16'), '5' → (5, None)."""
    m = re.match(r"(\d+)-(\d+)", w_str)
    if m:
        return int(m.group(2)), w_str
    return int(w_str), None


def _parse_attacks(a_str: str) -> int | None:
    """Return integer or None if variable (D3, D6, *)."""
    if re.match(r"^\d+$", a_str):
        return int(a_str)
    return None


def _parse_save(sv_str: str) -> int:
    """'3+' → 3."""
    m = re.match(r"(\d+)\+", sv_str)
    return int(m.group(1)) if m else 7


def _parse_invuln(inv: str | None) -> int | None:
    if not inv:
        return None
    m = re.match(r"(\d+)\+", inv)
    return int(m.group(1)) if m else None


def _parse_leadership(ld: str) -> int | None:
    try:
        return int(ld)
    except (ValueError, TypeError):
        return None


def _oc(slug: str, keywords: list[str]) -> int:
    if slug in OC_OVERRIDES:
        return OC_OVERRIDES[slug]
    kw_upper = {k.upper() for k in keywords}
    if "CHARACTER" in kw_upper:
        return 1
    if "VEHICLE" in kw_upper or "MONSTER" in kw_upper:
        return 3
    return 2


def _weapon_id(faction: str, name: str) -> str:
    return f"wh40k_9e.{faction}.weapon.{_slugify(name)}"


def _is_melee(rng: str, typ: str) -> bool:
    return rng.lower() == "melee" or typ.lower().startswith("melee")


def _range_inches(rng: str) -> int:
    if _is_melee(rng, ""):
        return 0
    m = re.match(r"(\d+)", rng)
    return int(m.group(1)) if m else 0


def _strength_str(s_val: str) -> str:
    s = s_val.strip()
    if s in ("User", "user", "-"):
        return "User"
    if re.match(r"^[+-]\d+$", s) or re.match(r"^User[+\-×x]\d+$", s, re.I):
        return s
    # x2 notation
    s = re.sub(r"^x(\d+)$", r"User×\1", s)
    return s


def _weapon_type(typ: str) -> str:
    """Normalise Wahapedia weapon type string to a clean type name."""
    typ = typ.strip()
    # Dakka X/Y → Dakka (Ork special rule)
    typ = re.sub(r"Dakka\s+\S+", "Dakka", typ)
    return typ


# ── YAML serialisation ─────────────────────────────────────────────────────────


def _yaml_str(val: object) -> str:
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, int):
        return str(val)
    s = str(val)
    # Quote if contains special YAML chars, starts with special tokens, or is bare "-"
    if s == "-" or re.search(r'[:{}\[\],#&*?|<>=!%@`\'"]', s) or re.match(r'^\d+["+]', s):
        s = s.replace('"', '\\"')
        return f'"{s}"'
    return s


def build_units_yaml(units: list[dict], faction: str = "orks") -> str:
    lines = [
        f"# {faction.capitalize()} unit catalog — WH40k 9E",
        f"# Source: Wahapedia scrape {__import__('datetime').date.today()}",
        "# Keywords: UPPERCASE throughout.",
        "",
        "units:",
        "",
    ]

    role_groups: dict[str, list[dict]] = {}
    for u in units:
        slug = u["slug"]
        roles = BATTLEFIELD_ROLES.get(slug, ["Unknown"])
        role_key = roles[0]
        role_groups.setdefault(role_key, []).append(u)

    role_order = ["HQ", "Troops", "Elites", "Fast Attack", "Heavy Support", "Flyers", "Unknown"]
    separator = {
        "HQ": "HQ",
        "Troops": "Troops",
        "Elites": "Elites",
        "Fast Attack": "Fast Attack",
        "Heavy Support": "Heavy Support",
        "Flyers": "Flyers",
        "Unknown": "Unknown / Lord of War",
    }

    for role in role_order:
        group = role_groups.get(role, [])
        if not group:
            continue
        lines.append(f"  # ── {separator[role]} {'─' * (60 - len(separator[role]))}")
        lines.append("")

        for u in group:
            slug = u["slug"]
            stats = u["stats"]
            kws = [kw.upper() for kw in u["keywords"]]
            wounds_raw = stats.get("W", "1")
            wounds, bracket_note = _parse_wounds(wounds_raw)
            min_m, max_m = MODEL_COUNTS.get(slug, (1, 1))
            roles = BATTLEFIELD_ROLES.get(slug, ["Unknown"])
            attacks_val = _parse_attacks(stats.get("A", "1"))
            oc_val = _oc(slug, kws)
            inv_raw = _parse_invuln(u["invuln"])

            uid = f"wh40k_9e.{faction}.unit.{slug}"

            lines.append(f"  - id: {uid}")
            lines.append(f"    name_en: {u['name']}")
            lines.append(f"    name_de: {u['name']}")
            lines.append(f"    battlefield_role: [{', '.join(roles)}]")
            lines.append(f"    keywords: [{', '.join(kws)}]")
            lines.append(f"    wounds: {wounds}")
            lines.append(f"    models_min: {min_m}")
            lines.append(f"    models_max: {max_m}")
            lines.append("    power_level: 0  # TODO: fill from codex")
            lines.append(f"    move: {_yaml_str(stats.get('M', '6\"'))}")
            lines.append(f"    ws: {_yaml_str(stats.get('WS', '3+'))}")
            lines.append(f"    bs: {_yaml_str(stats.get('BS', '5+'))}")
            lines.append(f"    strength: {stats.get('S', '4')}")
            lines.append(f"    toughness: {stats.get('T', '4')}")
            if attacks_val is not None:
                lines.append(f"    attacks: {attacks_val}")
            else:
                lines.append(f"    attacks: null  # variable: {stats.get('A', '?')}")
            lines.append(f"    save: {_parse_save(stats.get('Sv', '7+'))}")
            lines.append(f"    invuln_save: {inv_raw if inv_raw is not None else 'null'}")
            lines.append(f"    leadership: {_parse_leadership(stats.get('Ld'))}")
            lines.append(f"    oc: {oc_val}")
            lines.append("    fnp: null")
            if bracket_note:
                lines.append(f"    # damage_bracket: true  # wounds range: {bracket_note}")
            lines.append("    rules: []")

            # Weapon refs — skip sub-profiles (they belong to the parent weapon)
            weapon_refs = []
            seen_weapon_names: set[str] = set()
            for w in u["weapons"]:
                if w["is_subprofile"]:
                    continue
                if w["name"] in seen_weapon_names:
                    continue
                seen_weapon_names.add(w["name"])
                wid = _weapon_id(faction, w["name"])
                weapon_refs.append(f"      - ref: {wid}")
            if weapon_refs:
                lines.append("    weapons:")
                lines.extend(weapon_refs)
            else:
                lines.append("    weapons: []")

            lines.append("    wargear_options: []")
            lines.append("")

    return "\n".join(lines)


def build_weapons_yaml(units: list[dict], faction: str = "orks") -> str:
    lines = [
        f"# {faction.capitalize()} weapon catalog — WH40k 9E",
        f"# Source: Wahapedia scrape {__import__('datetime').date.today()}",
        "",
        "weapons:",
        "",
    ]

    # Collect all unique weapons across all units
    seen: dict[str, dict] = {}  # name → first weapon dict with all sub-profiles
    weapon_order: list[str] = []

    for u in units:
        current_parent: dict | None = None
        for w in u["weapons"]:
            if not w["is_subprofile"]:
                name = w["name"]
                if name not in seen:
                    seen[name] = {"main": w, "subs": []}
                    weapon_order.append(name)
                current_parent = seen[name]
            else:
                if current_parent is not None:
                    # Only add sub if not already there
                    existing_subs = [s["name"] for s in current_parent["subs"]]
                    if w["name"] not in existing_subs:
                        current_parent["subs"].append(w)

    for name in weapon_order:
        entry = seen[name]
        main = entry["main"]
        subs = entry["subs"]
        wid = _weapon_id(faction, name)

        lines.append(f"  - id: {wid}")
        lines.append(f"    name_en: {name}")

        if subs:
            # Dual-profile weapon: main + subs become multiple profiles
            lines.append("    profiles:")
            all_profiles = [{"name": name, **main}] + [{"name": s["name"], **s} for s in subs]
            for prof in all_profiles:
                pname = prof["name"]
                melee = _is_melee(prof.get("range", ""), prof.get("type", ""))
                wtype = "Melee" if melee else _weapon_type(prof.get("type", ""))
                typ = prof.get("type", "")
                atk = typ.split()[-1] if typ else "1"
                lines.append(f"      - name_en: {pname}")
                lines.append(f"        weapon_type: {wtype}")
                lines.append(f"        range_inches: {_range_inches(prof.get('range', '0'))}")
                lines.append(f"        attacks: {_yaml_str(atk)}")
                lines.append(f"        strength: {_yaml_str(_strength_str(prof.get('S', 'User')))}")
                lines.append(f"        ap: {_yaml_str(prof.get('AP', '0'))}")
                lines.append(f"        damage: {_yaml_str(prof.get('D', '1'))}")
                ab = prof.get("abilities", "").replace("-", "").strip()
                lines.append(f"        abilities: {_yaml_str(ab)}")
                lines.append(f"        is_melee: {'true' if melee else 'false'}")
        else:
            # Single-profile
            melee = _is_melee(main.get("range", ""), main.get("type", ""))
            typ = main.get("type", "")
            atk = typ.split()[-1] if typ else "1"
            lines.append("    profiles:")
            lines.append(f"      - weapon_type: {_weapon_type(typ) if typ else 'Unknown'}")
            lines.append(f"        range_inches: {_range_inches(main.get('range', '0'))}")
            lines.append(f"        attacks: {_yaml_str(atk)}")
            lines.append(f"        strength: {_yaml_str(_strength_str(main.get('S', 'User')))}")
            lines.append(f"        ap: {_yaml_str(main.get('AP', '0'))}")
            lines.append(f"        damage: {_yaml_str(main.get('D', '1'))}")
            ab = main.get("abilities", "").replace("-", "").strip()
            lines.append(f"        abilities: {_yaml_str(ab)}")
            lines.append(f"        is_melee: {'true' if melee else 'false'}")

        lines.append("")

    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <raw_scrape.txt>", file=sys.stderr)
        sys.exit(1)

    raw_path = sys.argv[1]
    faction = "orks"
    out_dir = Path(__file__).parent.parent / "data" / "wh40k_9e" / faction

    print(f"Parsing {raw_path}...", file=sys.stderr)
    units = parse_raw(raw_path)
    print(f"  → {len(units)} units parsed", file=sys.stderr)

    units_yaml = build_units_yaml(units, faction)
    weapons_yaml = build_weapons_yaml(units, faction)

    units_path = out_dir / "units.yaml"
    weapons_path = out_dir / "weapons.yaml"

    units_path.write_text(units_yaml)
    weapons_path.write_text(weapons_yaml)

    print(f"Written: {units_path}", file=sys.stderr)
    print(f"Written: {weapons_path}", file=sys.stderr)

    # Quick sanity check
    weapon_count = weapons_yaml.count("\n  - id:")
    print(f"  → {weapon_count} unique weapons", file=sys.stderr)


if __name__ == "__main__":
    main()
