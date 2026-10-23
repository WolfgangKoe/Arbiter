"""Bestimmt, welche Rolle bei welchem Anliegen dran ist, nach der Statustabelle des Ablaufs."""

from pathlib import Path

from gemeinsam.gitAufruf import dateiBeiCommit, letzteFreigabe
from lesen.anliegenKopf import Anliegen, Status, gelesene, kopfAusText, stakeholder
from standregeln.phasenfolge import lage


def nachprüfungen(wurzel: Path) -> dict[str, list[int]]:
    """Fällige Nachprüfungen je Rolle: `angenommen` prüft der Absender, Wartende nicht."""
    fällig: dict[str, list[int]] = {}
    for anliegen in gelesene(wurzel):
        if anliegen.status == Status.angenommen and not wartet(wurzel, anliegen):
            fällig.setdefault(anliegen.absender, []).append(anliegen.nummer)
    return fällig


def beantwortetDurchFreigabe(wurzel: Path, anliegen: Anliegen, freigabe: str | None) -> bool:
    """Ein Anliegen an den Stakeholder, das in der Freigabe schon so offen war (gleiche Runde)."""
    if freigabe is None or anliegen.empfänger != stakeholder or anliegen.status != Status.offen:
        return False
    damals = kopfAusText(dateiBeiCommit(wurzel, freigabe, anliegen.datei), anliegen.datei)
    return damals is not None and (damals.status, damals.runde) == (Status.offen, anliegen.runde)


def wartetAuf(wurzel: Path, anliegen: Anliegen, freigabe: str | None) -> str | None:
    """Die Rolle, die dran ist, nach der Statustabelle in `prozess/ablauf.md`."""
    if anliegen.status == Status.offen:
        beantwortet = beantwortetDurchFreigabe(wurzel, anliegen, freigabe)
        return anliegen.absender if beantwortet else anliegen.empfänger
    if anliegen.status in (
        Status.angenommen,
        Status.abgelehnt,
        Status.beantwortet,
        Status.rückfrage,
    ):
        return anliegen.absender
    if anliegen.status == Status.eskaliert:
        return stakeholder
    return None


def wartet(wurzel: Path, anliegen: Anliegen) -> bool:
    """Das Anliegen wartet noch: auf ein anderes im Ordner oder auf die Prozessphase."""
    if anliegen.wartetAuf is None or anliegen.status == Status.erledigt:
        return False
    if not anliegen.wartetAuf.isdigit():
        return anliegen.wartetAuf != str(lage(wurzel).phase)
    return int(anliegen.wartetAuf) in {andere.nummer for andere in gelesene(wurzel)}


def wartende(wurzel: Path) -> dict[int, str]:
    """Wartende Anliegen mit dem, worauf sie warten; sie sind für niemanden dran."""
    return {
        anliegen.nummer: str(anliegen.wartetAuf)
        for anliegen in gelesene(wurzel)
        if wartet(wurzel, anliegen)
    }


def dran(wurzel: Path) -> dict[str, list[int]]:
    """Offene Anliegen je Rolle, die dran ist; `angenommen` steht bei `nachprüfungen`."""
    zuständig: dict[str, list[int]] = {}
    freigabe = letzteFreigabe(wurzel)
    for anliegen in gelesene(wurzel):
        if wartet(wurzel, anliegen):
            continue
        rolle = wartetAuf(wurzel, anliegen, freigabe)
        if rolle and anliegen.status != Status.angenommen:
            zuständig.setdefault(rolle, []).append(anliegen.nummer)
    return zuständig
