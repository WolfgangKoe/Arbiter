from src.domain.models.army import Army
from src.domain.models.unit import BATTLEFIELD_ROLE_DE, Unit


def _unit(name_de: str, roles: list[str]) -> Unit:
    return Unit(id=f"test.{name_de}", name_en=name_de, name_de=name_de, roles=roles)


def test_unit_has_roles_and_keywords() -> None:
    unit = Unit(
        id="test.warrior",
        name_en="Necron Warrior",
        name_de="Necron-Krieger",
        roles=["Troops"],
        keywords=["Infantry", "Core"],
    )
    assert unit.roles == ["Troops"]
    assert "Infantry" in unit.keywords


def test_army_units_by_role_groups_correctly() -> None:
    warrior = _unit("Krieger", ["Troops"])
    overlord = _unit("Hochlord", ["HQ"])
    wraith = _unit("Phantom", ["Fast Attack"])

    army = Army(name="Necrons", faction="Necrons", units=[warrior, overlord, wraith])
    grouped = army.units_by_role()

    assert "HQ" in grouped
    assert "Standard" in grouped
    assert "Sturm" in grouped
    assert grouped["HQ"] == [overlord]
    assert grouped["Standard"] == [warrior]
    assert grouped["Sturm"] == [wraith]


def test_army_units_by_role_respects_order() -> None:
    units = [
        _unit("Gruftklingen", ["Fast Attack"]),
        _unit("Hochlord", ["HQ"]),
        _unit("Krieger", ["Troops"]),
    ]
    army = Army(name="Necrons", faction="Necrons", units=units)
    keys = list(army.units_by_role().keys())

    assert keys.index("HQ") < keys.index("Standard") < keys.index("Sturm")


def test_army_units_by_role_unknown_role_goes_to_sonstige() -> None:
    unit = _unit("Unbekannt", ["Unbekannte Rolle"])
    army = Army(name="Test", faction="Test", units=[unit])
    grouped = army.units_by_role()
    assert "Sonstige" in grouped
    assert grouped["Sonstige"] == [unit]


def test_army_units_by_role_empty_army() -> None:
    army = Army(name="Leer", faction="Test", units=[])
    assert army.units_by_role() == {}


def test_battlefield_role_de_contains_all_standard_roles() -> None:
    expected = {
        "HQ",
        "Troops",
        "Elites",
        "Fast Attack",
        "Heavy Support",
        "Flyer",
        "Dedicated Transport",
        "Lord of War",
    }
    assert expected == set(BATTLEFIELD_ROLE_DE.keys())
