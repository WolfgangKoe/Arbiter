"""Testdaten der Akzeptanztests: kleine Armeen auf dem Spielfeld von Only War."""

from dataclasses import replace
from fractions import Fraction

import pytest
from arbiter.katalog.ausgangslage import ausgangslageLaden

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone, Ausgangslage
from arbiter.domaene.sperre import Grund, Sperre
from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell, Spieler, Stelle

# Regel: 1 Zoll sind 25,4 mm (domaene/glossar.md, Durchmesser)
millimeterJeZoll = Fraction(254, 10)
# Regel: Spielfeld 44″ × 60″, die erste Aufstellungszone an der Kante x = 0, die zweite an x = 44
# (onlyWar.yaml); Stelle: Zoll von der Ecke, x entlang der ersten Seitenlänge, y der zweiten
breiteDesSpielfelds = 44
abstandDerReihen = Fraction(5, 2)
tiefeDerErstenReihe = Fraction(3, 2)
durchmesserDerTestmodelle = 32


def _spielerMit(*modellzahlen: int) -> Spieler:
    """Ein Spieler, dessen Armee je Zahl eine Einheit mit so vielen Modellen hat."""
    einheiten = tuple(
        Einheit(
            modelle=tuple(
                Modell(base=Base(durchmesser=durchmesserDerTestmodelle)) for _ in range(zahl)
            )
        )
        for zahl in modellzahlen
    )
    return Spieler(armee=Armee(einheiten=einheiten))


def _aufstellungVon(ersterSpieler: Spieler, zweiterSpieler: Spieler) -> Aufstellung:
    onlyWar = ausgangslageLaden()
    return Aufstellung(replace(onlyWar, ersterSpieler=ersterSpieler, zweiterSpieler=zweiterSpieler))


def _radiusInZoll(modell: Modell) -> Fraction:
    return Fraction(modell.base.durchmesser) / 2 / millimeterJeZoll


def _stelleInZone(zone: Aufstellungszone, tiefe: Fraction | int, länge: Fraction | int) -> Stelle:
    """Tiefe von der Spielfeldkante der Zone nach innen, Länge entlang dieser Kante."""
    ersteHälfte = zone is Aufstellungszone.erste
    breite = Fraction(tiefe) if ersteHälfte else breiteDesSpielfelds - Fraction(tiefe)
    return Stelle(x=breite, y=Fraction(länge))


def _stellenDerEinheit(
    aufstellung: Aufstellung, spieler: Spieler, einheit: Einheit
) -> list[tuple[Modell, Stelle]]:
    """Die Modelle in einer Reihe, Base an Base, je Einheit eine eigene Reihe in der Zone."""
    zone = aufstellung.aufstellungszone(spieler)
    reihe = spieler.armee.einheiten.index(einheit)
    tiefe = tiefeDerErstenReihe + abstandDerReihen * reihe
    länge = Fraction(0)
    stellen = []
    for modell in einheit.modelle:
        länge += _radiusInZoll(modell)
        stellen.append((modell, _stelleInZone(zone, tiefe, länge)))
        länge += _radiusInZoll(modell)
    return stellen


def _stelleDesErstenModells(aufstellung: Aufstellung, spieler: Spieler, einheit: Einheit) -> Stelle:
    (_, stelle), *_ = _stellenDerEinheit(aufstellung, spieler, einheit)
    return stelle


def _einheitAufstellen(aufstellung: Aufstellung, einheit: Einheit) -> None:
    spieler = aufstellung.anDerReihe
    aufstellung.einheitInAufstellungWählen(einheit)
    for modell, stelle in _stellenDerEinheit(aufstellung, spieler, einheit):
        aufstellung.modellSetzen(modell, stelle)
    aufstellung.aufstellenDerEinheitBeenden()


def _sperrgründe(handlung, *argumente) -> frozenset[Grund]:
    with pytest.raises(Sperre) as sperre:
        handlung(*argumente)
    return sperre.value.gründe


def _durchmesserJeEinheit(spieler: Spieler) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(modell.base.durchmesser for modell in einheit.modelle)
        for einheit in spieler.armee.einheiten
    )


@pytest.fixture
def sperrgründe():
    return _sperrgründe


@pytest.fixture
def durchmesserJeEinheit():
    return _durchmesserJeEinheit


@pytest.fixture
def ausgangslage() -> Ausgangslage:
    return ausgangslageLaden()


@pytest.fixture
def spielerMit():
    return _spielerMit


@pytest.fixture
def aufstellungVon():
    return _aufstellungVon


@pytest.fixture
def stellenDerEinheit():
    return _stellenDerEinheit


@pytest.fixture
def stelleDesErstenModells():
    return _stelleDesErstenModells


@pytest.fixture
def einheitAufstellen():
    return _einheitAufstellen


class Platz:
    """Stellen in der Zone des ersten Spielers und die Maße der Testmodelle."""

    def __init__(self, zone: Aufstellungszone) -> None:
        self._zone = zone
        self.radius = _radiusInZoll(Modell(base=Base(durchmesser=durchmesserDerTestmodelle)))
        # Warum: Schon ein Millionstel Zoll entscheidet, damit Grenzfälle ohne Toleranz gelten.
        self.millionstel = Fraction(1, 1_000_000)

    def stelle(self, tiefe, länge) -> Stelle:
        return _stelleInZone(self._zone, tiefe, länge)

    def sperrgründe(self, handlung, *argumente) -> frozenset[Grund]:
        return _sperrgründe(handlung, *argumente)


@pytest.fixture
def ersterSpieler() -> Spieler:
    return _spielerMit(2, 1)


@pytest.fixture
def zweiterSpieler() -> Spieler:
    return _spielerMit(2, 1)


@pytest.fixture
def aufstellung(ersterSpieler: Spieler, zweiterSpieler: Spieler) -> Aufstellung:
    return _aufstellungVon(ersterSpieler, zweiterSpieler)


@pytest.fixture(params=list(Aufstellungszone), ids=[zone.name for zone in Aufstellungszone])
def zone(request) -> Aufstellungszone:
    return request.param


@pytest.fixture
def platz(zone: Aufstellungszone) -> Platz:
    return Platz(zone)


@pytest.fixture
def einheitInAufstellung(
    aufstellung: Aufstellung, ersterSpieler: Spieler, zweiterSpieler: Spieler, zone
) -> Einheit:
    """Der erste Spieler ist mit der Zone an der Reihe und hat seine erste Einheit gewählt."""
    andereZone = next(kandidat for kandidat in Aufstellungszone if kandidat is not zone)
    aufstellung.gewinnerWählen(zweiterSpieler)
    aufstellung.aufstellungszoneWählen(andereZone)
    ersteEinheit, _ = ersterSpieler.armee.einheiten
    aufstellung.einheitInAufstellungWählen(ersteEinheit)
    return ersteEinheit


@pytest.fixture
def einheitNachDemAnderenSpieler(
    aufstellung: Aufstellung, ersterSpieler: Spieler, zweiterSpieler: Spieler, zone
) -> Einheit:
    """Beide haben ihre erste Einheit aufgestellt; der erste Spieler hat seine zweite gewählt."""
    andereZone = next(kandidat for kandidat in Aufstellungszone if kandidat is not zone)
    ersteEinheit, zweiteEinheit = ersterSpieler.armee.einheiten
    einheitDesAnderenSpielers, _ = zweiterSpieler.armee.einheiten
    aufstellung.gewinnerWählen(zweiterSpieler)
    aufstellung.aufstellungszoneWählen(andereZone)
    _einheitAufstellen(aufstellung, ersteEinheit)
    _einheitAufstellen(aufstellung, einheitDesAnderenSpielers)
    aufstellung.einheitInAufstellungWählen(zweiteEinheit)
    return zweiteEinheit
