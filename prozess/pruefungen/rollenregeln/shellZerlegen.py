"""Zerlegt einen Shell-Befehl in Wörter wie die Shell und entfernt Heredoc-Texte."""

import re
import shlex
from pathlib import Path

operatorZeichen = set(";&|<>()")
heredoc = re.compile(
    r"^(?P<kopf>[^\n]*?)<<-?\s*(?P<quote>['\"]?)(?P<ende>\w+)(?P=quote)[^\n]*\n"
    r".*?\n[ \t]*(?P=ende)[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
shells = {"bash", "sh", "zsh", "dash", "eval", "source", "."}


def ohneHeredocText(befehl: str) -> str:
    """Entfernt Heredoc-Texte (etwa `cat > datei <<EOF`), außer sie füttern eine Shell."""

    def ersetzen(treffer: re.Match) -> str:
        kopf = treffer["kopf"]
        wörterImKopf = kopf.replace(";", " ").replace("&", " ").replace("|", " ").split()
        if wörterImKopf and Path(wörterImKopf[-1]).name in shells:
            return treffer.group(0)
        return kopf

    return heredoc.sub(ersetzen, befehl)


def zerlegen(befehl: str) -> list[str] | None:
    zerleger = shlex.shlex(befehl, posix=True, punctuation_chars=True)
    zerleger.whitespace_split = True
    try:
        return list(zerleger)
    except ValueError:
        return None


def wörter(befehl: str) -> list[str] | None:
    """Zerlegt wie die Shell; `None`, wenn der Befehl Verkettung oder Umleitung enthält."""
    if "$(" in befehl or "`" in befehl or "\n" in befehl:
        return None
    teile = zerlegen(befehl)
    if teile is None or any(teil and set(teil) <= operatorZeichen for teil in teile):
        return None
    return teile


def beginntBefehl(teile: list[str], stelle: int) -> bool:
    """Ob das Wort an `stelle` ein Befehlsname ist: am Anfang oder nach einem Operator."""
    return stelle == 0 or set(teile[stelle - 1]) <= operatorZeichen
