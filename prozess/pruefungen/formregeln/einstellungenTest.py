import json
import os
import subprocess
from pathlib import Path

import pytest

from formregeln.einstellungen import hookBefehle, skripte, verstöße
from gemeinsam.pfade import wurzel


def einstellungenMit(tmp_path: Path, befehl: str) -> None:
    datei = tmp_path / ".claude" / "settings.json"
    datei.parent.mkdir(parents=True)
    gruppe = {"hooks": [{"type": "command", "command": befehl}]}
    datei.write_text(json.dumps({"hooks": {"PreToolUse": [gruppe]}}), encoding="utf-8")


@pytest.mark.stand
def testJederHookDerEinstellungenZeigtAufEineVorhandeneDatei():
    assert verstöße(wurzel) == []


def testHookAufFehlendeDateiIstRot(tmp_path):
    einstellungenMit(tmp_path, 'python3 "$CLAUDE_PROJECT_DIR/prozess/pruefungen/belegung.py"')
    assert verstöße(tmp_path) == [
        'Hook `python3 "$CLAUDE_PROJECT_DIR/prozess/pruefungen/belegung.py"`: belegung.py fehlt'
    ]


def testHookAufDateiMitSyntaxfehlerIstRot(tmp_path):
    einstellungenMit(tmp_path, 'python3 "$CLAUDE_PROJECT_DIR/kaputt.py"')
    (tmp_path / "kaputt.py").write_text("def (:\n", encoding="utf-8")
    assert "kein gültiges Python" in verstöße(tmp_path)[0]


def testHookAufVorhandeneDateiIstGrün(tmp_path):
    einstellungenMit(tmp_path, 'python3 "$CLAUDE_PROJECT_DIR/ok.py"')
    (tmp_path / "ok.py").write_text("x = 1\n", encoding="utf-8")
    assert verstöße(tmp_path) == []


def testBefehleUndSkriptpfadeWerdenAusDenEinstellungenGelesen(tmp_path):
    einstellungenMit(tmp_path, 'python3 "${CLAUDE_PROJECT_DIR}/a/b.py"')
    einstellungen = json.loads((tmp_path / ".claude" / "settings.json").read_text())
    befehl = hookBefehle(einstellungen)[0]
    assert skripte(befehl, tmp_path) == [tmp_path / "a" / "b.py"]


def testHinterDemStarterStehtDasPrüfskriptAlsModul(tmp_path):
    befehl = 'python3 "$CLAUDE_PROJECT_DIR/pruefungen/gemeinsam/lauf.py" rollenregeln.belegung'
    assert skripte(befehl, tmp_path) == [
        tmp_path / "pruefungen" / "gemeinsam" / "lauf.py",
        tmp_path / "pruefungen" / "rollenregeln" / "belegung.py",
    ]


def testHookAufFehlendesModulHinterDemStarterIstRot(tmp_path):
    befehl = 'python3 "$CLAUDE_PROJECT_DIR/p/gemeinsam/lauf.py" rollenregeln.fehlt'
    einstellungenMit(tmp_path, befehl)
    starter = tmp_path / "p" / "gemeinsam" / "lauf.py"
    starter.parent.mkdir(parents=True)
    starter.write_text("x = 1\n", encoding="utf-8")
    assert verstöße(tmp_path) == [f"Hook `{befehl}`: fehlt.py fehlt"]


@pytest.mark.stand
def testKeinHookBrauchtPythonpath():
    einstellungen = json.loads((wurzel / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert [befehl for befehl in hookBefehle(einstellungen) if "PYTHONPATH" in befehl] == []


@pytest.mark.stand
def testJederHookLäuftOhnePythonpathBisZumImport(tmp_path):
    einstellungen = json.loads((wurzel / ".claude" / "settings.json").read_text(encoding="utf-8"))
    umgebung = {
        key: wert for key, wert in os.environ.items() if key not in ("PYTHONPATH", "PYTHONHOME")
    }
    umgebung["CLAUDE_PROJECT_DIR"] = str(tmp_path)
    for befehl in sorted(set(hookBefehle(einstellungen))):
        lauf = subprocess.run(
            befehl.replace("$CLAUDE_PROJECT_DIR", str(wurzel)),
            shell=True,
            input="{}",
            env=umgebung,
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=False,
        )
        assert "ImportError" not in lauf.stderr, f"{befehl}: {lauf.stderr}"


@pytest.mark.stand
def testKeineErlaubnisNenntPythonpath():
    einstellungen = json.loads((wurzel / ".claude" / "settings.json").read_text(encoding="utf-8"))
    erlaubt = einstellungen["permissions"]["allow"]
    assert [eintrag for eintrag in erlaubt if "PYTHONPATH" in eintrag] == []
