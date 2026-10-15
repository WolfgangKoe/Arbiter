import ast

from mutationsregeln.mutanten import mutantenVon

# Warum: nicht, Verknüpfung, Vergleich, Zahl, raise, Summe und Rückgabe der Quelle unten
stellenDerQuelle = 7


def beschreibungen(quelle: str) -> list[str]:
    return [mutant.beschreibung for mutant in mutantenVon(quelle)]


def testEinVergleichWirdZumGegenteil():
    assert beschreibungen("def f(a, b):\n    return a < b\n") == [
        "Lt wird LtE",
        "Rückgabe wird None",
    ]


def testJedeStelleErgibtGenauEinenMutantenMitGültigemQuelltext():
    quelle = "def f(a, b):\n    if not a and b == 2:\n        raise ValueError\n    return a + b\n"
    mutanten = mutantenVon(quelle)
    assert len(mutanten) == stellenDerQuelle
    for mutant in mutanten:
        ast.parse(mutant.quelle)
        assert mutant.quelle != ast.unparse(ast.parse(quelle))


def testEinRaiseWirdZuPass():
    mutant = mutantenVon("def f():\n    raise ValueError\n")[0]
    assert (mutant.zeile, mutant.beschreibung) == (2, "raise entfällt")
    assert "pass" in mutant.quelle


def testEineRückgabeOhneWertHatKeinenMutanten():
    assert beschreibungen("def f():\n    return None\n") == []


def testEineTypangabeHatKeinenMutanten():
    assert beschreibungen("x: tuple[int, int]\n") == []


def testEineZahlMitVorgabewertInDerZuweisungWirdMutiert():
    assert beschreibungen("x: int = 3\n") == ["3 wird 4"]
