"""Das Anhalten der gezogenen Modelle an ihrer Bewegungsweite (BEW-3, V16)."""

from bisect import bisect_left
from collections.abc import Mapping
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Modell, Stelle


def anDerBewegungsweiteAngehalten(
    vorige: Mapping[Modell, Stelle], neue: Mapping[Modell, Stelle], anfang: Mapping[Modell, Stelle]
) -> dict[Modell, Stelle]:
    """Die neuen Stellen, der Weg gekürzt, bis keines weiter als seine Bewegungsweite steht."""
    modell, *_ = neue
    weg = messen.wegZwischen(vorige[modell], neue[modell])
    schritte = messen.schritteDesWegs(weg)

    def stellenBeiSchritt(schritt: int) -> dict[Modell, Stelle]:
        kurz = messen.teilDesWegs(weg, Fraction(schritt, schritte))
        return {gezogenes: messen.verschoben(vorige[gezogenes], kurz) for gezogenes in neue}

    def überBeiSchritt(schritt: int) -> bool:
        return any(
            messen.abstandImQuadrat(anfang[gezogenes], stelle) > gezogenes.bewegungsweite**2
            for gezogenes, stelle in stellenBeiSchritt(schritt).items()
        )

    if schritte == 0 or not überBeiSchritt(schritte):
        return dict(neue)
    erster = bisect_left(range(schritte + 1), x=True, key=überBeiSchritt)
    return stellenBeiSchritt(max(erster - 1, 0))
