"""Prüft Kommentare und Docstrings nach `prozess/praemissen/wir.md` (Regel 8)."""

import ast
import io
import re
import sys
import tokenize
from pathlib import Path

from agenten import projektordner
from benennung import geprüfteDateien

erlaubterKommentar = re.compile(r"^# (Regel|Warum): \S")
werkzeugkommentar = re.compile(r"^(#!|# ?(noqa|type:|pragma|ruff:|fmt:|cspell:|pyright:|mypy:))")
offenerPunkt = re.compile(r"\b(TODO|FIXME)\b")


def kommentarVerstöße(quelltext: str) -> list[str]:
    verstöße = []
    for art, text, (zeile, _), _, _ in tokenize.generate_tokens(io.StringIO(quelltext).readline):
        if art != tokenize.COMMENT:
            continue
        if offenerPunkt.search(text):
            verstöße.append(f"Zeile {zeile}: TODO oder FIXME")
        elif not (erlaubterKommentar.match(text) or werkzeugkommentar.match(text)):
            verstöße.append(f"Zeile {zeile}: Kommentar nur als `# Regel:` oder `# Warum:`")
    return verstöße


def docstringVerstöße(quelltext: str) -> list[str]:
    verstöße = []
    for knoten in ast.walk(ast.parse(quelltext)):
        if not isinstance(
            knoten, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef
        ):
            continue
        if not knoten.body or not ast.get_docstring(knoten, clean=False):
            continue
        docstring = knoten.body[0]
        if docstring.end_lineno != docstring.lineno:
            verstöße.append(f"Zeile {docstring.lineno}: Docstring länger als eine Zeile")
        if offenerPunkt.search(ast.get_docstring(knoten, clean=False) or ""):
            verstöße.append(f"Zeile {docstring.lineno}: TODO oder FIXME")
    return verstöße


def verstöße(wurzel: Path) -> list[str]:
    meldungen = []
    for pfad in geprüfteDateien(wurzel):
        if pfad.suffix != ".py":
            continue
        quelltext = pfad.read_text(encoding="utf-8")
        relativ = pfad.relative_to(wurzel).as_posix()
        for grund in kommentarVerstöße(quelltext) + docstringVerstöße(quelltext):
            meldungen.append(f"{relativ}: {grund}")
    return meldungen


if __name__ == "__main__":
    gefunden = verstöße(projektordner())
    print("\n".join(gefunden))
    sys.exit(1 if gefunden else 0)
