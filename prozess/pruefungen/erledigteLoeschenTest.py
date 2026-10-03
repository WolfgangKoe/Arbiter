import subprocess
from pathlib import Path

from anliegenTest import anliegenAnlegen, guterKopf
from erledigteLoeschen import erledigteLöschen

wurzel = Path(__file__).resolve().parents[2]
identität = ["-c", "user.name=t", "-c", "user.email=t@t"]


def versionieren(ordner: Path) -> None:
    """Legt in `ordner` ein git-Archiv an und committet alle Dateien."""
    for befehl in (["init", "-q"], ["add", "-A"], [*identität, "commit", "-q", "-m", "Probe"]):
        subprocess.run(["git", *befehl], cwd=ordner, check=True, capture_output=True)


def testErledigtesAnliegenWirdGelöscht(tmp_path):
    erledigt = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    offen = anliegenAnlegen(tmp_path, "13-probe.md", guterKopf.replace("12 ", "13 "))
    versionieren(tmp_path)
    assert erledigteLöschen(tmp_path) == ["12-probe.md"]
    assert not erledigt.exists()
    assert offen.exists()


def testOhneErledigteBleibtAllesStehen(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert erledigteLöschen(tmp_path) == []
    assert datei.exists()


def testDerPrüflaufRuftErledigteLöschenVorDemSammelnAuf():
    conftest = (Path(__file__).parent / "conftest.py").read_text(encoding="utf-8")
    assert "def pytest_configure" in conftest
    assert "erledigteLöschen(" in conftest


def testUnversioniertesErledigtesBleibtLiegen(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    assert erledigteLöschen(tmp_path) == []
    assert datei.exists()
    versionieren(tmp_path)
    assert erledigteLöschen(tmp_path) == ["12-probe.md"]


def testLinksAufDasGelöschteAnliegenWerdenZuAnliegenNummer(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    anliegenAnlegen(tmp_path, "13-andere.md", guterKopf.replace("12 ", "13 "))
    plan = tmp_path / "handoff" / "plan.md"
    plan.write_text(
        "Siehe [die Probe](anliegen/12-probe.md#runde-1) und [andere](anliegen/13-andere.md).\n",
        encoding="utf-8",
    )
    nachbar = tmp_path / "handoff" / "anliegen" / "13-andere.md"
    nachbar.write_text(nachbar.read_text(encoding="utf-8") + "[x](12-probe.md)\n", encoding="utf-8")
    versionieren(tmp_path)
    erledigteLöschen(tmp_path)
    assert plan.read_text(encoding="utf-8") == (
        "Siehe Anliegen 12 und [andere](anliegen/13-andere.md).\n"
    )
    assert nachbar.read_text(encoding="utf-8").endswith("Anliegen 12\n")


def testLinksAufAndereDateienBleiben(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    plan = tmp_path / "handoff" / "plan.md"
    plan.write_text("[Ablauf](../prozess/ablauf.md) [Web](https://x.de/12-probe.md)\n")
    versionieren(tmp_path)
    erledigteLöschen(tmp_path)
    assert plan.read_text() == "[Ablauf](../prozess/ablauf.md) [Web](https://x.de/12-probe.md)\n"


def testNurVorgemerktesErledigtesBleibtLiegen(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    assert erledigteLöschen(tmp_path) == []
    assert datei.exists()
