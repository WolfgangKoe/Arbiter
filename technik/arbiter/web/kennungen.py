"""Übersetzt die Kennungen nach W4 in Spieler, Einheiten und Modelle (web.md, W2, W4)."""

from collections.abc import Iterator
from typing import NamedTuple

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler


class ModellMitKennungen(NamedTuple):
    spielernummer: int
    einheitennummer: int
    modellnummer: int
    modell: Modell


def spielerNachNummer(aufstellung: Aufstellung) -> dict[int, Spieler]:
    ausgangslage = aufstellung.ausgangslage
    return dict(enumerate((ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler), start=1))


def nummerDesSpielers(aufstellung: Aufstellung, spieler: Spieler | None) -> int | None:
    """Die Spielernummer des Spielers, ohne Spieler `None`."""
    nummern = {einer: nummer for nummer, einer in spielerNachNummer(aufstellung).items()}
    return nummern.get(spieler)


def einheitenNachNummer(spieler: Spieler) -> dict[int, Einheit]:
    return dict(enumerate(spieler.armee.einheiten, start=1))


def modelleNachNummer(einheit: Einheit) -> dict[int, Modell]:
    return dict(enumerate(einheit.modelle, start=1))


def modelleMitKennungen(aufstellung: Aufstellung) -> Iterator[ModellMitKennungen]:
    for spielernummer, spieler in spielerNachNummer(aufstellung).items():
        for einheitennummer, einheit in einheitenNachNummer(spieler).items():
            for modellnummer, modell in modelleNachNummer(einheit).items():
                yield ModellMitKennungen(spielernummer, einheitennummer, modellnummer, modell)


def kennungenDerEinheit(aufstellung: Aufstellung, einheit: Einheit) -> tuple[int, int]:
    """Spielernummer und Einheitennummer der Einheit."""
    for spielernummer, spieler in spielerNachNummer(aufstellung).items():
        for einheitennummer, andere in einheitenNachNummer(spieler).items():
            if andere is einheit:
                return spielernummer, einheitennummer
    raise ValueError("Die Einheit gehört nicht zur Aufstellung")


def armeelisteNachNummer(aufstellung: Aufstellung, spieler: Spieler) -> dict[int, Einheit]:
    return {
        nummer: einheit
        for nummer, einheit in einheitenNachNummer(spieler).items()
        if not aufstellung.aufgestellt(einheit)
    }
