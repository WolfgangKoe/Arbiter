"""Der Spielstand der Aufstellung als JSON-fähige Werte (technik/architektur/web.md, W2, W4)."""

from arbiter.domaene.messen import radiusInZoll
from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone, grenzenInXDerZone
from arbiter.domaene.spielobjekte import Einheit, Spieler


def spielstand(aufstellung: Aufstellung) -> dict:
    ausgangslage = aufstellung.ausgangslage
    spieler = (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
    breite, länge = ausgangslage.spielfeld.seitenlängen
    return {
        "spielfeld": {"breite": float(breite), "länge": float(länge)},
        "zonen": [_zone(aufstellung, zone, spieler) for zone in Aufstellungszone],
        "modelle": _modelle(aufstellung, spieler),
        "spieler": [
            _spieler(aufstellung, nummer, einer) for nummer, einer in enumerate(spieler, start=1)
        ],
    }


def _nummer(spieler: tuple[Spieler, ...], gesucht: Spieler | None) -> int | None:
    return spieler.index(gesucht) + 1 if gesucht in spieler else None


def _zone(aufstellung: Aufstellung, zone: Aufstellungszone, spieler: tuple[Spieler, ...]) -> dict:
    breite, _ = aufstellung.ausgangslage.spielfeld.seitenlängen
    anfang, ende = grenzenInXDerZone(zone, breite, aufstellung.ausgangslage.tiefen[zone])
    besitzer = next(
        (einer for einer in spieler if aufstellung.aufstellungszone(einer) is zone), None
    )
    return {
        "x": float(anfang),
        "tiefe": float(ende - anfang),
        "spieler": _nummer(spieler, besitzer),
    }


def _modelle(aufstellung: Aufstellung, spieler: tuple[Spieler, ...]) -> list[dict]:
    return [
        {
            "x": float(aufstellung.stelle(modell).x),
            "y": float(aufstellung.stelle(modell).y),
            "radius": float(radiusInZoll(modell.base)),
            "spieler": nummer,
        }
        for nummer, einer in enumerate(spieler, start=1)
        for einheit in einer.armee.einheiten
        for modell in einheit.modelle
        if aufstellung.gesetzt(modell)
    ]


def _spieler(aufstellung: Aufstellung, nummer: int, spieler: Spieler) -> dict:
    return {
        "nummer": nummer,
        "name": f"Spieler {nummer}",
        "anDerReihe": aufstellung.anDerReihe is spieler,
        "ablage": [
            _einheit(aufstellung, einheit)
            for einheit in spieler.armee.einheiten
            if not aufstellung.aufgestellt(einheit)
        ],
    }


def _einheit(aufstellung: Aufstellung, einheit: Einheit) -> dict:
    return {
        "name": einheit.name,
        "nichtGesetzt": sum(1 for modell in einheit.modelle if not aufstellung.gesetzt(modell)),
        "inAufstellung": aufstellung.einheitInAufstellung is einheit,
    }
