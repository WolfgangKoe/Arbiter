"""AUF-1 · Reihenfolge der Aufstellung."""

import pytest
from arbiter.domaene.armeen import Einheit, Spieler
from arbiter.domaene.aufstellung import Aufstellung, Aufstellungszone, Grund, Sperre

ersteZone, zweiteZone = list(Aufstellungszone)


def nachDerWahl(aufstellung: Aufstellung, gewinner: Spieler) -> None:
    aufstellung.gewinnerWählen(gewinner)
    aufstellung.aufstellungszoneWählen(ersteZone)


def einheitAufstellen(aufstellung: Aufstellung, einheit: Einheit) -> None:
    aufstellung.einheitInAufstellungWählen(einheit)
    for modell in einheit.modelle:
        aufstellung.modellSetzen(modell)
    aufstellung.aufstellenDerEinheitBeenden()


def reihenfolgeBeimAufstellen(aufstellung: Aufstellung, einheiten: list[Einheit]) -> list[Spieler]:
    reihenfolge = []
    for einheit in einheiten:
        reihenfolge.append(aufstellung.anDerReihe)
        einheitAufstellen(aufstellung, einheit)
    return reihenfolge


def sperrgrund(handlung, *argumente) -> Grund:
    with pytest.raises(Sperre) as sperre:
        handlung(*argumente)
    return sperre.value.grund


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


def testAuf1_2ErstDerGewinnerDannDieAufstellungszoneIstErlaubt(aufstellung, ersterSpieler):
    aufstellung.gewinnerWählen(ersterSpieler)

    aufstellung.aufstellungszoneWählen(ersteZone)

    assert aufstellung.aufstellungszone(ersterSpieler) == ersteZone


def testAuf1_2DieAufstellungszoneVorDemGewinnerIstNichtWählbar(aufstellung):
    grund = sperrgrund(aufstellung.aufstellungszoneWählen, ersteZone)

    assert grund is Grund.nichtWählbar


def testAuf1_2NachDerGesperrtenZoneIstDerGewinnerNochWählbar(aufstellung, ersterSpieler):
    sperrgrund(aufstellung.aufstellungszoneWählen, ersteZone)

    aufstellung.gewinnerWählen(ersterSpieler)

    assert aufstellung.gewinner is ersterSpieler


def testAuf1_2DerGewinnerEinZweitesMalIstNichtWählbar(
    aufstellung, ersterSpieler, zweiterSpieler
):
    aufstellung.gewinnerWählen(ersterSpieler)

    grund = sperrgrund(aufstellung.gewinnerWählen, zweiterSpieler)

    assert grund is Grund.nichtWählbar
    assert aufstellung.gewinner is ersterSpieler


def testAuf1_2DerselbeGewinnerEinZweitesMalIstNichtWählbar(aufstellung, ersterSpieler):
    aufstellung.gewinnerWählen(ersterSpieler)

    grund = sperrgrund(aufstellung.gewinnerWählen, ersterSpieler)

    assert grund is Grund.nichtWählbar
    assert aufstellung.gewinner is ersterSpieler


@pytest.mark.parametrize("zweiteWahl", list(Aufstellungszone))
def testAuf1_2DieAufstellungszoneEinZweitesMalIstNichtWählbar(
    aufstellung, ersterSpieler, zweiteWahl
):
    aufstellung.gewinnerWählen(ersterSpieler)
    aufstellung.aufstellungszoneWählen(ersteZone)

    grund = sperrgrund(aufstellung.aufstellungszoneWählen, zweiteWahl)

    assert grund is Grund.nichtWählbar
    assert aufstellung.aufstellungszone(ersterSpieler) == ersteZone


def testAuf1_3VorDerWahlIstKeinerAnDerReihe(aufstellung):
    assert aufstellung.anDerReihe is None


def testAuf1_3NachDerWahlIstAnDerReiheWerNichtGewinnerIst(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)

    assert aufstellung.anDerReihe is zweiterSpieler


def testAuf1_3IstDerZweiteSpielerGewinnerIstDerErsteAnDerReihe(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=zweiterSpieler)

    assert aufstellung.anDerReihe is ersterSpieler


def testAuf1_4EinModellDerEinheitInAufstellungLässtSichSetzen(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, *_ = ersteEinheit.modelle
    aufstellung.einheitInAufstellungWählen(ersteEinheit)

    aufstellung.modellSetzen(erstesModell)

    assert erstesModell.gesetzt


def testAuf1_4OhneEinheitInAufstellungIstSetzenNichtInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, *_ = ersteEinheit.modelle

    grund = sperrgrund(aufstellung.modellSetzen, erstesModell)

    assert grund is Grund.nichtInAufstellung
    assert not erstesModell.gesetzt


def testAuf1_4VorDerWahlIstSetzenNichtInAufstellung(aufstellung, ersterSpieler):
    ersteEinheit, _ = ersterSpieler.armee.einheiten
    erstesModell, *_ = ersteEinheit.modelle

    grund = sperrgrund(aufstellung.modellSetzen, erstesModell)

    assert grund is Grund.nichtInAufstellung


def testAuf1_4EinModellEinerAnderenEinheitIstNichtInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    einheitInAufstellung, andereEinheit = zweiterSpieler.armee.einheiten
    modellDerAnderenEinheit, *_ = andereEinheit.modelle
    aufstellung.einheitInAufstellungWählen(einheitInAufstellung)

    grund = sperrgrund(aufstellung.modellSetzen, modellDerAnderenEinheit)

    assert grund is Grund.nichtInAufstellung
    assert not modellDerAnderenEinheit.gesetzt


def testAuf1_4EinModellDesGegnersIstNichtInAufstellung(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    einheitInAufstellung, _ = zweiterSpieler.armee.einheiten
    gegnerischeEinheit, _ = ersterSpieler.armee.einheiten
    gegnerischesModell, *_ = gegnerischeEinheit.modelle
    aufstellung.einheitInAufstellungWählen(einheitInAufstellung)

    grund = sperrgrund(aufstellung.modellSetzen, gegnerischesModell)

    assert grund is Grund.nichtInAufstellung
    assert not gegnerischesModell.gesetzt


def testAuf1_4OhneEinheitInAufstellungIstBeendenNichtInAufstellung(aufstellung, ersterSpieler):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)

    grund = sperrgrund(aufstellung.aufstellenDerEinheitBeenden)

    assert grund is Grund.nichtInAufstellung


def testAuf1_4VorDerWahlIstBeendenNichtInAufstellung(aufstellung):
    grund = sperrgrund(aufstellung.aufstellenDerEinheitBeenden)

    assert grund is Grund.nichtInAufstellung


def testAuf1_4NachDemBeendenGibtEsKeineEinheitZumErneutenBeenden(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    einheitAufstellen(aufstellung, ersteEinheit)

    grund = sperrgrund(aufstellung.aufstellenDerEinheitBeenden)

    assert grund is Grund.nichtInAufstellung


def testAuf1_5EineNichtAufgestellteEinheitDesSpielersAnDerReiheIstWählbar(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    _, zweiteEinheit = zweiterSpieler.armee.einheiten

    aufstellung.einheitInAufstellungWählen(zweiteEinheit)

    assert aufstellung.einheitInAufstellung is zweiteEinheit


def testAuf1_5VorDerWahlIstKeineEinheitWählbar(aufstellung, ersterSpieler):
    ersteEinheit, _ = ersterSpieler.armee.einheiten

    grund = sperrgrund(aufstellung.einheitInAufstellungWählen, ersteEinheit)

    assert grund is Grund.nichtWählbar
    assert aufstellung.einheitInAufstellung is None


def testAuf1_5EineEinheitDesSpielersNichtAnDerReiheIstNichtWählbar(aufstellung, ersterSpieler):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = ersterSpieler.armee.einheiten

    grund = sperrgrund(aufstellung.einheitInAufstellungWählen, ersteEinheit)

    assert grund is Grund.nichtWählbar
    assert aufstellung.einheitInAufstellung is None


def testAuf1_5EineAufgestellteEinheitIstNichtWählbar(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    aufgestellteEinheit, _ = zweiterSpieler.armee.einheiten
    einheitDesGegners, _ = ersterSpieler.armee.einheiten
    einheitAufstellen(aufstellung, aufgestellteEinheit)
    einheitAufstellen(aufstellung, einheitDesGegners)

    grund = sperrgrund(aufstellung.einheitInAufstellungWählen, aufgestellteEinheit)

    assert grund is Grund.nichtWählbar
    assert aufstellung.einheitInAufstellung is None


@pytest.mark.parametrize(
    "gewählteEinheit",
    ["ersteEinheitErster", "zweiteEinheitErster", "ersteEinheitZweiter", "zweiteEinheitZweiter"],
)
def testAuf1_5NachDerAufstellungIstKeineEinheitWählbar(
    aufstellung, ersterSpieler, zweiterSpieler, gewählteEinheit
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    ersteEinheitErster, zweiteEinheitErster = ersterSpieler.armee.einheiten
    ersteEinheitZweiter, zweiteEinheitZweiter = zweiterSpieler.armee.einheiten
    einheitAufstellen(aufstellung, ersteEinheitZweiter)
    einheitAufstellen(aufstellung, ersteEinheitErster)
    einheitAufstellen(aufstellung, zweiteEinheitZweiter)
    einheitAufstellen(aufstellung, zweiteEinheitErster)
    einheiten = {
        "ersteEinheitErster": ersteEinheitErster,
        "zweiteEinheitErster": zweiteEinheitErster,
        "ersteEinheitZweiter": ersteEinheitZweiter,
        "zweiteEinheitZweiter": zweiteEinheitZweiter,
    }

    grund = sperrgrund(aufstellung.einheitInAufstellungWählen, einheiten[gewählteEinheit])

    assert grund is Grund.nichtWählbar


def testAuf1_5GegenEineNichtWählbareEinheitGiltNichtWählbarAuchNachBegonnenerEinheit(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, *_ = begonneneEinheit.modelle
    einheitDesGegners, _ = ersterSpieler.armee.einheiten
    aufstellung.einheitInAufstellungWählen(begonneneEinheit)
    aufstellung.modellSetzen(erstesModell)

    grund = sperrgrund(aufstellung.einheitInAufstellungWählen, einheitDesGegners)

    assert grund is Grund.nichtWählbar


def testAuf1_6OhneGesetztesModellLöstDieWählbareEinheitDieBisherigeAb(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    bisherigeEinheit, wählbareEinheit = zweiterSpieler.armee.einheiten
    aufstellung.einheitInAufstellungWählen(bisherigeEinheit)

    aufstellung.einheitInAufstellungWählen(wählbareEinheit)

    assert aufstellung.einheitInAufstellung is wählbareEinheit


def testAuf1_6MitGesetztemModellIstDieEinheitBegonnen(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, andereEinheit = zweiterSpieler.armee.einheiten
    erstesModell, *_ = begonneneEinheit.modelle
    aufstellung.einheitInAufstellungWählen(begonneneEinheit)
    aufstellung.modellSetzen(erstesModell)

    grund = sperrgrund(aufstellung.einheitInAufstellungWählen, andereEinheit)

    assert grund is Grund.einheitBegonnen
    assert aufstellung.einheitInAufstellung is begonneneEinheit


def testAuf1_6DieBegonneneEinheitErneutZuWählenIstNichtGesperrt(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, *_ = begonneneEinheit.modelle
    aufstellung.einheitInAufstellungWählen(begonneneEinheit)
    aufstellung.modellSetzen(erstesModell)

    aufstellung.einheitInAufstellungWählen(begonneneEinheit)

    assert aufstellung.einheitInAufstellung is begonneneEinheit


def testAuf1_7NachDemBeendenIstDieEinheitAufgestelltUndKeineInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, zweiteEinheit = zweiterSpieler.armee.einheiten
    aufstellung.einheitInAufstellungWählen(ersteEinheit)
    for modell in ersteEinheit.modelle:
        aufstellung.modellSetzen(modell)

    aufstellung.aufstellenDerEinheitBeenden()

    assert ersteEinheit.aufgestellt
    assert aufstellung.einheitInAufstellung is None
    assert not zweiteEinheit.aufgestellt


def testAuf1_7NachDemBeendenIstDerAndereSpielerAnDerReihe(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    ersteEinheit, _ = zweiterSpieler.armee.einheiten
    aufstellung.einheitInAufstellungWählen(ersteEinheit)
    for modell in ersteEinheit.modelle:
        aufstellung.modellSetzen(modell)

    aufstellung.aufstellenDerEinheitBeenden()

    assert aufstellung.anDerReihe is ersterSpieler


def testAuf1_7DieSpielerStellenAbwechselndAuf(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)
    ersteEinheitErster, zweiteEinheitErster = ersterSpieler.armee.einheiten
    ersteEinheitZweiter, zweiteEinheitZweiter = zweiterSpieler.armee.einheiten
    einheiten = [
        ersteEinheitZweiter, ersteEinheitErster, zweiteEinheitZweiter, zweiteEinheitErster
    ]

    reihenfolge = reihenfolgeBeimAufstellen(aufstellung, einheiten)

    assert reihenfolge == [zweiterSpieler, ersterSpieler, zweiterSpieler, ersterSpieler]


def testAuf1_7HatDerAndereAlleEinheitenAufgestelltIstDerselbeWiederAnDerReihe(
    spielerMitEinheiten,
):
    kleinerSpieler, größererSpieler = spielerMitEinheiten(1), spielerMitEinheiten(1, 1, 1)
    aufstellung = Aufstellung(kleinerSpieler, größererSpieler)
    nachDerWahl(aufstellung, gewinner=größererSpieler)
    (einheitDesKleineren,) = kleinerSpieler.armee.einheiten

    einheitAufstellen(aufstellung, einheitDesKleineren)

    assert aufstellung.anDerReihe is größererSpieler


def testAuf1_7DerselbeSpielerBleibtNachSeinerErstenEinheitAnDerReihe(spielerMitEinheiten):
    kleinerSpieler, größererSpieler = spielerMitEinheiten(1), spielerMitEinheiten(1, 1, 1)
    aufstellung = Aufstellung(kleinerSpieler, größererSpieler)
    nachDerWahl(aufstellung, gewinner=größererSpieler)
    (einheitDesKleineren,) = kleinerSpieler.armee.einheiten
    ersteEinheit, _, _ = größererSpieler.armee.einheiten
    einheitAufstellen(aufstellung, einheitDesKleineren)

    einheitAufstellen(aufstellung, ersteEinheit)

    assert aufstellung.anDerReihe is größererSpieler


def testAuf1_7DerselbeSpielerBleibtNachSeinerZweitenEinheitAnDerReihe(spielerMitEinheiten):
    kleinerSpieler, größererSpieler = spielerMitEinheiten(1), spielerMitEinheiten(1, 1, 1)
    aufstellung = Aufstellung(kleinerSpieler, größererSpieler)
    nachDerWahl(aufstellung, gewinner=größererSpieler)
    (einheitDesKleineren,) = kleinerSpieler.armee.einheiten
    ersteEinheit, zweiteEinheit, _ = größererSpieler.armee.einheiten
    einheitAufstellen(aufstellung, einheitDesKleineren)
    einheitAufstellen(aufstellung, ersteEinheit)

    einheitAufstellen(aufstellung, zweiteEinheit)

    assert aufstellung.anDerReihe is größererSpieler


def testAuf1_7HabenBeideAlleEinheitenAufgestelltIstDieAufstellungBeendet(spielerMitEinheiten):
    kleinerSpieler, größererSpieler = spielerMitEinheiten(1), spielerMitEinheiten(1, 1)
    aufstellung = Aufstellung(kleinerSpieler, größererSpieler)
    nachDerWahl(aufstellung, gewinner=größererSpieler)
    (einheitDesKleineren,) = kleinerSpieler.armee.einheiten
    ersteEinheit, zweiteEinheit = größererSpieler.armee.einheiten
    einheitAufstellen(aufstellung, einheitDesKleineren)
    einheitAufstellen(aufstellung, ersteEinheit)

    einheitAufstellen(aufstellung, zweiteEinheit)

    assert aufstellung.beendet
    assert aufstellung.anDerReihe is None
    assert aufstellung.einheitInAufstellung is None


def testAuf1_7FehltNochEineEinheitIstDieAufstellungNichtBeendet(spielerMitEinheiten):
    kleinerSpieler, größererSpieler = spielerMitEinheiten(1), spielerMitEinheiten(1, 1)
    aufstellung = Aufstellung(kleinerSpieler, größererSpieler)
    nachDerWahl(aufstellung, gewinner=größererSpieler)
    (einheitDesKleineren,) = kleinerSpieler.armee.einheiten
    ersteEinheit, _ = größererSpieler.armee.einheiten
    einheitAufstellen(aufstellung, einheitDesKleineren)

    einheitAufstellen(aufstellung, ersteEinheit)

    assert not aufstellung.beendet


def testAuf1_7VorDerWahlIstDieAufstellungNichtBeendet(aufstellung):
    assert not aufstellung.beendet


def testAuf1_7NachDerWahlIstDieAufstellungNichtBeendet(aufstellung, ersterSpieler):
    nachDerWahl(aufstellung, gewinner=ersterSpieler)

    assert not aufstellung.beendet
