"""Vorgemerkte Züge des Stakeholders und verworfene Züge, je als Zeilen einer JSON-Datei."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

eingangDatei = "prozess/dashboard/eingang.jsonl"
verworfenDatei = "prozess/dashboard/verworfen.jsonl"


@dataclass(frozen=True)
class Zug:
    nummer: int
    art: str  # Warum: status, runde, antwort oder kommentar; `zuegeUebernehmen` kennt sie
    wert: str = ""
    frage: str = ""

    def beschreibung(self) -> str:
        inhalt = {
            "status": f"Status {self.wert}",
            "runde": "Runde senken",
            "antwort": f"Antwort auf {self.frage}: {self.wert}",
            "kommentar": f"Kommentar: {self.wert}",
        }
        return f"Anliegen {self.nummer} · {inhalt.get(self.art, self.art)}"


@dataclass(frozen=True)
class Verworfen:
    zug: Zug
    grund: str


def zeilenLesen(datei: Path) -> list[dict]:
    if not datei.is_file():
        return []
    eintraege = []
    for zeile in datei.read_text(encoding="utf-8").splitlines():
        try:
            eintraege.append(json.loads(zeile))
        except json.JSONDecodeError:
            continue  # Warum: eine halb geschriebene Zeile darf das Dashboard nicht stoppen
    return eintraege


def zeileAnhängen(datei: Path, eintrag: dict) -> None:
    datei.parent.mkdir(parents=True, exist_ok=True)
    with datei.open("a", encoding="utf-8") as ziel:
        ziel.write(json.dumps(eintrag, ensure_ascii=False) + "\n")


def zugVormerken(ordner: Path, zug: Zug) -> None:
    zeileAnhängen(ordner / eingangDatei, asdict(zug))


def vorgemerkte(ordner: Path) -> list[Zug]:
    return [Zug(**eintrag) for eintrag in zeilenLesen(ordner / eingangDatei)]


def ersteVorgemerkteEntfernen(ordner: Path, anzahl: int) -> None:
    """Entfernt die ersten Zeilen und lässt, was inzwischen dazukam, stehen."""
    datei = ordner / eingangDatei
    if not datei.is_file():
        return
    zeilen = datei.read_text(encoding="utf-8").splitlines(keepends=True)
    datei.write_text("".join(zeilen[anzahl:]), encoding="utf-8")


def verworfenVermerken(ordner: Path, verworfen: Verworfen) -> None:
    zeileAnhängen(ordner / verworfenDatei, {**asdict(verworfen.zug), "grund": verworfen.grund})


def verworfene(ordner: Path) -> list[Verworfen]:
    ergebnis = []
    for eintrag in zeilenLesen(ordner / verworfenDatei):
        grund = eintrag.pop("grund", "")
        ergebnis.append(Verworfen(Zug(**eintrag), grund))
    return ergebnis


def verworfeneLeeren(ordner: Path) -> None:
    (ordner / verworfenDatei).unlink(missing_ok=True)
