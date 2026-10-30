"""Das Anhalten der gezogenen Modelle an ihrer Bewegungsweite (BEW-3, V16)."""

from collections.abc import Mapping
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Modell, Stelle


def _distanzÜberDerBewegungsweite(gezogenes: Modell, anfang: Stelle, stelle: Stelle) -> bool:
    return messen.abstandImQuadrat(anfang, stelle) > gezogenes.bewegungsweite**2


def anDerBewegungsweiteAngehalten(
    vorige: Mapping[Modell, Stelle], weg: messen.Weg, anfang: Mapping[Modell, Stelle]
) -> dict[Modell, Stelle]:
    """Die Stellen nach dem Weg, gekürzt, bis keines weiter als seine Bewegungsweite steht."""
    schritte = messen.schritteDesWegs(weg)

    def stellenBeiSchritt(schritt: int) -> dict[Modell, Stelle]:
        kurz = messen.teilDesWegs(weg, Fraction(schritt, schritte))
        return {gezogenes: messen.verschoben(stelle, kurz) for gezogenes, stelle in vorige.items()}

    def überBeiSchritt(schritt: int) -> bool:
        return any(
            _distanzÜberDerBewegungsweite(gezogenes, anfang[gezogenes], stelle)
            for gezogenes, stelle in stellenBeiSchritt(schritt).items()
        )

    if schritte == 0 or not überBeiSchritt(schritte):
        return {gezogenes: messen.verschoben(stelle, weg) for gezogenes, stelle in vorige.items()}
    erster = messen.ersterSchrittMit(überBeiSchritt, schritte + 1)
    return stellenBeiSchritt(erster - 1)
