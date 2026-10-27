"""Handgriffe der Akzeptanztests zur Schlacht: Phasen durchlaufen, Stellen und Wege."""

from fractions import Fraction
from itertools import pairwise
from pathlib import Path

import yaml

from arbiter.domaene.querschnitt.schlachtrunden import Phase
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle
from tests.akzeptanz.dienst import stelleImSpielstand
from tests.akzeptanz.handgriffe import stellenAllerModelle

_datenordner = Path(__file__).parents[3] / "domaene" / "daten"
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


def _daten(dateiname: str) -> dict:
    with (_datenordner / dateiname).open(encoding="utf-8") as datei:
        return yaml.safe_load(datei)


def letzteSchlachtrunde() -> int:
    """Die letzte Schlachtrunde der Mission aus `onlyWar.yaml`, nicht kopiert."""
    return _daten("onlyWar.yaml")["Schlacht"]["schlachtrunde"]


def zurLetztenSchlachtrunde(schlacht) -> None:
    """Beide Spieler beenden alle Züge vor der letzten Schlachtrunde."""
    zügeBeenden(schlacht, 2 * (letzteSchlachtrunde() - 1))


def bewegungsweite(einheitenname: str) -> Fraction:
    """B der Einheit in Zoll aus `ausgangslage.yaml`, nicht kopiert."""
    einheiten = (einheit for armee in _daten("ausgangslage.yaml")["Armee"] for einheit in armee)
    eintrag = next(einheit for einheit in einheiten if einheit["Einheit"] == einheitenname)
    return Fraction(eintrag["bewegungsweite"])


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
