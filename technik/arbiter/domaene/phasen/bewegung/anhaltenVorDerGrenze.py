from collections.abc import Mapping
from fractions import Fraction
from functools import partial

from arbiter.domaene import messen
from arbiter.domaene.querschnitt.setzen import nahkampfreichweite
from arbiter.domaene.spielobjekte import Modell, Spielfeld, Stelle


def anteilBisZurSpielfeldkante(
    vorige: Mapping[Modell, Stelle], weg: messen.Weg, spielfeld: Spielfeld
) -> Fraction:
    breite, länge = spielfeld.seitenlängen
    grenzenInX, grenzenInY = (Fraction(0), breite), (Fraction(0), länge)

    def draußenBeiAnteil(anteil: Fraction) -> bool:
        kurz = messen.teilDesWegs(weg, anteil)
        return any(
            not messen.ganzIn(
                gezogenes.base, messen.verschoben(stelle, kurz), grenzenInX, grenzenInY
            )
            for gezogenes, stelle in vorige.items()
        )

    return messen.anteilVorDemErstenSchrittMit(draußenBeiAnteil, weg)


def anteilBisZurNahkampfreichweite(
    vorige: Mapping[Modell, Stelle], weg: messen.Weg, gegner: Mapping[Modell, Stelle]
) -> Fraction:
    bewegte = [(gezogenes.base, stelle) for gezogenes, stelle in vorige.items()]
    hindernisse = [(anderes.base, stelle) for anderes, stelle in gegner.items()]
    inReichweite = partial(messen.abstandHöchstens, zoll=nahkampfreichweite)
    return messen.anteilBisZurBerührungAufDemWeg(bewegte, hindernisse, weg, inReichweite)
