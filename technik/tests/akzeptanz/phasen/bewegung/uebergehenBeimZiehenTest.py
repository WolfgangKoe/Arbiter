"""BEW-8 · Gemeinsam übergehen beim Ziehen."""

from fractions import Fraction
from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import Weiterrücken
from arbiter.domaene.sperre import Grund
from tests.akzeptanz.anhalten import angehaltenVor, aufDerStrecke
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    knopfDerSeite,
    kreiseDesSpielfelds,
    protokollDerSeite,
    protokollEinträge,
    seiteDerSchlachtMitEingabe,
    sperrmeldungenDerSeite,
    übergehenKnopf,
)
from tests.akzeptanz.dienst import (
    angehaltenDesVertrags,
    auswählen,
    dienstFürSchlacht,
    eingabenNachDerAntwort,
    gemeinsamÜbergehen,
    gezeigteStellen,
    kennungenDerEinheiten,
    mitDenEingabenLoslassen,
    modellLoslassen,
    schlachtNachSchlüsselnDes,
    spielstandVon,
    stelleBeimLoslassenAbfragen,
    stellenDerEinheitIm,
)
from tests.akzeptanz.handgriffe import sperrgründe, versetzt
from tests.akzeptanz.schlacht import (
    angehaltenLoslassen,
    anhaltenUndÜbergehen,
    aufeinanderZuZiehen,
    einModellAusDerKohärenzZiehen,
    hältAnDerSpielfeldkante,
    jetzigeStellen,
    liegtAufDerGeradenVon,
    stellenAlsZahlen,
    stellenVersetzt,
    warbossNebenDenBoyZiehen,
    warbossÜbergehenBisZumZugDerNecrons,
    zehnZollNachOsten,
    zurBewegungsphaseDerNächstenSchlachtrunde,
)
from tests.akzeptanz.ziehen import liegtEinPixelGenauAn, modellZiehen

nichts = Fraction(0)
dreiZoll = (Fraction(3), nichts)
fünfZollNachSüden = (nichts, Fraction(5))
zehnZollNachSüden = (nichts, Fraction(10))
schrägÜberDieNordkante = (Fraction(6), Fraction(-8))

vorDemOverlord = pytest.mark.parametrize(
    ("abstandUndWeg", "erwarteteGründe"),
    [
        ((Fraction(12), Fraction(8)), {"bewegungsweite"}),
        ((Fraction(3), Fraction(5, 2)), {"nahkampfreichweite"}),
        ((Fraction(7), Fraction(13, 2)), {"bewegungsweite", "nahkampfreichweite"}),
    ],
    ids=["bewegungsweite", "nahkampfreichweite", "beide"],
)


def vorDenOverlord(schlacht, warboss, overlord, abstand: Fraction):
    (boss,) = warboss.modelle
    (modellDesAnderenSpielers,) = overlord.modelle
    aufeinanderZuZiehen(schlacht, boss, modellDesAnderenSpielers, abstand)
    return boss


def namenDerGründe(eintrag) -> set[str]:
    return {grund.name for grund in eintrag.gründe}


@pytest.fixture
def warbossAngehalten(schlachtInDerBewegungsphase, warboss):
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    schlachtInDerBewegungsphase.modellLoslassen(boss, ziel)
    return boss, ziel


@pytest.mark.usefixtures("warbossAngehalten")
def testBew8_3HältBewegungsweiteEinModellAnBietetArbiterGemeinsamÜbergehenAn(
    schlachtInDerBewegungsphase,
):
    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is True


def testBew8_3HältDieNahkampfreichweiteEinModellAnBietetArbiterGemeinsamÜbergehenAn(
    schlachtInDerBewegungsphase, warboss, overlord
):
    boss = vorDenOverlord(schlachtInDerBewegungsphase, warboss, overlord, Fraction(3))
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), (Fraction(5, 2), nichts))

    schlachtInDerBewegungsphase.modellLoslassen(boss, ziel)

    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is True


def testBew8_3OhneAnhaltenBietetArbiterGemeinsamÜbergehenNichtAn(
    schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle

    schlachtInDerBewegungsphase.modellLoslassen(
        boss, versetzt(schlachtInDerBewegungsphase.stelle(boss), dreiZoll)
    )

    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is False


def testBew8_3HältDieSpielfeldkanteEinModellAnBietetArbiterGemeinsamÜbergehenNichtAn(
    schlachtInDerBewegungsphase, boyz
):
    *_, letzter = boyz.modelle

    schlachtInDerBewegungsphase.modellLoslassen(
        letzter, versetzt(schlachtInDerBewegungsphase.stelle(letzter), (Fraction(-3), nichts))
    )

    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is False


def testBew8_3HältEineFremdeBaseVorDerBewegungsweiteAnBietetArbiterGemeinsamÜbergehenNichtAn(
    schlachtInDerBewegungsphase, warboss, boyz
):
    schlacht = schlachtInDerBewegungsphase
    (boss,) = warboss.modelle
    _, gezogener, *_ = boyz.modelle
    davor = schlacht.stelle(gezogener)
    stelleDesWarboss = warbossNebenDenBoyZiehen(
        schlacht, warboss, gezogener, (Fraction(11, 2), nichts)
    )
    aufDemWarboss = versetzt(davor, (Fraction(13, 2), nichts))

    schlacht.modellLoslassen(gezogener, aufDemWarboss)

    assert angehaltenVor(gezogener, schlacht.stelle(gezogener), boss, stelleDesWarboss)
    assert schlacht.gemeinsamÜbergehenAngeboten is False


def testBew8_3HältNachDemAnhaltenAufDemWegDieNahkampfreichweiteBietetDerDienstGemeinsamÜbergehenAn(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, necronWarriors
):
    schlacht = schlachtInDerBewegungsphase
    *_, letzter = necronWarriors.modelle
    davor = schlacht.stelle(letzter)
    amNeuntenVorbei = versetzt(davor, (Fraction(-6, 5), Fraction(-1)))
    punkt = versetzt(davor, (Fraction(-6, 5), Fraction(4)))
    stelleDesWarboss = versetzt(davor, (Fraction(-17, 5), Fraction(2)))
    warbossÜbergehenBisZumZugDerNecrons(schlacht, warboss, stelleDesWarboss)
    ersteAntwort = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, necronWarriors, letzter, amNeuntenVorbei
    )
    assert ersteAntwort.get_json().get("angehaltenAufDemWeg") is True, "Davor hielt nichts an"
    eingaben = eingabenNachDerAntwort(ersteAntwort, necronWarriors, letzter, punkt)

    antwort = mitDenEingabenLoslassen(
        dienstDerSchlacht, beendeteAufstellung, necronWarriors, letzter, eingaben
    )

    assert antwort.status_code == HTTPStatus.OK
    assert "gründe" not in antwort.get_json()
    assert antwort.get_json()["schlacht"]["gemeinsamÜbergehen"] == {"angeboten": True}


def testBew8_3NachDemAnhaltenAufDemWegOhneAnhaltenBietetArbiterGemeinsamÜbergehenNichtAn(
    schlachtInDerBewegungsphaseDesZweitenSpielers, necronWarriors
):
    schlacht = schlachtInDerBewegungsphaseDesZweitenSpielers
    *_, letzter = necronWarriors.modelle
    davor = schlacht.stelle(letzter)
    amNeuntenVorbei = versetzt(davor, (Fraction(-6, 5), Fraction(-1)))
    punkt = versetzt(davor, (Fraction(-6, 5), Fraction(4)))
    gezeigt = schlacht.stellenBeimLoslassen(letzter, amNeuntenVorbei)
    assert gezeigt.angehaltenAufDemWeg is True, "Davor hielt nichts an"
    weiter = Weiterrücken(gezeigt.stellen[letzter], angehaltenAufDemWeg=True)

    schlacht.modellLoslassen(letzter, punkt, weiter)

    assert schlacht.stelle(letzter) == punkt
    assert schlacht.gemeinsamÜbergehenAngeboten is False


def testBew8_3ZuBeginnDerBewegungsphaseBietetArbiterGemeinsamÜbergehenNichtAn(
    schlachtInDerBewegungsphase,
):
    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is False


@pytest.mark.usefixtures("warbossAngehalten")
@pytest.mark.parametrize("handlung", ["loslassenOhneAnhalten", "phaseBeenden"])
def testBew8_3DieNächsteHandlungBeendetDasAngebot(schlachtInDerBewegungsphase, boyz, handlung):
    boy, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boy), dreiZoll)

    if handlung == "phaseBeenden":
        schlachtInDerBewegungsphase.phaseBeenden()
    else:
        schlachtInDerBewegungsphase.modellLoslassen(boy, ziel)

    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is False


@pytest.mark.usefixtures("warbossAngehalten")
@pytest.mark.parametrize("abfrage", ["auswählen", "stellenBeimLoslassen"])
def testBew8_3AuswählenUndAbfragenSindKeineHandlungUndLassenDasAngebot(
    schlachtInDerBewegungsphase, boyz, abfrage
):
    boy, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boy), dreiZoll)

    if abfrage == "auswählen":
        schlachtInDerBewegungsphase.auswählen(boyz)
    else:
        schlachtInDerBewegungsphase.stellenBeimLoslassen(boy, ziel)

    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is True


def testBew8_3EineSperreIstKeineHandlungUndLässtDasAngebot(
    schlachtInDerBewegungsphase, boyz, warboss
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)
    (boss,) = warboss.modelle
    angehaltenLoslassen(
        schlachtInDerBewegungsphase,
        boss,
        versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten),
    )

    gründe = sperrgründe(schlachtInDerBewegungsphase.phaseBeenden)

    assert gründe == {Grund.keineKohärenz}
    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is True


def testBew8_3DerDienstSetztAngehaltenWieDieAbfrageUndNenntDasAngebotOhneGrundWieImBeispiel(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    abfrage = stelleBeimLoslassenAbfragen(
        dienstDerSchlacht, beendeteAufstellung, warboss, boss, ziel
    )

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, boss, ziel)

    beispiel = angehaltenDesVertrags()["schlacht"]
    assert antwort.status_code == HTTPStatus.OK
    assert "gründe" not in antwort.get_json()
    assert schlachtNachSchlüsselnDes(antwort.get_json(), beispiel) == beispiel
    assert stellenDerEinheitIm(antwort.get_json(), "Warboss") == stellenDerEinheitIm(
        abfrage.get_json(), "Warboss"
    )


@pytest.mark.usefixtures("schlachtInDerBewegungsphase")
def testBew8_3DerDienstNenntZuBeginnDerBewegungsphaseKeinAngebot(dienstDerSchlacht):
    spielstand = spielstandVon(dienstDerSchlacht)

    assert spielstand["schlacht"]["gemeinsamÜbergehen"] == {"angeboten": False}


@pytest.mark.usefixtures("warbossAngehalten")
def testBew8_3DerDienstLässtDasAngebotBeimAuswählen(dienstDerSchlacht):
    auswählen(dienstDerSchlacht, "Boyz")

    spielstand = spielstandVon(dienstDerSchlacht)

    assert spielstand["schlacht"]["gemeinsamÜbergehen"] == {"angeboten": True}


def testBew8_3DieSeiteZeigtNachDemAnhaltenGemeinsamÜbergehenOhneSperrmeldung(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(boss)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    modellZiehen(seite, davor, versetzt(davor, zehnZollNachOsten))

    expect(knopfDerSeite(seite, übergehenKnopf)).to_be_visible()
    assert sperrmeldungenDerSeite(seite) == []


def testBew8_3DieSeiteZeigtOhneAnhaltenKeinGemeinsamÜbergehen(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(boss)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    modellZiehen(seite, davor, versetzt(davor, dreiZoll))

    expect(knopfDerSeite(seite, übergehenKnopf)).to_have_count(0)


def testBew8_4GemeinsamÜbergehenSetztDasModellAnDenPunktDesLoslassens(
    schlachtInDerBewegungsphase, warbossAngehalten
):
    boss, ziel = warbossAngehalten

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    assert schlachtInDerBewegungsphase.stelle(boss) == ziel
    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is False


def testBew8_4BeiDerEinheitenebeneRücktJedesModellUmDenWegZumPunkt(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    angehaltenLoslassen(
        schlachtInDerBewegungsphase, gezogenes, versetzt(davor[gezogenes], zehnZollNachSüden)
    )

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == stellenVersetzt(
        davor, zehnZollNachSüden
    )


def testBew8_4InDerNahkampfreichweiteSperrtArbiterBeimÜbergehenNicht(
    schlachtInDerBewegungsphase, warboss, overlord
):
    boss = vorDenOverlord(schlachtInDerBewegungsphase, warboss, overlord, Fraction(3))
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), (Fraction(5, 2), nichts))
    angehaltenLoslassen(schlachtInDerBewegungsphase, boss, ziel)

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    assert schlachtInDerBewegungsphase.stelle(boss) == ziel


def testBew8_4AnDerSpielfeldkanteHältArbiterDasModellAuchBeimÜbergehenAn(
    schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    südlich = versetzt(schlachtInDerBewegungsphase.stelle(boss), fünfZollNachSüden)
    schlachtInDerBewegungsphase.modellLoslassen(boss, südlich)
    zurBewegungsphaseDerNächstenSchlachtrunde(schlachtInDerBewegungsphase)
    ziel = versetzt(südlich, schrägÜberDieNordkante)
    angehaltenLoslassen(schlachtInDerBewegungsphase, boss, ziel)

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    danach = schlachtInDerBewegungsphase.stelle(boss)
    assert hältAnDerSpielfeldkante(danach, boss)
    assert liegtAufDerGeradenVon(südlich, ziel, danach)


def testBew8_4VorEinerFremdenBaseHältArbiterDasModellAuchBeimÜbergehenAufDerStreckeAn(
    schlachtInDerBewegungsphase, warboss, overlord
):
    boss = vorDenOverlord(schlachtInDerBewegungsphase, warboss, overlord, Fraction(7))
    (modellDesAnderenSpielers,) = overlord.modelle
    stelleDesOverlord = schlachtInDerBewegungsphase.stelle(modellDesAnderenSpielers)
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), (Fraction(8), nichts))
    angehaltenLoslassen(schlachtInDerBewegungsphase, boss, ziel)
    angehalten = schlachtInDerBewegungsphase.stelle(boss)

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    danach = schlachtInDerBewegungsphase.stelle(boss)
    assert aufDerStrecke(danach, angehalten, ziel)
    assert angehaltenVor(boss, danach, modellDesAnderenSpielers, stelleDesOverlord)
    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is False


@pytest.mark.parametrize("ohneAngebot", ["vorDemLoslassen", "nachDemÜbergehen"])
def testBew8_4OhneAngebotÄndertGemeinsamÜbergehenNichts(
    schlachtInDerBewegungsphase, warboss, ohneAngebot
):
    (boss,) = warboss.modelle
    if ohneAngebot == "nachDemÜbergehen":
        ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
        anhaltenUndÜbergehen(schlachtInDerBewegungsphase, boss, ziel)
    stellen = stellenAlsZahlen(schlachtInDerBewegungsphase)
    einträge = list(schlachtInDerBewegungsphase.protokoll)

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    assert stellenAlsZahlen(schlachtInDerBewegungsphase) == stellen
    assert list(schlachtInDerBewegungsphase.protokoll) == einträge


def testBew8_4DasAngebotGiltDenAngehaltenenModellenNichtDerAuswahlDanach(
    schlachtInDerBewegungsphase, warbossAngehalten, boyz
):
    boss, ziel = warbossAngehalten
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    schlachtInDerBewegungsphase.auswählen(boyz)

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    assert schlachtInDerBewegungsphase.stelle(boss) == ziel
    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor


def testBew8_4EinWeiteresAnhaltenErsetztDasAngebot(
    schlachtInDerBewegungsphase, warbossAngehalten, boyz
):
    boss, _ = warbossAngehalten
    angehaltenerBoss = schlachtInDerBewegungsphase.stelle(boss)
    *_, letzter = boyz.modelle
    zielDesBoys = versetzt(schlachtInDerBewegungsphase.stelle(letzter), zehnZollNachOsten)
    angehaltenLoslassen(schlachtInDerBewegungsphase, letzter, zielDesBoys)

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    assert schlachtInDerBewegungsphase.stelle(letzter) == zielDesBoys
    assert schlachtInDerBewegungsphase.stelle(boss) == angehaltenerBoss


def testBew8_4DerDienstSetztDasModellAnDenPunktUndBeendetDasAngebot(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, boss, ziel)

    antwort = gemeinsamÜbergehen(dienstDerSchlacht)

    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(antwort.get_json(), "Warboss") == {1: (float(ziel.x), float(ziel.y))}
    assert antwort.get_json()["schlacht"]["gemeinsamÜbergehen"] == {"angeboten": False}


def testBew8_4DerDienstÄndertBeimZweitenÜbergehenNichts(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, boss, ziel)
    davor = gemeinsamÜbergehen(dienstDerSchlacht).get_json()

    antwort = gemeinsamÜbergehen(dienstDerSchlacht)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == davor


def testBew8_4DerDienstSetztDasModellBeimÜbergehenVorDerFremdenBaseAufDerStrecke(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, overlord
):
    boss = vorDenOverlord(schlachtInDerBewegungsphase, warboss, overlord, Fraction(7))
    (modellDesAnderenSpielers,) = overlord.modelle
    stelleDesOverlord = schlachtInDerBewegungsphase.stelle(modellDesAnderenSpielers)
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), (Fraction(8), nichts))
    modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, boss, ziel)
    angehalten = schlachtInDerBewegungsphase.stelle(boss)

    antwort = gemeinsamÜbergehen(dienstDerSchlacht)

    assert antwort.status_code == HTTPStatus.OK
    (gesetzt,) = gezeigteStellen(antwort, "Warboss").values()
    assert aufDerStrecke(gesetzt, angehalten, ziel)
    assert angehaltenVor(boss, gesetzt, modellDesAnderenSpielers, stelleDesOverlord)
    assert antwort.get_json()["schlacht"]["gemeinsamÜbergehen"] == {"angeboten": False}


def testBew8_4DieSeiteSetztNachDemKlickAufGemeinsamÜbergehenAmPunkt(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(boss)
    ziel = versetzt(davor, zehnZollNachOsten)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    modellZiehen(seite, davor, ziel)

    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, übergehenKnopf).click()

    expect(knopfDerSeite(seite, übergehenKnopf)).to_have_count(0)
    assert liegtEinPixelGenauAn(seite, schlachtInDerBewegungsphase.stelle(boss), ziel)
    assert kreiseDesSpielfelds(seite) == stellenAlsZahlen(schlachtInDerBewegungsphase)


@vorDemOverlord
def testBew8_5DasProtokollHatEinenEintragMitDenGründenDesAnhaltens(
    schlachtInDerBewegungsphase, warboss, overlord, abstandUndWeg, erwarteteGründe
):
    abstand, weg = abstandUndWeg
    boss = vorDenOverlord(schlachtInDerBewegungsphase, warboss, overlord, abstand)
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), (weg, nichts))
    angehaltenLoslassen(schlachtInDerBewegungsphase, boss, ziel)

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    (eintrag,) = schlachtInDerBewegungsphase.protokoll
    assert namenDerGründe(eintrag) == erwarteteGründe


def testBew8_5DerEintragNenntDieEinheitUndIhrenSpieler(zugÜberDieBewegungsweite):
    schlacht, spieler, einheit, modell, ziel = zugÜberDieBewegungsweite
    angehaltenLoslassen(schlacht, modell, ziel)

    schlacht.gemeinsamÜbergehen()

    (eintrag,) = schlacht.protokoll
    assert eintrag.einheit is einheit
    assert eintrag.spieler is spieler
    assert eintrag.gründe == {Grund.bewegungsweite}


def testBew8_5JedesÜbergehenTrägtGenauEinenEintragMehrEinUndBehältDieÄlteren(
    schlachtInDerBewegungsphase, warboss, boyz
):
    (boss,) = warboss.modelle
    anhaltenUndÜbergehen(
        schlachtInDerBewegungsphase,
        boss,
        versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten),
    )
    (älterer,) = schlachtInDerBewegungsphase.protokoll
    *_, letzter = boyz.modelle
    angehaltenLoslassen(
        schlachtInDerBewegungsphase,
        letzter,
        versetzt(schlachtInDerBewegungsphase.stelle(letzter), zehnZollNachOsten),
    )

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    davor, neuer = schlachtInDerBewegungsphase.protokoll
    assert davor is älterer
    assert neuer.einheit is boyz


def testBew8_5DerDienstNenntDenEintragImSpielstand(beendeteAufstellung, zugÜberDieBewegungsweite):
    schlacht, _, einheit, modell, ziel = zugÜberDieBewegungsweite
    dienst = dienstFürSchlacht(beendeteAufstellung, schlacht)
    spielernummer, einheitennummer = kennungenDerEinheiten[einheit.name]
    modellLoslassen(dienst, beendeteAufstellung, einheit, modell, ziel)

    antwort = gemeinsamÜbergehen(dienst)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json()["schlacht"]["protokoll"] == [
        {
            "spieler": spielernummer,
            "einheit": einheitennummer,
            "name": einheit.name,
            "gründe": [Grund.bewegungsweite.value],
        }
    ]


def testBew8_5DieSeiteZeigtNachDemKlickAufGemeinsamÜbergehenDenEintrag(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(boss)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    modellZiehen(seite, davor, versetzt(davor, zehnZollNachOsten))

    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, übergehenKnopf).click()

    expect(protokollEinträge(seite)).to_have_count(1)
    assert protokollDerSeite(seite) == {
        ("Warboss", "Spieler 1", frozenset({Grund.bewegungsweite.value}))
    }
