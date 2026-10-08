"""AUF-7 · Einheit in Aufstellung."""

from fractions import Fraction

from arbiter.domaene.phasen.aufstellen import Aufstellungszone
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.handgriffe import (
    aufstellungVon,
    einheitAufstellen,
    nachDerWahlDerAufstellungszone,
    sperrgründe,
    spielerMit,
    stelleDesErstenModells,
    stelleInZone,
    stellenDerEinheit,
)

ersteZone, zweiteZone = list(Aufstellungszone)
# Warum: Gesperrt wird vor jeder Prüfung der Stelle (AUF-3.8), welche Stelle ist gleich.
irgendeineStelle = Stelle(x=Fraction(3, 2), y=Fraction(1))
# Warum: Der Spieler an der Reihe ist der zweite, die erste Zone gehört dem anderen.
stelleInDerZoneDesAnderenSpielers = stelleInZone(ersteZone, Fraction(3, 2), Fraction(3))


def testAuf7_1VorDemSetzenEinesModellsIstKeineEinheitInAufstellung(aufstellung, ersterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)

    assert aufstellung.einheitInAufstellung is None


def testAuf7_1VorDerWahlIstKeineEinheitInAufstellung(aufstellung):
    assert aufstellung.einheitInAufstellung is None


def testAuf7_1MitDemErstenGesetztenModellIstDieEinheitDieEinheitInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, _ = ersteEinheit.modelle
    stelle = stelleDesErstenModells(aufstellung, zweiterSpieler, ersteEinheit)

    aufstellung.modellSetzen(erstesModell, stelle)

    assert aufstellung.einheitInAufstellung is ersteEinheit


def testAuf7_1MitWeiterenGesetztenModellenBleibtDieEinheitEinheitInAufstellung(
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


def testAuf7_1EinGesperrtesSetzenMachtDieEinheitNichtZurEinheitInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, _ = ersteEinheit.modelle

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, stelleInDerZoneDesAnderenSpielers)

    assert gründe == {Grund.nichtGanzInDerZone}
    assert aufstellung.einheitInAufstellung is None


def testAuf7_1NachDemBeendenIstDieAufgestellteEinheitKeineEinheitInAufstellung(
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


def testAuf7_2EinModellEinerAufgestelltenEinheitIstNichtWählbar():
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


def testAuf7_2EinModellDesSpielersNichtAnDerReiheIstNichtWählbar(
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


def testAuf7_2VorDerWahlIstJedesModellNichtWählbar(aufstellung, ersterSpieler):
    ersteEinheit, _ = ersterSpieler.armee.einheiten
    erstesModell, *_ = ersteEinheit.modelle

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, irgendeineStelle)

    assert gründe == {Grund.nichtWählbar}
    assert not aufstellung.gesetzt(erstesModell)
    assert aufstellung.einheitInAufstellung is None


def testAuf7_2NachDerAufstellungIstJedesModellNichtWählbar():
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


def testAuf7_2EinModellEinerAufgestelltenEinheitIstNichtWählbarAuchBeiBegonnenerEinheit():
    ersterSpieler, zweiterSpieler = spielerMit(1), spielerMit(1, 1, 1)
    aufstellung = aufstellungVon(ersterSpieler, zweiterSpieler)
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    (einheitDesErsten,) = ersterSpieler.armee.einheiten
    aufgestellteEinheit, begonneneEinheit, _ = zweiterSpieler.armee.einheiten
    aufgestelltesModell, *_ = aufgestellteEinheit.modelle
    begonnenesModell, *_ = begonneneEinheit.modelle
    einheitAufstellen(aufstellung, aufgestellteEinheit)
    einheitAufstellen(aufstellung, einheitDesErsten)
    stelleBeimAufstellen = aufstellung.stelle(aufgestelltesModell)
    stelleDerBegonnenen = stelleDesErstenModells(aufstellung, zweiterSpieler, begonneneEinheit)
    aufstellung.modellSetzen(begonnenesModell, stelleDerBegonnenen)

    gründe = sperrgründe(aufstellung.modellSetzen, aufgestelltesModell, irgendeineStelle)

    assert aufstellung.anDerReihe is zweiterSpieler
    assert gründe == {Grund.nichtWählbar}
    assert aufstellung.stelle(aufgestelltesModell) == stelleBeimAufstellen
    assert aufstellung.einheitInAufstellung is begonneneEinheit


def testAuf7_2GegenEinModellDesSpielersNichtAnDerReiheGiltNichtWählbarAuchBeiBegonnenerEinheit(
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


def testAuf7_3EinModellEinerAnderenEinheitIstEinheitBegonnen(
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


def testAuf7_3EinWeiteresModellDerEinheitInAufstellungSperrtNicht(
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


def testAuf7_3NachDemBeendenSperrtEinModellDerNächstenEinheitDesselbenSpielersNicht():
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


def testAuf7_4OhneEinheitInAufstellungIstBeendenNichtInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.nichtInAufstellung}
    assert aufstellung.anDerReihe is zweiterSpieler


def testAuf7_4VorDerWahlIstBeendenNichtInAufstellung(aufstellung):
    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.nichtInAufstellung}
    assert aufstellung.anDerReihe is None
    assert not aufstellung.beendet


def testAuf7_4NachDemBeendenGibtEsKeineEinheitZumErneutenBeenden(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    einheitAufstellen(aufstellung, ersteEinheit)

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.nichtInAufstellung}
    assert aufstellung.anDerReihe is ersterSpieler


def testAuf7_4EinGesperrtesSetzenMachtKeineEinheitZumBeenden(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, _ = ersteEinheit.modelle
    sperrgründe(aufstellung.modellSetzen, erstesModell, stelleInDerZoneDesAnderenSpielers)

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.nichtInAufstellung}
    assert aufstellung.anDerReihe is zweiterSpieler
