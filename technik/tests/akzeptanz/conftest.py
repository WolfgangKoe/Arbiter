"""Fixtures der Akzeptanztests: Testdaten, Spielstände, Bildschirm."""

import os
import select
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

import pytest
from playwright.sync_api import Browser, sync_playwright

from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone, Ausgangslage
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from arbiter.katalog.ausgangslage import ausgangslageLaden
from tests.akzeptanz.bildschirm import Bildschirm
from tests.akzeptanz.dienst import dienstFür, dienstFürSchlacht, stellenDesVertrags
from tests.akzeptanz.handgriffe import (
    Platz,
    alleEinheitenAufstellen,
    aufstellungVon,
    einheitAufstellen,
    modelleAnStellenSetzen,
    modelleSetzen,
    spielerMit,
)

_technik = Path(__file__).parents[2]
_sekundenBisZurAdresse = 15
_freierPort = 0


class Ende(NamedTuple):
    """Was ein beendeter Befehl hinterließ; ein Code unter 0 heißt, er lief weiter."""

    ausgabe: str
    fehlerausgabe: str
    code: int


class Befehl:
    """Der Befehl `python3 -m arbiter` als eigener Prozess; beendet, was er gestartet hat."""

    def __init__(self) -> None:
        self._prozesse: list[subprocess.Popen] = []

    def starten(self) -> str:
        """Startet Arbiter auf einem freien Port; gibt die Adresse der ersten Zeile zurück."""
        prozess = self._prozessStarten(_freierPort, subprocess.DEVNULL)
        bereit, _, _ = select.select([prozess.stdout], [], [], _sekundenBisZurAdresse)
        return prozess.stdout.readline().strip() if bereit else ""

    def startenBisZumEnde(self, port: int) -> Ende:
        """Startet Arbiter auf dem Port und wartet auf sein Ende; läuft er weiter, endet er hier."""
        prozess = self._prozessStarten(port, subprocess.PIPE)
        try:
            ausgabe, fehlerausgabe = prozess.communicate(timeout=_sekundenBisZurAdresse)
        except subprocess.TimeoutExpired:
            prozess.terminate()
            ausgabe, fehlerausgabe = prozess.communicate()
        return Ende(ausgabe, fehlerausgabe, prozess.returncode)

    def _prozessStarten(self, port: int, fehlerausgabe: int) -> subprocess.Popen:
        umgebung = {**os.environ, "PYTHONPATH": str(_technik), "PYTHONUNBUFFERED": "1"}
        prozess = subprocess.Popen(
            [sys.executable, "-m", "arbiter", "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=fehlerausgabe,
            text=True,
            env=umgebung,
        )
        self._prozesse.append(prozess)
        return prozess

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
def warboss(spielerEins: Spieler) -> Einheit:
    _, einheit = spielerEins.armee.einheiten
    return einheit


@pytest.fixture
def necronWarriors(spielerZwei: Spieler) -> Einheit:
    einheit, _ = spielerZwei.armee.einheiten
    return einheit


@pytest.fixture
def overlord(spielerZwei: Spieler) -> Einheit:
    _, einheit = spielerZwei.armee.einheiten
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
def aufstellungDesBeispiels(
    ausgangsaufstellung: Aufstellung, spielerEins: Spieler, necronWarriors: Einheit
) -> Aufstellung:
    """Der Start nach AUF-6.1 mit den gesetzten Modellen des Beispiels im Vertrag (V1)."""
    ausgangsaufstellung.gewinnerWählen(spielerEins)
    ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    modelleAnStellenSetzen(ausgangsaufstellung, necronWarriors, stellenDesVertrags(2))
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


@pytest.fixture
def dienstDesBeispiels(aufstellungDesBeispiels: Aufstellung):
    """Der Flask-Testclient der Anwendung über dem Stand des Beispiels im Vertrag."""
    return dienstFür(aufstellungDesBeispiels)


@pytest.fixture
def beendeteAufstellung(ausgangsaufstellung: Aufstellung, spielerEins: Spieler) -> Aufstellung:
    """Spieler 1 hat die erste Zone; beide Armeen sind aufgestellt, die Aufstellung ist beendet."""
    ausgangsaufstellung.gewinnerWählen(spielerEins)
    ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    alleEinheitenAufstellen(ausgangsaufstellung)
    return ausgangsaufstellung


@pytest.fixture
def schlacht(beendeteAufstellung: Aufstellung):
    """Die Schlacht nach der Aufstellung; der Import hier lässt nur sie rot sein."""
    from arbiter.domaene.querschnitt.schlachtrunden import Schlacht

    return Schlacht(beendeteAufstellung)


@pytest.fixture
def dienstNachDerAufstellung(beendeteAufstellung: Aufstellung):
    """Der Flask-Testclient über der beendeten Aufstellung; die Schlacht baut `web/` selbst."""
    return dienstFür(beendeteAufstellung)


@pytest.fixture
def dienstDerSchlacht(beendeteAufstellung: Aufstellung, schlacht):
    """Der Flask-Testclient über derselben Schlacht, die der Test in der Hand hält."""
    return dienstFürSchlacht(beendeteAufstellung, schlacht)


@pytest.fixture
def schlachtInDerKommandophase(schlacht, spielerEins: Spieler):
    """Spieler 1 hat den ersten Zug und ist am Zug in der Kommandophase der Schlachtrunde 1."""
    schlacht.ersterZugWählen(spielerEins)
    return schlacht


@pytest.fixture
def schlachtInDerBewegungsphase(schlachtInDerKommandophase):
    """Spieler 1 ist am Zug in der Bewegungsphase der Schlachtrunde 1."""
    schlachtInDerKommandophase.phaseBeenden()
    return schlachtInDerKommandophase


@pytest.fixture
def schlachtInDerBewegungsphaseDesZweitenSpielers(schlacht, spielerZwei: Spieler):
    """Spieler 2 hat den ersten Zug und ist am Zug in der Bewegungsphase der Schlachtrunde 1."""
    schlacht.ersterZugWählen(spielerZwei)
    schlacht.phaseBeenden()
    return schlacht


@pytest.fixture(params=["ersterSpieler", "zweiterSpieler"])
def spielerMitDemErstenZug(request, spielerEins: Spieler, spielerZwei: Spieler) -> Spieler:
    return {"ersterSpieler": spielerEins, "zweiterSpieler": spielerZwei}[request.param]


@pytest.fixture(params=["einheitDesSpielersAmZug", "einheitDesAnderenSpielers"])
def einheitJederSeite(request, boyz: Einheit, necronWarriors: Einheit) -> Einheit:
    """Spieler 1 ist am Zug; die Einheit gehört ihm oder dem anderen Spieler."""
    return {"einheitDesSpielersAmZug": boyz, "einheitDesAnderenSpielers": necronWarriors}[
        request.param
    ]
