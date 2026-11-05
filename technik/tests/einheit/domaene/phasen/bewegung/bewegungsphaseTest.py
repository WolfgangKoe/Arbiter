from fractions import Fraction

import pytest

from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import Weiterrücken
from arbiter.domaene.phasen.bewegung import Bewegungsphase, Gezogen
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Base, Spielfeld, Stelle
from tests.einheit.modelle import modellMit

berührungsabstandImQuadrat = 100
einZoll = Base(durchmesser=Fraction(254, 10))
spielfeld = Spielfeld(seitenlängen=(Fraction(60), Fraction(44)))


def stelleAn(inX: int, inY: int) -> Stelle:
    return Stelle(x=Fraction(inX + 10), y=Fraction(inY + 10))


def testAngehaltenAufDemWegKürztDieBewegungsweiteAbDerStelleVorDemZiehen():
    modell = modellMit(Base(durchmesser=25))
    stellen = {modell: stelleAn(0, 0)}
    weiter = Weiterrücken(stelleAn(0, 3), angehaltenAufDemWeg=True)

    gezeigt, _ = Bewegungsphase(stellen, spielfeld).stellenMitGründenNachDemZiehen(
        Gezogen(stellen, modell, stelleAn(20, 3), weiter), stellen, {}
    )

    stelle = gezeigt.stellen[modell]
    assert (round(float(stelle.x) - 10, 2), round(float(stelle.y) - 10, 2)) == (4.94, 0.74)


def testEinZeigerAufEinerFremdenBaseÄndertNichtsAnDerFreienStelleAnDerSpielfeldkante():
    klein = Base(durchmesser=25)
    boy, fremdes = modellMit(klein), modellMit(klein)
    vorher = Stelle(x=Fraction(30), y=Fraction(2))
    ebene = {boy: vorher}
    stellen = {**ebene, fremdes: Stelle(x=Fraction(31), y=Fraction(-3))}
    ziel = stellen[fremdes]
    phase = Bewegungsphase(ebene, spielfeld)

    gezogen = Gezogen(ebene, boy, ziel)
    erwartet, _ = phase.stellenMitGründenNachDemZiehen(gezogen, ebene, {})
    gezeigt, _ = phase.stellenMitGründenNachDemZiehen(gezogen, stellen, {})

    assert gezeigt.stellen == erwartet.stellen
    assert gezeigt.stellen[boy].y < vorher.y


def abstandsquadrat(erste: Stelle, zweite: Stelle) -> Fraction:
    return (erste.x - zweite.x) ** 2 + (erste.y - zweite.y) ** 2


def testEinFliegerWirdBeimZiehenÜberEineFremdeBaseGezeigtOhneGrund(zehnZoll):
    flieger, fremdes = modellMit(zehnZoll), modellMit(zehnZoll)
    ebene = {flieger: stelleAn(5, 10)}
    stellen = {**ebene, fremdes: stelleAn(14, 10)}
    gezogen = Gezogen(ebene, flieger, stelleAn(10, 10), fliegen=True)

    gezeigt, gründe = Bewegungsphase(ebene, spielfeld).stellenMitGründenNachDemZiehen(
        gezogen, stellen, {}
    )

    assert gezeigt.stellen == {flieger: stelleAn(10, 10)}
    assert gründe == set()


def testEinFliegerRücktBeimLoslassenAnDieNächsteFreieStelleOhneGrund(zehnZoll):
    flieger, fremdes = modellMit(zehnZoll), modellMit(zehnZoll)
    ebene = {flieger: stelleAn(5, 10)}
    stellen = {**ebene, fremdes: stelleAn(16, 10)}
    gezogen = Gezogen(ebene, flieger, stelleAn(10, 10), fliegen=True)

    gezeigt, gründe = Bewegungsphase(ebene, spielfeld).stellenMitGründenNachDemLoslassen(
        gezogen, stellen, {}
    )

    abstand = abstandsquadrat(gezeigt.stellen[flieger], stellen[fremdes])
    assert berührungsabstandImQuadrat <= abstand <= (10 + Fraction(1, 100)) ** 2
    assert gründe == set()


def testEinFliegerFindetBeimLoslassenKeineStelleInDerBewegungsweiteUndWirdGesperrt(zehnZoll):
    flieger, fremdes = modellMit(zehnZoll), modellMit(zehnZoll)
    zuBeginn = {flieger: stelleAn(12, 10)}
    ebene = {flieger: stelleAn(8, 10)}
    stellen = {**ebene, fremdes: stelleAn(13, 10)}
    gezogen = Gezogen(ebene, flieger, stelleAn(17, 10), fliegen=True)

    gezeigt, gründe = Bewegungsphase(zuBeginn, spielfeld).stellenMitGründenNachDemLoslassen(
        gezogen, stellen, {}
    )

    assert gezeigt.stellen == {flieger: stelleAn(17, 10)}
    assert Grund.baseÜberdeckt in gründe


def testEinFliegerRücktBeimLoslassenAuchDannAnDieFreieStelleWennEsNichtDasErsteModellDerEbeneIst(
    zehnZoll,
):
    erster, zweiter, fremdes = modellMit(zehnZoll), modellMit(zehnZoll), modellMit(zehnZoll)
    ebene = {erster: stelleAn(5, 10), zweiter: stelleAn(5, 22)}
    stellen = {**ebene, fremdes: stelleAn(16, 22)}
    gezogen = Gezogen(ebene, zweiter, stelleAn(10, 22), fliegen=True)
    phase = Bewegungsphase(ebene, spielfeld)

    gezeigt, gründe = phase.stellenMitGründenNachDemLoslassen(gezogen, stellen, {})

    abstand = abstandsquadrat(gezeigt.stellen[zweiter], stellen[fremdes])
    assert berührungsabstandImQuadrat <= abstand <= (10 + Fraction(1, 100)) ** 2
    assert gründe == set()


def testEinFliegerRücktBeimLoslassenVonDerStelleDesGezogenenZurückAuchWennEsNichtVorneSteht():
    hinten, gezogenes, fremdes = modellMit(einZoll), modellMit(einZoll), modellMit(einZoll)
    ebene = {hinten: stelleAn(20, 22), gezogenes: stelleAn(25, 22)}
    ziel = stelleAn(30, 22)
    stellen = {**ebene, fremdes: Stelle(x=ziel.x + Fraction(1, 2), y=ziel.y)}
    gezogen = Gezogen(ebene, gezogenes, ziel, fliegen=True)

    gezeigt, gründe = Bewegungsphase(ebene, spielfeld).stellenMitGründenNachDemLoslassen(
        gezogen, stellen, {}
    )

    assert gezeigt.stellen[gezogenes] != ziel
    assert gründe == set()


@pytest.mark.parametrize("richtung", [1, -1])
def testÜbergehenZweierFliegerRücktVonDerStelleDesGezogenenModellsZurückUnabhängigVonDerReihenfolge(
    richtung,
):
    erster, zweiter, fremdes = modellMit(einZoll), modellMit(einZoll), modellMit(einZoll)
    ebene = {erster: stelleAn(19, 22), zweiter: stelleAn(25, 22)}
    gezogenes = zweiter if richtung == 1 else erster
    ziel = Stelle(x=ebene[gezogenes].x + richtung * 6, y=ebene[gezogenes].y)
    stellen = {**ebene, fremdes: Stelle(x=ziel.x + richtung * Fraction(1, 2), y=ziel.y)}
    phase = Bewegungsphase(ebene, spielfeld)
    phase.angebotNachDemZiehen(Gezogen(ebene, gezogenes, ziel, fliegen=True), stellen, {})

    übergangen = phase.übergangen(stellen, {})

    assert übergangen is not None
    assert übergangen.stellen[gezogenes] != ziel
    assert übergangen.gründe == set()


def testOhneFliegenGiltBeimLoslassenDasZiehen(zehnZoll):
    boy, fremdes = modellMit(zehnZoll), modellMit(zehnZoll)
    ebene = {boy: stelleAn(5, 10)}
    stellen = {**ebene, fremdes: stelleAn(14, 10)}
    gezogen = Gezogen(ebene, boy, stelleAn(10, 10))
    phase = Bewegungsphase(ebene, spielfeld)

    beimZiehen = phase.stellenMitGründenNachDemZiehen(gezogen, stellen, {})
    beimLoslassen = phase.stellenMitGründenNachDemLoslassen(gezogen, stellen, {})

    assert beimLoslassen == beimZiehen


def testÜbergehenEinesFliegersGleitetNichtUndRücktNachHintenDerFremdenBase(zehnZoll):
    flieger, fremdes = modellMit(zehnZoll), modellMit(zehnZoll)
    ebene = {flieger: stelleAn(5, 10)}
    stellen = {**ebene, fremdes: stelleAn(14, 10)}
    phase = Bewegungsphase(ebene, spielfeld)
    phase.angebotNachDemZiehen(Gezogen(ebene, flieger, stelleAn(20, 10), fliegen=True), stellen, {})

    übergangen = phase.übergangen(stellen, {})

    assert übergangen is not None
    abstand = abstandsquadrat(übergangen.stellen[flieger], stellen[fremdes])
    assert abstand >= berührungsabstandImQuadrat
    assert übergangen.stellen[flieger].x > stelleAn(20, 10).x
    assert übergangen.gründe == set()
    assert übergangen.angehalten == {Grund.bewegungsweite}


def testÜbergehenEinesFliegersNenntAuchDieNahkampfreichweiteWennDieStelleDarinLiegt(zehnZoll):
    flieger, gegner = modellMit(zehnZoll), modellMit(zehnZoll)
    ebene = {flieger: stelleAn(10, 10)}
    stellen = {**ebene, gegner: stelleAn(31, 10)}
    phase = Bewegungsphase(ebene, spielfeld)
    phase.angebotNachDemZiehen(
        Gezogen(ebene, flieger, stelleAn(20, 10), fliegen=True), stellen, {gegner: stellen[gegner]}
    )

    übergangen = phase.übergangen(stellen, {gegner: stellen[gegner]})

    assert übergangen is not None
    assert übergangen.stellen[flieger] == stelleAn(20, 10)
    assert übergangen.angehalten == {Grund.bewegungsweite, Grund.nahkampfreichweite}
