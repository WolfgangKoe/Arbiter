"""Testdaten der Akzeptanztests: kleine Armeen, keine Ausgangslage (Plan 1).

Schnittstelle, vom Testautor festgelegt, vom Architekten zu prüfen: Modul- und Ordnernamen
(`technik/backend`, `arbiter.domaene.armeen`, `.aufstellung`) sind Wahl, nicht Kriterium; zwei
Aufstellungszone-Werte; Grund NICHT_WÄHLBAR, NICHT_IN_AUFSTELLUNG, EINHEIT_BEGONNEN;
modell_setzen(modell) ohne Stelle, weil Plan 1 sie nicht prüft.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from arbiter.domaene.armeen import Armee, Einheit, Modell, Spieler  # noqa: E402
from arbiter.domaene.aufstellung import Aufstellung  # noqa: E402


def spieler_mit(*modellzahlen: int) -> Spieler:
    """Ein Spieler, dessen Armee je Zahl eine Einheit mit so vielen Modellen hat."""
    einheiten = [Einheit(modelle=[Modell() for _ in range(zahl)]) for zahl in modellzahlen]
    return Spieler(armee=Armee(einheiten=einheiten))


@pytest.fixture
def spieler_mit_einheiten():
    return spieler_mit


@pytest.fixture
def a() -> Spieler:
    return spieler_mit(2, 1)


@pytest.fixture
def b() -> Spieler:
    return spieler_mit(2, 1)


@pytest.fixture
def aufstellung(a: Spieler, b: Spieler) -> Aufstellung:
    return Aufstellung(a, b)
