"""AUF-1 · Reihenfolge der Aufstellung."""

from fractions import Fraction

import pytest

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Spieler, Stelle
from tests.akzeptanz.handgriffe import (
    aufstellungVon,
    einheitAufstellen,
    sperrgründe,
    spielerMit,
    stelleDesErstenModells,
    stellenDerEinheit,
)

ersteZone, zweiteZone = list(Aufstellungszone)
# Warum: Gesperrt wird vor jeder Prüfung der Stelle (AUF-3.6), welche Stelle ist gleich.
irgendeineStelle = Stelle(x=Fraction(3, 2), y=Fraction(1))


def nachDerWahlDerAufstellungszone(aufstellung: Aufstellung, gewinner: Spieler) -> None:
    aufstellung.gewinnerWählen(gewinner)
    aufstellung.aufstellungszoneWählen(ersteZone)


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


def testAuf1_4EinModellDerEinheitInAufstellungLässtSichSetzen(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, *_ = ersteEinheit.modelle
    stelle = stelleDesErstenModells(aufstellung, zweiterSpieler, ersteEinheit)
    aufstellung.einheitInAufstellungWählen(ersteEinheit)

    aufstellung.modellSetzen(erstesModell, stelle)

    assert aufstellung.gesetzt(erstesModell)


def testAuf1_4OhneEinheitInAufstellungIstSetzenNichtInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, *_ = ersteEinheit.modelle

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, irgendeineStelle)

    assert gründe == {Grund.nichtInAufstellung}
    assert not aufstellung.gesetzt(erstesModell)


def testAuf1_4VorDerWahlIstSetzenNichtInAufstellung(aufstellung, ersterSpieler):
    ersteEinheit, _ = ersterSpieler.armee.einheiten
    erstesModell, *_ = ersteEinheit.modelle

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, irgendeineStelle)

    assert gründe == {Grund.nichtInAufstellung}
    assert not aufstellung.gesetzt(erstesModell)


def testAuf1_4EinModellEinerAnderenEinheitIstNichtInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheitInAufstellung, andereEinheit = zweiterSpieler.armee.einheiten
    modellDerAnderenEinheit, *_ = andereEinheit.modelle
    aufstellung.einheitInAufstellungWählen(einheitInAufstellung)

    gründe = sperrgründe(aufstellung.modellSetzen, modellDerAnderenEinheit, irgendeineStelle)

    assert gründe == {Grund.nichtInAufstellung}
    assert not aufstellung.gesetzt(modellDerAnderenEinheit)


def testAuf1_4EinModellDesAnderenSpielersIstNichtInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheitInAufstellung, _ = zweiterSpieler.armee.einheiten
    einheitDesAnderenSpielers, _ = ersterSpieler.armee.einheiten
    modellDesAnderenSpielers, *_ = einheitDesAnderenSpielers.modelle
    aufstellung.einheitInAufstellungWählen(einheitInAufstellung)

    gründe = sperrgründe(aufstellung.modellSetzen, modellDesAnderenSpielers, irgendeineStelle)

    assert gründe == {Grund.nichtInAufstellung}
    assert not aufstellung.gesetzt(modellDesAnderenSpielers)


def testAuf1_4OhneEinheitInAufstellungIstBeendenNichtInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.nichtInAufstellung}
    assert aufstellung.anDerReihe is zweiterSpieler


def testAuf1_4VorDerWahlIstBeendenNichtInAufstellung(aufstellung):
    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.nichtInAufstellung}
    assert aufstellung.anDerReihe is None
    assert not aufstellung.beendet


def testAuf1_4NachDemBeendenGibtEsKeineEinheitZumErneutenBeenden(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    einheitAufstellen(aufstellung, ersteEinheit)

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.nichtInAufstellung}
    assert aufstellung.anDerReihe is ersterSpieler


def testAuf1_5EineNichtAufgestellteEinheitDesSpielersAnDerReiheIstWählbar(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    _, zweiteEinheit = zweiterSpieler.armee.einheiten

    aufstellung.einheitInAufstellungWählen(zweiteEinheit)

    assert aufstellung.einheitInAufstellung is zweiteEinheit


def testAuf1_5VorDerWahlIstKeineEinheitWählbar(aufstellung, ersterSpieler):
    ersteEinheit, _ = ersterSpieler.armee.einheiten

    gründe = sperrgründe(aufstellung.einheitInAufstellungWählen, ersteEinheit)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.einheitInAufstellung is None


def testAuf1_5EineEinheitDesSpielersNichtAnDerReiheIstNichtWählbar(aufstellung, ersterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = ersterSpieler.armee.einheiten

    gründe = sperrgründe(aufstellung.einheitInAufstellungWählen, ersteEinheit)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.einheitInAufstellung is None


def testAuf1_5EineAufgestellteEinheitIstNichtWählbar(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    aufgestellteEinheit, _ = zweiterSpieler.armee.einheiten
    einheitDesAnderenSpielers, _ = ersterSpieler.armee.einheiten
    einheitAufstellen(aufstellung, aufgestellteEinheit)
    einheitAufstellen(aufstellung, einheitDesAnderenSpielers)

    gründe = sperrgründe(aufstellung.einheitInAufstellungWählen, aufgestellteEinheit)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.einheitInAufstellung is None


def testAuf1_5NachDerAufstellungIstKeineEinheitWählbar(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheitErster, zweiteEinheitErster = ersterSpieler.armee.einheiten
    ersteEinheitZweiter, zweiteEinheitZweiter = zweiterSpieler.armee.einheiten
    einheitAufstellen(aufstellung, ersteEinheitZweiter)
    einheitAufstellen(aufstellung, ersteEinheitErster)
    einheitAufstellen(aufstellung, zweiteEinheitZweiter)
    einheitAufstellen(aufstellung, zweiteEinheitErster)

    gründe = [
        sperrgründe(aufstellung.einheitInAufstellungWählen, einheit)
        for einheit in (
            ersteEinheitErster,
            zweiteEinheitErster,
            ersteEinheitZweiter,
            zweiteEinheitZweiter,
        )
    ]

    assert gründe == [{Grund.nichtWählbar}] * 4
    assert aufstellung.einheitInAufstellung is None


def testAuf1_5GegenEineNichtWählbareEinheitGiltNichtWählbarAuchNachBegonnenerEinheit(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, *_ = begonneneEinheit.modelle
    einheitDesAnderenSpielers, _ = ersterSpieler.armee.einheiten
    stelle = stelleDesErstenModells(aufstellung, zweiterSpieler, begonneneEinheit)
    aufstellung.einheitInAufstellungWählen(begonneneEinheit)
    aufstellung.modellSetzen(erstesModell, stelle)

    gründe = sperrgründe(aufstellung.einheitInAufstellungWählen, einheitDesAnderenSpielers)

    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.einheitInAufstellung is begonneneEinheit


def testAuf1_6OhneGesetztesModellLöstDieWählbareEinheitDieBisherigeAb(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    bisherigeEinheit, wählbareEinheit = zweiterSpieler.armee.einheiten
    aufstellung.einheitInAufstellungWählen(bisherigeEinheit)

    aufstellung.einheitInAufstellungWählen(wählbareEinheit)

    assert aufstellung.einheitInAufstellung is wählbareEinheit


def testAuf1_6MitGesetztemModellIstDieEinheitBegonnen(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, andereEinheit = zweiterSpieler.armee.einheiten
    erstesModell, *_ = begonneneEinheit.modelle
    stelle = stelleDesErstenModells(aufstellung, zweiterSpieler, begonneneEinheit)
    aufstellung.einheitInAufstellungWählen(begonneneEinheit)
    aufstellung.modellSetzen(erstesModell, stelle)

    gründe = sperrgründe(aufstellung.einheitInAufstellungWählen, andereEinheit)

    assert gründe == {Grund.einheitBegonnen}
    assert aufstellung.einheitInAufstellung is begonneneEinheit


def testAuf1_6DieBegonneneEinheitErneutWählenSperrtNicht(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, *_ = begonneneEinheit.modelle
    stelle = stelleDesErstenModells(aufstellung, zweiterSpieler, begonneneEinheit)
    aufstellung.einheitInAufstellungWählen(begonneneEinheit)
    aufstellung.modellSetzen(erstesModell, stelle)

    aufstellung.einheitInAufstellungWählen(begonneneEinheit)

    assert aufstellung.einheitInAufstellung is begonneneEinheit
    assert aufstellung.gesetzt(erstesModell)


def testAuf1_7NachDemBeendenIstDieEinheitAufgestelltUndKeineInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, zweiteEinheit = zweiterSpieler.armee.einheiten
    aufstellung.einheitInAufstellungWählen(ersteEinheit)
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
    aufstellung.einheitInAufstellungWählen(ersteEinheit)
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
