"""AUF-12 · Sperre ohne Stelle."""

from fractions import Fraction
from http import HTTPStatus

import pytest

from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.bildschirm import (
    gründeAlsText,
    klickenUndWarten,
    knopfDerSeite,
    sperrmeldungWarten,
)
from tests.akzeptanz.dienst import (
    aufstellenDerEinheitBeenden,
    auswählen,
    dienstFür,
    modellLoslassen,
    sperreDesVertrags,
    spielstandVon,
    stellenDesVertrags,
)
from tests.akzeptanz.handgriffe import (
    einGesperrtesModell,
    einheitAufstellen,
    modelleSetzen,
    nachDerWahlDerAufstellungszone,
    sperrgründe,
    stelleInDerZoneVon,
    stellenAllerModelle,
)
from tests.akzeptanz.ziehen import aufDieHandlungWarten, einheitZiehen

beenden = "Aufstellen der Einheit beenden"


def ohneEinheitInAufstellung(aufstellung):
    """Nichts gesetzt: AUF-7.4."""


def mitFehlendemModell(aufstellung):
    spieler = aufstellung.anDerReihe
    einheit, _ = spieler.armee.einheiten
    erstesModell, _ = einheit.modelle
    aufstellung.modellSetzen(erstesModell, stelleInDerZoneVon(aufstellung, spieler, 4, 20))


def ohneKohärenz(aufstellung):
    spieler = aufstellung.anDerReihe
    einheit, _ = spieler.armee.einheiten
    erstesModell, zweitesModell = einheit.modelle
    aufstellung.modellSetzen(erstesModell, stelleInDerZoneVon(aufstellung, spieler, 4, 10))
    aufstellung.modellSetzen(zweitesModell, stelleInDerZoneVon(aufstellung, spieler, 4, 30))


sperrenBeimBeenden = pytest.mark.parametrize(
    ("aufbau", "grund"),
    [
        (ohneEinheitInAufstellung, Grund.nichtInAufstellung),
        (mitFehlendemModell, Grund.modelleFehlen),
        (ohneKohärenz, Grund.keineKohärenz),
    ],
    ids=["nichtInAufstellung", "modelleFehlen", "keineKohärenz"],
)


def testAuf12_1DieAntwortDesDienstesAufDasBeendenBeiGesperrtemModellGleichtDemBeispielDesVertrags(
    dienstDesBeispiels, aufstellungDesBeispiels, necronWarriors
):
    auswählen(dienstDesBeispiels, "Warboss")
    auswählen(dienstDesBeispiels, "Necron Warriors")
    _, _, stelleDesDrittenModells = stellenDesVertrags(2)
    _, _, _, viertesModell, *_ = necronWarriors.modelle
    modellLoslassen(
        dienstDesBeispiels,
        aufstellungDesBeispiels,
        necronWarriors,
        viertesModell,
        stelleDesDrittenModells,
    )

    antwort = aufstellenDerEinheitBeenden(dienstDesBeispiels)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json() == sperreDesVertrags()


def testAuf12_1EinGesperrtesModellSperrtDasSetzenMitDemGrundModellGesperrt(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einGesperrtesModell(aufstellung, zweiterSpieler)
    _, zweiteEinheit = zweiterSpieler.armee.einheiten
    anderesModell, *_ = zweiteEinheit.modelle
    stelle = stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 30)
    davor = stellenAllerModelle(aufstellung)

    gründe = sperrgründe(aufstellung.modellSetzen, anderesModell, stelle)

    assert gründe == {Grund.modellGesperrt}
    assert stellenAllerModelle(aufstellung) == davor


def testAuf12_1EinGesperrtesModellSperrtDasZurücklegenMitDemGrundModellGesperrt(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    gesetztesModell, gesperrtesModell, _ = einGesperrtesModell(aufstellung, zweiterSpieler)
    davor = stellenAllerModelle(aufstellung)

    gründe = sperrgründe(aufstellung.modellZurücklegen, gesetztesModell, zweiterSpieler)

    assert gründe == {Grund.modellGesperrt}
    assert stellenAllerModelle(aufstellung) == davor
    assert aufstellung.gesperrt(gesperrtesModell)


def testAuf12_1EinGesperrtesModellSperrtDasBeendenMitDemGrundModellGesperrt(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einGesperrtesModell(aufstellung, zweiterSpieler)
    davor = stellenAllerModelle(aufstellung)

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {Grund.modellGesperrt}
    assert stellenAllerModelle(aufstellung) == davor
    assert not aufstellung.aufgestellt(aufstellung.einheitInAufstellung)


def testAuf12_2EinModellDesSpielersNichtAnDerReiheStehtNachDemLoslassenWieDavor(
    aufstellung, ersterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheitDesAnderen, _ = ersterSpieler.armee.einheiten
    modell, *_ = einheitDesAnderen.modelle
    davor = stellenAllerModelle(aufstellung)

    gründe = sperrgründe(
        aufstellung.modellLoslassen, modell, stelleInDerZoneVon(aufstellung, ersterSpieler, 4, 20)
    )

    assert gründe == {Grund.nichtWählbar}
    assert stellenAllerModelle(aufstellung) == davor
    assert not aufstellung.gesperrt(modell)


def testAuf12_2EinModellEinerAnderenEinheitStehtNachDemLoslassenWieDavor(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, andereEinheit = zweiterSpieler.armee.einheiten
    erstesModell, _ = begonneneEinheit.modelle
    modellDerAnderen, *_ = andereEinheit.modelle
    aufstellung.modellSetzen(erstesModell, stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 20))
    davor = stellenAllerModelle(aufstellung)

    gründe = sperrgründe(
        aufstellung.modellLoslassen,
        modellDerAnderen,
        stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 30),
    )

    assert gründe == {Grund.einheitBegonnen}
    assert stellenAllerModelle(aufstellung) == davor
    assert not aufstellung.gesperrt(modellDerAnderen)


def testAuf12_2EinModellAufEinerAblageStehtNachDemLoslassenWieDavor(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    aufgestellteEinheit, _ = zweiterSpieler.armee.einheiten
    modell, _ = aufgestellteEinheit.modelle
    einheitAufstellen(aufstellung, aufgestellteEinheit)
    davor = stellenAllerModelle(aufstellung)

    gründe = sperrgründe(aufstellung.modellZurücklegen, modell, zweiterSpieler)

    assert gründe == {Grund.nichtWählbar}
    assert stellenAllerModelle(aufstellung) == davor


def testAuf12_2EinGesperrtesModellSperrtDasLoslassenUndLässtDasModellWoEsWar(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    gesetztesModell, _, _ = einGesperrtesModell(aufstellung, zweiterSpieler)
    davor = stellenAllerModelle(aufstellung)
    neueStelle = stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 30)

    gründe = sperrgründe(aufstellung.modellLoslassen, gesetztesModell, neueStelle)

    assert gründe == {Grund.modellGesperrt}
    assert stellenAllerModelle(aufstellung) == davor


def testAuf12_2EineEinheitDesSpielersNichtAnDerReiheStehtNachDemLoslassenWieDavor(
    aufstellung, ersterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheitDesAnderen, _ = ersterSpieler.armee.einheiten
    davor = stellenAllerModelle(aufstellung)

    gründe = sperrgründe(
        aufstellung.einheitLoslassen,
        einheitDesAnderen,
        stelleInDerZoneVon(aufstellung, ersterSpieler, 4, 20),
    )

    assert gründe == {Grund.nichtWählbar}
    assert stellenAllerModelle(aufstellung) == davor


def testAuf12_2EineAndereEinheitStehtNachDemLoslassenWieDavor(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    begonneneEinheit, andereEinheit = zweiterSpieler.armee.einheiten
    erstesModell, _ = begonneneEinheit.modelle
    aufstellung.modellSetzen(erstesModell, stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 20))
    davor = stellenAllerModelle(aufstellung)

    gründe = sperrgründe(
        aufstellung.einheitLoslassen,
        andereEinheit,
        stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 30),
    )

    assert gründe == {Grund.einheitBegonnen}
    assert stellenAllerModelle(aufstellung) == davor


def testAuf12_2EineEinheitStehtBeiGesperrtemModellNachDemLoslassenWieDavor(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einGesperrtesModell(aufstellung, zweiterSpieler)
    _, andereEinheit = zweiterSpieler.armee.einheiten
    davor = stellenAllerModelle(aufstellung)

    gründe = sperrgründe(
        aufstellung.einheitLoslassen,
        andereEinheit,
        stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 30),
    )

    assert gründe == {Grund.modellGesperrt}
    assert stellenAllerModelle(aufstellung) == davor


def testAuf12_3DerDienstAntwortetAufDasLoslassenAußerDerReiheMitDemGrundUndDemStandWieDavor(
    dienstDesBeispiels, aufstellungDesBeispiels, boyz
):
    erstesModell, *_ = boyz.modelle
    davor = spielstandVon(dienstDesBeispiels)

    antwort = modellLoslassen(
        dienstDesBeispiels,
        aufstellungDesBeispiels,
        boyz,
        erstesModell,
        Stelle(x=Fraction(2), y=Fraction(30)),
    )

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [Grund.nichtWählbar.value]
    assert antwort.get_json()["spielstand"] == davor


def testAuf12_3DieSeiteNenntDenGrundNachDemLoslassenAußerDerReiheUndBietetGemeinsamÜbergehenNichtAn(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins
):
    aufstellung = aufstellungNachDerZonenwahl
    seite = bildschirm.seiteZu(aufstellung)
    davor = stellenAllerModelle(aufstellung)

    einheitZiehen(
        seite, "Spieler 2", "Necron Warriors", stelleInDerZoneVon(aufstellung, spielerEins, 4, 30)
    )

    genannt = sperrmeldungWarten(seite, {Grund.nichtWählbar})
    assert genannt == gründeAlsText({Grund.nichtWählbar})
    assert knopfDerSeite(seite, "gemeinsam übergehen").count() == 0
    assert stellenAllerModelle(aufstellung) == davor


def testAuf12_3DieSeiteNenntDenGrundNochNachDemAuswählen(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins
):
    aufstellung = aufstellungNachDerZonenwahl
    seite = bildschirm.seiteZu(aufstellung)
    einheitZiehen(
        seite, "Spieler 2", "Necron Warriors", stelleInDerZoneVon(aufstellung, spielerEins, 4, 30)
    )
    sperrmeldungWarten(seite, {Grund.nichtWählbar})

    klickenUndWarten(seite, "Spieler 1", "Boyz")

    assert sperrmeldungWarten(seite, {Grund.nichtWählbar}) == gründeAlsText({Grund.nichtWählbar})


def testAuf12_3DieSeiteNenntDenGrundNichtMehrNachDerNächstenHandlung(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins
):
    aufstellung = aufstellungNachDerZonenwahl
    seite = bildschirm.seiteZu(aufstellung)
    stelle = stelleInDerZoneVon(aufstellung, spielerEins, 4, 30)
    einheitZiehen(seite, "Spieler 2", "Necron Warriors", stelle)
    sperrmeldungWarten(seite, {Grund.nichtWählbar})

    einheitZiehen(seite, "Spieler 1", "Boyz", stelle)

    assert sperrmeldungWarten(seite, set()) == frozenset()


@sperrenBeimBeenden
def testAuf12_4DerDienstAntwortetAufDasBeendenMitDemGrundUndDemStandWieDavor(
    aufstellung, ersterSpieler, aufbau, grund
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    aufbau(aufstellung)
    dienst = dienstFür(aufstellung)
    davor = spielstandVon(dienst)

    antwort = aufstellenDerEinheitBeenden(dienst)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [grund.value]
    assert antwort.get_json()["spielstand"] == davor


@sperrenBeimBeenden
def testAuf12_4DieSeiteNenntDenGrundNachDemKlickAufAufstellenDerEinheitBeenden(
    bildschirm, aufstellung, ersterSpieler, aufbau, grund
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    aufbau(aufstellung)
    seite = bildschirm.seiteZu(aufstellung)

    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, beenden).click()

    assert sperrmeldungWarten(seite, {grund}) == gründeAlsText({grund})


def testAuf12_4DieSeiteNenntDenGrundNochNachDemAuswählen(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, 3)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, beenden).click()
    sperrmeldungWarten(seite, {Grund.modelleFehlen})

    klickenUndWarten(seite, "Spieler 1", "Warboss")

    assert sperrmeldungWarten(seite, {Grund.modelleFehlen}) == gründeAlsText({Grund.modelleFehlen})


def testAuf12_4DieSeiteNenntDenGrundNichtMehrNachDerNächstenHandlung(
    bildschirm, aufstellungNachDerZonenwahl, boyz, spielerEins
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, 3)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, beenden).click()
    sperrmeldungWarten(seite, {Grund.modelleFehlen})
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 30)

    einheitZiehen(seite, "Spieler 1", "Boyz", stelle)

    assert sperrmeldungWarten(seite, set()) == frozenset()
