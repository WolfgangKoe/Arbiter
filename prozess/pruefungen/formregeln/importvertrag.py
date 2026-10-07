"""Importvertrag A1, A2 (`technik/architektur.md`) und W1, W2 (`technik/architektur/web.md`)."""

import ast
import sys
from pathlib import Path

from formregeln.glossar import domaeneOrdner
from gemeinsam.pfade import projektordner, webOrdner

eigenesPaket = "arbiter.domaene"
darstellungsDatei = "darstellung.py"
vorlagenModule = ("jinja2", "markupsafe", "flask.templating")
vorlagenFunktionen = ("render_template", "render_template_string", "*")
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


def istOderUnter(modul: str, name: str) -> bool:
    return modul == name or modul.startswith(name + ".")


def erlaubt(modul: str) -> bool:
    return istOderUnter(modul, eigenesPaket) or modul.split(".")[0] in sys.stdlib_module_names


def istVorlagenName(name: str) -> bool:
    """Ob der volle Name ein Vorlagenmodul, darunter, eine Vorlagenfunktion oder `flask.*` ist."""
    return any(istOderUnter(name, modul) for modul in vorlagenModule) or name in {
        f"flask.{funktion}" for funktion in vorlagenFunktionen
    }


def importierteNamen(baum: ast.AST, paket: list[str]) -> list[tuple[str, int]]:
    """Volle Namen aller Importe mit Zeile; bei `from` das Modul und jedes `modul.name`."""
    namen = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            namen += [(alias.name, knoten.lineno) for alias in knoten.names]
        elif isinstance(knoten, ast.ImportFrom):
            modul = aufgelöst(knoten, paket) or "?"
            namen.append((modul, knoten.lineno))
            namen += [(f"{modul}.{alias.name}", knoten.lineno) for alias in knoten.names]
    return namen


def gebundeneAusImport(knoten: ast.Import) -> dict[str, str]:
    gebunden = {}
    for alias in knoten.names:
        wurzelName = alias.name.split(".")[0]
        gebunden[alias.asname or wurzelName] = alias.name if alias.asname else wurzelName
    return gebunden


def gebundeneModule(baum: ast.AST, paket: list[str]) -> dict[str, str]:
    """Der Name, den ein Import bindet, und der volle Name dahinter (`import a.b` bindet `a`)."""
    gebunden = {}
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            gebunden |= gebundeneAusImport(knoten)
        elif isinstance(knoten, ast.ImportFrom):
            modul = aufgelöst(knoten, paket) or "?"
            gebunden |= {
                alias.asname or alias.name: f"{modul}.{alias.name}" for alias in knoten.names
            }
    return gebunden


def vollerName(zugriff: ast.Attribute, gebunden: dict[str, str]) -> str | None:
    """Der volle Name einer Attributkette, deren Wurzel an einen Import gebunden ist."""
    teile = [zugriff.attr]
    knoten = zugriff.value
    while isinstance(knoten, ast.Attribute):
        teile.append(knoten.attr)
        knoten = knoten.value
    if not isinstance(knoten, ast.Name) or knoten.id not in gebunden:
        return None
    return ".".join([gebunden[knoten.id], *reversed(teile)])


def vorlagenImporte(baum: ast.AST, paket: list[str]) -> list[tuple[str, int]]:
    """Importe und Attributzugriffe auf Vorlagen und HTML-Erzeugung (W1) mit Zeile."""
    gebunden = gebundeneModule(baum, paket)
    zugriffe = [
        (vollerName(knoten, gebunden), knoten.lineno)
        for knoten in ast.walk(baum)
        if isinstance(knoten, ast.Attribute)
    ]
    treffer = {
        (name, zeile)
        for name, zeile in [*importierteNamen(baum, paket), *zugriffe]
        if name and istVorlagenName(name)
    }
    return [(name, zeile) for zeile, name in sorted((zeile, name) for name, zeile in treffer)]


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
