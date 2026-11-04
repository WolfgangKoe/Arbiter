from collections.abc import Callable, Mapping
from dataclasses import dataclass
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.messen import BasenAnStellen, Weg
from arbiter.domaene.spielobjekte import Modell, Stelle

type Stellen = Mapping[Modell, Stelle]
type AnteilBisZumAnhalten = Callable[[Stellen, Weg], Fraction]

keinWeg: Weg = (Fraction(0), Fraction(0))


@dataclass(frozen=True)
class Weiterrücken:
    zuvor: Stelle | None
    angehaltenAufDemWeg: bool


@dataclass(frozen=True)
class Geglitten:
    stellen: dict[Modell, Stelle]
    angehaltenAufDemWeg: bool


def keinAnhaltenAufDemWeg(*_: object) -> Fraction:
    return Fraction(1)


def zuvorGezeigt(vor: Stellen, gezogenes: Modell, weiter: Weiterrücken) -> dict[Modell, Stelle]:
    if weiter.zuvor is None:
        return dict(vor)
    return _verschoben(vor, messen.wegZwischen(vor[gezogenes], weiter.zuvor))


def gleiten(  # noqa: PLR0913
    zuvor: Stellen,
    weg: Weg,
    fremde: Stellen,
    anteilBisZumAnhalten: AnteilBisZumAnhalten,
    *,
    angehaltenAufDemWeg: bool,
    geprüft: Stellen | None = None,
) -> Geglitten:
    bewegte = _basenAnStellen(zuvor)
    hindernisse = _hindernisse(bewegte, fremde)
    if not _überdeckt(geprüft or _verschoben(zuvor, weg), hindernisse):
        anteil = anteilBisZumAnhalten(zuvor, weg) if angehaltenAufDemWeg else Fraction(1)
        return Geglitten(_verschoben(zuvor, messen.teilDesWegs(weg, anteil)), angehaltenAufDemWeg)
    wegInX, wegInY = weg
    for teil in ((wegInX, Fraction(0)), (Fraction(0), wegInY)):
        if _freierTeil(zuvor, teil, hindernisse, anteilBisZumAnhalten):
            return Geglitten(_verschoben(zuvor, teil), angehaltenAufDemWeg=True)
    bisZurBase = messen.anteilBisZurBerührungAufDemWeg(bewegte, hindernisse, weg)
    anteil = min(bisZurBase, anteilBisZumAnhalten(zuvor, weg))
    return Geglitten(_verschoben(zuvor, messen.teilDesWegs(weg, anteil)), angehaltenAufDemWeg=True)


def überdecktFremde(zuvor: Stellen, stellen: Stellen, fremde: Stellen) -> bool:
    return _überdeckt(stellen, _hindernisse(_basenAnStellen(zuvor), fremde))


def _freierTeil(
    zuvor: Stellen,
    teil: Weg,
    hindernisse: BasenAnStellen,
    anteilBisZumAnhalten: AnteilBisZumAnhalten,
) -> bool:
    return (
        teil != keinWeg
        and not _überdeckt(_verschoben(zuvor, teil), hindernisse)
        and anteilBisZumAnhalten(zuvor, teil) == 1
    )


def _verschoben(stellen: Stellen, weg: Weg) -> dict[Modell, Stelle]:
    return {modell: messen.verschoben(stelle, weg) for modell, stelle in stellen.items()}


def _basenAnStellen(stellen: Stellen) -> BasenAnStellen:
    return [(modell.base, stelle) for modell, stelle in stellen.items()]


def _überdeckt(stellen: Stellen, hindernisse: BasenAnStellen) -> bool:
    return any(
        messen.überdecken(modell.base, stelle, base, ort)
        for modell, stelle in stellen.items()
        for base, ort in hindernisse
    )


def _hindernisse(bewegte: BasenAnStellen, fremde: Stellen) -> BasenAnStellen:
    return [
        (modell.base, stelle)
        for modell, stelle in fremde.items()
        if not any(messen.überdecken(base, ort, modell.base, stelle) for base, ort in bewegte)
    ]
