"""Kriterien und Tests lesen: Anforderungsdateien und Testdateien nach Kennung."""

import ast
import re
from collections import Counter
from pathlib import Path
from typing import NamedTuple

Anforderungsnummer = tuple[str, int]


class Kriterium(NamedTuple):
    kürzel: str
    hauptnummer: int
    unternummer: int

    @property
    def kennung(self) -> str:
        return f"{self.kürzel}-{self.hauptnummer}.{self.unternummer}"

    @property
    def anforderung(self) -> Anforderungsnummer:
        return self.kürzel, self.hauptnummer

    @classmethod
    def aus(cls, treffer: re.Match) -> "Kriterium":
        return cls(treffer[1].upper(), int(treffer[2]), int(treffer[3]))


class Fundstelle(NamedTuple):
    art: str
    pfad: str
    zeile: int


anforderungZeile = re.compile(r"^### ([A-ZÄÖÜ]+)-(\d+)\b")
kriteriumZeile = re.compile(r"^- ([A-ZÄÖÜ]+)-(\d+)\.(\d+)\b")
kriteriumKennung = re.compile(r"^([A-ZÄÖÜ]+)-(\d+)\.(\d+)$")
testKriterium = re.compile(r"^test([A-ZÄÖÜ][a-zäöüß]*)(\d+)_(\d+)")


def anforderungKennung(anforderung: Anforderungsnummer) -> str:
    kürzel, nummer = anforderung
    return f"{kürzel}-{nummer}"


def zeilen(datei: Path) -> list[str]:
    return datei.read_text(encoding="utf-8").splitlines()


def anforderungenMitZeile(anforderungsdatei: Path) -> list[tuple[Anforderungsnummer, int]]:
    return [
        ((treffer[1], int(treffer[2])), nummer)
        for nummer, zeile in enumerate(zeilen(anforderungsdatei), 1)
        if (treffer := anforderungZeile.match(zeile))
    ]


def kriterienMitZeile(anforderungsdatei: Path) -> list[tuple[Kriterium, int]]:
    return [
        (Kriterium.aus(treffer), nummer)
        for nummer, zeile in enumerate(zeilen(anforderungsdatei), 1)
        if (treffer := kriteriumZeile.match(zeile))
    ]


def kriterien(anforderungsdatei: Path) -> set[Kriterium]:
    return {kriterium for kriterium, _ in kriterienMitZeile(anforderungsdatei)}


def testsMitZeile(testdatei: Path) -> list[tuple[Kriterium, int, int]]:
    """Kriterium, erste und letzte Zeile jeder Testfunktion mit Kennung im Namen."""
    gefunden = []
    for knoten in ast.walk(ast.parse(testdatei.read_text(encoding="utf-8"))):
        if isinstance(knoten, ast.FunctionDef | ast.AsyncFunctionDef):
            treffer = testKriterium.match(knoten.name)
            if treffer:
                kriterium = Kriterium.aus(treffer)
                gefunden.append((kriterium, knoten.lineno, knoten.end_lineno or knoten.lineno))
    return gefunden


def getesteKriterien(testdatei: Path) -> set[Kriterium]:
    return {kriterium for kriterium, _, _ in testsMitZeile(testdatei)}


def doppelte(kennungen: list[str]) -> list[str]:
    return sorted(name for name, anzahl in Counter(kennungen).items() if anzahl > 1)


def pfadVon(wurzel: Path, datei: Path) -> str:
    return datei.relative_to(wurzel).as_posix()
