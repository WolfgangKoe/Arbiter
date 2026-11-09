import ast
import subprocess
import sys
from pathlib import Path

from gemeinsam.pfade import itemsOrdner
from kriterienregeln.kriterium import Kriterium, testKriterium
from kriterienregeln.rueckverfolgung import umfasst
from standregeln.fortschritt import kriterienZuordnungen
from standregeln.standVorDerUmsetzung import mitKopie, standJeTest

kritikAnDenTests = "Kritik an den Tests zu Item "
bestanden = "PASSED "
umfangMarke = "Umfang:"


def itemDesSchritts(schritt: str) -> str | None:
    if not schritt.startswith(kritikAnDenTests):
        return None
    return schritt.removeprefix(kritikAnDenTests) + ".md"


def testnamenZu(testdatei: Path, gefordert: list[Kriterium]) -> list[str]:
    baum = ast.parse(testdatei.read_text(encoding="utf-8"))
    namen = [knoten.name for knoten in baum.body if isinstance(knoten, ast.FunctionDef)]
    return [
        name
        for name in namen
        if (treffer := testKriterium.match(name)) and Kriterium.aus(treffer) in gefordert
    ]


def umfangDes(itemText: str) -> str:
    absatz: list[str] = []
    for zeile in itemText.splitlines():
        if absatz and not zeile.strip():
            break
        if absatz or zeile.startswith(umfangMarke):
            absatz.append(zeile)
    return "\n".join(absatz)


def testkennungenDesItems(wurzel: Path, itemName: str) -> list[str]:
    text = umfangDes((wurzel / itemsOrdner / itemName).read_text(encoding="utf-8"))
    kennungen = []
    for zuordnung in kriterienZuordnungen(wurzel, text):
        if not zuordnung.testdatei.is_file():
            continue
        gefordert = [kriterium for kriterium in zuordnung.verlangt if umfasst([text], kriterium)]
        pfad = zuordnung.testdatei.relative_to(wurzel).as_posix()
        kennungen += [f"{pfad}::{name}" for name in testnamenZu(zuordnung.testdatei, gefordert)]
    return kennungen


def grüneAmStand(wurzel: Path, stand: str, kennungen: list[str]) -> list[str]:
    befehl = [sys.executable, "-m", "pytest", "-q", "--tb=no", "-p", "no:cacheprovider", "-rp"]
    ordner, kopie = mitKopie(wurzel, stand)
    with ordner:
        lauf = subprocess.run(
            [*befehl, *kennungen], cwd=kopie, capture_output=True, text=True, check=False
        )
    return [
        zeile.removeprefix(bestanden).split("::")[-1]
        for zeile in lauf.stdout.splitlines()
        if zeile.startswith(bestanden)
    ]


def grüneTests(wurzel: Path, itemName: str) -> list[str]:
    kennungen = testkennungenDesItems(wurzel, itemName)
    gruppen = standJeTest(wurzel, itemName, kennungen)
    return [
        name for stand, gruppe in gruppen.items() for name in grüneAmStand(wurzel, stand, gruppe)
    ]
