from pathlib import Path

from anliegenregeln.anliegenTest import anliegenAnlegen, guterKopf
from anliegenregeln.erledigteLoeschen import erledigteLöschen


def testErledigtesAnliegenWirdGelöscht(tmp_path, gitRepo):
    erledigt = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    offen = anliegenAnlegen(tmp_path, "13-probe.md", guterKopf.replace("12 ", "13 "))
    gitRepo.festhalten("Probe")
    assert erledigteLöschen(tmp_path) == ["12-probe.md"]
    assert not erledigt.exists()
    assert offen.exists()


def testOhneErledigteBleibtAllesStehen(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert erledigteLöschen(tmp_path) == []
    assert datei.exists()


def testDerPrüflaufRuftErledigteLöschenVorDemSammelnAuf():
    conftest = (Path(__file__).parents[1] / "conftest.py").read_text(encoding="utf-8")
    assert "def pytest_configure" in conftest
    assert "erledigteLöschen(" in conftest


def testUnversioniertesErledigtesBleibtLiegen(tmp_path, gitRepo):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    assert erledigteLöschen(tmp_path) == []
    assert datei.exists()
    gitRepo.festhalten("Probe")
    assert erledigteLöschen(tmp_path) == ["12-probe.md"]


def testLinksAufDasGelöschteAnliegenWerdenZuAnliegenNummer(tmp_path, gitRepo):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    anliegenAnlegen(tmp_path, "13-andere.md", guterKopf.replace("12 ", "13 "))
    plan = tmp_path / "handoff" / "plan.md"
    plan.write_text(
        "Siehe [die Probe](anliegen/12-probe.md#runde-1) und [andere](anliegen/13-andere.md).\n",
        encoding="utf-8",
    )
    nachbar = tmp_path / "handoff" / "anliegen" / "13-andere.md"
    nachbar.write_text(nachbar.read_text(encoding="utf-8") + "[x](12-probe.md)\n", encoding="utf-8")
    gitRepo.festhalten("Probe")
    erledigteLöschen(tmp_path)
    assert plan.read_text(encoding="utf-8") == (
        "Siehe Anliegen 12 und [andere](anliegen/13-andere.md).\n"
    )
    assert nachbar.read_text(encoding="utf-8").endswith("Anliegen 12\n")


def testLinksAufAndereDateienBleiben(tmp_path, gitRepo):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    plan = tmp_path / "handoff" / "plan.md"
    plan.write_text("[Ablauf](../prozess/ablauf.md) [Web](https://x.de/12-probe.md)\n")
    gitRepo.festhalten("Probe")
    erledigteLöschen(tmp_path)
    assert plan.read_text() == "[Ablauf](../prozess/ablauf.md) [Web](https://x.de/12-probe.md)\n"


def testNurVorgemerktesErledigtesBleibtLiegen(tmp_path, gitRepo):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    gitRepo.git("add", "-A")
    assert erledigteLöschen(tmp_path) == []
    assert datei.exists()


def testErledigtSeitDemLetztenCommitBleibtBisZumCommitLiegen(tmp_path, gitRepo):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "angenommen"))
    gitRepo.festhalten("Probe")
    datei.write_text(datei.read_text().replace("angenommen", "erledigt"), encoding="utf-8")
    assert erledigteLöschen(tmp_path) == []
    assert datei.exists()
    gitRepo.festhalten("Probe")
    assert erledigteLöschen(tmp_path) == ["12-probe.md"]
