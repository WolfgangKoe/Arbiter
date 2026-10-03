import ast
from pathlib import Path

import pytest

from pfade import etappenOrdner, itemsOrdner

ordner = Path(__file__).resolve().parent
doppelteOrdner = (etappenOrdner, itemsOrdner)


def docstringKnoten(baum: ast.AST) -> set[ast.AST]:
    knoten = set()
    for teil in ast.walk(baum):
        if isinstance(teil, ast.Module | ast.FunctionDef | ast.ClassDef):
            erste = teil.body[0] if teil.body else None
            if isinstance(erste, ast.Expr) and isinstance(erste.value, ast.Constant):
                knoten.add(erste.value)
    return knoten


def ordnerLiterale(quelltext: str) -> list[str]:
    baum = ast.parse(quelltext)
    docstrings = docstringKnoten(baum)
    teile = [ordnerName.split("/")[-1] for ordnerName in doppelteOrdner]
    return [
        knoten.value
        for knoten in ast.walk(baum)
        if isinstance(knoten, ast.Constant)
        and isinstance(knoten.value, str)
        and knoten not in docstrings
        and (knoten.value in teile or any(name in knoten.value for name in doppelteOrdner))
    ]


def testKeinOrdnerLiteralStehtAußerhalbVonPfade():
    funde = {
        datei.name: treffer
        for datei in ordner.glob("*.py")
        if not datei.name.endswith("Test.py") and datei.name != "pfade.py"
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
