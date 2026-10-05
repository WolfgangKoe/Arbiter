"""Liest den maschinenlesbaren Kopf der Anliegen (`prozess/ablauf.md`, Anliegen)."""

import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from gemeinsam.pfade import anliegenOrdner


class Status(StrEnum):
    offen = "offen"
    angenommen = "angenommen"
    abgelehnt = "abgelehnt"
    beantwortet = "beantwortet"
    eskaliert = "eskaliert"
    erledigt = "erledigt"


typWerte = ("Kritik", "Fragen", "Anliegen")
höchstRunde = 3
kopfzeile = re.compile(
    rf"^(?P<nummer>\d+) · (?P<typ>\w+) · von (?P<absender>[^\s(]+)(?: \([^)]+\))?"
    rf" → (?P<empfänger>[^\s(]+)(?: \([^)]+\))?"
    rf" · Runde (?P<runde>\d+)/{höchstRunde} · (?P<status>\w+)$"
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
    status: Status | str  # Warum: ein unbekannter Text bleibt Text, `kopfVerstöße` meldet ihn


def statusAusText(text: str) -> Status | str:
    return Status(text) if text in Status.__members__ else text


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
        status=statusAusText(treffer["status"]),
    )


def gelesene(wurzel: Path) -> list[Anliegen]:
    gelesen = (kopfLesen(datei) for datei in anliegenDateien(wurzel))
    return [anliegen for anliegen in gelesen if anliegen is not None]
