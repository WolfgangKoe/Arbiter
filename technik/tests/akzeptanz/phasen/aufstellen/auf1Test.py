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
    stelleInZone,
    stellenDerEinheit,
)

ersteZone, zweiteZone = list(Aufstellungszone)
# Warum: Gesperrt wird vor jeder Prüfung der Stelle (AUF-3.8), welche Stelle ist gleich.
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


def testAuf1_8VorDemSetzenEinesModellsIstKeineEinheitInAufstellung(aufstellung, ersterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)

    assert aufstellung.einheitInAufstellung is None


def testAuf1_8VorDerWahlIstKeineEinheitInAufstellung(aufstellung):
    assert aufstellung.einheitInAufstellung is None


def testAuf1_8MitDemErstenGesetztenModellIstDieEinheitDieEinheitInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, _ = ersteEinheit.modelle
    stelle = stelleDesErstenModells(aufstellung, zweiterSpieler, ersteEinheit)

    aufstellung.modellSetzen(erstesModell, stelle)

    assert aufstellung.einheitInAufstellung is ersteEinheit


def testAuf1_8MitWeiterenGesetztenModellenBleibtDieEinheitEinheitInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    (erstesModell, ersteStelle), (zweitesModell, zweiteStelle) = stellenDerEinheit(
        aufstellung, zweiterSpieler, ersteEinheit
    )
    aufstellung.modellSetzen(erstesModell, ersteStelle)

    aufstellung.modellSetzen(zweitesModell, zweiteStelle)

    assert aufstellung.einheitInAufstellung is ersteEinheit


def testAuf1_8EinGesperrtesSetzenMachtDieEinheitNichtZurEinheitInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, _ = ersteEinheit.modelle
    stelleInDerZoneDesAnderen = stelleInZone(ersteZone, Fraction(3, 2), Fraction(3))

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, stelleInDerZoneDesAnderen)

    assert gründe == {Grund.nichtGanzInDerZone}
    assert aufstellung.einheitInAufstellung is None


def testAuf1_8NachDemBeendenIstDieAufgestellteEinheitKeineEinheitInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, _ = ersteEinheit.modelle
    stelle = stelleDesErstenModells(aufstellung, zweiterSpieler, ersteEinheit)
    for modell, stelleDesModells in stellenDerEinheit(aufstellung, zweiterSpieler, ersteEinheit):
        aufstellung.modellSetzen(modell, stelleDesModells)

    aufstellung.aufstellenDerEinheitBeenden()

    assert aufstellung.gesetzt(erstesModell)
    assert aufstellung.stelle(erstesModell) == stelle
    assert aufstellung.einheitInAufstellung is None


def testAuf1_9EinModellEinerAufgestelltenEinheitIstNichtWählbar():
    kleinerSpieler, größererSpieler = spielerMit(1), spielerMit(1, 1)
    aufstellung = aufstellungVon(kleinerSpieler, größererSpieler)
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=größererSpieler)
    (einheitDesKleineren,) = kleinerSpieler.armee.einheiten
    aufgestellteEinheit, _ = größererSpieler.armee.einheiten
    aufgestelltesModell, *_ = aufgestellteEinheit.modelle
    einheitAufstellen(aufstellung, einheitDesKleineren)
    einheitAufstellen(aufstellung, aufgestellteEinheit)
    stelleBeimAufstellen = aufstellung.stelle(aufgestelltesModell)

    gründe = sperrgründe(aufstellung.modellSetzen, aufgestelltesModell, irgendeineStelle)

    assert aufstellung.anDerReihe is größererSpieler
    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.stelle(aufgestelltesModell) == stelleBeimAufstellen
    assert aufstellung.einheitInAufstellung is None


def testAuf1_9EinModellDesSpielersNichtAnDerReiheIstNichtWählbar(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheitDesAnderenSpielers, _ = ersterSpieler.armee.einheiten
    modellDesAnderenSpielers, *_ = einheitDesAnderenSpielers.modelle

    gründe = sperrgründe(aufstellung.modellSetzen, modellDesAnderenSpielers, irgendeineStelle)

    assert aufstellung.anDerReihe is zweiterSpieler
    assert gründe == {Grund.nichtWählbar}
    assert not aufstellung.gesetzt(modellDesAnderenSpielers)
    assert aufstellung.einheitInAufstellung is None


def testAuf1_9VorDerWahlIstJedesModellNichtWählbar(aufstellung, ersterSpieler):
    ersteEinheit, _ = ersterSpieler.armee.einheiten
    erstesModell, *_ = ersteEinheit.modelle

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, irgendeineStelle)

    assert gründe == {Grund.nichtWählbar}
    assert not aufstellung.gesetzt(erstesModell)
    assert aufstellung.einheitInAufstellung is None


def testAuf1_9NachDerAufstellungIstJedesModellNichtWählbar():
    ersterSpieler, zweiterSpieler = spielerMit(1), spielerMit(1)
    aufstellung = aufstellungVon(ersterSpieler, zweiterSpieler)
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    (einheitDesErsten,) = ersterSpieler.armee.einheiten
    (einheitDesZweiten,) = zweiterSpieler.armee.einheiten
    modellDesErsten, *_ = einheitDesErsten.modelle
    modellDesZweiten, *_ = einheitDesZweiten.modelle
    einheitAufstellen(aufstellung, einheitDesZweiten)
    einheitAufstellen(aufstellung, einheitDesErsten)

    gründeDesErsten = sperrgründe(aufstellung.modellSetzen, modellDesErsten, irgendeineStelle)
    gründeDesZweiten = sperrgründe(aufstellung.modellSetzen, modellDesZweiten, irgendeineStelle)

    assert aufstellung.beendet
    assert gründeDesErsten == {Grund.nichtWählbar}
    assert gründeDesZweiten == {Grund.nichtWählbar}


def testAuf1_9GegenEinModellDesSpielersNichtAnDerReiheGiltNichtWählbarAuchBeiBegonnenerEinheit(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, _ = begonneneEinheit.modelle
    einheitDesAnderenSpielers, _ = ersterSpieler.armee.einheiten
    modellDesAnderenSpielers, *_ = einheitDesAnderenSpielers.modelle
    stelle = stelleDesErstenModells(aufstellung, zweiterSpieler, begonneneEinheit)
    aufstellung.modellSetzen(erstesModell, stelle)

    gründe = sperrgründe(aufstellung.modellSetzen, modellDesAnderenSpielers, irgendeineStelle)

    assert gründe == {Grund.nichtWählbar}
    assert not aufstellung.gesetzt(modellDesAnderenSpielers)
    assert aufstellung.einheitInAufstellung is begonneneEinheit


def testAuf1_10EinModellEinerAnderenEinheitIstEinheitBegonnen(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, andereEinheit = zweiterSpieler.armee.einheiten
    erstesModell, _ = begonneneEinheit.modelle
    modellDerAnderenEinheit, *_ = andereEinheit.modelle
    stelle = stelleDesErstenModells(aufstellung, zweiterSpieler, begonneneEinheit)
    stelleDerAnderenEinheit = stelleDesErstenModells(aufstellung, zweiterSpieler, andereEinheit)
    aufstellung.modellSetzen(erstesModell, stelle)

    gründe = sperrgründe(aufstellung.modellSetzen, modellDerAnderenEinheit, stelleDerAnderenEinheit)

    assert gründe == {Grund.einheitBegonnen}
    assert not aufstellung.gesetzt(modellDerAnderenEinheit)
    assert aufstellung.einheitInAufstellung is begonneneEinheit


def testAuf1_10EinWeiteresModellDerEinheitInAufstellungSperrtNicht(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, _ = zweiterSpieler.armee.einheiten
    (erstesModell, ersteStelle), (zweitesModell, zweiteStelle) = stellenDerEinheit(
        aufstellung, zweiterSpieler, begonneneEinheit
    )
    aufstellung.modellSetzen(erstesModell, ersteStelle)

    aufstellung.modellSetzen(zweitesModell, zweiteStelle)

    assert aufstellung.gesetzt(zweitesModell)
    assert aufstellung.einheitInAufstellung is begonneneEinheit


def testAuf1_10NachDemBeendenSperrtEinModellDerNächstenEinheitDesselbenSpielersNicht():
    kleinerSpieler, größererSpieler = spielerMit(1), spielerMit(1, 1)
    aufstellung = aufstellungVon(kleinerSpieler, größererSpieler)
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=größererSpieler)
    (einheitDesKleineren,) = kleinerSpieler.armee.einheiten
    ersteEinheit, zweiteEinheit = größererSpieler.armee.einheiten
    modellDerZweitenEinheit, *_ = zweiteEinheit.modelle
    stelle = stelleDesErstenModells(aufstellung, größererSpieler, zweiteEinheit)
    einheitAufstellen(aufstellung, einheitDesKleineren)
    einheitAufstellen(aufstellung, ersteEinheit)

    aufstellung.modellSetzen(modellDerZweitenEinheit, stelle)

    assert aufstellung.einheitInAufstellung is zweiteEinheit


def testAuf1_11OhneEinheitInAufstellungIstBeendenNichtInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.nichtInAufstellung}
    assert aufstellung.anDerReihe is zweiterSpieler


def testAuf1_11VorDerWahlIstBeendenNichtInAufstellung(aufstellung):
    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.nichtInAufstellung}
    assert aufstellung.anDerReihe is None
    assert not aufstellung.beendet


def testAuf1_11NachDemBeendenGibtEsKeineEinheitZumErneutenBeenden(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    einheitAufstellen(aufstellung, ersteEinheit)

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.nichtInAufstellung}
    assert aufstellung.anDerReihe is ersterSpieler


def testAuf1_11EinGesperrtesSetzenMachtKeineEinheitZumBeenden(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, _ = ersteEinheit.modelle
    sperrgründe(aufstellung.modellSetzen, erstesModell, stelleInZone(ersteZone, 1, 3))

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.nichtInAufstellung}
    assert aufstellung.anDerReihe is zweiterSpieler
