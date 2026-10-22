"""Prüft den Spiegel der Anforderungen: Inhalt der Akzeptanztests, Module der Domäne."""

import ast
import sys
from pathlib import Path

from formregeln.glossar import domaeneOrdner
from gemeinsam.pfade import akzeptanzOrdner, anforderungsOrdner, projektordner
from kriterienregeln.kriterium import (
    Kriterium,
    anforderungenMitZeile,
    anforderungKennung,
    kriterienMitZeile,
    testsMitZeile,
    zeilen,
)

überschriftPräfix = "### "
modulOhneAnforderung = {"messen.py", "sperre.py"}


def anforderungZu(testdatei: Path, wurzel: Path) -> Path:
    relativ = testdatei.relative_to(wurzel / akzeptanzOrdner)
    name = relativ.name.removesuffix("Test.py")
    return wurzel / anforderungsOrdner / relativ.parent / f"{name}.md"


def überschriftVon(anforderung: Path) -> str | None:
    überschriften = (zeile for zeile in zeilen(anforderung) if zeile.startswith(überschriftPräfix))
    return next(überschriften, None)


def docstringVerstoß(testdatei: Path, überschrift: str) -> str | None:
    """T1 (1): Der Docstring der Testdatei ist die Überschrift ihrer Anforderung mit Punkt."""
    erwartet = f"{überschrift.removeprefix(überschriftPräfix)}."
    vorhanden = ast.get_docstring(ast.parse(testdatei.read_text(encoding="utf-8")))
    if vorhanden == erwartet:
        return None
    return f"Docstring `{vorhanden}` statt `{erwartet}`"


def kennungVerstöße(testdatei: Path, anforderung: Path) -> list[str]:
    """T1 (2): Jede Testfunktion trägt Kürzel und Nummer der Anforderung ihrer Datei."""
    eigene = anforderungenMitZeile(anforderung)
    if not eigene:
        return []
    (erwartet, _), *_ = eigene
    return [
        f"Zeile {zeile}: {kriterium.kennung} gehört nicht zu {anforderungKennung(erwartet)}"
        for kriterium, zeile, _ in testsMitZeile(testdatei)
        if kriterium.anforderung != erwartet
    ]


def folgeVerstöße(testdatei: Path, anforderung: Path) -> list[str]:
    """T1 (3): Die Kennungen der Tests stehen in der Folge der Kriterien, gleiche beisammen."""
    alle = kriterienMitZeile(anforderung)
    folge = {kriterium: platz for platz, (kriterium, _) in enumerate(alle)}
    tests = sorted(
        (zeile, kriterium) for kriterium, zeile, _ in testsMitZeile(testdatei) if kriterium in folge
    )
    verstöße = []
    vorher: Kriterium | None = None
    for zeile, kriterium in tests:
        if kriterium == vorher:
            continue
        if vorher is not None and folge[kriterium] <= folge[vorher]:
            verstöße.append(f"Zeile {zeile}: {kriterium.kennung} nach {vorher.kennung}")
        vorher = kriterium
    return verstöße


def akzeptanztestVerstöße(testdatei: Path, wurzel: Path) -> list[str]:
    anforderung = anforderungZu(testdatei, wurzel)
    überschrift = überschriftVon(anforderung) if anforderung.is_file() else None
    if überschrift is None:
        return []
    docstring = docstringVerstoß(testdatei, überschrift)
    return [
        *([docstring] if docstring else []),
        *kennungVerstöße(testdatei, anforderung),
        *folgeVerstöße(testdatei, anforderung),
    ]


def hatSpiegel(modul: Path, domäne: Path, anforderungen: Path) -> bool:
    relativ = modul.relative_to(domäne)
    if modul.name == "__init__.py":
        return (anforderungen / relativ.parent).is_dir()
    ohneEndung = relativ.with_suffix("")
    return (anforderungen / ohneEndung).is_dir() or (anforderungen / f"{ohneEndung}.md").is_file()


def modulVerstöße(wurzel: Path) -> list[str]:
    """Grundschnitt: Jedes Modul der Domäne außer den Werkzeugen hat einen Spiegel."""
    domäne = wurzel / domaeneOrdner
    anforderungen = wurzel / anforderungsOrdner
    return [
        f"{modul.relative_to(wurzel).as_posix()}: kein Spiegel in {anforderungsOrdner}"
        for modul in sorted(domäne.rglob("*.py"))
        if "__pycache__" not in modul.parts
        and modul != domäne / "__init__.py"
        and modul.name not in modulOhneAnforderung
        and not hatSpiegel(modul, domäne, anforderungen)
    ]


def verstöße(wurzel: Path) -> list[str]:
    meldungen = []
    for testdatei in sorted((wurzel / akzeptanzOrdner).rglob("*Test.py")):
        relativ = testdatei.relative_to(wurzel).as_posix()
        meldungen += [f"{relativ}: {grund}" for grund in akzeptanztestVerstöße(testdatei, wurzel)]
    return meldungen + modulVerstöße(wurzel)


if __name__ == "__main__":
    gefunden = verstöße(projektordner())
    print("\n".join(gefunden))
    sys.exit(1 if gefunden else 0)
