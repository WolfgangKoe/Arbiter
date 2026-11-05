from collections.abc import Collection, Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import NamedTuple

from arbiter.domaene.querschnitt.setzen import befundeDesSetzens
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Modell, Stelle


@dataclass(frozen=True)
class Angebot:
    ebene: frozenset[Modell]
    gezogenes: Modell
    punkt: Stelle
    fliegen: bool = False


@dataclass(frozen=True)
class Übergangen:
    stellen: dict[Modell, Stelle]
    gründe: set[Grund]
    angehalten: frozenset[Grund]
    gezogenes: Modell


class Anteile(NamedTuple):
    bewegungsweite: Fraction
    spielfeldkante: Fraction
    nahkampfreichweite: Fraction

    @property
    def hältAnDerBewegungsweiteOderNahkampfreichweite(self) -> bool:
        früher = min(self.bewegungsweite, self.nahkampfreichweite)
        return früher < 1 and früher <= self.spielfeldkante

    @property
    def gründeDesAnhaltens(self) -> frozenset[Grund]:
        return frozenset(
            grund
            for grund, anteil in (
                (Grund.bewegungsweite, self.bewegungsweite),
                (Grund.nahkampfreichweite, self.nahkampfreichweite),
            )
            if anteil < 1
        )


def gründeBeimÜbergehen(
    neue: Mapping[Modell, Stelle],
    fremde: Mapping[Modell, Stelle],
    eigene: Collection[Modell],
) -> set[Grund]:
    gründe: set[Grund] = set()
    for modell, stelle in neue.items():
        gründe |= {
            grund
            for grund, trifft in befundeDesSetzens(modell, stelle, fremde, eigene).items()
            if trifft
        }
    return gründe - {Grund.nahkampfreichweite}
