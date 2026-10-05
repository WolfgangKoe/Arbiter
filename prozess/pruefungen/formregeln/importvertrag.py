"""Importvertrag A1, A2 (`technik/architektur.md`): nur Standardbibliothek und eigene Domäne."""

import ast
import sys
from pathlib import Path

from formregeln.glossar import domaeneOrdner
from gemeinsam.pfade import projektordner

eigenesPaket = "arbiter.domaene"


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


def verstöße(wurzel: Path) -> list[str]:
    gefunden = []
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
