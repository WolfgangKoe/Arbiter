"""AUF-12 · Sperre ohne Stelle."""

from dataclasses import dataclass
from http import HTTPStatus

import pytest

from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle
from tests.akzeptanz.auswahl import klickenUndWarten
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    beendenKnopf,
    gründeAlsText,
    knopfDerSeite,
    sperrmeldungWarten,
)
from tests.akzeptanz.dienst import (
    aufstellenDerEinheitBeenden,
    dienstFür,
    spielstandVon,
)
from tests.akzeptanz.handgriffe import (
    einheitenAufstellen,
    nachDerWahlDerAufstellungszone,
    sperrgründe,
    stelleInDerZoneVon,
    stellenAllerModelle,
)
from tests.akzeptanz.ziehen import modellZiehen


@dataclass(frozen=True)
class Loslassen:
    einheit: Einheit
    modell: Modell
    stelle: Stelle


def inDerDomäneLoslassen(aufstellung, fall: Loslassen) -> None:
    aufstellung.modellLoslassen(fall.modell, fall.stelle)


def freieStelleDesSpielersAnDerReihe(aufstellung) -> Stelle:
    return stelleInDerZoneVon(aufstellung, aufstellung.anDerReihe, 4, 40)


def einModellAnEinerFreienStelle(aufstellung, einheit) -> Loslassen:
    einheitenAufstellen(aufstellung, 2)
    modell, *_ = einheit.modelle
    return Loslassen(einheit, modell, stelle=freieStelleDesSpielersAnDerReihe(aufstellung))


@pytest.fixture(
    params=["necronWarriors", "boyz"],
    ids=[
        "auf7_2ModellDesSpielersNichtAnDerReihe",
        "auf7_2ModellEinerAufgestelltenEinheit",
    ],
)
def sperrendesLoslassen(request, aufstellungNachDerZonenwahl) -> Loslassen:
    einheit = request.getfixturevalue(request.param)
    return einModellAnEinerFreienStelle(aufstellungNachDerZonenwahl, einheit)


def ohneEinheitInAufstellung(aufstellung): ...


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
        knopfDerSeite(seite, beendenKnopf).click()

    assert sperrmeldungWarten(seite, {grund}) == gründeAlsText({grund})


def testAuf12_7DieSeiteNenntDenGrundNochNachDemAuswählen(bildschirm, aufstellungNachDerZonenwahl):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, beendenKnopf).click()
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
        knopfDerSeite(seite, beendenKnopf).click()
    sperrmeldungWarten(seite, {Grund.keineKohärenz})

    modellZiehen(seite, stelleDesZweitenModells, nebenDemErsten)

    assert sperrmeldungWarten(seite, set()) == frozenset()
