import pytest

from mutationsregeln.mutation import (
    Ergebnis,
    bericht,
    geänderteModule,
    mutationenPrüfen,
    schwelleErreicht,
    volleProzent,
)

halbeProzent = volleProzent // 2

modul = "technik/arbiter/domaene/probe.py"
testpfade = ("technik/tests",)
pyproject = '[tool.pytest.ini_options]\npythonpath = ["technik"]\npython_files = ["*Test.py"]\n'
quelle = "def kleiner(erste, zweite):\n    return erste < zweite\n"
lückenhaft = (
    "from arbiter.domaene.probe import kleiner\n\n\n"
    "def testKleinerAlsDrei():\n    assert kleiner(1, 3)\n\n\n"
    "def testNichtKleinerAlsEins():\n    assert not kleiner(2, 1)\n"
)
vollständig = lückenhaft + "\n\ndef testGleichIstNichtKleiner():\n    assert not kleiner(2, 2)\n"


def projektMit(tmp_path, testtext):
    (tmp_path / "pyproject.toml").write_text(pyproject, encoding="utf-8")
    ordner = tmp_path / "technik" / "arbiter" / "domaene"
    ordner.mkdir(parents=True)
    for paket in (ordner, ordner.parent):
        (paket / "__init__.py").write_text("", encoding="utf-8")
    (ordner / "probe.py").write_text(quelle, encoding="utf-8")
    tests = tmp_path / "technik" / "tests"
    tests.mkdir()
    (tests / "probeTest.py").write_text(testtext, encoding="utf-8")
    return tmp_path


def testEineLückeImTestIstEinÜberlebender(tmp_path):
    ergebnis = mutationenPrüfen(projektMit(tmp_path, lückenhaft), [modul], testpfade)
    assert [(lücke.zeile, lücke.beschreibung) for lücke in ergebnis.überlebende] == [
        (2, "Lt wird LtE")
    ]
    assert ergebnis.prozentGefangen == halbeProzent


def testVollständigeTestsFangenAlleMutanten(tmp_path):
    ergebnis = mutationenPrüfen(projektMit(tmp_path, vollständig), [modul], testpfade)
    assert (ergebnis.gesamt, ergebnis.überlebende) == (2, [])
    assert ergebnis.prozentGefangen == volleProzent


def testRoteTestsOhneMutantZeigenKeineLücke(tmp_path):
    rot = lückenhaft + "\n\ndef testRot():\n    assert False\n"
    projekt = projektMit(tmp_path, rot)
    with pytest.raises(AssertionError, match="ohne Mutant rot"):
        mutationenPrüfen(projekt, [modul], testpfade)


def testDerBerichtNenntDieLückeMitDateiUndZeile(tmp_path):
    ergebnis = mutationenPrüfen(projektMit(tmp_path, lückenhaft), [modul], testpfade)
    assert bericht(ergebnis).splitlines()[0] == f"{modul}:2 Lt wird LtE"


def testOhneMutantenSindAlleGefangen():
    assert Ergebnis(0, []).prozentGefangen == volleProzent


def testGeändertSindNurDieSeitDerPlanfreigabeGeänderten(gitRepo):
    ordner = gitRepo.ordner / "technik" / "arbiter" / "domaene"
    ordner.mkdir(parents=True)
    for name in ("alt.py", "geändert.py"):
        (ordner / name).write_text("x = 1\n", encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 1")
    (ordner / "geändert.py").write_text("x = 2\n", encoding="utf-8")
    (ordner / "neu.py").write_text("x = 1\n", encoding="utf-8")
    (ordner / "notiz.md").write_text("x\n", encoding="utf-8")
    assert geänderteModule(gitRepo.ordner) == [
        "technik/arbiter/domaene/geändert.py",
        "technik/arbiter/domaene/neu.py",
    ]


def testUnterDerSchwelleIstDerLaufRot(tmp_path):
    ergebnis = mutationenPrüfen(projektMit(tmp_path, lückenhaft), [modul], testpfade)
    assert not schwelleErreicht(ergebnis)


def testAnDerSchwelleIstDerLaufGrün():
    assert schwelleErreicht(Ergebnis(20, [("datei", 1, "Fehler")]))
    assert not schwelleErreicht(Ergebnis(20, [("datei", 1, "Fehler")] * 2))
