"""Alle Aufrufe von git im Projektordner, nur lesend."""

import subprocess
from pathlib import Path
from typing import NamedTuple

from gemeinsam.pfade import relativZurWurzel


class Freigabe(NamedTuple):
    kennung: str
    betreff: str


def gitAusgabe(wurzel: Path, *argumente: str) -> str:
    return subprocess.run(
        ["git", *argumente], cwd=wurzel, capture_output=True, text=True, check=False
    ).stdout


def freigaben(wurzel: Path) -> list[Freigabe]:
    """Kennung und Betreff aller Commits mit Betreff `Freigabe …`, jüngster zuerst."""
    gefunden = []
    for zeile in gitAusgabe(wurzel, "log", "--format=%H %s").splitlines():
        kennung, _, betreff = zeile.partition(" ")
        if betreff.startswith("Freigabe "):
            gefunden.append(Freigabe(kennung, betreff))
    return gefunden


def freigabeCommit(wurzel: Path, gegenstand: str, nummer: int) -> str | None:
    """Der Commit mit der Betreffzeile `Freigabe <gegenstand> <nummer>`, sonst `None`."""
    for freigabe in freigaben(wurzel):
        if freigabe.betreff == f"Freigabe {gegenstand} {nummer}":
            return freigabe.kennung
    return None


def letzteFreigabe(wurzel: Path) -> str | None:
    """Der jüngste Commit `Freigabe …`, sonst `None`."""
    alle = freigaben(wurzel)
    return alle[0].kennung if alle else None


def dateiBeiCommit(wurzel: Path, kennung: str, datei: Path) -> str:
    """Der Text der Datei im Commit; leer, wenn es sie dort nicht gab."""
    pfad = relativZurWurzel(datei, wurzel)
    assert pfad is not None, f"{datei} liegt außerhalb von {wurzel}"
    return gitAusgabe(wurzel, "show", f"{kennung}:{pfad}")
