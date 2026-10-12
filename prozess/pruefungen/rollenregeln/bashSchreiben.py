"""Erkennt Bash-Befehle, die Dateien im Projekt ändern oder committen."""

import os
import shlex
import tempfile
from collections.abc import Callable
from pathlib import PurePosixPath

Entfernen = Callable[[str, list[str]], str | None]

ablage = PurePosixPath(tempfile.gettempdir())
trennzeichen = {";", "&&", "||", "|", "&", "(", ")", "|&"}
umleitungen = {">", ">>", ">|"}
umhüllungen = {"sudo", "env", "command", "time", "nohup", "nice"}
gitÄnderungen = {"add", "commit", "checkout", "restore", "reset", "stash", "rm", "mv"}
alleZieleFrei = {"rm", "mv", "touch", "tee"}
nurZielFrei = {"cp"}
löschenUndUmbenennen = {"rm", "mv"}
pythonMitSkriptInDerEingabe = {"-", "-c"}
weg = "Nimm Write und Edit; Bash nur zum Lesen, für Prüfungen und Tests und in /tmp."


def liegtInTmp(pfad: str) -> bool:
    if pfad == os.devnull:
        return True
    teile = PurePosixPath(pfad).parts
    return ".." not in teile and teile[:2] == (ablage.parts[0], ablage.parts[1])


class Umleitung(str):
    """Ein unquotiertes `>`, `>>` oder `>|` im Befehl."""


def ohneAnführung(wort: str) -> str:
    if len(wort) > 1 and wort[0] == wort[-1] and wort[0] in "'\"":
        return wort[1:-1]
    return Umleitung(wort) if wort in umleitungen else wort


def zerlegen(befehl: str) -> list[list[str]]:
    """Die Wörter je Teilbefehl; Zeilenumbrüche, `;`, `&&`, `||` und `|` trennen."""
    # Warum: Ohne `posix` behalten Wörter ihre Anführungszeichen, `'>'` bleibt kein Operator.
    lexer = shlex.shlex(befehl.replace("\n", " ; "), posix=False, punctuation_chars=True)
    lexer.whitespace_split = True
    teile: list[list[str]] = [[]]
    for wort in lexer:
        if wort in trennzeichen:
            teile.append([])
        else:
            teile[-1].append(ohneAnführung(wort))
    return [teil for teil in teile if teil]


def umleitungImProjekt(wörter: list[str]) -> str | None:
    for stelle, wort in enumerate(wörter):
        ziel = wörter[stelle + 1] if stelle + 1 < len(wörter) else ""
        if isinstance(wort, Umleitung) and not liegtInTmp(ziel):
            return f"Umleitung nach {ziel or '?'}"
    return None


def istUmhüllung(wort: str) -> bool:
    return wort in umhüllungen or "=" in wort.split("/")[0]


def ohneUmhüllung(wörter: list[str]) -> list[str]:
    stelle = 0
    while stelle < len(wörter) and istUmhüllung(wörter[stelle]):
        stelle += 1
    return wörter[stelle:]


def argumente(wörter: list[str]) -> list[str]:
    return [wort for wort in wörter[1:] if not wort.startswith("-")]


def gitÄndertImProjekt(wörter: list[str]) -> str | None:
    stelle = 1
    verzeichnis = ""
    while stelle < len(wörter) and wörter[stelle].startswith("-"):
        if wörter[stelle] in ("-C", "-c") and stelle + 1 < len(wörter):
            verzeichnis = wörter[stelle + 1] if wörter[stelle] == "-C" else verzeichnis
            stelle += 1
        stelle += 1
    unterbefehl = wörter[stelle] if stelle < len(wörter) else ""
    if unterbefehl in gitÄnderungen and not liegtInTmp(verzeichnis):
        return f"git {unterbefehl}"
    return None


def ändertInPlace(wort: str) -> bool:
    kurz = wort.startswith("-") and not wort.startswith("--") and "i" in wort
    return wort.startswith("--in-place") or kurz


def entfernenName(wörter: list[str]) -> str:
    """`rm` oder `mv`, sonst leer."""
    wörter = ohneUmhüllung(wörter)
    name = PurePosixPath(wörter[0]).name if wörter else ""
    return name if name in löschenUndUmbenennen else ""


def grundGegenEntfernen(wörter: list[str], entfernen: Entfernen, *, gewechselt: bool) -> str | None:
    wörter = ohneUmhüllung(wörter)
    name = PurePosixPath(wörter[0]).name
    # Warum: Nach einem `cd` ins Projekt sind relative Pfade nicht mehr prüfbar.
    return f"{name} nach cd" if gewechselt else entfernen(name, wörter[1:])


def urteilenÜber(
    wörter: list[str], *, inTmp: bool, gewechselt: bool, entfernen: Entfernen | None
) -> str | None:
    umleitung = umleitungImProjekt(wörter)
    if umleitung or not (entfernen and entfernenName(wörter) and not inTmp):
        return umleitung or befehlImProjekt(wörter, inTmp=inTmp)
    return grundGegenEntfernen(wörter, entfernen, gewechselt=gewechselt)


def befehlImProjekt(wörter: list[str], *, inTmp: bool) -> str | None:
    wörter = ohneUmhüllung(wörter)
    if not wörter:
        return None
    name = PurePosixPath(wörter[0]).name
    if name == "git":
        return None if inTmp else gitÄndertImProjekt(wörter)
    if name == "sed" and any(ändertInPlace(wort) for wort in wörter[1:]):
        return "sed -i"
    erstes = wörter[1:2]
    if name.startswith("python") and any(wort in pythonMitSkriptInDerEingabe for wort in erstes):
        return f"{name} {wörter[1]}"
    ziele = argumente(wörter)
    if name in nurZielFrei and ziele and not liegtInTmp(ziele[-1]):
        return name
    if name in alleZieleFrei and not all(liegtInTmp(ziel) for ziel in ziele):
        return name
    return None


def verbotenesSchreiben(befehl: str, entfernen: Entfernen | None = None) -> str | None:
    """Der Teil des Befehls, der im Projekt schreibt oder committet; sonst `None`."""
    try:
        teile = zerlegen(befehl)
    except ValueError:
        return "Befehl nicht lesbar"
    inTmp = False
    gewechselt = False
    for wörter in teile:
        gefunden = urteilenÜber(wörter, inTmp=inTmp, gewechselt=gewechselt, entfernen=entfernen)
        if gefunden:
            return gefunden
        if wörter[0] == "cd" and len(wörter) > 1:
            inTmp = liegtInTmp(wörter[1])
            gewechselt = gewechselt or not inTmp
    return None
