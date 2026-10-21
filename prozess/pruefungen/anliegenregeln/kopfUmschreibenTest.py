from anliegenregeln.anliegenTest import alterKopf, anliegenAnlegen, guterKopf
from anliegenregeln.freieNummer import hauptprogramm
from anliegenregeln.kopfUmschreiben import köpfeUmschreiben
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
