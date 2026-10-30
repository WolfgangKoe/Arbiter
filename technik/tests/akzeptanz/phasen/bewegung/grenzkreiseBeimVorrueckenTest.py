"""BEW-13 · Grenzkreise beim Vorrücken."""

from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import spielstandVon
from tests.akzeptanz.grenzen import (
    alsZahlen,
    grenzenDerEinheit,
    grenzenDerEinheitIm,
    grenzenNachDemVorrückwurf,
    grenzenVorDemVorrückwurf,
    mitJedemWurf,
    mitJederEbene,
    vorgerücktMit,
    wartetAufDenVorrückwurf,
    zweiZollEntlangDerReihe,
)

dreiAugen = 3
vierAugen = 4


@mitJederEbene
def testBew13_1WartetDieEinheitZeigtDieKarteSechsWeitereGrenzenUmEinBisSechsZollGrößer(
    einheitAmZug, ebene
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = wartetAufDenVorrückwurf(schlacht, einheit, ebene)

    assert grenzenDerEinheit(schlacht, einheit) == grenzenVorDemVorrückwurf(stellen)


def testBew13_1DerDienstNenntDieSechsWählbarenGrenzenMitWurfUndExaktenRadien(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    stellen = wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "ganzeEinheit")

    spielstand = spielstandVon(dienstDerSchlacht)
    assert grenzenDerEinheitIm(spielstand, "Boyz") == alsZahlen(grenzenVorDemVorrückwurf(stellen))


def testBew13_1DieSeiteZeigtSechsWählbareGrenzenUndDieAusBew11(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "ganzeEinheit")
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    expect(seite.locator(".karte g.grenze.spieler1.wählbar")).to_have_count(6)
    expect(seite.locator(".karte g.grenze.spieler1")).to_have_count(7)


@mitJederEbene
@mitJedemWurf
def testBew13_2IstDieEinheitVorgerücktZeigtDieKarteVonDenSechsNurDieIhresWurfs(
    einheitAmZug, ebene, wurf
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = vorgerücktMit(schlacht, einheit, wurf, ebene)

    assert grenzenDerEinheit(schlacht, einheit) == grenzenNachDemVorrückwurf(stellen, wurf)


def testBew13_2NachDemZiehenBleibtDieGrenzeDesWurfsAnDenStellenZuBeginnDerBewegungsphase(
    einheitAmZug,
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = vorgerücktMit(schlacht, einheit, dreiAugen)
    erstes, *_ = einheit.modelle
    schlacht.modellLoslassen(erstes, zweiZollEntlangDerReihe(stellen[erstes]))

    assert schlacht.stelle(erstes) != stellen[erstes]
    assert grenzenDerEinheit(schlacht, einheit) == grenzenNachDemVorrückwurf(stellen, dreiAugen)


def testBew13_2DerDienstNenntNurDieGrenzeDesWurfsNichtWählbar(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    stellen = vorgerücktMit(schlachtInDerBewegungsphase, boyz, vierAugen)

    spielstand = spielstandVon(dienstDerSchlacht)
    assert grenzenDerEinheitIm(spielstand, "Boyz") == alsZahlen(
        grenzenNachDemVorrückwurf(stellen, vierAugen)
    )


def testBew13_2DieSeiteZeigtKeineWählbareGrenzeMehr(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    vorgerücktMit(schlachtInDerBewegungsphase, boyz, vierAugen)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    expect(seite.locator(".karte g.grenze.spieler1")).to_have_count(2)
    expect(seite.locator(".karte g.grenze.spieler1.wählbar")).to_have_count(0)
