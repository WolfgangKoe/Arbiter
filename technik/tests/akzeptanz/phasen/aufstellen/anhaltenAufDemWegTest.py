"""AUF-29 · Anhalten auf dem Weg."""

from fractions import Fraction
from http import HTTPStatus

import pytest

from tests.akzeptanz.anhalten import (
    angehaltenVor,
    aufDerStrecke,
    nichtAusgewähltOderMitModellebene,
    stelleAn,
)
from tests.akzeptanz.dienst import (
    eingabenDesWeiterrückens,
    gezeigteStellen,
    stelleBeimLoslassenAbfragen,
    stelleBeimWeiterrückenAbfragen,
    stellenDerEinheitIm,
    zuvorNachDerAbfrage,
)
from tests.akzeptanz.handgriffe import modelleAnStellenSetzen, radiusInZoll, versetzt
from tests.akzeptanz.ziehen import (
    WeitergereichteAbfragen,
    mitEinheitenebeneZiehen,
    zuvorDerEingaben,
    überEinenPunktZiehenUndLoslassen,
)


def testAuf29_1DerDienstHältDasModellAufDerStreckeVorDerFremdenBaseAn(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    aufstellung = aufstellungNachDerZonenwahl
    gezogenes, angestoßenes, *_ = boyz.modelle
    davor, stelleDesAngestoßenen = stelleAn(aufstellung, (4, 20)), stelleAn(aufstellung, (4, 23))
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleDesAngestoßenen])

    antwort = stelleBeimLoslassenAbfragen(
        dienst, aufstellung, boyz, gezogenes, stelleDesAngestoßenen
    )

    (gezeigt,) = gezeigteStellen(antwort, "Boyz").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, davor, stelleDesAngestoßenen)
    assert angehaltenVor(gezogenes, gezeigt, angestoßenes, stelleDesAngestoßenen)


def testAuf29_1AmFreienZielZeigtDerDienstDasZielAuchWennDerWegÜberEineBaseFührt(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    aufstellung = aufstellungNachDerZonenwahl
    gezogenes, *_ = boyz.modelle
    davor, stelleImWeg = stelleAn(aufstellung, (4, 20)), stelleAn(aufstellung, (4, 23))
    freiesZiel = stelleAn(aufstellung, (4, 26))
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleImWeg])

    antwort = stelleBeimLoslassenAbfragen(dienst, aufstellung, boyz, gezogenes, freiesZiel)

    assert antwort.status_code == HTTPStatus.OK
    assert gezeigteStellen(antwort, "Boyz") == {1: freiesZiel}


def testAuf29_1DerDienstHältAufDerStreckeAbDerZuvorGezeigtenStelleAn(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    aufstellung = aufstellungNachDerZonenwahl
    gezogenes, angestoßenes, *_ = boyz.modelle
    davor, stelleDesAngestoßenen = stelleAn(aufstellung, (4, 20)), stelleAn(aufstellung, (6, 23))
    zuvorGezeigt = stelleAn(aufstellung, (6, 20))
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleDesAngestoßenen])
    zuvor = zuvorNachDerAbfrage(dienst, aufstellung, boyz, gezogenes, zuvorGezeigt)
    eingaben = eingabenDesWeiterrückens(stelleDesAngestoßenen, zuvor)

    antwort = stelleBeimWeiterrückenAbfragen(dienst, aufstellung, boyz, gezogenes, eingaben)

    (gezeigt,) = gezeigteStellen(antwort, "Boyz").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, zuvorGezeigt, stelleDesAngestoßenen)
    assert angehaltenVor(gezogenes, gezeigt, angestoßenes, stelleDesAngestoßenen)


def testAuf29_1DieSeiteSchicktJederAbfrageDieZuvorGezeigteStelleDesGezogenenModells(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    aufstellung = aufstellungNachDerZonenwahl
    davor, stelleDesAngestoßenen = stelleAn(aufstellung, (4, 20)), stelleAn(aufstellung, (4, 23))
    daneben = stelleAn(aufstellung, (6, 23))
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleDesAngestoßenen])
    seite = bildschirm.seiteZu(aufstellung)
    abfragen = WeitergereichteAbfragen(seite)

    überEinenPunktZiehenUndLoslassen(seite, davor, stelleDesAngestoßenen, daneben)

    zuvorGezeigt = [
        stellenDerEinheitIm(antwort, "Boyz")[1] if antwort else ()
        for antwort in abfragen.letzte200VorJederAbfrage()
    ]
    assert [zuvorDerEingaben(eingaben) for eingaben in abfragen.eingaben] == zuvorGezeigt


@pytest.mark.parametrize(
    "orteDesWeiterrückens",
    [
        (
            (Fraction("4.5"), Fraction("21.5")),
            (Fraction("5.25"), Fraction("22.25")),
            (Fraction("5.25"), Fraction("21.5")),
        ),
        (
            (Fraction("4.5"), Fraction(23)),
            (Fraction("5.25"), Fraction("23.75")),
            (Fraction("4.5"), Fraction("23.75")),
        ),
        (
            (Fraction(6), Fraction("21.5")),
            (Fraction("6.75"), Fraction("22.25")),
            (Fraction("6.75"), Fraction("21.5")),
        ),
    ],
    ids=["beideTeileFreiWaagrecht", "nurSenkrechtFrei", "nurWaagrechtFrei"],
)
def testAuf29_2DerDienstZeigtDasModellUmDenFreienTeilDesWegesVerschoben(
    dienst, aufstellungNachDerZonenwahl, boyz, orteDesWeiterrückens
):
    aufstellung = aufstellungNachDerZonenwahl
    zuvorGezeigtAn, zielAn, gezeigtAn = orteDesWeiterrückens
    gezogenes, *_ = boyz.modelle
    davor, stelleImWeg = stelleAn(aufstellung, (3, 20)), stelleAn(aufstellung, (6, 23))
    zuvorGezeigt, ziel = stelleAn(aufstellung, zuvorGezeigtAn), stelleAn(aufstellung, zielAn)
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleImWeg])
    zuvor = zuvorNachDerAbfrage(dienst, aufstellung, boyz, gezogenes, zuvorGezeigt)
    eingaben = eingabenDesWeiterrückens(ziel, zuvor)

    antwort = stelleBeimWeiterrückenAbfragen(dienst, aufstellung, boyz, gezogenes, eingaben)

    assert antwort.status_code == HTTPStatus.OK
    assert gezeigteStellen(antwort, "Boyz") == {1: stelleAn(aufstellung, gezeigtAn)}


def testAuf29_3BeiDerEinheitenebeneZeigtDerDienstAlleAmEigenenModellVorbeiVerschoben(
    dienst, aufstellungNachDerZonenwahl, necronWarriors, warriorsVorDemOverlord
):
    aufstellung = aufstellungNachDerZonenwahl
    gesetzte, zielAmOverlord = warriorsVorDemOverlord
    (gezogenes, _), *_ = gesetzte
    umDenSenkrechtenTeil = (Fraction(0), radiusInZoll(gezogenes))
    mitEinheitenebeneZiehen(aufstellung, necronWarriors)

    antwort = stelleBeimLoslassenAbfragen(
        dienst, aufstellung, necronWarriors, gezogenes, zielAmOverlord
    )

    assert antwort.status_code == HTTPStatus.OK
    assert gezeigteStellen(antwort, "Necron Warriors") == {
        nummer: versetzt(stelle, umDenSenkrechtenTeil)
        for nummer, (_, stelle) in enumerate(gesetzte, start=1)
    }


@nichtAusgewähltOderMitModellebene
def testAuf29_3AlleinGezogenHältDerDienstVorDemModellDerselbenEinheitAn(
    dienst, aufstellungNachDerZonenwahl, necronWarriors, warriorsVorDemOverlord, ebeneLegen
):
    aufstellung = aufstellungNachDerZonenwahl
    gesetzte, zielAmOverlord = warriorsVorDemOverlord
    (gezogenes, davor), (angestoßenes, stelleDesAngestoßenen), _ = gesetzte
    ebeneLegen(aufstellung, necronWarriors, gezogenes)

    antwort = stelleBeimLoslassenAbfragen(
        dienst, aufstellung, necronWarriors, gezogenes, zielAmOverlord
    )

    (gezeigt,) = gezeigteStellen(antwort, "Necron Warriors").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, davor, zielAmOverlord)
    assert angehaltenVor(gezogenes, gezeigt, angestoßenes, stelleDesAngestoßenen)
