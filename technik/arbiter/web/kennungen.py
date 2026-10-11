"""Übersetzt die Kennungen nach W4 in Spieler, Einheiten und Modelle (web.md, W2, W4)."""

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler


def spielerNachNummer(aufstellung: Aufstellung) -> dict[int, Spieler]:
    ausgangslage = aufstellung.ausgangslage
    return dict(enumerate((ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler), start=1))


def einheitenNachNummer(spieler: Spieler) -> dict[int, Einheit]:
    return dict(enumerate(spieler.armee.einheiten, start=1))


def modelleNachNummer(einheit: Einheit) -> dict[int, Modell]:
    return dict(enumerate(einheit.modelle, start=1))


def ablageNachNummer(aufstellung: Aufstellung, spieler: Spieler) -> dict[int, Einheit]:
    return {
        nummer: einheit
        for nummer, einheit in einheitenNachNummer(spieler).items()
        if not aufstellung.aufgestellt(einheit)
    }
