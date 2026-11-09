import re
from pathlib import Path
from typing import NamedTuple

from anliegenregeln.anliegenDran import dran
from gemeinsam.pfade import handoffOrdner
from lesen.plan import zyklus
from standregeln.fortschritt import bisherigeZeilen
from standregeln.phasenfolge import Phase, lage
from standregeln.wartendeSchritte import dateiJePhase

dateiDerPhase = {**dateiJePhase, Phase.prozessphase: "retro.md"}
nichtStartbar = ("Stakeholder", "Koordinator")
gruppenmuster = re.compile(r"Item ([^\s,]+)|^(P\d+)$|^(Anliegen \d+) ")
offenesHindernis = "- [ ] Hindernis"
auftrag = "Starte, was frei ist, oder nenne je den Grund"


class Fortschrittszeile(NamedTuple):
    rolle: str
    schritt: str
    abgehakt: bool
    hindert: bool
    gruppe: str | None


def gruppeVon(schritt: str) -> str | None:
    treffer = gruppenmuster.search(schritt)
    return next((teil for teil in treffer.groups() if teil), None) if treffer else None


def zeilenLesen(text: str) -> list[Fortschrittszeile]:
    zeilen = []
    for schlüssel, (abgehakt, zusatz) in bisherigeZeilen(text).items():
        rolle, _, schritt = schlüssel.partition(": ")
        hindert = any(offenesHindernis in eintrag for eintrag in zusatz)
        zeilen.append(Fortschrittszeile(rolle, schritt, abgehakt, hindert, gruppeVon(schritt)))
    return zeilen


def vorgänger(zeilen: list[Fortschrittszeile], stelle: int) -> list[Fortschrittszeile]:
    zeile = zeilen[stelle]
    return [
        frühere
        for frühere in zeilen[:stelle]
        if frühere.schritt != zeile.schritt
        and (zeile.gruppe is None or frühere.gruppe in (None, zeile.gruppe))
    ]


def istFrei(zeilen: list[Fortschrittszeile], stelle: int) -> bool:
    zeile = zeilen[stelle]
    if zeile.abgehakt or zeile.hindert or zeile.rolle in nichtStartbar:
        return False
    if zeile.gruppe and zeile.gruppe.startswith("Anliegen"):
        return False
    return all(frühere.abgehakt for frühere in vorgänger(zeilen, stelle))


def freieZeilen(text: str) -> dict[str, list[str]]:
    zeilen = zeilenLesen(text)
    frei: dict[str, list[str]] = {}
    for stelle, zeile in enumerate(zeilen):
        if istFrei(zeilen, stelle):
            frei.setdefault(zeile.rolle, []).append(zeile.schritt)
    return frei


def fortschrittstext(wurzel: Path) -> str:
    datei = wurzel / handoffOrdner / dateiDerPhase[lage(wurzel).phase]
    return datei.read_text(encoding="utf-8") if zyklus(datei) is not None else ""


def freiAlsText(wurzel: Path) -> str:
    frei = freieZeilen(fortschrittstext(wurzel))
    teile = [f"{rolle} ({', '.join(schritte)})" for rolle, schritte in frei.items()]
    if dran(wurzel):
        teile.append("die Anliegen unter Dran")
    return f"Frei: {', '.join(teile)} · {auftrag}" if teile else ""
