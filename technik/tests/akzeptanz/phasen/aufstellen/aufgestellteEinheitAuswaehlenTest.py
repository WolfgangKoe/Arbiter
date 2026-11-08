"""AUF-30 · Aufgestellte Einheit auswählen."""

from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.auswahl import ausgewählteModelle
from tests.akzeptanz.bildschirm import seiteMitEingabe
from tests.akzeptanz.dienst import (
    ausgewählteModelleIm,
    modellAnklicken,
    modellebenenIm,
    stelleImSpielstand,
)
from tests.akzeptanz.handgriffe import einheitenAufstellen, modelleSetzen, stellenAllerModelle
from tests.akzeptanz.ziehen import klickenMit, mitMausUndFinger, punktAufDemSpielfeld


@pytest.fixture
def aufstellungMitDemWarbossInAufstellung(aufstellungNachDerZonenwahl, warboss):
    einheitenAufstellen(aufstellungNachDerZonenwahl, 2)
    modelleSetzen(aufstellungNachDerZonenwahl, warboss, 1)
    return aufstellungNachDerZonenwahl


@pytest.fixture(params=["boyz", "necronWarriors"], ids=["eigeneEinheit", "einheitDesAnderen"])
def aufgestellteEinheit(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize(
    "warbossAusgewählt", [False, True], ids=["ohneAuswahl", "warbossAusgewählt"]
)
def testAuf30_1EinKlickWähltDieAufgestellteEinheitMitDerEinheitenebene(
    aufstellungMitDemWarbossInAufstellung, aufgestellteEinheit, warboss, warbossAusgewählt
):
    aufstellung = aufstellungMitDemWarbossInAufstellung
    if warbossAusgewählt:
        aufstellung.auswählen(warboss)
    angeklickt, *_ = aufgestellteEinheit.modelle

    aufstellung.modellAnklicken(angeklickt)

    assert aufstellung.ausgewählt(aufgestellteEinheit)
    assert aufstellung.hatEinheitenebene(aufgestellteEinheit)
    assert not aufstellung.ausgewählt(warboss)


def testAuf30_1EinKlickLässtSpielerAnDerReiheEinheitInAufstellungUndModelleGleich(
    aufstellungMitDemWarbossInAufstellung, aufgestellteEinheit, spielerEins, warboss
):
    aufstellung = aufstellungMitDemWarbossInAufstellung
    davor = stellenAllerModelle(aufstellung)
    angeklickt, *_ = aufgestellteEinheit.modelle

    aufstellung.modellAnklicken(angeklickt)

    assert aufstellung.anDerReihe is spielerEins
    assert aufstellung.einheitInAufstellung is warboss
    assert stellenAllerModelle(aufstellung) == davor


def testAuf30_1DerDienstWähltDieAufgestellteEinheitMitDerEinheitenebene(
    dienst, aufstellungMitDemWarbossInAufstellung, boyz
):
    aufstellung = aufstellungMitDemWarbossInAufstellung
    angeklickt, *_ = boyz.modelle

    antwort = modellAnklicken(dienst, aufstellung, boyz, angeklickt)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteModelleIm(spielstand) == {
        stelleImSpielstand(aufstellung.stelle(modell)) for modell in boyz.modelle
    }
    assert modellebenenIm(spielstand) == frozenset()


@mitMausUndFinger
def testAuf30_1DieSeiteKennzeichnetNachDemKlickDieAufgestellteEinheit(
    bildschirm, aufstellungMitDemWarbossInAufstellung, boyz, eingabe
):
    aufstellung = aufstellungMitDemWarbossInAufstellung
    angeklickt, *_ = boyz.modelle
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)

    klickenMit[eingabe](seite, punktAufDemSpielfeld(seite, aufstellung.stelle(angeklickt)))

    expect(seite.locator(".spielfeld .modell.ausgewählt")).to_have_count(len(boyz.modelle))
    assert ausgewählteModelle(seite) == {
        stelleImSpielstand(aufstellung.stelle(modell)) for modell in boyz.modelle
    }
