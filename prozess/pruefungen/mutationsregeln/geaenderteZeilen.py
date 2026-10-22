"""Die Zeilen der Module, die seit der jüngsten `Freigabe Plan` geändert oder neu sind."""

import re
from pathlib import Path

from gemeinsam.gitAufruf import freigaben, gitAusgabe

planFreigabe = "Freigabe Plan "
ohneAnführung = ("-c", "core.quotepath=false")
kopfzeile = re.compile(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@")
neuePräfix = "+++ b/"


def planKennung(wurzel: Path) -> str:
    return next(
        (frei.kennung for frei in freigaben(wurzel) if frei.betreff.startswith(planFreigabe)),
        "HEAD",
    )


def zeilenAusDiff(diff: str) -> dict[str, set[int]]:
    """Je Datei die neuen Zeilen eines Diffs mit `-U0`; eine gelöschte Datei fehlt."""
    zeilen: dict[str, set[int]] = {}
    aktuell: set[int] | None = None
    for zeile in diff.splitlines():
        if zeile.startswith(neuePräfix):
            aktuell = zeilen.setdefault(zeile.removeprefix(neuePräfix), set())
            continue
        if zeile.startswith("+++ "):
            aktuell = None
            continue
        treffer = kopfzeile.match(zeile)
        if treffer and aktuell is not None:
            beginn = int(treffer.group(1))
            anzahl = 1 if treffer.group(2) is None else int(treffer.group(2))
            aktuell.update(range(beginn, beginn + anzahl))
    return zeilen


def geänderteZeilen(wurzel: Path, ordner: str) -> dict[str, set[int]]:
    """Je Python-Datei unter `ordner` die seit der Planfreigabe geänderten oder neuen Zeilen."""
    diff = gitAusgabe(wurzel, *ohneAnführung, "diff", "-U0", planKennung(wurzel), "--", ordner)
    zeilen = zeilenAusDiff(diff)
    neu = gitAusgabe(
        wurzel, *ohneAnführung, "ls-files", "--others", "--exclude-standard", "--", ordner
    ).splitlines()
    for name in neu:
        if (wurzel / name).is_file():
            anzahl = len((wurzel / name).read_text(encoding="utf-8").splitlines())
            zeilen[name] = set(range(1, anzahl + 1))
    return {
        name: nummern
        for name, nummern in sorted(zeilen.items())
        if name.endswith(".py") and (wurzel / name).is_file()
    }
