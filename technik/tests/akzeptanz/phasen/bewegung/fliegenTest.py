"""BEW-18 · Fliegen."""

from fractions import Fraction
from http import HTTPStatus

import pytest

from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import Weiterrücken
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle
from tests.akzeptanz.anhalten import aufDerStrecke, überdeckt
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    kreiseDesSpielfelds,
    seiteDerSchlachtMitEingabe,
)
from tests.akzeptanz.dienst import (
    eingabenDesWeiterrückens,
    gezeigteStellen,
    körperDerStelle,
    stelleBeimWeiterrückenAbfragen,
    stelleImSpielstand,
)
from tests.akzeptanz.grenzen import dreiAugen
from tests.akzeptanz.handgriffe import breiteDesSpielfelds, gestreckt, radiusInZoll, versetzt
from tests.akzeptanz.ruecken import (
    Kreis,
    frei,
    ganzImSpielfeld,
    höchstensUmHundertstelWeiter,
    randDerNahkampfreichweite,
    wegZumNächstenSchnitt,
    wurzelAufgerundet,
)
from tests.akzeptanz.schlacht import (
    abstandImQuadrat,
    angehaltenLoslassen,
    anhaltenUndÜbergehen,
    außerhalbDerNahkampfreichweite,
    bewegungsweite,
    ersteStelleAnDerSpielfeldkante,
    hältAnDerBewegungsweite,
    hältVorDerNahkampfreichweite,
    orksÜbergehenBisZumZugDerNecrons,
    summeDerRadien,
)
from tests.akzeptanz.vorruecken import vorgerücktMit
from tests.akzeptanz.ziehen import (
    halten,
    liegtEinPixelGenauAn,
    mitMausUndFinger,
    punktAufDemSpielfeld,
)

nichts = Fraction(0)
bewegungsweiteDerSpinne = bewegungsweite("Canoptek Spyder", "Canoptek Spyder")
knappNebenDerMitte = Fraction(1, 10)
hinterDerMitte = -knappNebenDerMitte
vorDerMitte = knappNebenDerMitte
halbesZoll = Fraction(1, 2)
flachZurKante = (Fraction(7, 25), Fraction(24, 25))


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


def testBew18_1DasSpielfeldZeigtDieSpinneÜberDerFremdenBaseAmPunkt(
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
def testBew18_1AuchAbDerZuvorGezeigtenStelleZeigtDasSpielfeldDieSpinneÜberDerFremdenBaseAmPunkt(
    schlachtInDerBewegungsphaseDesZweitenSpielers, spinne, warrior, angehaltenAufDemWeg
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    punkt = warriorÜbergehen(schlacht, warrior, versetzt(davor, (Fraction(-3), nichts)))
    weiter = Weiterrücken(versetzt(davor, (Fraction(-1), nichts)), angehaltenAufDemWeg)

    gezeigt = schlacht.stellenBeimLoslassen(spinne, punkt, weiter)

    assert gezeigt.stellen == {spinne: punkt}
    assert gezeigt.angehaltenAufDemWeg is False


def testBew18_1AnDerBewegungsweiteZeigtDasSpielfeldDieSpinneAuchÜberDerFremdenBase(
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


def testBew18_1DasSpielfeldZeigtDieSpinneÜberDieBaseDesWarbossHinwegAmPunkt(
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


def testBew18_2NachDemVorrückenRücktArbiterDieSpinneBisAnBewegungsweitePlusVorrückwurf(
    schlachtInDerBewegungsphaseDesZweitenSpielers, einheitDerSpinne, spinne, warrior
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    davor = schlacht.stelle(spinne)
    weiteNachDemVorrücken = bewegungsweiteDerSpinne + dreiAugen
    stelleDesWarriors = warriorÜbergehen(
        schlacht, warrior, versetzt(davor, (-bewegungsweiteDerSpinne - 2, nichts))
    )
    vorgerücktMit(schlacht, einheitDerSpinne, dreiAugen)
    punkt = versetzt(stelleDesWarriors, (-knappNebenDerMitte, nichts))
    zumSchnitt = wegZumNächstenSchnitt(
        punkt,
        Kreis(davor, weiteNachDemVorrücken),
        Kreis(stelleDesWarriors, summeDerRadien(spinne, warrior)),
    )

    schlacht.modellLoslassen(spinne, punkt)

    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert abstandImQuadrat(davor, danach) <= weiteNachDemVorrücken**2
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
        "Das Spielfeld zeigt die Spinne an der Bewegungsweite nicht über dem Warrior"
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
        schlacht, warrior, Stelle(x=Fraction(breiteDesSpielfelds - 2), y=davor.y - 3)
    )
    punkt = versetzt(stelleDesWarriors, (1 + knappNebenDerMitte, -knappNebenDerMitte))
    (gezeigteStelle,) = schlacht.stellenBeimLoslassen(spinne, punkt).stellen.values()
    assert überdeckt(spinne, gezeigteStelle, warrior, stelleDesWarriors), (
        "Das Spielfeld zeigt die Spinne an der Spielfeldkante nicht über dem Warrior"
    )
    assert gezeigteStelle.x > stelleDesWarriors.x, (
        "Der Warrior drückt die Spinne nicht gegen die Spielfeldkante"
    )
    anDerKante = breiteDesSpielfelds - radiusInZoll(spinne)
    schnittAnDerKante = Stelle(
        x=anDerKante,
        y=stelleDesWarriors.y
        + wurzelAufgerundet(
            summeDerRadien(spinne, warrior) ** 2 - (anDerKante - stelleDesWarriors.x) ** 2
        ),
    )
    zurKante = wurzelAufgerundet(abstandImQuadrat(gezeigteStelle, schnittAnDerKante))

    schlacht.modellLoslassen(spinne, punkt)

    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert ganzImSpielfeld(danach, spinne)
    assert höchstensUmHundertstelWeiter(gezeigteStelle, danach, zurKante)


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
def testBew18_2DasSpielfeldZeigtDieSpinneBeimHaltenÜberDerBaseUndDanachAnIhrerStelle(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphaseDesZweitenSpielers, eingabe
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    einheitDerSpinne, warrior = einheitDerSpinneUndWarrior(beendeteAufstellung)
    (spinne,) = einheitDerSpinne.modelle
    davor = schlacht.stelle(spinne)
    stelleDesWarriors = warriorÜbergehen(schlacht, warrior, versetzt(davor, (Fraction(-3), nichts)))
    punkt = versetzt(stelleDesWarriors, (-halbesZoll, nichts))
    kürzesterWeg = summeDerRadien(spinne, warrior) - halbesZoll
    seite = seiteDerSchlachtMitEingabe(bildschirm, beendeteAufstellung, schlacht, eingabe)
    zeiger = halten(seite, davor, punkt, eingabe)
    beimHalten = [
        Stelle(x=Fraction(inX), y=Fraction(inY)) for inX, inY in kreiseDesSpielfelds(seite)
    ]

    with aufDieHandlungWarten(seite):
        zeiger.loslassen(punktAufDemSpielfeld(seite, punkt))

    assert any(liegtEinPixelGenauAn(seite, kreis, punkt) for kreis in beimHalten)
    danach = schlacht.stelle(spinne)
    assert frei(spinne, danach, warrior, stelleDesWarriors)
    assert höchstensUmHundertstelWeiter(punkt, danach, kürzesterWeg)
    assert stelleImSpielstand(danach) in kreiseDesSpielfelds(seite)


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


def testBew18_3EndetDieBewegungsweiteInDerNahkampfreichweiteHältArbiterDieSpinneDavor(
    schlachtInDerBewegungsphase, spinne, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    davor = schlacht.stelle(spinne)
    radien = summeDerRadien(spinne, boss)
    stelleDesWarboss = versetzt(davor, (-bewegungsweiteDerSpinne, radien + halbesZoll))
    orksÜbergehenBisZumZugDerNecrons(schlacht, {boss: stelleDesWarboss})
    punkt = versetzt(davor, (-bewegungsweiteDerSpinne - radien - Fraction(2), nichts))
    assert außerhalbDerNahkampfreichweite(punkt, spinne, stelleDesWarboss, boss), (
        "Der Punkt liegt in der Nahkampfreichweite des Warboss"
    )

    schlacht.modellLoslassen(spinne, punkt)

    danach = schlacht.stelle(spinne)
    assert aufDerStrecke(danach, davor, punkt)
    assert hältVorDerNahkampfreichweite(danach, spinne, stelleDesWarboss, boss)


def testBew18_3EndetDieStreckeAnDerSpielfeldkanteInDerNahkampfreichweiteHältArbiterDieSpinneDavor(
    schlachtInDerBewegungsphase, spinne, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    davor = schlacht.stelle(spinne)
    stelleDesWarboss = versetzt(davor, (Fraction(-23, 10), Fraction(11, 5)))
    orksÜbergehenBisZumZugDerNecrons(schlacht, {boss: stelleDesWarboss})
    nachDerBewegungsweite = versetzt(davor, gestreckt(flachZurKante, bewegungsweiteDerSpinne))
    punkt = versetzt(davor, gestreckt(flachZurKante, bewegungsweiteDerSpinne + 2))
    anDerKante = ersteStelleAnDerSpielfeldkante(davor, punkt, spinne)
    assert außerhalbDerNahkampfreichweite(davor, spinne, stelleDesWarboss, boss), (
        "Die Anfangsstelle liegt in der Nahkampfreichweite des Warboss"
    )
    assert außerhalbDerNahkampfreichweite(nachDerBewegungsweite, spinne, stelleDesWarboss, boss), (
        "Der Punkt nach der Bewegungsweite liegt in der Nahkampfreichweite des Warboss"
    )
    assert not außerhalbDerNahkampfreichweite(anDerKante, spinne, stelleDesWarboss, boss), (
        "Die letzte Stelle an der Spielfeldkante liegt außerhalb der Nahkampfreichweite des Warboss"
    )

    schlacht.modellLoslassen(spinne, punkt)

    danach = schlacht.stelle(spinne)
    assert aufDerStrecke(danach, davor, punkt)
    assert hältVorDerNahkampfreichweite(danach, spinne, stelleDesWarboss, boss)


def testBew18_3DurchDieNahkampfreichweiteGezogenZeigtDasSpielfeldDieSpinneAmPunkt(
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


def testBew18_3EndetDieStreckeInDerNahkampfreichweiteZeigtDasSpielfeldDieSpinneDavor(
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


def inDerNahkampfreichweiteDesWarbossLoslassen(
    schlacht, spinne: Modell, boss: Modell, wegNachWesten: Fraction
) -> Stelle:
    davor = schlacht.stelle(spinne)
    punkt = versetzt(davor, (-wegNachWesten, nichts))
    stelleDesWarboss = versetzt(punkt, (-summeDerRadien(spinne, boss) - halbesZoll, nichts))
    orksÜbergehenBisZumZugDerNecrons(schlacht, {boss: stelleDesWarboss})
    angehaltenLoslassen(schlacht, spinne, punkt)
    return punkt


def testBew18_7OhneFremdeBaseInDerNahkampfreichweiteNenntDerEintragBeideGründe(
    schlachtInDerBewegungsphase, einheitDerSpinne, spinne, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    punkt = inDerNahkampfreichweiteDesWarbossLoslassen(schlacht, spinne, boss, Fraction(8))
    einträge = list(schlacht.protokoll)

    schlacht.gemeinsamÜbergehen()

    assert schlacht.stelle(spinne) == punkt, "Die Spinne steht nicht in der Nahkampfreichweite"
    *älter, neuer = schlacht.protokoll
    assert älter == einträge
    assert neuer.einheit is einheitDerSpinne
    assert neuer.gründe == {Grund.bewegungsweite, Grund.nahkampfreichweite}


def testBew18_7InDerBewegungsweiteInDerNahkampfreichweiteNenntDerEintragNurDieNahkampfreichweite(
    schlachtInDerBewegungsphase, einheitDerSpinne, spinne, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    punkt = inDerNahkampfreichweiteDesWarbossLoslassen(schlacht, spinne, boss, Fraction(5))
    einträge = list(schlacht.protokoll)

    schlacht.gemeinsamÜbergehen()

    assert schlacht.stelle(spinne) == punkt, "Die Spinne steht nicht in der Nahkampfreichweite"
    *älter, neuer = schlacht.protokoll
    assert älter == einträge
    assert neuer.einheit is einheitDerSpinne
    assert neuer.gründe == {Grund.nahkampfreichweite}


def testBew18_7HinterDerBewegungsweiteDurchDieNahkampfreichweiteNenntDerEintragNurDieBewegungsweite(
    schlachtInDerBewegungsphase, einheitDerSpinne, spinne, warboss
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    davor = schlacht.stelle(spinne)
    wegZurMitte = bewegungsweiteDerSpinne + Fraction(5, 2)
    stelleDesWarboss = versetzt(davor, (-wegZurMitte, Fraction(2)))
    orksÜbergehenBisZumZugDerNecrons(schlacht, {boss: stelleDesWarboss})
    mitte = versetzt(davor, (-wegZurMitte, nichts))
    punkt = versetzt(mitte, (Fraction(-5, 2), nichts))
    assert außerhalbDerNahkampfreichweite(punkt, spinne, stelleDesWarboss, boss)
    assert not außerhalbDerNahkampfreichweite(mitte, spinne, stelleDesWarboss, boss)
    angehaltenLoslassen(schlacht, spinne, punkt)
    einträge = list(schlacht.protokoll)

    schlacht.gemeinsamÜbergehen()

    assert schlacht.stelle(spinne) == punkt
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
