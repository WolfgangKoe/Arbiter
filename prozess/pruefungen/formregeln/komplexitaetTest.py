"""Komplexitätsschwelle im Lauf der Prüfungen: complexipy (Verschachtelung)."""

import pytest

from formregeln.werkzeugaufruf import complexipyAufrufen

codeOrdner = ("prozess/pruefungen", "technik")


@pytest.mark.stand
def testDerCodeLiegtUnterDerKomplexitätsschwelle():
    ergebnis = complexipyAufrufen(*codeOrdner)
    assert ergebnis.returncode == 0, ergebnis.stdout
