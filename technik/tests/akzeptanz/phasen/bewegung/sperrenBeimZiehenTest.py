"""BEW-2 · Sperren beim Ziehen."""

from fractions import Fraction
from http import HTTPStatus

import pytest

from arbiter.domaene.sperre import Grund
from tests.akzeptanz.bildschirm import gründeAlsText, kreiseDerKarte, sperrmeldungWarten
from tests.akzeptanz.dienst import modellLoslassen, spielstandVon, weiterAlsBDesVertrags
from tests.akzeptanz.handgriffe import millionstel, schrägOhneWurzel, sperrgründe, versetzt
from tests.akzeptanz.schlacht import (
    bewegungsweite,
    jetzigeStellen,
    ostenUndNorden,
    schrägOhneHindernis,
    seiteDerSchlachtMitEingabe,
    stellenAlsZahlen,
    stellenVersetzt,
    zurBewegungsphaseDerNächstenSchlachtrunde,
)
from tests.akzeptanz.ziehen import mitMausUndFinger, modellZiehen

nichts = Fraction(0)
dreiZoll = Fraction(3)
fünfZoll = Fraction(5)


def nachOsten(zoll: Fraction) -> tuple[Fraction, Fraction]:
    return zoll, nichts


def nachNorden(zoll: Fraction) -> tuple[Fraction, Fraction]:
    return nichts, zoll


def schräg(strecke: Fraction) -> tuple[Fraction, Fraction]:
    """Ein Weg dieser Länge im Verhältnis 3 zu 4 nach Osten und Norden."""
    anteilX, anteilY = schrägOhneWurzel
    return anteilX * strecke, anteilY * strecke


def testBew2_1ZiehtEinModellGenauSoWeitWieSeinBGehtEsOhneSperre(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    ziel = versetzt(
        schlachtInDerBewegungsphase.stelle(modell), nachOsten(bewegungsweite("Warboss"))
    )

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    assert schlachtInDerBewegungsphase.stelle(modell) == ziel


def testBew2_1ZiehtEinModellWeiterAlsSeinBIstEsMitDemGrundWeiterAlsBGesperrt(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    weg = nachOsten(bewegungsweite("Warboss") + millionstel)

    gründe = sperrgründe(schlachtInDerBewegungsphase.modellLoslassen, modell, versetzt(davor, weg))

    assert gründe == {Grund.weiterAlsB}
    assert schlachtInDerBewegungsphase.stelle(modell) == davor
    assert schlachtInDerBewegungsphase.einheitInBewegung is None


def testBew2_1ZiehtEinModellSchrägGenauSoWeitWieSeinBGehtEsOhneSperre(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), schräg(bewegungsweite("Warboss")))

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel)

    assert schlachtInDerBewegungsphase.stelle(modell) == ziel


def testBew2_1ZiehtEinModellSchrägWeiterAlsSeinBIstEsMitDemGrundWeiterAlsBGesperrt(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    weg = schräg(bewegungsweite("Warboss") + millionstel)

    gründe = sperrgründe(schlachtInDerBewegungsphase.modellLoslassen, modell, versetzt(davor, weg))

    assert gründe == {Grund.weiterAlsB}
    assert schlachtInDerBewegungsphase.stelle(modell) == davor
    assert schlachtInDerBewegungsphase.einheitInBewegung is None


def testBew2_1JedesModellHatSeinEigenesB(schlachtInDerBewegungsphaseDesZweitenSpielers, overlord):
    (modell,) = overlord.modelle
    ziel = versetzt(
        schlachtInDerBewegungsphaseDesZweitenSpielers.stelle(modell),
        nachOsten(-bewegungsweite("Overlord")),
    )

    schlachtInDerBewegungsphaseDesZweitenSpielers.modellLoslassen(modell, ziel)

    assert schlachtInDerBewegungsphaseDesZweitenSpielers.stelle(modell) == ziel


@pytest.mark.parametrize(
    "zweiterSchritt",
    [nachOsten(dreiZoll), nachOsten(-dreiZoll)],
    ids=["inDieselbeRichtung", "zurück"],
)
def testBew2_1DieDistanzZähltJedeStelleSeitDemBeginnDerBewegungsphase(
    schlachtInDerBewegungsphase, warboss, zweiterSchritt
):
    (modell,) = warboss.modelle
    start = schlachtInDerBewegungsphase.stelle(modell)
    nachDemErstenSchritt = versetzt(start, nachOsten(dreiZoll))
    schlachtInDerBewegungsphase.modellLoslassen(modell, nachDemErstenSchritt)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen,
        modell,
        versetzt(nachDemErstenSchritt, zweiterSchritt),
    )

    assert gründe == {Grund.weiterAlsB}
    assert schlachtInDerBewegungsphase.stelle(modell) == nachDemErstenSchritt


def testBew2_1DieDistanzBeginntMitJederBewegungsphaseNeu(schlachtInDerBewegungsphase, warboss):
    (modell,) = warboss.modelle
    erstesZiel = versetzt(schlachtInDerBewegungsphase.stelle(modell), nachOsten(fünfZoll))
    schlachtInDerBewegungsphase.modellLoslassen(modell, erstesZiel)
    schlachtInDerBewegungsphase.bewegungDerEinheitBeenden()
    zurBewegungsphaseDerNächstenSchlachtrunde(schlachtInDerBewegungsphase)
    zweitesZiel = versetzt(erstesZiel, nachOsten(fünfZoll))

    schlachtInDerBewegungsphase.modellLoslassen(modell, zweitesZiel)

    assert schlachtInDerBewegungsphase.stelle(modell) == zweitesZiel


def testBew2_2LiegtEineFremdeBaseAufDerStreckeIstDasModellMitDemGrundÜberEineBaseGesperrt(
    schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen, gezogenes, versetzt(davor, nachOsten(fünfZoll))
    )

    assert gründe == {Grund.überEineBase}
    assert schlachtInDerBewegungsphase.stelle(gezogenes) == davor


def testBew2_2LiegtKeineFremdeBaseAufDerStreckeGehtDasModellOhneSperre(
    schlachtInDerBewegungsphase, boyz
):
    _, _, drittes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(drittes), nachOsten(fünfZoll))

    schlachtInDerBewegungsphase.modellLoslassen(drittes, ziel)

    assert schlachtInDerBewegungsphase.stelle(drittes) == ziel


def testBew2_2IstDieEinheitNichtAusgewähltGiltAuchEinAnderesModellDerselbenEinheitAlsFremd(
    schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen, gezogenes, versetzt(davor, ostenUndNorden)
    )

    assert gründe == {Grund.überEineBase}
    assert schlachtInDerBewegungsphase.stelle(gezogenes) == davor


def testBew2_2IstDieGanzeEinheitEbeneGiltDieBaseEinerAnderenEinheitAlsFremd(
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


def testBew2_3NachDerSperreWeiterAlsBStehtJedesModellDerGanzenEinheitWieDavor(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    weg = nachNorden(bewegungsweite("Boyz") + millionstel)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen, gezogenes, versetzt(davor[gezogenes], weg)
    )

    assert gründe == {Grund.weiterAlsB}
    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor
    assert schlachtInDerBewegungsphase.einheitInBewegung is None


def testBew2_3NachDerSperreÜberEineBaseStehtJedesModellWieDavor(
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
    assert schlachtInDerBewegungsphase.einheitInBewegung is None


def testBew2_3SetztEinModellAufEineFremdeBaseNenntArbiterBaseÜberdecktUndÜberEineBase(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    aufDieBoyz = versetzt(davor, nachOsten(Fraction(-5, 2)))

    gründe = sperrgründe(schlachtInDerBewegungsphase.modellLoslassen, modell, aufDieBoyz)

    assert gründe == {Grund.baseÜberdeckt, Grund.überEineBase}
    assert schlachtInDerBewegungsphase.stelle(modell) == davor
    assert schlachtInDerBewegungsphase.einheitInBewegung is None


def testBew2_3ZiehtEinModellÜberEineBaseUndWeiterAlsBNenntArbiterBeideGründe(
    schlachtInDerBewegungsphase, boyz, warboss
):
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    davorWarboss = jetzigeStellen(schlachtInDerBewegungsphase, warboss)
    weg = nachOsten(bewegungsweite("Boyz") + millionstel)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen, gezogenes, versetzt(davor[gezogenes], weg)
    )

    assert gründe == {Grund.weiterAlsB, Grund.überEineBase}
    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == davor
    assert jetzigeStellen(schlachtInDerBewegungsphase, warboss) == davorWarboss
    assert schlachtInDerBewegungsphase.einheitInBewegung is None


def testBew2_3DerDienstNenntBeiWeiterAlsBDenGrundWieDasBeispielImVertragUndDenStandWieDavor(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    ziel = versetzt(davor, nachOsten(bewegungsweite("Warboss") + millionstel))
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, modell, ziel)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == weiterAlsBDesVertrags()["gründe"]
    assert antwort.get_json()["spielstand"] == spielstandDavor


def testBew2_3DerDienstNenntBeiWeiterAlsBUndÜberEineBaseBeideGründeUndDenStandWieDavor(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)
    ziel = versetzt(davor, nachOsten(bewegungsweite("Boyz") + millionstel))
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, boyz, gezogenes, ziel)

    gründe = antwort.get_json()["gründe"]
    assert antwort.status_code == HTTPStatus.CONFLICT
    assert len(gründe) == len(frozenset(gründe))
    assert frozenset(gründe) == gründeAlsText({Grund.weiterAlsB, Grund.überEineBase})
    assert antwort.get_json()["spielstand"] == spielstandDavor


def testBew2_3DerDienstNenntBeiEinerÜberdeckungBaseÜberdecktUndÜberEineBaseUndDenStandWieDavor(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    aufDieBoyz = versetzt(davor, nachOsten(Fraction(-5, 2)))
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, modell, aufDieBoyz)

    gründe = antwort.get_json()["gründe"]
    assert antwort.status_code == HTTPStatus.CONFLICT
    assert len(gründe) == len(frozenset(gründe))
    assert frozenset(gründe) == gründeAlsText({Grund.baseÜberdeckt, Grund.überEineBase})
    assert antwort.get_json()["spielstand"] == spielstandDavor


@mitMausUndFinger
def testBew2_3DieSeiteNenntBeiWeiterAlsBDenGrundUndZeigtDasModellWieDavor(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, eingabe
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    ziel = versetzt(davor, nachOsten(bewegungsweite("Warboss") + 1))
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    modellZiehen(seite, davor, ziel, eingabe)

    assert sperrmeldungWarten(seite, {Grund.weiterAlsB}) == gründeAlsText({Grund.weiterAlsB})
    assert schlachtInDerBewegungsphase.stelle(modell) == davor
    assert kreiseDerKarte(seite) == stellenAlsZahlen(schlachtInDerBewegungsphase)


@mitMausUndFinger
def testBew2_3DieSeiteNenntBeiEinerÜberdeckungBeideGründeUndZeigtDasModellWieDavor(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, eingabe
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    aufDieBoyz = versetzt(davor, nachOsten(Fraction(-5, 2)))
    gründe = {Grund.baseÜberdeckt, Grund.überEineBase}
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, eingabe
    )

    modellZiehen(seite, davor, aufDieBoyz, eingabe)

    assert sperrmeldungWarten(seite, gründe) == gründeAlsText(gründe)
    assert schlachtInDerBewegungsphase.stelle(modell) == davor
    assert kreiseDerKarte(seite) == stellenAlsZahlen(schlachtInDerBewegungsphase)


def testBew2_3DieSeiteNenntDenGrundBisDieNächsteHandlungBeantwortetIst(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    zuWeit = versetzt(davor, nachOsten(bewegungsweite("Warboss") + 1))
    erlaubt = versetzt(davor, nachOsten(dreiZoll))
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    modellZiehen(seite, davor, zuWeit)
    sperrmeldungWarten(seite, {Grund.weiterAlsB})

    modellZiehen(seite, davor, erlaubt)

    assert sperrmeldungWarten(seite, set()) == frozenset()


def testBew2_4IstDieGanzeEinheitEbeneSperrtDieÜberdeckungKeinModellWegenDerselbenEinheit(
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
