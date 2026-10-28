import ast
import io
import re
import sys
import tokenize
from collections.abc import Iterator
from pathlib import Path

from formregeln.benennung import geprüfteDateien
from formregeln.technikphase import (
    technikGeprüft,
    technikOhneDocstrings,
    zeilenVorDerTechnikphase,
)
from gemeinsam.pfade import projektordner

höchstzahlOffenerPunkte = 3
technikordner = "technik/"
akzeptanzordner = technikordner + "tests/akzeptanz/"
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


def docstringKnoten(baum: ast.Module) -> list[ast.Expr]:
    knoten = []
    for teil in ast.walk(baum):
        if not isinstance(teil, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        anweisung = teil.body[0] if teil.body else None
        if isinstance(anweisung, ast.Expr) and ast.get_docstring(teil, clean=False):
            knoten.append(anweisung)
    return knoten


def istAkzeptanztest(relativ: str) -> bool:
    return relativ.startswith(akzeptanzordner) and relativ.endswith("Test.py")


def docstringVerstöße(quelltext: str, relativ: str) -> list[str]:
    baum = ast.parse(quelltext)
    kopf = baum.body[0] if istAkzeptanztest(relativ) and baum.body else None
    return [
        f"Zeile {docstring.lineno}: Docstring nur als Spiegel der Anforderung (Es 8)"
        for docstring in docstringKnoten(baum)
        if docstring is not kopf
    ]


def geprüfteQuelltexte(wurzel: Path) -> list[Path]:
    dateien = [pfad for pfad in geprüfteDateien(wurzel) if pfad.suffix in (".py", ".js")]
    dateien += sorted(wurzel.glob("*.mjs")) + sorted((wurzel / "prozess").rglob("*.mjs"))
    return dateien


def docstringMeldungen(wurzel: Path, *, unterTechnik: bool) -> list[str]:
    meldungen = []
    for pfad in geprüfteQuelltexte(wurzel):
        relativ = pfad.relative_to(wurzel).as_posix()
        if pfad.suffix == ".py" and relativ.startswith(technikordner) == unterTechnik:
            quelltext = pfad.read_text(encoding="utf-8")
            meldungen += [f"{relativ}: {grund}" for grund in docstringVerstöße(quelltext, relativ)]
    return meldungen


def docstringVerstößeUnterTechnik(wurzel: Path) -> list[str]:
    return docstringMeldungen(wurzel, unterTechnik=True) if technikOhneDocstrings(wurzel) else []


def verstöße(wurzel: Path) -> list[str]:
    meldungen = docstringMeldungen(wurzel, unterTechnik=False)
    gesamtzahl = 0
    mitTechnik = technikGeprüft(wurzel)
    for pfad in geprüfteQuelltexte(wurzel):
        relativ = pfad.relative_to(wurzel).as_posix()
        quelltext = pfad.read_text(encoding="utf-8")
        gründe = []
        if mitTechnik or not relativ.startswith(technikordner):
            if not relativ.startswith(technikordner + "frontend/"):
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
