import re
from pathlib import Path

from gemeinsam.gitAufruf import gitAusgabe
from gemeinsam.pfade import anliegenOrdner
from lesen.anliegenKopf import Status, anliegenDateien, kopfAusText, nummerAusDatei

hindernisMuster = re.compile(r"^ {2}Hindernis: .*\(Anliegen (\d+)\)$")
behoben = (Status.angenommen, Status.erledigt)


def anliegenDatei(wurzel: Path, nummer: str) -> str | None:
    gefunden = gitAusgabe(
        wurzel, "log", "--format=", "--name-only", "--", f"{anliegenOrdner}/{int(nummer):02d}-*.md"
    ).split()
    return gefunden[0] if gefunden else None


def beseitigendeBetreffe(wurzel: Path, pfad: str, festgehalten: str) -> list[str]:
    betreffe = gitAusgabe(wurzel, "log", "--format=%s", "--", pfad).splitlines()
    return betreffe if festgehalten else betreffe[1:]


def istUnverändert(datei: Path, festgehalten: str) -> bool:
    if not datei.is_file():
        return not festgehalten
    return datei.read_text(encoding="utf-8") == festgehalten


def beseitigtDurch(wurzel: Path, nummer: str) -> str | None:
    pfad = anliegenDatei(wurzel, nummer)
    if pfad is None:
        return None
    festgehalten = gitAusgabe(wurzel, "show", f"HEAD:{pfad}")
    gelesen = kopfAusText(festgehalten, Path(pfad))
    erledigt = gelesen is not None and gelesen.status in behoben
    gelöschtVomHook = erledigt and not (wurzel / pfad).is_file()
    if not (gelöschtVomHook or istUnverändert(wurzel / pfad, festgehalten)):
        return None
    if festgehalten and not erledigt:
        return None
    betreffe = beseitigendeBetreffe(wurzel, pfad, festgehalten)
    return betreffe[0] if betreffe else None


def anliegenBesteht(wurzel: Path, nummer: str) -> bool:
    vorhanden = any(nummerAusDatei(datei) == int(nummer) for datei in anliegenDateien(wurzel))
    return vorhanden or anliegenDatei(wurzel, nummer) is not None


def verwaisteFallenLassen(wurzel: Path, zusatz: list[str]) -> list[str]:
    behalten = []
    for zeile in zusatz:
        treffer = hindernisMuster.match(zeile)
        if treffer is None or anliegenBesteht(wurzel, treffer[1]):
            behalten.append(zeile)
    return behalten


def beseitigtErgänzen(wurzel: Path, zusatz: list[str]) -> list[str]:
    ergebnis = []
    for zeile in zusatz:
        treffer = hindernisMuster.match(zeile)
        betreff = beseitigtDurch(wurzel, treffer[1]) if treffer else None
        ergebnis.append(f"{zeile}; beseitigt: Commit „{betreff}“" if betreff else zeile)
    return ergebnis
