from fractions import Fraction

import pytest

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone, Ausgangslage
from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell, Spieler, Spielfeld


def spielerMitEinerEinheit() -> Spieler:
    modell = Modell(base=Base(durchmesser=32))
    return Spieler(armee=Armee(einheiten=(Einheit(modelle=(modell,)),)))


def aufstellungVon(ersterSpieler: Spieler, zweiterSpieler: Spieler) -> Aufstellung:
    spielfeld = Spielfeld(seitenlängen=(Fraction(44), Fraction(60)))
    return Aufstellung(
        Ausgangslage(
            ersterSpieler,
            zweiterSpieler,
            spielfeld,
            {zone: Fraction(9) for zone in Aufstellungszone},
        )
    )


def testDerselbeSpielerAlsBeideSpielerIstEineVorbedingungsverletzung():
    spieler = spielerMitEinerEinheit()

    with pytest.raises(ValueError):
        aufstellungVon(spieler, spieler)


def testEinFremderSpielerAlsGewinnerIstEineVorbedingungsverletzung():
    aufstellung = aufstellungVon(spielerMitEinerEinheit(), spielerMitEinerEinheit())

    with pytest.raises(ValueError):
        aufstellung.gewinnerWählen(spielerMitEinerEinheit())

    assert aufstellung.gewinner is None


def testDieAufstellungszoneEinesFremdenSpielersIstEineVorbedingungsverletzung():
    aufstellung = aufstellungVon(spielerMitEinerEinheit(), spielerMitEinerEinheit())

    with pytest.raises(ValueError):
        aufstellung.aufstellungszone(spielerMitEinerEinheit())


def testWerKeineEinheitAufzustellenHatWirdNachDerZonenwahlÜbersprungen():
    gewinner = spielerMitEinerEinheit()
    ohneEinheit = Spieler(armee=Armee())
    aufstellung = aufstellungVon(gewinner, ohneEinheit)

    aufstellung.gewinnerWählen(gewinner)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)

    assert aufstellung.anDerReihe is gewinner


def testZweiSpielerMitDerselbenArmeeSindEineVorbedingungsverletzung():
    armee = spielerMitEinerEinheit().armee

    with pytest.raises(ValueError):
        aufstellungVon(Spieler(armee=armee), Spieler(armee=armee))


def testZweiSpielerMitEinerGemeinsamenEinheitSindEineVorbedingungsverletzung():
    gemeinsam = spielerMitEinerEinheit().armee.einheiten
    eigene, *_ = spielerMitEinerEinheit().armee.einheiten

    with pytest.raises(ValueError):
        aufstellungVon(
            Spieler(armee=Armee(einheiten=gemeinsam)),
            Spieler(armee=Armee(einheiten=(*gemeinsam, eigene))),
        )


def testZweiSpielerMitEinemGemeinsamenModellSindEineVorbedingungsverletzung():
    einheit, *_ = spielerMitEinerEinheit().armee.einheiten
    modell, *_ = einheit.modelle
    ersteArmee = Armee(einheiten=(Einheit(modelle=(modell,)),))
    zweiteArmee = Armee(einheiten=(Einheit(modelle=(modell,)),))

    with pytest.raises(ValueError):
        aufstellungVon(Spieler(armee=ersteArmee), Spieler(armee=zweiteArmee))
