"""Testdaten der Akzeptanztests: kleine Armeen ohne Ausgangslage."""

import pytest
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Armee, Einheit, Modell, Spieler


def spielerMit(*modellzahlen: int) -> Spieler:
    """Ein Spieler, dessen Armee je Zahl eine Einheit mit so vielen Modellen hat."""
    einheiten = [Einheit(modelle=[Modell() for _ in range(zahl)]) for zahl in modellzahlen]
    return Spieler(armee=Armee(einheiten=einheiten))


@pytest.fixture
def spielerMitEinheiten():
    return spielerMit


@pytest.fixture
def ersterSpieler() -> Spieler:
    return spielerMit(2, 1)


@pytest.fixture
def zweiterSpieler() -> Spieler:
    return spielerMit(2, 1)


@pytest.fixture
def aufstellung(ersterSpieler: Spieler, zweiterSpieler: Spieler) -> Aufstellung:
    return Aufstellung(ersterSpieler, zweiterSpieler)
