"""BEW-11 · Grenzkreise."""

import pytest
from playwright.sync_api import expect

from arbiter.domaene.querschnitt.schlachtrunden import Phase
from tests.akzeptanz.bildschirm import kreiseDerGrenzenUndIhrerMasken, seiteDerSchlachtMitEingabe
from tests.akzeptanz.dienst import grenzenDerEinheitIm, grenzenImSpielstand, spielstandVon
from tests.akzeptanz.grenzen import (
    grenzeDerBewegung,
    grenzeDerNahkampfreichweite,
    grenzenDerEinheit,
    grenzenDerEinheitenDes,
    zweiZollEntlangDerReihe,
)
from tests.akzeptanz.schlacht import (
    jetzigeStellen,
    mitteDesSpielfelds,
    phaseBeendenBis,
    phasenAußerDerBewegungsphase,
    phasenAußerDerBewegungsphaseIds,
)
from tests.akzeptanz.vorruecken import (
    ebenen,
    ganzeEinheitAuswählen,
    letztesModellZurEbeneMachen,
    mitJederEbene,
)
from tests.akzeptanz.ziehen import mitDerMausKlicken, punktAufDerKarte


def testBew11_1UmEinModellAlsEbeneZeigtDieKarteSeinenGrenzkreis(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = letztesModellZurEbeneMachen(schlacht, einheit)

    assert grenzenDerEinheit(schlacht, einheit) == {grenzeDerBewegung(stellen)}


def testBew11_1NachDemZiehenBleibtDerGrenzkreisAnDerStelleZuBeginnDerBewegungsphase(
    einheitAmZug,
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = letztesModellZurEbeneMachen(schlacht, einheit)
    ((modell, stelle),) = stellen.items()
    schlacht.modellLoslassen(modell, zweiZollEntlangDerReihe(stelle))

    assert schlacht.stelle(modell) != stelle
    assert grenzenDerEinheit(schlacht, einheit) == {grenzeDerBewegung(stellen)}


def testBew11_1DerDienstNenntDenGrenzkreisDesModellsMitExaktemRadius(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    stellen = letztesModellZurEbeneMachen(schlachtInDerBewegungsphase, boyz)

    spielstand = spielstandVon(dienstDerSchlacht)
    assert grenzenDerEinheitIm(spielstand, "Boyz") == grenzenImSpielstand(
        {grenzeDerBewegung(stellen)}
    )


def testBew11_5UmDieGanzeEinheitAlsEbeneZeigtDieKarteDieEinhüllendeIhrerGrenzkreise(
    einheitAmZug,
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = ganzeEinheitAuswählen(schlacht, einheit)

    assert grenzenDerEinheit(schlacht, einheit) == {grenzeDerBewegung(stellen)}


def testBew11_5NachDemZiehenBleibtDieEinhüllendeAnDenStellenZuBeginnDerBewegungsphase(
    einheitAmZug,
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = ganzeEinheitAuswählen(schlacht, einheit)
    erstes, *_ = einheit.modelle
    schlacht.modellLoslassen(erstes, zweiZollEntlangDerReihe(stellen[erstes]))

    assert jetzigeStellen(schlacht, einheit) != stellen
    assert grenzenDerEinheit(schlacht, einheit) == {grenzeDerBewegung(stellen)}


def testBew11_5DerDienstNenntDieEinhüllendeDerEinheitMitExaktenRadien(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    stellen = ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)

    spielstand = spielstandVon(dienstDerSchlacht)
    assert grenzenDerEinheitIm(spielstand, "Boyz") == grenzenImSpielstand(
        {grenzeDerBewegung(stellen)}
    )


def testBew11_5DieSeiteZeigtJedeEinhüllendeDurchIhreMaskeAusDenselbenGrenzkreisen(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, spielerZwei
):
    ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    expect(seite.locator(".karte g.grenze")).to_have_count(3)

    grenzen, masken = kreiseDerGrenzenUndIhrerMasken(seite)

    assert masken == grenzen
    assert sorted(map(len, grenzen)) == sorted(
        len(einheit.modelle) for einheit in (boyz, *spielerZwei.armee.einheiten)
    )


@mitJederEbene
def testBew11_3UmJedeEinheitDesAnderenSpielersZeigtDieKarteIhreNahkampfreichweite(
    einheitAmZug, ebene
):
    schlacht, einheit, _, andererSpieler = einheitAmZug
    ebenen[ebene](schlacht, einheit)

    assert grenzenDerEinheitenDes(schlacht, andererSpieler) == {
        andere: {grenzeDerNahkampfreichweite(jetzigeStellen(schlacht, andere))}
        for andere in andererSpieler.armee.einheiten
    }


@pytest.mark.parametrize(
    "einheitenname", ["Necron Warriors", "Overlord"], ids=["necronWarriors", "overlord"]
)
def testBew11_3DerDienstNenntDieNahkampfreichweiteDesGegnersMitExaktenRadien(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz, spielerZwei, einheitenname
):
    einheitenDesGegners = spielerZwei.armee.einheiten
    gegner = next(einheit for einheit in einheitenDesGegners if einheit.name == einheitenname)
    ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)
    stellen = jetzigeStellen(schlachtInDerBewegungsphase, gegner)

    spielstand = spielstandVon(dienstDerSchlacht)
    assert grenzenDerEinheitIm(spielstand, einheitenname) == grenzenImSpielstand(
        {grenzeDerNahkampfreichweite(stellen)}
    )


def testBew11_3DieSeiteZeigtJeEinheitDesAnderenSpielersDieNahkampfreichweite(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    expect(seite.locator(".karte g.grenze.spieler1")).to_have_count(1)
    expect(seite.locator(".karte g.grenze.spieler1.nahkampfreichweite")).to_have_count(0)
    expect(seite.locator(".karte g.grenze.spieler2.nahkampfreichweite")).to_have_count(2)
    expect(seite.locator(".karte g.grenze")).to_have_count(3)


def testBew11_4OhneAuswahlZeigtDieKarteKeinenGrenzkreis(schlachtInDerBewegungsphase):
    assert tuple(schlachtInDerBewegungsphase.grenzen) == ()


def testBew11_4UmEineAusgewählteEinheitDesAnderenSpielersZeigtDieKarteKeinenGrenzkreis(
    schlachtInDerBewegungsphase, necronWarriors
):
    schlachtInDerBewegungsphase.auswählen(necronWarriors)

    assert tuple(schlachtInDerBewegungsphase.grenzen) == ()


@pytest.mark.parametrize("phase", phasenAußerDerBewegungsphase, ids=phasenAußerDerBewegungsphaseIds)
def testBew11_4AußerhalbDerBewegungsphaseZeigtDieKarteKeinenGrenzkreis(
    schlachtNachDerWahlDesErstenZugs, boyz, phase: Phase
):
    phaseBeendenBis(schlachtNachDerWahlDesErstenZugs, phase)
    schlachtNachDerWahlDesErstenZugs.auswählen(boyz)

    assert tuple(schlachtNachDerWahlDesErstenZugs.grenzen) == ()


def testBew11_4NachDemAbwählenZeigtDieKarteKeinenGrenzkreis(schlachtInDerBewegungsphase, boyz):
    ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)
    schlachtInDerBewegungsphase.karteAnklicken(mitteDesSpielfelds)

    assert tuple(schlachtInDerBewegungsphase.grenzen) == ()


@pytest.mark.usefixtures("schlachtInDerBewegungsphase")
def testBew11_4DerDienstNenntOhneAuswahlKeinenGrenzkreis(dienstDerSchlacht):
    spielstand = spielstandVon(dienstDerSchlacht)
    assert spielstand["schlacht"]["grenzen"] == []


def testBew11_4DieSeiteZeigtOhneAuswahlKeinenGrenzkreis(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    ganzeEinheitAuswählen(schlachtInDerBewegungsphase, boyz)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    expect(seite.locator(".karte g.grenze.spieler1")).to_have_count(1)

    mitDerMausKlicken(seite, punktAufDerKarte(seite, mitteDesSpielfelds))

    expect(seite.locator(".karte g.grenze")).to_have_count(0)
