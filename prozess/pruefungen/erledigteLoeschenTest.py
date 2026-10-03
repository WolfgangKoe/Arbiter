import subprocess
import sys
from pathlib import Path

from anliegenTest import anliegenAnlegen, guterKopf
from erledigteLoeschen import erledigteLöschen

wurzel = Path(__file__).resolve().parents[2]


def testErledigtesAnliegenWirdGelöscht(tmp_path):
    erledigt = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    offen = anliegenAnlegen(tmp_path, "13-probe.md", guterKopf.replace("12 ", "13 "))
    assert erledigteLöschen(tmp_path) == ["12-probe.md"]
    assert not erledigt.exists()
    assert offen.exists()


def testOhneErledigteBleibtAllesStehen(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert erledigteLöschen(tmp_path) == []
    assert datei.exists()


def testPrüflaufLöschtErledigteAnliegenVorDemSammeln():
    probe = wurzel / "handoff" / "anliegen" / "99-probeErledigt.md"
    probe.write_text(f"# Probe\n\n{guterKopf.replace('12 ', '99 ').replace('offen', 'erledigt')}\n")
    subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", str(Path(__file__).parent)],
        cwd=wurzel, capture_output=True, check=False,
    )
    try:
        assert not probe.exists()
    finally:
        probe.unlink(missing_ok=True)


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
    erledigteLöschen(tmp_path)
    assert plan.read_text(encoding="utf-8") == (
        "Siehe Anliegen 12 und [andere](anliegen/13-andere.md).\n"
    )
    assert nachbar.read_text(encoding="utf-8").endswith("Anliegen 12\n")


def testLinksAufAndereDateienBleiben(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    plan = tmp_path / "handoff" / "plan.md"
    plan.write_text("[Ablauf](../prozess/ablauf.md) [Web](https://x.de/12-probe.md)\n")
    erledigteLöschen(tmp_path)
    assert plan.read_text() == "[Ablauf](../prozess/ablauf.md) [Web](https://x.de/12-probe.md)\n"
