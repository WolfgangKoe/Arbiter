from collections.abc import Iterator
from dataclasses import dataclass

from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Spieler


@dataclass(frozen=True, eq=False)
class Eintrag:
    einheit: Einheit
    spieler: Spieler
    gründe: frozenset[Grund]


class Protokoll:
    def __init__(self) -> None:
        self._einträge: list[Eintrag] = []

    def __iter__(self) -> Iterator[Eintrag]:
        return iter(tuple(self._einträge))

    def eintragen(self, einheit: Einheit, spieler: Spieler, gründe: frozenset[Grund]) -> None:
        self._einträge.append(Eintrag(einheit, spieler, gründe))
