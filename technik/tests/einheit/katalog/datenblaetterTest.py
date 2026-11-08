from fractions import Fraction

import pytest

from arbiter.katalog.datenblaetter import datenblattLesen, datenblätterLesen, modellartLesen


def testDieDatenblätterDerOrksNennenJeModellartDieWerteDerModellart():
    modellart = datenblätterLesen("orks")["Boyz"].modellarten["Boss Nob"]

    assert (modellart.bewegungsweite, modellart.durchmesser) == (Fraction(5), 32)


@pytest.mark.parametrize("fraktion", ["elfen", "../orks", "./orks", ""])
def testEineFraktionOhneOrdnerIstEinFehler(fraktion):
    with pytest.raises(ValueError):
        datenblätterLesen(fraktion)


@pytest.mark.parametrize("wert", ["5 Zoll", 0, -5, 5.5, True], ids=str)
@pytest.mark.parametrize("schlüssel", ["bewegungsweite", "durchmesser"])
def testEinWertKeineGanzeZahlÜberNullIstEinFehler(schlüssel, wert):
    werte = {"bewegungsweite": 5, "durchmesser": 32, schlüssel: wert}

    with pytest.raises(ValueError):
        modellartLesen(werte)


_modellarten = {"Boy": {"bewegungsweite": 5, "durchmesser": 32}}


def testEinDatenblattOhneFliegenHatKeinFliegen():
    assert datenblattLesen({"modellarten": _modellarten}).fliegen is False


def testEinDatenblattMitFliegenTrueHatFliegen():
    assert datenblattLesen({"modellarten": _modellarten, "fliegen": True}).fliegen is True


@pytest.mark.parametrize("wert", ["true", 1, None], ids=str)
def testEinFliegenKeinWahrheitswertIstEinFehler(wert):
    with pytest.raises(ValueError):
        datenblattLesen({"modellarten": _modellarten, "fliegen": wert})


def testEinDatenblattMitUnbekanntemSchlüsselIstEinFehler():
    with pytest.raises(ValueError):
        datenblattLesen({"modellarten": _modellarten, "oc": 2})
