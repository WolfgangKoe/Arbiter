"""Import BattleScribe .rosz/.ros roster files into Arbiter roster YAML format.

Supported flow:
- parse_rosz_bytes / parse_ros_bytes  →  (roster_name, xml_root)
- import_roster(roster_name, root)    →  (output_path, unmatched_names)
"""

import io
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import yaml
from defusedxml.ElementTree import fromstring as _safe_fromstring

from gameObjects.loader import load_unit_catalog

_BS_NS = "http://www.battlescribe.net/schema/rosterSchema"
_MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

_ROSTERS_DIR = Path(__file__).parent.parent.parent / "data" / "rosters"

# Maps catalogue name fragment (lowercase) → faction_dir
_FACTION_CATALOGUE_MAP: dict[str, str] = {
    "necrons": "necrons",
    "adeptus custodes": "adeptus_custodes",
    "custodes": "adeptus_custodes",
    "orks": "orks",
    "ork": "orks",
}


def _normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def _build_name_map(catalog: dict) -> dict[str, str]:
    """Build normalized-display-name and slug → unit-id lookup."""
    mapping: dict[str, str] = {}
    for uid, unit in catalog.items():
        slug = uid.rsplit(".", 1)[-1]
        mapping[_normalize(unit.name_en)] = uid
        mapping[slug] = uid
    return mapping


def _build_weapon_name_map(weapon_catalog: dict) -> dict[str, str]:
    """Build normalized-display-name and slug → weapon-id lookup."""
    mapping: dict[str, str] = {}
    for wid, weapon in weapon_catalog.items():
        slug = wid.rsplit(".", 1)[-1]
        mapping[_normalize(weapon.name_en)] = wid
        mapping[slug] = wid
    return mapping


def _match_unit_name(bs_name: str, name_map: dict[str, str], faction_dir: str) -> str | None:
    """Return unit ID for a BattleScribe selection name, or None if unmatched.

    BattleScribe sometimes prepends the faction name (e.g. "Necron Warriors", "Ork Boyz").
    Strips "{faction_dir}_" and singular form "{faction_dir.rstrip('s')}_" as prefixes.
    """
    norm = _normalize(bs_name)
    if norm in name_map:
        return name_map[norm]
    singular = faction_dir.rstrip("s")
    for prefix in (f"{faction_dir}_", f"{singular}_"):
        if norm.startswith(prefix):
            stripped = norm[len(prefix) :]
            if stripped in name_map:
                return name_map[stripped]
    return None


def _collect_upgrade_names(element: ET.Element, ns: dict) -> list[str]:
    """Recursively collect all 'upgrade' selection names inside element."""
    names: list[str] = []
    sub_sels = element.find("bs:selections", ns)
    if sub_sels is None:
        return names
    for sel in sub_sels.findall("bs:selection", ns):
        if sel.attrib.get("type") == "upgrade":
            name = sel.attrib.get("name", "")
            if name:
                names.append(name)
            names.extend(_collect_upgrade_names(sel, ns))
        else:
            # Recurse into model sub-selections to catch nested upgrades
            names.extend(_collect_upgrade_names(sel, ns))
    return names


def _extract_units(root: ET.Element) -> list[tuple[str, int, list[str]]]:
    """Extract (unit_name, model_count, wargear_names) triples from a BattleScribe XML.

    BattleScribe structure:
      <roster> → <forces> → <force> → <selections> → <selection type="unit">
        → <selections> → <selection type="model" quantity="N">
    Single-model units may be exported as top-level type="model" selections.
    wargear_names contains all nested 'upgrade' selection names (weapons/wargear).
    """
    ns = {"bs": _BS_NS}
    units: list[tuple[str, int, list[str]]] = []

    for selections_el in root.findall(".//bs:force/bs:selections", ns):
        for sel in selections_el.findall("bs:selection", ns):
            sel_type = sel.attrib.get("type", "")
            if sel_type not in ("unit", "model"):
                continue

            name = sel.attrib.get("name", "")
            quantity = int(sel.attrib.get("quantity", sel.attrib.get("number", "1")))
            wargear_names = _collect_upgrade_names(sel, ns)

            if sel_type == "unit":
                model_count = _count_models(sel, ns)
                if model_count == 0:
                    model_count = quantity
                units.append((name, model_count, wargear_names))
            else:
                units.append((name, quantity, wargear_names))

    return units


def _count_models(unit_sel: ET.Element, ns: dict) -> int:
    sub_sels = unit_sel.find("bs:selections", ns)
    if sub_sels is None:
        return 0
    return sum(
        int(s.attrib.get("quantity", s.attrib.get("number", "1")))
        for s in sub_sels.findall("bs:selection", ns)
        if s.attrib.get("type") == "model"
    )


def _detect_faction(root: ET.Element) -> str | None:
    ns = {"bs": _BS_NS}
    for force in root.findall(".//bs:force", ns):
        catalogue_name = force.attrib.get("catalogueName", "").lower()
        for key, faction_dir in _FACTION_CATALOGUE_MAP.items():
            if key in catalogue_name:
                return faction_dir
    return None


def _validate_and_parse_xml(data: bytes) -> ET.Element:
    root = _safe_fromstring(data)
    if _BS_NS not in root.tag:
        raise ValueError(f"Not a BattleScribe roster (unexpected root namespace: {root.tag!r})")
    return root


def parse_rosz_bytes(data: bytes) -> tuple[str, ET.Element]:
    """Unpack a .rosz (ZIP) from raw bytes and return (roster_name, xml_root)."""
    if len(data) > _MAX_SIZE_BYTES:
        raise ValueError(f"File too large ({len(data):,} bytes; max 5 MB)")
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            ros_files = [n for n in zf.namelist() if n.endswith(".ros")]
            if not ros_files:
                raise ValueError("No .ros file found inside the .rosz archive")
            xml_bytes = zf.read(ros_files[0])
    except zipfile.BadZipFile as exc:
        raise ValueError(f"Invalid .rosz file (not a ZIP archive): {exc}") from exc
    root = _validate_and_parse_xml(xml_bytes)
    return root.attrib.get("name", "imported_roster"), root


def parse_ros_bytes(data: bytes) -> tuple[str, ET.Element]:
    """Parse a bare .ros XML file from raw bytes and return (roster_name, xml_root)."""
    if len(data) > _MAX_SIZE_BYTES:
        raise ValueError(f"File too large ({len(data):,} bytes; max 5 MB)")
    root = _validate_and_parse_xml(data)
    return root.attrib.get("name", "imported_roster"), root


def import_roster(
    roster_name: str,
    root: ET.Element,
    faction_dir: str | None = None,
    output_dir: Path = _ROSTERS_DIR,
) -> tuple[Path, list[str]]:
    """Convert a parsed BS XML roster into an Arbiter roster YAML.

    Returns (output_path, unmatched_names).
    Unmatched names are units that could not be resolved against the catalog.
    """
    if faction_dir is None:
        faction_dir = _detect_faction(root)
        if faction_dir is None:
            raise ValueError(
                "Unknown faction in BattleScribe roster. "
                "Add the catalogue name to _FACTION_CATALOGUE_MAP in rosz_importer.py."
            )

    from gameObjects.loader import load_weapon_catalog  # noqa: PLC0415

    catalog = load_unit_catalog(faction_dir)
    if not catalog:
        raise ValueError(
            f"No unit catalog found for faction '{faction_dir}'. "
            "Add a units.yaml to data/wh40k_9e/{faction_dir}/ before importing."
        )
    weapon_catalog = load_weapon_catalog(faction_dir)
    name_map = _build_name_map(catalog)
    weapon_name_map = _build_weapon_name_map(weapon_catalog)
    bs_units = _extract_units(root)

    matched: list[dict] = []
    unmatched: list[str] = []
    for name, count, wargear_names in bs_units:
        uid = _match_unit_name(name, name_map, faction_dir)
        if uid is None:
            unmatched.append(name)
        else:
            entry: dict = {"id": uid, "models": count}
            matched_wargear = [
                weapon_name_map[_normalize(wn)]
                for wn in wargear_names
                if _normalize(wn) in weapon_name_map
            ]
            if matched_wargear:
                entry["wargear"] = matched_wargear
            matched.append(entry)

    safe_name = re.sub(r"[^a-z0-9_]+", "_", roster_name.lower()).strip("_") or "roster"
    output_path = output_dir / f"{safe_name}.yaml"

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(
            {"display_name": roster_name, "faction_dir": faction_dir, "units": matched},
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    return output_path, unmatched
