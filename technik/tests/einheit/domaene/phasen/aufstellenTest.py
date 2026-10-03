import pytest

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone
from arbiter.domaene.spielobjekte import Armee, Einheit, Modell, Spieler


def spielerMitEinerEinheit() -> Spieler:
    return Spieler(armee=Armee(einheiten=(Einheit(modelle=(Modell(),)),)))


def testDerselbeSpielerAlsBeideSpielerIstEineVorbedingungsverletzung():
    spieler = spielerMitEinerEinheit()

    with pytest.raises(ValueError):
        Aufstellung(spieler, spieler)


def testEinFremderSpielerAlsGewinnerIstEineVorbedingungsverletzung():
    aufstellung = Aufstellung(spielerMitEinerEinheit(), spielerMitEinerEinheit())

    with pytest.raises(ValueError):
        aufstellung.gewinnerWählen(spielerMitEinerEinheit())

    assert aufstellung.gewinner is None


def testWerKeineEinheitAufzustellenHatWirdNachDerZonenwahlÜbersprungen():
    gewinner = spielerMitEinerEinheit()
    ohneEinheit = Spieler(armee=Armee())
    aufstellung = Aufstellung(gewinner, ohneEinheit)

    aufstellung.gewinnerWählen(gewinner)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.nord)

    assert aufstellung.anDerReihe is gewinner
