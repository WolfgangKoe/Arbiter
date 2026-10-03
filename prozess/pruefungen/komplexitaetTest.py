"""Komplexitätsschwellen im Lauf der Prüfungen: complexipy (Verschachtelung), ruff PLR0912."""

import shutil
import subprocess
from pathlib import Path

from konfigurationTest import ruffAufrufen

wurzel = Path(__file__).resolve().parents[2]
codeOrdner = ("prozess/pruefungen", "technik")


def complexipyAufrufen(*pfade: str) -> subprocess.CompletedProcess:
    """Rot, wenn complexipy fehlt: `pyproject.toml` nennt es unter `dependency-groups`."""
    programm = shutil.which("complexipy") or shutil.which(
        "complexipy", path=str(wurzel / ".venv" / "bin")
    )
    assert programm, "complexipy ist nicht installiert (pyproject.toml, dependency-groups)"
    return subprocess.run(
        [programm, "--plain", "--failed", *pfade],
        cwd=wurzel,
        capture_output=True,
        text=True,
        check=False,
    )


def testComplexipyMeldetEineTiefVerschachtelteFunktion(tmp_path):
    probe = tmp_path / "probe.py"
    probe.write_text(
        "def suchen(a):\n"
        "    for i in a:\n"
        "        if i:\n"
        "            for j in i:\n"
        "                if j:\n"
        "                    for k in j:\n"
        "                        if k:\n"
        "                            while k:\n"
        "                                if k > 1:\n"
        "                                    return 1\n"
        "    return 0\n"
    )
    assert complexipyAufrufen(str(probe)).returncode != 0


def testRuffMeldetEineFunktionMitZuvielenFällen(tmp_path):
    fälle = "".join(f"    if wert == {zahl}:\n        return {zahl}\n" for zahl in range(13))
    probe = tmp_path / "probe.py"
    probe.write_text(f"def wählen(wert):\n{fälle}    return 0\n")
    ergebnis = ruffAufrufen("--select", "PLR0912", str(probe))
    assert ergebnis.returncode != 0
    assert "PLR0912" in ergebnis.stdout


def testDerCodeLiegtUnterDerKomplexitätsschwelle():
    ergebnis = complexipyAufrufen(*codeOrdner)
    assert ergebnis.returncode == 0, ergebnis.stdout
