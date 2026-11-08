"""QUE-7 · Ruhiges Spielfeld."""

from fractions import Fraction

import pytest
from playwright.sync_api import Browser, Page, expect

from arbiter.domaene.querschnitt.schlachtrunden import Phase
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.auswahl import klickenUndWarten
from tests.akzeptanz.bildschirm import (
    Bildschirm,
    amZugGekennzeichnet,
    aufDieHandlungWarten,
    beendenKnopf,
    griffVon,
    knopfDerArmeeliste,
    knopfDerSeite,
    kopfzeileVon,
    phaseBeendenKnopf,
    protokollEinträge,
    sperrmeldungWarten,
    spielerAnDerReihe,
    zurücklegenKnopf,
    übergehenKnopf,
)
from tests.akzeptanz.handgriffe import (
    einheitenAufstellen,
    modelleSetzen,
    stelleInDerZoneVon,
    versetzt,
)
from tests.akzeptanz.schlacht import (
    angehaltenLoslassen,
    einModellAusDerKohärenzZiehen,
    phaseBeendenBis,
    warbossUndDanachEinenBoyÜbergehen,
    zehnZollNachOsten,
    zurLetztenSchlachtrunde,
    zügeBeenden,
)
from tests.akzeptanz.ziehen import (
    Bildpunkt,
    mitDerMausKlicken,
    modellZiehen,
    punktAufDemSpielfeld,
)

_pixelgenauigkeit = 1e-4
_rollweiteInPixeln = 500
_nachDemRollenInMillisekunden = 200
_ersterZugKnopf = "Erster Zug"
_vorrückenKnopf = "Vorrücken"
_einheitZurücksetzenKnopf = "Einheit zurücksetzen"
mitteDesSpielfelds = Stelle(x=Fraction(22), y=Fraction(30))

_abbildungLesen = """spielfeld => {
    const matrix = spielfeld.getScreenCTM()
    return [matrix.a, matrix.b, matrix.c, matrix.d, matrix.e, matrix.f]
}"""


def abbildungDesSpielfelds(seite: Page) -> list[float]:
    return seite.locator("svg.spielfeld").evaluate(_abbildungLesen)


def wieDavor(abbildung: list[float]):
    return pytest.approx(abbildung, rel=_pixelgenauigkeit)


def aufDieStelleKlicken(seite: Page, stelle) -> None:
    with aufDieHandlungWarten(seite):
        mitDerMausKlicken(seite, punktAufDemSpielfeld(seite, stelle))


def knopfKlicken(seite: Page, text: str) -> None:
    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, text).click()


def mitteVon(rahmen: dict) -> Bildpunkt:
    return Bildpunkt(
        links=rahmen["x"] + rahmen["width"] / 2,
        oben=rahmen["y"] + rahmen["height"] / 2,
    )


def mitDemMausradÜberDenKnöpfenRollen(seite: Page) -> None:
    punkt = mitteVon(seite.locator(".spalteMitte .knopfGruppe").bounding_box())
    seite.mouse.move(punkt.links, punkt.oben)
    seite.mouse.wheel(0, _rollweiteInPixeln)
    seite.wait_for_timeout(_nachDemRollenInMillisekunden)


def knopfAnSeinemPlatzKlicken(seite: Page, text: str) -> None:
    punkt = mitteVon(knopfDerSeite(seite, text).bounding_box())
    with aufDieHandlungWarten(seite):
        mitDerMausKlicken(seite, punkt)


def knöpfeBeimAusgewähltenWarboss(seite: Page) -> None:
    expect(knopfDerSeite(seite, übergehenKnopf)).to_be_visible()
    expect(knopfDerSeite(seite, _vorrückenKnopf)).to_be_visible()
    expect(knopfDerSeite(seite, _einheitZurücksetzenKnopf)).to_be_visible()
    expect(knopfDerSeite(seite, phaseBeendenKnopf)).to_be_visible()


def einheitDesSpielersAnDerReiheSetzen(aufstellung) -> None:
    spieler = aufstellung.anDerReihe
    nächste = next(
        einheit for einheit in spieler.armee.einheiten if not aufstellung.aufgestellt(einheit)
    )
    modelleSetzen(aufstellung, nächste, len(nächste.modelle))


@pytest.fixture(
    params=[(1024, 768), (1100, 800), (1280, 720), (1920, 1080)],
    ids=["fenster1024", "fenster1100", "fenster1280", "fenster1920"],
)
def bildschirmJeFenster(request, browserMitRollbalken: Browser):
    breite, höhe = request.param
    bildschirm = Bildschirm(browserMitRollbalken, fenster={"width": breite, "height": höhe})
    yield bildschirm
    bildschirm.beenden()


@pytest.fixture
def gesperrteStelle(aufstellungNachDerZonenwahl, spielerEins, necronWarriors):
    aufstellungNachDerZonenwahl.auswählen(necronWarriors)
    return stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 30)


@pytest.fixture
def warbossAngehalten(schlachtInDerBewegungsphase, warboss):
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    angehaltenLoslassen(schlachtInDerBewegungsphase, boss, ziel)
    return schlachtInDerBewegungsphase


@pytest.fixture
def moralphaseAmEndeDerSchlacht(schlachtNachDerWahlDesErstenZugs):
    zurLetztenSchlachtrunde(schlachtNachDerWahlDesErstenZugs)
    zügeBeenden(schlachtNachDerWahlDesErstenZugs, 1)
    phaseBeendenBis(schlachtNachDerWahlDesErstenZugs, Phase.moralphase)
    return schlachtNachDerWahlDesErstenZugs


def testQue7_1DasSpielfeldBleibtStehenWennEinGrundZuSehenBeginnt(
    bildschirmJeFenster, aufstellungNachDerZonenwahl, gesperrteStelle
):
    seite = bildschirmJeFenster.seiteZu(aufstellungNachDerZonenwahl)
    davor = abbildungDesSpielfelds(seite)

    aufDieStelleKlicken(seite, gesperrteStelle)

    sperrmeldungWarten(seite, {Grund.nichtWählbar})
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennEinGrundAufhörtZuSehenZuSein(
    bildschirmJeFenster, aufstellungNachDerZonenwahl, gesperrteStelle
):
    seite = bildschirmJeFenster.seiteZu(aufstellungNachDerZonenwahl)
    aufDieStelleKlicken(seite, gesperrteStelle)
    sperrmeldungWarten(seite, {Grund.nichtWählbar})
    klickenUndWarten(seite, "Spieler 1", "Boyz")
    davor = abbildungDesSpielfelds(seite)

    aufDieStelleKlicken(seite, gesperrteStelle)

    sperrmeldungWarten(seite, set())
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennEinheitZurücklegenZuSehenBeginnt(
    bildschirmJeFenster, aufstellungNachDerZonenwahl, spielerEins, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 4, 30)
    seite = bildschirmJeFenster.seiteZu(aufstellungNachDerZonenwahl)
    davor = abbildungDesSpielfelds(seite)

    aufDieStelleKlicken(seite, stelle)

    expect(knopfDerSeite(seite, zurücklegenKnopf)).to_be_visible()
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennEinheitZurücklegenAufhörtZuSehenZuSein(
    bildschirmJeFenster, einGesetztesModell
):
    aufstellung, _ = einGesetztesModell
    seite = bildschirmJeFenster.seiteZu(aufstellung)
    davor = abbildungDesSpielfelds(seite)

    knopfKlicken(seite, zurücklegenKnopf)

    expect(knopfDerSeite(seite, zurücklegenKnopf)).to_have_count(0)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


@pytest.mark.parametrize(
    ("aufgestellteEinheiten", "spielerDanach"),
    [(0, "Spieler 2"), (1, "Spieler 1")],
    ids=["vonSpielerEinsZuSpielerZwei", "vonSpielerZweiZuSpielerEins"],
)
def testQue7_1DasSpielfeldBleibtStehenWennEinAndererSpielerAnDerReiheIst(
    bildschirmJeFenster, aufstellungNachDerZonenwahl, aufgestellteEinheiten, spielerDanach
):
    einheitenAufstellen(aufstellungNachDerZonenwahl, aufgestellteEinheiten)
    einheitDesSpielersAnDerReiheSetzen(aufstellungNachDerZonenwahl)
    seite = bildschirmJeFenster.seiteZu(aufstellungNachDerZonenwahl)
    davor = abbildungDesSpielfelds(seite)

    knopfKlicken(seite, beendenKnopf)

    expect(spielerAnDerReihe(seite)).to_contain_text(spielerDanach)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennKeinSpielerAnDerReiheIstUndAufstellenDerEinheitBeendenAufhört(  # noqa: E501
    bildschirmJeFenster, aufstellungNachDerZonenwahl, ausgangslage
):
    letzteEinheit = 1
    einheitenAufstellen(
        aufstellungNachDerZonenwahl,
        len(ausgangslage.ersterSpieler.armee.einheiten)
        + len(ausgangslage.zweiterSpieler.armee.einheiten)
        - letzteEinheit,
    )
    einheitDesSpielersAnDerReiheSetzen(aufstellungNachDerZonenwahl)
    seite = bildschirmJeFenster.seiteZu(aufstellungNachDerZonenwahl)
    expect(spielerAnDerReihe(seite)).to_have_count(1)
    davor = abbildungDesSpielfelds(seite)

    knopfKlicken(seite, beendenKnopf)

    expect(spielerAnDerReihe(seite)).to_have_count(0)
    expect(knopfDerSeite(seite, beendenKnopf)).to_have_count(0)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


@pytest.mark.parametrize("spielername", ["Spieler 1", "Spieler 2"], ids=["eins", "zwei"])
def testQue7_1DasSpielfeldBleibtStehenWennErsterZugAufhörtUndPhaseBeendenBeginnt(
    bildschirmJeFenster, beendeteAufstellung, schlacht, spielername
):
    seite = bildschirmJeFenster.seiteZuSchlacht(beendeteAufstellung, schlacht)
    davor = abbildungDesSpielfelds(seite)

    with aufDieHandlungWarten(seite):
        knopfDerArmeeliste(seite, spielername, _ersterZugKnopf).click()

    expect(knopfDerSeite(seite, phaseBeendenKnopf)).to_be_visible()
    expect(kopfzeileVon(seite, spielername)).to_have_class(amZugGekennzeichnet)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennEineEinheitAusgewähltWird(
    bildschirmJeFenster, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    seite = bildschirmJeFenster.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)
    (boss,) = warboss.modelle
    davor = abbildungDesSpielfelds(seite)

    mitDerMausKlicken(seite, punktAufDemSpielfeld(seite, schlachtInDerBewegungsphase.stelle(boss)))

    expect(seite.locator(".spielfeld .modell.ausgewählt")).to_have_count(1)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennEineEinheitNichtMehrAusgewähltIst(
    bildschirmJeFenster, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    schlachtInDerBewegungsphase.auswählen(boyz)
    seite = bildschirmJeFenster.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)
    expect(seite.locator(".spielfeld .modell.ausgewählt")).to_have_count(len(boyz.modelle))
    davor = abbildungDesSpielfelds(seite)

    mitDerMausKlicken(seite, punktAufDemSpielfeld(seite, mitteDesSpielfelds))

    expect(seite.locator(".spielfeld .modell.ausgewählt")).to_have_count(0)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennGemeinsamÜbergehenZuSehenBeginnt(
    bildschirmJeFenster, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    stelle = schlachtInDerBewegungsphase.stelle(boss)
    seite = bildschirmJeFenster.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)
    davor = abbildungDesSpielfelds(seite)

    modellZiehen(seite, stelle, versetzt(stelle, zehnZollNachOsten))

    expect(knopfDerSeite(seite, übergehenKnopf)).to_be_visible()
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennGemeinsamÜbergehenAufhörtUndDerEintragZuSehenBeginnt(
    bildschirmJeFenster, beendeteAufstellung, warbossAngehalten
):
    seite = bildschirmJeFenster.seiteZuSchlacht(beendeteAufstellung, warbossAngehalten)
    davor = abbildungDesSpielfelds(seite)

    knopfKlicken(seite, übergehenKnopf)

    expect(knopfDerSeite(seite, übergehenKnopf)).to_have_count(0)
    expect(protokollEinträge(seite)).to_have_count(1)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennGemeinsamÜbergehenDieKnöpfeZumUmbruchBringt(
    bildschirmJeFenster, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    schlachtInDerBewegungsphase.auswählen(warboss)
    (boss,) = warboss.modelle
    stelle = schlachtInDerBewegungsphase.stelle(boss)
    seite = bildschirmJeFenster.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)
    davor = abbildungDesSpielfelds(seite)

    modellZiehen(seite, stelle, versetzt(stelle, zehnZollNachOsten))

    knöpfeBeimAusgewähltenWarboss(seite)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennGemeinsamÜbergehenNebenDenÜbrigenKnöpfenAufhört(
    bildschirmJeFenster, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    schlachtInDerBewegungsphase.auswählen(warboss)
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    angehaltenLoslassen(schlachtInDerBewegungsphase, boss, ziel)
    seite = bildschirmJeFenster.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)
    knöpfeBeimAusgewähltenWarboss(seite)
    davor = abbildungDesSpielfelds(seite)

    knopfKlicken(seite, übergehenKnopf)

    expect(knopfDerSeite(seite, übergehenKnopf)).to_have_count(0)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1NachDemRollenBleibtDasSpielfeldStehenWennGemeinsamÜbergehenNebenDenÜbrigenKnöpfenAufhört(  # noqa: E501
    bildschirmJeFenster, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    schlachtInDerBewegungsphase.auswählen(warboss)
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    angehaltenLoslassen(schlachtInDerBewegungsphase, boss, ziel)
    seite = bildschirmJeFenster.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)
    knöpfeBeimAusgewähltenWarboss(seite)
    mitDemMausradÜberDenKnöpfenRollen(seite)
    davor = abbildungDesSpielfelds(seite)

    knopfAnSeinemPlatzKlicken(seite, übergehenKnopf)

    expect(knopfDerSeite(seite, übergehenKnopf)).to_have_count(0)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennEinWeitererEintragZuSehenBeginnt(
    bildschirmJeFenster, beendeteAufstellung, schlachtInDerBewegungsphase, warboss, boyz
):
    warbossUndDanachEinenBoyÜbergehen(schlachtInDerBewegungsphase, warboss, boyz)
    _, weitererBoy, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(weitererBoy), zehnZollNachOsten)
    angehaltenLoslassen(schlachtInDerBewegungsphase, weitererBoy, ziel)
    seite = bildschirmJeFenster.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)
    expect(protokollEinträge(seite)).to_have_count(2)
    davor = abbildungDesSpielfelds(seite)

    knopfKlicken(seite, übergehenKnopf)

    expect(protokollEinträge(seite)).to_have_count(3)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennEinGrundBeginntUndGemeinsamÜbergehenAufhört(
    bildschirmJeFenster, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, warboss
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    angehaltenLoslassen(schlachtInDerBewegungsphase, boss, ziel)
    seite = bildschirmJeFenster.seiteZuSchlacht(beendeteAufstellung, schlachtInDerBewegungsphase)
    expect(knopfDerSeite(seite, übergehenKnopf)).to_be_visible()
    davor = abbildungDesSpielfelds(seite)

    knopfKlicken(seite, phaseBeendenKnopf)

    sperrmeldungWarten(seite, {Grund.keineKohärenz})
    expect(knopfDerSeite(seite, übergehenKnopf)).to_have_count(0)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennEinAndererSpielerAmZugIst(
    bildschirmJeFenster, beendeteAufstellung, schlachtNachDerWahlDesErstenZugs
):
    phaseBeendenBis(schlachtNachDerWahlDesErstenZugs, Phase.moralphase)
    seite = bildschirmJeFenster.seiteZuSchlacht(
        beendeteAufstellung, schlachtNachDerWahlDesErstenZugs
    )
    davor = abbildungDesSpielfelds(seite)

    knopfKlicken(seite, phaseBeendenKnopf)

    expect(kopfzeileVon(seite, "Spieler 2")).to_have_class(amZugGekennzeichnet)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


def testQue7_1DasSpielfeldBleibtStehenWennPhaseBeendenAufhörtUndSchlachtBeendetBeginnt(
    bildschirmJeFenster, beendeteAufstellung, moralphaseAmEndeDerSchlacht
):
    seite = bildschirmJeFenster.seiteZuSchlacht(beendeteAufstellung, moralphaseAmEndeDerSchlacht)
    davor = abbildungDesSpielfelds(seite)

    knopfKlicken(seite, phaseBeendenKnopf)

    expect(seite.locator(".kopfzeileSchlachtBeendet")).to_have_count(1)
    expect(knopfDerSeite(seite, phaseBeendenKnopf)).to_have_count(0)
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)


@pytest.mark.parametrize(
    "leistenname",
    ["Armeeliste Spieler 1", "Armeeliste Spieler 2", "Protokoll"],
    ids=["links", "rechts", "unten"],
)
def testQue7_1DasSpielfeldBleibtBeiEingefahrenerLeisteStehenWennEinGrundZuSehenBeginnt(
    bildschirmJeFenster, aufstellungNachDerZonenwahl, gesperrteStelle, leistenname
):
    seite = bildschirmJeFenster.seiteZu(aufstellungNachDerZonenwahl)
    griffVon(seite, leistenname).click()
    davor = abbildungDesSpielfelds(seite)

    aufDieStelleKlicken(seite, gesperrteStelle)

    sperrmeldungWarten(seite, {Grund.nichtWählbar})
    assert abbildungDesSpielfelds(seite) == wieDavor(davor)
