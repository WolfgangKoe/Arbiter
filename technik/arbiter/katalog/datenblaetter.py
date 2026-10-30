from collections.abc import Callable, Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from arbiter.katalog.yamlLesen import yamlLesen


@dataclass(frozen=True)
class Modellart:
    bewegungsweite: Fraction
    durchmesser: int


type Datenblatt = Mapping[str, Modellart]


def ganzeZahlÜberNull(zahl: object, was: str) -> int:
    if type(zahl) is not int or zahl <= 0:
        raise ValueError(f"{was} muss eine ganze Zahl über 0 sein: {zahl!r}")
    return zahl


def _durchmesserLesen(zahl: object) -> int:
    return ganzeZahlÜberNull(zahl, "Der Durchmesser in mm")


def _bewegungsweiteLesen(zahl: object) -> Fraction:
    return Fraction(ganzeZahlÜberNull(zahl, "Die Bewegungsweite in Zoll"))


_modellartzeilen: Mapping[str, Callable[[object], Any]] = {
    "bewegungsweite": _bewegungsweiteLesen,
    "durchmesser": _durchmesserLesen,
}


def genauDieseSchlüsselLesen(
    eintrag: object, zeilen: Mapping[str, Callable[[object], Any]], was: str
) -> dict:
    if not isinstance(eintrag, dict) or set(eintrag) != set(zeilen):
        raise ValueError(f"{was} braucht genau die Schlüssel {sorted(zeilen)}")
    return {schlüssel: lesen(eintrag[schlüssel]) for schlüssel, lesen in zeilen.items()}


def modellartLesen(werte: object) -> Modellart:
    return Modellart(**genauDieseSchlüsselLesen(werte, _modellartzeilen, "Eine Modellart"))


def _modellartenLesen(modellarten: object) -> Datenblatt:
    if not isinstance(modellarten, dict) or not modellarten:
        raise ValueError("Ein Datenblatt braucht mindestens eine Modellart")
    return {name: modellartLesen(werte) for name, werte in modellarten.items()}


def _datenblattLesen(datenblatt: object) -> Datenblatt:
    return genauDieseSchlüsselLesen(
        datenblatt, {"modellarten": _modellartenLesen}, "Ein Datenblatt"
    )["modellarten"]


def datenblätterLesen(fraktion: str) -> Mapping[str, Datenblatt]:
    if not fraktion.isalnum():
        raise ValueError(f"Die Fraktion {fraktion!r} hat keinen Ordner")
    try:
        datenblätter = yamlLesen("katalog", fraktion, "datenblaetter.yaml")
    except FileNotFoundError as fehler:
        raise ValueError(f"Die Fraktion {fraktion} hat keinen Ordner") from fehler
    return {name: _datenblattLesen(datenblatt) for name, datenblatt in datenblätter.items()}
