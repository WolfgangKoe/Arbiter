"""SonarLint ohne VS Code: der Analysator der Erweiterung meldet die Funde des Standardprofils."""

import json
import os
import subprocess
import sys
import threading
from pathlib import Path
from typing import BinaryIO

from pfade import akzeptanzOrdner, wurzel

geprüfteOrdner = ("technik/arbiter", "technik/tests/einheit", akzeptanzOrdner, "prozess/pruefungen")
erweiterungenOrdner = Path.home() / ".vscode" / "extensions"
umgebungsvariable = "SONARLINT_ERWEITERUNG"
wartezeitSekunden = 120
# Warum: Ein Update der Erweiterung brächte still neue Regeln; die Version hebt man bewusst.
erwarteteVersion = "6.0."
dateiAnfrage = "sonarlint/listFilesInFolder"
offenAnfrage = "sonarlint/isOpenInEditor"
konfigurationAnfrage = "workspace/configuration"


# Warum: Bezeichner und Dateinamen sind camelCase (wir.md, 1 und 2), das Profil will snake_case.
abgeschalteteRegeln = (
    "python:S100",
    "python:S101",
    "python:S116",
    "python:S117",
    "python:S1542",
    "python:S1578",
)


def version(ordner: Path) -> str:
    """Feld `version` aus `package.json` der Erweiterung."""
    paket = ordner / "package.json"
    assert paket.is_file(), (
        f"SonarLint-Erweiterung {ordner}: Version nicht erkennbar, kein package.json"
    )
    return json.loads(paket.read_text(encoding="utf-8"))["version"]


def versionszahlen(ordner: Path) -> tuple[int, ...]:
    return tuple(int(teil) for teil in version(ordner).split("."))


def erweiterungFinden() -> Path:
    """Ordner der SonarLint-Erweiterung: `SONARLINT_ERWEITERUNG` oder die neueste in VS Code."""
    vorgabe = os.environ.get(umgebungsvariable)
    # Warum: VS Code lässt alte, auch halb gelöschte Versionsordner liegen; sie zählen nicht.
    gefunden = (
        [Path(vorgabe)]
        if vorgabe
        else [
            ordner
            for ordner in erweiterungenOrdner.glob("sonarsource.sonarlint-vscode-*")
            if (ordner / "package.json").is_file()
        ]
    )
    gefunden = sorted(gefunden, key=versionszahlen)
    assert gefunden, f"SonarLint-Erweiterung fehlt in {erweiterungenOrdner}; {umgebungsvariable}"
    neueste = gefunden[-1]
    installiert = version(neueste)
    assert (installiert + ".").startswith(erwarteteVersion), (
        f"SonarLint-Erweiterung {neueste.name} hat Version {installiert} "
        f"statt {erwarteteVersion}x: `erwarteteVersion` in sonarlint.py bewusst heben"
    )
    return neueste


def serverAufruf(erweiterung: Path) -> list[str]:
    analysator = erweiterung / "analyzers" / "sonarpython.jar"
    server = erweiterung / "server" / "sonarlint-ls.jar"
    return ["java", "-jar", str(server), "-stdio", "-analyzers", str(analysator)]


def nachrichtSchreiben(strom: BinaryIO, nachricht: dict) -> None:
    inhalt = json.dumps(nachricht).encode()
    strom.write(b"Content-Length: %d\r\n\r\n" % len(inhalt) + inhalt)
    strom.flush()


def nachrichtLesen(strom: BinaryIO) -> dict | None:
    kopf = b""
    while not kopf.endswith(b"\r\n\r\n"):
        zeichen = strom.read(1)
        if not zeichen:
            return None
        kopf += zeichen
    länge = int(kopf.split(b":")[1].split()[0])
    return json.loads(strom.read(länge))


def dateiEintrag(datei: Path) -> dict:
    return {
        "fileName": datei.name,
        "uri": datei.as_uri(),
        "filePath": str(datei),
        "content": datei.read_text(encoding="utf-8"),
        "isTest": False,
        "detectedLanguage": "python",
    }


def antwortAuf(anfrage: dict, dateien: list[Path]):
    """Antwort des Clients auf eine Anfrage des Servers."""
    art = anfrage["method"]
    if art == konfigurationAnfrage:
        regeln = {regel: {"level": "off"} for regel in abgeschalteteRegeln}
        return [
            {"rules": regeln} if eintrag["section"] == "sonarlint" else {}
            for eintrag in anfrage["params"]["items"]
        ]
    if art == offenAnfrage:
        return True
    if art == dateiAnfrage:
        return {"foundFiles": [dateiEintrag(datei) for datei in dateien]}
    return None


def initialisierung(ordner: Path) -> dict:
    optionen = {
        "productKey": "arbiter",
        "productName": "arbiter",
        "productVersion": "0",
        "workspaceName": ordner.name,
        "platform": "linux",
        "architecture": "x64",
        "additionalAttributes": {},
        "disableTelemetry": True,
        "showVerboseLogs": False,
        "firstSecretDetected": False,
        "enableNotebooks": False,
        "includeRuleDetailsInCodeAction": False,
    }
    parameter = {
        "processId": None,
        "rootUri": ordner.as_uri(),
        "capabilities": {},
        "workspaceFolders": [{"uri": ordner.as_uri(), "name": ordner.name}],
        "initializationOptions": optionen,
    }
    return {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": parameter}


def öffnen(datei: Path) -> dict:
    """Meldet dem Server die Datei als im Editor geöffnet; er antwortet mit `publishDiagnostics`."""
    text = {"uri": datei.as_uri(), "languageId": "python", "version": 1}
    text["text"] = datei.read_text(encoding="utf-8")
    return {"jsonrpc": "2.0", "method": "textDocument/didOpen", "params": {"textDocument": text}}


def fundText(ordner: Path, datei: Path, diagnose: dict) -> str:
    zeile = diagnose["range"]["start"]["line"] + 1
    return f"{datei.relative_to(ordner)}:{zeile}: {diagnose['code']} {diagnose['message']}"


def dateienSammeln(ordner: Path, unterordner: tuple[str, ...]) -> list[Path]:
    dateien: list[Path] = []
    for name in unterordner:
        gefunden = [
            datei
            for datei in sorted((ordner / name).rglob("*.py"))
            if "__pycache__" not in datei.parts
        ]
        assert gefunden, f"{name}: Ordner fehlt oder hat keine .py-Datei, SonarLint prüfte nichts"
        dateien += gefunden
    return dateien


def funde(ordner: Path, dateien: list[Path]) -> list[str]:
    """Funde des Standardprofils zu `dateien`, je Zeile `pfad:zeile: regel meldung`."""
    server = subprocess.Popen(
        serverAufruf(erweiterungFinden()),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    sitzung = Sitzung(server, ordner, dateien)
    abbruch = threading.Timer(wartezeitSekunden, sitzung.abbrechen)
    abbruch.start()
    try:
        return sitzung.lauf()
    finally:
        abbruch.cancel()
        server.kill()


class Sitzung:
    """Gespräch mit dem Server: Dateien nacheinander öffnen, ihre Funde einsammeln."""

    def __init__(self, server: subprocess.Popen, ordner: Path, dateien: list[Path]):
        self.server = server
        self.ordner = ordner
        self.dateien = dateien
        self.übrige = list(dateien)
        self.erwartet: Path | None = None
        self.bereit = False
        self.funde: list[str] = []
        self.zeitüberschreitung = False

    def abbrechen(self) -> None:
        self.zeitüberschreitung = True
        self.server.kill()

    def senden(self, nachricht: dict) -> None:
        nachrichtSchreiben(self.server.stdin, nachricht)

    def behandeln(self, nachricht: dict) -> None:
        art = nachricht.get("method")
        if nachricht.get("id") == 1 and "result" in nachricht:
            self.senden({"jsonrpc": "2.0", "method": "initialized", "params": {}})
        elif art is not None and "id" in nachricht:
            antwort = antwortAuf(nachricht, self.dateien)
            self.senden({"jsonrpc": "2.0", "id": nachricht["id"], "result": antwort})
        elif art == "sonarlint/didChangePluginStatuses":
            self.bereit = True
        elif art == "textDocument/publishDiagnostics":
            self.fundeAufnehmen(nachricht["params"])

    def fundeAufnehmen(self, parameter: dict) -> None:
        if self.erwartet is None or parameter["uri"] != self.erwartet.as_uri():
            return
        for diagnose in parameter["diagnostics"]:
            self.funde.append(fundText(self.ordner, self.erwartet, diagnose))
        self.erwartet = None
        self.bereit = True

    def nächsteÖffnen(self) -> None:
        self.bereit = False
        self.erwartet = self.übrige.pop(0)
        self.senden(öffnen(self.erwartet))

    def lauf(self) -> list[str]:
        # Warum: Alle Dateien zugleich geöffnet liefern je Lauf andere Funde, nacheinander stabil.
        self.senden(initialisierung(self.ordner))
        while not (self.bereit and not self.übrige):
            nachricht = nachrichtLesen(self.server.stdout)
            assert not self.zeitüberschreitung, f"SonarLint nach {wartezeitSekunden} s abgebrochen"
            assert nachricht is not None, "Der SonarLint-Server hat sich vor dem Ergebnis beendet"
            self.behandeln(nachricht)
            if self.bereit and self.übrige:
                self.nächsteÖffnen()
        return self.funde


def lauf(ordner: Path, unterordner: tuple[str, ...]) -> list[str]:
    dateien = dateienSammeln(ordner, unterordner)
    return funde(ordner, dateien)


def einstellung() -> str:
    """Block für die Benutzereinstellungen von VS Code, gleiche Regeln wie die Sperre."""
    regeln = {regel: {"level": "off"} for regel in abgeschalteteRegeln}
    return json.dumps({"sonarlint.rules": regeln}, indent=2)


if __name__ == "__main__":
    if "--einstellung" in sys.argv:
        print(einstellung())
        sys.exit(0)
    meldungen = lauf(wurzel, geprüfteOrdner)
    print("\n".join(meldungen) or "SonarLint: keine Funde")
    sys.exit(1 if meldungen else 0)
