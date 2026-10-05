"""Liest die git-Unterbefehle eines Shell-Befehls; Rollen nutzen git nur lesend."""

from pathlib import Path

from rollenregeln.shellZerlegen import beginntBefehl, zerlegen

gitLesend = (
    "status",
    "log",
    "diff",
    "show",
    "grep",
    "ls-files",
    "ls-tree",
    "blame",
    "rev-parse",
    "shortlog",
    "cat-file",
    "describe",
)
gitOptionenMitWert = ("-C", "-c", "--git-dir", "--work-tree")


def unterbefehlNach(teile: list[str], stelle: int) -> str:
    """Das Wort nach `git` und seinen Optionen, `""` ohne Unterbefehl."""
    nächste = stelle + 1
    while nächste < len(teile) and teile[nächste].startswith("-"):
        nächste += 2 if teile[nächste] in gitOptionenMitWert else 1
    return teile[nächste] if nächste < len(teile) else ""


def gitUnterbefehle(befehl: str) -> list[str]:
    """Die Unterbefehle aller git-Aufrufe, auch in verketteten Befehlen."""
    teile = zerlegen(befehl.replace("\n", " ; "))
    if teile is None:
        return ["(nicht lesbar)"] if "git" in befehl else []
    return [
        unterbefehlNach(teile, stelle)
        for stelle, teil in enumerate(teile)
        if Path(teil).name == "git" and beginntBefehl(teile, stelle)
    ]
