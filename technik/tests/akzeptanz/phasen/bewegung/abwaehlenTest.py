"""BEW-9 · Abwählen in der Schlacht."""

from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import ausgewählteModelleIm, spielfeldAnklicken
from tests.akzeptanz.grenzen import mitJedemWurf, stelleNurImGrenzkreisDesWurfs
from tests.akzeptanz.handgriffe import modellebeneWählen
from tests.akzeptanz.schlacht import mitteDesSpielfelds
from tests.akzeptanz.vorruecken import wartetAufDenVorrückwurf
from tests.akzeptanz.ziehen import klickenMit, mitMausUndFinger, punktAufDemSpielfeld


def testBew9_1EinKlickAufDasSpielfeldWoKeinModellStehtHebtDieAuswahlAuf(
    schlachtInDerBewegungsphase, einheitJederSeite
):
    schlachtInDerBewegungsphase.auswählen(einheitJederSeite)

    schlachtInDerBewegungsphase.spielfeldAnklicken(mitteDesSpielfelds)

    assert not schlachtInDerBewegungsphase.ausgewählt(einheitJederSeite)


def testBew9_1EinKlickAufDasSpielfeldWoKeinModellStehtHebtAuchEineAuswahlMitEinerModellebeneAuf(
    schlachtNachDerWahlDesErstenZugs, boyz
):
    angeklickt, *_ = boyz.modelle
    modellebeneWählen(schlachtNachDerWahlDesErstenZugs, boyz, angeklickt)
    assert schlachtNachDerWahlDesErstenZugs.istModellebene(angeklickt)

    schlachtNachDerWahlDesErstenZugs.spielfeldAnklicken(mitteDesSpielfelds)

    assert not schlachtNachDerWahlDesErstenZugs.ausgewählt(boyz)
    assert not schlachtNachDerWahlDesErstenZugs.modellAusgewählt(angeklickt)


def testBew9_1DerDienstNenntNachDemKlickAufDasSpielfeldWoKeinModellStehtKeineAuswahl(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)

    antwort = spielfeldAnklicken(dienstDerSchlacht, mitteDesSpielfelds)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteModelleIm(spielstand) == frozenset()


@mitMausUndFinger
def testBew9_1DieSeiteKennzeichnetNachDemKlickAufDasSpielfeldWoKeinModellStehtNichtsAlsAusgewählt(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )
    expect(seite.locator(".spielfeld .modell.ausgewählt")).to_have_count(len(boyz.modelle))

    klickenMit[eingabe](seite, punktAufDemSpielfeld(seite, mitteDesSpielfelds))

    expect(seite.locator(".spielfeld .modell.ausgewählt")).to_have_count(0)
    expect(seite.locator(".einheitenKarte.ausgewählt")).to_have_count(0)


@pytest.fixture
def abgewähltBeimWarten(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    wartetAufDenVorrückwurf(schlacht, einheit, "ganzeEinheit")
    schlacht.spielfeldAnklicken(mitteDesSpielfelds)
    assert not schlacht.ausgewählt(einheit), "Der Klick hob die Auswahl nicht auf"
    return schlacht, einheit


def testBew9_2NachDemAbwählenWartetDieEinheitWeiterAufIhrenVorrückwurf(abgewähltBeimWarten):
    schlacht, einheit = abgewähltBeimWarten

    assert schlacht.wartetAufVorrückwurf(einheit)
    assert not schlacht.vorgerückt(einheit)


@mitJedemWurf
def testBew9_2NachDemAbwählenBeendetDerKlickAufEinenDerSechsDasWarten(abgewähltBeimWarten, wurf):
    schlacht, einheit = abgewähltBeimWarten
    schlacht.auswählen(einheit)

    schlacht.spielfeldAnklicken(stelleNurImGrenzkreisDesWurfs(schlacht, einheit, wurf))

    assert schlacht.vorrückwurf(einheit) == wurf
    assert not schlacht.wartetAufVorrückwurf(einheit)


def testBew9_2NachDemAbwählenBeendetZurücknehmenDasWarten(abgewähltBeimWarten):
    schlacht, einheit = abgewähltBeimWarten
    schlacht.auswählen(einheit)

    schlacht.vorrückenZurücknehmen()

    assert not schlacht.wartetAufVorrückwurf(einheit)
    assert not schlacht.vorgerückt(einheit)
