"""Der Spielstand der Aufstellung als JSON-fähige Werte (technik/architektur/web.md, W2, W4)."""

from arbiter.domaene.messen import radiusInZoll
from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone
from arbiter.domaene.spielobjekte import Einheit, Spieler
from arbiter.web.kennungen import ablageNachNummer, spielerNachNummer


def spielstand(aufstellung: Aufstellung) -> dict:
    ausgangslage = aufstellung.ausgangslage
    spielerNummern = spielerNachNummer(aufstellung)
    spieler = tuple(spielerNummern.values())
    breite, länge = ausgangslage.spielfeld.seitenlängen
    return {
        "spielfeld": {"breite": float(breite), "länge": float(länge)},
        "zonen": [_zone(aufstellung, zone, spieler) for zone in Aufstellungszone],
        "modelle": _modelle(aufstellung, spieler),
        "spieler": [
            _spieler(aufstellung, spielernummer, einer)
            for spielernummer, einer in spielerNummern.items()
        ],
    }


def _nummer(spieler: tuple[Spieler, ...], gesucht: Spieler | None) -> int | None:
    return spieler.index(gesucht) + 1 if gesucht in spieler else None


def _zone(aufstellung: Aufstellung, zone: Aufstellungszone, spieler: tuple[Spieler, ...]) -> dict:
    (anfangX, endeX), (anfangY, endeY) = aufstellung.ausgangslage.grenzenDerZone(zone)
    besitzer = next(
        (einer for einer in spieler if aufstellung.aufstellungszone(einer) is zone), None
    )
    return {
        "x": float(anfangX),
        "y": float(anfangY),
        "breite": float(endeX - anfangX),
        "länge": float(endeY - anfangY),
        "spieler": _nummer(spieler, besitzer),
    }


def _modelle(aufstellung: Aufstellung, spieler: tuple[Spieler, ...]) -> list[dict]:
    return [
        {
            "x": float(stelle.x),
            "y": float(stelle.y),
            "radius": float(radiusInZoll(modell.base)),
            "spieler": nummer,
            "ausgewählt": aufstellung.ausgewählt(einheit),
        }
        for nummer, einer in enumerate(spieler, start=1)
        for einheit in einer.armee.einheiten
        for modell in einheit.modelle
        if (stelle := aufstellung.stelle(modell))
    ]


def _spieler(aufstellung: Aufstellung, spielernummer: int, spieler: Spieler) -> dict:
    return {
        "nummer": spielernummer,
        "name": f"Spieler {spielernummer}",
        "anDerReihe": aufstellung.anDerReihe is spieler,
        "ablage": [
            _einheit(aufstellung, einheitennummer, einheit)
            for einheitennummer, einheit in ablageNachNummer(aufstellung, spieler).items()
        ],
    }


def _einheit(aufstellung: Aufstellung, einheitennummer: int, einheit: Einheit) -> dict:
    return {
        "nummer": einheitennummer,
        "name": einheit.name,
        "nichtGesetzt": sum(1 for modell in einheit.modelle if not aufstellung.gesetzt(modell)),
        "inAufstellung": aufstellung.einheitInAufstellung is einheit,
        "ausgewählt": aufstellung.ausgewählt(einheit),
    }
