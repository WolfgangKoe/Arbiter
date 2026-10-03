"""Liest den maschinenlesbaren Kopf der Anliegen (`prozess/ablauf.md`, Anliegen)."""

import re
from dataclasses import dataclass
from pathlib import Path

from agenten import rollennamen

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
    return sorted((wurzel / "handoff" / "anliegen").glob("*.md"))


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


def kopfVerstöße(datei: Path, wurzel: Path) -> list[str]:
    """Was am Kopf der Anliegen-Datei nicht stimmt; leer, wenn er in Ordnung ist."""
    zeilen = datei.read_text(encoding="utf-8").splitlines()
    if not zeilen or not zeilen[0].startswith("# "):
        return ["Zeile 1 ist kein Titel `# <Titel>`"]
    anliegen = kopfLesen(datei)
    if anliegen is None:
        return [
            "Zeile 3: Kopf `<nr> · <Typ> · von <Rolle> → <Rolle> · Runde <n>/3 · <Status>` erwartet"
        ]
    verstöße = []
    if not datei.name.startswith(f"{anliegen.nummer:02d}-"):
        verstöße.append(f"Nummer {anliegen.nummer} passt nicht zum Dateinamen")
    if anliegen.typ not in typWerte:
        verstöße.append(f"Typ {anliegen.typ} ist keiner von {', '.join(typWerte)}")
    if not 1 <= anliegen.runde <= höchstRunde:
        verstöße.append(f"Runde {anliegen.runde} liegt außerhalb von 1 bis {höchstRunde}")
    if anliegen.status not in statusWerte:
        verstöße.append(f"Status {anliegen.status} ist keiner von {', '.join(statusWerte)}")
    bekannt = {name.lower() for name in rollennamen(wurzel)} | {stakeholder.lower()}
    for rolle in (anliegen.absender, anliegen.empfänger):
        if rolle.lower() not in bekannt:
            verstöße.append(f"Rolle {rolle} gibt es nicht in .claude/agents/")
    return verstöße


def gelesene(wurzel: Path) -> list[Anliegen]:
    gelesen = (kopfLesen(datei) for datei in anliegenDateien(wurzel))
    return [anliegen for anliegen in gelesen if anliegen is not None]


def nachprüfungen(wurzel: Path) -> dict[str, list[int]]:
    """Fällige Nachprüfungen je Rolle: Anliegen mit Status `angenommen` prüft der Absender."""
    fällig: dict[str, list[int]] = {}
    for anliegen in gelesene(wurzel):
        if anliegen.status == "angenommen":
            fällig.setdefault(anliegen.absender, []).append(anliegen.nummer)
    return fällig


def nachprüfungenAlsText(wurzel: Path) -> str:
    fällig = nachprüfungen(wurzel)
    if not fällig:
        return ""
    teile = [
        f"{rolle} ({', '.join(f'{nummer:02d}' for nummer in nummern)})"
        for rolle, nummern in sorted(fällig.items())
    ]
    return "Nachprüfung fällig: " + ", ".join(teile)
