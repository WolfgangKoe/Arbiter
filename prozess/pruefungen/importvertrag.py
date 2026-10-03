"""Importvertrag A1 und A2 (`technik/architektur.md`): die Domäne importiert nur die
Standardbibliothek und sich selbst."""

import ast
import sys
from pathlib import Path

from agenten import projektordner

domaeneOrdner = "technik/arbiter/domaene"
eigenesPaket = "arbiter.domaene"


def importierteModule(baum: ast.AST) -> list[tuple[str, int]]:
    """Absolute Modulnamen mit Zeile; relative Importe bleiben im Paket und fehlen hier."""
    module = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            module += [(alias.name, knoten.lineno) for alias in knoten.names]
        elif isinstance(knoten, ast.ImportFrom) and knoten.level == 0 and knoten.module:
            module.append((knoten.module, knoten.lineno))
    return module


def erlaubt(modul: str) -> bool:
    if modul == eigenesPaket or modul.startswith(eigenesPaket + "."):
        return True
    return modul.split(".")[0] in sys.stdlib_module_names


def verstöße(wurzel: Path) -> list[str]:
    gefunden = []
    for datei in sorted((wurzel / domaeneOrdner).rglob("*.py")):
        baum = ast.parse(datei.read_text(encoding="utf-8"))
        for modul, zeile in importierteModule(baum):
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
