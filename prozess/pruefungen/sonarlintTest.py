"""Scheiter-Test und Stand: SonarLint ohne VS Code."""

import io
import json
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
    einstellung,
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


class ServerAttrappe:
    def __init__(self):
        self.stdin = io.BytesIO()
        self.stdout = io.BytesIO()

    def kill(self) -> None:
        pass


def erweiterungAnlegen(ordner: Path, version: str) -> Path:
    ordner.mkdir()
    (ordner / "package.json").write_text(json.dumps({"version": version}), encoding="utf-8")
    return ordner


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


def testZweiAufrufeInPytestRaisesSindEinFund(tmp_path):
    # Regel: Anliegen 179, Einheitstests mit S5778 sperrt die Prüfung
    text = (
        "import pytest\n\n\n"
        "def baue():\n    return 1\n\n\n"
        "def wirf(wert):\n    raise ValueError(wert)\n\n\n"
        "def testWirft():\n"
        "    with pytest.raises(ValueError):\n"
        "        wirf(baue())\n"
    )
    datei = tmp_path / "wirftTest.py"
    datei.write_text(text, encoding="utf-8")
    gefunden = funde(tmp_path, [datei])
    assert any("python:S5778" in fund for fund in gefunden)


def testDieEinheitstestsSindGeprüft():
    assert "technik/tests/einheit" in geprüfteOrdner


def testDieNamensregelnDesProfilsSindAus():
    # Regel: wir.md, Regel 1; camelCase ist entschieden, `benennung.py` prüft die Namen
    assert "python:S1542" in abgeschalteteRegeln
    assert "python:S117" in abgeschalteteRegeln


def testDerFundNenntPfadZeileRegelUndMeldung(tmp_path):
    datei = tmp_path / "a.py"
    diagnose = {"range": {"start": {"line": 6}}, "code": "python:S1", "message": "Text"}
    assert fundText(tmp_path, datei, diagnose) == "a.py:7: python:S1 Text"


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
    ordner = erweiterungAnlegen(tmp_path / "sonarlint", "6.0.3")
    monkeypatch.setenv(sonarlint.umgebungsvariable, str(ordner))
    assert erweiterungFinden() == ordner


def testDieNeuesteErweiterungAusVsCodeGewinnt(monkeypatch, tmp_path):
    monkeypatch.delenv(sonarlint.umgebungsvariable, raising=False)
    monkeypatch.setattr(sonarlint, "erweiterungenOrdner", tmp_path)
    for version in ("6.0.1", "6.0.2"):
        erweiterungAnlegen(tmp_path / f"sonarsource.sonarlint-vscode-{version}-linux-x64", version)
    assert erweiterungFinden().name == "sonarsource.sonarlint-vscode-6.0.2-linux-x64"


def testEinAlterOrdnerOhnePackageJsonStörtDieNeuesteNicht(monkeypatch, tmp_path):
    monkeypatch.delenv(sonarlint.umgebungsvariable, raising=False)
    monkeypatch.setattr(sonarlint, "erweiterungenOrdner", tmp_path)
    (tmp_path / "sonarsource.sonarlint-vscode-6.0.0-linux-x64").mkdir()
    erweiterungAnlegen(tmp_path / "sonarsource.sonarlint-vscode-6.0.1-linux-x64", "6.0.1")
    assert erweiterungFinden().name == "sonarsource.sonarlint-vscode-6.0.1-linux-x64"


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


def testEinFehlenderOrdnerIstRotUndNenntSeinenNamen(tmp_path):
    with pytest.raises(AssertionError, match="gibtsNicht"):
        dateienSammeln(tmp_path, ("gibtsNicht",))


def testEinOrdnerOhnePythonDateienIstRot(tmp_path):
    (tmp_path / "leer").mkdir()
    with pytest.raises(AssertionError, match="leer"):
        dateienSammeln(tmp_path, ("leer",))


def testDieVersionsordnerWerdenNachZahlSortiert(monkeypatch, tmp_path):
    monkeypatch.delenv(sonarlint.umgebungsvariable, raising=False)
    monkeypatch.setattr(sonarlint, "erweiterungenOrdner", tmp_path)
    monkeypatch.setattr(sonarlint, "erwarteteVersion", "6.")
    for version in ("6.9.0", "6.10.0"):
        erweiterungAnlegen(tmp_path / f"sonarsource.sonarlint-vscode-{version}-linux-x64", version)
    assert "6.10.0" in erweiterungFinden().name


def testEineAndereVersionAlsErwartetIstRotUndNenntBeide(monkeypatch, tmp_path):
    monkeypatch.delenv(sonarlint.umgebungsvariable, raising=False)
    monkeypatch.setattr(sonarlint, "erweiterungenOrdner", tmp_path)
    erweiterungAnlegen(tmp_path / "sonarsource.sonarlint-vscode-7.0.0-linux-x64", "7.0.0")
    with pytest.raises(AssertionError, match=r"7\.0\.0.*6\.0\."):
        erweiterungFinden()


def testNachDerWartezeitMeldetDiePrüfungDieWartezeit(tmp_path):
    server = ServerAttrappe()
    sitzung = Sitzung(server, tmp_path, [])
    sitzung.abbrechen()
    with pytest.raises(AssertionError, match="abgebrochen"):
        sitzung.lauf()


def testDieEinstellungNenntGenauDieAbgeschaltetenRegeln():
    regeln = json.loads(einstellung())["sonarlint.rules"]
    assert set(regeln) == set(abgeschalteteRegeln)
    assert all(wert == {"level": "off"} for wert in regeln.values())


@pytest.mark.stand
def testPreCommitPrüftSonarLintBeiPythonDateien():
    konfiguration = (wurzel / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert "python3 prozess/pruefungen/sonarlint.py" in konfiguration


def testEinOrdnerOhnePackageJsonHatKeineErkennbareVersion(monkeypatch, tmp_path):
    ordner = tmp_path / "sonarlint"
    ordner.mkdir()
    monkeypatch.setenv(sonarlint.umgebungsvariable, str(ordner))
    with pytest.raises(AssertionError, match=r"sonarlint: Version nicht erkennbar"):
        erweiterungFinden()
