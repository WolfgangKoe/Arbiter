"""BEW-24 · Einheit zurücksetzen."""

from fractions import Fraction
from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from arbiter.domaene.querschnitt.schlachtrunden import Phase
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    knopfDerSeite,
    kreiseDesSpielfelds,
    seiteDerSchlachtMitEingabe,
)
from tests.akzeptanz.dienst import (
    einheitZurücksetzen,
    einheitZurückzusetzenDesVertrags,
    modellAnklicken,
    modellLoslassen,
    schlachtNachSchlüsselnDes,
    spielstandVon,
    stelleImSpielstand,
    stellenDerEinheitIm,
)
from tests.akzeptanz.grenzen import dreiAugen, zweiZollEntlangDerReihe
from tests.akzeptanz.handgriffe import versetzt
from tests.akzeptanz.schlacht import (
    angehaltenLoslassen,
    anhaltenUndÜbergehen,
    jetzigeStellen,
    mitteDesSpielfelds,
    phaseBeendenBis,
    stellenAlsZahlen,
    zehnZollNachOsten,
)
from tests.akzeptanz.vorruecken import (
    ebenen,
    ganzeEinheitAuswählen,
    mitJederEbene,
    modellebeneDesLetztenWählen,
    vorgerücktMit,
)

zurücksetzenKnopf = "Einheit zurücksetzen"
dreiZollNachOsten = (Fraction(3), Fraction(0))
phasenNachDerBewegungsphase = (
    Phase.psiphase,
    Phase.schussphase,
    Phase.angriffsphase,
    Phase.nahkampfphase,
    Phase.moralphase,
)


def ganzeEinheitZiehen(schlacht, einheit):
    stellen = ganzeEinheitAuswählen(schlacht, einheit)
    erstes, *_ = einheit.modelle
    schlacht.modellLoslassen(erstes, zweiZollEntlangDerReihe(stellen[erstes]))
    assert jetzigeStellen(schlacht, einheit) != stellen, "Die Einheit wurde nicht gezogen"
    return stellen


def nurDasLetzteModellZiehen(schlacht, einheit):
    stellen = jetzigeStellen(schlacht, einheit)
    modellebeneDesLetztenWählen(schlacht, einheit)
    *_, letztes = einheit.modelle
    ziel = zweiZollEntlangDerReihe(stellen[letztes])
    schlacht.modellLoslassen(letztes, ziel)
    gezogen = jetzigeStellen(schlacht, einheit)
    assert gezogen == {**stellen, letztes: ziel}, "Nicht nur das letzte Modell wurde gezogen"
    return stellen


def warbossZiehen(schlacht, warboss):
    (boss,) = warboss.modelle
    davor = schlacht.stelle(boss)
    ziel = versetzt(davor, dreiZollNachOsten)
    schlacht.modellLoslassen(boss, ziel)
    assert schlacht.stelle(boss) == ziel, "Der Warboss steht nicht, wo der Test ihn braucht"
    return davor


@mitJederEbene
def testBew24_1IstEinModellDerAusgewähltenEinheitGezogenBietetArbiterZurücksetzenAn(
    einheitAmZug, ebene
):
    schlacht, einheit, _, _ = einheitAmZug
    ganzeEinheitZiehen(schlacht, einheit)
    schlacht.spielfeldAnklicken(mitteDesSpielfelds)
    ebenen[ebene](schlacht, einheit)

    assert schlacht.einheitZurücksetzenAngeboten is True


def testBew24_1IstNurEinModellDerEinheitGezogenBietetArbiterZurücksetzenAn(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    nurDasLetzteModellZiehen(schlacht, einheit)

    assert schlacht.einheitZurücksetzenAngeboten is True


def testBew24_1IstKeinModellDerAusgewähltenEinheitGezogenBietetArbiterZurücksetzenNichtAn(
    einheitAmZug,
):
    schlacht, einheit, _, _ = einheitAmZug
    ganzeEinheitAuswählen(schlacht, einheit)

    assert schlacht.einheitZurücksetzenAngeboten is False


def testBew24_1StehtJedesModellWiederWoEsZuBeginnStandBietetArbiterZurücksetzenNichtAn(
    einheitAmZug,
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = ganzeEinheitZiehen(schlacht, einheit)
    erstes, *_ = einheit.modelle
    schlacht.modellLoslassen(erstes, stellen[erstes])
    assert jetzigeStellen(schlacht, einheit) == stellen, "Die Einheit steht nicht am Beginn"
    assert schlacht.ausgewählt(einheit), "Die Einheit ist nicht ausgewählt"

    assert schlacht.einheitZurücksetzenAngeboten is False


def testBew24_1WartetDieGezogeneEinheitAufIhrenVorrückwurfBietetArbiterZurücksetzenNichtAn(
    einheitAmZug,
):
    schlacht, einheit, _, _ = einheitAmZug
    ganzeEinheitZiehen(schlacht, einheit)
    schlacht.vorrücken()
    assert schlacht.wartetAufVorrückwurf(einheit), "Die Einheit wartet nicht"
    assert schlacht.ausgewählt(einheit), "Die Einheit ist nicht ausgewählt"

    assert schlacht.einheitZurücksetzenAngeboten is False


def testBew24_1IstDieGezogeneEinheitVorgerücktBietetArbiterZurücksetzenNichtAn(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = vorgerücktMit(schlacht, einheit, dreiAugen)
    erstes, *_ = einheit.modelle
    schlacht.modellLoslassen(erstes, zweiZollEntlangDerReihe(stellen[erstes]))
    assert jetzigeStellen(schlacht, einheit) != stellen, "Die Einheit wurde nicht gezogen"
    assert schlacht.ausgewählt(einheit), "Die Einheit ist nicht ausgewählt"

    assert schlacht.einheitZurücksetzenAngeboten is False


def testBew24_1IstEineAndereEinheitAusgewähltBietetArbiterZurücksetzenNichtAn(einheitAmZug):
    schlacht, einheit, andereEinheit, _ = einheitAmZug
    ganzeEinheitZiehen(schlacht, einheit)
    schlacht.auswählen(andereEinheit)

    assert schlacht.einheitZurücksetzenAngeboten is False


def testBew24_1OhneAuswahlBietetArbiterZurücksetzenNichtAn(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    ganzeEinheitZiehen(schlacht, einheit)
    schlacht.spielfeldAnklicken(mitteDesSpielfelds)

    assert schlacht.einheitZurücksetzenAngeboten is False


def testBew24_1ZurEinheitDesAnderenSpielersBietetArbiterZurücksetzenNichtAn(einheitAmZug):
    schlacht, einheit, _, andererSpieler = einheitAmZug
    ganzeEinheitZiehen(schlacht, einheit)
    einheitDesAnderenSpielers, *_ = andererSpieler.armee.einheiten
    schlacht.auswählen(einheitDesAnderenSpielers)

    assert schlacht.einheitZurücksetzenAngeboten is False


@pytest.mark.parametrize(
    "phase", phasenNachDerBewegungsphase, ids=[phase.name for phase in phasenNachDerBewegungsphase]
)
def testBew24_1NachDerBewegungsphaseBietetArbiterZurücksetzenNichtAn(
    schlachtInDerBewegungsphase, warboss, phase
):
    warbossZiehen(schlachtInDerBewegungsphase, warboss)
    phaseBeendenBis(schlachtInDerBewegungsphase, phase)
    schlachtInDerBewegungsphase.auswählen(warboss)

    assert schlachtInDerBewegungsphase.einheitZurücksetzenAngeboten is False


def testBew24_1DerDienstNenntZurücksetzenAngebotenWieImBeispielDesVertrags(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), dreiZollNachOsten)
    modellAnklicken(dienstDerSchlacht, beendeteAufstellung, warboss, boss)
    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, boss, ziel)

    beispiel = einheitZurückzusetzenDesVertrags()["schlacht"]
    assert antwort.status_code == HTTPStatus.OK
    assert schlachtNachSchlüsselnDes(antwort.get_json(), beispiel) == beispiel


def testBew24_1DerDienstNenntZurVorgerücktenEinheitZurücksetzenNichtAngeboten(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    stellen = vorgerücktMit(schlachtInDerBewegungsphase, boyz, dreiAugen)
    erstes, *_ = boyz.modelle
    schlachtInDerBewegungsphase.modellLoslassen(erstes, zweiZollEntlangDerReihe(stellen[erstes]))

    spielstand = spielstandVon(dienstDerSchlacht)

    assert spielstand["schlacht"]["einheitZurücksetzen"] == {"angeboten": False}


def testBew24_1DieSeiteZeigtZurGezogenenEinheitDenKnopfVorPhaseBeenden(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    warbossZiehen(schlachtInDerBewegungsphase, warboss)
    schlachtInDerBewegungsphase.auswählen(warboss)

    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    expect(knopfDerSeite(seite, zurücksetzenKnopf)).to_have_count(1)
    knöpfe = [text.strip() for text in seite.locator(".knopfGruppe .knopf").all_text_contents()]
    assert knöpfe == ["Vorrücken", zurücksetzenKnopf, "Phase beenden"]


def testBew24_1DieSeiteZeigtOhneGezogenesModellKeinenKnopfZurücksetzen(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    schlachtInDerBewegungsphase.auswählen(warboss)

    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    expect(knopfDerSeite(seite, "Vorrücken")).to_have_count(1)
    expect(knopfDerSeite(seite, zurücksetzenKnopf)).to_have_count(0)


@mitJederEbene
def testBew24_2NachDemZurücksetzenStehtJedesModellWoEsZuBeginnDerBewegungsphaseStand(
    einheitAmZug, ebene
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = ganzeEinheitZiehen(schlacht, einheit)
    ebenen[ebene](schlacht, einheit)

    schlacht.einheitZurücksetzen()

    assert jetzigeStellen(schlacht, einheit) == stellen
    assert schlacht.ausgewählt(einheit)
    assert schlacht.einheitZurücksetzenAngeboten is False


def testBew24_2IstNurEinModellGezogenStehtNachDemZurücksetzenJedesModellWoEsZuBeginnStand(
    einheitAmZug,
):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = nurDasLetzteModellZiehen(schlacht, einheit)

    schlacht.einheitZurücksetzen()

    assert jetzigeStellen(schlacht, einheit) == stellen


def testBew24_2NachDemÜbergehenUndWeiterziehenStehtDasModellWoEsZuBeginnStand(
    schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(boss)
    vorige = versetzt(davor, zehnZollNachOsten)
    anhaltenUndÜbergehen(schlachtInDerBewegungsphase, boss, vorige)
    anhaltenUndÜbergehen(schlachtInDerBewegungsphase, boss, versetzt(vorige, zehnZollNachOsten))
    schlachtInDerBewegungsphase.auswählen(warboss)
    protokoll = tuple(schlachtInDerBewegungsphase.protokoll)

    schlachtInDerBewegungsphase.einheitZurücksetzen()

    assert schlachtInDerBewegungsphase.stelle(boss) == davor
    assert tuple(schlachtInDerBewegungsphase.protokoll) == protokoll


def testBew24_2NachDemZurücksetzenSetztGemeinsamÜbergehenNichtMehrAmPunkt(
    schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(boss)
    angehaltenLoslassen(schlachtInDerBewegungsphase, boss, versetzt(davor, zehnZollNachOsten))
    schlachtInDerBewegungsphase.auswählen(warboss)
    schlachtInDerBewegungsphase.einheitZurücksetzen()

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    assert schlachtInDerBewegungsphase.stelle(boss) == davor
    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is False


def testBew24_2DasZurücksetzenLässtJedeAndereEinheitWoSieHingezogenWurde(
    schlachtInDerBewegungsphase, boyz, warboss
):
    ganzeEinheitZiehen(schlachtInDerBewegungsphase, boyz)
    gezogeneBoyz = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    davor = warbossZiehen(schlachtInDerBewegungsphase, warboss)
    schlachtInDerBewegungsphase.auswählen(warboss)

    schlachtInDerBewegungsphase.einheitZurücksetzen()

    (boss,) = warboss.modelle
    assert schlachtInDerBewegungsphase.stelle(boss) == davor
    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == gezogeneBoyz


def testBew24_2OhneAngebotBleibtDieVorgerückteEinheitWoSieHingezogenWurde(einheitAmZug):
    schlacht, einheit, _, _ = einheitAmZug
    stellen = vorgerücktMit(schlacht, einheit, dreiAugen)
    erstes, *_ = einheit.modelle
    schlacht.modellLoslassen(erstes, zweiZollEntlangDerReihe(stellen[erstes]))
    gezogen = jetzigeStellen(schlacht, einheit)
    assert schlacht.ausgewählt(einheit), "Die Einheit ist nicht ausgewählt"

    schlacht.einheitZurücksetzen()

    assert jetzigeStellen(schlacht, einheit) == gezogen
    assert schlacht.vorgerückt(einheit)


def testBew24_2DerDienstSetztJedesModellAnSeineStelleZuBeginnDerBewegungsphase(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    stellen = ganzeEinheitZiehen(schlachtInDerBewegungsphase, boyz)

    antwort = einheitZurücksetzen(dienstDerSchlacht)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(spielstand, "Boyz") == {
        nummer: stelleImSpielstand(stellen[modell])
        for nummer, modell in enumerate(boyz.modelle, start=1)
    }
    assert spielstand["schlacht"]["einheitZurücksetzen"] == {"angeboten": False}


def testBew24_2DerDienstÄndertBeimZweitenZurücksetzenNichts(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    ganzeEinheitZiehen(schlachtInDerBewegungsphase, boyz)
    einheitZurücksetzen(dienstDerSchlacht)
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    antwort = einheitZurücksetzen(dienstDerSchlacht)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == spielstandDavor


def testBew24_2AmBildschirmSetztDerKnopfDieEinheitAnIhreStellenZuBeginn(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    zuBeginn = stellenAlsZahlen(schlachtInDerBewegungsphase)
    warbossZiehen(schlachtInDerBewegungsphase, warboss)
    schlachtInDerBewegungsphase.auswählen(warboss)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, zurücksetzenKnopf).click()

    expect(knopfDerSeite(seite, zurücksetzenKnopf)).to_have_count(0)
    assert kreiseDesSpielfelds(seite) == zuBeginn
