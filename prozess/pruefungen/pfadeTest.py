import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

import pfade
from kommentare import docstringKnoten

ordner = Path(__file__).resolve().parent


def pfadeAus(modul: object) -> list[str]:
    return [
        wert
        for name, wert in vars(modul).items()
        if not name.startswith("_") and isinstance(wert, str)
    ]


alleOrdner = pfadeAus(pfade)
prüfTests = {
    datei.name
    for datei in ordner.glob("*Test.py")
    if not datei.with_name(datei.name.removesuffix("Test.py") + ".py").exists()
}


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
    docstrings = {docstring.value for _, docstring, _ in docstringKnoten(baum)}
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


def istTestOderPfade(dateiname: str) -> bool:
    return dateiname.endswith("Test.py") or dateiname == "pfade.py"


def testKeinOrdnerLiteralStehtAußerhalbVonPfade():
    funde = {
        datei.name: treffer
        for datei in ordner.glob("*.py")
        if datei.name in prüfTests or not istTestOderPfade(datei.name)
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


def testDieListeDerPfadeIstNichtLeer():
    assert alleOrdner


def testNurÖffentlicheZeichenkettenDesModulsZählen():
    modul = SimpleNamespace(planDatei="handoff/plan.md", __doc__="Text", _x="y", zahl=3)
    assert pfadeAus(modul) == ["handoff/plan.md"]


def testNurPfadeUndTestsSindAusgenommen():
    assert istTestOderPfade("pfade.py")
    assert istTestOderPfade("pfadeTest.py")
    assert not istTestOderPfade("schreibpfade.py")


def testEinPrüfTestOhneEigenesModulIstEingeschlossen():
    assert {"cspellTest.py", "hoechstmassTest.py"} <= prüfTests
    assert "pfadeTest.py" not in prüfTests
