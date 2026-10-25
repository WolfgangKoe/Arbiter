"""Liest und schreibt den Kopf der Anliegen und vergibt freie Nummern (`ablauf/anliegen.md`)."""

import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from gemeinsam.gitAufruf import gitAusgabe
from gemeinsam.pfade import anliegenOrdner


class Status(StrEnum):
    offen = "offen"
    angenommen = "angenommen"
    abgelehnt = "abgelehnt"
    rückfrage = "rückfrage"
    beantwortet = "beantwortet"
    eskaliert = "eskaliert"
    erledigt = "erledigt"


typWerte = ("Kritik", "Fragen", "Anliegen", "Auftrag")
höchstRunde = 3
stakeholder = "Stakeholder"
wartetAufName = "Wartet auf"
feldNamen = ("Form", "Von", "An", "Runde", "Status", wartetAufName)
wartetAufFeld = re.compile(
    r"^(?P<nummer>\d+)$|^(?P<phase>(?:Domänen|Technik|Prozess)phase(?: \d+)?)$"
)
rundeFeld = re.compile(rf"^(\d+)/{höchstRunde}$")
dateinummer = re.compile(rf"{anliegenOrdner}/(\d+)-")


@dataclass(frozen=True)
class Anliegen:
    datei: Path
    nummer: int
    typ: str
    absender: str
    empfänger: str
    runde: int
    status: Status | str
    wartetAuf: str | None = None


def statusAusText(text: str) -> Status | str:
    return Status(text) if text in Status else text


def anliegenDateien(wurzel: Path) -> list[Path]:
    return sorted((wurzel / anliegenOrdner).glob("*.md"))


def kopfLesen(datei: Path) -> Anliegen | None:
    return kopfAusText(datei.read_text(encoding="utf-8"), datei)


def felderLesen(zeilen: list[str]) -> dict[str, str]:
    """Die Felder `Name: Wert` ab Zeile 3, solange eine Zeile ein bekanntes Feld ist."""
    felder: dict[str, str] = {}
    for zeile in zeilen[2:]:
        name, trenner, wert = zeile.partition(": ")
        if not trenner or name not in feldNamen:
            break
        felder[name] = wert.strip()
    return felder


def nummerAusDatei(datei: Path) -> int | None:
    vorn = datei.name.partition("-")[0]
    return int(vorn) if vorn.isdigit() else None


def kopfAusText(text: str, datei: Path) -> Anliegen | None:
    felder = felderLesen(text.splitlines())
    return anliegenAusFeldern(felder, datei) if felder else None


def ohnePerspektive(rolle: str) -> str:
    """Die Rolle ohne die Perspektive in Klammern, die der Ablauf nicht verlangt, aber duldet."""
    return rolle.partition(" (")[0]


def anliegenAusFeldern(felder: dict[str, str], datei: Path) -> Anliegen | None:
    nummer = nummerAusDatei(datei)
    runde = rundeFeld.match(felder.get("Runde", ""))
    wartet = wartetAufFeld.match(felder[wartetAufName]) if wartetAufName in felder else None
    if nummer is None or runde is None or set(felder) - {wartetAufName} != set(feldNamen[:5]):
        return None
    if wartetAufName in felder and wartet is None:
        return None
    return Anliegen(
        datei=datei,
        nummer=nummer,
        typ=felder["Form"],
        absender=ohnePerspektive(felder["Von"]),
        empfänger=ohnePerspektive(felder["An"]),
        runde=int(runde[1]),
        status=statusAusText(felder["Status"]),
        wartetAuf=(wartet["nummer"] or wartet["phase"]) if wartet else None,
    )


def kopfÄndern(text: str, änderungen: dict[str, str]) -> str | None:
    """Der Text mit den geänderten Feldern im Kopf; `None` ohne Kopf."""
    zeilen = text.splitlines()
    felder = felderLesen(zeilen)
    if not felder:
        return None
    ende = 2 + len(felder)
    felder = {**felder, **änderungen}
    kopf = [f"{name}: {felder[name]}" for name in feldNamen if name in felder]
    neu = [*zeilen[:2], *kopf, *zeilen[ende:]]
    return "\n".join(neu) + ("\n" if text.endswith("\n") else "")


def belegteNummern(wurzel: Path) -> set[int]:
    """Nummern im Ordner und in der Geschichte von git; sie sind nie wieder frei."""
    log = ("log", "--all", "--format=", "--name-only", "--", anliegenOrdner)
    geschichte = gitAusgabe(wurzel, *log)
    dateien = (wurzel / anliegenOrdner).glob("*.md")
    nummern = {nummerAusDatei(datei) for datei in dateien}
    return {nummer for nummer in nummern if nummer is not None} | {
        int(nummer) for nummer in dateinummer.findall(geschichte)
    }


def freieNummer(wurzel: Path, bereich: range) -> int | None:
    """Die erste Nummer im Bereich des Auftrags, die nie vergeben war; `None`, wenn er voll ist."""
    belegt = belegteNummern(wurzel)
    return next((nummer for nummer in bereich if nummer not in belegt), None)


def gelesene(wurzel: Path) -> list[Anliegen]:
    gelesen = (kopfLesen(datei) for datei in anliegenDateien(wurzel))
    return [anliegen for anliegen in gelesen if anliegen is not None]
