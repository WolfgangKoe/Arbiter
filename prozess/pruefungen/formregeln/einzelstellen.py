"""Was in den Prüfskripten nur an einer Stelle stehen darf (Anliegen 253, Punkte 3 und 4)."""

import ast
import re
import sys
from pathlib import Path
from typing import NamedTuple

from gemeinsam.pfade import projektordner, relativZurWurzel

prüfskripteOrdner = "prozess/pruefungen"


class Einzelstelle(NamedTuple):
    """Ein Muster, das nur die Datei `erlaubteDatei` enthalten darf."""

    erlaubteDatei: str
    meldung: str
    muster: re.Pattern[str] | None = None


eingabeFelder = Einzelstelle(
    "gemeinsam/hookProtokoll.py",
    "liest ein Feld der Hook-Eingabe selbst; das tut nur `HookEingabe`",
    re.compile(r"\beingabe(\.get\(|\[)"),
)
handoffOrdnerLiteral = Einzelstelle(
    "gemeinsam/pfade.py",
    "nennt den Ordner `handoff` als Text; der Name steht nur in `pfade.handoffOrdner`",
    re.compile(r"""[fr]?["']handoff"""),
)
gitAufruf = Einzelstelle(
    "gemeinsam/gitAufruf.py", "ruft git per `subprocess` selbst auf; das tut nur `gitAufruf.py`"
)
einzelstellen = (eingabeFelder, handoffOrdnerLiteral, gitAufruf)


def skripte(wurzel: Path) -> list[Path]:
    """Module der Prüfskripte ohne Tests und `conftest.py`."""
    ordner = wurzel / prüfskripteOrdner
    return [
        datei
        for datei in sorted(ordner.rglob("*.py"))
        if not datei.name.endswith("Test.py") and datei.name != "conftest.py"
    ]


def rufGitAuf(knoten: ast.AST) -> bool:
    """Ein Aufruf `subprocess.xyz(["git", …])`."""
    if not (isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Attribute)):
        return False
    quelle = knoten.func.value
    if not (isinstance(quelle, ast.Name) and quelle.id == "subprocess" and knoten.args):
        return False
    befehl = knoten.args[0]
    if not (isinstance(befehl, ast.List) and befehl.elts):
        return False
    erstes = befehl.elts[0]
    return isinstance(erstes, ast.Constant) and erstes.value == "git"


def stellenIn(einzelstelle: Einzelstelle, text: str) -> list[int]:
    """Zeilen des Textes, die das Muster der Einzelstelle enthalten."""
    if einzelstelle.muster is not None:
        zeilen = text.splitlines()
        return [
            nummer for nummer, zeile in enumerate(zeilen, 1) if einzelstelle.muster.search(zeile)
        ]
    return [knoten.lineno for knoten in ast.walk(ast.parse(text)) if rufGitAuf(knoten)]


def verstöße(wurzel: Path) -> list[str]:
    gefunden = []
    for datei in skripte(wurzel):
        relativ = relativZurWurzel(datei, wurzel / prüfskripteOrdner)
        text = datei.read_text(encoding="utf-8")
        for einzelstelle in einzelstellen:
            if relativ == einzelstelle.erlaubteDatei:
                continue
            gefunden += [
                f"{prüfskripteOrdner}/{relativ}:{zeile} {einzelstelle.meldung}"
                for zeile in stellenIn(einzelstelle, text)
            ]
    return gefunden


if __name__ == "__main__":
    meldungen = verstöße(projektordner())
    print("\n".join(meldungen))
    sys.exit(1 if meldungen else 0)
