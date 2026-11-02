from fnmatch import fnmatch
from pathlib import Path

from gemeinsam.gitAufruf import freigabeCommit
from gemeinsam.pfade import handoffOrdner
from lesen.plan import zyklus
from standregeln.phasenfolge import Phase, lage, offenesProzessItem

geschützteMuster = (
    "prozess/*.md",
    ".claude/agents/*",
    ".claude/skills/*",
    ".claude/rules/*",
    "CLAUDE.md",
    "*/CLAUDE.md",
)
ausgenommen = ("prozess/backlog.md", "prozess/pruefungen/*")
regelumsetzer = "regelumsetzer"
regelnMuster = "prozess/regeln/*.md"
regelnAusnahme = "prozess/regeln/CLAUDE.md"
regelnMeldung = (
    "Prozessregeln, Prämissen und Rollen ändern sich nur in der Prozessphase nach "
    "`Freigabe Retro <n>`; davor beschreibt die Retro die Änderung."
)


def istGeschützt(relativ: str) -> bool:
    if any(fnmatch(relativ, muster) for muster in ausgenommen):
        return False
    return any(fnmatch(relativ, muster) for muster in geschützteMuster)


def retroMitOffenemProzessItem(wurzel: Path) -> bool:
    retro = zyklus(wurzel / handoffOrdner / "retro.md")
    if retro is None:
        return False
    freigabe = freigabeCommit(wurzel, "Retro", retro)
    return freigabe is not None and offenesProzessItem(wurzel, retro, freigabe) is not None


def prozessphaseFreigegeben(wurzel: Path) -> bool:
    if retroMitOffenemProzessItem(wurzel):
        return True
    aktuell = lage(wurzel)
    if aktuell.phase != Phase.prozessphase:
        return False
    return freigabeCommit(wurzel, "Retro", aktuell.zyklus) is not None


def regelnGesperrt(relativ: str, wurzel: Path, rolle: str | None = None) -> bool:
    if rolle == regelumsetzer and fnmatch(relativ, regelnMuster) and relativ != regelnAusnahme:
        return False
    return istGeschützt(relativ) and not prozessphaseFreigegeben(wurzel)
