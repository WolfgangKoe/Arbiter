"""Dienst der Akzeptanztests: Anfragen nach dem Vertrag und das Lesen des Spielstands."""

import json
from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle
from arbiter.web.anwendung import anwendungFür

_vertrag = Path(__file__).parents[2] / "architektur" / "vertrag"

# Warum: web/ vergibt die Kennungen aus der Reihenfolge der Ausgangslage (web.md, W4)
kennungenDerEinheiten = {
    "Boyz": (1, 1),
    "Warboss": (1, 2),
    "Necron Warriors": (2, 1),
    "Overlord": (2, 2),
}


def dienstFür(aufstellung: Aufstellung):
    return anwendungFür(aufstellung).test_client()


def _beispielDesVertrags(datei: str) -> dict:
    with (_vertrag / datei).open(encoding="utf-8") as quelle:
        return json.load(quelle)


def spielstandDesVertrags() -> dict:
    """Das Beispiel von V1 aus `spielstand.json`, nicht kopiert."""
    return _beispielDesVertrags("spielstand.json")


def sperreDesVertrags() -> dict:
    """Das Beispiel von V6 aus `sperre.json`, nicht kopiert."""
    return _beispielDesVertrags("sperre.json")


def stelleBeimLoslassenDesVertrags() -> dict:
    """Das Beispiel von V10 aus `stelleBeimLoslassen.json`, nicht kopiert."""
    return _beispielDesVertrags("stelleBeimLoslassen.json")


def stellenDesVertrags(spielernummer: int) -> list[Stelle]:
    """Die Stellen der Modelle des Spielers im Beispiel, in der Reihenfolge der Datei."""
    return [
        Stelle(x=Fraction(str(modell["x"])), y=Fraction(str(modell["y"])))
        for modell in spielstandDesVertrags()["modelle"]
        if modell["spieler"] == spielernummer
    ]


def pfadDerEinheit(aufstellung: Aufstellung, einheit: Einheit) -> str:
    ausgangslage = aufstellung.ausgangslage
    spieler = (ausgangslage.ersterSpieler, ausgangslage.zweiterSpieler)
    for spielernummer, einer in enumerate(spieler, start=1):
        for einheitennummer, kandidat in enumerate(einer.armee.einheiten, start=1):
            if kandidat is einheit:
                return f"/api/spieler/{spielernummer}/einheiten/{einheitennummer}"
    raise LookupError(einheit)


def pfadDesModells(aufstellung: Aufstellung, einheit: Einheit, modell: Modell) -> str:
    modellnummer = next(
        nummer for nummer, kandidat in enumerate(einheit.modelle, start=1) if kandidat is modell
    )
    return f"{pfadDerEinheit(aufstellung, einheit)}/modelle/{modellnummer}"


def stelleImSpielstand(stelle: Stelle) -> tuple[float, float]:
    """Die Stelle als Zahlenpaar, wie der Spielstand sie führt (V1)."""
    return float(stelle.x), float(stelle.y)


def körperDerStelle(stelle: Stelle) -> dict[str, float]:
    inX, inY = stelleImSpielstand(stelle)
    return {"x": inX, "y": inY}


def modellLoslassen(
    dienst, aufstellung: Aufstellung, einheit: Einheit, modell: Modell, stelle: Stelle
):
    pfad = pfadDesModells(aufstellung, einheit, modell)
    return dienst.put(f"{pfad}/stelle", json=körperDerStelle(stelle))


def stelleBeimLoslassenAbfragen(
    dienst, aufstellung: Aufstellung, einheit: Einheit, modell: Modell, stelle: Stelle
):
    pfad = pfadDesModells(aufstellung, einheit, modell)
    return dienst.get(f"{pfad}/stelleBeimLoslassen", query_string=körperDerStelle(stelle))


def stellenDerAbfrage(
    einheit: Einheit, abfrage: Mapping[Modell, Stelle]
) -> dict[int, tuple[float, float]]:
    """Die Antwort der Abfrage je Nummer des Modells in der Einheit, wie der Dienst sie nennt."""
    return {
        nummer: stelleImSpielstand(abfrage[modell])
        for nummer, modell in enumerate(einheit.modelle, start=1)
        if modell in abfrage
    }


def modellAufAblageLoslassen(
    dienst, aufstellung: Aufstellung, einheit: Einheit, modell: Modell, spielernummer: int
):
    pfad = pfadDesModells(aufstellung, einheit, modell)
    return dienst.delete(f"{pfad}/stelle", query_string={"ablage": spielernummer})


def karteAnklicken(dienst, stelle: Stelle):
    return dienst.put("/api/karteAnklicken", json=körperDerStelle(stelle))


def aufstellenDerEinheitBeenden(dienst):
    return dienst.put("/api/aufstellenDerEinheitBeenden")


def zurück(dienst):
    return dienst.put("/api/zurück")


def pfadDerAuswahl(einheitenname: str) -> str:
    spielernummer, einheitennummer = kennungenDerEinheiten[einheitenname]
    return f"/api/spieler/{spielernummer}/einheiten/{einheitennummer}/ausgewählt"


def auswählen(dienst, einheitenname: str):
    return dienst.put(pfadDerAuswahl(einheitenname))


def abwählen(dienst, einheitenname: str):
    return dienst.delete(pfadDerAuswahl(einheitenname))


def ebeneDesVertrags() -> dict:
    """Das Beispiel von V9 aus `ebene.json`, nicht kopiert."""
    return _beispielDesVertrags("ebene.json")


def modellAlsEbene(dienst, aufstellung: Aufstellung, einheit: Einheit, modell: Modell):
    return dienst.put(f"{pfadDesModells(aufstellung, einheit, modell)}/ebene")


def einheitAlsEbene(dienst, aufstellung: Aufstellung, einheit: Einheit, modell: Modell):
    return dienst.delete(f"{pfadDesModells(aufstellung, einheit, modell)}/ebene")


def stellenDerEinheitIm(spielstand: dict, einheitenname: str) -> dict[int, tuple[float, float]]:
    """Die Stellen der gesetzten Modelle der Einheit, je Nummer des Modells."""
    spielernummer, einheitennummer = kennungenDerEinheiten[einheitenname]
    return {
        modell["nummer"]: (modell["x"], modell["y"])
        for modell in spielstand["modelle"]
        if (modell["spieler"], modell["einheit"]) == (spielernummer, einheitennummer)
    }


def ebenenIm(spielstand: dict) -> frozenset[tuple[float, float]]:
    """Die Stellen der Modelle, die der Spielstand als Ebene kennzeichnet."""
    return frozenset(
        (modell["x"], modell["y"]) for modell in spielstand["modelle"] if modell.get("ebene")
    )


def spielstandVon(dienst) -> dict:
    return dienst.get("/api/spielstand").get_json()


def einheitenDerAblagen(spielstand: dict) -> dict[str, dict]:
    return {
        einheit["name"]: einheit for einer in spielstand["spieler"] for einheit in einer["ablage"]
    }


def ausgewählteEinheitenIm(spielstand: dict) -> frozenset[str]:
    einheiten = einheitenDerAblagen(spielstand)
    return frozenset(name for name, einheit in einheiten.items() if einheit["ausgewählt"])


def ausgewählteModelleIm(spielstand: dict) -> frozenset[tuple[float, float]]:
    return frozenset(
        (modell["x"], modell["y"]) for modell in spielstand["modelle"] if modell["ausgewählt"]
    )
