import ast
from pathlib import Path
from typing import NamedTuple

from formregeln.erlaubteImporte import kastenDesModuls, kastenNamen, pfeilErlaubt
from formregeln.importvertrag import importierteModule, paketDerDatei

produktOrdner = "technik/arbiter"
seiteOrdner = "technik/frontend"
seiteEndungen = (".html", ".css", ".js")
architekturOrdner = "technik/architektur"
übersichtDatei = "technik/architektur.md"
vertragOrdner = "technik/architektur/vertrag"
startDatei = "__main__.py"
architekturDateien = {"seite": "frontend"}


class Kasten(NamedTuple):
    name: str
    codeZeichen: int
    architekturZeichen: int | None


class Pfeil(NamedTuple):
    von: str
    nach: str
    anzahl: int
    erlaubt: bool


def zeichen(dateien: list[Path]) -> int:
    return sum(len(datei.read_text(encoding="utf-8")) for datei in dateien if datei.is_file())


def codeDateien(wurzel: Path, kasten: str) -> list[Path]:
    if kasten == "seite":
        ordner = wurzel / seiteOrdner
        return [datei for datei in ordner.rglob("*") if datei.suffix in seiteEndungen]
    if kasten == "start":
        return [datei for datei in [wurzel / produktOrdner / startDatei] if datei.is_file()]
    return [
        datei
        for datei in (wurzel / produktOrdner / kasten).rglob("*.py")
        if "__pycache__" not in datei.parts
    ]


def architekturZeichen(wurzel: Path, kasten: str) -> int | None:
    if kasten == "start":
        return None
    datei = wurzel / architekturOrdner / f"{architekturDateien.get(kasten, kasten)}.md"
    return zeichen([datei]) if datei.is_file() else None


def kästenMessen(wurzel: Path) -> list[Kasten]:
    return [
        Kasten(name, zeichen(codeDateien(wurzel, name)), architekturZeichen(wurzel, name))
        for name in kastenNamen
    ]


def kastenDerDatei(datei: Path, wurzel: Path) -> str | None:
    teile = datei.relative_to(wurzel / produktOrdner).parts
    if datei.name == startDatei and len(teile) == 1:
        return "start"
    return teile[0] if len(teile) > 1 else None


def importzeilen(wurzel: Path) -> dict[tuple[str, str], int]:
    anzahl: dict[tuple[str, str], int] = {}
    for datei in sorted((wurzel / produktOrdner).rglob("*.py")):
        von = kastenDerDatei(datei, wurzel)
        if von is None or "__pycache__" in datei.parts:
            continue
        baum = ast.parse(datei.read_text(encoding="utf-8"))
        for modul, _ in importierteModule(baum, paketDerDatei(datei, wurzel)):
            nach = kastenDesModuls(modul)
            if nach is not None and nach != von:
                anzahl[(von, nach)] = anzahl.get((von, nach), 0) + 1
    return anzahl


def pfeileMessen(wurzel: Path, kästen: list[Kasten]) -> list[Pfeil]:
    mitCode = frozenset(kasten.name for kasten in kästen if kasten.codeZeichen)
    return [
        Pfeil(von, nach, anzahl, pfeilErlaubt(von, nach, mitCode))
        for (von, nach), anzahl in sorted(importzeilen(wurzel).items())
    ]


def übersichtUndVertrag(wurzel: Path) -> tuple[int, int]:
    vertrag = [datei for datei in (wurzel / vertragOrdner).rglob("*") if datei.is_file()]
    return zeichen([wurzel / übersichtDatei]), zeichen(vertrag)
