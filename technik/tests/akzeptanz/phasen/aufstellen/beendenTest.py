"""AUF-10 · Aufstellen der Einheit beenden."""

from http import HTTPStatus

from playwright.sync_api import expect

from arbiter.domaene.sperre import Grund
from tests.akzeptanz.bildschirm import aufDieHandlungWarten, knopfDerSeite, spielerAnDerReihe
from tests.akzeptanz.dienst import aufstellenDerEinheitBeenden, dienstFür
from tests.akzeptanz.handgriffe import (
    aufstellungVon,
    modelleSetzen,
    nachDerWahlDerAufstellungszone,
    sperrgründe,
    spielerMit,
    stelleInDerZoneVon,
    stellenDerEinheit,
)


def aufstellungMitEinerEinheitAusDreiModellen():
    anderer, beginner = spielerMit(1), spielerMit(3)
    aufstellung = aufstellungVon(anderer, beginner)
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=anderer)
    (einheit,) = beginner.armee.einheiten
    return aufstellung, beginner, einheit


def testAuf10_1EineEinheitInKohärenzMitAllenGesetztenModellenIstNachDemBeendenAufgestellt(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    for modell, stelle in stellenDerEinheit(aufstellung, zweiterSpieler, einheit):
        aufstellung.modellSetzen(modell, stelle)

    aufstellung.aufstellenDerEinheitBeenden()

    assert aufstellung.aufgestellt(einheit)
    assert aufstellung.anDerReihe is ersterSpieler
    assert aufstellung.einheitInAufstellung is None


def testAuf10_1EinKlickAufAufstellenDerEinheitBeendenWähltAufstellenDerEinheitBeenden(
    bildschirm, aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    modelleSetzen(aufstellung, einheit, len(einheit.modelle))
    seite = bildschirm.seiteZu(aufstellung)
    knopf = knopfDerSeite(seite, "Aufstellen der Einheit beenden")

    with aufDieHandlungWarten(seite):
        knopf.click()

    assert aufstellung.aufgestellt(einheit)
    assert aufstellung.anDerReihe is ersterSpieler
    assert aufstellung.einheitInAufstellung is None
    expect(spielerAnDerReihe(seite)).to_contain_text("Spieler 1")


def testAuf10_1DieAnfrageAufstellenDerEinheitBeendenWähltAufstellenDerEinheitBeenden(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    modelleSetzen(aufstellung, einheit, len(einheit.modelle))
    dienst = dienstFür(aufstellung)

    antwort = aufstellenDerEinheitBeenden(dienst)

    assert antwort.status_code == HTTPStatus.OK
    assert aufstellung.aufgestellt(einheit)
    assert aufstellung.anDerReihe is ersterSpieler
    spielerImStand = antwort.get_json()["spieler"]
    namenAnDerReihe = [spieler["name"] for spieler in spielerImStand if spieler["anDerReihe"]]
    assert namenAnDerReihe == ["Spieler 1"]


def testAuf10_2EinNichtGesetztesModellSperrtDasBeendenMitModelleFehlen(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, _ = einheit.modelle
    aufstellung.modellSetzen(erstesModell, stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 20))

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.modelleFehlen}
    assert not aufstellung.aufgestellt(einheit)
    assert aufstellung.einheitInAufstellung is einheit
    assert aufstellung.anDerReihe is zweiterSpieler


def testAuf10_3EineEinheitNichtInKohärenzSperrtDasBeendenMitKeineKohärenz(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, zweitesModell = einheit.modelle
    aufstellung.modellSetzen(erstesModell, stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 10))
    aufstellung.modellSetzen(zweitesModell, stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 30))

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.keineKohärenz}
    assert not aufstellung.aufgestellt(einheit)
    assert aufstellung.einheitInAufstellung is einheit
    assert aufstellung.anDerReihe is zweiterSpieler


def testAuf10_4ZweiSperrenZugleichNenntArbiterBeideGründe():
    aufstellung, beginner, einheit = aufstellungMitEinerEinheitAusDreiModellen()
    erstesModell, zweitesModell, _ = einheit.modelle
    aufstellung.modellSetzen(erstesModell, stelleInDerZoneVon(aufstellung, beginner, 4, 10))
    aufstellung.modellSetzen(zweitesModell, stelleInDerZoneVon(aufstellung, beginner, 4, 30))

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.modelleFehlen, Grund.keineKohärenz}
    assert not aufstellung.aufgestellt(einheit)
