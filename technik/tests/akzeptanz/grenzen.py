from collections.abc import Mapping
from fractions import Fraction
from typing import NamedTuple

import pytest

from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from tests.akzeptanz.dienst import kennungenDerEinheiten, stelleImSpielstand
from tests.akzeptanz.handgriffe import radiusInZoll, versetzt
from tests.akzeptanz.schlacht import jetzigeStellen, mitteDesSpielfelds, modellZurEbeneMachen

würfe = tuple(range(1, 7))
würfeIds = [f"wurf{wurf}" for wurf in würfe]
mitJedemWurf = pytest.mark.parametrize("wurf", würfe, ids=würfeIds)
halberZoll = Fraction(1, 2)
außerhalbDerSechsRinge = len(würfe) + 1
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


def alsZahlen(grenzen: frozenset[GrenzeDerKarte]) -> frozenset[GrenzeDerKarte]:
    return frozenset(
        grenze._replace(
            kreise=frozenset(
                (*stelleImSpielstand(stelle), float(radius)) for stelle, radius in grenze.kreise
            )
        )
        for grenze in grenzen
    )


def grenzenDerEinheitIm(spielstand: dict, einheitenname: str) -> frozenset[GrenzeDerKarte]:
    kennung = kennungenDerEinheiten[einheitenname]
    return frozenset(
        GrenzeDerKarte(
            frozenset((kreis["x"], kreis["y"], kreis["r"]) for kreis in grenze["kreise"]),
            grenze.get("wurf"),
            grenze.get("wählbar", False),
            grenze.get("nahkampfreichweite", False),
        )
        for grenze in spielstand["schlacht"]["grenzen"]
        if (grenze["spieler"], grenze["einheit"]) == kennung
    )


def ganzeEinheitAuswählen(schlacht, einheit: Einheit) -> dict[Modell, Stelle]:
    schlacht.auswählen(einheit)
    return jetzigeStellen(schlacht, einheit)


def letztesModellZurEbeneMachen(schlacht, einheit: Einheit) -> dict[Modell, Stelle]:
    *_, letztes = einheit.modelle
    modellZurEbeneMachen(schlacht, einheit, letztes)
    return {letztes: schlacht.stelle(letztes)}


ebenen = {"ganzeEinheit": ganzeEinheitAuswählen, "einModell": letztesModellZurEbeneMachen}
mitJederEbene = pytest.mark.parametrize("ebene", list(ebenen), ids=list(ebenen))


def unterDemLetztenModell(schlacht, einheit: Einheit, mehrAlsDieBewegung: Fraction) -> Stelle:
    *_, letztes = einheit.modelle
    abstand = letztes.bewegungsweite + radiusInZoll(letztes) + mehrAlsDieBewegung
    return versetzt(schlacht.stelle(letztes), (Fraction(0), abstand))


def stelleImRing(schlacht, einheit: Einheit, wurf: int) -> Stelle:
    return unterDemLetztenModell(schlacht, einheit, wurf - halberZoll)


def stelleAufDemKreis(schlacht, einheit: Einheit, wurf: int) -> Stelle:
    return unterDemLetztenModell(schlacht, einheit, Fraction(wurf))


def zweiZollZurMitte(stelle: Stelle) -> Stelle:
    richtung = 1 if stelle.x < mitteDesSpielfelds.x else -1
    return versetzt(stelle, (Fraction(2 * richtung), Fraction(0)))


def wartetAufDenVorrückwurf(schlacht, einheit: Einheit, ebene: str) -> dict[Modell, Stelle]:
    stellen = ebenen[ebene](schlacht, einheit)
    schlacht.vorrücken()
    return stellen


def vorgerücktMit(
    schlacht, einheit: Einheit, wurf: int, ebene: str = "ganzeEinheit"
) -> dict[Modell, Stelle]:
    stellen = wartetAufDenVorrückwurf(schlacht, einheit, ebene)
    schlacht.karteAnklicken(stelleImRing(schlacht, einheit, wurf))
    return stellen
