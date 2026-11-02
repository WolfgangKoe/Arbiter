from collections.abc import Callable, Mapping
from typing import Any


def ganzeZahlÜberNull(zahl: object, was: str) -> int:
    if type(zahl) is not int or zahl <= 0:
        raise ValueError(f"{was} muss eine ganze Zahl über 0 sein: {zahl!r}")
    return zahl


def genauDieseSchlüsselLesen(
    eintrag: object, zeilen: Mapping[str, Callable[[object], Any]], was: str
) -> dict:
    if not isinstance(eintrag, dict) or set(eintrag) != set(zeilen):
        raise ValueError(f"{was} braucht genau die Schlüssel {sorted(zeilen)}")
    return {schlüssel: lesen(eintrag[schlüssel]) for schlüssel, lesen in zeilen.items()}


def abbildungLesen(werte: object, lesen: Callable[[object], Any], was: str) -> dict:
    if not isinstance(werte, dict) or not werte:
        raise ValueError(f"{was} braucht mindestens einen Eintrag")
    return {name: lesen(wert) for name, wert in werte.items()}
