"""BEW-14 · Vorrückwurf per Fläche."""

from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import ausgewählteEinheitenIm, karteAnklicken
from tests.akzeptanz.grenzen import (
    alsZahlen,
    außerhalbDerSechsRinge,
    grenzenDerEinheitIm,
    grenzenNachDemVorrückwurf,
    innerhalbDesGrenzkreisesOhneWurf,
    mitJedemWurf,
    mitJederEbene,
    stelleAufDemKreis,
    stelleImRing,
    wartetAufDenVorrückwurf,
)
from tests.akzeptanz.ziehen import klickenMit, mitMausUndFinger, punktAufDerKarte

vierAugen = 4


@mitJederEbene
@mitJedemWurf
def testBew14_1EinKlickInDenRingEinesWurfsIstDerKlickAufSeinenGrenzkreis(einheitAmZug, ebene, wurf):
    schlacht, einheit, _, _ = einheitAmZug
    wartetAufDenVorrückwurf(schlacht, einheit, ebene)

    schlacht.karteAnklicken(stelleImRing(schlacht, einheit, wurf))

    assert schlacht.vorrückwurf(einheit) == wurf


@mitJederEbene
@mitJedemWurf
def testBew14_1EinKlickAufDenGrenzkreisEinesWurfsGiltAlsInnerhalbSeinerFläche(
    einheitAmZug, ebene, wurf
):
    schlacht, einheit, _, _ = einheitAmZug
    wartetAufDenVorrückwurf(schlacht, einheit, ebene)

    schlacht.karteAnklicken(stelleAufDemKreis(schlacht, einheit, wurf))

    assert schlacht.vorrückwurf(einheit) == wurf


@mitJederEbene
@pytest.mark.parametrize(
    "mehrAlsDieBewegung",
    [innerhalbDesGrenzkreisesOhneWurf, außerhalbDerSechsRinge],
    ids=["imGrenzkreisAusBew11", "außerhalbDesSechstenRings"],
)
def testBew14_1EinKlickAußerhalbDerRingeHebtDieAuswahlAufStattZuWählen(
    einheitAmZug, ebene, mehrAlsDieBewegung
):
    schlacht, einheit, _, _ = einheitAmZug
    wartetAufDenVorrückwurf(schlacht, einheit, ebene)

    schlacht.karteAnklicken(stelleImRing(schlacht, einheit, mehrAlsDieBewegung))

    assert not schlacht.ausgewählt(einheit)
    assert not schlacht.vorgerückt(einheit)
    assert schlacht.vorrückwurf(einheit) is None


def testBew14_1DerDienstNimmtDenKlickZwischenRingDreiUndVierAlsWurfVier(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    stellen = wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "ganzeEinheit")
    stelle = stelleImRing(schlachtInDerBewegungsphase, boyz, vierAugen)

    antwort = karteAnklicken(dienstDerSchlacht, stelle)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert grenzenDerEinheitIm(spielstand, "Boyz") == alsZahlen(
        grenzenNachDemVorrückwurf(stellen, vierAugen)
    )
    assert ausgewählteEinheitenIm(spielstand) == {"Boyz"}


def testBew14_1DerDienstHebtNachDemKlickInDenGrenzkreisAusBew11DieAuswahlAuf(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "ganzeEinheit")
    stelle = stelleImRing(schlachtInDerBewegungsphase, boyz, innerhalbDesGrenzkreisesOhneWurf)

    antwort = karteAnklicken(dienstDerSchlacht, stelle)

    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteEinheitenIm(antwort.get_json()) == frozenset()


@mitMausUndFinger
def testBew14_1AmBildschirmWähltEinKlickZwischenRingDreiUndVierDenWurfVier(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "ganzeEinheit")
    stelle = stelleImRing(schlachtInDerBewegungsphase, boyz, vierAugen)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )
    expect(seite.locator(".karte g.grenze.spieler1.wählbar")).to_have_count(6)

    klickenMit[eingabe](seite, punktAufDerKarte(seite, stelle))

    expect(seite.locator(".karte g.grenze.spieler1.wählbar")).to_have_count(0)
    expect(seite.locator(".karte g.grenze.spieler1")).to_have_count(2)
    assert schlachtInDerBewegungsphase.vorrückwurf(boyz) == vierAugen
