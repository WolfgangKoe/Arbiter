import json
from pathlib import Path

from einstellungen import hookBefehle, skripte, verstöße

wurzel = Path(__file__).resolve().parents[2]


def einstellungenMit(tmp_path: Path, befehl: str) -> None:
    datei = tmp_path / ".claude" / "settings.json"
    datei.parent.mkdir(parents=True)
    gruppe = {"hooks": [{"type": "command", "command": befehl}]}
    datei.write_text(json.dumps({"hooks": {"PreToolUse": [gruppe]}}), encoding="utf-8")


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
