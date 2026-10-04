import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

from formregeln.benennung import ausgeschlosseneOrdner
from gemeinsam.gitAufruf import gitAusgabe
from gemeinsam.pfade import wurzel
from rollenregeln.agenten import altbestandOrdner

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


@pytest.mark.stand
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


@pytest.mark.stand
def testPreCommitRuftDiePrüfungenAuf():
    text = (wurzel / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert "python3 -m pytest prozess/pruefungen" in text
    assert "formregeln.benennung" in text


def ruffAufrufen(
    *argumente: str, cwd: Path = wurzel, config: Path = wurzel / "pyproject.toml"
) -> subprocess.CompletedProcess:
    """Rot, wenn ruff fehlt: `pyproject.toml` nennt es unter `dependency-groups`."""
    ruff = shutil.which("ruff") or shutil.which("ruff", path=str(wurzel / ".venv" / "bin"))
    assert ruff, "ruff ist nicht installiert (pyproject.toml, dependency-groups, entwicklung)"
    return subprocess.run(
        [ruff, "check", "--no-cache", "--config", str(config), *argumente],
        cwd=cwd,
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


def testArbiterGiltAuchFürNochFehlendeModuleAlsEigenesPaket(tmp_path):
    probe = tmp_path / "probe.py"
    probe.write_text(
        "import pytest\n\nfrom arbiter.domaene.sperre import Sperre\n"
        "from arbiter.gibtEsNicht.modul import Ding\n\n\n"
        "def tun():\n    return pytest, Sperre, Ding\n"
    )
    assert ruffAufrufen(str(probe)).returncode == 0


@pytest.mark.parametrize("ordner", altbestandOrdner)
def testRuffPrüftDenAltbestandNicht(tmp_path, ordner):
    (tmp_path / ordner).mkdir()
    (tmp_path / ordner / "probe.py").write_text("def rechnen(a, b, c, d, e, f):\n    return 7\n")
    ergebnis = ruffAufrufen(cwd=tmp_path, config=wurzel / "pyproject.toml")
    assert ergebnis.returncode == 0, ergebnis.stdout


@pytest.mark.parametrize("ordner", altbestandOrdner)
def testRuffSchließtDenAltbestandAus(ordner):
    assert ordner in pyproject()["tool"]["ruff"]["extend-exclude"]


@pytest.mark.stand
@pytest.mark.parametrize("ordner", altbestandOrdner)
def testGitIgnoriertDenAltbestand(ordner):
    assert gitAusgabe(wurzel, "check-ignore", f"{ordner}/alt.py").strip() == f"{ordner}/alt.py"


@pytest.mark.parametrize("ordner", altbestandOrdner)
def testDieBenennungÜbergehtDenAltbestand(ordner):
    assert ordner in ausgeschlosseneOrdner


@pytest.mark.stand
def testPytestOhnePfadSammeltNurDieEigenenTests():
    ausgabe = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=wurzel,
        capture_output=True,
        text=True,
        check=False,
    )
    assert ausgabe.returncode == 0, ausgabe.stdout[-500:]
    zeilen = ausgabe.stdout.splitlines()
    assert not any(
        zeile.startswith(f"{ordner}/") for zeile in zeilen for ordner in altbestandOrdner
    )


@pytest.mark.stand
def testDasRepoIstRuffSauber():
    ergebnis = ruffAufrufen(".")
    assert ergebnis.returncode == 0, ergebnis.stdout


def testDerSuchpfadEnthältDasProduktAberNichtDiePrüfskripte():
    suchpfad = pyproject()["tool"]["pytest"]["ini_options"]["pythonpath"]
    assert "technik" in suchpfad
    assert "prozess/pruefungen" not in suchpfad


def testPyYamlIstLaufzeitAbhängigkeitMitFesterMinorVersion():
    konfiguration = pyproject()
    abhängigkeiten = konfiguration.get("project", {}).get("dependencies", [])
    assert any(re.fullmatch(r"PyYAML==\d+\.\d+\.\*", eintrag) for eintrag in abhängigkeiten)
    assert not any(
        "PyYAML" in eintrag for eintrag in konfiguration["dependency-groups"]["entwicklung"]
    )


def testFlaskIstLaufzeitAbhängigkeitMitFesterMinorVersion():
    konfiguration = pyproject()
    abhängigkeiten = konfiguration.get("project", {}).get("dependencies", [])
    assert any(re.fullmatch(r"Flask==\d+\.\d+\.\*", eintrag) for eintrag in abhängigkeiten)
    entwicklung = konfiguration["dependency-groups"]["entwicklung"]
    assert not any("Flask" in eintrag for eintrag in entwicklung)


def testPlaywrightIstEntwicklungsAbhängigkeitMitFesterMinorVersion():
    konfiguration = pyproject()
    entwicklung = konfiguration["dependency-groups"]["entwicklung"]
    assert any(re.fullmatch(r"playwright==\d+\.\d+\.\*", eintrag) for eintrag in entwicklung)
    laufzeit = konfiguration.get("project", {}).get("dependencies", [])
    assert not any("playwright" in eintrag for eintrag in laufzeit)
