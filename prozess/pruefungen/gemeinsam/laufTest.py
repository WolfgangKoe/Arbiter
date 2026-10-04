import os
import subprocess
import sys

from gemeinsam.lauf import starten
from gemeinsam.pfade import wurzel

starter = wurzel / "prozess" / "pruefungen" / "gemeinsam" / "lauf.py"


def ohnePythonpath() -> dict[str, str]:
    return {schlüssel: wert for schlüssel, wert in os.environ.items() if schlüssel != "PYTHONPATH"}


def testDerStarterFindetQuerimporteOhnePythonpath():
    lauf = subprocess.run(
        [sys.executable, str(starter), "formregeln.einstellungen"],
        cwd=wurzel,
        env={**ohnePythonpath(), "CLAUDE_PROJECT_DIR": str(wurzel)},
        capture_output=True,
        text=True,
        check=False,
    )
    assert lauf.returncode == 0, lauf.stderr


def testEinUnbekanntesModulIstRot():
    lauf = subprocess.run(
        [sys.executable, str(starter), "gibtEsNicht"],
        cwd=wurzel,
        env=ohnePythonpath(),
        capture_output=True,
        text=True,
        check=False,
    )
    assert lauf.returncode != 0
    assert "gibtEsNicht" in lauf.stderr


def testDerStarterGibtDieArgumenteAnDasSkriptWeiter(monkeypatch, capsys):
    monkeypatch.setattr(sys, "path", ["x", *sys.path])
    monkeypatch.setattr(sys, "argv", ["alt"])
    starten("gemeinsam.argumenteProbe", ["a", "b"])
    assert capsys.readouterr().out.strip() == "['a', 'b']"


def testImWurzelordnerDerPrüfskripteLiegtNurDieConftest():
    module = sorted(datei.name for datei in starter.parents[1].glob("*.py"))
    assert module == ["conftest.py"]
