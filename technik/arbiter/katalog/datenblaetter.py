from collections.abc import Callable, Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from arbiter.katalog.eintragLesen import (
    abbildungLesen,
    ganzeZahlÜberNull,
    genauDieseSchlüsselLesen,
)
from arbiter.katalog.yamlLesen import yamlLesen


@dataclass(frozen=True)
class Modellart:
    bewegungsweite: Fraction
    durchmesser: int


type Datenblatt = Mapping[str, Modellart]


def _durchmesserLesen(zahl: object) -> int:
    return ganzeZahlÜberNull(zahl, "Der Durchmesser in mm")


def _bewegungsweiteLesen(zahl: object) -> Fraction:
    return Fraction(ganzeZahlÜberNull(zahl, "Die Bewegungsweite in Zoll"))


_modellartzeilen: Mapping[str, Callable[[object], Any]] = {
    "bewegungsweite": _bewegungsweiteLesen,
    "durchmesser": _durchmesserLesen,
}


def modellartLesen(werte: object) -> Modellart:
    return Modellart(**genauDieseSchlüsselLesen(werte, _modellartzeilen, "Eine Modellart"))


def _modellartenLesen(modellarten: object) -> Datenblatt:
    return abbildungLesen(modellarten, modellartLesen, "Ein Datenblatt")


def _datenblattLesen(datenblatt: object) -> Datenblatt:
    return genauDieseSchlüsselLesen(
        datenblatt, {"modellarten": _modellartenLesen}, "Ein Datenblatt"
    )["modellarten"]


def datenblätterLesen(fraktion: str) -> Mapping[str, Datenblatt]:
    keineDatenblätter = ValueError(f"Die Fraktion {fraktion!r} hat keine datenblaetter.yaml")
    if not fraktion.isalnum():
        raise keineDatenblätter
    try:
        datenblätter = yamlLesen("katalog", fraktion, "datenblaetter.yaml")
    except FileNotFoundError as fehler:
        raise keineDatenblätter from fehler
    return abbildungLesen(datenblätter, _datenblattLesen, f"Die datenblaetter.yaml von {fraktion}")
