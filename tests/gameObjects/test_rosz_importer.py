"""Tests for the BattleScribe .rosz importer."""

import io
import sys
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameObjects.loader import load_unit_catalog
from gameObjects.rosz_importer import (
    _build_name_map,
    _extract_units,
    _match_unit_name,
    import_roster,
    parse_ros_bytes,
    parse_rosz_bytes,
)

_BS_NS = "http://www.battlescribe.net/schema/rosterSchema"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_ros_xml(
    roster_name: str = "Test Army",
    units: list[tuple[str, int]] | None = None,
    catalogue_name: str = "Necrons",
) -> bytes:
    """Build a minimal BattleScribe XML roster as bytes."""
    if units is None:
        units = [("Overlord", 1), ("Necron Warriors", 10)]

    unit_els = ""
    for name, model_count in units:
        unit_els += (
            f'\n<selection xmlns="{_BS_NS}" type="unit" name="{name}" quantity="1">'
            f"<selections>"
            f'<selection xmlns="{_BS_NS}" type="model" name="{name}" quantity="{model_count}"/>'
            f"</selections>"
            f"</selection>"
        )

    return (
        f'<?xml version="1.0" encoding="utf-8"?>'
        f'<roster xmlns="{_BS_NS}" name="{roster_name}">'
        f'<forces><force catalogueName="{catalogue_name}">'
        f"<selections>{unit_els}</selections>"
        f"</force></forces>"
        f"</roster>"
    ).encode()


def _make_rosz_bytes(
    roster_name: str = "Test Army", units: list[tuple[str, int]] | None = None
) -> bytes:
    """Pack a minimal .ros XML into a .rosz ZIP archive."""
    xml = _make_ros_xml(roster_name, units)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("roster.ros", xml)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# _build_name_map
# ---------------------------------------------------------------------------


def test_build_name_map_contains_slug() -> None:
    catalog = load_unit_catalog("necrons")
    name_map = _build_name_map(catalog)
    assert "overlord" in name_map
    assert name_map["overlord"] == "wh40k_9e.necrons.unit.overlord"


def test_build_name_map_contains_display_name() -> None:
    catalog = load_unit_catalog("necrons")
    name_map = _build_name_map(catalog)
    # "Royal Warden" normalises to "royal_warden"
    assert "royal_warden" in name_map
    assert name_map["royal_warden"] == "wh40k_9e.necrons.unit.royal_warden"


# ---------------------------------------------------------------------------
# _match_unit_name
# ---------------------------------------------------------------------------


def test_match_exact_name() -> None:
    catalog = load_unit_catalog("necrons")
    name_map = _build_name_map(catalog)
    uid = _match_unit_name("Overlord", name_map, "necrons")
    assert uid == "wh40k_9e.necrons.unit.overlord"


def test_match_necron_prefix_stripped() -> None:
    """BattleScribe exports 'Necron Warriors'; catalog has slug 'warriors'."""
    catalog = load_unit_catalog("necrons")
    name_map = _build_name_map(catalog)
    uid = _match_unit_name("Necron Warriors", name_map, "necrons")
    assert uid == "wh40k_9e.necrons.unit.warriors"


def test_match_necron_immortals_prefix_stripped() -> None:
    catalog = load_unit_catalog("necrons")
    name_map = _build_name_map(catalog)
    uid = _match_unit_name("Necron Immortals", name_map, "necrons")
    assert uid == "wh40k_9e.necrons.unit.immortals"


def test_match_unknown_returns_none() -> None:
    catalog = load_unit_catalog("necrons")
    name_map = _build_name_map(catalog)
    uid = _match_unit_name("Space Marine Captain", name_map, "necrons")
    assert uid is None


def test_match_canoptek_scarabs() -> None:
    catalog = load_unit_catalog("necrons")
    name_map = _build_name_map(catalog)
    uid = _match_unit_name("Canoptek Scarabs", name_map, "necrons")
    assert uid == "wh40k_9e.necrons.unit.canoptek_scarabs"


def test_match_ork_prefix_stripped() -> None:
    """BattleScribe exports 'Ork Boyz'; catalog has slug 'boyz'."""
    catalog = load_unit_catalog("orks")
    name_map = _build_name_map(catalog)
    uid = _match_unit_name("Ork Boyz", name_map, "orks")
    assert uid == "wh40k_9e.orks.unit.boyz"


def test_match_ork_exact_name() -> None:
    catalog = load_unit_catalog("orks")
    name_map = _build_name_map(catalog)
    uid = _match_unit_name("Warboss", name_map, "orks")
    assert uid == "wh40k_9e.orks.unit.warboss"


# ---------------------------------------------------------------------------
# _extract_units
# ---------------------------------------------------------------------------


def test_extract_units_basic() -> None:
    import xml.etree.ElementTree as ET

    xml_bytes = _make_ros_xml("Test", [("Overlord", 1), ("Warriors", 10)])
    root = ET.fromstring(xml_bytes)
    units = _extract_units(root)
    assert len(units) == 2
    names = {name for name, _ in units}
    assert "Overlord" in names
    assert "Warriors" in names


def test_extract_units_model_count() -> None:
    import xml.etree.ElementTree as ET

    xml_bytes = _make_ros_xml("Test", [("Lychguard", 5)])
    root = ET.fromstring(xml_bytes)
    units = _extract_units(root)
    assert units[0] == ("Lychguard", 5)


# ---------------------------------------------------------------------------
# parse_rosz_bytes / parse_ros_bytes
# ---------------------------------------------------------------------------


def test_parse_rosz_bytes_returns_roster_name() -> None:
    data = _make_rosz_bytes("My Necrons")
    roster_name, root = parse_rosz_bytes(data)
    assert roster_name == "My Necrons"


def test_parse_ros_bytes_returns_roster_name() -> None:
    data = _make_ros_xml("Alpha Legion")
    roster_name, root = parse_ros_bytes(data)
    assert roster_name == "Alpha Legion"


def test_parse_rosz_rejects_too_large() -> None:
    oversized = b"X" * (5 * 1024 * 1024 + 1)
    with pytest.raises(ValueError, match="too large"):
        parse_rosz_bytes(oversized)


def test_parse_rosz_rejects_bad_zip() -> None:
    with pytest.raises(ValueError, match="not a ZIP"):
        parse_rosz_bytes(b"this is not a zip file")


def test_parse_ros_bytes_rejects_wrong_namespace() -> None:
    bad_xml = b'<roster xmlns="http://example.com/wrong" name="Bad"/>'
    with pytest.raises(ValueError, match="namespace"):
        parse_ros_bytes(bad_xml)


def test_parse_rosz_rejects_zip_without_ros() -> None:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("readme.txt", "nothing here")
    with pytest.raises(ValueError, match="No .ros file"):
        parse_rosz_bytes(buf.getvalue())


# ---------------------------------------------------------------------------
# import_roster (round-trip)
# ---------------------------------------------------------------------------


def test_import_roster_writes_yaml(tmp_path: Path) -> None:

    import yaml

    xml_bytes = _make_ros_xml("Gamma Force", [("Overlord", 1), ("Necron Warriors", 10)])
    roster_name, root = parse_ros_bytes(xml_bytes)
    out_path, unmatched = import_roster(
        roster_name, root, faction_dir="necrons", output_dir=tmp_path
    )

    assert out_path.exists()
    data = yaml.safe_load(out_path.read_text())
    assert data["display_name"] == "Gamma Force"
    assert data["faction_dir"] == "necrons"
    assert any(u["id"] == "wh40k_9e.necrons.unit.overlord" for u in data["units"])
    assert any(u["id"] == "wh40k_9e.necrons.unit.warriors" for u in data["units"])


def test_import_roster_flags_unmatched(tmp_path: Path) -> None:

    xml_bytes = _make_ros_xml("Mixed", [("Overlord", 1), ("Unknown Unit", 5)])
    roster_name, root = parse_ros_bytes(xml_bytes)
    _, unmatched = import_roster(roster_name, root, faction_dir="necrons", output_dir=tmp_path)

    assert "Unknown Unit" in unmatched


def test_import_roster_matched_count(tmp_path: Path) -> None:
    import yaml

    xml_bytes = _make_ros_xml(
        "Full Army",
        [("Overlord", 1), ("Necron Warriors", 10), ("Canoptek Scarabs", 3)],
    )
    roster_name, root = parse_ros_bytes(xml_bytes)
    out_path, unmatched = import_roster(
        roster_name, root, faction_dir="necrons", output_dir=tmp_path
    )

    assert unmatched == []
    data = yaml.safe_load(out_path.read_text())
    warriors_entry = next(u for u in data["units"] if u["id"] == "wh40k_9e.necrons.unit.warriors")
    assert warriors_entry["models"] == 10


def test_import_roster_safe_filename(tmp_path: Path) -> None:
    xml_bytes = _make_ros_xml("Meine Armee / Test!", [("Overlord", 1)])
    roster_name, root = parse_ros_bytes(xml_bytes)
    out_path, _ = import_roster(roster_name, root, faction_dir="necrons", output_dir=tmp_path)
    assert out_path.suffix == ".yaml"
    assert "/" not in out_path.name
    assert "!" not in out_path.name


def test_import_roster_unknown_faction_raises(tmp_path: Path) -> None:
    """Unknown catalogueName without explicit faction_dir must raise ValueError."""
    xml_bytes = _make_ros_xml("Alpha Legion", [("Chaos Lord", 1)], catalogue_name="Space Marines")
    roster_name, root = parse_ros_bytes(xml_bytes)
    with pytest.raises(ValueError, match="_FACTION_CATALOGUE_MAP"):
        import_roster(roster_name, root, output_dir=tmp_path)


def test_import_roster_orks_roundtrip(tmp_path: Path) -> None:
    import yaml

    xml_bytes = _make_ros_xml(
        "Bad Moons Waaagh",
        [("Warboss", 1), ("Boyz", 10), ("Ork Boyz", 10)],
        catalogue_name="Orks",
    )
    roster_name, root = parse_ros_bytes(xml_bytes)
    out_path, unmatched = import_roster(roster_name, root, output_dir=tmp_path)

    assert out_path.exists()
    data = yaml.safe_load(out_path.read_text())
    assert data["faction_dir"] == "orks"
    assert any(u["id"] == "wh40k_9e.orks.unit.warboss" for u in data["units"])
    assert any(u["id"] == "wh40k_9e.orks.unit.boyz" for u in data["units"])
    assert unmatched == []
