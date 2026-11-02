"""QUE-5 · Gemeinsam übergehen."""

from fractions import Fraction
from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from arbiter.domaene.querschnitt.schlachtrunden import Phase
from arbiter.domaene.sperre import Grund
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    beendenKnopf,
    eintragDerEinheit,
    knopfDerSeite,
    leisteVon,
    neuLaden,
    protokollDerSeite,
    protokollEinträge,
    seiteDerSchlachtMitEingabe,
    sperrmeldungWarten,
    übergehenKnopf,
)
from tests.akzeptanz.dienst import (
    aufstellenDerEinheitBeenden,
    dienstFür,
    gemeinsamÜbergehen,
    modellLoslassen,
    phaseBeenden,
    protokollDesVertrags,
    schlachtNachSchlüsselnDes,
    spielstandVon,
)
from tests.akzeptanz.handgriffe import (
    nachDerWahlDerAufstellungszone,
    sperreBei,
    stelleInDerZoneVon,
    versetzt,
)
from tests.akzeptanz.schlacht import (
    angehaltenLoslassen,
    anhaltenUndÜbergehen,
    einModellAusDerKohärenzZiehen,
    warbossUndDanachEinenBoyÜbergehen,
    zehnZollNachOsten,
)

weitAuseinander = (10, 30)
dreiZollNachSüden = (Fraction(0), Fraction(3))


def einheitOhneKohärenzSetzen(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, zweitesModell = einheit.modelle
    nah, fern = weitAuseinander
    aufstellung.modellSetzen(erstesModell, stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, nah))
    aufstellung.modellSetzen(
        zweitesModell, stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, fern)
    )
    return einheit


@pytest.fixture
def schlachtNachDemÜbergehenVonBoyUndWarboss(schlachtInDerBewegungsphase, boyz, warboss):
    warbossUndDanachEinenBoyÜbergehen(schlachtInDerBewegungsphase, warboss, boyz)
    return schlachtInDerBewegungsphase


@pytest.mark.parametrize("erneut", ["neuLaden", "adresseErneutÖffnen"])
def testQue5_2ÖffnetEinSpielerDieAdresseErneutZeigtDasProtokollDieselbenEinträge(
    bildschirm, beendeteAufstellung, schlachtNachDemÜbergehenVonBoyUndWarboss, erneut
):
    davor = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtNachDemÜbergehenVonBoyUndWarboss, "maus"
    )
    expect(protokollEinträge(davor)).to_have_count(2)
    einträgeDavor = protokollDerSeite(davor)

    if erneut == "neuLaden":
        neuLaden(davor)
        danach = davor
    else:
        danach = bildschirm.seiteBei(davor.url)

    expect(protokollEinträge(danach)).to_have_count(2)
    assert protokollDerSeite(danach) == einträgeDavor


def testQue5_2DerDienstLiefertAufJedeWeitereAnfrageDasselbeProtokoll(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, boss, ziel)
    übergangen = gemeinsamÜbergehen(dienstDerSchlacht)
    assert übergangen.status_code == HTTPStatus.OK
    davor = übergangen.get_json()

    danach = spielstandVon(dienstDerSchlacht)

    assert danach["schlacht"]["protokoll"] == davor["schlacht"]["protokoll"]
    assert len(danach["schlacht"]["protokoll"]) == 1


def testQue5_3NachDemStartIstDasProtokollLeer(adresseDesBefehls, bildschirm):
    seite = bildschirm.seiteBei(adresseDesBefehls)

    expect(leisteVon(seite, "Protokoll")).to_be_visible()
    expect(protokollEinträge(seite)).to_have_count(0)


def testQue5_3ZuBeginnDerSchlachtIstDasProtokollLeer(schlacht):
    assert list(schlacht.protokoll) == []


def testQue5_3DerDienstNenntZuBeginnDerSchlachtEinLeeresProtokoll(dienstNachDerAufstellung):
    spielstand = spielstandVon(dienstNachDerAufstellung)

    assert spielstand["schlacht"]["protokoll"] == []


def testQue5_4DieSchlachtFührtDenÄlterenEintragVorDemNeueren(
    schlachtInDerBewegungsphase, boyz, warboss
):
    (boss,) = warboss.modelle
    anhaltenUndÜbergehen(
        schlachtInDerBewegungsphase,
        boss,
        versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten),
    )
    boy, *_ = boyz.modelle
    angehaltenLoslassen(
        schlachtInDerBewegungsphase,
        boy,
        versetzt(schlachtInDerBewegungsphase.stelle(boy), zehnZollNachOsten),
    )

    schlachtInDerBewegungsphase.gemeinsamÜbergehen()

    älterer, neuerer = schlachtInDerBewegungsphase.protokoll
    assert älterer.einheit is warboss
    assert neuerer.einheit is boyz


def testQue5_4DerDienstNenntDenNeuerenEintragZuerstWieImBeispiel(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, warboss
):
    boy, *_ = boyz.modelle
    (boss,) = warboss.modelle
    zielDesBoss = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    zielDesBoys = versetzt(schlachtInDerBewegungsphase.stelle(boy), zehnZollNachOsten)
    modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, boss, zielDesBoss)
    gemeinsamÜbergehen(dienstDerSchlacht)
    modellLoslassen(dienstDerSchlacht, beendeteAufstellung, boyz, boy, zielDesBoys)

    antwort = gemeinsamÜbergehen(dienstDerSchlacht)

    assert antwort.status_code == HTTPStatus.OK
    beispiel = protokollDesVertrags()["schlacht"]
    assert schlachtNachSchlüsselnDes(antwort.get_json(), beispiel) == beispiel


def testQue5_4DieSeiteZeigtDenNeuerenEintragÜberDemÄlteren(
    bildschirm, beendeteAufstellung, schlachtNachDemÜbergehenVonBoyUndWarboss
):
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtNachDemÜbergehenVonBoyUndWarboss, "maus"
    )

    expect(protokollEinträge(seite)).to_have_count(2)
    älterer = eintragDerEinheit(seite, "Warboss").bounding_box()
    neuerer = eintragDerEinheit(seite, "Boyz").bounding_box()
    assert neuerer["y"] + neuerer["height"] <= älterer["y"]


@pytest.mark.usefixtures("schlachtInDerBewegungsphase")
def testQue5_4DieSeiteZeigtDasBeispielMitDemNeuerenEintragOben(
    bildschirm, beendeteAufstellung, dienstDerSchlacht
):
    stand = spielstandVon(dienstDerSchlacht)
    beispiel = protokollDesVertrags()["schlacht"]
    spielstand = {**stand, "schlacht": {**stand["schlacht"], **beispiel}}

    seite = bildschirm.seiteMitSpielstand(beendeteAufstellung, spielstand)

    expect(protokollEinträge(seite)).to_have_count(2)
    älterer = eintragDerEinheit(seite, "Warboss").bounding_box()
    neuerer = eintragDerEinheit(seite, "Boyz").bounding_box()
    assert neuerer["y"] + neuerer["height"] <= älterer["y"]


def testQue5_5BeimBeendenDerBewegungsphaseOhneKohärenzBietetArbiterGemeinsamÜbergehenNichtAn(
    schlachtInDerBewegungsphase, boyz
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)

    sperre = sperreBei(schlachtInDerBewegungsphase.phaseBeenden)

    assert Grund.keineKohärenz in sperre.gründe
    assert schlachtInDerBewegungsphase.gemeinsamÜbergehenAngeboten is False
    assert schlachtInDerBewegungsphase.phase is Phase.bewegungsphase


def testQue5_5DerDienstNenntBeimBeendenDerBewegungsphaseOhneKohärenzKeinÜbergehbar(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)

    antwort = phaseBeenden(dienstDerSchlacht, 1, 1, Phase.bewegungsphase)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [Grund.keineKohärenz.value]
    assert set(antwort.get_json()) == {"gründe", "spielstand"}


def testQue5_5DerDienstNenntBeimAufstellenDerEinheitBeendenOhneKohärenzKeinÜbergehbar(
    aufstellung, ersterSpieler, zweiterSpieler
):
    einheitOhneKohärenzSetzen(aufstellung, ersterSpieler, zweiterSpieler)
    dienst = dienstFür(aufstellung)

    antwort = aufstellenDerEinheitBeenden(dienst)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [Grund.keineKohärenz.value]
    assert set(antwort.get_json()) == {"gründe", "spielstand"}


def testQue5_5DieSeiteBietetBeimBeendenDerBewegungsphaseOhneKohärenzGemeinsamÜbergehenNichtAn(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, "Phase beenden").click()

    assert sperrmeldungWarten(seite, {Grund.keineKohärenz}) == {Grund.keineKohärenz.value}
    expect(knopfDerSeite(seite, übergehenKnopf)).to_have_count(0)


def testQue5_5DieSeiteBietetBeimAufstellenDerEinheitBeendenOhneKohärenzGemeinsamÜbergehenNichtAn(
    bildschirm, aufstellung, ersterSpieler, zweiterSpieler
):
    einheitOhneKohärenzSetzen(aufstellung, ersterSpieler, zweiterSpieler)
    seite = bildschirm.seiteZu(aufstellung)

    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, beendenKnopf).click()

    assert sperrmeldungWarten(seite, {Grund.keineKohärenz}) == {Grund.keineKohärenz.value}
    expect(knopfDerSeite(seite, übergehenKnopf)).to_have_count(0)


def testQue5_5DieSeiteZeigtNebenDerSperrmeldungKeinGemeinsamÜbergehen(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, warboss
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)
    (boss,) = warboss.modelle
    angehaltenLoslassen(
        schlachtInDerBewegungsphase,
        boss,
        versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten),
    )
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    expect(knopfDerSeite(seite, übergehenKnopf)).to_be_visible()

    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, "Phase beenden").click()

    assert sperrmeldungWarten(seite, {Grund.keineKohärenz}) == {Grund.keineKohärenz.value}
    expect(knopfDerSeite(seite, übergehenKnopf)).to_have_count(0)


@pytest.mark.parametrize("weg", [dreiZollNachSüden, zehnZollNachOsten], ids=["frei", "angehalten"])
def testQue5_6BeimLoslassenÄndertSichDasProtokollNicht(
    schlachtInDerBewegungsphase, warboss, boyz, weg
):
    (boss,) = warboss.modelle
    anhaltenUndÜbergehen(
        schlachtInDerBewegungsphase,
        boss,
        versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten),
    )
    einträge = list(schlachtInDerBewegungsphase.protokoll)
    *_, letzter = boyz.modelle

    schlachtInDerBewegungsphase.modellLoslassen(
        letzter, versetzt(schlachtInDerBewegungsphase.stelle(letzter), weg)
    )

    assert list(schlachtInDerBewegungsphase.protokoll) == einträge


def testQue5_6DerDienstNenntNachDemLoslassenDasProtokollWieDavor(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, warboss
):
    (boss,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(boss), zehnZollNachOsten)
    davor = spielstandVon(dienstDerSchlacht)["schlacht"]["protokoll"]

    antwort = modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, boss, ziel)

    assert antwort.get_json()["schlacht"]["protokoll"] == davor
