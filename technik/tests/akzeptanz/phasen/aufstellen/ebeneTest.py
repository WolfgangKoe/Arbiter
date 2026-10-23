"""AUF-20 · Ganze Einheit oder ein Modell."""

from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.auswahl import (
    ausgewählteEinheiten,
    ausgewählteModelle,
    auswählenMit,
)
from tests.akzeptanz.bildschirm import aufDieHandlungWarten, seiteMitEingabe
from tests.akzeptanz.dienst import (
    ausgewählteEinheitenIm,
    ausgewählteModelleIm,
    auswählen,
    ebenenIm,
    karteAnklicken,
    modellAlsEbene,
    modellLoslassen,
    spielstandVon,
    stelleImSpielstand,
    stellenDerEinheitIm,
)
from tests.akzeptanz.handgriffe import stelleInDerZoneVon
from tests.akzeptanz.ziehen import (
    klickenMit,
    liegtEinPixelGenauAn,
    mitMausUndFinger,
    modellZiehen,
    punktAufDerKarte,
)

mitteDerZone = 4
längsDerZone = 30
nummerDesGezogenen = 1


def nichtAuswählen(aufstellung, einheit, modell):
    """Die Einheit bleibt, wie sie ist: nicht ausgewählt."""


def ebeneAufDasModellLegen(aufstellung, einheit, modell):
    aufstellung.auswählen(einheit)
    aufstellung.ebeneWählen(modell)


@pytest.fixture(
    params=[nichtAuswählen, ebeneAufDasModellLegen], ids=["nichtAusgewählt", "ebeneIstEinModell"]
)
def dreiBoyzNachDerVorgeschichte(request, aufstellungNachDerZonenwahl, boyz, boyzSetzen):
    """Drei gesetzte Boyz; die Vorgeschichte betrifft das erste, gezogene Modell."""
    gesetzte = boyzSetzen(3)
    [(gezogenes, _), *_] = gesetzte
    request.param(aufstellungNachDerZonenwahl, boyz, gezogenes)
    return gesetzte


def testAuf20_2DieEbeneEinerAusgewähltenEinheitIstDieGanzeEinheit(
    aufstellungNachDerZonenwahl, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)

    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyz)


def testAuf20_2WiederAusgewähltIstDieEbeneDieGanzeEinheitAuchNachEinemModell(
    aufstellungNachDerZonenwahl, boyzSetzen, boyz, warboss
):
    [(modell, _), *_] = boyzSetzen(3)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    aufstellungNachDerZonenwahl.ebeneWählen(modell)
    aufstellungNachDerZonenwahl.auswählen(warboss)

    aufstellungNachDerZonenwahl.auswählen(boyz)

    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyz)


def testAuf20_2DerDienstKennzeichnetNachDemWiederAuswählenKeinModellAlsEbene(
    dienst, aufstellungNachDerZonenwahl, boyzSetzen, boyz
):
    [(modell, _), *_] = boyzSetzen(3)
    auswählen(dienst, "Boyz")
    mitEbene = modellAlsEbene(dienst, aufstellungNachDerZonenwahl, boyz, modell)
    auswählen(dienst, "Warboss")

    antwort = auswählen(dienst, "Boyz")

    assert len(ebenenIm(mitEbene.get_json())) == 1
    assert ausgewählteEinheitenIm(antwort.get_json()) == {"Boyz"}
    assert ebenenIm(antwort.get_json()) == frozenset()


@mitMausUndFinger
def testAuf20_2DieSeiteKennzeichnetNachDemAuswählenAlleGesetztenModelleDerEinheit(
    bildschirm, aufstellungNachDerZonenwahl, boyzSetzen, boyz, eingabe
):
    gesetzte = boyzSetzen(3)
    [(modell, _), *_] = gesetzte
    ebeneAufDasModellLegen(aufstellungNachDerZonenwahl, boyz, modell)
    aufstellungNachDerZonenwahl.abwählen(boyz)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    auswählenMit[eingabe](seite, "Spieler 1", "Boyz")

    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(len(gesetzte))
    assert ausgewählteModelle(seite) == frozenset(
        stelleImSpielstand(stelle) for _, stelle in gesetzte
    )


def testAuf20_4ZiehenEinesModellsOhneEbeneEinheitLässtDieAnderenModelleStehen(
    aufstellungNachDerZonenwahl, spielerEins, dreiBoyzNachDerVorgeschichte
):
    [(gezogenes, stelleDavor), (zweites, stelleZweites), (drittes, stelleDrittes)] = (
        dreiBoyzNachDerVorgeschichte
    )
    ziel = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 20)

    aufstellungNachDerZonenwahl.modellLoslassen(gezogenes, ziel)

    assert ziel != stelleDavor
    assert aufstellungNachDerZonenwahl.stelle(gezogenes) == ziel
    assert aufstellungNachDerZonenwahl.stelle(zweites) == stelleZweites
    assert aufstellungNachDerZonenwahl.stelle(drittes) == stelleDrittes


def testAuf20_4ZiehenEinesAnderenModellsAlsDerEbeneLässtAuchDieEbeneStehen(
    aufstellungNachDerZonenwahl, spielerEins, boyz, boyzSetzen
):
    [(modellDerEbene, stelleDerEbene), (gezogenes, _), (drittes, stelleDrittes)] = boyzSetzen(3)
    ebeneAufDasModellLegen(aufstellungNachDerZonenwahl, boyz, modellDerEbene)
    ziel = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 20)

    aufstellungNachDerZonenwahl.modellLoslassen(gezogenes, ziel)

    assert aufstellungNachDerZonenwahl.stelle(gezogenes) == ziel
    assert aufstellungNachDerZonenwahl.stelle(modellDerEbene) == stelleDerEbene
    assert aufstellungNachDerZonenwahl.stelle(drittes) == stelleDrittes


def testAuf20_4DerDienstVerschiebtNurDasGezogeneModell(
    dienst, aufstellungNachDerZonenwahl, boyz, dreiBoyzNachDerVorgeschichte
):
    [(gezogenes, _), *_] = dreiBoyzNachDerVorgeschichte
    davor = stellenDerEinheitIm(spielstandVon(dienst), "Boyz")
    spieler = aufstellungNachDerZonenwahl.anDerReihe
    ziel = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spieler, 4, 20)

    antwort = modellLoslassen(dienst, aufstellungNachDerZonenwahl, boyz, gezogenes, ziel)

    danach = stellenDerEinheitIm(antwort.get_json(), "Boyz")
    übrigeDavor = {
        nummer: stelle for nummer, stelle in davor.items() if nummer != nummerDesGezogenen
    }
    übrigeDanach = {
        nummer: stelle for nummer, stelle in danach.items() if nummer != nummerDesGezogenen
    }
    assert antwort.status_code == HTTPStatus.OK
    assert danach[nummerDesGezogenen] != davor[nummerDesGezogenen]
    assert danach[nummerDesGezogenen] == stelleImSpielstand(ziel)
    assert übrigeDanach == übrigeDavor


@mitMausUndFinger
def testAuf20_4DieSeiteZiehtNurDasGezogeneModell(
    bildschirm, aufstellungNachDerZonenwahl, dreiBoyzNachDerVorgeschichte, eingabe
):
    [(gezogenes, stelleDavor), (zweites, stelleZweites), (drittes, stelleDrittes)] = (
        dreiBoyzNachDerVorgeschichte
    )
    spieler = aufstellungNachDerZonenwahl.anDerReihe
    ziel = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spieler, 4, 20)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    modellZiehen(seite, stelleDavor, ziel, eingabe)

    assert liegtEinPixelGenauAn(seite, aufstellungNachDerZonenwahl.stelle(gezogenes), ziel)
    assert aufstellungNachDerZonenwahl.stelle(zweites) == stelleZweites
    assert aufstellungNachDerZonenwahl.stelle(drittes) == stelleDrittes


def testAuf20_5NachDemSetzenDerFormationBleibtDieEinheitAusgewähltMitIhrerEbene(
    aufstellungNachDerZonenwahl, spielerEins, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, längsDerZone)

    aufstellungNachDerZonenwahl.karteAnklicken(klick)

    assert aufstellungNachDerZonenwahl.ausgewählt(boyz)
    assert aufstellungNachDerZonenwahl.ganzeEinheitIstEbene(boyz)
    assert all(aufstellungNachDerZonenwahl.modellAusgewählt(modell) for modell in boyz.modelle)


def testAuf20_5DerDienstLässtNachDemSetzenDieEinheitAusgewähltOhneModellAlsEbene(
    dienst, aufstellungNachDerZonenwahl, spielerEins, boyz
):
    auswählen(dienst, "Boyz")
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, längsDerZone)

    antwort = karteAnklicken(dienst, klick)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteEinheitenIm(spielstand) == {"Boyz"}
    assert len(ausgewählteModelleIm(spielstand)) == len(boyz.modelle)
    assert ebenenIm(spielstand) == frozenset()


@mitMausUndFinger
def testAuf20_5DieSeiteZeigtNachDemSetzenDieEinheitUndAlleIhreModelleAusgewählt(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins, boyz, eingabe
):
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)
    auswählenMit[eingabe](seite, "Spieler 1", "Boyz")
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, längsDerZone)

    with aufDieHandlungWarten(seite):
        klickenMit[eingabe](seite, punktAufDerKarte(seite, klick))

    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(len(boyz.modelle))
    assert ausgewählteEinheiten(seite) == {"Boyz"}
