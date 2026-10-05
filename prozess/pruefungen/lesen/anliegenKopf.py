"""Liest den maschinenlesbaren Kopf der Anliegen (`prozess/ablauf.md`, Anliegen)."""

import re
from dataclasses import dataclass
from pathlib import Path

from gemeinsam.pfade import anliegenOrdner

statusWerte = ("offen", "angenommen", "abgelehnt", "beantwortet", "eskaliert", "erledigt")
typWerte = ("Kritik", "Fragen", "Anliegen")
höchstRunde = 3
kopfzeile = re.compile(
    r"^(?P<nummer>\d+) · (?P<typ>\w+) · von (?P<absender>[^\s(]+)(?: \([^)]+\))?"
    r" → (?P<empfänger>[^\s(]+)(?: \([^)]+\))? · Runde (?P<runde>\d+)/3 · (?P<status>\w+)$"
)
stakeholder = "Stakeholder"


@dataclass(frozen=True)
class Anliegen:
    datei: Path
    nummer: int
    typ: str
    absender: str
    empfänger: str
    runde: int
    status: str


def anliegenDateien(wurzel: Path) -> list[Path]:
    return sorted((wurzel / anliegenOrdner).glob("*.md"))


def kopfLesen(datei: Path) -> Anliegen | None:
    return kopfAusText(datei.read_text(encoding="utf-8"), datei)


def kopfAusText(text: str, datei: Path) -> Anliegen | None:
    zeilen = text.splitlines()
    dritteZeile = zeilen[2:3]
    treffer = kopfzeile.match(dritteZeile[0]) if dritteZeile else None
    if treffer is None:
        return None
    return Anliegen(
        datei=datei,
        nummer=int(treffer["nummer"]),
        typ=treffer["typ"],
        absender=treffer["absender"],
        empfänger=treffer["empfänger"],
        runde=int(treffer["runde"]),
        status=treffer["status"],
    )


def gelesene(wurzel: Path) -> list[Anliegen]:
    gelesen = (kopfLesen(datei) for datei in anliegenDateien(wurzel))
    return [anliegen for anliegen in gelesen if anliegen is not None]
