"""Zweigabdeckung und toter Code messen (ablauf.md, DoD 1 und 2)."""

import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

from pfade import wurzel

schwelle = 95
# Regel: vulture meldet 0 für nichts gefunden und 3 für toten Code; alles andere ist ein Fehler
vultureGültig = (0, 3)


class Abdeckung(NamedTuple):
    zeilen: float
    zweige: float


def prozentText(prozent: float) -> str:
    """Auf eine Stelle abgerundet, damit die Meldung nie „95.0 %“ unter der Schwelle nennt."""
    return f"{math.floor(prozent * 10) / 10:.1f} %"


def verstoß(name: str, abdeckung: Abdeckung) -> str | None:
    """Meldung, wenn Zeilen oder Zweige von `name` unter der Schwelle liegen."""
    if min(abdeckung) >= schwelle:
        return None
    return (
        f"Abdeckung von {name}: Zeilen {prozentText(abdeckung.zeilen)}, "
        f"Zweige {prozentText(abdeckung.zweige)}, verlangt {schwelle} %"
    )


def quote(gedeckt: int, gesamt: int) -> float:
    return 100 * gedeckt / gesamt if gesamt else 100.0


def abdeckungMessen(wurzel: Path, quelle: str, tests: str, auswahl: str | None = None) -> Abdeckung:
    """Zeilen und Zweige von `quelle` im Lauf von `tests`; `auswahl` ist ein pytest-Ausdruck."""
    with tempfile.TemporaryDirectory() as ablage:
        messdatei = Path(ablage) / "messung"
        umgebung = {**os.environ, "COVERAGE_FILE": str(messdatei)}
        aufruf = [sys.executable, "-m", "coverage", "run", "--branch", f"--source={quelle}"]
        aufruf += ["--omit=*Test.py,*conftest.py", "-m", "pytest", "-q", "-p", "no:cacheprovider"]
        if auswahl:
            aufruf += ["-m", auswahl]
        lauf = subprocess.run(
            [*aufruf, tests], cwd=wurzel, env=umgebung, capture_output=True, text=True, check=False
        )
        assert messdatei.exists(), f"coverage ist nicht installiert (pyproject.toml): {lauf.stderr}"
        bericht = Path(ablage) / "bericht.json"
        subprocess.run(
            [sys.executable, "-m", "coverage", "json", "-q", "-o", str(bericht)],
            cwd=wurzel,
            env=umgebung,
            capture_output=True,
            check=True,
        )
        summen = json.loads(bericht.read_text())["totals"]
        return Abdeckung(
            quote(summen["covered_lines"], summen["num_statements"]),
            quote(summen["covered_branches"], summen["num_branches"]),
        )


def unbenutzterCode(wurzel: Path, *pfade: str) -> list[str]:
    """Meldungen von vulture über `pfade` bei 60 % Konfidenz; Ausnahmen stehen in pyproject.toml."""
    lauf = subprocess.run(
        [sys.executable, "-m", "vulture", *pfade, "--min-confidence", "60"],
        cwd=wurzel,
        capture_output=True,
        text=True,
        check=False,
    )
    assert lauf.returncode in vultureGültig, f"vulture ist gescheitert: {lauf.stderr}"
    return lauf.stdout.splitlines()


if __name__ == "__main__":
    gemessen = abdeckungMessen(wurzel, "prozess/pruefungen", "prozess/pruefungen", "not stand")
    meldung = verstoß("prozess/pruefungen", gemessen)
    print(meldung or f"Abdeckung von prozess/pruefungen: ausreichend ({gemessen})")
    sys.exit(1 if meldung else 0)
