"""Komplexitätsschwellen im Lauf der Prüfungen: complexipy (Verschachtelung), ruff PLR0912."""

import shutil
import subprocess

import pytest

from konfigurationTest import ruffAufrufen
from pfade import wurzel

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


def funktionMitKomplexität(einfacheFälle: int) -> str:
    """Kognitive Komplexität 12 plus ein Punkt je einfachem Fall auf oberster Ebene."""
    return (
        "def probe(a, b, c, d):\n"
        "    for i in a:\n"
        "        if i:\n"
        "            for j in i:\n"
        "                if j:\n"
        "                    pass\n"
        "    if c and d:\n"
        "        pass\n" + "    if b:\n        pass\n" * einfacheFälle + "    return 0\n"
    )


def funktionMitFällen(zahl: int) -> str:
    return "def probe(wert):\n" + "    if wert:\n        return 1\n" * zahl + "    return 0\n"


def complexipyUrteil(tmp_path, einfacheFälle: int) -> subprocess.CompletedProcess:
    probe = tmp_path / "probe.py"
    probe.write_text(funktionMitKomplexität(einfacheFälle))
    return complexipyAufrufen(str(probe))


def testComplexipyLässtKomplexität15Zu(tmp_path):
    assert complexipyUrteil(tmp_path, 3).returncode == 0


def testComplexipyMeldetKomplexität16(tmp_path):
    assert complexipyUrteil(tmp_path, 4).returncode != 0


def meldetFälle(tmp_path, zahl: int) -> bool:
    probe = tmp_path / "probe.py"
    probe.write_text(funktionMitFällen(zahl))
    return "PLR0912" in ruffAufrufen(str(probe)).stdout


def testRuffLässtZwölfFälleZu(tmp_path):
    assert not meldetFälle(tmp_path, 12)


def testRuffMeldetDreizehnFälle(tmp_path):
    assert meldetFälle(tmp_path, 13)


@pytest.mark.stand
def testDerCodeLiegtUnterDerKomplexitätsschwelle():
    ergebnis = complexipyAufrufen(*codeOrdner)
    assert ergebnis.returncode == 0, ergebnis.stdout
