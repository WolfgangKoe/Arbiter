import re
from pathlib import Path

from gemeinsam.gitAufruf import gitAusgabe
from gemeinsam.pfade import anliegenOrdner
from lesen.anliegenKopf import Status, kopfAusText

hindernisMuster = re.compile(r"^ {2}Hindernis: .*\(Anliegen (\d+)\)$")
behoben = (Status.angenommen, Status.erledigt)


def anliegenDatei(wurzel: Path, nummer: str) -> str | None:
    gefunden = gitAusgabe(
        wurzel, "log", "--format=", "--name-only", "--", f"{anliegenOrdner}/{int(nummer):02d}-*.md"
    ).split()
    return gefunden[0] if gefunden else None


def beseitigendeBetreffe(wurzel: Path, pfad: str) -> list[str]:
    betreffe = gitAusgabe(wurzel, "log", "--format=%s", "--", pfad).splitlines()
    return betreffe if (wurzel / pfad).is_file() else betreffe[1:]


def beseitigtDurch(wurzel: Path, nummer: str) -> str | None:
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
    ergebnis = []
    for zeile in zusatz:
        treffer = hindernisMuster.match(zeile)
        betreff = beseitigtDurch(wurzel, treffer[1]) if treffer else None
        ergebnis.append(f"{zeile}; beseitigt: Commit „{betreff}“" if betreff else zeile)
    return ergebnis
