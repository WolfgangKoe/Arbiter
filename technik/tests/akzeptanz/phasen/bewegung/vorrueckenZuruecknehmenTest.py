"""BEW-12 · Vorrücken zurücknehmen."""

from http import HTTPStatus

from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import knopfDerSeite, seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import (
    spielstandVon,
    stelleImSpielstand,
    stellenDerEinheitIm,
    vorrückenZurücknehmen,
)
from tests.akzeptanz.grenzen import (
    ganzeEinheitAuswählen,
    mitJedemWurf,
    vorgerücktMit,
    wartetAufDenVorrückwurf,
    zweiZollEntlangDerReihe,
)
from tests.akzeptanz.schlacht import jetzigeStellen, mitteDesSpielfelds

vorrückenKnopf = "Vorrücken"
zurücknehmenKnopf = "Vorrücken zurücknehmen"
dreiAugen = 3


def testBew12_1WartetDieEinheitAufIhrenVorrückwurfBietetArbiterZurücknehmenAn(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    wartetAufDenVorrückwurf(schlacht, einheit, "ganzeEinheit")

    assert schlacht.vorrückenZurücknehmenAngeboten


@mitJedemWurf
def testBew12_1IstDieEinheitVorgerücktBietetArbiterZurücknehmenAn(einheitAmZug, wurf):
    schlacht, einheit, _, _ = einheitAmZug
    vorgerücktMit(schlacht, einheit, wurf)

    assert schlacht.vorrückenZurücknehmenAngeboten


def testBew12_1ZuEinerEinheitDieWederWartetNochVorgerücktIstBietetArbiterZurücknehmenNichtAn(
    einheitAmZug,
):
    schlacht, einheit, _, _ = einheitAmZug
    ganzeEinheitAuswählen(schlacht, einheit)

    assert not schlacht.vorrückenZurücknehmenAngeboten


def testBew12_1IstEineAndereEinheitAusgewähltBietetArbiterZurücknehmenNichtAn(einheitAmZug):
    schlacht, einheit, andereEinheit, _ = einheitAmZug
    vorgerücktMit(schlacht, einheit, dreiAugen)
    schlacht.auswählen(andereEinheit)

    assert not schlacht.vorrückenZurücknehmenAngeboten


def testBew12_1OhneAuswahlBietetArbiterZurücknehmenNichtAn(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    vorgerücktMit(schlacht, einheit, dreiAugen)
    schlacht.karteAnklicken(mitteDesSpielfelds)

    assert not schlacht.vorrückenZurücknehmenAngeboten


def testBew12_1DerDienstNenntZurücknehmenZurVorgerücktenEinheit(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    vorgerücktMit(schlachtInDerBewegungsphase, boyz, dreiAugen)

    spielstand = spielstandVon(dienstDerSchlacht)
    assert spielstand["schlacht"]["vorrücken"] == {"angeboten": False, "zurücknehmen": True}


def testBew12_1DieSeiteZeigtZurVorgerücktenEinheitDenKnopfZurücknehmen(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    vorgerücktMit(schlachtInDerBewegungsphase, boyz, dreiAugen)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    expect(knopfDerSeite(seite, zurücknehmenKnopf)).to_have_count(1)


def testBew12_1DieSeiteZeigtOhneVorrückenKeinenKnopfZurücknehmen(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)

    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    expect(knopfDerSeite(seite, vorrückenKnopf)).to_have_count(1)
    expect(knopfDerSeite(seite, zurücknehmenKnopf)).to_have_count(0)


def testBew12_2NachDemZurücknehmenWartetDieEinheitAufKeinenVorrückwurfMehr(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = wartetAufDenVorrückwurf(schlacht, einheit, "ganzeEinheit")

    schlacht.vorrückenZurücknehmen()

    assert not schlacht.wartetAufVorrückwurf(einheit)
    assert not schlacht.vorgerückt(einheit)
    assert jetzigeStellen(schlacht, einheit) == stellen


@mitJedemWurf
def testBew12_2NachDemZurücknehmenIstDieEinheitNichtMehrVorgerückt(einheitAmZug, wurf):
    schlacht, einheit, _, _ = einheitAmZug
    vorgerücktMit(schlacht, einheit, wurf)

    schlacht.vorrückenZurücknehmen()

    assert not schlacht.vorgerückt(einheit)
    assert not schlacht.wartetAufVorrückwurf(einheit)
    assert schlacht.vorrückwurf(einheit) is None


def testBew12_2NachDemZurücknehmenStehtJedesModellWoEsZuBeginnDerBewegungsphaseStand(
    einheitAmZug,
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = vorgerücktMit(schlacht, einheit, dreiAugen)
    erstes, *_ = einheit.modelle
    schlacht.modellLoslassen(erstes, zweiZollEntlangDerReihe(stellen[erstes]))
    assert jetzigeStellen(schlacht, einheit) != stellen

    schlacht.vorrückenZurücknehmen()

    assert jetzigeStellen(schlacht, einheit) == stellen


def testBew12_2OhneAngebotBleibtJedesModellWoEsHingezogenWurde(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = ganzeEinheitAuswählen(schlacht, einheit)
    erstes, *_ = einheit.modelle
    schlacht.modellLoslassen(erstes, zweiZollEntlangDerReihe(stellen[erstes]))
    gezogen = jetzigeStellen(schlacht, einheit)

    schlacht.vorrückenZurücknehmen()

    assert jetzigeStellen(schlacht, einheit) == gezogen


def testBew12_2DerDienstNenntNachDemZurücknehmenDieStellenZuBeginnDerBewegungsphase(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    stellen = vorgerücktMit(schlachtInDerBewegungsphase, boyz, dreiAugen)
    erstes, *_ = boyz.modelle
    schlachtInDerBewegungsphase.modellLoslassen(erstes, zweiZollEntlangDerReihe(stellen[erstes]))

    antwort = vorrückenZurücknehmen(dienstDerSchlacht)

    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(antwort.get_json(), "Boyz") == {
        nummer: stelleImSpielstand(stellen[modell])
        for nummer, modell in enumerate(boyz.modelle, start=1)
    }
    assert not schlachtInDerBewegungsphase.vorgerückt(boyz)


def testBew12_2AmBildschirmNimmtDerKnopfDieGrenzeDesWurfsZurück(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    vorgerücktMit(schlachtInDerBewegungsphase, boyz, dreiAugen)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    expect(seite.locator(".karte g.grenze.spieler1")).to_have_count(2)

    knopfDerSeite(seite, zurücknehmenKnopf).click()

    expect(seite.locator(".karte g.grenze.spieler1")).to_have_count(1)
    expect(knopfDerSeite(seite, zurücknehmenKnopf)).to_have_count(0)
    assert not schlachtInDerBewegungsphase.vorgerückt(boyz)
