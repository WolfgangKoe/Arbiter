"""Ein lesender Aufruf von git im Projektordner."""

import re
import subprocess
from pathlib import Path


def gitAusgabe(wurzel: Path, *argumente: str) -> str:
    return subprocess.run(
        ["git", *argumente], cwd=wurzel, capture_output=True, text=True, check=False
    ).stdout


def freigabeCommit(wurzel: Path, gegenstand: str, nummer: int) -> str | None:
    """Der Commit mit der Betreffzeile `Freigabe <gegenstand> <nummer>`, sonst `None`."""
    for zeile in gitAusgabe(wurzel, "log", "--format=%H %s").splitlines():
        kennung, _, betreff = zeile.partition(" ")
        if betreff == f"Freigabe {gegenstand} {nummer}":
            return kennung
    return None


def jüngsteFreigabe(wurzel: Path) -> str | None:
    """Der jüngste Commit mit dem Betreff `Freigabe <Etappe|Plan|Retro> <n>`, sonst `None`."""
    for zeile in gitAusgabe(wurzel, "log", "--format=%H %s").splitlines():
        kennung, _, betreff = zeile.partition(" ")
        if re.fullmatch(r"Freigabe (Etappe|Plan|Retro) \d+", betreff):
            return kennung
    return None


def seitFreigabeUnverändert(wurzel: Path, datei: Path) -> bool:
    """Die Datei ist committet, ohne Änderung im Arbeitsbaum, und ihre letzte Änderung liegt
    nicht nach der jüngsten Freigabe (der Freigabe-Commit selbst zählt noch dazu)."""
    freigabe = jüngsteFreigabe(wurzel)
    pfad = str(datei.resolve().relative_to(wurzel.resolve()))
    if freigabe is None or gitAusgabe(wurzel, "status", "--porcelain", "--", pfad).strip():
        return False
    letzte = gitAusgabe(wurzel, "log", "-1", "--format=%H", "--", pfad).strip()
    return (
        bool(letzte)
        and letzte == gitAusgabe(wurzel, "log", "-1", "--format=%H", freigabe, "--", pfad).strip()
    )
