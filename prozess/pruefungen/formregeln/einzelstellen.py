"""Was in den Prüfskripten nur an einer Stelle stehen darf: Hook-Eingabe, git, Ordner `handoff`."""

import ast
import re
import sys
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

from gemeinsam.hookProtokoll import feldnamen
from gemeinsam.pfade import projektordner, relativZurWurzel

prüfskripteOrdner = "prozess/pruefungen"


class Einzelstelle(NamedTuple):
    """Ein Muster im Syntaxbaum, das nur die Datei `erlaubteDatei` enthalten darf."""

    erlaubteDatei: str
    meldung: str
    trifft: Callable[[ast.AST], bool]


feldnamenDerEingabe = frozenset(feldnamen.values())
gitWort = "git"
prozessAufrufe = ("run", "Popen", "call", "check_call", "check_output", "system")
handoffMuster = re.compile(r"(^|/)handoff(/|$)")


def textVon(knoten: ast.AST | None) -> str | None:
    """Der Wert einer Text-Konstante; sonst `None`."""
    if isinstance(knoten, ast.Constant) and isinstance(knoten.value, str):
        return knoten.value
    return None


def liestFeldDerEingabe(knoten: ast.AST) -> bool:
    """Ein `.get("<Feld>")` oder `["<Feld>"]` mit dem Namen eines Feldes der Hook-Eingabe."""
    if isinstance(knoten, ast.Subscript):
        return textVon(knoten.slice) in feldnamenDerEingabe
    if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Attribute):
        gelesen = textVon(knoten.args[0]) if knoten.args else None
        return knoten.func.attr == "get" and gelesen in feldnamenDerEingabe
    return False


def nenntHandoff(knoten: ast.AST) -> bool:
    """Ein Text oder Textteil eines f-Strings, der den Ordner `handoff` nennt."""
    text = textVon(knoten)
    return text is not None and handoffMuster.search(text) is not None


def aufrufName(knoten: ast.Call) -> str:
    """Der Name der aufgerufenen Funktion, bei `subprocess.run` also `run`."""
    if isinstance(knoten.func, ast.Attribute):
        return knoten.func.attr
    return knoten.func.id if isinstance(knoten.func, ast.Name) else ""


def rufGitAuf(knoten: ast.AST) -> bool:
    """Eine Liste oder ein Tupel, das mit `"git"` beginnt, oder ein Prozessaufruf mit `git …`."""
    if isinstance(knoten, ast.List | ast.Tuple):
        return bool(knoten.elts) and textVon(knoten.elts[0]) == gitWort
    if isinstance(knoten, ast.Call) and knoten.args and aufrufName(knoten) in prozessAufrufe:
        befehl = textVon(knoten.args[0])
        return befehl is not None and befehl.split()[:1] == [gitWort]
    return False


eingabeFelder = Einzelstelle(
    "gemeinsam/hookProtokoll.py",
    "liest ein Feld der Hook-Eingabe selbst; das tut nur `HookEingabe`",
    liestFeldDerEingabe,
)
handoffOrdnerLiteral = Einzelstelle(
    "gemeinsam/pfade.py",
    "nennt den Ordner `handoff` als Text; der Name steht nur in `pfade.handoffOrdner`",
    nenntHandoff,
)
gitAufruf = Einzelstelle(
    "gemeinsam/gitAufruf.py",
    "ruft git selbst auf; das tut nur `gitAufruf.py`",
    rufGitAuf,
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


def docstrings(baum: ast.AST) -> set[ast.AST]:
    """Die Text-Konstanten, die Docstrings sind."""
    gefunden = set()
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            erste = knoten.body[0] if knoten.body else None
            if isinstance(erste, ast.Expr):
                gefunden.add(erste.value)
    return gefunden


def stellenIn(einzelstelle: Einzelstelle, text: str) -> list[int]:
    """Zeilen des Textes, die die Einzelstelle treffen; Docstrings zählen nicht."""
    baum = ast.parse(text)
    ausgenommen = docstrings(baum)
    zeilen = {
        knoten.lineno
        for knoten in ast.walk(baum)
        if knoten not in ausgenommen and einzelstelle.trifft(knoten)
    }
    return sorted(zeilen)


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
