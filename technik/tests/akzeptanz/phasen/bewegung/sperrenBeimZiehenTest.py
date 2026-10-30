"""BEW-2 · Sperren beim Ziehen."""

from fractions import Fraction
from http import HTTPStatus

from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.bildschirm import (
    gründeAlsText,
    kreiseDerKarte,
    seiteDerSchlachtMitEingabe,
    sperrmeldungenDerSeite,
    sperrmeldungWarten,
)
from tests.akzeptanz.dienst import modellLoslassen, spielstandVon
from tests.akzeptanz.handgriffe import sperrgründe, versetzt
from tests.akzeptanz.schlacht import (
    abstandImQuadrat,
    aufeinanderZuZiehen,
    hältAnDerSpielfeldkante,
    hältVorDerNahkampfreichweite,
    jetzigeStellen,
    liegtAufDerGeradenVon,
    ostenUndNorden,
    schrägOhneHindernis,
    stellenAlsZahlen,
    stellenVersetzt,
    summeDerRadien,
)
from tests.akzeptanz.ziehen import halten, mitMausUndFinger, modellZiehen

nichts = Fraction(0)
dreiZoll = Fraction(3)
fünfZoll = Fraction(5)
nebenDerStrecke = (Fraction(3), Fraction(2))
schrägDieFremdeBaseStreifend = (Fraction(3), Fraction(4))
aufDieBoyz = (Fraction(-5, 2), nichts)


def nachOsten(zoll: Fraction) -> tuple[Fraction, Fraction]:
    return zoll, nichts


def gründeInDerReiheDesVertrags(gründe: set[Grund]) -> list[str]:
    return [grund.value for grund in Grund if grund in gründe]


def testBew2_5LiegtEineFremdeBaseAufDerStreckeIstDasModellMitDemGrundÜberEineBaseGesperrt(
    schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen, gezogenes, versetzt(davor, nachOsten(fünfZoll))
    )

    assert gründe == {Grund.überEineBase}
    assert schlachtInDerBewegungsphase.stelle(gezogenes) == davor


def testBew2_5LiegtKeineFremdeBaseAufDerStreckeGehtDasModellOhneSperre(
    schlachtInDerBewegungsphase, boyz
):
    _, _, drittes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(drittes), nachOsten(fünfZoll))

    schlachtInDerBewegungsphase.modellLoslassen(drittes, ziel)

    assert schlachtInDerBewegungsphase.stelle(drittes) == ziel


def testBew2_5LiegtEineFremdeBaseSchrägMittenAufDerStreckeIstDasModellÜberEineBaseGesperrt(
    schlachtInDerBewegungsphase, boyz
):
    *_, vorletztes, letztes = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(vorletztes)
    fremdeBase = versetzt(davor, nebenDerStrecke)
    schlachtInDerBewegungsphase.modellLoslassen(letztes, fremdeBase)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen,
        vorletztes,
        versetzt(davor, schrägDieFremdeBaseStreifend),
    )

    assert gründe == {Grund.überEineBase}
    assert schlachtInDerBewegungsphase.stelle(vorletztes) == davor


def testBew2_5IstDieEinheitNichtAusgewähltGiltAuchEinAnderesModellDerselbenEinheitAlsFremd(
    schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen, gezogenes, versetzt(davor, ostenUndNorden)
    )

    assert gründe == {Grund.überEineBase}
    assert schlachtInDerBewegungsphase.stelle(gezogenes) == davor


def testBew2_5IstDieGanzeEinheitEbeneGiltDieBaseEinerAnderenEinheitAlsFremd(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen,
        gezogenes,
        versetzt(davor[gezogenes], nachOsten(fünfZoll)),
    )

    assert gründe == {Grund.überEineBase}
    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor


def testBew2_5IstDieGanzeEinheitEbeneSperrtDieÜberEineBaseJedesModellsNichtNurDieDesGezogenen(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    _, _, drittes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen,
        drittes,
        versetzt(davor[drittes], nachOsten(fünfZoll)),
    )

    assert gründe == {Grund.überEineBase}
    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor


def testBew2_6NachDerSperreÜberEineBaseStehtJedesModellWieDavor(
    schlachtInDerBewegungsphase, boyz, warboss
):
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    davorWarboss = jetzigeStellen(schlachtInDerBewegungsphase, warboss)

    sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen,
        gezogenes,
        versetzt(davor[gezogenes], nachOsten(fünfZoll)),
    )

    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor
    assert jetzigeStellen(schlachtInDerBewegungsphase, warboss) == davorWarboss


def testBew2_6NachDerSperreÜberEineBaseStehtJedesModellDerGanzenEinheitWieDavor(
    schlachtInDerBewegungsphase, boyz, warboss
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    davorWarboss = jetzigeStellen(schlachtInDerBewegungsphase, warboss)

    sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen,
        gezogenes,
        versetzt(davor[gezogenes], nachOsten(fünfZoll)),
    )

    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor
    assert jetzigeStellen(schlachtInDerBewegungsphase, warboss) == davorWarboss


def testBew2_6SetztEinModellAufEineFremdeBaseNenntArbiterBaseÜberdecktUndÜberEineBase(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen, modell, versetzt(davor, aufDieBoyz)
    )

    assert gründe == {Grund.baseÜberdeckt, Grund.überEineBase}
    assert schlachtInDerBewegungsphase.stelle(modell) == davor


def testBew2_6DerDienstNenntBeiÜberEineBaseDenGrundUndDenStandWieDavor(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), nachOsten(fünfZoll))
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, boyz, gezogenes, ziel)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [Grund.überEineBase.value]
    assert antwort.get_json()["spielstand"] == spielstandDavor


def testBew2_6DerDienstNenntBeiEinerÜberdeckungBeideGründeInDerReiheVonGrundUndDenStandWieDavor(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), aufDieBoyz)
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, modell, ziel)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == gründeInDerReiheDesVertrags(
        {Grund.baseÜberdeckt, Grund.überEineBase}
    )
    assert antwort.get_json()["spielstand"] == spielstandDavor


@mitMausUndFinger
def testBew2_6DieSeiteNenntBeiÜberEineBaseDenGrundUndZeigtDasModellWieDavor(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, eingabe
):
    gezogenes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)
    ziel = versetzt(davor, nachOsten(fünfZoll))
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    modellZiehen(seite, davor, ziel, eingabe)

    assert sperrmeldungWarten(seite, {Grund.überEineBase}) == gründeAlsText({Grund.überEineBase})
    assert schlachtInDerBewegungsphase.stelle(gezogenes) == davor
    assert kreiseDerKarte(seite) == stellenAlsZahlen(schlachtInDerBewegungsphase)


@mitMausUndFinger
def testBew2_6DieSeiteNenntBeiEinerÜberdeckungBeideGründeUndZeigtDasModellWieDavor(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, eingabe
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    gründe = {Grund.baseÜberdeckt, Grund.überEineBase}
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    modellZiehen(seite, davor, versetzt(davor, aufDieBoyz), eingabe)

    assert sperrmeldungWarten(seite, gründe) == gründeAlsText(gründe)
    assert schlachtInDerBewegungsphase.stelle(modell) == davor
    assert kreiseDerKarte(seite) == stellenAlsZahlen(schlachtInDerBewegungsphase)


def testBew2_6DieSeiteNenntDenGrundNochWährendSieBeimNächstenZiehenNachDerStelleFragt(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, _, drittes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)
    davorDesDritten = schlachtInDerBewegungsphase.stelle(drittes)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    modellZiehen(seite, davor, versetzt(davor, nachOsten(fünfZoll)))
    sperrmeldungWarten(seite, {Grund.überEineBase})

    halten(seite, davorDesDritten, versetzt(davorDesDritten, nachOsten(dreiZoll)), "maus")

    assert sperrmeldungenDerSeite(seite) == [Grund.überEineBase.value]


def testBew2_6DieSeiteNenntDenGrundBisDieNächsteHandlungBeantwortetIst(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, _, drittes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)
    davorDesDritten = schlachtInDerBewegungsphase.stelle(drittes)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    modellZiehen(seite, davor, versetzt(davor, nachOsten(fünfZoll)))
    sperrmeldungWarten(seite, {Grund.überEineBase})

    modellZiehen(seite, davorDesDritten, versetzt(davorDesDritten, nachOsten(dreiZoll)))

    assert sperrmeldungWarten(seite, set()) == frozenset()


def testBew2_7IstDieGanzeEinheitEbeneSperrtDieÜberdeckungKeinModellWegenDerselbenEinheit(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], schrägOhneHindernis)

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel)

    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == stellenVersetzt(
        davor, schrägOhneHindernis
    )


def testBew2_8HältArbiterVorDerNahkampfreichweiteAnPrüftQue1NurDieStelleDesAnhaltens(
    schlachtInDerBewegungsphase, warboss, overlord
):
    (modell,) = warboss.modelle
    (modellDesAnderenSpielers,) = overlord.modelle
    aufeinanderZuZiehen(schlachtInDerBewegungsphase, modell, modellDesAnderenSpielers, dreiZoll)
    davor = schlachtInDerBewegungsphase.stelle(modell)
    stelleDesAnderen = schlachtInDerBewegungsphase.stelle(modellDesAnderenSpielers)
    aufDieBaseDesAnderen = Stelle(x=stelleDesAnderen.x, y=davor.y)
    assert abstandImQuadrat(aufDieBaseDesAnderen, stelleDesAnderen) < (
        summeDerRadien(modell, modellDesAnderenSpielers) ** 2
    )

    schlachtInDerBewegungsphase.modellLoslassen(modell, aufDieBaseDesAnderen)

    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert hältVorDerNahkampfreichweite(danach, modell, stelleDesAnderen, modellDesAnderenSpielers)
    assert liegtAufDerGeradenVon(davor, aufDieBaseDesAnderen, danach)


def testBew2_8HältArbiterAnDerKanteAnPrüfenQue1UndÜberEineBaseDieStelleUndDieStreckeBisDorthin(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    überDieBoyzZurKante = versetzt(davor, nachOsten(-fünfZoll))

    gründe = sperrgründe(schlachtInDerBewegungsphase.modellLoslassen, modell, überDieBoyzZurKante)

    assert gründe == {Grund.baseÜberdeckt, Grund.überEineBase}
    assert schlachtInDerBewegungsphase.stelle(modell) == davor


def testBew2_8GemeinsamÜbergehenSetztDasModellDorthinWoArbiterEsAnhält(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    überDieBoyzZurKante = versetzt(davor, nachOsten(-fünfZoll))
    gründe = sperrgründe(schlachtInDerBewegungsphase.modellLoslassen, modell, überDieBoyzZurKante)

    schlachtInDerBewegungsphase.modellLoslassen(modell, überDieBoyzZurKante, übergehen=gründe)

    danach = schlachtInDerBewegungsphase.stelle(modell)
    assert hältAnDerSpielfeldkante(danach, modell)
    assert liegtAufDerGeradenVon(davor, überDieBoyzZurKante, danach)
