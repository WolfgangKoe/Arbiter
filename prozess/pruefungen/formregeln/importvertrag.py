"""Importvertrag A1, A2 (`technik/architektur.md`) und W1, W2 (`technik/architektur/web.md`)."""

import ast
import sys
from pathlib import Path

from formregeln.glossar import domaeneOrdner
from gemeinsam.pfade import projektordner

eigenesPaket = "arbiter.domaene"
webOrdner = "technik/arbiter/web"
darstellungsDatei = "darstellung.py"
vorlagenModule = ("jinja2", "markupsafe", "flask.templating")
vorlagenFunktionen = ("render_template", "render_template_string")
serverModule = ("flask", "werkzeug")


def paketDerDatei(datei: Path, wurzel: Path) -> list[str]:
    """Das Paket, in dem die Datei liegt, aus ihrem Pfad unter `technik/`."""
    return list(datei.parent.relative_to(wurzel / "technik").parts)


def aufgelöst(knoten: ast.ImportFrom, paket: list[str]) -> str | None:
    """Der absolute Modulname eines `from`-Imports; `None`, wenn er über das Paket hinausführt."""
    if knoten.level == 0:
        return knoten.module
    if knoten.level > len(paket):
        return None
    ziel = paket[: len(paket) - (knoten.level - 1)]
    return ".".join([*ziel, *([knoten.module] if knoten.module else [])])


def importierteModule(baum: ast.AST, paket: list[str]) -> list[tuple[str, int]]:
    """Absolute Modulnamen mit Zeile; ein Import über das Paket hinaus heißt `?`."""
    module = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            module += [(alias.name, knoten.lineno) for alias in knoten.names]
        elif isinstance(knoten, ast.ImportFrom):
            module.append((aufgelöst(knoten, paket) or "?", knoten.lineno))
    return module


def erlaubt(modul: str) -> bool:
    if modul == eigenesPaket or modul.startswith(eigenesPaket + "."):
        return True
    return modul.split(".")[0] in sys.stdlib_module_names


def istOderUnter(modul: str, name: str) -> bool:
    return modul == name or modul.startswith(name + ".")


def vorlagenImporte(baum: ast.AST, paket: list[str]) -> list[tuple[str, int]]:
    """Importe von Vorlagen und HTML-Erzeugung (W1) mit Zeile."""
    gefunden = [
        (modul, zeile)
        for modul, zeile in importierteModule(baum, paket)
        if any(istOderUnter(modul, name) for name in vorlagenModule)
    ]
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.ImportFrom) and knoten.level == 0 and knoten.module == "flask":
            gefunden += [
                (f"flask.{alias.name}", knoten.lineno)
                for alias in knoten.names
                if alias.name in vorlagenFunktionen
            ]
    return gefunden


def serverImporte(baum: ast.AST, paket: list[str]) -> list[tuple[str, int]]:
    """Importe von Flask und Werkzeug (W2) mit Zeile."""
    return [
        (modul, zeile)
        for modul, zeile in importierteModule(baum, paket)
        if any(istOderUnter(modul, name) for name in serverModule)
    ]


def webVerstöße(wurzel: Path) -> list[str]:
    gefunden = []
    for datei in sorted((wurzel / webOrdner).rglob("*.py")):
        baum = ast.parse(datei.read_text(encoding="utf-8"))
        paket = paketDerDatei(datei, wurzel)
        verboten = [(*treffer, "W1") for treffer in vorlagenImporte(baum, paket)]
        if datei.name == darstellungsDatei:
            verboten += [(*treffer, "W2") for treffer in serverImporte(baum, paket)]
        pfad = datei.relative_to(wurzel)
        gefunden += [
            f"{pfad}:{zeile} importiert {modul}, verboten nach {regel}"
            for modul, zeile, regel in verboten
        ]
    return gefunden


def verstöße(wurzel: Path) -> list[str]:
    gefunden = webVerstöße(wurzel)
    for datei in sorted((wurzel / domaeneOrdner).rglob("*.py")):
        baum = ast.parse(datei.read_text(encoding="utf-8"))
        for modul, zeile in importierteModule(baum, paketDerDatei(datei, wurzel)):
            if not erlaubt(modul):
                pfad = datei.relative_to(wurzel)
                gefunden.append(
                    f"{pfad}:{zeile} importiert {modul}, erlaubt sind nur die "
                    f"Standardbibliothek und {eigenesPaket}"
                )
    return gefunden


if __name__ == "__main__":
    meldungen = verstöße(projektordner())
    print("\n".join(meldungen))
    sys.exit(1 if meldungen else 0)
