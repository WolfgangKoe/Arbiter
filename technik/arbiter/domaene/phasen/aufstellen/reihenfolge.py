from collections.abc import Collection

from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone
from arbiter.domaene.spielobjekte import Einheit, Spieler


def gegnerVon(beideSpieler: tuple[Spieler, Spieler], spieler: Spieler) -> Spieler:
    return next(andere for andere in beideSpieler if andere is not spieler)


def zonenVerteilen(
    beideSpieler: tuple[Spieler, Spieler], gewinner: Spieler, zone: Aufstellungszone
) -> dict[Spieler, Aufstellungszone]:
    andere = next(übrige for übrige in Aufstellungszone if übrige is not zone)
    return {gewinner: zone, gegnerVon(beideSpieler, gewinner): andere}


def nächsterAnDerReihe(
    beideSpieler: tuple[Spieler, Spieler], bisher: Spieler, aufgestellt: Collection[Einheit]
) -> Spieler | None:
    for kandidat in (gegnerVon(beideSpieler, bisher), bisher):
        if any(einheit not in aufgestellt for einheit in kandidat.armee.einheiten):
            return kandidat
    return None
