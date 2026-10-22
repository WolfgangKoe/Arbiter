"""Die laufende Technikphase aus den Commits `Freigabe Plan <n>` und das Alter von Zeilen."""

import re
from pathlib import Path

from gemeinsam.gitAufruf import freigaben, gitAusgabe

planFreigabe = "Freigabe Plan "
ersteGeprüfteTechnikphase = 7
blameKopf = re.compile(r"^([0-9a-f]{40}) \d+ (\d+)")


def jüngsterPlan(wurzel: Path) -> tuple[str, int] | None:
    """Kennung des Commits und Nummer der jüngsten `Freigabe Plan <n>`, sonst `None`."""
    for freigabe in freigaben(wurzel):
        nummer = freigabe.betreff.removeprefix(planFreigabe)
        if freigabe.betreff.startswith(planFreigabe) and nummer.isdigit():
            return freigabe.kennung, int(nummer)
    return None


def technikGeprüft(wurzel: Path) -> bool:
    """Ab der Technikphase 7 gilt die Kommentarregel auch unter `technik/`."""
    plan = jüngsterPlan(wurzel)
    return plan is not None and plan[1] >= ersteGeprüfteTechnikphase


def commitsJeZeile(wurzel: Path, relativ: str) -> dict[int, str]:
    """Je Zeile der Datei der Commit, der sie zuletzt geändert hat; Ungespeichertes fehlt."""
    commits = {}
    aktuell = ""
    zeilennummer = 0
    for zeile in gitAusgabe(wurzel, "blame", "--line-porcelain", "--", relativ).splitlines():
        if treffer := blameKopf.match(zeile):
            aktuell, zeilennummer = treffer.group(1), int(treffer.group(2))
        elif zeile.startswith("\t"):
            commits[zeilennummer] = aktuell
    return commits


def zeilenVorDerTechnikphase(wurzel: Path, relativ: str, zeilen: list[int]) -> list[int]:
    """Die Zeilen der Datei, die schon vor der jüngsten `Freigabe Plan` committet waren."""
    plan = jüngsterPlan(wurzel)
    if plan is None or not zeilen:
        return []
    ältere = set(gitAusgabe(wurzel, "rev-list", plan[0]).split())
    commits = commitsJeZeile(wurzel, relativ)
    return [zeile for zeile in zeilen if commits.get(zeile) in ältere]
