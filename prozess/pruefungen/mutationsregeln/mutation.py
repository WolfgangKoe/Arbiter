"""Mutationstest: baut Fehler in geänderte Zeilen und nennt, welche kein Test bemerkt."""

import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import NamedTuple

from formregeln.glossar import domaeneOrdner
from gemeinsam.pfade import projektordner
from mutationsregeln.abdeckungKontext import auswahl, messen
from mutationsregeln.ergebnisse import (
    Gleichwertig,
    gemerkt,
    gleichwertigeLesen,
    merken,
    standKennung,
)
from mutationsregeln.geaenderteZeilen import geänderteZeilen
from mutationsregeln.mutanten import Mutant, mutantenVon

testpfade = ("technik/tests",)
produktOrdner = "technik/arbiter"
schwelle = 95
sekundenMindestens = 10
wartefaktor = 3
volleProzent = 100
vollerLauf = "--voll"
ohneBytecode = {"PYTHONDONTWRITEBYTECODE": "1"}


class Überlebender(NamedTuple):
    datei: str
    zeile: int
    beschreibung: str


class Ergebnis(NamedTuple):
    gesamt: int
    überlebende: list[Überlebender]
    gleichwertige: int = 0

    @property
    def prozentGefangen(self) -> int:
        if not self.gesamt:
            return volleProzent
        return (self.gesamt - len(self.überlebende)) * volleProzent // self.gesamt


def schwelleErreicht(ergebnis: Ergebnis) -> bool:
    return ergebnis.prozentGefangen >= schwelle


def geänderteModule(wurzel: Path) -> list[str]:
    """Domänenmodule, die seit der jüngsten `Freigabe Plan` geändert oder neu sind."""
    return list(geänderteZeilen(wurzel, domaeneOrdner))


def testenAufrufen(kopie: Path, pfade: tuple[str, ...], wartezeit: float) -> bool:
    """Wahr, wenn alle Tests der Kopie grün sind; Absturz oder Zeitüberschreitung ist rot."""
    befehl = [sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *pfade]
    try:
        lauf = subprocess.run(
            befehl,
            cwd=kopie,
            env={**os.environ, **ohneBytecode},
            capture_output=True,
            check=False,
            timeout=wartezeit,
        )
    except subprocess.TimeoutExpired:
        return False
    return lauf.returncode == 0


def kopieAnlegen(wurzel: Path, ziel: Path) -> None:
    ignorieren = shutil.ignore_patterns("__pycache__", "node_modules", "*.pyc")
    shutil.copytree(wurzel / "technik", ziel / "technik", ignore=ignorieren)
    shutil.copy(wurzel / "pyproject.toml", ziel / "pyproject.toml")
    daten = wurzel / "domaene" / "daten"
    if daten.is_dir():
        shutil.copytree(daten, ziel / "domaene" / "daten")


def überlebt(
    kopie: Path, ausgewählt: tuple[str, ...] | None, pfade: tuple[str, ...], wartezeit: float
) -> bool:
    """Wahr, wenn kein Test den Mutanten fängt; ein Überlebender prüft sich gegen alle nach."""
    if ausgewählt == ():
        return True
    if ausgewählt is None:
        return testenAufrufen(kopie, pfade, wartezeit)
    return testenAufrufen(kopie, ausgewählt, wartezeit) and testenAufrufen(kopie, pfade, wartezeit)


def mutantenWählen(
    modul: str,
    original: str,
    zeilen: dict[str, set[int]] | None,
    gleichwertige: frozenset[Gleichwertig],
) -> tuple[list[tuple[int, Mutant]], int]:
    """Die Mutanten in den genannten Zeilen mit ihrer Nummer, und wie viele gleichwertig sind."""
    quellzeilen = original.splitlines()
    gewählt = []
    begründet = 0
    for nummer, mutant in enumerate(mutantenVon(original)):
        if zeilen is not None and mutant.zeile not in zeilen.get(modul, set()):
            continue
        quelle = quellzeilen[mutant.zeile - 1].strip()
        if Gleichwertig(modul, quelle, mutant.beschreibung) in gleichwertige:
            begründet += 1
        else:
            gewählt.append((nummer, mutant))
    return gewählt, begründet


class Vorgaben(NamedTuple):
    """Zeilen je Modul (ohne: alle), Merkzettel (ohne: nichts merken) und gleichwertige Mutanten."""

    zeilen: dict[str, set[int]] | None = None
    ablage: Path | None = None
    gleichwertige: frozenset[Gleichwertig] = frozenset()


def mutationenPrüfen(
    wurzel: Path,
    module: list[str],
    pfade: tuple[str, ...] = testpfade,
    vorgaben: Vorgaben = Vorgaben(),  # noqa: B008
) -> Ergebnis:
    """Baut je Mutant in eine Kopie und lässt nur die Tests laufen, die seine Zeile ausführen."""
    zeilen, ablage, gleichwertige = vorgaben
    überlebende: list[Überlebender] = []
    gesamt = 0
    ohneWirkung = 0
    stand = standKennung(wurzel)
    ergebnisse = dict(gemerkt(ablage, stand))
    with tempfile.TemporaryDirectory() as ordner:
        kopie = Path(ordner)
        kopieAnlegen(wurzel, kopie)
        beginn = time.monotonic()
        messung = messen(kopie, pfade, 3600)
        assert messung.grün, "Die Tests sind ohne Mutant rot; so zeigt keiner eine Lücke"
        wartezeit = max(sekundenMindestens, wartefaktor * (time.monotonic() - beginn))
        for modul in module:
            original = (wurzel / modul).read_text(encoding="utf-8")
            mutanten, begründet = mutantenWählen(modul, original, zeilen, gleichwertige)
            ohneWirkung += begründet
            for nummer, mutant in mutanten:
                gesamt += 1
                schlüssel = f"{modul}#{nummer}"
                if schlüssel not in ergebnisse:
                    (kopie / modul).write_text(mutant.quelle, encoding="utf-8")
                    ausgewählt = auswahl(messung.karten.get(modul), mutant.zeile)
                    ergebnisse[schlüssel] = überlebt(kopie, ausgewählt, pfade, wartezeit)
                    (kopie / modul).write_text(original, encoding="utf-8")
                if ergebnisse[schlüssel]:
                    überlebende.append(Überlebender(modul, mutant.zeile, mutant.beschreibung))
    merken(ablage, stand, ergebnisse)
    return Ergebnis(gesamt, überlebende, ohneWirkung)


def bericht(ergebnis: Ergebnis) -> str:
    lücken = [f"{lücke.datei}:{lücke.zeile} {lücke.beschreibung}" for lücke in ergebnis.überlebende]
    kopf = (
        f"{ergebnis.gesamt} Mutanten, {ergebnis.prozentGefangen} % gefangen, Schwelle {schwelle} %"
        f", {ergebnis.gleichwertige} gleichwertig begründet, nicht gezählt"
    )
    return "\n".join([*lücken, kopf])


def ziel(wurzel: Path, argument: str) -> tuple[str, set[int]]:
    """Ein Modul, ganz oder nur `modul:von-bis` (eine Zeile: `modul:zeile`)."""
    modul, _, bereich = argument.partition(":")
    if not bereich:
        anzahl = len((wurzel / modul).read_text(encoding="utf-8").splitlines())
        return modul, set(range(1, anzahl + 1))
    erste, _, letzte = bereich.partition("-")
    return modul, set(range(int(erste), int(letzte or erste) + 1))


def alleModule(wurzel: Path) -> dict[str, set[int]]:
    """Jede Zeile jedes Moduls des Produkts, auch `web/`: der volle Lauf der Retro."""
    ergebnis = {}
    for datei in sorted((wurzel / produktOrdner).rglob("*.py")):
        name = datei.relative_to(wurzel).as_posix()
        ergebnis[name] = ziel(wurzel, name)[1]
    return ergebnis


def zeilenWählen(wurzel: Path, argumente: list[str]) -> dict[str, set[int]]:
    """Voll: alles; Module genannt: diese Zeilen; sonst die seit der Planfreigabe geänderten."""
    if vollerLauf in argumente:
        return alleModule(wurzel)
    if argumente:
        return dict(ziel(wurzel, argument) for argument in argumente)
    return geänderteZeilen(wurzel, domaeneOrdner)


def main(argumente: list[str]) -> int:
    wurzel = projektordner()
    zeilen = zeilenWählen(wurzel, argumente)
    ablage = wurzel / ".git" / "arbiter" / "mutation.json"
    gleichwertige = frozenset(gleichwertigeLesen())
    vorgaben = Vorgaben(zeilen, ablage, gleichwertige)
    ergebnis = mutationenPrüfen(wurzel, list(zeilen), testpfade, vorgaben)
    print(bericht(ergebnis))
    return 0 if schwelleErreicht(ergebnis) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
