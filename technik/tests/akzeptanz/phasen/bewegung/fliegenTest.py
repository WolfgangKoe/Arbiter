"""BEW-18 · Fliegen."""

import math
from fractions import Fraction
from http import HTTPStatus
from typing import NamedTuple

import pytest

from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import Weiterrücken
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle
from tests.akzeptanz.anhalten import aufDerStrecke, überdeckt
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    kreiseDerKarte,
    seiteDerSchlachtMitEingabe,
)
from tests.akzeptanz.dienst import (
    eingabenDesWeiterrückens,
    gezeigteStellen,
    körperDerStelle,
    stelleBeimWeiterrückenAbfragen,
    stelleImSpielstand,
)
from tests.akzeptanz.handgriffe import (
    breiteDesSpielfelds,
    millionstel,
    radiusInZoll,
    versetzt,
    wegVon,
)
from tests.akzeptanz.schlacht import (
    abstandImQuadrat,
    abständeZuDenSpielfeldkanten,
    angehaltenLoslassen,
    anhaltenUndÜbergehen,
    außerhalbDerNahkampfreichweite,
    bewegungsweite,
    hundertstelZoll,
    hältAnDerBewegungsweite,
    hältVorDerNahkampfreichweite,
    summeDerRadien,
    zurBewegungsphaseDesNächstenZugs,
)
from tests.akzeptanz.ziehen import halten, liegtEinPixelGenauAn, mitMausUndFinger, punktAufDerKarte

nichts = Fraction(0)
bewegungsweiteDerSpinne = bewegungsweite("Canoptek Spyder", "Canoptek Spyder")
knappNebenDerMitte = Fraction(1, 10)
hinterDerMitte = -knappNebenDerMitte
vorDerMitte = knappNebenDerMitte
halbesZoll = Fraction(1, 2)


def einheitMitDemNamen(spieler, name: str) -> Einheit:
    (einheit,) = (einheit for einheit in spieler.armee.einheiten if einheit.name == name)
    return einheit


def einheitDerSpinneUndWarrior(aufstellung) -> tuple[Einheit, Modell]:
    necrons = aufstellung.ausgangslage.zweiterSpieler
    *_, letzter = einheitMitDemNamen(necrons, "Necron Warriors").modelle
    return einheitMitDemNamen(necrons, "Canoptek Spyder"), letzter


@pytest.fixture
def einheitDerSpinne(spielerZwei) -> Einheit:
    return einheitMitDemNamen(spielerZwei, "Canoptek Spyder")


@pytest.fixture
def spinne(einheitDerSpinne) -> Modell:
    (modell,) = einheitDerSpinne.modelle
    return modell


@pytest.fixture
def weirdboy(spielerEins) -> Modell:
    (modell,) = einheitMitDemNamen(spielerEins, "Weirdboy").modelle
    return modell


@pytest.fixture
def warrior(necronWarriors) -> Modell:
    *_, letzter = necronWarriors.modelle
    return letzter


def warriorÜbergehen(schlacht, warrior: Modell, stelle: Stelle) -> Stelle:
    anhaltenUndÜbergehen(schlacht, warrior, stelle)
    assert schlacht.stelle(warrior) == stelle, "Der Warrior steht nicht, wo der Test ihn braucht"
    return stelle


def orksÜbergehenBisZumZugDerNecrons(schlacht, stellen: dict[Modell, Stelle]) -> None:
    for modell, stelle in stellen.items():
        anhaltenUndÜbergehen(schlacht, modell, stelle)
        assert schlacht.stelle(modell) == stelle, f"{modell.modellart} steht nicht am Ort des Tests"
    zurBewegungsphaseDesNächstenZugs(schlacht)


def frei(spinne: Modell, stelle: Stelle, anderes: Modell, stelleDesAnderen: Stelle) -> bool:
    return not überdeckt(spinne, stelle, anderes, stelleDesAnderen)


def höchstensUmHundertstelWeiter(punkt: Stelle, stelle: Stelle, kürzesterWeg: Fraction) -> bool:
    return abstandImQuadrat(punkt, stelle) <= (kürzesterWeg + hundertstelZoll) ** 2


def wurzelAufgerundet(quadrat: Fraction) -> Fraction:
    return Fraction(math.sqrt(quadrat)) + millionstel


def ganzImSpielfeld(stelle: Stelle, modell: Modell) -> bool:
    return all(abstand >= 0 for abstand in abständeZuDenSpielfeldkanten(stelle, modell))


class Kreis(NamedTuple):
    mitte: Stelle
    radius: Fraction


def schnittpunkte(kreis: Kreis, andererKreis: Kreis) -> tuple[Stelle, ...]:
    abstandImQuadratDerMitten = abstandImQuadrat(kreis.mitte, andererKreis.mitte)
    abstand = math.sqrt(abstandImQuadratDerMitten)
    entlang = float(kreis.radius**2 - andererKreis.radius**2 + abstandImQuadratDerMitten) / (
        2 * abstand
    )
    quer = math.sqrt(kreis.radius**2 - entlang**2)
    wegInX, wegInY = (float(teil) / abstand for teil in wegVon(kreis.mitte, andererKreis.mitte))
    return tuple(
        versetzt(
            kreis.mitte,
            (
                Fraction(entlang * wegInX - seite * quer * wegInY),
                Fraction(entlang * wegInY + seite * quer * wegInX),
            ),
        )
        for seite in (1, -1)
    )


def wegZumNächstenSchnitt(punkt: Stelle, kreis: Kreis, andererKreis: Kreis) -> Fraction:
    return wurzelAufgerundet(
        min(abstandImQuadrat(punkt, schnitt) for schnitt in schnittpunkte(kreis, andererKreis))
    )


def randDerNahkampfreichweite(modell: Modell, stelleDesAnderen: Stelle, anderes: Modell) -> Kreis:
    return Kreis(stelleDesAnderen, summeDerRadien(modell, anderes) + 1)


def stelleDesWarriorsHinterDerBewegungsweite(davor: Stelle) -> Stelle:
    return versetzt(davor, (-bewegungsweiteDerSpinne - halbesZoll, nichts))


def aufDemWarriorHinterDerBewegungsweiteLoslassen(
    schlacht, spinne: Modell, warrior: Modell, zurMitte: Fraction
) -> tuple[Stelle, Stelle]:
    davor = schlacht.stelle(spinne)
    stelleDesWarriors = warriorÜbergehen(
        schlacht, warrior, stelleDesWarriorsHinterDerBewegungsweite(davor)
    )
    punkt = versetzt(stelleDesWarriors, (zurMitte, nichts))
    angehaltenLoslassen(schlacht, spinne, punkt)
    return punkt, stelleDesWarriors


def aufDemWarriorHinterDerBewegungsweiteVorDemWarbossLoslassen(
    schlacht, spinne: Modell, warrior: Modell, boss: Modell
) -> tuple[Stelle, Stelle, Stelle]:
    davor = schlacht.stelle(spinne)
    stelleDesWarriors = stelleDesWarriorsHinterDerBewegungsweite(davor)
    stelleDesWarboss = versetzt(stelleDesWarriors, (-summeDerRadien(spinne, warrior) - 2, nichts))
    orksÜbergehenBisZumZugDerNecrons(schlacht, {boss: stelleDesWarboss})
    warriorÜbergehen(schlacht, warrior, stelleDesWarriors)
    punkt = versetzt(stelleDesWarriors, (hinterDerMitte, nichts))
    assert außerhalbDerNahkampfreichweite(punkt, spinne, stelleDesWarboss, boss), (
        "Der Punkt liegt in der Nahkampfreichweite des Warboss"
    )
    angehaltenLoslassen(schlacht, spinne, punkt)
    return punkt, stelleDesWarriors, stelleDesWarboss


def aufDemWarriorInDerNahkampfreichweiteLoslassen(
    schlacht, spinne: Modell, warrior: Modell, boss: Modell
) -> tuple[Stelle, Stelle, Stelle]:
    davor = schlacht.stelle(spinne)
    stelleDesWarriors = versetzt(davor, (Fraction(-3), Fraction(-3)))
    stelleDesWarboss = versetzt(stelleDesWarriors, (-summeDerRadien(spinne, warrior) - 1, nichts))
    orksÜbergehenBisZumZugDerNecrons(schlacht, {boss: stelleDesWarboss})
    warriorÜbergehen(schlacht, warrior, stelleDesWarriors)
    punkt = versetzt(stelleDesWarriors, (hinterDerMitte, knappNebenDerMitte))
    assert not außerhalbDerNahkampfreichweite(punkt, spinne, stelleDesWarboss, boss), (
        "Der Punkt liegt nicht in der Nahkampfreichweite des Warboss"
    )
    angehaltenLoslassen(schlacht, spinne, punkt)
    return punkt, stelleDesWarriors, stelleDesWarboss


def testBew18_1DieKarteZeigtDieSpinneÜberDerFremdenBaseAmPunkt(
    schlachtInDerBewegungsphaseDesZweitenSpielers, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    punkt = warriorÜbergehen(schlacht, warrior, versetzt(davor, (Fraction(-3), nichts)))

    gezeigt = schlacht.stellenBeimLoslassen(spinne, punkt)

    assert gezeigt.stellen == {spinne: punkt}
    assert gezeigt.angehaltenAufDemWeg is False


@pytest.mark.parametrize(
    "angehaltenAufDemWeg", [False, True], ids=["ohneAnhaltenAufDemWeg", "nachAnhaltenAufDemWeg"]
)
def testBew18_1AuchAbDerZuvorGezeigtenStelleZeigtDieKarteDieSpinneÜberDerFremdenBaseAmPunkt(
    schlachtInDerBewegungsphaseDesZweitenSpielers, spinne, warrior, angehaltenAufDemWeg
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    punkt = warriorÜbergehen(schlacht, warrior, versetzt(davor, (Fraction(-3), nichts)))
    weiter = Weiterrücken(versetzt(davor, (Fraction(-1), nichts)), angehaltenAufDemWeg)

    gezeigt = schlacht.stellenBeimLoslassen(spinne, punkt, weiter)

    assert gezeigt.stellen == {spinne: punkt}
    assert gezeigt.angehaltenAufDemWeg is False


def testBew18_1AnDerBewegungsweiteZeigtDieKarteDieSpinneAuchÜberDerFremdenBase(
    schlachtInDerBewegungsphaseDesZweitenSpielers, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    stelleDesWarriors = warriorÜbergehen(
        schlacht, warrior, versetzt(davor, (-bewegungsweiteDerSpinne, nichts))
    )
    punkt = versetzt(davor, (Fraction(-8), nichts))

    gezeigt = schlacht.stellenBeimLoslassen(spinne, punkt)

    (gezeigteStelle,) = gezeigt.stellen.values()
    assert aufDerStrecke(gezeigteStelle, davor, punkt)
    assert hältAnDerBewegungsweite(davor, gezeigteStelle, bewegungsweiteDerSpinne)
    assert überdeckt(spinne, gezeigteStelle, warrior, stelleDesWarriors)


@pytest.mark.parametrize(
    "zuvorUndAngehalten",
    [None, (Fraction(-1), False), (Fraction(-1), True)],
    ids=["ohneZuvor", "mitZuvor", "mitAngehaltenAufDemWeg"],
)
def testBew18_1DerDienstZeigtDieSpinneÜberDerFremdenBaseAmPunkt(
    dienstDerSchlacht,
    beendeteAufstellung,
    schlachtInDerBewegungsphaseDesZweitenSpielers,
    zuvorUndAngehalten,
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    einheitDerSpinne, warrior = einheitDerSpinneUndWarrior(beendeteAufstellung)
    (spinne,) = einheitDerSpinne.modelle
    davor = schlacht.stelle(spinne)
    punkt = warriorÜbergehen(schlacht, warrior, versetzt(davor, (Fraction(-3), nichts)))
    eingaben = körperDerStelle(punkt)
    if zuvorUndAngehalten is not None:
        wegNachZuvor, angehaltenAufDemWeg = zuvorUndAngehalten
        zuvor = stelleImSpielstand(versetzt(davor, (wegNachZuvor, nichts)))
        eingaben = eingabenDesWeiterrückens(punkt, zuvor)
        if angehaltenAufDemWeg:
            eingaben = {**eingaben, "angehaltenAufDemWeg": True}

    antwort = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, einheitDerSpinne, spinne, eingaben
    )

    assert antwort.status_code == HTTPStatus.OK
    assert gezeigteStellen(antwort, "Canoptek Spyder") == {1: punkt}
    assert antwort.get_json().get("angehaltenAufDemWeg", False) is False


def warbossAufDieStreckeÜbergehen(schlacht, spinne: Modell, boss: Modell) -> Stelle:
    davor = schlacht.stelle(spinne)
    stelleDesWarboss = versetzt(davor, (-bewegungsweiteDerSpinne / 2, nichts))
    orksÜbergehenBisZumZugDerNecrons(schlacht, {boss: stelleDesWarboss})
    punkt = versetzt(davor, (-bewegungsweiteDerSpinne, nichts))
    assert außerhalbDerNahkampfreichweite(punkt, spinne, stelleDesWarboss, boss), (
        "Der Punkt liegt in der Nahkampfreichweite des Warboss"
    )
    return punkt


def testBew18_1DieKarteZeigtDieSpinneÜberDieBaseDesWarbossHinwegAmPunkt(
    schlachtInDerBewegungsphase, spinne, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    punkt = warbossAufDieStreckeÜbergehen(schlacht, spinne, boss)

    gezeigt = schlacht.stellenBeimLoslassen(spinne, punkt)

    assert gezeigt.stellen == {spinne: punkt}
    assert gezeigt.angehaltenAufDemWeg is False


def testBew18_2AufDerFremdenBaseLosgelassenSetztArbiterDieSpinneAnDieNächsteFreieStelle(
    schlachtInDerBewegungsphaseDesZweitenSpielers, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    stelleDesWarriors = warriorÜbergehen(schlacht, warrior, versetzt(davor, (Fraction(-3), nichts)))
    punkt = versetzt(stelleDesWarriors, (-knappNebenDerMitte, nichts))
    kürzesterWeg = summeDerRadien(spinne, warrior) - knappNebenDerMitte

    schlacht.modellLoslassen(spinne, punkt)

    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert höchstensUmHundertstelWeiter(punkt, danach, kürzesterWeg)


def testBew18_2BeimRückenNenntArbiterKeinenGrund(
    schlachtInDerBewegungsphaseDesZweitenSpielers, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    stelleDesWarriors = warriorÜbergehen(schlacht, warrior, versetzt(davor, (Fraction(-3), nichts)))
    punkt = versetzt(stelleDesWarriors, (-knappNebenDerMitte, nichts))
    einträge = list(schlacht.protokoll)

    schlacht.modellLoslassen(spinne, punkt)

    assert schlacht.stelle(spinne).x < stelleDesWarriors.x, "Arbiter rückte die Spinne nicht"
    assert list(schlacht.protokoll) == einträge


def testBew18_2AnDerBewegungsweiteRücktArbiterDieSpinneNichtÜberSieHinaus(
    schlachtInDerBewegungsphaseDesZweitenSpielers, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    abstandDesWarriors = Fraction(5)
    stelleDesWarriors = warriorÜbergehen(
        schlacht, warrior, versetzt(davor, (-abstandDesWarriors, nichts))
    )
    punkt = versetzt(stelleDesWarriors, (-knappNebenDerMitte, nichts))
    zumSchnitt = wegZumNächstenSchnitt(
        punkt,
        Kreis(davor, bewegungsweiteDerSpinne),
        Kreis(stelleDesWarriors, summeDerRadien(spinne, warrior)),
    )

    schlacht.modellLoslassen(spinne, punkt)

    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert abstandImQuadrat(davor, danach) <= bewegungsweiteDerSpinne**2
    assert höchstensUmHundertstelWeiter(punkt, danach, zumSchnitt)


def testBew18_2AnDerBewegungsweiteAufDerFremdenBaseRücktArbiterDieSpinneVonDerGezeigtenStelle(
    schlachtInDerBewegungsphaseDesZweitenSpielers, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    stelleDesWarriors = warriorÜbergehen(
        schlacht, warrior, versetzt(davor, (-bewegungsweiteDerSpinne, nichts))
    )
    punkt = versetzt(davor, (Fraction(-8), nichts))
    (gezeigteStelle,) = schlacht.stellenBeimLoslassen(spinne, punkt).stellen.values()
    assert überdeckt(spinne, gezeigteStelle, warrior, stelleDesWarriors), (
        "Die Karte zeigt die Spinne an der Bewegungsweite nicht über dem Warrior"
    )
    kürzesterWeg = summeDerRadien(spinne, warrior) - (gezeigteStelle.x - stelleDesWarriors.x)

    schlacht.modellLoslassen(spinne, punkt)

    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert abstandImQuadrat(davor, danach) <= bewegungsweiteDerSpinne**2
    assert höchstensUmHundertstelWeiter(gezeigteStelle, danach, kürzesterWeg)


def testBew18_2AnDerSpielfeldkanteRücktArbiterDieSpinneGanzInDasSpielfeld(
    schlachtInDerBewegungsphaseDesZweitenSpielers, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    stelleDesWarriors = warriorÜbergehen(
        schlacht, warrior, Stelle(x=Fraction(breiteDesSpielfelds - 1), y=davor.y - 3)
    )
    punkt = versetzt(stelleDesWarriors, (knappNebenDerMitte, -knappNebenDerMitte))
    anDerKante = breiteDesSpielfelds - radiusInZoll(spinne)
    südlichAnDerKante = wurzelAufgerundet(
        summeDerRadien(spinne, warrior) ** 2 - (anDerKante - stelleDesWarriors.x) ** 2
    )
    zurKante = (punkt.x - anDerKante) ** 2 + (südlichAnDerKante - knappNebenDerMitte) ** 2

    schlacht.modellLoslassen(spinne, punkt)

    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert ganzImSpielfeld(danach, spinne)
    assert höchstensUmHundertstelWeiter(punkt, danach, wurzelAufgerundet(zurKante))


def testBew18_2NebenEinemModellDesAnderenSpielersRücktArbiterDieSpinneNichtInDieNahkampfreichweite(
    schlachtInDerBewegungsphase, spinne, warrior, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    davor = schlacht.stelle(spinne)
    summe = summeDerRadien(spinne, warrior)
    stelleDesWarriors = versetzt(davor, (Fraction(-3), Fraction(-3)))
    stelleDesWarboss = versetzt(stelleDesWarriors, (-summe - 2, nichts))
    orksÜbergehenBisZumZugDerNecrons(schlacht, {boss: stelleDesWarboss})
    warriorÜbergehen(schlacht, warrior, stelleDesWarriors)
    punkt = versetzt(stelleDesWarriors, (-knappNebenDerMitte, nichts))
    zurFreienStelle = wegZumNächstenSchnitt(
        punkt,
        Kreis(stelleDesWarriors, summe),
        randDerNahkampfreichweite(spinne, stelleDesWarboss, boss),
    )

    schlacht.modellLoslassen(spinne, punkt)

    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert außerhalbDerNahkampfreichweite(danach, spinne, stelleDesWarboss, boss)
    assert höchstensUmHundertstelWeiter(punkt, danach, zurFreienStelle)


@mitMausUndFinger
def testBew18_2DieKarteZeigtDieSpinneBeimHaltenÜberDerBaseUndDanachAnIhrerStelle(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphaseDesZweitenSpielers, eingabe
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    einheitDerSpinne, warrior = einheitDerSpinneUndWarrior(beendeteAufstellung)
    (spinne,) = einheitDerSpinne.modelle
    davor = schlacht.stelle(spinne)
    stelleDesWarriors = warriorÜbergehen(schlacht, warrior, versetzt(davor, (Fraction(-3), nichts)))
    punkt = versetzt(stelleDesWarriors, (Fraction(-1, 2), nichts))
    seite = seiteDerSchlachtMitEingabe(bildschirm, beendeteAufstellung, schlacht, eingabe)
    zeiger = halten(seite, davor, punkt, eingabe)
    beimHalten = [Stelle(x=Fraction(inX), y=Fraction(inY)) for inX, inY in kreiseDerKarte(seite)]

    with aufDieHandlungWarten(seite):
        zeiger.loslassen(punktAufDerKarte(seite, punkt))

    assert any(liegtEinPixelGenauAn(seite, kreis, punkt) for kreis in beimHalten)
    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert stelleImSpielstand(danach) in kreiseDerKarte(seite)


def testBew18_3DurchDieNahkampfreichweiteGezogenHältArbiterDieSpinneNichtAn(
    schlachtInDerBewegungsphase, spinne, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    davor = schlacht.stelle(spinne)
    stelleDesWarboss = versetzt(davor, (Fraction(-5, 2), Fraction(5, 2)))
    orksÜbergehenBisZumZugDerNecrons(schlacht, {boss: stelleDesWarboss})
    punkt = versetzt(davor, (Fraction(-5), nichts))

    schlacht.modellLoslassen(spinne, punkt)

    assert schlacht.stelle(spinne) == punkt
    assert not schlacht.gemeinsamÜbergehenAngeboten


def testBew18_3EndetDieStreckeInDerNahkampfreichweiteHältArbiterDieSpinneAnIhrerLetztenStelleDavor(
    schlachtInDerBewegungsphase, spinne, warboss, weirdboy
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    davor = schlacht.stelle(spinne)
    stelleDesWarboss = versetzt(davor, (-bewegungsweiteDerSpinne, Fraction(-5, 2)))
    stelleDesWeirdboys = versetzt(davor, (Fraction(-2), Fraction(13, 5)))
    orksÜbergehenBisZumZugDerNecrons(
        schlacht, {boss: stelleDesWarboss, weirdboy: stelleDesWeirdboys}
    )
    punkt = versetzt(davor, (-bewegungsweiteDerSpinne, nichts))

    schlacht.modellLoslassen(spinne, punkt)

    danach = schlacht.stelle(spinne)
    assert aufDerStrecke(danach, davor, punkt)
    assert hältVorDerNahkampfreichweite(danach, spinne, stelleDesWarboss, boss)
    assert außerhalbDerNahkampfreichweite(danach, spinne, stelleDesWeirdboys, weirdboy)


def testBew18_3DurchDieNahkampfreichweiteGezogenZeigtDieKarteDieSpinneAmPunkt(
    schlachtInDerBewegungsphase, spinne, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    davor = schlacht.stelle(spinne)
    stelleDesWarboss = versetzt(davor, (Fraction(-5, 2), Fraction(5, 2)))
    orksÜbergehenBisZumZugDerNecrons(schlacht, {boss: stelleDesWarboss})
    punkt = versetzt(davor, (Fraction(-5), nichts))

    gezeigt = schlacht.stellenBeimLoslassen(spinne, punkt)

    assert gezeigt.stellen == {spinne: punkt}


def testBew18_3EndetDieStreckeInDerNahkampfreichweiteZeigtDieKarteDieSpinneDavor(
    schlachtInDerBewegungsphase, spinne, warboss, weirdboy
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    davor = schlacht.stelle(spinne)
    stelleDesWarboss = versetzt(davor, (-bewegungsweiteDerSpinne, Fraction(-5, 2)))
    stelleDesWeirdboys = versetzt(davor, (Fraction(-2), Fraction(13, 5)))
    orksÜbergehenBisZumZugDerNecrons(
        schlacht, {boss: stelleDesWarboss, weirdboy: stelleDesWeirdboys}
    )
    punkt = versetzt(davor, (-bewegungsweiteDerSpinne, nichts))

    gezeigt = schlacht.stellenBeimLoslassen(spinne, punkt)

    (gezeigteStelle,) = gezeigt.stellen.values()
    assert aufDerStrecke(gezeigteStelle, davor, punkt)
    assert hältVorDerNahkampfreichweite(gezeigteStelle, spinne, stelleDesWarboss, boss)
    assert außerhalbDerNahkampfreichweite(gezeigteStelle, spinne, stelleDesWeirdboys, weirdboy)


def testBew18_3ÜberDieBaseDesWarbossHinwegGezogenSetztArbiterDieSpinneAmPunkt(
    schlachtInDerBewegungsphase, spinne, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    punkt = warbossAufDieStreckeÜbergehen(schlacht, spinne, boss)

    schlacht.modellLoslassen(spinne, punkt)

    assert schlacht.stelle(spinne) == punkt
    assert not schlacht.gemeinsamÜbergehenAngeboten


def anDerBewegungsweiteVorDemWarriorLoslassen(schlacht, spinne: Modell, warrior: Modell) -> Stelle:
    davor = schlacht.stelle(spinne)
    warriorÜbergehen(schlacht, warrior, versetzt(davor, (-bewegungsweiteDerSpinne, nichts)))
    punkt = versetzt(davor, (Fraction(-8), nichts))
    angehaltenLoslassen(schlacht, spinne, punkt)
    return punkt


def testBew18_7OhneFremdeBaseAmPunktSetztArbiterDieSpinneNachDemÜbergehenDorthin(
    schlachtInDerBewegungsphaseDesZweitenSpielers, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    punkt = anDerBewegungsweiteVorDemWarriorLoslassen(schlacht, spinne, warrior)

    schlacht.gemeinsamÜbergehen()

    assert schlacht.stelle(spinne) == punkt


def testBew18_7OhneFremdeBaseAmPunktNenntDerEintragDieBewegungsweite(
    schlachtInDerBewegungsphaseDesZweitenSpielers, einheitDerSpinne, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    anDerBewegungsweiteVorDemWarriorLoslassen(schlacht, spinne, warrior)
    einträge = list(schlacht.protokoll)

    schlacht.gemeinsamÜbergehen()

    *älter, neuer = schlacht.protokoll
    assert älter == einträge
    assert neuer.einheit is einheitDerSpinne
    assert neuer.gründe == {Grund.bewegungsweite}


def testBew18_7AufDerFremdenBaseRücktArbiterDieSpinneNachDemÜbergehenAuchÜberDieBewegungsweite(
    schlachtInDerBewegungsphaseDesZweitenSpielers, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    punkt, stelleDesWarriors = aufDemWarriorHinterDerBewegungsweiteLoslassen(
        schlacht, spinne, warrior, hinterDerMitte
    )
    kürzesterWeg = summeDerRadien(spinne, warrior) - knappNebenDerMitte

    schlacht.gemeinsamÜbergehen()

    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert abstandImQuadrat(davor, danach) > bewegungsweiteDerSpinne**2
    assert höchstensUmHundertstelWeiter(punkt, danach, kürzesterWeg)


def testBew18_7AufDerFremdenBaseRücktArbiterDieSpinneNachDemÜbergehenNichtInDieNahkampfreichweite(
    schlachtInDerBewegungsphase, spinne, warrior, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    punkt, stelleDesWarriors, stelleDesWarboss = (
        aufDemWarriorHinterDerBewegungsweiteVorDemWarbossLoslassen(schlacht, spinne, warrior, boss)
    )
    zurFreienStelle = wegZumNächstenSchnitt(
        punkt,
        Kreis(stelleDesWarriors, summeDerRadien(spinne, warrior)),
        randDerNahkampfreichweite(spinne, stelleDesWarboss, boss),
    )

    schlacht.gemeinsamÜbergehen()

    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert außerhalbDerNahkampfreichweite(danach, spinne, stelleDesWarboss, boss)
    assert höchstensUmHundertstelWeiter(punkt, danach, zurFreienStelle)


def testBew18_7NachDemRückenÜberDieBewegungsweiteNenntDerEintragDieBewegungsweite(
    schlachtInDerBewegungsphaseDesZweitenSpielers, einheitDerSpinne, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    aufDemWarriorHinterDerBewegungsweiteLoslassen(schlacht, spinne, warrior, hinterDerMitte)
    einträge = list(schlacht.protokoll)

    schlacht.gemeinsamÜbergehen()

    *älter, neuer = schlacht.protokoll
    assert älter == einträge
    assert neuer.einheit is einheitDerSpinne
    assert neuer.gründe == {Grund.bewegungsweite}


def testBew18_7NachDemRückenInDieBewegungsweiteNenntDerEintragKeinenGrund(
    schlachtInDerBewegungsphaseDesZweitenSpielers, einheitDerSpinne, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    aufDemWarriorHinterDerBewegungsweiteLoslassen(schlacht, spinne, warrior, vorDerMitte)
    einträge = list(schlacht.protokoll)

    schlacht.gemeinsamÜbergehen()

    assert abstandImQuadrat(davor, schlacht.stelle(spinne)) <= bewegungsweiteDerSpinne**2, (
        "Arbiter rückte die Spinne nicht in die Bewegungsweite"
    )
    *älter, neuer = schlacht.protokoll
    assert älter == einträge
    assert neuer.einheit is einheitDerSpinne
    assert neuer.gründe == set()


def testBew18_7NachDemÜbergehenDerNahkampfreichweiteRücktArbiterDieSpinneAusIhr(
    schlachtInDerBewegungsphase, spinne, warrior, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    punkt, stelleDesWarriors, stelleDesWarboss = aufDemWarriorInDerNahkampfreichweiteLoslassen(
        schlacht, spinne, warrior, boss
    )
    zurFreienStelle = wegZumNächstenSchnitt(
        punkt,
        Kreis(stelleDesWarriors, summeDerRadien(spinne, warrior)),
        randDerNahkampfreichweite(spinne, stelleDesWarboss, boss),
    )

    schlacht.gemeinsamÜbergehen()

    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert außerhalbDerNahkampfreichweite(danach, spinne, stelleDesWarboss, boss)
    assert höchstensUmHundertstelWeiter(punkt, danach, zurFreienStelle)


def testBew18_7NachDemRückenAusDerNahkampfreichweiteNenntDerEintragKeinenGrund(
    schlachtInDerBewegungsphase, einheitDerSpinne, spinne, warrior, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    aufDemWarriorInDerNahkampfreichweiteLoslassen(schlacht, spinne, warrior, boss)
    einträge = list(schlacht.protokoll)

    schlacht.gemeinsamÜbergehen()

    *älter, neuer = schlacht.protokoll
    assert älter == einträge
    assert neuer.einheit is einheitDerSpinne
    assert neuer.gründe == set()
