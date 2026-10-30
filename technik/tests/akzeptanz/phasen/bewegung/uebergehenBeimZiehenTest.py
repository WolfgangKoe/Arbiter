"""BEW-8 · Gemeinsam übergehen beim Ziehen."""

from fractions import Fraction
from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from arbiter.domaene.sperre import Grund
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    gründeAlsText,
    knopfDerSeite,
    kreiseDerKarte,
    seiteDerSchlachtMitEingabe,
    sperrmeldungWarten,
    übergehenKnopf,
)
from tests.akzeptanz.dienst import (
    modellLoslassen,
    modellLoslassenUndÜbergehen,
    schlachtNachSchlüsselnDes,
    spielstandVon,
    übergehbarDesVertrags,
)
from tests.akzeptanz.handgriffe import sperreBei, sperrgründe, versetzt
from tests.akzeptanz.schlacht import (
    fünfZollNachOsten,
    hältAnDerBewegungsweite,
    jetzigeStellen,
    liegtAufDerGeradenVon,
    stellenAlsZahlen,
    stellenVersetzt,
)
from tests.akzeptanz.ziehen import liegtEinPixelGenauAn, modellZiehen

achtZollNachOsten = (Fraction(8), Fraction(0))
dreiZollNachOsten = (Fraction(3), Fraction(0))
aufDieBoyz = (Fraction(-5, 2), Fraction(0))
beideGründe = frozenset({Grund.baseÜberdeckt, Grund.überEineBase})


def testBew8_1EineSperreÜberEineBaseBietetGemeinsamÜbergehenAn(schlachtInDerBewegungsphase, boyz):
    gezogenes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), fünfZollNachOsten)

    sperre = sperreBei(schlachtInDerBewegungsphase.modellLoslassen, gezogenes, ziel)

    assert sperre.gründe == {Grund.überEineBase}
    assert sperre.übergehbar is True


def testBew8_1EineSperreNachQue1BietetGemeinsamÜbergehenAn(schlachtInDerBewegungsphase, warboss):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), aufDieBoyz)

    sperre = sperreBei(schlachtInDerBewegungsphase.modellLoslassen, modell, ziel)

    assert sperre.gründe == beideGründe
    assert sperre.übergehbar is True


def testBew8_1DerDienstBietetBeiÜberEineBaseGemeinsamÜbergehenAnWieImBeispiel(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), fünfZollNachOsten)
    beispiel = übergehbarDesVertrags()

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, boyz, gezogenes, ziel)

    assert antwort.status_code == HTTPStatus.CONFLICT
    körper = antwort.get_json()
    assert körper["gründe"] == beispiel["gründe"]
    assert körper["übergehbar"] == beispiel["übergehbar"]
    schlachtDesBeispiels = beispiel["spielstand"]["schlacht"]
    assert schlachtNachSchlüsselnDes(körper["spielstand"], schlachtDesBeispiels) == (
        schlachtDesBeispiels
    )


def testBew8_1DieSeiteBietetGemeinsamÜbergehenAnSolangeSieDenGrundNennt(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    modellZiehen(seite, davor, versetzt(davor, fünfZollNachOsten))

    assert sperrmeldungWarten(seite, {Grund.überEineBase}) == gründeAlsText({Grund.überEineBase})
    expect(knopfDerSeite(seite, übergehenKnopf)).to_be_visible()


def testBew8_1NachDerNächstenHandlungOhneSperreBietetDieSeiteGemeinsamÜbergehenNichtMehrAn(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, _, drittes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)
    davorDesDritten = schlachtInDerBewegungsphase.stelle(drittes)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    modellZiehen(seite, davor, versetzt(davor, fünfZollNachOsten))
    sperrmeldungWarten(seite, {Grund.überEineBase})
    expect(knopfDerSeite(seite, übergehenKnopf)).to_be_visible()

    modellZiehen(seite, davorDesDritten, versetzt(davorDesDritten, dreiZollNachOsten))

    assert sperrmeldungWarten(seite, set()) == frozenset()
    expect(knopfDerSeite(seite, übergehenKnopf)).to_have_count(0)


def testBew8_2GemeinsamÜbergehenSetztDasGezogeneModellAnDieGezogeneStelle(
    schlachtInDerBewegungsphase, boyz, warboss
):
    gezogenes, *andere = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), fünfZollNachOsten)
    davorDerAnderen = {modell: schlachtInDerBewegungsphase.stelle(modell) for modell in andere}
    davorWarboss = jetzigeStellen(schlachtInDerBewegungsphase, warboss)
    gründe = sperrgründe(schlachtInDerBewegungsphase.modellLoslassen, gezogenes, ziel)

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel, übergehen=gründe)

    assert schlachtInDerBewegungsphase.stelle(gezogenes) == ziel
    assert {
        modell: schlachtInDerBewegungsphase.stelle(modell) for modell in andere
    } == davorDerAnderen
    assert jetzigeStellen(schlachtInDerBewegungsphase, warboss) == davorWarboss


def testBew8_2IstDieGanzeEinheitEbeneSetztGemeinsamÜbergehenJedesModellUmDieselbeStrecke(
    schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    gezogenes, *_ = boyz.modelle
    davor = jetzigeStellen(schlachtInDerBewegungsphase, boyz)
    ziel = versetzt(davor[gezogenes], fünfZollNachOsten)
    gründe = sperrgründe(schlachtInDerBewegungsphase.modellLoslassen, gezogenes, ziel)

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel, übergehen=gründe)

    assert jetzigeStellen(schlachtInDerBewegungsphase, boyz) == stellenVersetzt(
        davor, fünfZollNachOsten
    )


def testBew8_2HältBew3DasModellAnSetztGemeinsamÜbergehenEsDortWoBew3EsAnhält(
    schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)
    ziel = versetzt(davor, achtZollNachOsten)
    gründe = sperrgründe(schlachtInDerBewegungsphase.modellLoslassen, gezogenes, ziel)

    schlachtInDerBewegungsphase.modellLoslassen(gezogenes, ziel, übergehen=gründe)

    danach = schlachtInDerBewegungsphase.stelle(gezogenes)
    assert gründe == {Grund.überEineBase}
    assert hältAnDerBewegungsweite(davor, danach, gezogenes.bewegungsweite)
    assert liegtAufDerGeradenVon(davor, ziel, danach)


def testBew8_2GemeinsamÜbergehenSetztBeiBaseÜberdecktUndÜberEineBaseAnDieGezogeneStelle(
    schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), aufDieBoyz)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel, übergehen=beideGründe)

    assert schlachtInDerBewegungsphase.stelle(modell) == ziel


@pytest.mark.parametrize(
    "übergangen",
    [frozenset({Grund.überEineBase}), frozenset({Grund.baseÜberdeckt})],
    ids=["nurÜberEineBase", "nurBaseÜberdeckt"],
)
def testBew8_2ÜbergehenOhneJedenGrundDerSperreSperrtMitAllenGründenUndLässtDenStand(
    schlachtInDerBewegungsphase, warboss, übergangen
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    ziel = versetzt(davor, aufDieBoyz)

    gründe = sperrgründe(
        schlachtInDerBewegungsphase.modellLoslassen, modell, ziel, übergehen=übergangen
    )

    assert gründe == beideGründe
    assert schlachtInDerBewegungsphase.stelle(modell) == davor
    assert list(schlachtInDerBewegungsphase.protokoll) == []


def testBew8_2DerDienstSetztMitÜbergehenWieOhneSperre(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), fünfZollNachOsten)
    modellLoslassen(dienstDerSchlacht, beendeteAufstellung, boyz, gezogenes, ziel)

    antwort = modellLoslassenUndÜbergehen(
        dienstDerSchlacht, beendeteAufstellung, gezogenes, ziel, {Grund.überEineBase}
    )

    assert antwort.status_code == HTTPStatus.OK
    assert schlachtInDerBewegungsphase.stelle(gezogenes) == ziel
    assert antwort.get_json() == spielstandVon(dienstDerSchlacht)


def testBew8_2DerDienstSperrtMitEinemGrundAußerhalbVonÜbergehenUndLässtDenStand(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (modell,) = warboss.modelle
    davor = schlachtInDerBewegungsphase.stelle(modell)
    ziel = versetzt(davor, aufDieBoyz)
    spielstandDavor = spielstandVon(dienstDerSchlacht)

    antwort = modellLoslassenUndÜbergehen(
        dienstDerSchlacht, beendeteAufstellung, modell, ziel, {Grund.überEineBase}
    )

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [Grund.baseÜberdeckt.value, Grund.überEineBase.value]
    assert antwort.get_json()["spielstand"] == spielstandDavor
    assert schlachtInDerBewegungsphase.stelle(modell) == davor


def testBew8_2EinKlickAufGemeinsamÜbergehenSetztDasModellWoEsLosgelassenWurde(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)
    ziel = versetzt(davor, fünfZollNachOsten)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    modellZiehen(seite, davor, ziel)
    sperrmeldungWarten(seite, {Grund.überEineBase})

    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, übergehenKnopf).click()

    assert sperrmeldungWarten(seite, set()) == frozenset()
    assert liegtEinPixelGenauAn(seite, schlachtInDerBewegungsphase.stelle(gezogenes), ziel)
    assert kreiseDerKarte(seite) == stellenAlsZahlen(schlachtInDerBewegungsphase)
