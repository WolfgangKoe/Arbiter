"""Scheiter-Test und Stand: Prüfskripte importieren nur aus gleicher oder tieferer Schicht."""

from pathlib import Path

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
    assert len(meldungen) == 1
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


def testDieSchichtenDesReposSindEingehalten():
    assert verstöße(wurzel) == []
