import pytest

from src.adapters.yaml.necron_yaml_army_repository import NecronYamlArmyRepository
from src.domain.models.army import Army
from src.domain.models.unit import Unit


@pytest.fixture()
def repo() -> NecronYamlArmyRepository:
    return NecronYamlArmyRepository()


def test_get_army_returns_army(repo: NecronYamlArmyRepository) -> None:
    army = repo.get_army()
    assert isinstance(army, Army)
    assert army.name == "Necrons"
    assert army.faction == "Necrons"


def test_get_army_loads_units(repo: NecronYamlArmyRepository) -> None:
    army = repo.get_army()
    assert len(army.units) > 0


def test_units_are_unit_instances(repo: NecronYamlArmyRepository) -> None:
    army = repo.get_army()
    for unit in army.units:
        assert isinstance(unit, Unit)


def test_units_have_german_names(repo: NecronYamlArmyRepository) -> None:
    army = repo.get_army()
    necron_warriors = next(u for u in army.units if "warrior" in u.id)
    assert necron_warriors.name_de == "Necron-Krieger"


def test_units_have_roles(repo: NecronYamlArmyRepository) -> None:
    army = repo.get_army()
    for unit in army.units:
        assert isinstance(unit.roles, list)


def test_overlord_is_hq(repo: NecronYamlArmyRepository) -> None:
    army = repo.get_army()
    overlord = next(u for u in army.units if "overlord" in u.id and "catacomb" not in u.id)
    assert "HQ" in overlord.roles


def test_no_curated_data_leaks_into_unit(repo: NecronYamlArmyRepository) -> None:
    army = repo.get_army()
    unit = army.units[0]
    assert not hasattr(unit, "curated_status")
    assert not hasattr(unit, "notes")
    assert not hasattr(unit, "curation")


def test_units_by_role_contains_hq_and_troops(repo: NecronYamlArmyRepository) -> None:
    army = repo.get_army()
    grouped = army.units_by_role()
    assert "HQ" in grouped
    assert "Standard" in grouped
