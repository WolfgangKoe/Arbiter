from collections.abc import Callable, Collection, Mapping
from dataclasses import dataclass, field
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import Weiterrücken
from arbiter.domaene.querschnitt.setzen import befundeDesSetzens
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Modell, Spielfeld, Stelle

type Stellen = Mapping[Modell, Stelle]
type AnteilAufDemWeg = Callable[[Stellen, messen.Weg], Fraction]


@dataclass(frozen=True)
class Gezogen:
    ebene: Mapping[Modell, Stelle]
    gezogenes: Modell
    ziel: Stelle
    weiter: Weiterrücken | None = None
    fliegen: bool = False


@dataclass(frozen=True)
class Weite:
    anfang: Stelle
    zoll: Fraction


@dataclass(frozen=True)
class Umgebung:
    fremde: Stellen
    gegner: Stellen
    spielfeld: Spielfeld
    weiten: Mapping[Modell, Weite] = field(default_factory=dict)


def verschobenUm(stellen: Stellen, weg: messen.Weg) -> dict[Modell, Stelle]:
    return {modell: messen.verschoben(stelle, weg) for modell, stelle in stellen.items()}


def gründeBeimZiehen(
    vorige: Mapping[Modell, Stelle],
    neue: Mapping[Modell, Stelle],
    fremde: Mapping[Modell, Stelle],
    eigene: Collection[Modell],
) -> set[Grund]:
    gründe: set[Grund] = set()
    for modell, stelle in neue.items():
        if stelle == vorige[modell]:
            continue
        befunde = befundeDesSetzens(modell, stelle, fremde, eigene)
        gründe |= {grund for grund, trifft in befunde.items() if trifft}
    return gründe
