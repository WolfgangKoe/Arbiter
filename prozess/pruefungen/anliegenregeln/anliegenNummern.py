"""Vergibt Nummern der Anliegen: vergebene, nächste freie, doppelte."""

import re
from pathlib import Path

from gemeinsam.gitAufruf import gitAusgabe
from gemeinsam.pfade import anliegenOrdner
from lesen.anliegenKopf import anliegenDateien


def nummerAusDateiname(name: str) -> int | None:
    treffer = re.match(r"(\d+)-", name)
    return int(treffer[1]) if treffer else None


def vergebeneNummern(wurzel: Path) -> set[int]:
    """Nummern der vorhandenen und der in git je angelegten Anliegen; nie neu vergeben."""
    namen = [datei.name for datei in anliegenDateien(wurzel)]
    verlauf = gitAusgabe(wurzel, "log", "--all", "--name-only", "--format=", "--", anliegenOrdner)
    namen += [Path(zeile).name for zeile in verlauf.splitlines()]
    nummern = (nummerAusDateiname(name) for name in namen)
    return {nummer for nummer in nummern if nummer is not None}


def nächsteFreieNummer(wurzel: Path) -> int:
    return max(vergebeneNummern(wurzel), default=0) + 1


def doppelteNummern(wurzel: Path) -> dict[int, list[str]]:
    """Nummern, die mehr als eine Datei in `handoff/anliegen/` trägt."""
    dateien: dict[int, list[str]] = {}
    for datei in anliegenDateien(wurzel):
        nummer = nummerAusDateiname(datei.name)
        if nummer is not None:
            dateien.setdefault(nummer, []).append(datei.name)
    return {nummer: namen for nummer, namen in dateien.items() if len(namen) > 1}
