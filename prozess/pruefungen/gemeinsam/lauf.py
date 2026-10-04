"""Startet ein Prüfskript über seinen Modulnamen, ohne PYTHONPATH: `lauf.py standregeln.stand`."""

import runpy
import sys
from pathlib import Path

prüfskripteOrdner = Path(__file__).resolve().parents[1]


def starten(modul: str, argumente: list[str]) -> None:
    # Warum: Querimporte wie `gemeinsam.pfade` brauchen den Ordner der Themenordner im Suchpfad.
    sys.path[0] = str(prüfskripteOrdner)
    sys.argv = [modul, *argumente]
    runpy.run_module(modul, run_name="__main__", alter_sys=True)


if __name__ == "__main__":
    starten(sys.argv[1], sys.argv[2:])
