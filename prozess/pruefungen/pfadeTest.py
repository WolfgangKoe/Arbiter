import ast
from pathlib import Path

import pytest

import pfade
from kommentare import docstringKnoten

ordner = Path(__file__).resolve().parent
alleOrdner = [wert for name, wert in vars(pfade).items() if name.endswith("Ordner")]
prüfTests = {"hoechstmassTest.py", "komplexitaetTest.py", "konfigurationTest.py"}


def pfadSegmente(baum: ast.AST) -> set[ast.AST]:
    """Zeichenketten, die als Teil eines Pfads mit `/` stehen."""
    return {
        seite
        for teil in ast.walk(baum)
        if isinstance(teil, ast.BinOp) and isinstance(teil.op, ast.Div)
        for seite in (teil.left, teil.right)
    }


def ordnerLiterale(quelltext: str) -> list[str]:
    baum = ast.parse(quelltext)
    docstrings = {docstring.value for _, docstring in docstringKnoten(baum)}
    segmente = pfadSegmente(baum)
    letzteTeile = [ordnerName.split("/")[-1] for ordnerName in alleOrdner]
    return [
        knoten.value
        for knoten in ast.walk(baum)
        if isinstance(knoten, ast.Constant)
        and isinstance(knoten.value, str)
        and knoten not in docstrings
        and (
            any(name in knoten.value for name in alleOrdner)
            or (knoten in segmente and knoten.value in letzteTeile)
        )
    ]


def testKeinOrdnerLiteralStehtAußerhalbVonPfade():
    funde = {
        datei.name: treffer
        for datei in ordner.glob("*.py")
        if datei.name in prüfTests or not datei.name.endswith(("Test.py", "pfade.py"))
        if (treffer := ordnerLiterale(datei.read_text(encoding="utf-8")))
    }
    assert funde == {}


@pytest.mark.parametrize(
    "quelltext",
    [
        pytest.param('x = "domaene/etappen"\n', id="Pfad als Literal"),
        pytest.param('x = wurzel / "domaene" / "items"\n', id="Pfad in Segmenten"),
        pytest.param('x = f"Link auf domaene/items/"\n', id="Pfad im f-String"),
    ],
)
def testEinLiteralDesOrdnersWirdGefunden(quelltext):
    assert ordnerLiterale(quelltext)


def testEinDocstringMitDemOrdnerIstErlaubt():
    assert ordnerLiterale('"""Items in `domaene/items/`."""\n') == []


def testEinDocstringEinerAsyncFunktionIstErlaubt():
    assert ordnerLiterale('async def f():\n    """Liest domaene/items/."""\n') == []


def testEinSchlüsselMitDemNamenDesOrdnersIstErlaubt():
    assert ordnerLiterale('x = daten["items"]\n') == []


def testAlleOrdnerAusPfadeWerdenGeprüft():
    assert all(ordnerLiterale(f'x = "{ordnerName}"\n') for ordnerName in alleOrdner)
