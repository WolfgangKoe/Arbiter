import json
from collections.abc import Iterable, Mapping
from fractions import Fraction
from pathlib import Path

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle
from arbiter.web.anwendung import anwendungFür

_vertrag = Path(__file__).parents[2] / "architektur" / "vertrag"

kennungenDerEinheiten = {
    "Boyz": (1, 1),
    "Warboss": (1, 2),
    "Necron Warriors": (2, 1),
    "Overlord": (2, 2),
}


def dienstFür(aufstellung: Aufstellung):
    return anwendungFür(aufstellung).test_client()


def dienstFürSchlacht(aufstellung: Aufstellung, schlacht):
    return anwendungFür(aufstellung, schlacht=schlacht).test_client()


def _beispielDesVertrags(datei: str) -> dict:
    with (_vertrag / datei).open(encoding="utf-8") as quelle:
        return json.load(quelle)


def spielstandDesVertrags() -> dict:
    return _beispielDesVertrags("spielstand.json")


def sperreDesVertrags() -> dict:
    return _beispielDesVertrags("sperre.json")


def zurückgelegtDesVertrags() -> dict:
    return _beispielDesVertrags("zurueckgelegt.json")


def stelleBeimLoslassenDesVertrags() -> dict:
    return _beispielDesVertrags("stelleBeimLoslassen.json")


def losgelassenDesVertrags() -> dict:
    return _beispielDesVertrags("losgelassen.json")


def keineStelleBeimLoslassenDesVertrags() -> dict:
    return _beispielDesVertrags("keineStelleBeimLoslassen.json")


def schlachtDesVertrags() -> dict:
    return _beispielDesVertrags("schlacht.json")


def protokollDesVertrags() -> dict:
    return _beispielDesVertrags("protokoll.json")


def schlachtNachSchlüsselnDes(spielstand: dict, beispiel: Mapping) -> dict:
    return {
        schlüssel: wert
        for schlüssel, wert in spielstand["schlacht"].items()
        if schlüssel in beispiel
    }


def gemeinsamÜbergehen(dienst):
    return dienst.put("/api/gemeinsamÜbergehen")


def angehaltenDesVertrags() -> dict:
    return _beispielDesVertrags("angehalten.json")


def stellenDesVertrags(spielernummer: int) -> list[Stelle]:
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
    return {
        nummer: stelleImSpielstand(abfrage[modell])
        for nummer, modell in enumerate(einheit.modelle, start=1)
        if modell in abfrage
    }


def karteAnklicken(dienst, stelle: Stelle):
    return dienst.put("/api/karteAnklicken", json=körperDerStelle(stelle))


def vorrücken(dienst):
    return dienst.put("/api/vorrücken")


def vorrückenZurücknehmen(dienst):
    return dienst.put("/api/vorrückenZurücknehmen")


def aufstellenDerEinheitBeenden(dienst):
    return dienst.put("/api/aufstellenDerEinheitBeenden")


def zurücklegen(dienst):
    return dienst.put("/api/zurücklegen")


def pfadDerAuswahl(einheitenname: str) -> str:
    spielernummer, einheitennummer = kennungenDerEinheiten[einheitenname]
    return f"/api/spieler/{spielernummer}/einheiten/{einheitennummer}/ausgewählt"


def auswählen(dienst, einheitenname: str):
    return dienst.put(pfadDerAuswahl(einheitenname))


def abwählen(dienst, einheitenname: str):
    return dienst.delete(pfadDerAuswahl(einheitenname))


def ebeneDesVertrags() -> dict:
    return _beispielDesVertrags("ebene.json")


def stellenDerEinheitIm(spielstand: dict, einheitenname: str) -> dict[int, tuple[float, float]]:
    spielernummer, einheitennummer = kennungenDerEinheiten[einheitenname]
    return {
        modell["nummer"]: (modell["x"], modell["y"])
        for modell in spielstand["modelle"]
        if (modell["spieler"], modell["einheit"]) == (spielernummer, einheitennummer)
    }


def ebenenIm(spielstand: dict) -> frozenset[tuple[float, float]]:
    return frozenset(
        (modell["x"], modell["y"]) for modell in spielstand["modelle"] if modell.get("ebene")
    )


def spielstandVon(dienst) -> dict:
    return dienst.get("/api/spielstand").get_json()


def einheitenDerArmeelisten(spielstand: dict) -> dict[str, dict]:
    return {
        einheit["name"]: einheit
        for einer in spielstand["spieler"]
        for einheit in einer["armeeliste"]
    }


def ausgewählteEinheitenIm(spielstand: dict) -> frozenset[str]:
    einheiten = einheitenDerArmeelisten(spielstand)
    return frozenset(name for name, einheit in einheiten.items() if einheit["ausgewählt"])


def ersterZugWählen(dienst, spielernummer: int):
    return dienst.put(f"/api/spieler/{spielernummer}/ersterZug")


def phaseBeenden(dienst, schlachtrunde: int, spielernummer: int, phase):
    körper = {"schlachtrunde": schlachtrunde, "spieler": spielernummer, "phase": phase.value}
    return dienst.put("/api/phaseBeenden", json=körper)


def modellAnklicken(dienst, aufstellung: Aufstellung, einheit: Einheit, modell: Modell):
    return dienst.put(f"{pfadDesModells(aufstellung, einheit, modell)}/anklicken")


def ausgewählteModelleIm(spielstand: dict) -> frozenset[tuple[float, float]]:
    return frozenset(
        (modell["x"], modell["y"]) for modell in spielstand["modelle"] if modell["ausgewählt"]
    )


def grenzenImSpielstand(grenzen: Iterable[tuple]) -> frozenset[tuple]:
    return frozenset(
        (
            frozenset((*stelleImSpielstand(stelle), float(radius)) for stelle, radius in kreise),
            *merkmale,
        )
        for kreise, *merkmale in grenzen
    )


def grenzenDerEinheitIm(spielstand: dict, einheitenname: str) -> frozenset[tuple]:
    kennung = kennungenDerEinheiten[einheitenname]
    return frozenset(
        (
            frozenset((kreis["x"], kreis["y"], kreis["radius"]) for kreis in grenze["kreise"]),
            grenze.get("wurf"),
            grenze.get("wählbar", False),
            grenze.get("nahkampfreichweite", False),
        )
        for grenze in spielstand["schlacht"]["grenzen"]
        if (grenze["spieler"], grenze["einheit"]) == kennung
    )
