from collections.abc import Collection

from arbiter.domaene.messen import radiusInZoll
from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone
from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.phasen.bewegung.grenzkreise import Einhüllende
from arbiter.domaene.querschnitt.schlachtrunden import Schlacht
from arbiter.domaene.querschnitt.setzen import Gezeigt
from arbiter.domaene.querschnitt.uebergehen import Eintrag
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from arbiter.web.kennungen import (
    armeelisteNachNummer,
    kennungenDerEinheit,
    modelleMitKennungen,
    nummerDesSpielers,
    spielerNachNummer,
)


def spielstand(aufstellung: Aufstellung, schlacht: Schlacht | None = None) -> dict:
    ausgangslage = aufstellung.ausgangslage
    spielerNummern = spielerNachNummer(aufstellung)
    breite, länge = ausgangslage.spielfeld.seitenlängen
    stand = {
        "spielfeld": {"breite": float(breite), "länge": float(länge)},
        "zonen": [_zone(aufstellung, zone, spielerNummern) for zone in Aufstellungszone],
        "modelle": _modelle(aufstellung, schlacht or aufstellung),
        "einheitInAufstellung": _einheitInAufstellung(aufstellung),
        "spieler": [
            _spieler(aufstellung, spielernummer, einer)
            for spielernummer, einer in spielerNummern.items()
        ],
    }
    if schlacht is not None:
        stand["schlacht"] = _schlacht(aufstellung, schlacht)
    return stand


def _schlacht(aufstellung: Aufstellung, schlacht: Schlacht) -> dict:
    return {
        "ersterZug": nummerDesSpielers(aufstellung, schlacht.ersterZug),
        "amZug": nummerDesSpielers(aufstellung, schlacht.amZug),
        "schlachtrunde": schlacht.schlachtrunde,
        "phase": schlacht.phase.value,
        "beendet": schlacht.beendet,
        "protokoll": [
            _eintrag(aufstellung, eintrag) for eintrag in reversed(list(schlacht.protokoll))
        ],
        "gemeinsamÜbergehen": {"angeboten": schlacht.gemeinsamÜbergehenAngeboten},
        "grenzen": [_grenze(aufstellung, grenze) for grenze in schlacht.grenzen],
        "vorrücken": {
            "angeboten": schlacht.vorrückenAngeboten,
            "zurücknehmen": schlacht.vorrückenZurücknehmenAngeboten,
        },
        "einheitZurücksetzen": {"angeboten": schlacht.einheitZurücksetzenAngeboten},
    }


def _grenze(aufstellung: Aufstellung, grenze: Einhüllende) -> dict:
    spielernummer, einheitennummer = kennungenDerEinheit(aufstellung, grenze.einheit)
    beschreibung = {
        "spieler": spielernummer,
        "einheit": einheitennummer,
        "kreise": [
            {"x": float(kreis.stelle.x), "y": float(kreis.stelle.y), "radius": float(kreis.radius)}
            for kreis in grenze.kreise
        ],
    }
    if grenze.wurf is not None:
        beschreibung["wurf"] = grenze.wurf
    if grenze.wählbar:
        beschreibung["wählbar"] = True
    if grenze.nahkampfreichweite:
        beschreibung["nahkampfreichweite"] = True
    return beschreibung


def _eintrag(aufstellung: Aufstellung, eintrag: Eintrag) -> dict:
    spielernummer, einheitennummer = kennungenDerEinheit(aufstellung, eintrag.einheit)
    return {
        "spieler": spielernummer,
        "einheit": einheitennummer,
        "name": eintrag.einheit.name,
        "gründe": texteDerGründe(eintrag.gründe),
    }


def stellenBeimLoslassen(aufstellung: Aufstellung, gezeigt: Gezeigt) -> dict:
    angehalten = {"angehaltenAufDemWeg": True} if gezeigt.angehaltenAufDemWeg else {}
    return {
        **angehalten,
        "modelle": [
            {
                "spieler": kennungen.spielernummer,
                "einheit": kennungen.einheitennummer,
                "nummer": kennungen.modellnummer,
                "x": float(gezeigt.stellen[kennungen.modell].x),
                "y": float(gezeigt.stellen[kennungen.modell].y),
            }
            for kennungen in modelleMitKennungen(aufstellung)
            if kennungen.modell in gezeigt.stellen
        ],
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


def _modell(quelle: Aufstellung | Schlacht, modell: Modell, stelle: Stelle) -> dict:
    beschreibung = {
        "x": float(stelle.x),
        "y": float(stelle.y),
        "radius": float(radiusInZoll(modell.base)),
        "ausgewählt": quelle.modellAusgewählt(modell),
    }
    if quelle.modellIstEbene(modell):
        beschreibung["ebene"] = True
    return beschreibung


def _modelle(aufstellung: Aufstellung, quelle: Aufstellung | Schlacht) -> list[dict]:
    return [
        {
            **_modell(quelle, kennungen.modell, stelle),
            "spieler": kennungen.spielernummer,
            "einheit": kennungen.einheitennummer,
            "nummer": kennungen.modellnummer,
        }
        for kennungen in modelleMitKennungen(aufstellung)
        if (stelle := quelle.stelle(kennungen.modell))
    ]


def texteDerGründe(gründe: Collection[Grund]) -> list[str]:
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
