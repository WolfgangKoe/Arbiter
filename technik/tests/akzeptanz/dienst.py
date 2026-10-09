"""Dienst der Akzeptanztests: Anfragen nach dem Vertrag und das Lesen des Spielstands."""

import json
from fractions import Fraction
from pathlib import Path

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Stelle
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


def spielstandDesVertrags() -> dict:
    """Das Beispiel von V1 aus `spielstand.json`, nicht kopiert."""
    with (_vertrag / "spielstand.json").open(encoding="utf-8") as datei:
        return json.load(datei)


def stellenDesVertrags(spielernummer: int) -> list[Stelle]:
    """Die Stellen der Modelle des Spielers im Beispiel, in der Reihenfolge der Datei."""
    return [
        Stelle(x=Fraction(str(modell["x"])), y=Fraction(str(modell["y"])))
        for modell in spielstandDesVertrags()["modelle"]
        if modell["spieler"] == spielernummer
    ]


def pfadDerAuswahl(einheitenname: str) -> str:
    spielernummer, einheitennummer = kennungenDerEinheiten[einheitenname]
    return f"/api/spieler/{spielernummer}/einheiten/{einheitennummer}/ausgewählt"


def auswählen(dienst, einheitenname: str):
    return dienst.put(pfadDerAuswahl(einheitenname))


def abwählen(dienst, einheitenname: str):
    return dienst.delete(pfadDerAuswahl(einheitenname))


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
