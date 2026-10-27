"""QUE-9 · Erster Zug."""

from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from arbiter.domaene.querschnitt.schlachtrunden import Phase
from tests.akzeptanz.bildschirm import (
    amZugGekennzeichnet,
    armeelisteVon,
    knopfDerArmeeliste,
    kopfzeileVon,
    spielerAmZug,
)
from tests.akzeptanz.dienst import ersterZugWählen, spielstandVon

ersterZugKnopf = "Erster Zug"
spielernamen = pytest.mark.parametrize(
    "spielername",
    ["Spieler 1", "Spieler 2"],
    ids=["armeelisteVonSpielerEins", "armeelisteVonSpielerZwei"],
)


@pytest.fixture
def nameDesSpielersMitDemErstenZug(spielerMitDemErstenZug, spielerEins) -> str:
    return "Spieler 1" if spielerMitDemErstenZug is spielerEins else "Spieler 2"


def testQue9_1NachDerAufstellungHatKeinSpielerDenErstenZugUndKeinerIstAmZug(schlacht):
    assert schlacht.ersterZug is None
    assert schlacht.amZug is None


@spielernamen
def testQue9_1NachDerAufstellungZeigtJedeArmeelisteErsterZug(
    bildschirm, beendeteAufstellung, schlacht, spielername
):
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlacht)

    expect(knopfDerArmeeliste(seite, spielername, ersterZugKnopf)).to_have_count(1)


@spielernamen
def testQue9_1HatEinSpielerDenErstenZugZeigtKeineArmeelisteErsterZug(
    bildschirm, beendeteAufstellung, schlacht, spielerMitDemErstenZug, spielername
):
    schlacht.ersterZugWählen(spielerMitDemErstenZug)
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlacht)
    expect(spielerAmZug(seite)).to_have_count(1)

    expect(knopfDerArmeeliste(seite, spielername, ersterZugKnopf)).to_have_count(0)


@spielernamen
def testQue9_1VorDemEndeDerAufstellungZeigtKeineArmeelisteErsterZug(
    bildschirm, ausgangsaufstellung, spielername
):
    seite = bildschirm.seiteZu(ausgangsaufstellung)
    expect(armeelisteVon(seite, spielername)).to_have_count(1)

    expect(knopfDerArmeeliste(seite, spielername, ersterZugKnopf)).to_have_count(0)


def testQue9_1DerSpielstandNenntNachDerAufstellungKeinenErstenZugUndKeinenAmZug(
    dienstNachDerAufstellung,
):
    spielstand = spielstandVon(dienstNachDerAufstellung)

    assert spielstand["schlacht"]["ersterZug"] is None
    assert spielstand["schlacht"]["amZug"] is None


def testQue9_2DerSpielerMitDemErstenZugHatIhn(schlacht, spielerMitDemErstenZug):
    schlacht.ersterZugWählen(spielerMitDemErstenZug)

    assert schlacht.ersterZug is spielerMitDemErstenZug


def testQue9_2DerSpielerMitDemErstenZugIstAmZug(schlacht, spielerMitDemErstenZug):
    schlacht.ersterZugWählen(spielerMitDemErstenZug)

    assert schlacht.amZug is spielerMitDemErstenZug


def testQue9_2DieSchlachtrunde1Beginnt(schlacht, spielerMitDemErstenZug):
    schlacht.ersterZugWählen(spielerMitDemErstenZug)

    assert schlacht.schlachtrunde == 1


def testQue9_2DieErstePhaseIstDieKommandophase(schlacht, spielerMitDemErstenZug):
    schlacht.ersterZugWählen(spielerMitDemErstenZug)

    assert schlacht.phase is Phase.kommandophase


@pytest.mark.parametrize("spielernummer", [1, 2], ids=["spielerEins", "spielerZwei"])
def testQue9_2DerDienstSetztDenSpielerMitDemErstenZugAmZugInDieKommandophaseDerSchlachtrunde1(
    dienstNachDerAufstellung, spielernummer
):
    antwort = ersterZugWählen(dienstNachDerAufstellung, spielernummer)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json()["schlacht"] == {
        "ersterZug": spielernummer,
        "amZug": spielernummer,
        "schlachtrunde": 1,
        "phase": "Kommandophase",
        "beendet": False,
        "einheitInBewegung": None,
    }


def testQue9_2DieSeiteZeigtNachDemKlickAufErsterZugDenSpielerAmZugInDerKommandophase(
    bildschirm, beendeteAufstellung, schlacht, nameDesSpielersMitDemErstenZug
):
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlacht)

    knopfDerArmeeliste(seite, nameDesSpielersMitDemErstenZug, ersterZugKnopf).click()

    kopfzeile = kopfzeileVon(seite, nameDesSpielersMitDemErstenZug)
    expect(kopfzeile).to_have_class(amZugGekennzeichnet)
    expect(kopfzeile.locator(".kopfzeileAmZug")).to_have_text("Schlachtrunde 1 · Kommandophase")
