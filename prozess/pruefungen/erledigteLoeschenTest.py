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
