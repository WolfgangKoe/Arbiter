"""AUF-21 · Einheit verschieben."""

from fractions import Fraction
from http import HTTPStatus

import pytest

from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.bildschirm import seiteMitEingabe
from tests.akzeptanz.dienst import (
    auswählen,
    modellLoslassen,
    stelleImSpielstand,
    stellenDerEinheitIm,
)
from tests.akzeptanz.handgriffe import (
    erwarteteStelle,
    gezogenesUndRest,
    millionstel,
    modelleSetzen,
    radiusInZoll,
    stelleInDerZoneDesSpielersAnDerReihe,
    tiefeDerZone,
    versetzt,
    wegVon,
    welchesGezogenWird,
)
from tests.akzeptanz.ziehen import liegtEinPixelGenauAn, mitMausUndFinger, modellZiehen

hineinrücken = pytest.mark.parametrize(
    ("ziel", "erwartet"),
    [
        ((12, 20), ((9, -1), (20, 0))),
        ((-3, 20), ((0, 1), (20, 0))),
        ((4, -5), ((4, 0), (0, 1))),
        ((4, 60), ((4, 0), (60, -3))),
        ((12, -5), ((9, -1), (0, 1))),
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


def endstellen(aufstellung, radius: Fraction, erwartet) -> tuple[Stelle, Stelle]:
    """Die Stellen der zwei Modelle in einer Reihe entlang y, das erste an `erwartet`."""
    erstes = erwarteteStelle(aufstellung, radius, erwartet)
    return erstes, Stelle(x=erstes.x, y=erstes.y + 2 * radius)


@welchesGezogenWird
def testAuf21_1ZiehenEinesModellsVerschiebtAlleGesetztenModelleUmSeinenWeg(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, zweitesGezogen
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    gesetzte = modelleSetzen(aufstellung, einheit, 2)
    (erstes, stelleErstes), (zweites, stelleZweites) = gesetzte
    (gezogenes, davor), _ = gezogenesUndRest(gesetzte, zweitesGezogen=zweitesGezogen)
    aufstellung.auswählen(einheit)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 4, 20)
    weg = wegVon(davor, ziel)

    aufstellung.modellLoslassen(gezogenes, ziel)

    assert aufstellung.stelle(erstes) == versetzt(stelleErstes, weg)
    assert aufstellung.stelle(zweites) == versetzt(stelleZweites, weg)


def testAuf21_1UngesetzteModelleDerEinheitBleibenUngesetzt(aufstellungNachDerZonenwahl, boyz):
    aufstellung = aufstellungNachDerZonenwahl
    [(erstes, _), _] = modelleSetzen(aufstellung, boyz, 2)
    *_, ungesetztes = boyz.modelle
    aufstellung.auswählen(boyz)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 4, 20)

    aufstellung.modellLoslassen(erstes, ziel)

    assert aufstellung.stelle(erstes) == ziel
    assert not aufstellung.gesetzt(ungesetztes)
    assert aufstellung.stelle(ungesetztes) is None


@welchesGezogenWird
def testAuf21_1DerDienstVerschiebtAlleGesetztenModelleUmDenWegDesGezogenen(
    dienst, aufstellungNachDerZonenwahl, boyz, zweitesGezogen
):
    aufstellung = aufstellungNachDerZonenwahl
    gesetzte = modelleSetzen(aufstellung, boyz, 3)
    erstesGesetztes, zweitesGesetztes, _ = gesetzte
    (gezogenes, davor), _ = gezogenesUndRest(
        [erstesGesetztes, zweitesGesetztes], zweitesGezogen=zweitesGezogen
    )
    auswählen(dienst, "Boyz")
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 4, 20)
    weg = wegVon(davor, ziel)

    antwort = modellLoslassen(dienst, aufstellung, boyz, gezogenes, ziel)

    erwartet = {
        nummer: stelleImSpielstand(versetzt(stelle, weg))
        for nummer, (_, stelle) in enumerate(gesetzte, start=1)
    }
    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(antwort.get_json(), "Boyz") == erwartet


@mitMausUndFinger
def testAuf21_1DieSeiteVerschiebtBeimZiehenEinesModellsDieGanzeEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyz, eingabe
):
    aufstellung = aufstellungNachDerZonenwahl
    gesetzte = modelleSetzen(aufstellung, boyz, 3)
    [(erstes, davor), *_] = gesetzte
    aufstellung.auswählen(boyz)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 4, 20)
    weg = wegVon(davor, ziel)
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)

    modellZiehen(seite, davor, ziel, eingabe)

    for modell, stelleDavor in gesetzte:
        assert aufstellung.gesetzt(modell)
        assert liegtEinPixelGenauAn(seite, aufstellung.stelle(modell), versetzt(stelleDavor, weg))
    assert liegtEinPixelGenauAn(seite, aufstellung.stelle(erstes), ziel)


@hineinrücken
@welchesGezogenWird
def testAuf21_2RagtDerBlockAusDerZoneRücktAlleGemeinsamAufKürzestemWegHinein(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, ziel, erwartet, zweitesGezogen
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    gesetzte = modelleSetzen(aufstellung, einheit, 2)
    (erstes, _), (zweites, _) = gesetzte
    (gezogenes, _), _ = gezogenesUndRest(gesetzte, zweitesGezogen=zweitesGezogen)
    aufstellung.auswählen(einheit)
    radius = radiusInZoll(erstes)
    zielTiefe, zielLänge = ziel
    versatzDesGezogenenImBlock = 2 * radius if zweitesGezogen else 0
    stelleDesLoslassens = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, zielTiefe, zielLänge + versatzDesGezogenenImBlock
    )

    aufstellung.modellLoslassen(gezogenes, stelleDesLoslassens)

    stelleErstes, stelleZweites = endstellen(aufstellung, radius, erwartet)
    assert aufstellung.stelle(erstes) == stelleErstes
    assert aufstellung.stelle(zweites) == stelleZweites


@hineinrücken
def testAuf21_2DerDienstRücktDenBlockAufKürzestemWegHinein(
    dienst, aufstellungNachDerZonenwahl, boyz, ziel, erwartet
):
    aufstellung = aufstellungNachDerZonenwahl
    [(erstes, _), _] = modelleSetzen(aufstellung, boyz, 2)
    auswählen(dienst, "Boyz")
    radius = radiusInZoll(erstes)
    zielTiefe, zielLänge = ziel
    stelleDesLoslassens = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, zielTiefe, zielLänge)

    antwort = modellLoslassen(dienst, aufstellung, boyz, erstes, stelleDesLoslassens)

    stelleErstes, stelleZweites = endstellen(aufstellung, radius, erwartet)
    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(antwort.get_json(), "Boyz") == {
        1: stelleImSpielstand(stelleErstes),
        2: stelleImSpielstand(stelleZweites),
    }


@mitMausUndFinger
def testAuf21_2DieSeiteRücktDenBlockBeimLoslassenInnerhalbDerKarteInDieZoneHinein(
    bildschirm, aufstellungNachDerZonenwahl, boyz, eingabe
):
    aufstellung = aufstellungNachDerZonenwahl
    [(erstes, davor), (zweites, _)] = modelleSetzen(aufstellung, boyz, 2)
    aufstellung.auswählen(boyz)
    radius = radiusInZoll(erstes)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 12, 20)
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)

    modellZiehen(seite, davor, ziel, eingabe)

    stelleErstes, stelleZweites = endstellen(aufstellung, radius, ((9, -1), (20, 0)))
    assert aufstellung.gesetzt(erstes)
    assert aufstellung.gesetzt(zweites)
    assert liegtEinPixelGenauAn(seite, aufstellung.stelle(erstes), stelleErstes)
    assert liegtEinPixelGenauAn(seite, aufstellung.stelle(zweites), stelleZweites)


def testAuf21_2BerührtDieBaseDieGrenzeDerZoneBleibtDerBlockStehen(
    aufstellung, ersteEinheitDesSpielersAnDerReihe
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    [(erstes, _), (zweites, _)] = modelleSetzen(aufstellung, einheit, 2)
    aufstellung.auswählen(einheit)
    radius = radiusInZoll(erstes)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefeDerZone - radius, 20)
    nachbar = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, tiefeDerZone - radius, 20 + 2 * radius
    )

    aufstellung.modellLoslassen(erstes, ziel)

    assert aufstellung.stelle(erstes) == ziel
    assert aufstellung.stelle(zweites) == nachbar


def testAuf21_2EinMillionstelZollÜberDerGrenzeRücktDenBlockHinein(
    aufstellung, ersteEinheitDesSpielersAnDerReihe
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    [(erstes, _), (zweites, _)] = modelleSetzen(aufstellung, einheit, 2)
    aufstellung.auswählen(einheit)
    radius = radiusInZoll(erstes)
    grenze = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefeDerZone - radius, 20)
    nachbar = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, tiefeDerZone - radius, 20 + 2 * radius
    )
    knappDrüber = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, tiefeDerZone - radius + millionstel, 20
    )

    aufstellung.modellLoslassen(erstes, knappDrüber)

    assert aufstellung.stelle(erstes) == grenze
    assert aufstellung.stelle(zweites) == nachbar
