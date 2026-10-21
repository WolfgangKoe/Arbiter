import os
import re
import subprocess

from anliegenregeln.anliegenTest import alterKopf, anliegenAnlegen, guterKopf
from anliegenregeln.freieNummer import hauptprogramm
from anliegenregeln.kopfUmschreiben import köpfeUmschreiben
from gemeinsam.pfade import wurzel
from lesen.anliegenKopf import kopfLesen


def testAlteKöpfeWerdenFelderUndNeueBleiben(tmp_path):
    alt = anliegenAnlegen(tmp_path, "12-alt.md", alterKopf + " · wartet auf die Prozessphase")
    neu = anliegenAnlegen(tmp_path, "13-neu.md", guterKopf)
    vorher = neu.read_text(encoding="utf-8")
    assert köpfeUmschreiben(tmp_path) == ["12-alt.md"]
    assert "Von: Architekt\nAn: Planer\nRunde: 1/3\nStatus: offen\nWartet auf: Prozessphase" in (
        alt.read_text(encoding="utf-8")
    )
    assert kopfLesen(alt).wartetAuf == "die Prozessphase"
    assert neu.read_text(encoding="utf-8") == vorher
    assert köpfeUmschreiben(tmp_path) == []


def testFreieNummerAlsBefehlNenntDieNummerOderScheitert(tmp_path, monkeypatch, capsys):
    anliegenAnlegen(tmp_path, "1980-erste.md", guterKopf)
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    assert hauptprogramm(["1980", "1981"]) == 0
    assert capsys.readouterr().out == "1981\n"
    assert hauptprogramm(["1980", "1980"]) == 1
    assert hauptprogramm(["x"]) == 1


def testDerInRegelnGenannteBefehlFürFreieNummernLäuftAlsKindprozess():
    regeln = (wurzel / "prozess" / "regeln.md").read_text(encoding="utf-8")
    zeile = next(zeile for zeile in regeln.splitlines() if "anliegenregeln.freieNummer" in zeile)
    befehl = re.search(r"`(python3 [^`]*anliegenregeln\.freieNummer <erste> <letzte>)`", zeile)
    assert befehl, "Regeln nennen keinen Befehl mit <erste> <letzte>"
    lauf = subprocess.run(
        befehl.group(1).replace("<erste>", "9000").replace("<letzte>", "9001").split(),
        cwd=wurzel,
        env={name: wert for name, wert in os.environ.items() if name != "PYTHONPATH"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert lauf.returncode == 0, lauf.stderr
    assert lauf.stdout.strip() == "9000"
