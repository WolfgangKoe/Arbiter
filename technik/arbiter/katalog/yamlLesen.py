from pathlib import Path
from typing import Any

import yaml

_datenordner = Path(__file__).parents[3] / "domaene" / "daten"


def yamlLesen(*teileDesPfads: str) -> Any:
    pfad = _datenordner.joinpath(*teileDesPfads)
    with pfad.open(encoding="utf-8") as datei:
        text = datei.read()
    yamlPrüfen(text, pfad.name)
    return yaml.safe_load(text)


def yamlPrüfen(text: str, dateiname: str) -> None:
    for ereignis in yaml.parse(text):
        if isinstance(ereignis, yaml.AliasEvent) or getattr(ereignis, "anchor", None):
            raise ValueError(f"{dateiname} nutzt einen Anker oder Verweis")
    _schlüsselPrüfen(yaml.compose(text), dateiname)


def _schlüsselPrüfen(knoten: yaml.Node | None, dateiname: str) -> None:
    if isinstance(knoten, yaml.SequenceNode):
        for kind in knoten.value:
            _schlüsselPrüfen(kind, dateiname)
    if not isinstance(knoten, yaml.MappingNode):
        return
    schlüssel = [schlüsselknoten.value for schlüsselknoten, _ in knoten.value]
    if len(set(schlüssel)) != len(schlüssel):
        raise ValueError(f"{dateiname} nennt einen Schlüssel zweimal")
    for _, wert in knoten.value:
        _schlüsselPrüfen(wert, dateiname)
