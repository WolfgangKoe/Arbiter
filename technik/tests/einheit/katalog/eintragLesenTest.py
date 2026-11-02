import pytest

from arbiter.katalog.eintragLesen import abbildungLesen, genauDieseSchlüsselLesen


@pytest.mark.parametrize(
    "eintrag",
    [{"bewegungsweite": 5}, {"bewegungsweite": 5, "durchmesser": 32, "oc": 2}, [5, 32], None],
    ids=["schlüsselFehlt", "schlüsselUnbekannt", "keineAbbildung", "leer"],
)
def testEinEintragMitAnderenSchlüsselnAlsDieTabelleIstEinFehler(eintrag):
    tabelle = {"bewegungsweite": int, "durchmesser": int}

    with pytest.raises(ValueError):
        genauDieseSchlüsselLesen(eintrag, tabelle, "Eine Modellart")


def testEineAbbildungLiestJedenWert():
    assert abbildungLesen({"Boyz": 1, "Grots": 2}, str, "Eine Einheit") == {
        "Boyz": "1",
        "Grots": "2",
    }


@pytest.mark.parametrize("werte", [{}, None, [1]], ids=["leer", "nichts", "liste"])
def testEineLeereAbbildungOderEineAndereFormIstEinFehler(werte):
    with pytest.raises(ValueError):
        abbildungLesen(werte, str, "Eine Einheit")
