"""Abhängigkeit der Prüfskripte in einer Richtung, ohne Kreis, nur Standardbibliothek."""

import ast
import sys
from pathlib import Path

from gemeinsam.pfade import projektordner, relativZurWurzel

prüfskripteOrdner = "prozess/pruefungen"
# Warum: Tests prüfen das Produkt (Flask, `arbiter`) und laufen unter pytest.
nurInTestsErlaubt = ("pytest", "flask", "arbiter")
schichten = (
    ("gemeinsam",),
    ("lesen",),
    ("kriterienregeln",),
    ("anliegenregeln",),
    ("standregeln",),
    ("rollenregeln",),
    ("formregeln", "frontendregeln"),
)


def schichtVon(ordner: str) -> int | None:
    """Die Nummer der Schicht, die den Themenordner enthält; unten ist 0."""
    return next((nummer for nummer, namen in enumerate(schichten) if ordner in namen), None)


def importierteNamen(baum: ast.AST) -> list[tuple[str, int, bool]]:
    """Vollständige Importnamen mit Zeile; `True` bei relativem Import, auch in Funktionen."""
    namen = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            namen += [(alias.name, knoten.lineno, False) for alias in knoten.names]
        elif isinstance(knoten, ast.ImportFrom):
            vorn = knoten.module or ""
            namen += [
                (f"{vorn}.{alias.name}", knoten.lineno, knoten.level > 0) for alias in knoten.names
            ]
    return namen


def zielModul(importName: str, module: set[str]) -> str | None:
    """Das längste Modul des Repos, das der Importname benennt."""
    teile = importName.split(".")
    return next(
        (
            ".".join(teile[:länge])
            for länge in range(len(teile), 0, -1)
            if ".".join(teile[:länge]) in module
        ),
        None,
    )


def erreichbar(kanten: dict[str, set[str]], start: str) -> set[str]:
    """Alle Module, die von `start` aus über Importe zu erreichen sind."""
    gesehen, offen = set(), [start]
    while offen:
        for nachbar in kanten[offen.pop()] - gesehen:
            gesehen.add(nachbar)
            offen.append(nachbar)
    return gesehen


def kreise(kanten: dict[str, set[str]]) -> list[list[str]]:
    """Gruppen von Modulen, die einander gegenseitig erreichen."""
    erreicht = {modul: erreichbar(kanten, modul) for modul in kanten}
    gruppen = {
        tuple(sorted(andere for andere in erreicht[modul] if modul in erreicht[andere]))
        for modul in kanten
        if modul in erreicht[modul]
    }
    return [list(gruppe) for gruppe in sorted(gruppen)]


def fremderImport(ordner: str, datei: Path) -> bool:
    """Ein Name außerhalb der Schichten, der weder Standardbibliothek noch Testwerkzeug ist."""
    if ordner in sys.stdlib_module_names:
        return False
    return not (ordner in nurInTestsErlaubt and datei.stem.endswith("Test"))


def importVerstoß(importName: str, eigener: str, datei: Path) -> str | None:
    """Die Meldung zu einem Import ohne Zeilenangabe; `None`, wenn er erlaubt ist."""
    ordner = importName.split(".")[0]
    schicht = schichtVon(ordner)
    if schicht is None:
        return (
            f"importiert `{ordner}`, nicht Standardbibliothek"
            if fremderImport(ordner, datei)
            else None
        )
    if schicht > schichtVon(eigener):
        return f"importiert aus `{ordner}`, höhere Schicht als `{eigener}`"
    return None


def dateiVerstöße(datei: Path, basis: Path, module: set[str]) -> tuple[list[str], set[str]]:
    """Verstöße einer Datei und die Module des Repos, die sie importiert."""
    eigener = datei.relative_to(basis).parts[0]
    pfad = f"{prüfskripteOrdner}/{relativZurWurzel(datei, basis)}"
    if schichtVon(eigener) is None:
        return [f"{pfad}: Ordner `{eigener}` gehört zu keiner Schicht"], set()
    gefunden, ziele = [], set()
    for importName, zeile, relativ in importierteNamen(ast.parse(datei.read_text("utf-8"))):
        meldung = "relativer Import" if relativ else importVerstoß(importName, eigener, datei)
        if meldung:
            gefunden.append(f"{pfad}:{zeile} {meldung}")
        ziele.add(zielModul(importName, module))
    return gefunden, ziele - {None}


def verstöße(wurzel: Path) -> list[str]:
    basis = wurzel / prüfskripteOrdner
    dateien = [datei for datei in sorted(basis.rglob("*.py")) if datei.parent != basis]
    modulVon = {datei: relativZurWurzel(datei, basis)[:-3].replace("/", ".") for datei in dateien}
    module = set(modulVon.values())
    gefunden, kanten = [], {}
    for datei in dateien:
        meldungen, ziele = dateiVerstöße(datei, basis, module)
        gefunden += meldungen
        kanten[modulVon[datei]] = ziele - {modulVon[datei]}
    return gefunden + [f"Kreis zwischen Modulen: {', '.join(kreis)}" for kreis in kreise(kanten)]


if __name__ == "__main__":
    meldungen = verstöße(projektordner())
    print("\n".join(meldungen))
    sys.exit(1 if meldungen else 0)
