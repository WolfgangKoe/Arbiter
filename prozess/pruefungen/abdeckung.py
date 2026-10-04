"""Zweigabdeckung und toter Code messen (ablauf.md, DoD 1 und 2)."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

schwelle = 95
# Warum: Die Messung der Prüfskripte startet diesen Lauf noch einmal; die Marke hält sie dort an.
innenMarke = "ARBITER_ABDECKUNG_INNEN"


def zweigabdeckung(
    wurzel: Path,
    quelle: str,
    tests: str,
    suchpfad: str | None = None,
) -> float:
    """Prozent der Zeilen und Zweige von `quelle`, gemessen an den Läufen von `tests`."""
    with tempfile.TemporaryDirectory() as ablage:
        messdatei = Path(ablage) / "messung"
        umgebung = {**os.environ, "COVERAGE_FILE": str(messdatei), innenMarke: "1"}
        lauf = subprocess.run(
            messenAufruf(quelle, tests, suchpfad),
            cwd=wurzel,
            env=umgebung,
            capture_output=True,
            text=True,
            check=False,
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
        return json.loads(bericht.read_text())["totals"]["percent_covered"]


def messenAufruf(quelle: str, tests: str, suchpfad: str | None) -> list[str]:
    pytestAufruf = ["-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "python_files=*Test.py"]
    if suchpfad:
        pytestAufruf += ["-o", f"pythonpath={suchpfad}"]
    messen = [sys.executable, "-m", "coverage", "run", "--branch", f"--source={quelle}"]
    return [*messen, "--omit=*Test.py,*conftest.py", *pytestAufruf, tests]


def unbenutzterCode(wurzel: Path, *pfade: str) -> list[str]:
    """Meldungen von vulture über `pfade` bei 60 % Konfidenz; Ausnahmen stehen in pyproject.toml."""
    lauf = subprocess.run(
        [sys.executable, "-m", "vulture", *pfade, "--min-confidence", "60"],
        cwd=wurzel,
        capture_output=True,
        text=True,
        check=False,
    )
    assert "No module named" not in lauf.stderr, "vulture ist nicht installiert (pyproject.toml)"
    return lauf.stdout.splitlines()
