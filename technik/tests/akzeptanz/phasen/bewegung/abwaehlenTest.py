"""BEW-9 · Abwählen in der Schlacht."""

from http import HTTPStatus

from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import ausgewählteEinheitenIm, ausgewählteModelleIm, karteAnklicken
from tests.akzeptanz.handgriffe import modellZurEbeneMachen
from tests.akzeptanz.schlacht import mitteDesSpielfelds
from tests.akzeptanz.ziehen import klickenMit, mitMausUndFinger, punktAufDerKarte


def testBew9_1EinKlickAufDieLeereKarteHebtDieAuswahlAuf(
    schlachtInDerBewegungsphase, einheitJederSeite
):
    schlachtInDerBewegungsphase.auswählen(einheitJederSeite)

    schlachtInDerBewegungsphase.karteAnklicken(mitteDesSpielfelds)

    assert not schlachtInDerBewegungsphase.ausgewählt(einheitJederSeite)


def testBew9_1EinKlickAufDieLeereKarteHebtAuchEineAuswahlMitEinemModellAlsEbeneAuf(
    schlachtInDerKommandophase, boyz
):
    angeklickt, *_ = boyz.modelle
    modellZurEbeneMachen(schlachtInDerKommandophase, boyz, angeklickt)
    assert schlachtInDerKommandophase.modellIstEbene(angeklickt)

    schlachtInDerKommandophase.karteAnklicken(mitteDesSpielfelds)

    assert not schlachtInDerKommandophase.ausgewählt(boyz)
    assert not schlachtInDerKommandophase.modellAusgewählt(angeklickt)


def testBew9_1DerDienstNenntNachDemKlickAufDieLeereKarteKeineAuswahl(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)

    antwort = karteAnklicken(dienstDerSchlacht, mitteDesSpielfelds)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteEinheitenIm(spielstand) == frozenset()
    assert ausgewählteModelleIm(spielstand) == frozenset()


@mitMausUndFinger
def testBew9_1DieSeiteKennzeichnetNachDemKlickAufDieLeereKarteNichtsAlsAusgewählt(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )
    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(len(boyz.modelle))

    klickenMit[eingabe](seite, punktAufDerKarte(seite, mitteDesSpielfelds))

    expect(seite.locator(".karte .modell.ausgewählt")).to_have_count(0)
    expect(seite.locator(".einheitenKarte.ausgewählt")).to_have_count(0)
