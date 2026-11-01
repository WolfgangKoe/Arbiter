import json
import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

from formregeln.frontendMessung import umgebungsvariable
from formregeln.frontendZeilen import zeilenabdeckung

schwelle = 95
vultureGültig = (0, 3)


class Abdeckung(NamedTuple):
    zeilen: float
    zweige: float
    rote: int = 0
    frontendZeilen: float | None = None


def prozentText(prozent: float) -> str:
    return f"{math.floor(prozent * 10) / 10:.1f} %"


def abdeckungText(name: str, abdeckung: Abdeckung) -> str:
    return (
        f"Abdeckung von {name}: Zeilen {prozentText(abdeckung.zeilen)}, "
        f"Zweige {prozentText(abdeckung.zweige)}"
    )


def verstoß(name: str, abdeckung: Abdeckung) -> str | None:
    if abdeckung.rote:
        return f"{name}: {abdeckung.rote} Tests rot, die Schwelle gilt erst, wenn sie grün sind"
    if min(abdeckung.zeilen, abdeckung.zweige) < schwelle:
        return f"{abdeckungText(name, abdeckung)}, verlangt {schwelle} %"
    if abdeckung.frontendZeilen is not None and abdeckung.frontendZeilen < schwelle:
        return (
            f"Abdeckung des Frontends: Zeilen {prozentText(abdeckung.frontendZeilen)}, "
            f"verlangt {schwelle} %"
        )
    return None


def aussetzung(abdeckung: Abdeckung) -> str | None:
    if abdeckung.rote:
        return f"{abdeckung.rote} Tests rot (Tests vor dem Code), Abdeckung nicht gemessen"
    return None


def roteTests(pytestAusgabe: str) -> int:
    zeilen = pytestAusgabe.strip().splitlines()
    if not zeilen:
        return 0
    return sum(int(zahl) for zahl in re.findall(r"\b(\d+) (?:failed|error)", zeilen[-1]))


def quote(gedeckt: int, gesamt: int) -> float:
    return 100 * gedeckt / gesamt if gesamt else 100.0


def coverageAufrufen(wurzel: Path, umgebung: dict, *argumente: str):
    return subprocess.run(
        [sys.executable, "-m", "coverage", *argumente],
        cwd=wurzel,
        env=umgebung,
        capture_output=True,
        text=True,
        check=False,
    )


def frontendEinstellen(umgebung: dict, frontendMessdatei: Path) -> list[str]:
    umgebung[umgebungsvariable] = str(frontendMessdatei)
    umgebung["PYTHONPATH"] = os.pathsep.join(
        filter(None, [str(Path(__file__).parent), umgebung.get("PYTHONPATH")])
    )
    return ["-p", "frontendMessung"]


def abdeckungMessen(
    wurzel: Path, quelle: str, tests: str, auswahl: str | None = None, frontend: str | None = None
) -> Abdeckung:
    with tempfile.TemporaryDirectory() as ablage:
        messdatei = Path(ablage) / "messung"
        frontendMessdatei = Path(ablage) / "frontend.jsonl"
        umgebung = {**os.environ, "COVERAGE_FILE": str(messdatei)}
        aufruf = ["run", "--branch", f"--source={quelle}", "--omit=*Test.py,*conftest.py"]
        aufruf += ["-m", "pytest", "-q", "-p", "no:cacheprovider"]
        if frontend:
            aufruf += frontendEinstellen(umgebung, frontendMessdatei)
        if auswahl:
            aufruf += ["-m", auswahl]
        lauf = coverageAufrufen(wurzel, umgebung, *aufruf, tests)
        vereint = coverageAufrufen(wurzel, umgebung, "combine", "-q")
        assert messdatei.exists(), (
            f"coverage ist nicht installiert (pyproject.toml): {lauf.stderr}{vereint.stderr}"
        )
        bericht = Path(ablage) / "bericht.json"
        auswertung = coverageAufrufen(wurzel, umgebung, "json", "-q", "-o", str(bericht))
        assert auswertung.returncode == 0, (
            f"coverage hat zu {quelle} nichts gemessen: {auswertung.stdout}{auswertung.stderr}"
        )
        summen = json.loads(bericht.read_text())["totals"]
        return Abdeckung(
            quote(summen["covered_lines"], summen["num_statements"]),
            quote(summen["covered_branches"], summen["num_branches"]),
            roteTests(lauf.stdout),
            zeilenabdeckung(frontendMessdatei, wurzel / frontend) if frontend else None,
        )


def unbenutzterCode(wurzel: Path, *pfade: str) -> list[str]:
    lauf = subprocess.run(
        [sys.executable, "-m", "vulture", *pfade, "--min-confidence", "60"],
        cwd=wurzel,
        capture_output=True,
        text=True,
        check=False,
    )
    assert lauf.returncode in vultureGültig, f"vulture ist gescheitert: {lauf.stderr}"
    return lauf.stdout.splitlines()
