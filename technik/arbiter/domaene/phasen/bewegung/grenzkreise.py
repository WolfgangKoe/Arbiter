from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.querschnitt.setzen import gesetzteModelle, nahkampfreichweite
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle

möglicheWürfe = range(1, 7)


@dataclass(frozen=True)
class Grenzkreis:
    stelle: Stelle
    radius: Fraction


@dataclass(frozen=True)
class Einhüllende:
    einheit: Einheit
    kreise: tuple[Grenzkreis, ...]
    wurf: int | None = None
    wählbar: bool = False
    nahkampfreichweite: bool = False


def _kreiseDerBewegung(ebene: Mapping[Modell, Stelle], wurf: int) -> tuple[Grenzkreis, ...]:
    return tuple(
        Grenzkreis(stelle, messen.radiusInZoll(modell.base) + modell.bewegungsweite + wurf)
        for modell, stelle in ebene.items()
    )


def grenzeDerBewegung(einheit: Einheit, ebene: Mapping[Modell, Stelle]) -> Einhüllende:
    return Einhüllende(einheit, _kreiseDerBewegung(ebene, 0))


def grenzenDerWürfe(
    einheit: Einheit, ebene: Mapping[Modell, Stelle], würfe: Iterable[int], *, wählbar: bool
) -> tuple[Einhüllende, ...]:
    return tuple(
        Einhüllende(einheit, _kreiseDerBewegung(ebene, wurf), wurf, wählbar) for wurf in würfe
    )


def grenzenDerNahkampfreichweite(
    einheiten: Iterable[Einheit], stellen: Mapping[Modell, Stelle]
) -> tuple[Einhüllende, ...]:
    grenzen = (
        Einhüllende(
            einheit,
            tuple(
                Grenzkreis(stelle, messen.radiusInZoll(modell.base) + nahkampfreichweite)
                for modell, stelle in gesetzteModelle(einheit, stellen).items()
            ),
            nahkampfreichweite=True,
        )
        for einheit in einheiten
    )
    return tuple(grenze for grenze in grenzen if grenze.kreise)


def enthält(kreise: Collection[Grenzkreis], stelle: Stelle) -> bool:
    return any(messen.abstandImQuadrat(kreis.stelle, stelle) <= kreis.radius**2 for kreis in kreise)


def kleinsterWurfAn(
    stelle: Stelle, bewegung: Einhüllende, würfe: Iterable[Einhüllende]
) -> int | None:
    if enthält(bewegung.kreise, stelle):
        return None
    return min(
        (
            grenze.wurf
            for grenze in würfe
            if grenze.wurf is not None and enthält(grenze.kreise, stelle)
        ),
        default=None,
    )
