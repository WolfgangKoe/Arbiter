"""Testdaten der Akzeptanztests: kleine Armeen ohne Ausgangslage."""

import sys
from pathlib import Path

import pytest

# Warum: Modul- und Ordnernamen (arbiter.domaene.armeen, .aufstellung) sind Wahl, nicht Kriterium.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from arbiter.domaene.armeen import Armee, Einheit, Modell, Spieler  # noqa: E402
from arbiter.domaene.aufstellung import Aufstellung  # noqa: E402


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
