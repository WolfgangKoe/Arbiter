"""BEW-17 · Anhalten vor fremden Bases."""

from fractions import Fraction
from http import HTTPStatus

import pytest

from tests.akzeptanz.anhalten import angehaltenVor, aufDerStrecke
from tests.akzeptanz.dienst import (
    eingabenDesWeiterrückens,
    eingabenNachDerAntwort,
    gezeigteStellen,
    mitDenEingabenLoslassen,
    modellLoslassen,
    stelleBeimLoslassenAbfragen,
    stelleBeimWeiterrückenAbfragen,
    stellenDerEinheitIm,
    zuvorNachDerAbfrage,
)
from tests.akzeptanz.handgriffe import versetzt, wegVon
from tests.akzeptanz.schlacht import (
    anhaltenUndÜbergehen,
    außerhalbDerNahkampfreichweite,
    bewegungsweite,
    hältAnDerBewegungsweite,
    hältAnDerSpielfeldkante,
    hältVorDerNahkampfreichweite,
    jetzigeStellen,
    zurBewegungsphaseDesNächstenZugs,
)
from tests.akzeptanz.ziehen import (
    WeitergereichteAbfragen,
    alsKörper,
    überEinenPunktZiehenUndLoslassen,
)

nichts = Fraction(0)
bewegungsweiteDesWarboss = bewegungsweite("Warboss", "Warboss")


def warbossÜbergehenBisZumZugDerNecrons(schlacht, warboss, stelle) -> None:
    (boss,) = warboss.modelle
    anhaltenUndÜbergehen(schlacht, boss, stelle)
    assert schlacht.stelle(boss) == stelle, "Der Warboss steht nicht, wo der Test ihn braucht"
    zurBewegungsphaseDesNächstenZugs(schlacht)


def testBew17_1DerDienstHältDasModellAufDerStreckeVorDerFremdenBaseAn(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, boyz
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    angestoßener, *_ = boyz.modelle
    davor, stelleDesAngestoßenen = schlacht.stelle(boss), schlacht.stelle(angestoßener)
    ziel = versetzt(davor, (Fraction(-5, 2), nichts))

    antwort = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, warboss, boss, ziel
    )

    (gezeigt,) = gezeigteStellen(antwort, "Warboss").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, davor, ziel)
    assert angehaltenVor(boss, gezeigt, angestoßener, stelleDesAngestoßenen)


def testBew17_1AmFreienZielZeigtDerDienstDasZielAuchWennDerWegÜberEineBaseFührt(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    erster, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(erster), (Fraction(9, 2), nichts))

    antwort = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, boyz, erster, ziel
    )

    assert antwort.status_code == HTTPStatus.OK
    assert gezeigteStellen(antwort, "Boyz") == {1: ziel}


def testBew17_1DerDienstHältAufDerStreckeAbDerZuvorGezeigtenStelleAn(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, boyz
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    _, _, _, angestoßener, *_ = boyz.modelle
    davor, stelleDesAngestoßenen = schlacht.stelle(boss), schlacht.stelle(angestoßener)
    zuvorGezeigt = versetzt(davor, (nichts, stelleDesAngestoßenen.y - davor.y))
    zuvor = zuvorNachDerAbfrage(dienstDerSchlacht, beendeteAufstellung, warboss, boss, zuvorGezeigt)
    eingaben = eingabenDesWeiterrückens(stelleDesAngestoßenen, zuvor)

    antwort = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, warboss, boss, eingaben
    )

    (gezeigt,) = gezeigteStellen(antwort, "Warboss").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, zuvorGezeigt, stelleDesAngestoßenen)
    assert angehaltenVor(boss, gezeigt, angestoßener, stelleDesAngestoßenen)


@pytest.mark.parametrize(
    "wegeVomWarboss",
    [
        (
            (Fraction(3, 2), Fraction(3, 2)),
            (Fraction(3, 4), Fraction(3, 4)),
            (Fraction(3, 4), Fraction(3, 2)),
        ),
        (
            (Fraction(3, 2), nichts),
            (Fraction(3, 4), Fraction(3, 4)),
            (Fraction(3, 2), Fraction(3, 4)),
        ),
        (
            (nichts, Fraction(3, 2)),
            (Fraction(3, 4), Fraction(3, 4)),
            (Fraction(3, 4), Fraction(3, 2)),
        ),
    ],
    ids=["beideTeileFreiWaagrecht", "nurSenkrechtFrei", "nurWaagrechtFrei"],
)
def testBew17_1DerDienstZeigtDasModellUmDenFreienTeilDesWegesVerschoben(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, spielerEins, wegeVomWarboss
):
    boyz, warboss, *_ = spielerEins.armee.einheiten
    (boss,) = warboss.modelle
    erster, *_ = boyz.modelle
    stelleDesWarboss = schlachtInDerBewegungsphase.stelle(boss)
    zuvorGezeigt, ziel, erwartet = (versetzt(stelleDesWarboss, weg) for weg in wegeVomWarboss)
    zuvor = zuvorNachDerAbfrage(dienstDerSchlacht, beendeteAufstellung, boyz, erster, zuvorGezeigt)
    eingaben = eingabenDesWeiterrückens(ziel, zuvor)

    antwort = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, boyz, erster, eingaben
    )

    assert antwort.status_code == HTTPStatus.OK
    assert gezeigteStellen(antwort, "Boyz") == {1: erwartet}


@pytest.mark.parametrize(
    "wegeVomWarboss",
    [
        ((Fraction(12, 5), nichts), (Fraction(1, 2), Fraction(6, 5))),
        ((Fraction(3, 2), nichts), (Fraction(3, 4), Fraction(-3, 4))),
    ],
    ids=["senkrechterTeilÜberDieBewegungsweite", "senkrechterTeilÜberDieSpielfeldkante"],
)
def testBew17_1HältArbiterAufDemFreienTeilAnZeigtDerDienstDasModellAufDerStrecke(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, spielerEins, wegeVomWarboss
):
    boyz, warboss, *_ = spielerEins.armee.einheiten
    (boss,) = warboss.modelle
    erster, *_ = boyz.modelle
    stelleDesWarboss = schlachtInDerBewegungsphase.stelle(boss)
    zuvorGezeigt, ziel = (versetzt(stelleDesWarboss, weg) for weg in wegeVomWarboss)
    zuvor = zuvorNachDerAbfrage(dienstDerSchlacht, beendeteAufstellung, boyz, erster, zuvorGezeigt)
    eingaben = eingabenDesWeiterrückens(ziel, zuvor)

    antwort = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, boyz, erster, eingaben
    )

    (gezeigt,) = gezeigteStellen(antwort, "Boyz").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, zuvorGezeigt, ziel)
    assert angehaltenVor(erster, gezeigt, boss, stelleDesWarboss)


def testBew17_1HältDieNahkampfreichweiteAufDemFreienTeilAnZeigtDerDienstDasModellAufDerStrecke(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, necronWarriors
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    *_, neunter, letzter = necronWarriors.modelle
    stelleDesNeunten = schlacht.stelle(neunter)
    zuvorGezeigt = versetzt(stelleDesNeunten, (Fraction(-2), nichts))
    ziel = versetzt(stelleDesNeunten, (Fraction(-1, 2), Fraction(1)))
    endeDesSenkrechtenTeils = versetzt(zuvorGezeigt, (nichts, Fraction(1)))
    stelleDesWarboss = versetzt(stelleDesNeunten, (Fraction(-4), Fraction(19, 10)))
    assert not außerhalbDerNahkampfreichweite(
        endeDesSenkrechtenTeils, letzter, stelleDesWarboss, boss
    ), "Der senkrechte Teil führt nicht in die Nahkampfreichweite des Warboss"
    warbossÜbergehenBisZumZugDerNecrons(schlacht, warboss, stelleDesWarboss)
    zuvor = zuvorNachDerAbfrage(
        dienstDerSchlacht, beendeteAufstellung, necronWarriors, letzter, zuvorGezeigt
    )
    eingaben = eingabenDesWeiterrückens(ziel, zuvor)

    antwort = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, necronWarriors, letzter, eingaben
    )

    (gezeigt,) = gezeigteStellen(antwort, "Necron Warriors").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, zuvorGezeigt, ziel)
    assert angehaltenVor(letzter, gezeigt, neunter, stelleDesNeunten)


def testBew17_1AlleinGezogenHältDerDienstVorDemModellDerselbenEinheitAn(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    schlacht = schlachtInDerBewegungsphase
    *_, angestoßener, gezogener = boyz.modelle
    stelleDesAngestoßenen = schlacht.stelle(angestoßener)
    zuvorGezeigt = versetzt(stelleDesAngestoßenen, (Fraction(2), nichts))
    ziel = versetzt(stelleDesAngestoßenen, (Fraction(1, 2), nichts))
    zuvor = zuvorNachDerAbfrage(
        dienstDerSchlacht, beendeteAufstellung, boyz, gezogener, zuvorGezeigt
    )
    eingaben = eingabenDesWeiterrückens(ziel, zuvor)

    antwort = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, boyz, gezogener, eingaben
    )

    (gezeigt,) = gezeigteStellen(antwort, "Boyz").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, zuvorGezeigt, ziel)
    assert angehaltenVor(gezogener, gezeigt, angestoßener, stelleDesAngestoßenen)


def testBew17_1IstDieGanzeEinheitEbeneHältDerDienstAlleIhreModelleGemeinsamAn(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, boyz
):
    schlacht = schlachtInDerBewegungsphase
    schlacht.auswählen(boyz)
    (boss,) = warboss.modelle
    erster, *_ = boyz.modelle
    davor = jetzigeStellen(schlacht, boyz)
    ziel = versetzt(davor[erster], (Fraction(5, 2), nichts))

    antwort = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, boyz, erster, ziel
    )

    gezeigt = gezeigteStellen(antwort, "Boyz")
    gezeigtesErstes, *_ = gezeigt.values()
    weg = wegVon(davor[erster], gezeigtesErstes)
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigtesErstes, davor[erster], ziel)
    assert angehaltenVor(erster, gezeigtesErstes, boss, schlacht.stelle(boss))
    assert gezeigt == {
        nummer: versetzt(stelle, weg) for nummer, stelle in enumerate(davor.values(), start=1)
    }


def testBew17_2NachDemAnhaltenSetztDerDienstDasModellWoDieZweiteAbfrageEsZeigte(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, boyz
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    _, _, _, angestoßener, *_ = boyz.modelle
    davor, stelleDesAngestoßenen = schlacht.stelle(boss), schlacht.stelle(angestoßener)
    zuvorGezeigt = versetzt(davor, (nichts, stelleDesAngestoßenen.y - davor.y))
    zuvor = zuvorNachDerAbfrage(dienstDerSchlacht, beendeteAufstellung, warboss, boss, zuvorGezeigt)
    eingaben = eingabenDesWeiterrückens(stelleDesAngestoßenen, zuvor)
    abgefragt = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, warboss, boss, eingaben
    )

    antwort = mitDenEingabenLoslassen(
        dienstDerSchlacht, beendeteAufstellung, warboss, boss, eingaben
    )

    assert antwort.status_code == HTTPStatus.OK
    assert "gründe" not in antwort.get_json()
    assert stellenDerEinheitIm(antwort.get_json(), "Warboss") == stellenDerEinheitIm(
        abgefragt.get_json(), "Warboss"
    )


def testBew17_2IstDieGanzeEinheitEbeneSetztDerDienstJedesIhrerModelleWoDieAbfrageSieZeigte(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    schlacht = schlachtInDerBewegungsphase
    schlacht.auswählen(boyz)
    erster, *_ = boyz.modelle
    ziel = versetzt(schlacht.stelle(erster), (Fraction(5, 2), nichts))
    abgefragt = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, boyz, erster, ziel
    )

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, boyz, erster, ziel)

    assert antwort.status_code == HTTPStatus.OK
    assert "gründe" not in antwort.get_json()
    assert stellenDerEinheitIm(antwort.get_json(), "Boyz") == stellenDerEinheitIm(
        abgefragt.get_json(), "Boyz"
    )


def testBew17_2DieSeiteSendetBeimLoslassenDieEingabenDerLetztenAbfrageMitAngehaltenAufDemWeg(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(boss)
    amBoy = versetzt(davor, (Fraction(-5, 2), nichts))
    danach = versetzt(davor, (Fraction(-1), Fraction(2)))
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)
    abfragen = WeitergereichteAbfragen(seite)

    körper = überEinenPunktZiehenUndLoslassen(seite, davor, amBoy, danach)

    *_, letzteEingaben = abfragen.eingaben
    assert körper == alsKörper(letzteEingaben)
    assert körper.get("angehaltenAufDemWeg") is True


def testBew17_3HältDieBewegungsweiteFrüherAnZeigtDerDienstDasModellAnIhr(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(boss)
    zuvorGezeigt = versetzt(davor, (nichts, Fraction(99, 20)))
    ziel = versetzt(zuvorGezeigt, (Fraction(-5, 2), nichts))
    zuvor = zuvorNachDerAbfrage(dienstDerSchlacht, beendeteAufstellung, warboss, boss, zuvorGezeigt)
    eingaben = eingabenDesWeiterrückens(ziel, zuvor)

    antwort = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, warboss, boss, eingaben
    )

    (gezeigt,) = gezeigteStellen(antwort, "Warboss").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, zuvorGezeigt, ziel)
    assert hältAnDerBewegungsweite(davor, gezeigt, bewegungsweiteDesWarboss)


def testBew17_3HältDieSpielfeldkanteFrüherAnZeigtDerDienstDasModellAnIhr(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, boyz
):
    (boss,) = warboss.modelle
    erster, *_ = boyz.modelle
    stelleDesWarboss = schlachtInDerBewegungsphase.stelle(boss)
    zuvorGezeigt = versetzt(stelleDesWarboss, (Fraction(2), Fraction(1, 2)))
    ziel = versetzt(stelleDesWarboss, (Fraction(1), Fraction(-9, 10)))
    zuvor = zuvorNachDerAbfrage(dienstDerSchlacht, beendeteAufstellung, boyz, erster, zuvorGezeigt)
    eingaben = eingabenDesWeiterrückens(ziel, zuvor)

    antwort = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, boyz, erster, eingaben
    )

    (gezeigt,) = gezeigteStellen(antwort, "Boyz").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, zuvorGezeigt, ziel)
    assert hältAnDerSpielfeldkante(gezeigt, erster)


def testBew17_3HältDieNahkampfreichweiteFrüherAnZeigtDerDienstDasModellVorIhr(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, necronWarriors
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    *_, neunter, letzter = necronWarriors.modelle
    davor, stelleDesNeunten = schlacht.stelle(letzter), schlacht.stelle(neunter)
    zuvorGezeigt = versetzt(davor, (Fraction(-1), Fraction(3)))
    ziel = versetzt(stelleDesNeunten, (Fraction(-1), Fraction(1, 2)))
    stelleDesWarboss = versetzt(davor, (Fraction(-16, 5), Fraction(1)))
    warbossÜbergehenBisZumZugDerNecrons(schlacht, warboss, stelleDesWarboss)
    zuvor = zuvorNachDerAbfrage(
        dienstDerSchlacht, beendeteAufstellung, necronWarriors, letzter, zuvorGezeigt
    )
    eingaben = eingabenDesWeiterrückens(ziel, zuvor)

    antwort = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, necronWarriors, letzter, eingaben
    )

    (gezeigt,) = gezeigteStellen(antwort, "Necron Warriors").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, zuvorGezeigt, ziel)
    assert hältVorDerNahkampfreichweite(gezeigt, letzter, stelleDesWarboss, boss)


def testBew17_4NachDemAnhaltenAufDemWegHältDerDienstAuchAbDerZuvorGezeigtenStelleAn(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, necronWarriors
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    *_, letzter = necronWarriors.modelle
    davor = schlacht.stelle(letzter)
    amNeuntenVorbei = versetzt(davor, (Fraction(-6, 5), Fraction(-1)))
    zuvorGezeigt = versetzt(davor, (Fraction(-6, 5), nichts))
    ziel = versetzt(zuvorGezeigt, (nichts, Fraction(4)))
    stelleDesWarboss = versetzt(zuvorGezeigt, (Fraction(-11, 5), Fraction(2)))
    warbossÜbergehenBisZumZugDerNecrons(schlacht, warboss, stelleDesWarboss)
    ersteAntwort = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, necronWarriors, letzter, amNeuntenVorbei
    )
    eingaben = eingabenNachDerAntwort(ersteAntwort, necronWarriors, letzter, ziel)

    antwort = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, necronWarriors, letzter, eingaben
    )

    (gezeigt,) = gezeigteStellen(antwort, "Necron Warriors").values()
    assert antwort.status_code == HTTPStatus.OK
    assert aufDerStrecke(gezeigt, zuvorGezeigt, ziel)
    assert hältVorDerNahkampfreichweite(gezeigt, letzter, stelleDesWarboss, boss)


def testBew17_4OhneAnhaltenAufDemWegHältDerDienstNichtAbDerZuvorGezeigtenStelleAn(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, necronWarriors
):
    schlacht = schlachtInDerBewegungsphase
    *_, letzter = necronWarriors.modelle
    zuvorGezeigt = versetzt(schlacht.stelle(letzter), (Fraction(-6, 5), nichts))
    ziel = versetzt(zuvorGezeigt, (nichts, Fraction(4)))
    stelleDesWarboss = versetzt(zuvorGezeigt, (Fraction(-11, 5), Fraction(2)))
    warbossÜbergehenBisZumZugDerNecrons(schlacht, warboss, stelleDesWarboss)
    ersteAntwort = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, necronWarriors, letzter, zuvorGezeigt
    )
    eingaben = eingabenNachDerAntwort(ersteAntwort, necronWarriors, letzter, ziel)

    antwort = stelleBeimWeiterrückenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, necronWarriors, letzter, eingaben
    )

    assert antwort.status_code == HTTPStatus.OK
    assert gezeigteStellen(antwort, "Necron Warriors") == {10: ziel}


def testBew17_4DieSeiteSchicktNachDemAnhaltenAufDemWegJederAbfrageAngehaltenAufDemWeg(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(boss)
    amBoy = versetzt(davor, (Fraction(-5, 2), nichts))
    danach = versetzt(davor, (Fraction(-1), Fraction(2)))
    seite = bildschirm.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)
    abfragen = WeitergereichteAbfragen(seite)

    überEinenPunktZiehenUndLoslassen(seite, davor, amBoy, danach)

    nannteEs = [
        antwort is not None and antwort.get("angehaltenAufDemWeg") is True
        for antwort in abfragen.letzte200VorJederAbfrage()
    ]
    assert any(nannteEs), "Keine Antwort nannte angehaltenAufDemWeg, der Warboss hielt nicht an"
    assert [eingaben.get("angehaltenAufDemWeg") == "true" for eingaben in abfragen.eingaben] == (
        nannteEs
    )
