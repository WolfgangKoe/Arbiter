"""Scheiter-Test und Stand: Prüfskripte importieren nur aus gleicher oder tieferer Schicht."""

from pathlib import Path

import pytest

from formregeln.schichten import prüfskripteOrdner, verstöße
from gemeinsam.pfade import wurzel


def skriptAnlegen(ordner: Path, name: str, inhalt: str) -> None:
    datei = ordner / prüfskripteOrdner / name
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(inhalt, encoding="utf-8")


def testEinRückimportInEineHöhereSchichtIstRot(tmp_path):
    skriptAnlegen(tmp_path, "lesen/plan.py", "from standregeln.stand import stand\n")
    skriptAnlegen(tmp_path, "standregeln/stand.py", "from lesen.plan import zyklus\n")
    meldungen = verstöße(tmp_path)
    assert "lesen/plan.py:1 importiert aus `standregeln`" in meldungen[0]


def testEinImportInnerhalbEinerFunktionZähltAuch(tmp_path):
    skriptAnlegen(tmp_path, "anliegenregeln/kopf.py", "def f():\n    import rollenregeln.agenten\n")
    assert len(verstöße(tmp_path)) == 1


def testEinTestImportiertWieSeinModul(tmp_path):
    skriptAnlegen(tmp_path, "gemeinsam/pfadeTest.py", "from formregeln.glossar import x\n")
    assert len(verstöße(tmp_path)) == 1


def testImportAusGleicherOderTieferSchichtUndStandardbibliothekIstGrün(tmp_path):
    skriptAnlegen(tmp_path, "standregeln/stand.py", "import json\nfrom standregeln.plan import a\n")
    skriptAnlegen(tmp_path, "formregeln/glossar.py", "from frontendregeln.frontend import b\n")
    skriptAnlegen(tmp_path, "formregeln/abdeckung.py", "from gemeinsam.pfade import wurzel\n")
    assert verstöße(tmp_path) == []


def testEinOrdnerOhneSchichtIstRot(tmp_path):
    skriptAnlegen(tmp_path, "neu/modul.py", "import json\n")
    assert "gehört zu keiner Schicht" in verstöße(tmp_path)[0]


def testEinKreisZwischenZweiModulenDesselbenOrdnersIstRot(tmp_path):
    skriptAnlegen(tmp_path, "rollenregeln/laufLog.py", "from rollenregeln.dashboard import a\n")
    skriptAnlegen(
        tmp_path, "rollenregeln/dashboard.py", "def f():\n    from rollenregeln import laufLog\n"
    )
    meldungen = verstöße(tmp_path)
    assert meldungen == ["Kreis zwischen Modulen: rollenregeln.dashboard, rollenregeln.laufLog"]


def testEinKreisZwischenFormregelnUndFrontendregelnIstRot(tmp_path):
    skriptAnlegen(tmp_path, "formregeln/a.py", "from frontendregeln.b import x\n")
    skriptAnlegen(tmp_path, "frontendregeln/b.py", "from formregeln.a import y\n")
    assert "Kreis zwischen Modulen" in verstöße(tmp_path)[0]


def testEineEinseitigeAbhängigkeitImOrdnerIstGrün(tmp_path):
    skriptAnlegen(tmp_path, "rollenregeln/a.py", "from rollenregeln.b import x\n")
    skriptAnlegen(tmp_path, "rollenregeln/b.py", "import json\n")
    assert verstöße(tmp_path) == []


def testEinUnterordnerGehörtZuSeinemThemenordner(tmp_path):
    skriptAnlegen(tmp_path, "lesen/hilfe/modul.py", "from standregeln.stand import s\n")
    meldungen = verstöße(tmp_path)
    assert len(meldungen) == 1
    assert "lesen/hilfe/modul.py:1 importiert aus `standregeln`" in meldungen[0]


@pytest.mark.parametrize("zeile", ["import requests", "from arbiter.domaene import a"])
def testEinImportAußerhalbDerStandardbibliothekIstRot(tmp_path, zeile):
    skriptAnlegen(tmp_path, "lesen/modul.py", zeile + "\n")
    assert "nicht Standardbibliothek" in verstöße(tmp_path)[0]


def testPytestUndDasProduktSindInTestsErlaubt(tmp_path):
    skriptAnlegen(tmp_path, "lesen/modulTest.py", "import pytest\nfrom arbiter.web import a\n")
    assert verstöße(tmp_path) == []


def testEinRelativerImportIstRot(tmp_path):
    skriptAnlegen(tmp_path, "lesen/modul.py", "from . import nachbar\n")
    assert "relativer Import" in verstöße(tmp_path)[0]


def testMehrereNamenEinesImportsMeldenNurEinmal(tmp_path):
    skriptAnlegen(tmp_path, "lesen/plan.py", "from standregeln.stand import a, b, c\n")
    skriptAnlegen(tmp_path, "lesen/zweiter.py", "from . import x, y\n")
    meldungen = verstöße(tmp_path)
    assert meldungen == [
        "prozess/pruefungen/lesen/plan.py:1 importiert aus `standregeln`, "
        "höhere Schicht als `lesen`",
        "prozess/pruefungen/lesen/zweiter.py:1 relativer Import",
    ]


def testConftestImportiertPytestWieEinTest(tmp_path):
    skriptAnlegen(tmp_path, "formregeln/conftest.py", "import pytest\n")
    assert verstöße(tmp_path) == []


@pytest.mark.stand
def testDieSchichtenDesReposSindEingehalten():
    assert verstöße(wurzel) == []
