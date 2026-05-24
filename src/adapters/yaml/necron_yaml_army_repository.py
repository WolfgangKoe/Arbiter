from pathlib import Path

import yaml

from src.domain.models.army import Army
from src.domain.models.unit import Unit
from src.domain.ports.army_repository import ArmyRepository

_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
_DEFAULT_UNITS_FILE = _PROJECT_ROOT / "data" / "wh40k_9e" / "necrons" / "units.yaml"


class NecronYamlArmyRepository(ArmyRepository):
    def __init__(self, units_file: Path = _DEFAULT_UNITS_FILE) -> None:
        self._units_file = units_file

    def get_army(self) -> Army:
        with self._units_file.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)

        units = [_parse_unit(entry) for entry in data.get("units", [])]
        return Army(name="Necrons", faction="Necrons", units=units)


def _parse_unit(entry: dict) -> Unit:
    keywords = entry.get("keywords", {})
    return Unit(
        id=entry["id"],
        name_en=entry["name_en"],
        name_de=entry["name_de"],
        roles=list(keywords.get("battlefield_role", [])),
        keywords=list(keywords.get("other", [])),
    )
