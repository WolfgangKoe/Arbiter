"""Fixtures der Akzeptanztests: Testdaten, Spielstände, Bildschirm."""

import pytest
from playwright.sync_api import Browser, sync_playwright

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone, Ausgangslage
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from arbiter.katalog.ausgangslage import ausgangslageLaden
from tests.akzeptanz.bildschirm import Bildschirm
from tests.akzeptanz.handgriffe import (
    Platz,
    aufstellungVon,
    einheitAufstellen,
    modelleSetzen,
    spielerMit,
)


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
def einheitInAufstellung(
    aufstellung: Aufstellung, ersterSpieler: Spieler, zweiterSpieler: Spieler, zone
) -> Einheit:
    """Der erste Spieler ist mit der Zone an der Reihe und hat seine erste Einheit gewählt."""
    andereZone = next(kandidat for kandidat in Aufstellungszone if kandidat is not zone)
    aufstellung.gewinnerWählen(zweiterSpieler)
    aufstellung.aufstellungszoneWählen(andereZone)
    ersteEinheit, _ = ersterSpieler.armee.einheiten
    aufstellung.einheitInAufstellungWählen(ersteEinheit)
    return ersteEinheit


@pytest.fixture
def einheitNachDemAnderenSpieler(
    aufstellung: Aufstellung, ersterSpieler: Spieler, zweiterSpieler: Spieler, zone
) -> Einheit:
    """Beide haben ihre erste Einheit aufgestellt; der erste Spieler hat seine zweite gewählt."""
    andereZone = next(kandidat for kandidat in Aufstellungszone if kandidat is not zone)
    ersteEinheit, zweiteEinheit = ersterSpieler.armee.einheiten
    einheitDesAnderenSpielers, _ = zweiterSpieler.armee.einheiten
    aufstellung.gewinnerWählen(zweiterSpieler)
    aufstellung.aufstellungszoneWählen(andereZone)
    einheitAufstellen(aufstellung, ersteEinheit)
    einheitAufstellen(aufstellung, einheitDesAnderenSpielers)
    aufstellung.einheitInAufstellungWählen(zweiteEinheit)
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
