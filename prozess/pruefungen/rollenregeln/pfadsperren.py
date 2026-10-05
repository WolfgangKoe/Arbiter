"""Erkennt, ob ein Bash-Befehl einen gesperrten Pfad ändert, und nennt die Meldung dazu."""

from collections.abc import Callable
from pathlib import Path

from gemeinsam.pfade import (
    anliegenOrdner,
    handoffOrdner,
    istNurLesbar,
    nurLesbar,
    relativZurWurzel,
)
from lesen.artefakt import artefakte
from rollenregeln.shellZerlegen import zerlegen

trennOperatoren = {";", "&", "&&", "|", "||", "(", ")"}
umleitungen = {">", ">>", ">|", "&>"}

# Warum: Befehle, die jedes Pfadargument ändern; bei Kopierbefehlen zählt nur das Ziel.
ändernAlle = {
    "rm",
    "unlink",
    "shred",
    "truncate",
    "touch",
    "tee",
    "chmod",
    "chown",
    "mkdir",
    "rmdir",
    "patch",
    "dd",
    "mv",
}
ändernZiel = {"cp", "ln", "rsync", "install"}


def istAnliegen(relativerPfad: str) -> bool:
    return relativerPfad.startswith(f"{anliegenOrdner}/")


def istFreigabeArtefakt(relativerPfad: str) -> bool:
    return relativerPfad in {f"{handoffOrdner}/{artefakt.datei}" for artefakt in artefakte}


def meintPfad(wort: str, wurzel: Path, gesperrt: Callable[[str], bool]) -> bool:
    """Ob ein Pfadwort auf einen gesperrten Pfad zeigt (relativ, absolut oder mit `..`)."""
    pfad = wort.split("=", 1)[-1] if wort.startswith(("of=", "--file=")) else wort
    if not pfad or pfad.startswith("-"):
        return False
    relativ = relativZurWurzel(Path(pfad), wurzel)
    return relativ is not None and gesperrt(relativ)


def ändertPfad(befehl: str, wurzel: Path, gesperrt: Callable[[str], bool]) -> bool:
    """Heuristik für Bash: Umleitung, rm, mv, cp (Ziel), sed -i auf einen gesperrten Pfad."""
    teile = zerlegen(befehl.replace("\n", " ; "))
    if teile is None:
        return False
    segment: list[str] = []
    segmente = [segment]
    for stelle, teil in enumerate(teile):
        if teil in trennOperatoren:
            segment = []
            segmente.append(segment)
        elif teil in umleitungen:
            ziel = teile[stelle + 1] if stelle + 1 < len(teile) else ""
            if meintPfad(ziel, wurzel, gesperrt):
                return True
        else:
            segment.append(teil)
    return any(segmentÄndert(wörterDesSegments, wurzel, gesperrt) for wörterDesSegments in segmente)


def segmentÄndert(segment: list[str], wurzel: Path, gesperrt: Callable[[str], bool]) -> bool:
    if not segment:
        return False
    befehl, *argumente = segment
    name = Path(befehl).name
    pfade = [argument for argument in argumente if not argument.startswith("-")]
    if name in ändernAlle:
        return any(meintPfad(argument, wurzel, gesperrt) for argument in argumente)
    if name in ändernZiel:
        return bool(pfade) and meintPfad(pfade[-1], wurzel, gesperrt)
    if name == "sed" and any(argument.startswith(("-i", "--in-place")) for argument in argumente):
        return any(meintPfad(argument, wurzel, gesperrt) for argument in pfade)
    return False


pfadsperren = (
    (
        istNurLesbar,
        f"Dieser Pfad ist nur lesbar, für alle Rollen: {', '.join(nurLesbar)}. "
        "Löschen tut nur der Stakeholder.",
    ),
    (
        istAnliegen,
        "Anliegen ändern Rollen nur mit Write und Edit, nie per Bash: Daran vorbei "
        "greifen Statusrecht und Nummernprüfung nicht (prozess/ablauf.md, Anliegen).",
    ),
    (
        istFreigabeArtefakt,
        "Plan, Review und Retro ändern Rollen nur mit Write und Edit, nie per Bash: Daran "
        "vorbei greift die Freigabesperre nicht (prozess/ablauf.md, Freigabe und Kommentare).",
    ),
)
