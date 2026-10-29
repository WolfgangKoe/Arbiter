import ast
import posixpath
import re
from pathlib import Path
from typing import NamedTuple

from formregeln.erlaubteImporte import pfeilErlaubt
from formregeln.importvertrag import aufgelöst, paketDerDatei
from rollenregeln.architekturMessung import (
    Kasten,
    Knoten,
    leerePaketDatei,
    paketDatei,
    produktOrdner,
    seiteOrdner,
    startDatei,
)

paketName = "arbiter"
jsImport = re.compile(
    r"""\b(?:import|export)\b[^'";]*?\bfrom\s*['"]([^'"]+)['"]|\bimport\s*['"]([^'"]+)['"]"""
)
htmlVerweise = (
    re.compile(r"""<script\b[^>]*\bsrc=["']([^"']+)["']"""),
    re.compile(r"""<link\b[^>]*\bhref=["']([^"']+)["']"""),
)


class Kante(NamedTuple):
    von: str
    nach: str
    anzahl: int
    erlaubt: bool


def kastenDesPfads(pfad: str) -> str | None:
    if pfad.startswith(f"{seiteOrdner}/"):
        return "seite"
    teile = pfad.removeprefix(f"{produktOrdner}/").split("/")
    if not pfad.startswith(f"{produktOrdner}/") or teile[0] == paketDatei:
        return None
    if len(teile) == 1:
        return "start" if teile[0] == startDatei else teile[0].removesuffix(".py")
    return teile[0]


def pythonZiel(modul: str, wurzel: Path) -> str | None:
    teile = modul.split(".")
    if teile[0] != paketName or len(teile) == 1:
        return None
    pfad = "technik/" + "/".join(teile)
    datei = wurzel / f"{pfad}.py"
    if datei.is_file():
        return f"{pfad}.py"
    if (wurzel / pfad).is_dir():
        init = wurzel / pfad / paketDatei
        return f"{pfad}/{paketDatei}" if init.is_file() and not leerePaketDatei(init) else pfad
    return None


def pythonZiele(knoten: ast.stmt, paket: list[str], wurzel: Path) -> set[str]:
    if isinstance(knoten, ast.Import):
        einzeln = [pythonZiel(alias.name, wurzel) for alias in knoten.names]
        return {ziel for ziel in einzeln if ziel}
    if not isinstance(knoten, ast.ImportFrom):
        return set()
    modul = aufgelöst(knoten, paket) or "?"
    einzeln = [pythonZiel(f"{modul}.{alias.name}", wurzel) for alias in knoten.names]
    ziele = {ziel for ziel in einzeln if ziel}
    gesamt = pythonZiel(modul, wurzel)
    if gesamt and None in einzeln:
        ziele.add(gesamt)
    return ziele


def pythonVerweise(datei: Path, wurzel: Path) -> list[str]:
    baum = ast.parse(datei.read_text(encoding="utf-8"))
    paket = paketDerDatei(datei, wurzel)
    verweise: list[str] = []
    for knoten in ast.walk(baum):
        verweise += sorted(pythonZiele(knoten, paket, wurzel))
    return verweise


def seiteVerweise(datei: Path, wurzel: Path) -> list[str]:
    text = datei.read_text(encoding="utf-8")
    if datei.suffix == ".js":
        angaben = [erste or zweite for erste, zweite in jsImport.findall(text)]
    elif datei.suffix == ".html":
        angaben = [angabe for muster in htmlVerweise for angabe in muster.findall(text)]
    else:
        return []
    ziele = []
    for angabe in angaben:
        if angabe.startswith(("http", "/")):
            continue
        ordner = datei.parent.relative_to(wurzel).as_posix()
        ziel = posixpath.normpath(posixpath.join(ordner, angabe))
        if (wurzel / ziel).is_file():
            ziele.append(ziel)
    return ziele


def dateien(knoten: Knoten) -> list[Knoten]:
    if not knoten.istOrdner:
        return [knoten]
    return [datei for kind in knoten.kinder for datei in dateien(kind)]


def verweiseDerDatei(pfad: str, wurzel: Path) -> list[str]:
    datei = wurzel / pfad
    if datei.suffix == ".py":
        return pythonVerweise(datei, wurzel)
    return seiteVerweise(datei, wurzel)


def kastenDerKante(pfad: str) -> str:
    return kastenDesPfads(pfad) or ""


def verweiseDerKästen(wurzel: Path, kästen: list[Kasten]) -> list[tuple[str, str]]:
    alle = [datei for kasten in kästen if kasten.wurzel for datei in dateien(kasten.wurzel)]
    return [
        (datei.pfad, ziel)
        for datei in alle
        for ziel in verweiseDerDatei(datei.pfad, wurzel)
        if kastenDesPfads(ziel) is not None and ziel != datei.pfad
    ]


def kantenMessen(wurzel: Path, kästen: list[Kasten]) -> list[Kante]:
    mitCode = frozenset(kasten.name for kasten in kästen if kasten.codeZeichen)
    anzahl: dict[tuple[str, str], int] = {}
    for von, nach in verweiseDerKästen(wurzel, kästen):
        anzahl[(von, nach)] = anzahl.get((von, nach), 0) + 1
    return [
        Kante(von, nach, zahl, pfeilErlaubt(kastenDerKante(von), kastenDerKante(nach), mitCode))
        for (von, nach), zahl in sorted(anzahl.items())
    ]


def kastenPfeile(kanten: list[Kante]) -> list[Kante]:
    summe: dict[tuple[str, str], list] = {}
    for kante in kanten:
        schlüssel = (kastenDerKante(kante.von), kastenDerKante(kante.nach))
        if schlüssel[0] == schlüssel[1]:
            continue
        eintrag = summe.setdefault(schlüssel, [0, True])
        eintrag[0] += kante.anzahl
        eintrag[1] = eintrag[1] and kante.erlaubt
    return [
        Kante(von, nach, zahl, erlaubt) for (von, nach), (zahl, erlaubt) in sorted(summe.items())
    ]
