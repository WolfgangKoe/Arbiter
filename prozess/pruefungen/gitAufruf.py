"""Ein lesender Aufruf von git im Projektordner."""

import subprocess
from pathlib import Path


def gitAusgabe(wurzel: Path, *argumente: str) -> str:
    return subprocess.run(
        ["git", *argumente], cwd=wurzel, capture_output=True, text=True, check=False
    ).stdout


def freigaben(wurzel: Path) -> list[tuple[str, str]]:
    """Kennung und Betreff aller Commits mit Betreff `Freigabe …`, jüngster zuerst."""
    gefunden = []
    for zeile in gitAusgabe(wurzel, "log", "--format=%H %s").splitlines():
        kennung, _, betreff = zeile.partition(" ")
        if betreff.startswith("Freigabe "):
            gefunden.append((kennung, betreff))
    return gefunden


def freigabeCommit(wurzel: Path, gegenstand: str, nummer: int) -> str | None:
    """Der Commit mit der Betreffzeile `Freigabe <gegenstand> <nummer>`, sonst `None`."""
    for kennung, betreff in freigaben(wurzel):
        if betreff == f"Freigabe {gegenstand} {nummer}":
            return kennung
    return None


def letzteFreigabe(wurzel: Path) -> str | None:
    """Der jüngste Commit, dessen Betreff mit `Freigabe ` beginnt, sonst `None`."""
    alle = freigaben(wurzel)
    return alle[0][0] if alle else None


def dateiBeiCommit(wurzel: Path, kennung: str, datei: Path) -> str:
    """Der Text der Datei im Commit; leer, wenn es sie dort nicht gab."""
    pfad = datei.resolve().relative_to(wurzel.resolve()).as_posix()
    return gitAusgabe(wurzel, "show", f"{kennung}:{pfad}")
