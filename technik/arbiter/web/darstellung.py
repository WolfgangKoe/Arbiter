"""Der Spielstand der Aufstellung als JSON-fähige Werte (technik/architektur/web.md, W2, W4)."""

from collections.abc import Collection, Mapping

from arbiter.domaene.messen import radiusInZoll
from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from arbiter.web.kennungen import (
    armeelisteNachNummer,
    kennungenDerEinheit,
    modelleMitKennungen,
    spielerNachNummer,
)


def spielstand(aufstellung: Aufstellung) -> dict:
    ausgangslage = aufstellung.ausgangslage
    spielerNummern = spielerNachNummer(aufstellung)
    breite, länge = ausgangslage.spielfeld.seitenlängen
    return {
        "spielfeld": {"breite": float(breite), "länge": float(länge)},
        "zonen": [_zone(aufstellung, zone, spielerNummern) for zone in Aufstellungszone],
        "modelle": _modelle(aufstellung),
        "einheitInAufstellung": _einheitInAufstellung(aufstellung),
        "spieler": [
            _spieler(aufstellung, spielernummer, einer)
            for spielernummer, einer in spielerNummern.items()
        ],
    }


def stellenBeimLoslassen(aufstellung: Aufstellung, abfrage: Mapping[Modell, Stelle]) -> dict:
    """Die Antwort der Abfrage: jedes genannte Modell mit seiner Stelle (V10)."""
    return {
        "modelle": [
            {
                "spieler": kennungen.spielernummer,
                "einheit": kennungen.einheitennummer,
                "nummer": kennungen.modellnummer,
                "x": float(abfrage[kennungen.modell].x),
                "y": float(abfrage[kennungen.modell].y),
            }
            for kennungen in modelleMitKennungen(aufstellung)
            if kennungen.modell in abfrage
        ]
    }


def _zone(
    aufstellung: Aufstellung, zone: Aufstellungszone, spielerNummern: dict[int, Spieler]
) -> dict:
    (anfangX, endeX), (anfangY, endeY) = aufstellung.ausgangslage.grenzenDerZone(zone)
    besitzer = next(
        (
            nummer
            for nummer, einer in spielerNummern.items()
            if aufstellung.aufstellungszone(einer) is zone
        ),
        None,
    )
    return {
        "x": float(anfangX),
        "y": float(anfangY),
        "breite": float(endeX - anfangX),
        "länge": float(endeY - anfangY),
        "spieler": besitzer,
    }


def _einheitInAufstellung(aufstellung: Aufstellung) -> dict | None:
    einheit = aufstellung.einheitInAufstellung
    if einheit is None:
        return None
    spielernummer, einheitennummer = kennungenDerEinheit(aufstellung, einheit)
    return {"spieler": spielernummer, "einheit": einheitennummer}


def _modell(aufstellung: Aufstellung, modell: Modell, stelle: Stelle) -> dict:
    beschreibung = {
        "x": float(stelle.x),
        "y": float(stelle.y),
        "radius": float(radiusInZoll(modell.base)),
        "ausgewählt": aufstellung.modellAusgewählt(modell),
    }
    if aufstellung.modellIstEbene(modell):
        beschreibung["ebene"] = True
    return beschreibung


def _modelle(aufstellung: Aufstellung) -> list[dict]:
    return [
        {
            **_modell(aufstellung, kennungen.modell, stelle),
            "spieler": kennungen.spielernummer,
            "einheit": kennungen.einheitennummer,
            "nummer": kennungen.modellnummer,
        }
        for kennungen in modelleMitKennungen(aufstellung)
        if (stelle := aufstellung.stelle(kennungen.modell))
    ]


def texteDerGründe(gründe: Collection[Grund]) -> list[str]:
    """Die Texte der Gründe in der Reihenfolge von `Grund` (V1, V6)."""
    return [grund.value for grund in Grund if grund in gründe]


def _spieler(aufstellung: Aufstellung, spielernummer: int, spieler: Spieler) -> dict:
    return {
        "nummer": spielernummer,
        "name": f"Spieler {spielernummer}",
        "anDerReihe": aufstellung.anDerReihe is spieler,
        "armeeliste": [
            _einheit(aufstellung, einheitennummer, einheit)
            for einheitennummer, einheit in armeelisteNachNummer(aufstellung, spieler).items()
        ],
    }


def _einheit(aufstellung: Aufstellung, einheitennummer: int, einheit: Einheit) -> dict:
    return {
        "nummer": einheitennummer,
        "name": einheit.name,
        "nichtGesetzt": sum(1 for modell in einheit.modelle if not aufstellung.gesetzt(modell)),
        "ausgewählt": aufstellung.ausgewählt(einheit),
    }
