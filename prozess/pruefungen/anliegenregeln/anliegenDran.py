"""Bestimmt, welche Rolle bei welchem Anliegen dran ist, nach der Statustabelle des Ablaufs."""

from pathlib import Path

from gemeinsam.gitAufruf import dateiBeiCommit, letzteFreigabe
from lesen.anliegenKopf import Anliegen, gelesene, kopfAusText, stakeholder


def nachprüfungen(wurzel: Path) -> dict[str, list[int]]:
    """Fällige Nachprüfungen je Rolle: Anliegen mit Status `angenommen` prüft der Absender."""
    fällig: dict[str, list[int]] = {}
    for anliegen in gelesene(wurzel):
        if anliegen.status == "angenommen":
            fällig.setdefault(anliegen.absender, []).append(anliegen.nummer)
    return fällig


def beantwortetDurchFreigabe(wurzel: Path, anliegen: Anliegen, freigabe: str | None) -> bool:
    """Ein Anliegen an den Stakeholder, das in der Freigabe schon so offen war (gleiche Runde)."""
    if freigabe is None or anliegen.empfänger != stakeholder or anliegen.status != "offen":
        return False
    damals = kopfAusText(dateiBeiCommit(wurzel, freigabe, anliegen.datei), anliegen.datei)
    return damals is not None and (damals.status, damals.runde) == ("offen", anliegen.runde)


def wartetAuf(wurzel: Path, anliegen: Anliegen, freigabe: str | None) -> str | None:
    """Die Rolle, die dran ist, nach der Statustabelle in `prozess/ablauf.md`."""
    if anliegen.status == "offen":
        beantwortet = beantwortetDurchFreigabe(wurzel, anliegen, freigabe)
        return anliegen.absender if beantwortet else anliegen.empfänger
    if anliegen.status in ("angenommen", "abgelehnt", "beantwortet"):
        return anliegen.absender
    if anliegen.status == "eskaliert":
        return stakeholder
    return None


def dran(wurzel: Path) -> dict[str, list[int]]:
    """Offene Anliegen je Rolle, die dran ist; `angenommen` steht bei `nachprüfungen`."""
    zuständig: dict[str, list[int]] = {}
    freigabe = letzteFreigabe(wurzel)
    for anliegen in gelesene(wurzel):
        rolle = wartetAuf(wurzel, anliegen, freigabe)
        if rolle and anliegen.status != "angenommen":
            zuständig.setdefault(rolle, []).append(anliegen.nummer)
    return zuständig
