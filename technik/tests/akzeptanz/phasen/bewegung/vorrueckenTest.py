"""BEW-5 · Vorrücken."""

from fractions import Fraction
from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from arbiter.domaene.querschnitt.schlachtrunden import Phase
from tests.akzeptanz.bildschirm import knopfDerSeite, seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import spielstandVon, vorrücken
from tests.akzeptanz.grenzen import (
    ebenen,
    ganzeEinheitAuswählen,
    mitJedemWurf,
    mitJederEbene,
    stelleImRing,
    vorgerücktMit,
    wartetAufDenVorrückwurf,
)
from tests.akzeptanz.handgriffe import versetzt
from tests.akzeptanz.schlacht import (
    hältAnDerBewegungsweite,
    jetzigeStellen,
    mitteDesSpielfelds,
    phaseBeendenBis,
    phasenAußerDerBewegungsphase,
    phasenAußerDerBewegungsphaseIds,
)
from tests.akzeptanz.ziehen import mitDerMausKlicken, punktAufDerKarte

vorrückenKnopf = "Vorrücken"
zweiZoll = Fraction(2)
einAuge = 1


def nachUnten(stelle, strecke: Fraction):
    return versetzt(stelle, (Fraction(0), strecke))


@mitJederEbene
def testBew5_1ZuEinerAusgewähltenEinheitDesSpielersAmZugBietetArbiterVorrückenAn(
    einheitAmZug, ebene
):
    schlacht, einheit, _, _ = einheitAmZug
    ebenen[ebene](schlacht, einheit)

    assert schlacht.vorrückenAngeboten


def testBew5_1OhneAuswahlBietetArbiterVorrückenNichtAn(schlachtInDerBewegungsphase):
    assert not schlachtInDerBewegungsphase.vorrückenAngeboten


def testBew5_1ZurEinheitDesAnderenSpielersBietetArbiterVorrückenNichtAn(
    schlachtInDerBewegungsphase, necronWarriors
):
    schlachtInDerBewegungsphase.auswählen(necronWarriors)

    assert not schlachtInDerBewegungsphase.vorrückenAngeboten


@pytest.mark.parametrize("phase", phasenAußerDerBewegungsphase, ids=phasenAußerDerBewegungsphaseIds)
def testBew5_1AußerhalbDerBewegungsphaseBietetArbiterVorrückenNichtAn(
    schlachtInDerKommandophase, boyz, phase: Phase
):
    phaseBeendenBis(schlachtInDerKommandophase, phase)
    schlachtInDerKommandophase.auswählen(boyz)

    assert not schlachtInDerKommandophase.vorrückenAngeboten


def testBew5_1WartetDieEinheitAufIhrenVorrückwurfBietetArbiterVorrückenNichtAn(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    wartetAufDenVorrückwurf(schlacht, einheit, "ganzeEinheit")

    assert not schlacht.vorrückenAngeboten


def testBew5_1IstDieEinheitVorgerücktBietetArbiterVorrückenNichtAn(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    vorgerücktMit(schlacht, einheit, einAuge)

    assert not schlacht.vorrückenAngeboten


def testBew5_1DerDienstNenntVorrückenAngeboten(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)

    spielstand = spielstandVon(dienstDerSchlacht)
    assert spielstand["schlacht"]["vorrücken"] == {"angeboten": True, "zurücknehmen": False}


@pytest.mark.usefixtures("schlachtInDerBewegungsphase")
def testBew5_1DerDienstNenntOhneAuswahlVorrückenNichtAngeboten(dienstDerSchlacht):
    spielstand = spielstandVon(dienstDerSchlacht)

    assert spielstand["schlacht"]["vorrücken"] == {"angeboten": False, "zurücknehmen": False}


def testBew5_1DieSeiteZeigtZurAusgewähltenEinheitDenKnopfVorrücken(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    expect(knopfDerSeite(seite, vorrückenKnopf)).to_have_count(1)


def testBew5_1DieSeiteZeigtOhneAuswahlKeinenKnopfVorrücken(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    expect(knopfDerSeite(seite, vorrückenKnopf)).to_have_count(1)

    mitDerMausKlicken(seite, punktAufDerKarte(seite, mitteDesSpielfelds))

    expect(knopfDerSeite(seite, vorrückenKnopf)).to_have_count(0)


@mitJederEbene
def testBew5_2NachDemKlickAufVorrückenWartetDieEinheitAufIhrenVorrückwurf(einheitAmZug, ebene):
    schlacht, einheit, _, _ = einheitAmZug
    ebenen[ebene](schlacht, einheit)

    schlacht.vorrücken()

    assert schlacht.wartetAufVorrückwurf(einheit)
    assert not schlacht.vorgerückt(einheit)
    assert schlacht.vorrückwurf(einheit) is None


def testBew5_2OhneAngebotWartetNachVorrückenKeineEinheit(
    schlachtInDerBewegungsphase, necronWarriors
):
    schlachtInDerBewegungsphase.auswählen(necronWarriors)

    schlachtInDerBewegungsphase.vorrücken()

    assert not schlachtInDerBewegungsphase.wartetAufVorrückwurf(necronWarriors)
    assert not schlachtInDerBewegungsphase.vorgerückt(necronWarriors)


def testBew5_2DerDienstNenntNachVorrückenZurücknehmenStattVorrücken(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)

    antwort = vorrücken(dienstDerSchlacht)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json()["schlacht"]["vorrücken"] == {
        "angeboten": False,
        "zurücknehmen": True,
    }
    assert schlachtInDerBewegungsphase.wartetAufVorrückwurf(boyz)


def testBew5_2AmBildschirmZeigtDerKlickAufVorrückenDieSechsWählbarenGrenzen(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    knopfDerSeite(seite, vorrückenKnopf).click()

    expect(seite.locator(".karte g.grenze.spieler1.wählbar")).to_have_count(6)
    expect(knopfDerSeite(seite, vorrückenKnopf)).to_have_count(0)
    assert schlachtInDerBewegungsphase.wartetAufVorrückwurf(boyz)


@mitJederEbene
@mitJedemWurf
def testBew5_3DerKlickAufEinenDerSechsIstIhrVorrückwurfUndSieIstVorgerückt(
    einheitAmZug, ebene, wurf
):
    schlacht, einheit, _, _ = einheitAmZug
    wartetAufDenVorrückwurf(schlacht, einheit, ebene)

    schlacht.karteAnklicken(stelleImRing(schlacht, einheit, wurf))

    assert schlacht.vorrückwurf(einheit) == wurf
    assert schlacht.vorgerückt(einheit)
    assert not schlacht.wartetAufVorrückwurf(einheit)
    assert schlacht.ausgewählt(einheit)


@mitJedemWurf
def testBew5_3NachDemVorrückwurfZiehtEinModellBisBewegungsweitePlusWurfOhneAnzuhalten(
    einheitAmZug, wurf
):
    schlacht, einheit, _, _ = einheitAmZug
    vorgerücktMit(schlacht, einheit, wurf)
    erstes, *_ = einheit.modelle
    ziel = nachUnten(schlacht.stelle(erstes), erstes.bewegungsweite + wurf)

    schlacht.modellLoslassen(erstes, ziel)

    assert schlacht.stelle(erstes) == ziel


@mitJedemWurf
def testBew5_3NachDemVorrückwurfHältArbiterJedesModellAnBewegungsweitePlusWurfAn(
    einheitAmZug, wurf
):
    schlacht, einheit, _, _ = einheitAmZug
    vorgerücktMit(schlacht, einheit, wurf)
    davor = jetzigeStellen(schlacht, einheit)
    erstes, *_ = einheit.modelle
    ziel = nachUnten(davor[erstes], erstes.bewegungsweite + wurf + zweiZoll)

    schlacht.modellLoslassen(erstes, ziel)

    danach = jetzigeStellen(schlacht, einheit)
    nichtAngehalten = {
        modell
        for modell in einheit.modelle
        if not hältAnDerBewegungsweite(davor[modell], danach[modell], modell.bewegungsweite + wurf)
    }
    assert nichtAngehalten == set()
