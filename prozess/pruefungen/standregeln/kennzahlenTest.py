import subprocess
import sys
from datetime import date

import pytest

from anliegenregeln.anliegenTest import anliegenAnlegen, guterKopf
from standregeln.kennzahlen import kennzahlen


def testOffeneAnliegenStehenJeRolleMitAlter(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    git = ["git", "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run([*git, "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(
        [*git, "commit", "-qm", "x", "--date=2026-01-01T12:00:00"], cwd=tmp_path, check=True
    )
    anliegenAnlegen(tmp_path, "13-neu.md", guterKopf.replace("12 ", "13 "))
    text = kennzahlen(tmp_path, date(2026, 1, 11))
    assert "- Planer: 2: 12 (10 T), 13 (0 T)" in text


def testErledigteAnliegenZählenNicht(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "erledigt"))
    assert "Planer" not in kennzahlen(tmp_path, date(2026, 1, 1))


@pytest.mark.stand
def testSkriptLäuftImRepo():
    ergebnis = subprocess.run(
        [sys.executable, "prozess/pruefungen/gemeinsam/lauf.py", "standregeln.kennzahlen"],
        capture_output=True,
        text=True,
        check=False,
        cwd=__file__.rsplit("/prozess/", 1)[0],
    )
    assert ergebnis.returncode == 0
    assert "Offene Anliegen je Rolle" in ergebnis.stdout
