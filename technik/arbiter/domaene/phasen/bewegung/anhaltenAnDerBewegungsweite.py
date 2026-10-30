from collections.abc import Mapping
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Modell, Stelle


def _distanzÜberDerBewegungsweite(
    gezogenes: Modell, anfang: Stelle, stelle: Stelle, zuschlag: int
) -> bool:
    return messen.abstandImQuadrat(anfang, stelle) > (gezogenes.bewegungsweite + zuschlag) ** 2


def anteilBisZurBewegungsweite(
    vorige: Mapping[Modell, Stelle],
    weg: messen.Weg,
    anfang: Mapping[Modell, Stelle],
    zuschlag: int = 0,
) -> Fraction:
    def überBeiAnteil(anteil: Fraction) -> bool:
        kurz = messen.teilDesWegs(weg, anteil)
        return any(
            _distanzÜberDerBewegungsweite(
                gezogenes, anfang[gezogenes], messen.verschoben(stelle, kurz), zuschlag
            )
            for gezogenes, stelle in vorige.items()
        )

    return messen.anteilVorDemErstenSchrittMit(überBeiAnteil, weg)
