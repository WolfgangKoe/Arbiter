from fractions import Fraction

import pytest

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone, Ausgangslage
from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell, Spieler, Spielfeld, Stelle


def spielerMitEinerEinheit() -> Spieler:
    modell = Modell(base=Base(durchmesser=32))
    return Spieler(armee=Armee(einheiten=(Einheit(name="Einheit", modelle=(modell,)),)))


def ausgangslageVon(ersterSpieler: Spieler, zweiterSpieler: Spieler) -> Ausgangslage:
    spielfeld = Spielfeld(seitenlängen=(Fraction(44), Fraction(60)))
    tiefen = {zone: Fraction(9) for zone in Aufstellungszone}
    return Ausgangslage(ersterSpieler, zweiterSpieler, spielfeld, tiefen)


def aufstellungVon(ersterSpieler: Spieler, zweiterSpieler: Spieler) -> Aufstellung:
    return Aufstellung(ausgangslageVon(ersterSpieler, zweiterSpieler))


def testDerselbeSpielerAlsBeideSpielerIstEineVorbedingungsverletzung():
    spieler = spielerMitEinerEinheit()

    with pytest.raises(ValueError):
        ausgangslageVon(spieler, spieler)


def testEinFremderSpielerAlsGewinnerIstEineVorbedingungsverletzung():
    aufstellung = aufstellungVon(spielerMitEinerEinheit(), spielerMitEinerEinheit())

    fremder = spielerMitEinerEinheit()

    with pytest.raises(ValueError):
        aufstellung.gewinnerWählen(fremder)

    assert aufstellung.gewinner is None


def testDieAufstellungszoneEinesFremdenSpielersIstEineVorbedingungsverletzung():
    aufstellung = aufstellungVon(spielerMitEinerEinheit(), spielerMitEinerEinheit())

    fremder = spielerMitEinerEinheit()

    with pytest.raises(ValueError):
        aufstellung.aufstellungszone(fremder)


def testWerKeineEinheitAufzustellenHatWirdNachDerZonenwahlÜbersprungen():
    gewinner = spielerMitEinerEinheit()
    ohneEinheit = Spieler(armee=Armee())
    aufstellung = aufstellungVon(gewinner, ohneEinheit)

    aufstellung.gewinnerWählen(gewinner)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)

    assert aufstellung.anDerReihe is gewinner


def testZweiSpielerMitDerselbenArmeeSindEineVorbedingungsverletzung():
    armee = spielerMitEinerEinheit().armee

    ersterSpieler = Spieler(armee=armee)
    zweiterSpieler = Spieler(armee=armee)

    with pytest.raises(ValueError):
        ausgangslageVon(ersterSpieler, zweiterSpieler)


def testZweiSpielerMitEinerGemeinsamenEinheitSindEineVorbedingungsverletzung():
    gemeinsam = spielerMitEinerEinheit().armee.einheiten
    eigene, *_ = spielerMitEinerEinheit().armee.einheiten

    ersterSpieler = Spieler(armee=Armee(einheiten=gemeinsam))
    zweiterSpieler = Spieler(armee=Armee(einheiten=(*gemeinsam, eigene)))

    with pytest.raises(ValueError):
        ausgangslageVon(ersterSpieler, zweiterSpieler)


def testZweiSpielerMitEinemGemeinsamenModellSindEineVorbedingungsverletzung():
    einheit, *_ = spielerMitEinerEinheit().armee.einheiten
    modell, *_ = einheit.modelle
    ersteArmee = Armee(einheiten=(Einheit(name="Einheit", modelle=(modell,)),))
    zweiteArmee = Armee(einheiten=(Einheit(name="Einheit", modelle=(modell,)),))

    ersterSpieler = Spieler(armee=ersteArmee)
    zweiterSpieler = Spieler(armee=zweiteArmee)

    with pytest.raises(ValueError):
        ausgangslageVon(ersterSpieler, zweiterSpieler)


def testZweiSpielerMitDerselbenLeerenArmeeSindEineVorbedingungsverletzung():
    leer = Armee()

    ersterSpieler = Spieler(armee=leer)
    zweiterSpieler = Spieler(armee=leer)

    with pytest.raises(ValueError):
        ausgangslageVon(ersterSpieler, zweiterSpieler)


def testEinFremdesModellSetzenIstEineVorbedingungsverletzung():
    aufstellung = aufstellungVon(spielerMitEinerEinheit(), spielerMitEinerEinheit())
    fremdes = Modell(base=Base(durchmesser=32))
    stelle = Stelle(x=Fraction(1), y=Fraction(1))

    with pytest.raises(ValueError):
        aufstellung.modellSetzen(fremdes, stelle)


def testAuswählenUndAbwählenMerktSichDieEinheit():
    spieler = spielerMitEinerEinheit()
    aufstellung = aufstellungVon(spieler, spielerMitEinerEinheit())
    einheit, *_ = spieler.armee.einheiten

    aufstellung.auswählen(einheit)
    ausgewähltDanach = aufstellung.ausgewählt(einheit)
    aufstellung.abwählen(einheit)
    aufstellung.abwählen(einheit)

    assert ausgewähltDanach
    assert not aufstellung.ausgewählt(einheit)


def testEineFremdeEinheitAuswählenIstEineVorbedingungsverletzung():
    aufstellung = aufstellungVon(spielerMitEinerEinheit(), spielerMitEinerEinheit())
    fremde = Einheit(name="Fremde", modelle=())

    with pytest.raises(ValueError):
        aufstellung.auswählen(fremde)


def testEineFremdeEinheitAbwählenIstEineVorbedingungsverletzung():
    aufstellung = aufstellungVon(spielerMitEinerEinheit(), spielerMitEinerEinheit())
    fremde = Einheit(name="Fremde", modelle=())

    with pytest.raises(ValueError):
        aufstellung.abwählen(fremde)


def testEineAufgestellteEinheitAuswählenIstEineVorbedingungsverletzung():
    gewinner, gegner = spielerMitEinerEinheit(), spielerMitEinerEinheit()
    aufstellung = aufstellungVon(gewinner, gegner)
    aufstellung.gewinnerWählen(gewinner)
    aufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    einheit, *_ = gegner.armee.einheiten
    modell, *_ = einheit.modelle
    aufstellung.modellSetzen(modell, Stelle(x=Fraction(40), y=Fraction(2)))
    aufstellung.aufstellenDerEinheitBeenden()

    with pytest.raises(ValueError):
        aufstellung.auswählen(einheit)
