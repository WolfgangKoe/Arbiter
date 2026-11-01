import ast
import subprocess
import sys
from pathlib import Path

from gemeinsam.pfade import itemsOrdner
from kriterienregeln.kriterium import Kriterium, testKriterium
from kriterienregeln.rueckverfolgung import umfasst
from standregeln.fortschritt import kriterienZuordnungen

kritikAnDenTests = "Kritik an den Tests zu Item "
bestanden = "PASSED "


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


def testkennungenDesItems(wurzel: Path, itemName: str) -> list[str]:
    text = (wurzel / itemsOrdner / itemName).read_text(encoding="utf-8")
    kennungen = []
    for zuordnung in kriterienZuordnungen(wurzel, text):
        if not zuordnung.testdatei.is_file():
            continue
        gefordert = [kriterium for kriterium in zuordnung.verlangt if umfasst([text], kriterium)]
        pfad = zuordnung.testdatei.relative_to(wurzel).as_posix()
        kennungen += [f"{pfad}::{name}" for name in testnamenZu(zuordnung.testdatei, gefordert)]
    return kennungen


def grüneTests(wurzel: Path, itemName: str) -> list[str]:
    kennungen = testkennungenDesItems(wurzel, itemName)
    if not kennungen:
        return []
    befehl = [sys.executable, "-m", "pytest", "-q", "--tb=no", "-p", "no:cacheprovider", "-rp"]
    lauf = subprocess.run(
        [*befehl, *kennungen], cwd=wurzel, capture_output=True, text=True, check=False
    )
    return [
        zeile.removeprefix(bestanden).split("::")[-1]
        for zeile in lauf.stdout.splitlines()
        if zeile.startswith(bestanden)
    ]
