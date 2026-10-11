"""Wem die Einheiten gehören und wer als Nächster eine aufstellt (AUF-1)."""

from collections.abc import Collection

from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler


def gegnerVon(spieler: tuple[Spieler, Spieler], einer: Spieler) -> Spieler:
    return next(andere for andere in spieler if andere is not einer)


def einheitVon(spieler: tuple[Spieler, Spieler], modell: Modell) -> Einheit:
    for einer in spieler:
        einheit = einer.armee.einheitVon(modell)
        if einheit is not None:
            return einheit
    raise ValueError("Das Modell gehört nicht zur Aufstellung")


def zonenVerteilen(
    spieler: tuple[Spieler, Spieler], gewinner: Spieler, zone: Aufstellungszone
) -> dict[Spieler, Aufstellungszone]:
    """Der Gewinner bekommt die gewählte Zone, sein Gegner die andere (AUF-1.1)."""
    andere = next(übrige for übrige in Aufstellungszone if übrige is not zone)
    return {gewinner: zone, gegnerVon(spieler, gewinner): andere}


def nächsterAnDerReihe(
    spieler: tuple[Spieler, Spieler], bisher: Spieler, aufgestellt: Collection[Einheit]
) -> Spieler | None:
    """Der Gegner, sonst `bisher`, solange er Einheiten hat, die nicht aufgestellt sind."""
    for kandidat in (gegnerVon(spieler, bisher), bisher):
        if any(einheit not in aufgestellt for einheit in kandidat.armee.einheiten):
            return kandidat
    return None
