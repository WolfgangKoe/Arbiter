import pytest

from mutationsregeln.ergebnisse import Gleichwertig
from mutationsregeln.mutation import (
    Ergebnis,
    Vorgaben,
    alleModule,
    bericht,
    geänderteModule,
    mutationenPrüfen,
    schwelleErreicht,
    volleProzent,
    ziel,
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
    tmp_path.mkdir(parents=True, exist_ok=True)
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


zweiVergleiche = (
    "def kleiner(erste, zweite):\n    return erste < zweite\n\n\n"
    "def größer(erste, zweite):\n    return erste > zweite\n"
)
nurKleinerGeprüft = (
    "from arbiter.domaene.probe import kleiner\n\n\ndef testKleiner():\n    assert kleiner(1, 3)\n"
)
protokollKopf = (
    "import os\n\n\ndef vermerken(name):\n"
    "    with open(os.environ['MUTATIONSLOG'], 'a') as datei:\n"
    "        datei.write(name + '\\n')\n\n\n"
)
andereQuelle = "def eins():\n    return 1\n"
andererTest = (
    protokollKopf
    + "from arbiter.domaene.andere import eins\n\n\n"
    + "def testEins():\n    vermerken('andere')\n    assert eins() == 1\n"
)
probeMitProtokoll = (
    protokollKopf
    + "from arbiter.domaene.probe import kleiner\n\n\n"
    + "def testProtokoll():\n    vermerken('probe')\n\n\n"
    + vollständig.split("\n\n\n", 1)[1]
)


def projektMitZweiModulen(tmp_path):
    projekt = projektMit(tmp_path, probeMitProtokoll)
    (projekt / "technik/arbiter/domaene/andere.py").write_text(andereQuelle, encoding="utf-8")
    (projekt / "technik/tests/andereTest.py").write_text(andererTest, encoding="utf-8")
    return projekt


def zähle(protokoll, name):
    return protokoll.read_text(encoding="utf-8").splitlines().count(name)


def testNurDieGenanntenZeilenBekommenMutanten(tmp_path):
    projekt = projektMit(tmp_path, nurKleinerGeprüft)
    (projekt / modul).write_text(zweiVergleiche, encoding="utf-8")
    ergebnis = mutationenPrüfen(projekt, [modul], testpfade, Vorgaben(zeilen={modul: {6}}))
    assert {lücke.zeile for lücke in ergebnis.überlebende} == {6}
    assert ergebnis.gesamt == len(ergebnis.überlebende)


def testJederMutantLässtNurDieTestsLaufenDieSeineZeileAusführen(tmp_path, monkeypatch):
    protokoll = tmp_path / "protokoll.txt"
    monkeypatch.setenv("MUTATIONSLOG", str(protokoll))
    projekt = projektMitZweiModulen(tmp_path / "projekt")
    mutationenPrüfen(projekt, [modul], testpfade)
    assert zähle(protokoll, "andere") == 1


def testEinErgebnisGiltSolangeDerStandGleichBleibt(tmp_path, monkeypatch):
    protokoll = tmp_path / "protokoll.txt"
    monkeypatch.setenv("MUTATIONSLOG", str(protokoll))
    projekt = projektMit(tmp_path / "projekt", probeMitProtokoll)
    ablage = tmp_path / "merkzettel.json"
    erstes = mutationenPrüfen(projekt, [modul], testpfade, Vorgaben(ablage=ablage))
    nachBeginn = zähle(protokoll, "probe")
    zweites = mutationenPrüfen(projekt, [modul], testpfade, Vorgaben(ablage=ablage))
    assert zweites == erstes
    assert zähle(protokoll, "probe") == nachBeginn + 1
    (projekt / "technik/arbiter/domaene/probe.py").write_text(quelle + "\n\n", encoding="utf-8")
    mutationenPrüfen(projekt, [modul], testpfade, Vorgaben(ablage=ablage))
    assert zähle(protokoll, "probe") > nachBeginn + 2


def testEinGleichwertigerMutantMitBegründungZähltNicht(tmp_path):
    gleichwertig = frozenset({Gleichwertig(modul, "return erste < zweite", "Lt wird LtE")})
    projekt = projektMit(tmp_path, lückenhaft)
    ergebnis = mutationenPrüfen(projekt, [modul], testpfade, Vorgaben(gleichwertige=gleichwertig))
    assert (ergebnis.gesamt, ergebnis.überlebende, ergebnis.gleichwertige) == (1, [], 1)


def testDerBerichtNenntDieGleichwertigen():
    assert bericht(Ergebnis(4, [], 2)).endswith("2 gleichwertig begründet, nicht gezählt")


def testEinModulMitBereichBekommtNurDessenZeilen(tmp_path):
    (tmp_path / "technik").mkdir()
    (tmp_path / "technik/probe.py").write_text("a = 1\nb = 2\nc = 3\n", encoding="utf-8")
    assert ziel(tmp_path, "technik/probe.py") == ("technik/probe.py", {1, 2, 3})
    assert ziel(tmp_path, "technik/probe.py:2-3") == ("technik/probe.py", {2, 3})
    assert ziel(tmp_path, "technik/probe.py:2") == ("technik/probe.py", {2})


def testDerVolleLaufUmfasstAuchDasWeb(tmp_path):
    web = tmp_path / "technik/arbiter/web"
    web.mkdir(parents=True)
    (web / "anwendung.py").write_text("x = 1\n", encoding="utf-8")
    assert alleModule(tmp_path) == {"technik/arbiter/web/anwendung.py": {1}}
