"""Ergänzt am Hindernis im Fortschritt den Commit, der das Anliegen dazu angenommen hat."""

import re
from pathlib import Path

from gemeinsam.gitAufruf import gitAusgabe
from gemeinsam.pfade import anliegenOrdner
from lesen.anliegenKopf import Status, kopfAusText

hindernisMuster = re.compile(r"^ {2}Hindernis: .*\(Anliegen (\d+)\)$")
behoben = (Status.angenommen, Status.erledigt)


def anliegenDatei(wurzel: Path, nummer: str) -> str | None:
    """Der Pfad des Anliegens, auch eines gelöschten, aus der Geschichte."""
    gefunden = gitAusgabe(
        wurzel, "log", "--format=", "--name-only", "--", f"{anliegenOrdner}/{int(nummer):02d}-*.md"
    ).split()
    return gefunden[0] if gefunden else None


def beseitigendeBetreffe(wurzel: Path, pfad: str) -> list[str]:
    """Die Betreffe der Commits am Anliegen, jüngster zuerst; ohne den Commit, der es löschte."""
    betreffe = gitAusgabe(wurzel, "log", "--format=%s", "--", pfad).splitlines()
    return betreffe if (wurzel / pfad).is_file() else betreffe[1:]


def beseitigtDurch(wurzel: Path, nummer: str) -> str | None:
    """Der Betreff des Commits, der das Anliegen als angenommen oder erledigt festhält."""
    pfad = anliegenDatei(wurzel, nummer)
    if pfad is None:
        return None
    festgehalten = gitAusgabe(wurzel, "show", f"HEAD:{pfad}")
    gelesen = kopfAusText(festgehalten, Path(pfad))
    gelöscht = not festgehalten
    if not gelöscht and (gelesen is None or gelesen.status not in behoben):
        return None
    betreffe = beseitigendeBetreffe(wurzel, pfad)
    return betreffe[0] if betreffe else None


def beseitigtErgänzen(wurzel: Path, zusatz: list[str]) -> list[str]:
    """Die eingerückten Zeilen einer Fortschrittszeile; Hindernisse mit angenommenem Anliegen."""
    ergebnis = []
    for zeile in zusatz:
        treffer = hindernisMuster.match(zeile)
        betreff = beseitigtDurch(wurzel, treffer[1]) if treffer else None
        ergebnis.append(f"{zeile}; beseitigt: Commit „{betreff}“" if betreff else zeile)
    return ergebnis
