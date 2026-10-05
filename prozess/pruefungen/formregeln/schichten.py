"""Abhängigkeit der Prüfskripte in einer Richtung: ein Ordner importiert nur tiefere."""

import ast
import sys
from pathlib import Path

from gemeinsam.pfade import projektordner, relativZurWurzel

prüfskripteOrdner = "prozess/pruefungen"
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


def importierteOrdner(baum: ast.AST) -> list[tuple[str, int]]:
    """Oberste Namen aller Importe mit Zeile, auch innerhalb von Funktionen."""
    ordner = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            ordner += [(alias.name.split(".")[0], knoten.lineno) for alias in knoten.names]
        elif isinstance(knoten, ast.ImportFrom) and knoten.module and knoten.level == 0:
            ordner.append((knoten.module.split(".")[0], knoten.lineno))
    return ordner


def verstöße(wurzel: Path) -> list[str]:
    gefunden = []
    basis = wurzel / prüfskripteOrdner
    for datei in sorted(basis.glob("*/*.py")):
        eigener = datei.parent.name
        eigeneSchicht = schichtVon(eigener)
        pfad = f"{prüfskripteOrdner}/{relativZurWurzel(datei, basis)}"
        if eigeneSchicht is None:
            gefunden.append(f"{pfad}: Ordner `{eigener}` gehört zu keiner Schicht")
            continue
        for ordner, zeile in importierteOrdner(ast.parse(datei.read_text(encoding="utf-8"))):
            schicht = schichtVon(ordner)
            if schicht is not None and schicht > eigeneSchicht:
                gefunden.append(
                    f"{pfad}:{zeile} importiert aus `{ordner}`, höhere Schicht als `{eigener}`"
                )
    return gefunden


if __name__ == "__main__":
    meldungen = verstöße(projektordner())
    print("\n".join(meldungen))
    sys.exit(1 if meldungen else 0)
