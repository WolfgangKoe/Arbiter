"""AUF-26 · Klemmen beim Ziehen."""

from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.anhalten import (
    ebeneAufDasModellLegen,
    freiesZiel,
    hineinrückenOhneBase,
    stellenAlsZahlen,
    stellenDesZugs,
)
from tests.akzeptanz.bildschirm import seiteMitEingabe, sperrmeldungenDerSeite
from tests.akzeptanz.dienst import (
    modellLoslassen,
    spielstandVon,
    stelleBeimLoslassenAbfragen,
    stelleImSpielstand,
    stellenDerAbfrage,
    stellenDerEinheitIm,
)
from tests.akzeptanz.handgriffe import (
    erwarteteStelle,
    millionstel,
    modelleAnStellenSetzen,
    modelleSetzen,
    radiusInZoll,
    stelleInDerZoneDesSpielersAnDerReihe,
    tiefeDerZone,
)
from tests.akzeptanz.ziehen import (
    haltenUndLosslassen,
    liegtEinPixelGenauAn,
    mitMausUndFinger,
    modellZiehen,
)

hineinrücken = pytest.mark.parametrize(
    ("ziel", "erwartet"),
    [
        ((12, 20), ((9, -1), (20, 0))),
        ((-3, 20), ((0, 1), (20, 0))),
        ((4, -5), ((4, 0), (0, 1))),
        ((4, 65), ((4, 0), (60, -1))),
        ((12, 65), ((9, -1), (60, -1))),
        ((40, 20), ((9, -1), (20, 0))),
    ],
    ids=[
        "überDieInnenkante",
        "überDieSpielfeldkante",
        "amAnfang",
        "amEnde",
        "inDerEcke",
        "inDerZoneDesAnderen",
    ],
)


@hineinrücken
def testAuf26_1EinModellAußerhalbDerZoneRücktAufKürzestemWegHineinOhneGrund(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, ziel, erwartet
):
    [(modell, _)] = modelleSetzen(aufstellung, ersteEinheitDesSpielersAnDerReihe, 1)
    tiefe, länge = ziel
    stelleDesLoslassens = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefe, länge)
    stelleNachDemRücken = erwarteteStelle(aufstellung, radiusInZoll(modell), erwartet)

    aufstellung.modellLoslassen(modell, stelleDesLoslassens)

    assert aufstellung.gesetzt(modell)
    assert aufstellung.stelle(modell) == stelleNachDemRücken


def testAuf26_1EineBaseDieDieGrenzeDerZoneBerührtBleibtDortOhneGrund(
    aufstellung, ersteEinheitDesSpielersAnDerReihe
):
    [(modell, _)] = modelleSetzen(aufstellung, ersteEinheitDesSpielersAnDerReihe, 1)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, tiefeDerZone - radiusInZoll(modell), 20
    )

    aufstellung.modellLoslassen(modell, ziel)

    assert aufstellung.gesetzt(modell)
    assert aufstellung.stelle(modell) == ziel


def testAuf26_1EineBaseEinMillionstelZollJenseitsDerGrenzeRücktAnDieGrenzeOhneGrund(
    aufstellung, ersteEinheitDesSpielersAnDerReihe
):
    [(modell, _)] = modelleSetzen(aufstellung, ersteEinheitDesSpielersAnDerReihe, 1)
    radius = radiusInZoll(modell)
    grenze = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefeDerZone - radius, 20)
    knappDrüber = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, tiefeDerZone - radius + millionstel, 20
    )

    aufstellung.modellLoslassen(modell, knappDrüber)

    assert aufstellung.gesetzt(modell)
    assert aufstellung.stelle(modell) == grenze


@hineinrücken
def testAuf26_1DerDienstRücktDasModellHineinOhneGrund(
    dienst, aufstellungNachDerZonenwahl, boyz, ziel, erwartet
):
    aufstellung = aufstellungNachDerZonenwahl
    [(modell, _)] = modelleSetzen(aufstellung, boyz, 1)
    tiefe, länge = ziel
    stelleDesLoslassens = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefe, länge)
    stelleNachDemRücken = erwarteteStelle(aufstellung, radiusInZoll(modell), erwartet)

    antwort = modellLoslassen(dienst, aufstellung, boyz, modell, stelleDesLoslassens)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(spielstand, "Boyz") == {1: stelleImSpielstand(stelleNachDemRücken)}


@mitMausUndFinger
def testAuf26_1DieSeiteRücktDasModellInnerhalbDerKarteHineinOhneGrund(
    bildschirm, aufstellungNachDerZonenwahl, boyz, eingabe
):
    aufstellung = aufstellungNachDerZonenwahl
    [(modell, davor)] = modelleSetzen(aufstellung, boyz, 1)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 12, 20)
    stelleNachDemRücken = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, tiefeDerZone - radiusInZoll(modell), 20
    )
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)

    modellZiehen(seite, davor, ziel, eingabe)

    assert aufstellung.gesetzt(modell)
    assert liegtEinPixelGenauAn(seite, aufstellung.stelle(modell), stelleNachDemRücken)
    expect(seite.locator(".karte .modell")).to_have_count(1)
    assert sperrmeldungenDerSeite(seite) == []


zügeFürDieAbfrage = pytest.mark.parametrize(
    "zug", [freiesZiel, hineinrückenOhneBase], ids=["freiesZiel", "hineinrückenOhneBase"]
)


def nichtAuswählen(aufstellung, einheit, modell):
    """Die Einheit bleibt, wie sie ist: nicht ausgewählt."""


mitUndOhneEbene = pytest.mark.parametrize(
    "ebeneLegen",
    [nichtAuswählen, ebeneAufDasModellLegen],
    ids=["nichtAusgewählt", "ebeneIstEinModell"],
)


@zügeFürDieAbfrage
@mitUndOhneEbene
def testAuf26_5DieAbfrageNenntNurDasAlleinGezogeneModellUndSetztNichts(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, zug, ebeneLegen
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    modell, modellImWeg = einheit.modelle
    davor, stelleDesLoslassens, stelleImWeg, _ = stellenDesZugs(
        aufstellung, radiusInZoll(modell), zug
    )
    modelleAnStellenSetzen(aufstellung, einheit, [davor, stelleImWeg])
    ebeneLegen(aufstellung, einheit, modell)

    abfrage = aufstellung.stellenBeimLoslassen(modell, stelleDesLoslassens)

    assert set(abfrage) == {modell}
    assert aufstellung.stelle(modell) == davor
    assert aufstellung.stelle(modellImWeg) == stelleImWeg


@zügeFürDieAbfrage
@mitUndOhneEbene
def testAuf26_5BeimLoslassenStehtDasModellDortWoDieAbfrageEsZeigte(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, zug, ebeneLegen
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    modell, _ = einheit.modelle
    davor, stelleDesLoslassens, stelleImWeg, _ = stellenDesZugs(
        aufstellung, radiusInZoll(modell), zug
    )
    modelleAnStellenSetzen(aufstellung, einheit, [davor, stelleImWeg])
    ebeneLegen(aufstellung, einheit, modell)
    gezeigt = aufstellung.stellenBeimLoslassen(modell, stelleDesLoslassens)

    aufstellung.modellLoslassen(modell, stelleDesLoslassens)

    assert aufstellung.stelle(modell) == gezeigt[modell]


@zügeFürDieAbfrage
def testAuf26_5DerDienstNenntDieStelleBeimLoslassenNurDesGezogenenModells(
    dienst, aufstellungNachDerZonenwahl, boyz, zug
):
    aufstellung = aufstellungNachDerZonenwahl
    modell, *_ = boyz.modelle
    davor, stelleDesLoslassens, stelleImWeg, _ = stellenDesZugs(
        aufstellung, radiusInZoll(modell), zug
    )
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleImWeg])
    erwartet = aufstellung.stellenBeimLoslassen(modell, stelleDesLoslassens)
    spielstandDavor = spielstandVon(dienst)

    antwort = stelleBeimLoslassenAbfragen(dienst, aufstellung, boyz, modell, stelleDesLoslassens)

    abgefragt = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert len(abgefragt["modelle"]) == 1
    assert stellenDerEinheitIm(abgefragt, "Boyz") == stellenDerAbfrage(boyz, erwartet)
    assert spielstandVon(dienst) == spielstandDavor


@mitMausUndFinger
def testAuf26_5DieKarteZeigtBeimHaltenDasModellDortWoEsBeimLoslassenStehtNichtUnterDemZeiger(
    bildschirm, aufstellungNachDerZonenwahl, boyz, eingabe
):
    aufstellung = aufstellungNachDerZonenwahl
    modell, *_ = boyz.modelle
    davor, stelleDesLoslassens, stelleImWeg, _ = stellenDesZugs(
        aufstellung, radiusInZoll(modell), hineinrückenOhneBase
    )
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleImWeg])
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)

    gezeigt = haltenUndLosslassen(seite, davor, stelleDesLoslassens, eingabe)

    assert gezeigt == stellenAlsZahlen(aufstellung)
    assert not liegtEinPixelGenauAn(seite, aufstellung.stelle(modell), stelleDesLoslassens)
