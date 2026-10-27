"""QUE-10 · Schlachtrunden und Phasen."""

from fractions import Fraction
from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from arbiter.domaene.querschnitt.schlachtrunden import Phase
from tests.akzeptanz.bildschirm import (
    amZugGekennzeichnet,
    knopfDerSeite,
    kopfzeileVon,
    spielerAmZug,
)
from tests.akzeptanz.dienst import (
    ersterZugWählen,
    phaseBeenden,
    schlachtDesVertrags,
    spielstandVon,
)
from tests.akzeptanz.handgriffe import stellenAllerModelle, versetzt
from tests.akzeptanz.schlacht import (
    phaseBeendenBis,
    phasenAußerDerBewegungsphase,
    phasenAußerDerBewegungsphaseIds,
    phasenEinesZugs,
    phasenwechsel,
    phasenwechselIds,
    zurLetztenSchlachtrunde,
    zügeBeenden,
)

zweiteSchlachtrunde = 2
schlachtendeText = "Schlacht beendet"
phaseBeendenKnopf = "Phase beenden"


@pytest.fixture
def andererSpieler(spielerMitDemErstenZug, spielerEins, spielerZwei):
    return spielerZwei if spielerMitDemErstenZug is spielerEins else spielerEins


@pytest.fixture
def nameDesSpielersMitDemErstenZug(spielerMitDemErstenZug, spielerEins) -> str:
    return "Spieler 1" if spielerMitDemErstenZug is spielerEins else "Spieler 2"


@pytest.fixture
def nameDesAnderenSpielers(nameDesSpielersMitDemErstenZug) -> str:
    return "Spieler 2" if nameDesSpielersMitDemErstenZug == "Spieler 1" else "Spieler 1"


@pytest.fixture
def schlachtMitErstemZug(schlacht, spielerMitDemErstenZug):
    schlacht.ersterZugWählen(spielerMitDemErstenZug)
    return schlacht


@pytest.fixture
def moralphaseDesErstenSpielers(schlachtMitErstemZug):
    phaseBeendenBis(schlachtMitErstemZug, Phase.moralphase)
    return schlachtMitErstemZug


@pytest.fixture
def moralphaseDesZweitenSpielers(schlachtMitErstemZug):
    zügeBeenden(schlachtMitErstemZug, 1)
    phaseBeendenBis(schlachtMitErstemZug, Phase.moralphase)
    return schlachtMitErstemZug


@pytest.fixture
def moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde(schlachtMitErstemZug):
    zurLetztenSchlachtrunde(schlachtMitErstemZug)
    zügeBeenden(schlachtMitErstemZug, 1)
    phaseBeendenBis(schlachtMitErstemZug, Phase.moralphase)
    return schlachtMitErstemZug


def testQue10_1DieKopfzeileDesSpielersAmZugNenntSchlachtrundeUndPhase(
    bildschirm, beendeteAufstellung, schlachtMitErstemZug, nameDesSpielersMitDemErstenZug
):
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlachtMitErstemZug)

    kopfzeile = kopfzeileVon(seite, nameDesSpielersMitDemErstenZug)

    expect(kopfzeile).to_have_class(amZugGekennzeichnet)
    expect(kopfzeile.locator(".kopfzeileAmZug")).to_have_text("Schlachtrunde 1 · Kommandophase")


def testQue10_1DieKopfzeileDesAnderenSpielersNenntKeinePhase(
    bildschirm, beendeteAufstellung, schlachtMitErstemZug, nameDesAnderenSpielers
):
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlachtMitErstemZug)
    expect(spielerAmZug(seite)).to_have_count(1)

    kopfzeile = kopfzeileVon(seite, nameDesAnderenSpielers)

    expect(kopfzeile).not_to_have_class(amZugGekennzeichnet)
    expect(kopfzeile.locator(".kopfzeileAmZug")).to_have_count(0)


@pytest.mark.parametrize("phase", phasenEinesZugs, ids=[phase.name for phase in phasenEinesZugs])
def testQue10_1DieKopfzeileNenntDenNamenDerLaufendenPhase(
    bildschirm, beendeteAufstellung, schlachtMitErstemZug, nameDesSpielersMitDemErstenZug, phase
):
    phaseBeendenBis(schlachtMitErstemZug, phase)
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlachtMitErstemZug)

    kopfzeile = kopfzeileVon(seite, nameDesSpielersMitDemErstenZug)

    expect(kopfzeile.locator(".kopfzeileAmZug")).to_have_text(f"Schlachtrunde 1 · {phase.value}")


def testQue10_1DieKopfzeileNenntNachDemZugDesErstenSpielersDenAnderenInDerNächstenPhaseDerRunde(
    bildschirm, beendeteAufstellung, moralphaseDesErstenSpielers, nameDesAnderenSpielers
):
    moralphaseDesErstenSpielers.phaseBeenden()
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, moralphaseDesErstenSpielers)

    kopfzeile = kopfzeileVon(seite, nameDesAnderenSpielers)

    expect(kopfzeile).to_have_class(amZugGekennzeichnet)
    expect(kopfzeile.locator(".kopfzeileAmZug")).to_have_text("Schlachtrunde 1 · Kommandophase")


def testQue10_1DerSpielstandNenntSchlachtrundeAmZugUndPhaseWieImBeispielDesVertrags(
    dienstNachDerAufstellung,
):
    beispiel = schlachtDesVertrags()
    ersterZugWählen(dienstNachDerAufstellung, 1)

    antwort = phaseBeenden(dienstNachDerAufstellung, 1, 1, Phase.kommandophase)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert spielstand["schlacht"] == beispiel["schlacht"]
    assert spielstand["spieler"] == beispiel["spieler"]


@pytest.mark.parametrize(("davor", "danach"), phasenwechsel, ids=phasenwechselIds)
def testQue10_2PhaseBeendenWechseltInDieNächsteStufeDerReihenfolge(
    schlachtInDerKommandophase, davor, danach
):
    phaseBeendenBis(schlachtInDerKommandophase, davor)

    schlachtInDerKommandophase.phaseBeenden()

    assert schlachtInDerKommandophase.phase is danach


@pytest.mark.parametrize(("davor", "danach"), phasenwechsel, ids=phasenwechselIds)
def testQue10_2DerSpielerBleibtInDerselbenSchlachtrundeAmZug(
    schlachtInDerKommandophase, spielerEins, davor, danach
):
    phaseBeendenBis(schlachtInDerKommandophase, davor)

    schlachtInDerKommandophase.phaseBeenden()

    assert schlachtInDerKommandophase.amZug is spielerEins
    assert schlachtInDerKommandophase.schlachtrunde == 1
    assert schlachtInDerKommandophase.phase is danach


def testQue10_3NachDerMoralphaseDesErstenSpielersIstDerAndereAmZug(
    moralphaseDesErstenSpielers, andererSpieler
):
    moralphaseDesErstenSpielers.phaseBeenden()

    assert moralphaseDesErstenSpielers.amZug is andererSpieler


def testQue10_3NachDerMoralphaseDesErstenSpielersBeginntDerAndereMitDerKommandophase(
    moralphaseDesErstenSpielers,
):
    moralphaseDesErstenSpielers.phaseBeenden()

    assert moralphaseDesErstenSpielers.phase is Phase.kommandophase


def testQue10_3NachDerMoralphaseDesErstenSpielersBleibtDieSchlachtrunde(
    moralphaseDesErstenSpielers,
):
    moralphaseDesErstenSpielers.phaseBeenden()

    assert moralphaseDesErstenSpielers.schlachtrunde == 1


def testQue10_3NachDerMoralphaseDesZweitenSpielersHatDerErsteZugWiederDenZug(
    moralphaseDesZweitenSpielers, spielerMitDemErstenZug
):
    moralphaseDesZweitenSpielers.phaseBeenden()

    assert moralphaseDesZweitenSpielers.amZug is spielerMitDemErstenZug
    assert moralphaseDesZweitenSpielers.phase is Phase.kommandophase


def testQue10_3NachDerMoralphaseDesZweitenSpielersBeginntDieNächsteSchlachtrunde(
    moralphaseDesZweitenSpielers,
):
    moralphaseDesZweitenSpielers.phaseBeenden()

    assert moralphaseDesZweitenSpielers.schlachtrunde == zweiteSchlachtrunde


def testQue10_4NachDerMoralphaseDesZweitenSpielersInDerLetztenSchlachtrundeIstSieBeendet(
    moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde,
):
    moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde.phaseBeenden()

    assert moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde.beendet


def testQue10_4NachDemEndeDerSchlachtIstKeinerAmZug(
    moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde,
):
    moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde.phaseBeenden()

    assert moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde.amZug is None


def testQue10_4NachDerMoralphaseDesErstenSpielersInDerLetztenSchlachtrundeIstSieNochNichtBeendet(
    schlachtMitErstemZug, andererSpieler
):
    zurLetztenSchlachtrunde(schlachtMitErstemZug)
    phaseBeendenBis(schlachtMitErstemZug, Phase.moralphase)

    schlachtMitErstemZug.phaseBeenden()

    assert not schlachtMitErstemZug.beendet
    assert schlachtMitErstemZug.amZug is andererSpieler


def testQue10_4NachDerVorletztenSchlachtrundeIstDieSchlachtNochNichtBeendet(
    schlachtMitErstemZug, spielerMitDemErstenZug
):
    zurLetztenSchlachtrunde(schlachtMitErstemZug)

    assert not schlachtMitErstemZug.beendet
    assert schlachtMitErstemZug.amZug is spielerMitDemErstenZug


def testQue10_4DieSeiteZeigtNachDemEndeDerSchlachtSchlachtBeendetUndKeinenSpielerAmZug(
    bildschirm, beendeteAufstellung, moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde
):
    schlacht = moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlacht)
    expect(spielerAmZug(seite)).to_have_count(1)

    knopfDerSeite(seite, phaseBeendenKnopf).click()

    expect(seite.locator(".kopfzeileTitel .kopfzeileSchlachtBeendet")).to_have_text(
        schlachtendeText
    )
    expect(spielerAmZug(seite)).to_have_count(0)
    expect(knopfDerSeite(seite, phaseBeendenKnopf)).to_have_count(0)


def testQue10_4DieSeiteZeigtVorDemEndeDerSchlachtKeineBeendeteSchlacht(
    bildschirm, beendeteAufstellung, moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde
):
    schlacht = moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlacht)
    expect(spielerAmZug(seite)).to_have_count(1)

    gezeigt = seite.locator(".kopfzeileSchlachtBeendet")

    expect(gezeigt).to_have_count(0)


def testQue10_4DerSpielstandNenntNachDemEndeDerSchlachtSieBeendetOhneSpielerAmZug(
    dienstDerSchlacht, moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde
):
    schlacht = moralphaseDesZweitenSpielersInDerLetztenSchlachtrunde
    schlacht.phaseBeenden()

    spielstand = spielstandVon(dienstDerSchlacht)

    assert spielstand["schlacht"]["beendet"] is True
    assert spielstand["schlacht"]["amZug"] is None


@pytest.mark.parametrize("phase", phasenAußerDerBewegungsphase, ids=phasenAußerDerBewegungsphaseIds)
def testQue10_5ZiehenAußerhalbDerBewegungsphaseLässtJedesModellStehenOhneGrund(
    schlachtInDerKommandophase, boyz, phase
):
    schlachtInDerKommandophase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerKommandophase.stelle(gezogenes), (Fraction(0), Fraction(2)))
    phaseBeendenBis(schlachtInDerKommandophase, phase)
    davor = stellenAllerModelle(schlachtInDerKommandophase)

    schlachtInDerKommandophase.modellLoslassen(gezogenes, ziel)

    assert stellenAllerModelle(schlachtInDerKommandophase) == davor
    assert ziel != davor[gezogenes]
