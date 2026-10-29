from pathlib import Path

from gemeinsam.gitAufruf import dateiBeiCommit, letzteFreigabe
from lesen.anliegenKopf import (
    Anliegen,
    Status,
    Ziel,
    gelesene,
    kopfAusText,
    stakeholder,
)
from standregeln.phasenfolge import lage


def nachprüfungen(wurzel: Path) -> dict[str, list[int]]:
    fällig: dict[str, list[int]] = {}
    for anliegen in gelesene(wurzel):
        if anliegen.status == Status.angenommen and not wartet(wurzel, anliegen):
            fällig.setdefault(anliegen.absender, []).append(anliegen.nummer)
    return fällig


def beantwortetDurchFreigabe(wurzel: Path, anliegen: Anliegen, freigabe: str | None) -> bool:
    if freigabe is None or anliegen.empfänger != stakeholder or anliegen.status != Status.offen:
        return False
    damals = kopfAusText(dateiBeiCommit(wurzel, freigabe, anliegen.datei), anliegen.datei)
    return damals is not None and (damals.status, damals.runde) == (Status.offen, anliegen.runde)


def wartetAuf(wurzel: Path, anliegen: Anliegen, freigabe: str | None) -> str | None:
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
    ziel = anliegen.wartetAuf
    if ziel is None or anliegen.status == Status.erledigt:
        return False
    if ziel.nummer is not None:
        return ziel.nummer in {andere.nummer for andere in gelesene(wurzel)}
    jetzt = lage(wurzel)
    späterer = ziel.zyklus is not None and jetzt.zyklus < ziel.zyklus
    return ziel.phase != str(jetzt.phase) or späterer


def wartende(wurzel: Path) -> dict[int, Ziel]:
    return {
        anliegen.nummer: anliegen.wartetAuf
        for anliegen in gelesene(wurzel)
        if anliegen.wartetAuf is not None and wartet(wurzel, anliegen)
    }


def dran(wurzel: Path) -> dict[str, list[int]]:
    zuständig: dict[str, list[int]] = {}
    freigabe = letzteFreigabe(wurzel)
    for anliegen in gelesene(wurzel):
        if wartet(wurzel, anliegen):
            continue
        rolle = wartetAuf(wurzel, anliegen, freigabe)
        if rolle and anliegen.status != Status.angenommen:
            zuständig.setdefault(rolle, []).append(anliegen.nummer)
    return zuständig
