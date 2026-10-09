"""Übersetzt die Kennungen nach W4 in Spieler und Einheiten der Ablage (web.md, W2, W4)."""

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Einheit, Spieler


def spielerNachNummer(aufstellung: Aufstellung) -> dict[int, Spieler]:
    ausgangslage = aufstellung.ausgangslage
    return dict(enumerate((ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler), start=1))


def ablageNachNummer(aufstellung: Aufstellung, spieler: Spieler) -> dict[int, Einheit]:
    return {
        nummer: einheit
        for nummer, einheit in enumerate(spieler.armee.einheiten, start=1)
        if not aufstellung.aufgestellt(einheit)
    }
