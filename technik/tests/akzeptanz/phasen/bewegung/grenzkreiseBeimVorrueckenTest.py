"""BEW-13 · Grenzkreise beim Vorrücken."""

from playwright.sync_api import expect

from tests.akzeptanz.bildschirm import kreiseDerGrenzenUndIhrerMasken, seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import grenzenDerEinheitIm, grenzenImSpielstand, spielstandVon
from tests.akzeptanz.grenzen import (
    dreiAugen,
    grenzenDerEinheit,
    grenzenNachDemVorrückwurf,
    grenzenVorDemVorrückwurf,
    mitJedemWurf,
    vierAugen,
    zweiZollEntlangDerReihe,
)
from tests.akzeptanz.vorruecken import mitJederEbene, vorgerücktMit, wartetAufDenVorrückwurf


@mitJederEbene
def testBew13_1WartetDieEinheitZeigtDasSpielfeldSechsWeitereEinhüllendeUmEinBisSechsZollGrößer(
    einheitAmZug, ebene
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = wartetAufDenVorrückwurf(schlacht, einheit, ebene)

    assert grenzenDerEinheit(schlacht, einheit) == grenzenVorDemVorrückwurf(stellen)


def testBew13_1DerDienstNenntDieSechsWählbarenEinhüllendenMitWurfUndExaktenRadien(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    stellen = wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "ganzeEinheit")

    spielstand = spielstandVon(dienstDerSchlacht)
    assert grenzenDerEinheitIm(spielstand, "Boyz") == grenzenImSpielstand(
        grenzenVorDemVorrückwurf(stellen)
    )


def testBew13_1DieSeiteZeigtSechsWählbareEinhüllendeUndDieAusBew11(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "ganzeEinheit")
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    expect(seite.locator(".spielfeld g.grenze.spieler1.wählbar")).to_have_count(6)
    expect(seite.locator(".spielfeld g.grenze.spieler1")).to_have_count(7)


def testBew13_1DieSeiteZeigtJedeDerSiebenEinhüllendenDurchIhreEigeneMaske(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    wartetAufDenVorrückwurf(schlachtInDerBewegungsphase, boyz, "ganzeEinheit")
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    expect(seite.locator(".spielfeld g.grenze.spieler1")).to_have_count(7)

    grenzen, masken = kreiseDerGrenzenUndIhrerMasken(seite)

    assert masken == grenzen


@mitJederEbene
@mitJedemWurf
def testBew13_2IstDieEinheitVorgerücktZeigtDasSpielfeldVonDenSechsNurDieIhresWurfs(
    einheitAmZug, ebene, wurf
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = vorgerücktMit(schlacht, einheit, wurf, ebene)

    assert grenzenDerEinheit(schlacht, einheit) == grenzenNachDemVorrückwurf(stellen, wurf)


def testBew13_2NachDemZiehenBleibtDieEinhüllendeDesWurfsAnDenStellenZuBeginnDerBewegungsphase(
    einheitAmZug,
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = vorgerücktMit(schlacht, einheit, dreiAugen)
    erstes, *_ = einheit.modelle
    schlacht.modellLoslassen(erstes, zweiZollEntlangDerReihe(stellen[erstes]))

    assert schlacht.stelle(erstes) != stellen[erstes]
    assert grenzenDerEinheit(schlacht, einheit) == grenzenNachDemVorrückwurf(stellen, dreiAugen)


def testBew13_2DerDienstNenntNurDieEinhüllendeDesWurfsNichtWählbar(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    stellen = vorgerücktMit(schlachtInDerBewegungsphase, boyz, vierAugen)

    spielstand = spielstandVon(dienstDerSchlacht)
    assert grenzenDerEinheitIm(spielstand, "Boyz") == grenzenImSpielstand(
        grenzenNachDemVorrückwurf(stellen, vierAugen)
    )


def testBew13_2DieSeiteZeigtKeineWählbareEinhüllendeMehr(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    vorgerücktMit(schlachtInDerBewegungsphase, boyz, vierAugen)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    expect(seite.locator(".spielfeld g.grenze.spieler1")).to_have_count(2)
    expect(seite.locator(".spielfeld g.grenze.spieler1.wählbar")).to_have_count(0)
