"""BEW-14 · Vorrückwurf per Fläche."""

from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import (
    ausgewählteModelleIm,
    grenzenDerEinheitIm,
    grenzenImSpielstand,
    karteAnklicken,
)
from tests.akzeptanz.grenzen import (
    außerhalbDerSechsGrenzkreise,
    grenzenNachDemVorrückwurf,
    innerhalbDesGrenzkreisesOhneWurf,
    mitJedemWurf,
    stelleAufDemGrenzkreisDesWurfs,
    stelleNurImGrenzkreisDesWurfs,
    vierAugen,
)
from tests.akzeptanz.schlacht import stellenDerEinheitAlsZahlen
from tests.akzeptanz.vorruecken import mitJederEbene, wartetAufDenVorrückwurf
from tests.akzeptanz.ziehen import (
    aufDasAnklickenWarten,
    klickenMit,
    mitMausUndFinger,
    punktAufDerKarte,
)


@mitJederEbene
@mitJedemWurf
def testBew14_1EinKlickNurImGrenzkreisEinesWurfsIstDerKlickAufIhn(einheitAmZug, ebene, wurf):
    schlacht, einheit, _, _ = einheitAmZug
    wartetAufDenVorrückwurf(schlacht, einheit, ebene)

    schlacht.karteAnklicken(stelleNurImGrenzkreisDesWurfs(schlacht, einheit, wurf))

    assert schlacht.vorrückwurf(einheit) == wurf


@mitJederEbene
@mitJedemWurf
def testBew14_1EinKlickAufDenGrenzkreisEinesWurfsGiltAlsInnerhalbSeinerFläche(
    einheitAmZug, ebene, wurf
):
    schlacht, einheit, _, _ = einheitAmZug
    wartetAufDenVorrückwurf(schlacht, einheit, ebene)

    schlacht.karteAnklicken(stelleAufDemGrenzkreisDesWurfs(schlacht, einheit, wurf))

    assert schlacht.vorrückwurf(einheit) == wurf


@mitJederEbene
@pytest.mark.parametrize(
    "mehrAlsDieBewegung",
    [innerhalbDesGrenzkreisesOhneWurf, außerhalbDerSechsGrenzkreise],
    ids=["imGrenzkreisAusBew11", "außerhalbDesSechstenGrenzkreises"],
)
def testBew14_1EinKlickAnJederAnderenStelleHebtDieAuswahlAufStattZuWählen(
    einheitAmZug, ebene, mehrAlsDieBewegung
):
    schlacht, einheit, _, _ = einheitAmZug
    wartetAufDenVorrückwurf(schlacht, einheit, ebene)

    schlacht.karteAnklicken(stelleNurImGrenzkreisDesWurfs(schlacht, einheit, mehrAlsDieBewegung))

    assert not schlacht.ausgewählt(einheit)
    assert not schlacht.vorgerückt(einheit)
    assert schlacht.vorrückwurf(einheit) is None


def testBew14_1EinKlickAufEinModellImGrenzkreisEinesWurfsWähltKeinenWurf(
    schlachtInDerBewegungsphase, boyz
):
    wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "einModell")
    _, _, modellNurImGrenzkreisFürVier, *_ = boyz.modelle

    schlachtInDerBewegungsphase.modellAnklicken(modellNurImGrenzkreisFürVier)

    assert schlachtInDerBewegungsphase.vorrückwurf(boyz) is None
    assert not schlachtInDerBewegungsphase.vorgerückt(boyz)
    assert schlachtInDerBewegungsphase.wartetAufVorrückwurf(boyz)


def testBew14_1DerDienstNimmtDenKlickNurImGrenzkreisFürVierAlsWurfVier(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    stellen = wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "ganzeEinheit")
    stelle = stelleNurImGrenzkreisDesWurfs(schlachtInDerBewegungsphase, boyz, vierAugen)

    antwort = karteAnklicken(dienstDerSchlacht, stelle)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert grenzenDerEinheitIm(spielstand, "Boyz") == grenzenImSpielstand(
        grenzenNachDemVorrückwurf(stellen, vierAugen)
    )
    assert ausgewählteModelleIm(spielstand) == stellenDerEinheitAlsZahlen(
        schlachtInDerBewegungsphase, boyz
    )


def testBew14_1DerDienstHebtNachDemKlickInDenGrenzkreisAusBew11DieAuswahlAuf(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "ganzeEinheit")
    assert schlachtInDerBewegungsphase.ausgewählt(boyz)
    stelle = stelleNurImGrenzkreisDesWurfs(
        schlachtInDerBewegungsphase, boyz, innerhalbDesGrenzkreisesOhneWurf
    )

    antwort = karteAnklicken(dienstDerSchlacht, stelle)

    assert antwort.status_code == HTTPStatus.OK
    assert ausgewählteModelleIm(antwort.get_json()) == frozenset()


@mitMausUndFinger
def testBew14_1AmBildschirmWähltEinKlickNurImGrenzkreisFürVierDenWurfVier(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "ganzeEinheit")
    stelle = stelleNurImGrenzkreisDesWurfs(schlachtInDerBewegungsphase, boyz, vierAugen)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )
    expect(seite.locator(".karte g.grenze.spieler1.wählbar")).to_have_count(6)

    klickenMit[eingabe](seite, punktAufDerKarte(seite, stelle))

    expect(seite.locator(".karte g.grenze.spieler1.wählbar")).to_have_count(0)
    expect(seite.locator(".karte g.grenze.spieler1")).to_have_count(2)
    assert schlachtInDerBewegungsphase.vorrückwurf(boyz) == vierAugen


@mitMausUndFinger
def testBew14_1AmBildschirmWähltEinKlickAufEinModellImGrenzkreisEinesWurfsKeinenWurf(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "einModell")
    _, _, modellNurImGrenzkreisFürVier, *_ = boyz.modelle
    stelle = schlachtInDerBewegungsphase.stelle(modellNurImGrenzkreisFürVier)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )
    expect(seite.locator(".karte g.grenze.spieler1.wählbar")).to_have_count(6)

    with aufDasAnklickenWarten(seite):
        klickenMit[eingabe](seite, punktAufDerKarte(seite, stelle))

    expect(seite.locator(".karte g.grenze.spieler1.wählbar")).to_have_count(6)
    assert schlachtInDerBewegungsphase.vorrückwurf(boyz) is None
    assert schlachtInDerBewegungsphase.wartetAufVorrückwurf(boyz)
