"""Die Gründe gegen das Beenden des Aufstellens einer Einheit (AUF-10.3, D4)."""

from collections.abc import Callable, Mapping

from arbiter.domaene.querschnitt.kohaerenz import inKohärenz
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle

Prüfung = Callable[[Einheit, Mapping[Modell, Stelle]], bool]


def gesetzteModelle(einheit: Einheit, stellen: Mapping[Modell, Stelle]) -> dict[Modell, Stelle]:
    """Die Stellen der gesetzten Modelle der Einheit."""
    return {modell: stellen[modell] for modell in einheit.modelle if modell in stellen}


def _ohneKohärenz(einheit: Einheit, stellen: Mapping[Modell, Stelle]) -> bool:
    return not inKohärenz(gesetzteModelle(einheit, stellen))


_prüfungen: dict[Grund, Prüfung] = {
    Grund.keineKohärenz: _ohneKohärenz,
}


def gründeGegenDasBeenden(einheit: Einheit, stellen: Mapping[Modell, Stelle]) -> set[Grund]:
    return {grund for grund, prüfung in _prüfungen.items() if prüfung(einheit, stellen)}
