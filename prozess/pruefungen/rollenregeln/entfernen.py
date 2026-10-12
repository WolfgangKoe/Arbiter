"""Urteilt, ob eine Rolle mit `rm` oder `mv` löschen und umbenennen darf."""

import subprocess
from pathlib import Path

from gemeinsam.pfade import anliegenOrdner, istNurLesbar, relativZurWurzel
from lesen.agenten import darfSchreiben, schreibpfade
from rollenregeln.bashSchreiben import liegtInTmp

erlaubteOptionen = {"rm": "fv", "mv": "fvn"}
platzhalter = set("*?[]{}$`~\\!")


def istCommittet(relativ: str, wurzel: Path) -> bool:
    ergebnis = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{relativ}"], cwd=wurzel, capture_output=True
    )
    return ergebnis.returncode == 0


def optionenUndPfade(wörter: list[str]) -> tuple[list[str], list[str]]:
    optionen: list[str] = []
    pfade: list[str] = []
    nachTrenner = False
    for wort in wörter:
        if nachTrenner or not wort.startswith("-") or wort == "-":
            pfade.append(wort)
        elif wort == "--":
            nachTrenner = True
        else:
            optionen.append(wort)
    return optionen, pfade


def unerlaubteOption(name: str, optionen: list[str]) -> str | None:
    for option in optionen:
        if option.startswith("--") or not set(option[1:]) <= set(erlaubteOptionen[name]):
            return option
    return None


def grundGegenPfad(relativ: str, rolle: str, wurzel: Path, *, istZielordner: bool) -> str | None:
    if istNurLesbar(relativ):
        return f"{relativ} ist nur lesbar"
    if not darfSchreiben(relativ, schreibpfade(rolle, wurzel)):
        return f"{rolle} darf {relativ} nicht schreiben"
    if (wurzel / relativ).is_dir() and not istZielordner:
        return f"{relativ} ist ein Ordner"
    inAnliegen = relativ.startswith(f"{anliegenOrdner}/")
    if inAnliegen and istCommittet(relativ, wurzel):
        return f"{relativ} ist schon committet"
    return None


def urteil(name: str, wörter: list[str], rolle: str, wurzel: Path) -> str | None:
    """Der Grund, warum `rm` oder `mv` nicht zulässig ist; `None`, wenn jeder Pfad frei ist."""
    optionen, pfade = optionenUndPfade(wörter)
    falsch = unerlaubteOption(name, optionen)
    if falsch:
        return f"{name} {falsch}: erlaubt sind nur -{erlaubteOptionen[name]}"
    if len(pfade) < (2 if name == "mv" else 1):
        return f"{name} ohne Pfade"
    for stelle, pfad in enumerate(pfade):
        istZiel = name == "mv" and stelle == len(pfade) - 1
        if liegtInTmp(pfad):
            continue
        if platzhalter & set(pfad):
            return f"{name} {pfad}: Platzhalter und Variablen sind nicht prüfbar"
        relativ = relativZurWurzel(Path(pfad), wurzel)
        grund = f"{pfad} liegt außerhalb des Projekts" if relativ is None else None
        grund = grund or grundGegenPfad(relativ or "", rolle, wurzel, istZielordner=istZiel)
        if grund:
            return f"{name}: {grund}"
    return None
