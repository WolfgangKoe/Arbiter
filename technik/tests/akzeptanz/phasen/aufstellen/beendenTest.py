"""AUF-10 · Aufstellen der Einheit beenden."""

from fractions import Fraction
from http import HTTPStatus

from playwright.sync_api import Route, expect

from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    knopfDerSeite,
    sperrmeldungWarten,
    spielerAnDerReihe,
)
from tests.akzeptanz.dienst import (
    abwählen,
    aufstellenDerEinheitBeenden,
    dienstFür,
    modellLoslassen,
    sperreDesVertrags,
)
from tests.akzeptanz.handgriffe import (
    modelleSetzen,
    nachDerWahlDerAufstellungszone,
    sperrgründe,
    stelleInDerZoneVon,
    stellenDerEinheit,
)


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


def testAuf10_3DerDienstSperrtDasBeendenMitDemBeispielDesVertrags(
    dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors
):
    abwählen(dienstDesBeispiels, "Necron Warriors")
    _, _, drittes, *_ = necronWarriors.modelle
    stelleDesBeispiels = Stelle(x=Fraction(42), y=Fraction(28))
    modellLoslassen(
        dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors, drittes, stelleDesBeispiels
    )

    antwort = aufstellenDerEinheitBeenden(dienstDesBeispiels)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json() == sperreDesVertrags()


def antwortMitDerSperreDesVertrags(anfrage: Route) -> None:
    anfrage.fulfill(status=HTTPStatus.CONFLICT, json=sperreDesVertrags())


def testAuf10_3DieSeiteNenntBeimBeendenDenGrundDerSperreImBeispiel(bildschirm, ausgangsaufstellung):
    stand = sperreDesVertrags()["spielstand"]
    seite = bildschirm.seiteMitSpielstand(ausgangsaufstellung, stand)
    seite.route("**/api/aufstellenDerEinheitBeenden", antwortMitDerSperreDesVertrags)
    knopf = knopfDerSeite(seite, "Aufstellen der Einheit beenden")

    with aufDieHandlungWarten(seite):
        knopf.click()

    assert sperrmeldungWarten(seite, {Grund.keineKohärenz}) == frozenset(
        sperreDesVertrags()["gründe"]
    )
