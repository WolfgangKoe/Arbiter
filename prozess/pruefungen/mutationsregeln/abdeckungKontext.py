"""Misst mit einem Lauf der Tests, welche Testdateien jede Zeile eines Moduls ausführen."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

# Warum: Eine Zeile im Kontext "" läuft beim Import oder in einem Kindprozess: alle Tests.
ohneTest = ""
konfiguration = """[run]
patch = subprocess
sigterm = true
source = technik/arbiter
omit = *Test.py,*conftest.py
"""
steckmodul = Path(__file__).with_name("kontext") / "conftest.py"


class Karte(NamedTuple):
    """Zeilen ohne Ausführung und je ausgeführter Zeile ihre Testdateien (`None`: alle)."""

    unausgeführt: frozenset[int]
    dateien: dict[int, frozenset[str] | None]


class Messung(NamedTuple):
    grün: bool
    karten: dict[str, Karte]


def testdateienDer(kontexte: list[str]) -> frozenset[str] | None:
    if ohneTest in kontexte:
        return None
    return frozenset(kontext.split("::")[0] for kontext in kontexte)


def kartenAus(bericht: dict) -> dict[str, Karte]:
    karten = {}
    for name, datei in bericht["files"].items():
        kontexte = {int(zeile): liste for zeile, liste in datei.get("contexts", {}).items()}
        karten[name] = Karte(
            frozenset(datei["missing_lines"]),
            {zeile: testdateienDer(liste) for zeile, liste in kontexte.items()},
        )
    return karten


def coverageAufrufen(kopie: Path, umgebung: dict, *argumente: str, wartezeit: float | None = None):
    return subprocess.run(
        [sys.executable, "-m", "coverage", *argumente],
        cwd=kopie,
        env=umgebung,
        capture_output=True,
        check=False,
        timeout=wartezeit,
    )


def messen(kopie: Path, pfade: tuple[str, ...], wartezeit: float) -> Messung:
    """Lässt alle Tests in der Kopie unter coverage laufen; `grün`: kein Test war rot."""
    shutil.copy(steckmodul, kopie / "conftest.py")
    regeln = kopie / ".mutationCoveragerc"
    regeln.write_text(konfiguration, encoding="utf-8")
    umgebung = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "COVERAGE_FILE": str(kopie / ".messung"),
        "COVERAGE_RCFILE": str(regeln),
    }
    pytestAufruf = ["run", "-m", "pytest", "-q", "-p", "no:cacheprovider", *pfade]
    lauf = coverageAufrufen(kopie, umgebung, *pytestAufruf, wartezeit=wartezeit)
    coverageAufrufen(kopie, umgebung, "combine", "-q")
    coverageAufrufen(kopie, umgebung, "json", "-q", "--show-contexts", "-o", "bericht.json")
    bericht = kopie / "bericht.json"
    karten = kartenAus(json.loads(bericht.read_text(encoding="utf-8"))) if bericht.is_file() else {}
    return Messung(lauf.returncode == 0, karten)


def auswahl(karte: Karte | None, zeile: int) -> tuple[str, ...] | None:
    """Testdateien, die `zeile` ausführen; leer: keine; `None`: nicht zu sagen, also alle."""
    if karte is None:
        return None
    if zeile in karte.unausgeführt:
        return ()
    dateien = karte.dateien.get(zeile)
    if dateien is None:
        return None
    # Regel: Einheitstests zuerst, denn sie scheitern am schnellsten.
    return tuple(sorted(dateien, key=einheitZuerst))


def einheitZuerst(datei: str) -> tuple[bool, str]:
    return ("/einheit/" not in datei, datei)
