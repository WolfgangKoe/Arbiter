from fractions import Fraction

import pytest

from arbiter.katalog.datenblaetter import datenblätterLesen, modellartLesen


def testDieDatenblätterDerOrksNennenJeModellartDieWerteDerModellart():
    modellart = datenblätterLesen("orks")["Boyz"]["Boss Nob"]

    assert (modellart.bewegungsweite, modellart.durchmesser) == (Fraction(5), 32)


@pytest.mark.parametrize("fraktion", ["elfen", "../orks", ""])
def testEineFraktionOhneOrdnerIstEinFehler(fraktion):
    with pytest.raises(ValueError):
        datenblätterLesen(fraktion)


@pytest.mark.parametrize("wert", ["5 Zoll", 0, -5, 5.5, True], ids=str)
@pytest.mark.parametrize("schlüssel", ["bewegungsweite", "durchmesser"])
def testEinWertKeineGanzeZahlÜberNullIstEinFehler(schlüssel, wert):
    werte = {"bewegungsweite": 5, "durchmesser": 32, schlüssel: wert}

    with pytest.raises(ValueError):
        modellartLesen(werte)
