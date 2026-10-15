"""Prozessregeln, Prämissen und Rollen schreibt nur die Prozessphase nach `Freigabe Retro`."""

from fnmatch import fnmatch
from pathlib import Path

from gemeinsam.gitAufruf import freigabeCommit
from standregeln.phasenfolge import Phase, lage

geschützteMuster = (
    "prozess/*.md",
    ".claude/agents/*",
    ".claude/skills/*",
    ".claude/rules/*",
    "CLAUDE.md",
    "*/CLAUDE.md",
)
ausgenommen = ("prozess/backlog.md", "prozess/pruefungen/*")
regelnMeldung = (
    "Prozessregeln, Prämissen und Rollen ändern sich nur in der Prozessphase nach "
    "`Freigabe Retro <n>`; davor beschreibt die Retro die Änderung."
)


def istGeschützt(relativ: str) -> bool:
    if any(fnmatch(relativ, muster) for muster in ausgenommen):
        return False
    return any(fnmatch(relativ, muster) for muster in geschützteMuster)


def prozessphaseFreigegeben(wurzel: Path) -> bool:
    """Die Prozessphase läuft, und `Freigabe Retro <n>` des laufenden Zyklus ist committet."""
    aktuell = lage(wurzel)
    if aktuell.phase != Phase.prozessphase:
        return False
    return freigabeCommit(wurzel, "Retro", aktuell.zyklus) is not None


def regelnGesperrt(relativ: str, wurzel: Path) -> bool:
    return istGeschützt(relativ) and not prozessphaseFreigegeben(wurzel)
