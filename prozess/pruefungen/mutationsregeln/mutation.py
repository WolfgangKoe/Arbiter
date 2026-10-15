"""Mutationstest: baut Fehler in geänderte Domänenmodule und nennt, welche kein Test bemerkt."""

import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import NamedTuple

from formregeln.glossar import domaeneOrdner
from gemeinsam.gitAufruf import freigaben, gitAusgabe
from gemeinsam.pfade import projektordner
from mutationsregeln.mutanten import mutantenVon

# Regel: Einheitstests zuerst, denn sie scheitern am schnellsten; dann die Akzeptanztests.
testpfade = ("technik/tests/einheit/domaene", "technik/tests/akzeptanz")
# Warum: Noch keine Mindestzahl; die Schwelle folgt nach dem ersten Lauf (Retro 5, P3).
schwelle = 0
sekundenMindestens = 10
wartefaktor = 3
volleProzent = 100
planFreigabe = "Freigabe Plan "
# Warum: Ohne Bytecode-Datei läuft kein Mutant in der zwischengespeicherten Fassung des Vorgängers.
umgebung = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


class Überlebender(NamedTuple):
    datei: str
    zeile: int
    beschreibung: str


class Ergebnis(NamedTuple):
    gesamt: int
    überlebende: list[Überlebender]

    @property
    def prozentGefangen(self) -> int:
        if not self.gesamt:
            return volleProzent
        return (self.gesamt - len(self.überlebende)) * volleProzent // self.gesamt


def geänderteModule(wurzel: Path) -> list[str]:
    """Domänenmodule, die seit der jüngsten `Freigabe Plan` geändert oder neu sind."""
    plan = next(
        (frei.kennung for frei in freigaben(wurzel) if frei.betreff.startswith(planFreigabe)),
        "HEAD",
    )
    ohneAnführung = ("-c", "core.quotepath=false")
    geändert = gitAusgabe(
        wurzel, *ohneAnführung, "diff", "--name-only", plan, "--", domaeneOrdner
    ).splitlines()
    neu = gitAusgabe(
        wurzel, *ohneAnführung, "ls-files", "--others", "--exclude-standard", "--", domaeneOrdner
    ).splitlines()
    vorhanden = (name for name in sorted({*geändert, *neu}) if (wurzel / name).is_file())
    return [name for name in vorhanden if name.endswith(".py")]


def testenAufrufen(kopie: Path, pfade: tuple[str, ...], wartezeit: float) -> bool:
    """Wahr, wenn alle Tests der Kopie grün sind; Absturz oder Zeitüberschreitung ist rot."""
    befehl = [sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *pfade]
    try:
        lauf = subprocess.run(
            befehl, cwd=kopie, env=umgebung, capture_output=True, check=False, timeout=wartezeit
        )
    except subprocess.TimeoutExpired:
        return False
    return lauf.returncode == 0


def kopieAnlegen(wurzel: Path, ziel: Path) -> None:
    ignorieren = shutil.ignore_patterns("__pycache__", "node_modules", "*.pyc")
    shutil.copytree(wurzel / "technik", ziel / "technik", ignore=ignorieren)
    shutil.copy(wurzel / "pyproject.toml", ziel / "pyproject.toml")
    # Warum: Der Katalog liest seine Daten aus `domaene/daten`, zwei Ordner über dem Produkt.
    daten = wurzel / "domaene" / "daten"
    if daten.is_dir():
        shutil.copytree(daten, ziel / "domaene" / "daten")


def mutationenPrüfen(
    wurzel: Path, module: list[str], pfade: tuple[str, ...] = testpfade
) -> Ergebnis:
    """Baut je Mutant eines Moduls in eine Kopie des Repos und lässt die Tests laufen."""
    überlebende: list[Überlebender] = []
    gesamt = 0
    with tempfile.TemporaryDirectory() as ordner:
        kopie = Path(ordner)
        kopieAnlegen(wurzel, kopie)
        beginn = time.monotonic()
        grün = testenAufrufen(kopie, pfade, 3600)
        assert grün, "Die Tests sind ohne Mutant rot; so zeigt keiner eine Lücke"
        wartezeit = max(sekundenMindestens, wartefaktor * (time.monotonic() - beginn))
        for modul in module:
            original = (wurzel / modul).read_text(encoding="utf-8")
            for mutant in mutantenVon(original):
                gesamt += 1
                (kopie / modul).write_text(mutant.quelle, encoding="utf-8")
                if testenAufrufen(kopie, pfade, wartezeit):
                    überlebende.append(Überlebender(modul, mutant.zeile, mutant.beschreibung))
            (kopie / modul).write_text(original, encoding="utf-8")
    return Ergebnis(gesamt, überlebende)


def bericht(ergebnis: Ergebnis) -> str:
    lücken = [f"{lücke.datei}:{lücke.zeile} {lücke.beschreibung}" for lücke in ergebnis.überlebende]
    kopf = (
        f"{ergebnis.gesamt} Mutanten, {ergebnis.prozentGefangen} % gefangen, Schwelle {schwelle} %"
    )
    return "\n".join([*lücken, kopf])


def main(argumente: list[str]) -> int:
    wurzel = projektordner()
    module = argumente or geänderteModule(wurzel)
    ergebnis = mutationenPrüfen(wurzel, module)
    print(bericht(ergebnis))
    return 1 if ergebnis.prozentGefangen < schwelle else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
