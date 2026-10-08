"""Fixtures der Akzeptanztests: Testdaten, Spielstände, Bildschirm."""

import os
import select
import subprocess
import sys
from pathlib import Path

import pytest
from playwright.sync_api import Browser, sync_playwright

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone, Ausgangslage
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from arbiter.katalog.ausgangslage import ausgangslageLaden
from tests.akzeptanz.bildschirm import Bildschirm
from tests.akzeptanz.handgriffe import (
    Platz,
    aufstellungVon,
    dienstFür,
    einheitAufstellen,
    modelleSetzen,
    spielerMit,
)

_technik = Path(__file__).parents[2]
_sekundenBisZurAdresse = 15


class Befehl:
    """Der Befehl `python3 -m arbiter` als eigener Prozess; beendet, was er gestartet hat."""

    def __init__(self) -> None:
        self._prozesse: list[subprocess.Popen] = []

    def starten(self) -> str:
        """Startet Arbiter neu und gibt die Adresse aus der ersten Zeile zurück."""
        # Warum: Ungepuffert wie an einem Terminal, sonst käme die Adresse in der Pipe zu spät
        umgebung = {**os.environ, "PYTHONPATH": str(_technik), "PYTHONUNBUFFERED": "1"}
        prozess = subprocess.Popen(
            [sys.executable, "-m", "arbiter"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            env=umgebung,
        )
        self._prozesse.append(prozess)
        bereit, _, _ = select.select([prozess.stdout], [], [], _sekundenBisZurAdresse)
        return prozess.stdout.readline().strip() if bereit else ""

    def beenden(self) -> None:
        for prozess in self._prozesse:
            prozess.terminate()
            prozess.wait(timeout=10)


@pytest.fixture
def befehl():
    befehl = Befehl()
    yield befehl
    befehl.beenden()


@pytest.fixture
def adresseDesBefehls(befehl: Befehl) -> str:
    return befehl.starten()


@pytest.fixture
def ausgangslage() -> Ausgangslage:
    return ausgangslageLaden()


@pytest.fixture
def ersterSpieler() -> Spieler:
    return spielerMit(2, 1)


@pytest.fixture
def zweiterSpieler() -> Spieler:
    return spielerMit(2, 1)


@pytest.fixture
def aufstellung(ersterSpieler: Spieler, zweiterSpieler: Spieler) -> Aufstellung:
    return aufstellungVon(ersterSpieler, zweiterSpieler)


@pytest.fixture(params=list(Aufstellungszone), ids=[zone.name for zone in Aufstellungszone])
def zone(request) -> Aufstellungszone:
    return request.param


@pytest.fixture
def platz(zone: Aufstellungszone) -> Platz:
    return Platz(zone)


@pytest.fixture
def ersteEinheitDesSpielersAnDerReihe(
    aufstellung: Aufstellung, ersterSpieler: Spieler, zweiterSpieler: Spieler, zone
) -> Einheit:
    """Der erste Spieler ist mit der Zone an der Reihe; kein Modell ist gesetzt."""
    andereZone = next(kandidat for kandidat in Aufstellungszone if kandidat is not zone)
    aufstellung.gewinnerWählen(zweiterSpieler)
    aufstellung.aufstellungszoneWählen(andereZone)
    ersteEinheit, _ = ersterSpieler.armee.einheiten
    return ersteEinheit


@pytest.fixture
def einheitNachDemAnderenSpieler(
    aufstellung: Aufstellung, ersterSpieler: Spieler, zweiterSpieler: Spieler, zone
) -> Einheit:
    """Beide haben ihre erste Einheit aufgestellt; der erste Spieler ist an der Reihe."""
    andereZone = next(kandidat for kandidat in Aufstellungszone if kandidat is not zone)
    ersteEinheit, zweiteEinheit = ersterSpieler.armee.einheiten
    einheitDesAnderenSpielers, _ = zweiterSpieler.armee.einheiten
    aufstellung.gewinnerWählen(zweiterSpieler)
    aufstellung.aufstellungszoneWählen(andereZone)
    einheitAufstellen(aufstellung, ersteEinheit)
    einheitAufstellen(aufstellung, einheitDesAnderenSpielers)
    return zweiteEinheit


@pytest.fixture
def spielerEins(ausgangslage: Ausgangslage) -> Spieler:
    return ausgangslage.ersterSpieler


@pytest.fixture
def spielerZwei(ausgangslage: Ausgangslage) -> Spieler:
    return ausgangslage.zweiterSpieler


@pytest.fixture
def boyz(spielerEins: Spieler) -> Einheit:
    einheit, _ = spielerEins.armee.einheiten
    return einheit


@pytest.fixture
def necronWarriors(spielerZwei: Spieler) -> Einheit:
    einheit, _ = spielerZwei.armee.einheiten
    return einheit


@pytest.fixture
def ausgangsaufstellung(ausgangslage: Ausgangslage) -> Aufstellung:
    return Aufstellung(ausgangslage)


@pytest.fixture
def aufstellungNachDerZonenwahl(
    ausgangsaufstellung: Aufstellung, spielerZwei: Spieler
) -> Aufstellung:
    """Spieler 2 hat gewonnen und die erste Zone gewählt; Spieler 1 ist an der Reihe."""
    ausgangsaufstellung.gewinnerWählen(spielerZwei)
    ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    return ausgangsaufstellung


@pytest.fixture
def aufstellungMitModellenBeiderSpieler(
    aufstellungNachDerZonenwahl: Aufstellung, boyz: Einheit, necronWarriors: Einheit
) -> Aufstellung:
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)
    einheitAufstellen(aufstellungNachDerZonenwahl, necronWarriors)
    return aufstellungNachDerZonenwahl


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        chromium = playwright.chromium.launch()
        yield chromium
        chromium.close()


@pytest.fixture
def bildschirm(browser: Browser):
    bildschirm = Bildschirm(browser)
    yield bildschirm
    bildschirm.beenden()


@pytest.fixture
def boyzSetzen(aufstellungNachDerZonenwahl, boyz):
    """Spieler 1 wählt die Boyz und setzt so viele ihrer Modelle, wie verlangt."""

    def setzen(anzahl: int) -> list[tuple[Modell, Stelle]]:
        return modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahl)

    return setzen


@pytest.fixture
def einGesetztesModell(aufstellungNachDerZonenwahl, boyzSetzen) -> tuple[Aufstellung, Modell]:
    [(modell, _)] = boyzSetzen(1)
    return aufstellungNachDerZonenwahl, modell


@pytest.fixture
def dienst(aufstellungNachDerZonenwahl: Aufstellung):
    """Der Flask-Testclient der Anwendung über dem Spielstand der Zonenwahl."""
    return dienstFür(aufstellungNachDerZonenwahl)
