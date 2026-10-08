"""AUF-1 · Reihenfolge der Aufstellung."""

import pytest

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Spieler
from tests.akzeptanz.handgriffe import (
    aufstellungVon,
    einheitAufstellen,
    nachDerWahlDerAufstellungszone,
    sperrgründe,
    spielerMit,
    stellenDerEinheit,
)

ersteZone, zweiteZone = list(Aufstellungszone)


def reihenfolgeBeimAufstellen(aufstellung: Aufstellung, einheiten: list[Einheit]) -> list[Spieler]:
    reihenfolge = []
    for einheit in einheiten:
        reihenfolge.append(aufstellung.anDerReihe)
        einheitAufstellen(aufstellung, einheit)
    return reihenfolge


@pytest.mark.parametrize("gewählteZone", list(Aufstellungszone))
def testAuf1_1DieGewählteAufstellungszoneGehörtDemGewinner(
    aufstellung, ersterSpieler, gewählteZone
):
    aufstellung.gewinnerWählen(ersterSpieler)

    aufstellung.aufstellungszoneWählen(gewählteZone)

    assert aufstellung.gewinner is ersterSpieler
    assert aufstellung.aufstellungszone(ersterSpieler) == gewählteZone


@pytest.mark.parametrize("gewählteZone", list(Aufstellungszone))
def testAuf1_1DieAndereAufstellungszoneGehörtDemAnderenSpieler(
    aufstellung, ersterSpieler, zweiterSpieler, gewählteZone
):
    aufstellung.gewinnerWählen(ersterSpieler)

    aufstellung.aufstellungszoneWählen(gewählteZone)

    assert aufstellung.aufstellungszone(zweiterSpieler) != gewählteZone
    assert aufstellung.aufstellungszone(zweiterSpieler) in Aufstellungszone


def testAuf1_1GewinnerKannJederDerBeidenSpielerSein(aufstellung, ersterSpieler, zweiterSpieler):
    aufstellung.gewinnerWählen(zweiterSpieler)

    aufstellung.aufstellungszoneWählen(ersteZone)

    assert aufstellung.gewinner is zweiterSpieler
    assert aufstellung.aufstellungszone(zweiterSpieler) == ersteZone
    assert aufstellung.aufstellungszone(ersterSpieler) == zweiteZone


def testAuf1_2DieAufstellungszoneVorDemGewinnerIstNichtWählbar(aufstellung, ersterSpieler):
    gründe = sperrgründe(aufstellung.aufstellungszoneWählen, ersteZone)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.gewinner is None
    assert aufstellung.aufstellungszone(ersterSpieler) is None


def testAuf1_2NachDerGesperrtenZoneSindGewinnerUndZoneNochWählbar(aufstellung, ersterSpieler):
    sperrgründe(aufstellung.aufstellungszoneWählen, ersteZone)
    aufstellung.gewinnerWählen(ersterSpieler)

    aufstellung.aufstellungszoneWählen(ersteZone)

    assert aufstellung.gewinner is ersterSpieler
    assert aufstellung.aufstellungszone(ersterSpieler) == ersteZone


def testAuf1_2DerGewinnerEinZweitesMalIstNichtWählbar(aufstellung, ersterSpieler, zweiterSpieler):
    aufstellung.gewinnerWählen(ersterSpieler)

    gründe = sperrgründe(aufstellung.gewinnerWählen, zweiterSpieler)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.gewinner is ersterSpieler


def testAuf1_2DerselbeGewinnerEinZweitesMalIstNichtWählbar(aufstellung, ersterSpieler):
    aufstellung.gewinnerWählen(ersterSpieler)

    gründe = sperrgründe(aufstellung.gewinnerWählen, ersterSpieler)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.gewinner is ersterSpieler


def testAuf1_2DerGewinnerNachDerAufstellungszoneIstNichtWählbar(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)

    gründe = sperrgründe(aufstellung.gewinnerWählen, zweiterSpieler)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.gewinner is ersterSpieler
    assert aufstellung.anDerReihe is zweiterSpieler


@pytest.mark.parametrize("zweiteWahl", list(Aufstellungszone))
def testAuf1_2DieAufstellungszoneEinZweitesMalIstNichtWählbar(
    aufstellung, ersterSpieler, zweiteWahl
):
    aufstellung.gewinnerWählen(ersterSpieler)
    aufstellung.aufstellungszoneWählen(ersteZone)

    gründe = sperrgründe(aufstellung.aufstellungszoneWählen, zweiteWahl)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.aufstellungszone(ersterSpieler) == ersteZone


def testAuf1_3VorDerWahlDesGewinnersIstKeinerAnDerReihe(aufstellung):
    assert aufstellung.anDerReihe is None


def testAuf1_3NachDerWahlDesGewinnersIstNochKeinerAnDerReihe(aufstellung, ersterSpieler):
    aufstellung.gewinnerWählen(ersterSpieler)

    assert aufstellung.anDerReihe is None


def testAuf1_3NachDerWahlDerAufstellungszoneIstAnDerReiheWerNichtGewinnerIst(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)

    assert aufstellung.anDerReihe is zweiterSpieler


def testAuf1_3IstDerZweiteSpielerGewinnerIstDerErsteAnDerReihe(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=zweiterSpieler)

    assert aufstellung.anDerReihe is ersterSpieler


def testAuf1_7NachDemBeendenIstDieEinheitAufgestelltUndKeineInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, zweiteEinheit = zweiterSpieler.armee.einheiten
    for modell, stelle in stellenDerEinheit(aufstellung, zweiterSpieler, ersteEinheit):
        aufstellung.modellSetzen(modell, stelle)

    aufstellung.aufstellenDerEinheitBeenden()

    assert aufstellung.aufgestellt(ersteEinheit)
    assert aufstellung.einheitInAufstellung is None
    assert not aufstellung.aufgestellt(zweiteEinheit)


def testAuf1_7NachDemBeendenIstDerAndereSpielerAnDerReihe(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    for modell, stelle in stellenDerEinheit(aufstellung, zweiterSpieler, ersteEinheit):
        aufstellung.modellSetzen(modell, stelle)

    aufstellung.aufstellenDerEinheitBeenden()

    assert aufstellung.anDerReihe is ersterSpieler


def testAuf1_7DieSpielerStellenAbwechselndAuf(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheitErster, zweiteEinheitErster = ersterSpieler.armee.einheiten
    ersteEinheitZweiter, zweiteEinheitZweiter = zweiterSpieler.armee.einheiten
    einheiten = [ersteEinheitZweiter, ersteEinheitErster, zweiteEinheitZweiter, zweiteEinheitErster]

    reihenfolge = reihenfolgeBeimAufstellen(aufstellung, einheiten)

    assert reihenfolge == [zweiterSpieler, ersterSpieler, zweiterSpieler, ersterSpieler]


def testAuf1_7DerselbeSpielerBleibtNachSeinerErstenEinheitAnDerReihe():
    kleinerSpieler, größererSpieler = spielerMit(1), spielerMit(1, 1, 1)
    aufstellung = aufstellungVon(kleinerSpieler, größererSpieler)
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=größererSpieler)
    (einheitDesKleineren,) = kleinerSpieler.armee.einheiten
    ersteEinheit, _, _ = größererSpieler.armee.einheiten
    einheitAufstellen(aufstellung, einheitDesKleineren)

    einheitAufstellen(aufstellung, ersteEinheit)

    assert aufstellung.anDerReihe is größererSpieler


def testAuf1_7DerselbeSpielerBleibtNachSeinerZweitenEinheitAnDerReihe():
    kleinerSpieler, größererSpieler = spielerMit(1), spielerMit(1, 1, 1)
    aufstellung = aufstellungVon(kleinerSpieler, größererSpieler)
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=größererSpieler)
    (einheitDesKleineren,) = kleinerSpieler.armee.einheiten
    ersteEinheit, zweiteEinheit, _ = größererSpieler.armee.einheiten
    einheitAufstellen(aufstellung, einheitDesKleineren)
    einheitAufstellen(aufstellung, ersteEinheit)

    einheitAufstellen(aufstellung, zweiteEinheit)

    assert aufstellung.anDerReihe is größererSpieler


def testAuf1_7HabenBeideAlleEinheitenAufgestelltIstDieAufstellungBeendet():
    kleinerSpieler, größererSpieler = spielerMit(1), spielerMit(1, 1)
    aufstellung = aufstellungVon(kleinerSpieler, größererSpieler)
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=größererSpieler)
    (einheitDesKleineren,) = kleinerSpieler.armee.einheiten
    ersteEinheit, zweiteEinheit = größererSpieler.armee.einheiten
    einheitAufstellen(aufstellung, einheitDesKleineren)
    einheitAufstellen(aufstellung, ersteEinheit)

    einheitAufstellen(aufstellung, zweiteEinheit)

    assert aufstellung.beendet
    assert aufstellung.anDerReihe is None
    assert aufstellung.einheitInAufstellung is None


def testAuf1_7FehltNochEineEinheitIstDieAufstellungNichtBeendet():
    kleinerSpieler, größererSpieler = spielerMit(1), spielerMit(1, 1)
    aufstellung = aufstellungVon(kleinerSpieler, größererSpieler)
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=größererSpieler)
    (einheitDesKleineren,) = kleinerSpieler.armee.einheiten
    ersteEinheit, _ = größererSpieler.armee.einheiten
    einheitAufstellen(aufstellung, einheitDesKleineren)

    einheitAufstellen(aufstellung, ersteEinheit)

    assert not aufstellung.beendet


def testAuf1_7VorDerWahlIstDieAufstellungNichtBeendet(aufstellung):
    assert not aufstellung.beendet


def testAuf1_7NachDerWahlIstDieAufstellungNichtBeendet(aufstellung, ersterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)

    assert not aufstellung.beendet
