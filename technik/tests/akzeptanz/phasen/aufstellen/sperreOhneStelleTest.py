"""AUF-12 · Sperre ohne Stelle."""

from dataclasses import dataclass
from http import HTTPStatus

import pytest

from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle
from tests.akzeptanz.auswahl import klickenUndWarten
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    gründeAlsText,
    knopfDerSeite,
    sperrmeldungWarten,
)
from tests.akzeptanz.dienst import (
    aufstellenDerEinheitBeenden,
    dienstFür,
    modellLoslassen,
    spielstandVon,
)
from tests.akzeptanz.handgriffe import (
    einheitenAufstellen,
    modelleSetzen,
    nachDerWahlDerAufstellungszone,
    sperrgründe,
    stelleInDerZoneVon,
    stellenAllerModelle,
)
from tests.akzeptanz.ziehen import modellZiehen

beenden = "Aufstellen der Einheit beenden"
übergehen = "gemeinsam übergehen"


@dataclass(frozen=True)
class Loslassen:
    """Ein Modell, losgelassen auf der Karte an der `stelle`."""

    einheit: Einheit
    modell: Modell
    stelle: Stelle


def inDerDomäneLoslassen(aufstellung, fall: Loslassen) -> None:
    aufstellung.modellLoslassen(fall.modell, fall.stelle)


def imDienstLoslassen(dienst, aufstellung, fall: Loslassen):
    return modellLoslassen(dienst, aufstellung, fall.einheit, fall.modell, fall.stelle)


def amBildschirmLoslassen(seite, aufstellung, fall: Loslassen):
    start = aufstellung.stelle(fall.modell)
    return modellZiehen(seite, start, fall.stelle)


def freieStelleDesSpielersAnDerReihe(aufstellung) -> Stelle:
    return stelleInDerZoneVon(aufstellung, aufstellung.anDerReihe, 4, 40)


def einModellDesSpielersNichtAnDerReihe(aufstellung, einheit) -> Loslassen:
    einheitenAufstellen(aufstellung, 2)
    modell, *_ = einheit.modelle
    return Loslassen(einheit, modell, stelle=freieStelleDesSpielersAnDerReihe(aufstellung))


def einModellEinerAufgestelltenEinheit(aufstellung, einheit) -> Loslassen:
    einheitenAufstellen(aufstellung, 2)
    modell, *_ = einheit.modelle
    return Loslassen(einheit, modell, stelle=freieStelleDesSpielersAnDerReihe(aufstellung))


@pytest.fixture(
    params=[
        (einModellDesSpielersNichtAnDerReihe, "necronWarriors"),
        (einModellEinerAufgestelltenEinheit, "boyz"),
    ],
    ids=[
        "auf7_2ModellDesSpielersNichtAnDerReihe",
        "auf7_2ModellEinerAufgestelltenEinheit",
    ],
)
def sperrendesLoslassen(request, aufstellungNachDerZonenwahl) -> Loslassen:
    aufbau, einheitenname = request.param
    return aufbau(aufstellungNachDerZonenwahl, request.getfixturevalue(einheitenname))


def ohneEinheitInAufstellung(aufstellung):
    """Nichts gesetzt: AUF-7.4."""


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
        (ohneKohärenz, Grund.keineKohärenz),
    ],
    ids=["nichtInAufstellung", "keineKohärenz"],
)


def testAuf12_5EinSperrendesLoslassenNenntNichtWählbarUndLässtJedesModellWoEsWar(
    aufstellungNachDerZonenwahl, sperrendesLoslassen
):
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)

    gründe = sperrgründe(inDerDomäneLoslassen, aufstellungNachDerZonenwahl, sperrendesLoslassen)

    assert gründe == {Grund.nichtWählbar}
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor


def testAuf12_6EinSperrendesLoslassenNenntDenGrund(
    aufstellungNachDerZonenwahl, sperrendesLoslassen
):
    gründe = sperrgründe(inDerDomäneLoslassen, aufstellungNachDerZonenwahl, sperrendesLoslassen)

    assert gründe == {Grund.nichtWählbar}


def testAuf12_6DerDienstAntwortetMitDemGrundUndDemStandWieDavor(
    aufstellungNachDerZonenwahl, sperrendesLoslassen
):
    dienst = dienstFür(aufstellungNachDerZonenwahl)
    davor = spielstandVon(dienst)

    antwort = imDienstLoslassen(dienst, aufstellungNachDerZonenwahl, sperrendesLoslassen)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [Grund.nichtWählbar.value]
    assert antwort.get_json()["spielstand"] == davor


def testAuf12_6DieSeiteNenntDenGrundUndBietetGemeinsamÜbergehenNichtAn(
    bildschirm, aufstellungNachDerZonenwahl, sperrendesLoslassen
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)

    antwort = amBildschirmLoslassen(seite, aufstellungNachDerZonenwahl, sperrendesLoslassen)
    genannt = sperrmeldungWarten(seite, {Grund.nichtWählbar})

    assert antwort.status == HTTPStatus.CONFLICT
    assert genannt == gründeAlsText({Grund.nichtWählbar})
    assert knopfDerSeite(seite, übergehen).count() == 0
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor


def einAufgestelltesModellAufDieKarteZiehen(seite, aufstellung, boyz) -> None:
    aufgestelltesModell, *_ = boyz.modelle
    freieStelle = freieStelleDesSpielersAnDerReihe(aufstellung)
    modellZiehen(seite, aufstellung.stelle(aufgestelltesModell), freieStelle)
    sperrmeldungWarten(seite, {Grund.nichtWählbar})


def testAuf12_6DieSeiteNenntDenGrundNochNachDemAuswählen(
    bildschirm, aufstellungNachDerZonenwahl, boyz
):
    einheitenAufstellen(aufstellungNachDerZonenwahl, 2)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    einAufgestelltesModellAufDieKarteZiehen(seite, aufstellungNachDerZonenwahl, boyz)

    klickenUndWarten(seite, "Spieler 1", "Warboss")

    assert sperrmeldungWarten(seite, {Grund.nichtWählbar}) == gründeAlsText({Grund.nichtWählbar})


def testAuf12_6DieSeiteNenntDenGrundNichtMehrNachDerNächstenHandlung(
    bildschirm, aufstellungNachDerZonenwahl, boyz, warboss, spielerEins
):
    einheitenAufstellen(aufstellungNachDerZonenwahl, 2)
    (_, stelleDesWarboss), *_ = modelleSetzen(aufstellungNachDerZonenwahl, warboss, 1)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    einAufgestelltesModellAufDieKarteZiehen(seite, aufstellungNachDerZonenwahl, boyz)
    neueStelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 30)

    modellZiehen(seite, stelleDesWarboss, neueStelle)

    assert sperrmeldungWarten(seite, set()) == frozenset()


@sperrenBeimBeenden
def testAuf12_7DieSperreBeimBeendenNenntDenGrundUndLässtDieModelleWoSieSind(
    aufstellung, ersterSpieler, aufbau, grund
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    aufbau(aufstellung)
    davor = stellenAllerModelle(aufstellung)

    gründe = sperrgründe(aufstellung.aufstellenDerEinheitBeenden)

    assert gründe == {grund}
    assert stellenAllerModelle(aufstellung) == davor


@sperrenBeimBeenden
def testAuf12_7DerDienstAntwortetAufDasBeendenMitDemGrundUndDemStandWieDavor(
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
def testAuf12_7DieSeiteNenntDenGrundNachDemKlickAufAufstellenDerEinheitBeenden(
    bildschirm, aufstellung, ersterSpieler, aufbau, grund
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    aufbau(aufstellung)
    seite = bildschirm.seiteZu(aufstellung)

    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, beenden).click()

    assert sperrmeldungWarten(seite, {grund}) == gründeAlsText({grund})


def testAuf12_7DieSeiteNenntDenGrundNochNachDemAuswählen(bildschirm, aufstellungNachDerZonenwahl):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, beenden).click()
    sperrmeldungWarten(seite, {Grund.nichtInAufstellung})

    klickenUndWarten(seite, "Spieler 1", "Warboss")

    assert sperrmeldungWarten(seite, {Grund.nichtInAufstellung}) == gründeAlsText(
        {Grund.nichtInAufstellung}
    )


def testAuf12_7DieSeiteNenntDenGrundNichtMehrNachDerNächstenHandlung(
    bildschirm, aufstellung, ersterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    ohneKohärenz(aufstellung)
    spielerAnDerReihe = aufstellung.anDerReihe
    einheit, _ = spielerAnDerReihe.armee.einheiten
    _, zweitesModell = einheit.modelle
    stelleDesZweitenModells = aufstellung.stelle(zweitesModell)
    nebenDemErsten = stelleInDerZoneVon(aufstellung, spielerAnDerReihe, 4, 12)
    seite = bildschirm.seiteZu(aufstellung)
    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, beenden).click()
    sperrmeldungWarten(seite, {Grund.keineKohärenz})

    modellZiehen(seite, stelleDesZweitenModells, nebenDemErsten)

    assert sperrmeldungWarten(seite, set()) == frozenset()
