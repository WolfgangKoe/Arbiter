"""AUF-17 · Zurück ohne Sperre."""

from http import HTTPStatus

import pytest

from tests.akzeptanz.dienst import dienstFür, spielstandVon, zurück
from tests.akzeptanz.handgriffe import (
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


ständeOhneSperre = pytest.mark.parametrize(
    "aufbau",
    [nachDerZonenwahl, mitGesetztenModellen],
    ids=["nachDerZonenwahl", "mitGesetztemModell"],
)


@ständeOhneSperre
def testAuf17_1ZurückOhneSperreLässtModelleEinheitInAufstellungUndAnDerReiheWieDavor(
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
def testAuf17_1DerDienstAntwortetAufZurückOhneSperreMitDemStandWieDavor(
    aufstellung, ersterSpieler, zweiterSpieler, aufbau
):
    aufbau(aufstellung, ersterSpieler, zweiterSpieler)
    dienst = dienstFür(aufstellung)
    davor = spielstandVon(dienst)

    antwort = zurück(dienst)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == davor
