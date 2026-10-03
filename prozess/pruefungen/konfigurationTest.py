import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

wurzel = Path(__file__).resolve().parents[2]
ordner = Path(__file__).resolve().parent


def pyproject() -> dict:
    return tomllib.loads((wurzel / "pyproject.toml").read_text(encoding="utf-8"))


def testRuffEnthältDenWerkzeugsatzAusE37():
    ausgewählt = pyproject()["tool"]["ruff"]["lint"]["select"]
    for regel in ("ARG", "PLR2004", "PLR0913", "FBT", "ERA"):
        assert regel in ausgewählt


@pytest.mark.parametrize("regel", ["N802", "N803", "N806", "N815", "N816"])
def testRuffLässtDieNamensregelnFürSnakeCaseAus(regel):
    assert regel in pyproject()["tool"]["ruff"]["lint"]["ignore"]


def testPytestErkenntDateienNachDemSchemaNameTest():
    assert "*Test.py" in pyproject()["tool"]["pytest"]["ini_options"]["python_files"]


def testPytestFindetAlleTestdateienDerPrüfungen():
    ausgabe = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", str(ordner)],
        cwd=wurzel,
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    gesucht = sorted(datei.name for datei in ordner.glob("*Test.py"))
    fehlend = [name for name in gesucht if name not in ausgabe]
    assert gesucht and fehlend == []


def testPreCommitRuftDiePrüfungenAuf():
    text = (wurzel / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert "python3 -m pytest prozess/pruefungen" in text
    assert "prozess/pruefungen/benennung.py" in text


@pytest.mark.skipif(shutil.which("ruff") is None, reason="ruff ist nicht installiert")
def testRuffMeldetEinenVerstoßGegenDenWerkzeugsatz(tmp_path):
    probe = tmp_path / "probe.py"
    probe.write_text("def rechnen(erste, zweite, dritte, vierte, fünfte, sechste):\n    return 7\n")
    ergebnis = subprocess.run(
        ["ruff", "check", "--config", str(wurzel / "pyproject.toml"), str(probe)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert ergebnis.returncode != 0
