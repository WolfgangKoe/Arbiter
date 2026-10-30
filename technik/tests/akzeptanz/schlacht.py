"""Handgriffe der Akzeptanztests zur Schlacht: Phasen durchlaufen, Stellen und Wege."""

from fractions import Fraction
from itertools import pairwise
from typing import NamedTuple

from arbiter.domaene.querschnitt.schlachtrunden import Phase
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from tests.akzeptanz.dienst import stelleImSpielstand
from tests.akzeptanz.handgriffe import (
    breiteDesSpielfelds,
    eintragDerAusgangslage,
    längeDerSpielfeldkante,
    modellartenImKatalog,
    radiusInZoll,
    sperrgründe,
    stellenAllerModelle,
    versetzt,
    yamlAusDenDaten,
)

schrägOhneHindernis = (Fraction(1), Fraction(2))
ostenUndNorden = (Fraction(2), Fraction(3))

phasenEinesZugs = (
    Phase.kommandophase,
    Phase.bewegungsphase,
    Phase.psiphase,
    Phase.schussphase,
    Phase.angriffsphase,
    Phase.nahkampfphase,
    Phase.moralphase,
)
phasenwechsel = tuple(pairwise(phasenEinesZugs))
phasenwechselIds = [f"{davor.name}Dann{danach.name}" for davor, danach in phasenwechsel]
phasenAußerDerBewegungsphase = tuple(
    phase for phase in phasenEinesZugs if phase is not Phase.bewegungsphase
)
phasenAußerDerBewegungsphaseIds = [phase.name for phase in phasenAußerDerBewegungsphase]


def phaseBeendenBis(schlacht, phase: Phase) -> None:
    """Beendet Phasen, bis die Schlacht in der Phase ist; ist sie es schon, geschieht nichts."""
    for _ in phasenEinesZugs:
        if schlacht.phase is phase:
            return
        schlacht.phaseBeenden()
    raise AssertionError(f"Die Phase {phase.name} kam nicht in einem Zug")


def zügeBeenden(schlacht, anzahl: int) -> None:
    """Beendet ganze Züge, beginnend in der Kommandophase."""
    for _ in range(anzahl * len(phasenEinesZugs)):
        schlacht.phaseBeenden()


def zurBewegungsphaseDerNächstenSchlachtrunde(schlacht) -> None:
    runde = schlacht.schlachtrunde
    for _ in range(2 * len(phasenEinesZugs)):
        if schlacht.schlachtrunde != runde:
            break
        schlacht.phaseBeenden()
    phaseBeendenBis(schlacht, Phase.bewegungsphase)


def letzteSchlachtrunde() -> int:
    """Die letzte Schlachtrunde der Mission aus `onlyWar.yaml`, nicht kopiert."""
    return yamlAusDenDaten("onlyWar.yaml")["Schlacht"]["schlachtrunde"]


def zurLetztenSchlachtrunde(schlacht) -> None:
    """Beide Spieler beenden alle Züge vor der letzten Schlachtrunde."""
    zügeBeenden(schlacht, 2 * (letzteSchlachtrunde() - 1))


def bewegungsweite(datenblatt: str, modellart: str) -> Fraction:
    """Bewegungsweite der Modellart in Zoll aus dem Datenblatt im Katalog, nicht kopiert."""
    modellarten = modellartenImKatalog(eintragDerAusgangslage(datenblatt))
    return Fraction(modellarten[modellart]["bewegungsweite"])


def jetzigeStellen(schlacht, einheit: Einheit) -> dict[Modell, Stelle]:
    return {modell: schlacht.stelle(modell) for modell in einheit.modelle}


def stellenAlsZahlen(schlacht) -> frozenset[tuple[float, float]]:
    """Die Stellen aller gesetzten Modelle als Zahlenpaare, wie die Karte sie zeichnet."""
    gesetzte = (stelle for stelle in stellenAllerModelle(schlacht).values() if stelle is not None)
    return frozenset(stelleImSpielstand(stelle) for stelle in gesetzte)


def stellenDerEinheitAlsZahlen(schlacht, einheit: Einheit) -> frozenset[tuple[float, float]]:
    return frozenset(stelleImSpielstand(schlacht.stelle(modell)) for modell in einheit.modelle)


def stellenVersetzt(
    stellen: dict[Modell, Stelle], weg: tuple[Fraction, Fraction]
) -> dict[Modell, Stelle]:
    """Dieselben Modelle, jedes um den Weg versetzt."""
    wegInX, wegInY = weg
    return {
        modell: Stelle(x=stelle.x + wegInX, y=stelle.y + wegInY)
        for modell, stelle in stellen.items()
    }


hundertstelZoll = Fraction(1, 100)


def abstandImQuadrat(von: Stelle, nach: Stelle) -> Fraction:
    """Das Quadrat der geraden Strecke, exakt (Vertrag S2)."""
    return (nach.x - von.x) ** 2 + (nach.y - von.y) ** 2


def hältAnDerBewegungsweite(davor: Stelle, danach: Stelle, bewegungsweite: Fraction) -> bool:
    """Das Modell steht höchstens die Bewegungsweite und höchstens 1/100″ davor (BEW-3.1)."""
    abstand = abstandImQuadrat(davor, danach)
    return (bewegungsweite - hundertstelZoll) ** 2 <= abstand <= bewegungsweite**2


def liegtAufDerGeradenVon(davor: Stelle, ziel: Stelle, danach: Stelle) -> bool:
    """Die Stelle `danach` liegt von `davor` aus in Richtung `ziel`."""
    zumZielInX, zumZielInY = ziel.x - davor.x, ziel.y - davor.y
    danachInX, danachInY = danach.x - davor.x, danach.y - davor.y
    parallel = zumZielInX * danachInY == zumZielInY * danachInX
    gleicheRichtung = zumZielInX * danachInX + zumZielInY * danachInY > 0
    return parallel and gleicheRichtung


def einModellAusDerKohärenzZiehen(schlacht, einheit: Einheit) -> None:
    """Das letzte Modell der Einheit geht fünf Zoll nach Osten, weit weg von seinen Nachbarn."""
    *_, letztes = einheit.modelle
    ziel = versetzt(schlacht.stelle(letztes), (Fraction(5), Fraction(0)))
    schlacht.modellLoslassen(letztes, ziel)


fünfZollNachOsten = (Fraction(5), Fraction(0))
fünfZollNachWesten = (Fraction(-5), Fraction(0))


class ZugÜberEineBase(NamedTuple):
    schlacht: object
    spieler: Spieler
    einheit: Einheit
    modell: Modell
    ziel: Stelle


def gemeinsamÜbergehen(schlacht, modell: Modell, ziel: Stelle) -> frozenset[Grund]:
    gründe = sperrgründe(schlacht.modellLoslassen, modell, ziel)
    schlacht.modellLoslassen(modell, ziel, übergehen=gründe)
    return gründe


def boyÜberDenWarbossÜbergehen(schlacht, boyz: Einheit) -> Stelle:
    erster, *_ = boyz.modelle
    ziel = versetzt(schlacht.stelle(erster), fünfZollNachOsten)
    gemeinsamÜbergehen(schlacht, erster, ziel)
    return ziel


def warbossÜberDieBoyzÜbergehen(schlacht, warboss: Einheit) -> Stelle:
    (modell,) = warboss.modelle
    ziel = versetzt(schlacht.stelle(modell), fünfZollNachOsten)
    gemeinsamÜbergehen(schlacht, modell, ziel)
    return ziel


def zurBewegungsphaseDesNächstenZugs(schlacht) -> None:
    schlacht.phaseBeenden()
    phaseBeendenBis(schlacht, Phase.bewegungsphase)


def summeDerRadien(modell: Modell, anderes: Modell) -> Fraction:
    return radiusInZoll(modell) + radiusInZoll(anderes)


def restBisZumAbstandInX(schlacht, modell: Modell, anderes: Modell, abstand: Fraction) -> Fraction:
    mittelpunkteInX = abs(schlacht.stelle(anderes).x - schlacht.stelle(modell).x)
    return mittelpunkteInX - summeDerRadien(modell, anderes) - abstand


def aufDasAndereZu(schlacht, modell: Modell, anderes: Modell, abstand: Fraction) -> None:
    davor = schlacht.stelle(modell)
    richtung = 1 if schlacht.stelle(anderes).x > davor.x else -1
    schritt = min(modell.bewegungsweite, restBisZumAbstandInX(schlacht, modell, anderes, abstand))
    schlacht.modellLoslassen(modell, versetzt(davor, (richtung * schritt, Fraction(0))))


def aufeinanderZuZiehen(
    schlacht, modellAmZug: Modell, modellDesAnderenSpielers: Modell, abstand: Fraction
) -> None:
    spielerAmZug = schlacht.amZug
    gezogenes, anderes = modellAmZug, modellDesAnderenSpielers
    while restBisZumAbstandInX(schlacht, gezogenes, anderes, abstand) > 0:
        aufDasAndereZu(schlacht, gezogenes, anderes, abstand)
        zurBewegungsphaseDesNächstenZugs(schlacht)
        gezogenes, anderes = anderes, gezogenes
    while schlacht.amZug is not spielerAmZug:
        zurBewegungsphaseDesNächstenZugs(schlacht)


def hältVorDerNahkampfreichweite(
    stelle: Stelle, modell: Modell, stelleDesAnderen: Stelle, anderes: Modell
) -> bool:
    grenze = summeDerRadien(modell, anderes) + 1
    abstandImQuadratDerMittelpunkte = abstandImQuadrat(stelle, stelleDesAnderen)
    return grenze**2 < abstandImQuadratDerMittelpunkte <= (grenze + hundertstelZoll) ** 2


def außerhalbDerNahkampfreichweite(
    stelle: Stelle, modell: Modell, stelleDesAnderen: Stelle, anderes: Modell
) -> bool:
    grenze = summeDerRadien(modell, anderes) + 1
    return abstandImQuadrat(stelle, stelleDesAnderen) > grenze**2


def abständeZuDenSpielfeldkanten(stelle: Stelle, modell: Modell) -> tuple[Fraction, ...]:
    radius = radiusInZoll(modell)
    return (
        stelle.x - radius,
        stelle.y - radius,
        breiteDesSpielfelds - stelle.x - radius,
        längeDerSpielfeldkante - stelle.y - radius,
    )


def hältAnDerSpielfeldkante(stelle: Stelle, modell: Modell) -> bool:
    nächsteKante = min(abständeZuDenSpielfeldkanten(stelle, modell))
    return 0 <= nächsteKante <= hundertstelZoll


mitteDesSpielfelds = Stelle(
    x=Fraction(breiteDesSpielfelds, 2), y=Fraction(längeDerSpielfeldkante, 2)
)


def modellZurEbeneMachen(schlacht, einheit: Einheit, modell: Modell) -> None:
    schlacht.auswählen(einheit)
    schlacht.modellAnklicken(modell)
