import pytest

from formregeln.werkzeugaufruf import pyproject, ruffAufrufen
from gemeinsam.pfade import altbestandOrdner, wurzel


def testPytestLäuftBeiSammelfehlernWeiter():
    optionen = pyproject()["tool"]["pytest"]["ini_options"]["addopts"]
    assert "--continue-on-collection-errors" in optionen


def testRuffEnthältDenWerkzeugsatzAusDemAblauf():
    ausgewählt = pyproject()["tool"]["ruff"]["lint"]["select"]
    for regel in ("ARG", "PLR2004", "PLR0913", "FBT", "ERA"):
        assert regel in ausgewählt


@pytest.mark.parametrize("regel", ["N802", "N803", "N806", "N815", "N816"])
def testRuffLässtDieNamensregelnFürSnakeCaseAus(regel):
    assert regel in pyproject()["tool"]["ruff"]["lint"]["ignore"]


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
def testDasRepoIstRuffSauber():
    ergebnis = ruffAufrufen(".")
    assert ergebnis.returncode == 0, ergebnis.stdout
