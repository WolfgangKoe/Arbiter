"""Scheiter-Test und Stand: SonarLint ohne VS Code (Anliegen 150)."""

import io
from pathlib import Path
from types import SimpleNamespace

import pytest

import sonarlint
from pfade import wurzel
from sonarlint import (
    Sitzung,
    abgeschalteteRegeln,
    antwortAuf,
    dateienSammeln,
    erweiterungFinden,
    funde,
    fundText,
    geprüfteOrdner,
    nachrichtLesen,
    nachrichtSchreiben,
    öffnen,
)

ungenutzteVariable = "def zähle():\n    ergebnis = 1\n    return 2\n"
camelCaseFunktion = "def meineFunktion(eingabeWert):\n    return eingabeWert\n"
saubererCode = "def zähle():\n    return 2\n"


def probeAnlegen(tmp_path: Path) -> list[Path]:
    for name, inhalt in (
        ("schlecht.py", ungenutzteVariable),
        ("camelCase.py", camelCaseFunktion),
        ("sauber.py", saubererCode),
    ):
        (tmp_path / name).write_text(inhalt, encoding="utf-8")
    return sorted(tmp_path.glob("*.py"))


def testEineUngenutzteVariableIstEinFund(tmp_path):
    dateien = probeAnlegen(tmp_path)
    gefunden = funde(tmp_path, dateien)
    assert len(gefunden) == 1
    assert gefunden[0].startswith("schlecht.py:2: python:S1481 ")


def testDieNamensregelnDesProfilsSindAus():
    # Regel: wir.md, Regel 1; camelCase ist entschieden, `benennung.py` prüft die Namen
    assert "python:S1542" in abgeschalteteRegeln
    assert "python:S117" in abgeschalteteRegeln


def testDerFundNenntPfadZeileRegelUndMeldung(tmp_path):
    datei = tmp_path / "a.py"
    diagnose = {"range": {"start": {"line": 6}}, "code": "python:S1", "message": "Text"}
    assert fundText(tmp_path, datei.as_uri(), diagnose) == "a.py:7: python:S1 Text"


def testNachrichtenRundlaufMitLängenkopf():
    strom = io.BytesIO()
    nachrichtSchreiben(strom, {"id": 1, "text": "Ünï"})
    strom.seek(0)
    assert nachrichtLesen(strom) == {"id": 1, "text": "Ünï"}
    assert nachrichtLesen(strom) is None


def testDerKopfEinerAbgebrochenenNachrichtIstKeineNachricht():
    assert nachrichtLesen(io.BytesIO(b"Content-Length: 5\r\n")) is None


def testAntwortenAufDieAnfragenDesServers(tmp_path):
    datei = tmp_path / "a.py"
    datei.write_text("x = 1\n", encoding="utf-8")
    einträge = {"params": {"items": [{"section": "sonarlint"}, {"section": "andere"}]}}
    konfiguration = antwortAuf({"method": "workspace/configuration", **einträge}, [datei])
    assert konfiguration[0]["rules"]["python:S117"] == {"level": "off"}
    assert konfiguration[1] == {}
    assert antwortAuf({"method": "sonarlint/isOpenInEditor"}, [datei]) is True
    dateiListe = antwortAuf({"method": "sonarlint/listFilesInFolder"}, [datei])["foundFiles"]
    assert dateiListe[0]["content"] == "x = 1\n"
    assert dateiListe[0]["detectedLanguage"] == "python"
    assert antwortAuf({"method": "window/workDoneProgress/create"}, [datei]) is None


def testGeöffnetWirdDerInhaltDerDatei(tmp_path):
    datei = tmp_path / "a.py"
    datei.write_text("x = 1\n", encoding="utf-8")
    text = öffnen(datei)["params"]["textDocument"]
    assert text["text"] == "x = 1\n"
    assert text["uri"] == datei.as_uri()


def testGesammeltWerdenPythonDateienOhnePycache(tmp_path):
    (tmp_path / "ordner" / "__pycache__").mkdir(parents=True)
    (tmp_path / "ordner" / "a.py").write_text("")
    (tmp_path / "ordner" / "__pycache__" / "b.py").write_text("")
    (tmp_path / "ordner" / "c.txt").write_text("")
    assert dateienSammeln(tmp_path, ("ordner",)) == [tmp_path / "ordner" / "a.py"]


def testDieErweiterungKommtAusDerUmgebungsvariable(monkeypatch, tmp_path):
    monkeypatch.setenv(sonarlint.umgebungsvariable, str(tmp_path))
    assert erweiterungFinden() == tmp_path


def testDieNeuesteErweiterungAusVsCodeGewinnt(monkeypatch, tmp_path):
    monkeypatch.delenv(sonarlint.umgebungsvariable, raising=False)
    monkeypatch.setattr(sonarlint, "erweiterungenOrdner", tmp_path)
    for version in ("6.0.1", "6.1.0"):
        (tmp_path / f"sonarsource.sonarlint-vscode-{version}-linux-x64").mkdir()
    assert erweiterungFinden().name == "sonarsource.sonarlint-vscode-6.1.0-linux-x64"


def testOhneErweiterungIstDiePrüfungRotUndNenntDieUmgebungsvariable(monkeypatch, tmp_path):
    monkeypatch.delenv(sonarlint.umgebungsvariable, raising=False)
    monkeypatch.setattr(sonarlint, "erweiterungenOrdner", tmp_path)
    with pytest.raises(AssertionError, match=sonarlint.umgebungsvariable):
        erweiterungFinden()


def testEinServerDerSichBeendetIstRot(tmp_path):
    server = SimpleNamespace(stdin=io.BytesIO(), stdout=io.BytesIO())
    sitzung = Sitzung(server, tmp_path, [])
    with pytest.raises(AssertionError, match="beendet"):
        sitzung.lauf()


@pytest.mark.stand
def testSonarLintMeldetNichtsZuProduktUndPrüfskripten():
    # Regel: ablauf.md, Technikphase, Werkzeuge: Die Sperre ist mindestens so streng wie SonarLint
    assert funde(wurzel, dateienSammeln(wurzel, geprüfteOrdner)) == []
