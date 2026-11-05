from collections.abc import Callable, Mapping
from types import MappingProxyType
from typing import Any


def ganzeZahlÜberNull(zahl: object, was: str) -> int:
    if type(zahl) is not int or zahl <= 0:
        raise ValueError(f"{was} muss eine ganze Zahl über 0 sein: {zahl!r}")
    return zahl


def genauDieseSchlüsselLesen(
    eintrag: object,
    zeilen: Mapping[str, Callable[[object], Any]],
    was: str,
    freiwillig: Mapping[str, Callable[[object], Any]] = MappingProxyType({}),
) -> dict:
    erlaubt = {**zeilen, **freiwillig}
    if not isinstance(eintrag, dict) or not set(zeilen) <= set(eintrag) <= set(erlaubt):
        raise ValueError(f"{was} braucht genau die Schlüssel {sorted(zeilen)}")
    return {schlüssel: erlaubt[schlüssel](wert) for schlüssel, wert in eintrag.items()}


def wahrheitswertLesen(wert: object, was: str) -> bool:
    if type(wert) is not bool:
        raise ValueError(f"{was} muss true oder false sein: {wert!r}")
    return wert


def abbildungLesen(werte: object, lesen: Callable[[object], Any], was: str) -> dict:
    if not isinstance(werte, dict) or not werte:
        raise ValueError(f"{was} braucht mindestens einen Eintrag")
    return {name: lesen(wert) for name, wert in werte.items()}
