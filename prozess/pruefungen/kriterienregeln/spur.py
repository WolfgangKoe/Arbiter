"""Spur eines Kriteriums: seine Fundstellen in den Anforderungen und in den Akzeptanztests."""

import re
from pathlib import Path

from gemeinsam.pfade import akzeptanzOrdner, anforderungsOrdner
from kriterienregeln.kriterium import (
    Fundstelle,
    Kriteriumsnummer,
    kriterienMitZeile,
    kriteriumKennung,
    pfadVon,
    testKriterium,
    testsMitZeile,
)

stellenAngabe = re.compile(r"^(.+):(\d+)$")


def kriteriumsstellen(wurzel: Path) -> dict[Kriteriumsnummer, list[Fundstelle]]:
    stellen: dict[Kriteriumsnummer, list[Fundstelle]] = {}
    for datei in sorted((wurzel / anforderungsOrdner).rglob("*.md")):
        for kriterium, zeile in kriterienMitZeile(datei):
            stellen.setdefault(kriterium, []).append(
                Fundstelle("Kriterium", pfadVon(wurzel, datei), zeile)
            )
    return stellen


def teststellen(wurzel: Path) -> dict[Kriteriumsnummer, list[Fundstelle]]:
    stellen: dict[Kriteriumsnummer, list[Fundstelle]] = {}
    for datei in sorted((wurzel / akzeptanzOrdner).rglob("*Test.py")):
        for kriterium, zeile, _ in testsMitZeile(datei):
            stelle = Fundstelle("Test", pfadVon(wurzel, datei), zeile)
            stellen.setdefault(kriterium, []).append(stelle)
    return stellen


def kriteriumZuStelle(wurzel: Path, pfad: str, zeile: int) -> Kriteriumsnummer | None:
    """Das Kriterium, das in der Zeile der Datei steht oder dessen Testfunktion sie enthält."""
    datei = wurzel / pfad
    if not datei.is_file():
        return None
    if datei.suffix == ".md":
        stellen = kriterienMitZeile(datei)
        return next((kriterium for kriterium, nummer in stellen if nummer == zeile), None)
    return next(
        (kriterium for kriterium, anfang, ende in testsMitZeile(datei) if anfang <= zeile <= ende),
        None,
    )


def kriteriumZuEingabe(wurzel: Path, eingabe: str) -> Kriteriumsnummer | None:
    treffer = kriteriumKennung.match(eingabe.upper())
    if treffer:
        return treffer[1], int(treffer[2]), int(treffer[3])
    treffer = testKriterium.match(eingabe)
    if treffer:
        return treffer[1].upper(), int(treffer[2]), int(treffer[3])
    stelle = stellenAngabe.match(eingabe)
    return kriteriumZuStelle(wurzel, stelle[1], int(stelle[2])) if stelle else None


def spur(wurzel: Path, eingabe: str) -> list[Fundstelle] | None:
    """Kriterium und seine Tests; `None`, wenn die Eingabe kein bekanntes Kriterium nennt."""
    kriterium = kriteriumZuEingabe(wurzel, eingabe)
    stellen = kriteriumsstellen(wurzel).get(kriterium, []) if kriterium else []
    if not stellen:
        return None
    return stellen + teststellen(wurzel).get(kriterium, [])


def spurAlsText(stellen: list[Fundstelle]) -> str:
    return "\n".join(f"{stelle.pfad}:{stelle.zeile}" for stelle in stellen)
