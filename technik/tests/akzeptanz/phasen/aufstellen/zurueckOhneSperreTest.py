"""AUF-17 · Zurück ohne Sperre."""

from http import HTTPStatus

import pytest

from arbiter.domaene.sperre import Grund
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    inhaltDerSeite,
    knopfDerSeite,
    sperrmeldungenDerSeite,
)
from tests.akzeptanz.dienst import dienstFür, spielstandVon, zurück
from tests.akzeptanz.handgriffe import (
    einGesperrtesModell,
    modelleSetzen,
    nachDerWahlDerAufstellungszone,
    stellenAllerModelle,
)


def nachDerZonenwahl(aufstellung, ersterSpieler, _zweiterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)


def mitGesetztenModellen(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    modelleSetzen(aufstellung, einheit, 1)


def nachZurückBeiGesperrtemModell(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einGesperrtesModell(aufstellung, zweiterSpieler)
    aufstellung.zurück()


ständeOhneSperre = pytest.mark.parametrize(
    "aufbau",
    [nachDerZonenwahl, mitGesetztenModellen, nachZurückBeiGesperrtemModell],
    ids=["nachDerZonenwahl", "mitGesetztemModell", "zumZweitenMalZurück"],
)


@ständeOhneSperre
def testAuf17_1ZurückOhneGesperrtesModellLässtModelleEinheitInAufstellungUndAnDerReiheWieDavor(
    aufstellung, ersterSpieler, zweiterSpieler, aufbau
):
    aufbau(aufstellung, ersterSpieler, zweiterSpieler)
    stellenDavor = stellenAllerModelle(aufstellung)
    einheitDavor = aufstellung.einheitInAufstellung
    anDerReiheDavor = aufstellung.anDerReihe

    aufstellung.zurück()

    assert stellenAllerModelle(aufstellung) == stellenDavor
    assert aufstellung.einheitInAufstellung is einheitDavor
    assert aufstellung.anDerReihe is anDerReiheDavor


@ständeOhneSperre
def testAuf17_1DerDienstAntwortetAufZurückOhneGesperrtesModellMitDemStandWieDavor(
    aufstellung, ersterSpieler, zweiterSpieler, aufbau
):
    aufbau(aufstellung, ersterSpieler, zweiterSpieler)
    dienst = dienstFür(aufstellung)
    davor = spielstandVon(dienst)

    antwort = zurück(dienst)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == davor


def testAuf17_1EinKlickAufZurückAufEinerVorherGeöffnetenSeiteÄndertNichtsUndNenntKeinenGrund(
    bildschirm, aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einGesperrtesModell(aufstellung, zweiterSpieler)
    veraltet = bildschirm.seiteZu(aufstellung)
    knopfDerSeite(veraltet, "zurück").wait_for()
    aufstellung.zurück()
    stellenDavor = stellenAllerModelle(aufstellung)
    einheitDavor = aufstellung.einheitInAufstellung

    with aufDieHandlungWarten(veraltet):
        knopfDerSeite(veraltet, "zurück").click()

    assert stellenAllerModelle(aufstellung) == stellenDavor
    assert aufstellung.einheitInAufstellung is einheitDavor
    assert aufstellung.anDerReihe is zweiterSpieler
    assert sperrmeldungenDerSeite(veraltet) == []
    assert Grund.modellGesperrt.value not in inhaltDerSeite(veraltet)
