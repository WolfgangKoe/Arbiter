"""Liest aus dem Transkript einer Rolle, welche Pfade sie angefasst hat."""

import json
from pathlib import Path

from gemeinsam.pfade import relativZurWurzel

dateiWerkzeuge = ("Write", "Edit", "NotebookEdit")


def blöckeDerZeile(zeile: str) -> list:
    try:
        nachricht = json.loads(zeile).get("message")
    except json.JSONDecodeError:
        return []
    inhalt = nachricht.get("content") if isinstance(nachricht, dict) else None
    return inhalt if isinstance(inhalt, list) else []


def werkzeugAufrufe(transkript: Path | None) -> list[tuple[str, dict]]:
    """Name und Eingabe aller Werkzeugaufrufe im Transkript; leer, wenn es fehlt."""
    if transkript is None or not transkript.is_file():
        return []
    return [
        (block.get("name", ""), block.get("input") or {})
        for zeile in transkript.read_text(encoding="utf-8").splitlines()
        for block in blöckeDerZeile(zeile)
        if isinstance(block, dict) and block.get("type") == "tool_use"
    ]


class AngefasstePfade:
    """Die Pfade, die eine Rolle in ihren Write-, Edit- und Bash-Aufrufen genannt hat."""

    def __init__(self, transkript: Path | None, wurzel: Path):
        aufrufe = werkzeugAufrufe(transkript)
        self.dateien = {
            relativZurWurzel(Path(eingabe["file_path"]), wurzel)
            for name, eingabe in aufrufe
            if name in dateiWerkzeuge and eingabe.get("file_path")
        }
        self.befehle = [eingabe.get("command", "") for name, eingabe in aufrufe if name == "Bash"]

    def enthält(self, pfad: str) -> bool:
        """Ob die Rolle den Pfad schrieb oder ihn oder seinen Ordner in einem Bash-Befehl nannte."""
        ordner = pfad.rpartition("/")[0]
        nennungen = (pfad, f"{ordner}/") if ordner else (pfad,)
        return pfad in self.dateien or any(
            nennung in befehl for befehl in self.befehle for nennung in nennungen
        )
