from fractions import Fraction

from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import Weiterrücken
from arbiter.domaene.phasen.bewegung import Bewegungsphase
from arbiter.domaene.spielobjekte import Base, Spielfeld, Stelle
from tests.einheit.modelle import modellMit

spielfeld = Spielfeld(seitenlängen=(Fraction(60), Fraction(44)))


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(x=Fraction(inX + 10), y=Fraction(inY + 10))


def testAngehaltenAufDemWegKürztDieBewegungsweiteAbDerStelleVorDemZiehen():
    modell = modellMit(Base(durchmesser=25))
    stellen = {modell: stelleAn(0, 0)}
    weiter = Weiterrücken(stelleAn(0, 3), angehaltenAufDemWeg=True)

    gezeigt, _ = Bewegungsphase(stellen, spielfeld).stellenMitGründenNachDemZiehen(
        stellen, modell, stelleAn(20, 3), stellen, {}, weiter
    )

    stelle = gezeigt.stellen[modell]
    assert (round(float(stelle.x) - 10, 2), round(float(stelle.y) - 10, 2)) == (4.94, 0.74)
