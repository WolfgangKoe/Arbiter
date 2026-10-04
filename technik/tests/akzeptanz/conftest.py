"""Testdaten der Akzeptanztests: kleine Armeen auf dem Spielfeld von Only War."""

from dataclasses import dataclass, replace
from fractions import Fraction

import pytest
from playwright.sync_api import Locator, Page, sync_playwright

from arbiter.domaene.phasen.aufstellen import Aufstellung, Aufstellungszone, Ausgangslage
from arbiter.domaene.sperre import Grund, Sperre
from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell, Spieler, Stelle
from arbiter.katalog.ausgangslage import ausgangslageLaden

# Regel: 1 Zoll sind 25,4 mm (domaene/glossar.md, Durchmesser)
millimeterJeZoll = Fraction(254, 10)
# Warum: Lage der Zonen, Ursprung und Achsen der Stelle stehen in technik/architektur.md, S1
breiteDesSpielfelds = 44
längeDerSpielfeldkante = 60
tiefeDerZone = 9
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
        self.breiteDesSpielfelds = breiteDesSpielfelds
        self.längeDerSpielfeldkante = längeDerSpielfeldkante
        self.tiefeDerZone = tiefeDerZone
        self.tiefeDerErstenReihe = tiefeDerErstenReihe

    def stelle(self, tiefe, länge) -> Stelle:
        return _stelleInZone(self._zone, tiefe, länge)

    def stelleBeimAnderenSpieler(self, abstandDerMittelpunkte, richtung) -> Stelle:
        """Eine Stelle, deren Mittelpunkt so weit vom letzten Modell der ersten Einheit liegt."""
        anteilX, anteilY = richtung
        tiefe = (
            self.breiteDesSpielfelds - self.tiefeDerErstenReihe - abstandDerMittelpunkte * anteilX
        )
        return self.stelle(tiefe, 3 * self.radius + abstandDerMittelpunkte * anteilY)


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


@pytest.fixture
def radiusInZoll():
    return _radiusInZoll


@pytest.fixture
def spielerEins(ausgangslage: Ausgangslage) -> Spieler:
    return ausgangslage.ersterSpieler


@pytest.fixture
def spielerZwei(ausgangslage: Ausgangslage) -> Spieler:
    return ausgangslage.zweiterSpieler


@pytest.fixture
def boyz(spielerEins: Spieler) -> Einheit:
    einheit, _ = spielerEins.armee.einheiten
    return einheit


@pytest.fixture
def warboss(spielerEins: Spieler) -> Einheit:
    _, einheit = spielerEins.armee.einheiten
    return einheit


@pytest.fixture
def necronWarriors(spielerZwei: Spieler) -> Einheit:
    einheit, _ = spielerZwei.armee.einheiten
    return einheit


@pytest.fixture
def ausgangsaufstellung(ausgangslage: Ausgangslage) -> Aufstellung:
    return Aufstellung(ausgangslage)


@pytest.fixture
def aufstellungNachDerZonenwahl(
    ausgangsaufstellung: Aufstellung, spielerZwei: Spieler
) -> Aufstellung:
    """Spieler 2 hat gewonnen und die erste Zone gewählt; Spieler 1 ist an der Reihe."""
    ausgangsaufstellung.gewinnerWählen(spielerZwei)
    ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.erste)
    return ausgangsaufstellung


def _modelleSetzen(
    aufstellung: Aufstellung, einheit: Einheit, anzahl: int
) -> list[tuple[Modell, Stelle]]:
    """Wählt die Einheit und setzt die ersten Modelle ihrer Reihe, ohne sie zu beenden."""
    spieler = aufstellung.anDerReihe
    aufstellung.einheitInAufstellungWählen(einheit)
    gesetzt = _stellenDerEinheit(aufstellung, spieler, einheit)[:anzahl]
    for modell, stelle in gesetzt:
        aufstellung.modellSetzen(modell, stelle)
    return gesetzt


@pytest.fixture
def modelleSetzen():
    return _modelleSetzen


@pytest.fixture
def aufstellungMitModellenBeiderSpieler(
    aufstellungNachDerZonenwahl: Aufstellung, boyz: Einheit, necronWarriors: Einheit
) -> Aufstellung:
    _einheitAufstellen(aufstellungNachDerZonenwahl, boyz)
    _einheitAufstellen(aufstellungNachDerZonenwahl, necronWarriors)
    return aufstellungNachDerZonenwahl


def _einheitenAufstellen(aufstellung: Aufstellung, anzahl: int) -> None:
    """Der jeweils an der Reihe ist, stellt seine nächste Einheit auf, so oft wie verlangt."""
    for _ in range(anzahl):
        spieler = aufstellung.anDerReihe
        nächste = next(
            einheit for einheit in spieler.armee.einheiten if not aufstellung.aufgestellt(einheit)
        )
        _einheitAufstellen(aufstellung, nächste)


@pytest.fixture
def einheitenAufstellen():
    return _einheitenAufstellen


@dataclass(frozen=True)
class Element:
    """Ein Element der Seite, wie der Browser es zeigt."""

    art: str
    attribute: dict[str, str]
    fill: str
    farbe: str
    text: str
    breiteInPixeln: float
    höheInPixeln: float

    def zahl(self, name: str) -> float:
        return float(self.attribute[name])


_elementeLesen = """elemente => elemente.map(element => {
    const stil = getComputedStyle(element)
    const rahmen = element.getBoundingClientRect()
    return {
        art: element.tagName.toLowerCase(),
        attribute: Object.fromEntries([...element.attributes].map(att => [att.name, att.value])),
        fill: stil.fill,
        farbe: stil.color,
        text: element.textContent.trim(),
        breiteInPixeln: rahmen.width,
        höheInPixeln: rahmen.height,
    }
})"""


def _elementeDerSeite(seite: Page, auswahl: str) -> tuple[Element, ...]:
    gelesen = seite.locator(auswahl).evaluate_all(_elementeLesen)
    return tuple(Element(**eintrag) for eintrag in gelesen)


def _modellfarben(seite: Page, aufstellung: Aufstellung, spieler: Spieler) -> frozenset[str]:
    """Die Füllfarben der Kreise, die an den Stellen der gesetzten Modelle des Spielers liegen."""
    farbeJeStelle = {
        (kreis.zahl("cx"), kreis.zahl("cy")): kreis.fill
        for kreis in _elementeDerSeite(seite, ".karte .modell")
    }
    return frozenset(
        farbeJeStelle[float(stelle.x), float(stelle.y)]
        for modell in spieler.armee.modelle
        if (stelle := aufstellung.stelle(modell)) is not None
    )


def _ablageVon(seite: Page, spielername: str) -> Locator:
    name = seite.locator(".armeeKartenName", has_text=spielername)
    return seite.locator(".armeeKarte").filter(has=name)


@pytest.fixture
def elementeDerSeite():
    return _elementeDerSeite


@pytest.fixture
def modellfarben():
    return _modellfarben


@pytest.fixture
def ablageVon():
    return _ablageVon


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        chromium = playwright.chromium.launch()
        yield chromium
        chromium.close()


@pytest.fixture
def seiteBei(browser):
    """Öffnet die Adresse und wartet auf das Spielfeld, erst dann gilt, was die Seite zeigt."""
    seiten = []

    def öffnen(adresse: str) -> Page:
        seite = browser.new_page()
        seiten.append(seite)
        seite.set_default_timeout(5000)
        seite.goto(adresse)
        seite.wait_for_selector(".karte .spielfeld")
        return seite

    yield öffnen
    for seite in seiten:
        seite.close()


@pytest.fixture
def seiteZu(seiteBei):
    """Startet den Server mit dem Spielstand im selben Prozess und öffnet seine Seite."""
    gestartete = []

    def öffnen(aufstellung: Aufstellung) -> Page:
        # Warum: web/ gibt es erst mit dem Code; ein Import oben bräche die Sammlung aller Tests
        from arbiter.web.server import serverStarten

        server = serverStarten(aufstellung)
        gestartete.append(server)
        return seiteBei(server.adresse)

    yield öffnen
    for server in gestartete:
        server.beenden()


@dataclass(frozen=True)
class Bildschirm:
    """Die Handgriffe der Bildschirmtests, als ein Fixture gebündelt."""

    seiteZu: object
    elementeDerSeite: object
    modellfarben: object
    ablageVon: object


@pytest.fixture
def bildschirm(seiteZu, elementeDerSeite, modellfarben, ablageVon) -> Bildschirm:
    return Bildschirm(seiteZu, elementeDerSeite, modellfarben, ablageVon)


@pytest.fixture
def boyzSetzen(aufstellungNachDerZonenwahl, boyz, modelleSetzen):
    """Spieler 1 wählt die Boyz und setzt so viele ihrer Modelle, wie verlangt."""

    def setzen(anzahl: int) -> list[tuple[Modell, Stelle]]:
        return modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahl)

    return setzen


@pytest.fixture
def einGesetztesModell(aufstellungNachDerZonenwahl, boyzSetzen) -> tuple[Aufstellung, Modell]:
    [(modell, _)] = boyzSetzen(1)
    return aufstellungNachDerZonenwahl, modell
