from collections.abc import Mapping
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Modell, Stelle


def _distanzÜberDerBewegungsweite(
    gezogenes: Modell, anfang: Stelle, stelle: Stelle, vorrückwurf: int
) -> bool:
    return messen.abstandImQuadrat(anfang, stelle) > (gezogenes.bewegungsweite + vorrückwurf) ** 2


def anteilBisZurBewegungsweite(
    vorige: Mapping[Modell, Stelle],
    weg: messen.Weg,
    anfang: Mapping[Modell, Stelle],
    vorrückwurf: int,
) -> Fraction:
    def überBeiAnteil(anteil: Fraction) -> bool:
        kurz = messen.teilDesWegs(weg, anteil)
        return any(
            _distanzÜberDerBewegungsweite(
                gezogenes, anfang[gezogenes], messen.verschoben(stelle, kurz), vorrückwurf
            )
            for gezogenes, stelle in vorige.items()
        )

    if weg != (0, 0) and überBeiAnteil(Fraction(0)):
        return Fraction(0)
    return messen.anteilVorDemErstenSchrittMit(überBeiAnteil, weg)
