import ast
import io
import re
import sys
import tokenize
from collections.abc import Iterator
from pathlib import Path

from formregeln.benennung import geprüfteDateien
from formregeln.technikphase import technikGeprüft, zeilenVorDerTechnikphase
from gemeinsam.pfade import projektordner

höchstzahlOffenerPunkte = 3
offenerPunkt = re.compile(r"\b(TODO|FIXME)\b")
todoKommentar = re.compile(r"^(#|//) TODO: \S")
werkzeugkommentar = re.compile(
    r"^(#!"
    r"|# (ruff: )?noqa: [A-Z]+\d+(, [A-Z]+\d+)*$"
    r"|# (type|pyright): ignore\[[\w-]+\]$"
    r"|// eslint-disable-next-line \S)"
)
zeilenkommentarJavaScript = re.compile(r"^\s*(//.*)$")
javaScriptEndungen = (".js", ".mjs")


def kommentare(quelltext: str, endung: str) -> Iterator[tuple[int, str]]:
    if endung in javaScriptEndungen:
        for zeile, text in enumerate(quelltext.splitlines(), start=1):
            if treffer := zeilenkommentarJavaScript.match(text):
                yield zeile, treffer.group(1)
        return
    for art, text, (zeile, _), _, _ in tokenize.generate_tokens(io.StringIO(quelltext).readline):
        if art == tokenize.COMMENT:
            yield zeile, text


def kommentarVerstöße(quelltext: str, endung: str = ".py") -> list[str]:
    return [
        f"Zeile {zeile}: Kommentar nur als Werkzeugkommentar mit Regelcode oder `TODO: <was>`"
        for zeile, text in kommentare(quelltext, endung)
        if not (todoKommentar.match(text) or werkzeugkommentar.match(text))
    ]


def todoZeilen(quelltext: str, endung: str = ".py") -> list[int]:
    return [zeile for zeile, text in kommentare(quelltext, endung) if todoKommentar.match(text)]


def docstringKnoten(baum: ast.AST) -> list[tuple[ast.Expr, str]]:
    knoten = []
    for teil in ast.walk(baum):
        if not isinstance(teil, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        anweisung = teil.body[0] if teil.body else None
        if isinstance(anweisung, ast.Expr) and (text := ast.get_docstring(teil, clean=False)):
            knoten.append((anweisung, text))
    return knoten


def docstringVerstöße(quelltext: str) -> list[str]:
    verstöße = []
    for docstring, text in docstringKnoten(ast.parse(quelltext)):
        if docstring.end_lineno != docstring.lineno:
            verstöße.append(f"Zeile {docstring.lineno}: Docstring länger als eine Zeile")
        if offenerPunkt.search(text):
            verstöße.append(f"Zeile {docstring.lineno}: TODO oder FIXME")
    return verstöße


def geprüfteQuelltexte(wurzel: Path) -> list[Path]:
    dateien = [pfad for pfad in geprüfteDateien(wurzel) if pfad.suffix in (".py", ".js")]
    dateien += sorted(wurzel.glob("*.mjs")) + sorted((wurzel / "prozess").rglob("*.mjs"))
    return dateien


def verstöße(wurzel: Path) -> list[str]:
    meldungen = []
    gesamtzahl = 0
    mitTechnik = technikGeprüft(wurzel)
    for pfad in geprüfteQuelltexte(wurzel):
        relativ = pfad.relative_to(wurzel).as_posix()
        quelltext = pfad.read_text(encoding="utf-8")
        gründe = docstringVerstöße(quelltext) if pfad.suffix == ".py" else []
        if mitTechnik or not relativ.startswith("technik/"):
            if not relativ.startswith("technik/frontend/"):
                gründe += kommentarVerstöße(quelltext, pfad.suffix)
            offene = todoZeilen(quelltext, pfad.suffix)
            gesamtzahl += len(offene)
            gründe += [
                f"Zeile {zeile}: TODO von vor der laufenden Technikphase"
                for zeile in zeilenVorDerTechnikphase(wurzel, relativ, offene)
            ]
        meldungen += [f"{relativ}: {grund}" for grund in gründe]
    if gesamtzahl > höchstzahlOffenerPunkte:
        meldungen.append(f"{gesamtzahl} TODOs, höchstens {höchstzahlOffenerPunkte} erlaubt")
    return meldungen


if __name__ == "__main__":
    gefunden = verstöße(projektordner())
    print("\n".join(gefunden))
    sys.exit(1 if gefunden else 0)
