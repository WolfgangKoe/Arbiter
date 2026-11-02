from collections.abc import Mapping
from fractions import Fraction
from typing import NamedTuple

import pytest

from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from tests.akzeptanz.handgriffe import radiusInZoll, versetzt

würfe = tuple(range(1, 7))
würfeIds = [f"wurf{wurf}" for wurf in würfe]
mitJedemWurf = pytest.mark.parametrize("wurf", würfe, ids=würfeIds)
einAuge = 1
dreiAugen = 3
vierAugen = 4
halberZoll = Fraction(1, 2)
außerhalbDerSechsGrenzkreise = len(würfe) + 1
innerhalbDesGrenzkreisesOhneWurf = 0


class EinheitAmZug(NamedTuple):
    schlacht: object
    einheit: Einheit
    andereEinheit: Einheit
    andererSpieler: Spieler


class GrenzeDerKarte(NamedTuple):
    kreise: frozenset[tuple]
    wurf: int | None = None
    wählbar: bool = False
    nahkampfreichweite: bool = False


def kreiseDerBewegung(
    stellen: Mapping[Modell, Stelle], wurf: int = 0
) -> frozenset[tuple[Stelle, Fraction]]:
    return frozenset(
        (stelle, modell.bewegungsweite + wurf + radiusInZoll(modell))
        for modell, stelle in stellen.items()
    )


def kreiseDerNahkampfreichweite(stellen: Mapping[Modell, Stelle]) -> frozenset[tuple]:
    return frozenset((stelle, radiusInZoll(modell) + 1) for modell, stelle in stellen.items())


def grenzeDerBewegung(stellen: Mapping[Modell, Stelle]) -> GrenzeDerKarte:
    return GrenzeDerKarte(kreiseDerBewegung(stellen))


def grenzeDesWurfs(stellen: Mapping[Modell, Stelle], wurf: int, *, wählbar: bool) -> GrenzeDerKarte:
    return GrenzeDerKarte(kreiseDerBewegung(stellen, wurf), wurf=wurf, wählbar=wählbar)


def grenzenVorDemVorrückwurf(stellen: Mapping[Modell, Stelle]) -> frozenset[GrenzeDerKarte]:
    sechs = (grenzeDesWurfs(stellen, wurf, wählbar=True) for wurf in würfe)
    return frozenset((grenzeDerBewegung(stellen), *sechs))


def grenzenNachDemVorrückwurf(
    stellen: Mapping[Modell, Stelle], wurf: int
) -> frozenset[GrenzeDerKarte]:
    return frozenset((grenzeDerBewegung(stellen), grenzeDesWurfs(stellen, wurf, wählbar=False)))


def grenzeDerNahkampfreichweite(stellen: Mapping[Modell, Stelle]) -> GrenzeDerKarte:
    return GrenzeDerKarte(kreiseDerNahkampfreichweite(stellen), nahkampfreichweite=True)


def grenzenDerEinheit(schlacht, einheit: Einheit) -> frozenset[GrenzeDerKarte]:
    return frozenset(
        GrenzeDerKarte(
            frozenset((kreis.stelle, kreis.radius) for kreis in grenze.kreise),
            grenze.wurf,
            grenze.wählbar,
            grenze.nahkampfreichweite,
        )
        for grenze in schlacht.grenzen
        if grenze.einheit is einheit
    )


def grenzenDerEinheitenDes(schlacht, spieler: Spieler) -> dict[Einheit, frozenset[GrenzeDerKarte]]:
    return {einheit: grenzenDerEinheit(schlacht, einheit) for einheit in spieler.armee.einheiten}


def unterDemLetztenModell(schlacht, einheit: Einheit, mehrAlsDieBewegung: Fraction) -> Stelle:
    *_, letztes = einheit.modelle
    abstand = letztes.bewegungsweite + radiusInZoll(letztes) + mehrAlsDieBewegung
    return versetzt(schlacht.stelle(letztes), (Fraction(0), abstand))


def stelleNurImGrenzkreisDesWurfs(schlacht, einheit: Einheit, wurf: int) -> Stelle:
    return unterDemLetztenModell(schlacht, einheit, wurf - halberZoll)


def stelleAufDemGrenzkreisDesWurfs(schlacht, einheit: Einheit, wurf: int) -> Stelle:
    return unterDemLetztenModell(schlacht, einheit, Fraction(wurf))


def zweiZollEntlangDerReihe(stelle: Stelle) -> Stelle:
    return versetzt(stelle, (Fraction(0), Fraction(2)))
