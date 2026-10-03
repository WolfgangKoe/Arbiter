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


def testRuffEnthältDenWerkzeugsatzAusDemAblauf():
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


def ruffAufrufen(*argumente: str) -> subprocess.CompletedProcess:
    """Rot, wenn ruff fehlt: `pyproject.toml` nennt es unter `dependency-groups`."""
    ruff = shutil.which("ruff") or shutil.which("ruff", path=str(wurzel / ".venv" / "bin"))
    assert ruff, "ruff ist nicht installiert (pyproject.toml, dependency-groups, entwicklung)"
    return subprocess.run(
        [ruff, "check", "--no-cache", "--config", str(wurzel / "pyproject.toml"), *argumente],
        cwd=wurzel,
        capture_output=True,
        text=True,
        check=False,
    )


def testRuffMeldetEinenVerstoßGegenDenWerkzeugsatz(tmp_path):
    probe = tmp_path / "probe.py"
    probe.write_text("def rechnen(erste, zweite, dritte, vierte, fünfte, sechste):\n    return 7\n")
    assert ruffAufrufen(str(probe)).returncode != 0


def testRuffMeldetKeineSperreOhneErrorEndung(tmp_path):
    probe = tmp_path / "probe.py"
    probe.write_text("class Sperre(Exception):\n    pass\n")
    assert ruffAufrufen(str(probe)).returncode == 0


def testDasRepoIstRuffSauber():
    ergebnis = ruffAufrufen(".")
    assert ergebnis.returncode == 0, ergebnis.stdout


def testDerSuchpfadEnthältDasProduktAberNichtDiePrüfskripte():
    suchpfad = pyproject()["tool"]["pytest"]["ini_options"]["pythonpath"]
    assert "technik" in suchpfad
    assert "prozess/pruefungen" not in suchpfad
