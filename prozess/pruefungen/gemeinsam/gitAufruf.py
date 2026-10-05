"""Alle Aufrufe von git im Projektordner, nur lesend."""

import subprocess
from pathlib import Path

from gemeinsam.pfade import relativZurWurzel


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


def betreffeSeit(wurzel: Path, kennung: str) -> list[str]:
    """Die Betreffzeilen aller Commits nach dem Commit `kennung`."""
    return gitAusgabe(wurzel, "log", "--format=%s", f"{kennung}..HEAD").splitlines()


def letzteFreigabe(wurzel: Path) -> str | None:
    """Der jüngste Commit `Freigabe …`, sonst `None`."""
    alle = freigaben(wurzel)
    return alle[0][0] if alle else None


def letzteFreigabeOhneReview(wurzel: Path) -> str | None:
    """Der jüngste Commit `Freigabe …` außer `Freigabe Review …`, sonst `None`."""
    # Warum: Die Freigabe des Reviews schließt keine Kritik am Code ab; das Fenster bleibt offen.
    alle = [
        kennung
        for kennung, betreff in freigaben(wurzel)
        if not betreff.startswith("Freigabe Review ")
    ]
    return alle[0] if alle else None


def dateiBeiCommit(wurzel: Path, kennung: str, datei: Path) -> str:
    """Der Text der Datei im Commit; leer, wenn es sie dort nicht gab."""
    pfad = relativZurWurzel(datei, wurzel)
    assert pfad is not None, f"{datei} liegt außerhalb von {wurzel}"
    return gitAusgabe(wurzel, "show", f"{kennung}:{pfad}")


def geänderteDateien(wurzel: Path) -> set[str]:
    """Pfade der geänderten und neuen Dateien (`git status --porcelain`)."""
    ausgabe = gitAusgabe(wurzel, "status", "--porcelain", "--untracked-files=all")
    return {zeile[3:].split(" -> ")[-1] for zeile in ausgabe.splitlines() if zeile}


def kopfCommit(wurzel: Path) -> str:
    return gitAusgabe(wurzel, "rev-parse", "HEAD").strip()


def blobGröße(wurzel: Path, angabe: str) -> int | None:
    """Größe von `<rev>:<pfad>` in Byte (mindestens die Zeichenzahl); `None`, wenn unbekannt."""
    ausgabe = gitAusgabe(wurzel, "cat-file", "-s", angabe)
    return int(ausgabe) if ausgabe.strip().isdigit() else None
