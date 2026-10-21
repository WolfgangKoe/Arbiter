from mutationsregeln.abdeckungKontext import Karte, auswahl, kartenAus

karte = Karte(
    frozenset({9}),
    {
        2: frozenset({"technik/tests/akzeptanz/aTest.py", "technik/tests/einheit/bTest.py"}),
        4: None,
    },
)


def testEineUnausgeführteZeileBrauchtKeinenTest():
    assert auswahl(karte, 9) == ()


def testEineAusgeführteZeileNenntIhreTestdateienEinheitstestsZuerst():
    assert auswahl(karte, 2) == (
        "technik/tests/einheit/bTest.py",
        "technik/tests/akzeptanz/aTest.py",
    )


def testEineZeileBeimImportLässtAlleTestsLaufen():
    assert auswahl(karte, 4) is None


def testEineUnbekannteZeileOderModulLässtAlleTestsLaufen():
    assert auswahl(karte, 77) is None
    assert auswahl(None, 2) is None


def testDerBerichtVonCoverageWirdZurKarte():
    bericht = {
        "files": {
            "a.py": {
                "missing_lines": [3],
                "contexts": {
                    "1": ["x/aTest.py::testA", "x/bTest.py::testB"],
                    "2": ["", "x/aTest.py::testA"],
                },
            }
        }
    }
    assert kartenAus(bericht) == {
        "a.py": Karte(frozenset({3}), {1: frozenset({"x/aTest.py", "x/bTest.py"}), 2: None})
    }
