import re
import sys
from pathlib import Path
from typing import NamedTuple

from gemeinsam.pfade import projektordner
from standregeln.beseitigt import anliegenText, hindernisMuster
from standregeln.fortschritt import (
    Zeile,
    abschnittBauen,
    abschnittEinsetzen,
    bisherigeZeilen,
    fortschrittSchreiben,
    gleicheRolle,
    zielUndZeilen,
)
from standregeln.hindernis import hindernisMelden, nächsteNummer
from standregeln.phasenfolge import lage
from standregeln.testsRot import grüneTests, itemDesSchritts

aufrufteileRolleUndSchritt = 2
testnamenMuster = re.compile(r"\btest\w+(?:\[[^\]\s]*\])?")


class Grün(NamedTuple):
    tests: list[str]
    anliegen: int | None


def eigeneZeilen(wurzel: Path, rolle: str) -> tuple[Path, list[Zeile]] | None:
    ziel = zielUndZeilen(wurzel, lage(wurzel))
    if ziel is None:
        return None
    datei, zeilen = ziel
    return datei, [zeile for zeile in zeilen if gleicheRolle(zeile, rolle) and zeile.fakt is None]


def offeneZeilen(wurzel: Path, rolle: str) -> list[str]:
    eigene = eigeneZeilen(wurzel, rolle)
    if eigene is None:
        return []
    datei, zeilen = eigene
    bisher = bisherigeZeilen(datei.read_text(encoding="utf-8"))
    return [zeile.schritt for zeile in zeilen if not bisher.get(zeile.schlüssel, (False,))[0]]


def passt(zeile: Zeile, rolle: str, schritt: str) -> bool:
    return (
        gleicheRolle(zeile, rolle)
        and zeile.fakt is None
        and schritt.casefold() in zeile.schritt.casefold()
    )


def bereitsAbgehakt(wurzel: Path, rolle: str, schritt: str) -> list[str]:
    ziel = zielUndZeilen(wurzel, lage(wurzel))
    if ziel is None:
        return []
    datei, zeilen = ziel
    bisher = bisherigeZeilen(datei.read_text(encoding="utf-8"))
    return [
        zeile.schritt
        for zeile in zeilen
        if passt(zeile, rolle, schritt) and bisher.get(zeile.schlüssel, (False,))[0]
    ]


def genannteTests(zeilen: list[str]) -> set[str]:
    return {name for zeile in zeilen for name in testnamenMuster.findall(zeile)}


def zuTestsGemeldet(
    wurzel: Path, hindernisse: list[re.Match], grün: list[str]
) -> tuple[list[str], int | None]:
    beseitigte = [anliegenText(wurzel, treffer[2]) for treffer in hindernisse if treffer[1] == "x"]
    übrige = [name for name in grün if name not in genannteTests(beseitigte)]
    for treffer in hindernisse:
        offen = übrige and treffer[1] == " "
        if offen and set(übrige) <= genannteTests([anliegenText(wurzel, treffer[2])]):
            return übrige, int(treffer[2])
    return übrige, None


def hindernisseDesItems(zeilen: list[Zeile], bisher: dict, schritt: str) -> list[re.Match]:
    gesammelt = []
    for zeile in zeilen:
        if zeile.fakt is None and zeile.schritt == schritt:
            gesammelt += bisher.get(zeile.schlüssel, (False, []))[1]
    return [treffer for eintrag in gesammelt if (treffer := hindernisMuster.match(eintrag))]


def grünVorDemCode(wurzel: Path, rolle: str, schritt: str) -> Grün:
    fortschrittSchreiben(wurzel)
    ziel = zielUndZeilen(wurzel, lage(wurzel))
    if ziel is None:
        return Grün([], None)
    datei, zeilen = ziel
    bisher = bisherigeZeilen(datei.read_text(encoding="utf-8"))
    for zeile in zeilen:
        itemName = itemDesSchritts(zeile.schritt)
        if not itemName or not passt(zeile, rolle, schritt):
            continue
        grün = grüneTests(wurzel, itemName)
        gemeldet = hindernisseDesItems(zeilen, bisher, zeile.schritt)
        übrige, bestehendes = zuTestsGemeldet(wurzel, gemeldet, grün)
        if übrige and bestehendes is None:
            nummer = nächsteNummer(wurzel)
            text = (
                "Diese Tests sind grün, bevor der Code besteht: " + ", ".join(übrige) + ". "
                "Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt."
            )
            freie = range(nummer, nummer + 1)
            hindernisMelden(wurzel, rolle, zeile.schritt, "Testautor", text, freie)
            return Grün(übrige, nummer)
        if übrige:
            return Grün(übrige, bestehendes)
    return Grün([], None)


def abhaken(wurzel: Path, rolle: str, schritt: str) -> list[str]:
    fortschrittSchreiben(wurzel)
    ziel = zielUndZeilen(wurzel, lage(wurzel))
    if ziel is None:
        return []
    datei, zeilen = ziel
    text = datei.read_text(encoding="utf-8")
    bisher = bisherigeZeilen(text)
    treffer = [
        zeile
        for zeile in zeilen
        if passt(zeile, rolle, schritt) and not bisher.get(zeile.schlüssel, (False,))[0]
    ]
    for zeile in treffer:
        bisher[zeile.schlüssel] = (True, bisher.get(zeile.schlüssel, (True, []))[1])
    datei.write_text(abschnittEinsetzen(text, abschnittBauen(zeilen, bisher)), encoding="utf-8")
    return [zeile.schritt for zeile in treffer]


def hauptprogramm(argumente: list[str]) -> int:
    if len(argumente) != aufrufteileRolleUndSchritt:
        print(
            "Aufruf: python3 prozess/pruefungen/gemeinsam/lauf.py standregeln.abhaken"
            " <Rolle> <Schritt>",
            file=sys.stderr,
        )
        return 1
    rolle, schritt = argumente
    wurzel = projektordner()
    grün = grünVorDemCode(wurzel, rolle, schritt)
    if grün.tests:
        print(
            "Nicht abgehakt: Diese Tests sind schon grün, ein Hindernis an den Testautor "
            f"besteht (Anliegen {grün.anliegen}): " + ", ".join(grün.tests),
            file=sys.stderr,
        )
        return 1
    gehakt = abhaken(wurzel, rolle, schritt)
    schon = [] if gehakt else bereitsAbgehakt(wurzel, rolle, schritt)
    if schon:
        print("Schon abgehakt, nichts geändert: " + "; ".join(schon))
        return 0
    if not gehakt:
        offen = "; ".join(offeneZeilen(wurzel, rolle)) or "keiner"
        print(f"Kein Schritt von {rolle} passt zu „{schritt}“. Offen: {offen}", file=sys.stderr)
        return 1
    print("Abgehakt: " + "; ".join(gehakt))
    return 0


if __name__ == "__main__":
    sys.exit(hauptprogramm(sys.argv[1:]))
