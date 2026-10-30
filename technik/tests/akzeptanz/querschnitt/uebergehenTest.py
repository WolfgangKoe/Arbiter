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
    dienstFürSchlacht,
    modellLoslassen,
    modellLoslassenUndÜbergehen,
    phaseBeenden,
    protokollDesVertrags,
    schlachtNachSchlüsselnDes,
    spielstandVon,
)
from tests.akzeptanz.handgriffe import (
    nachDerWahlDerAufstellungszone,
    sperreBei,
    sperrgründe,
    stelleInDerZoneVon,
    versetzt,
)
from tests.akzeptanz.schlacht import (
    boyÜberDenWarbossÜbergehen,
    einModellAusDerKohärenzZiehen,
    fünfZollNachOsten,
    warbossÜberDieBoyzÜbergehen,
)
from tests.akzeptanz.ziehen import modellZiehen

weitAuseinander = (10, 30)
aufDieBoyz = (Fraction(-5, 2), Fraction(0))


def gründeDesEintrags(eintrag) -> frozenset[Grund]:
    return frozenset(eintrag.gründe)


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


def testQue5_1GemeinsamÜbergehenTrägtEinheitSpielerUndGrundInsProtokollEin(zugÜberEineBase):
    schlacht, spieler, einheit, modell, ziel = zugÜberEineBase
    gründe = sperrgründe(schlacht.modellLoslassen, modell, ziel)

    schlacht.modellLoslassen(modell, ziel, übergehen=gründe)

    (eintrag,) = schlacht.protokoll
    assert eintrag.einheit is einheit
    assert eintrag.spieler is spieler
    assert gründeDesEintrags(eintrag) == {Grund.überEineBase}


def testQue5_1DerEintragNenntJedenÜbergangenenGrund(schlachtInDerBewegungsphase, warboss):
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), aufDieBoyz)
    gründe = sperrgründe(schlachtInDerBewegungsphase.modellLoslassen, modell, ziel)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel, übergehen=gründe)

    (eintrag,) = schlachtInDerBewegungsphase.protokoll
    assert gründeDesEintrags(eintrag) == {Grund.baseÜberdeckt, Grund.überEineBase}


def testQue5_1JedesÜbergehenTrägtGenauEinenEintragMehrEinUndBehältDieÄlteren(
    schlachtInDerBewegungsphase, boyz, warboss
):
    boyÜberDenWarbossÜbergehen(schlachtInDerBewegungsphase, boyz)
    (älterer,) = schlachtInDerBewegungsphase.protokoll
    (modell,) = warboss.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(modell), fünfZollNachOsten)
    gründe = sperrgründe(schlachtInDerBewegungsphase.modellLoslassen, modell, ziel)

    schlachtInDerBewegungsphase.modellLoslassen(modell, ziel, übergehen=gründe)

    davor, neuer = schlachtInDerBewegungsphase.protokoll
    assert davor is älterer
    assert neuer.einheit is warboss


def testQue5_1EineSperreOhneGemeinsamÜbergehenTrägtNichtsInsProtokollEin(zugÜberEineBase):
    schlacht, _, _, modell, ziel = zugÜberEineBase

    sperrgründe(schlacht.modellLoslassen, modell, ziel)

    assert list(schlacht.protokoll) == []


def testQue5_1DerDienstNenntDenEintragImSpielstand(
    beendeteAufstellung, zugÜberEineBase, spielerEins
):
    schlacht, spieler, einheit, modell, ziel = zugÜberEineBase
    dienst = dienstFürSchlacht(beendeteAufstellung, schlacht)
    spielernummer = 1 if spieler is spielerEins else 2
    modellLoslassen(dienst, beendeteAufstellung, einheit, modell, ziel)

    antwort = modellLoslassenUndÜbergehen(
        dienst, beendeteAufstellung, modell, ziel, {Grund.überEineBase}
    )

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json()["schlacht"]["protokoll"] == [
        {"spieler": spielernummer, "einheit": 1, "name": einheit.name, "gründe": ["über eine Base"]}
    ]


def testQue5_1DieSeiteZeigtNachDemKlickAufGemeinsamÜbergehenDenEintrag(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    davor = schlachtInDerBewegungsphase.stelle(gezogenes)
    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )
    modellZiehen(seite, davor, versetzt(davor, fünfZollNachOsten))
    sperrmeldungWarten(seite, {Grund.überEineBase})

    with aufDieHandlungWarten(seite):
        knopfDerSeite(seite, übergehenKnopf).click()

    expect(protokollEinträge(seite)).to_have_count(1)
    assert protokollDerSeite(seite) == {("Boyz", "Spieler 1", frozenset({"über eine Base"}))}


def boyUndWarbossÜbergehen(schlacht, spieler) -> None:
    boyz, warboss = spieler.armee.einheiten
    boyÜberDenWarbossÜbergehen(schlacht, boyz)
    warbossÜberDieBoyzÜbergehen(schlacht, warboss)


@pytest.mark.parametrize("erneut", ["neuLaden", "adresseErneutÖffnen"])
def testQue5_2ÖffnetEinSpielerDieAdresseErneutZeigtDasProtokollDieselbenEinträge(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, spielerEins, erneut
):
    boyUndWarbossÜbergehen(schlachtInDerBewegungsphase, spielerEins)
    davor = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
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
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz
):
    gezogenes, *_ = boyz.modelle
    ziel = versetzt(schlachtInDerBewegungsphase.stelle(gezogenes), fünfZollNachOsten)
    davor = modellLoslassenUndÜbergehen(
        dienstDerSchlacht, beendeteAufstellung, gezogenes, ziel, {Grund.überEineBase}
    ).get_json()

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
    boyÜberDenWarbossÜbergehen(schlachtInDerBewegungsphase, boyz)

    warbossÜberDieBoyzÜbergehen(schlachtInDerBewegungsphase, warboss)

    älterer, neuerer = schlachtInDerBewegungsphase.protokoll
    assert älterer.einheit is boyz
    assert neuerer.einheit is warboss


def testQue5_4DerDienstNenntDenNeuerenEintragZuerstWieImBeispiel(
    dienstDerSchlacht, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, warboss
):
    boy, *_ = boyz.modelle
    (boss,) = warboss.modelle
    zielDesBoys = versetzt(schlachtInDerBewegungsphase.stelle(boy), fünfZollNachOsten)
    zielDesBoss = versetzt(schlachtInDerBewegungsphase.stelle(boss), fünfZollNachOsten)
    modellLoslassen(dienstDerSchlacht, beendeteAufstellung, boyz, boy, zielDesBoys)
    modellLoslassenUndÜbergehen(
        dienstDerSchlacht, beendeteAufstellung, boy, zielDesBoys, {Grund.überEineBase}
    )
    modellLoslassen(dienstDerSchlacht, beendeteAufstellung, warboss, boss, zielDesBoss)

    antwort = modellLoslassenUndÜbergehen(
        dienstDerSchlacht, beendeteAufstellung, boss, zielDesBoss, {Grund.überEineBase}
    )

    assert antwort.status_code == HTTPStatus.OK
    beispiel = protokollDesVertrags()["schlacht"]
    assert schlachtNachSchlüsselnDes(antwort.get_json(), beispiel) == beispiel


def testQue5_4DieSeiteZeigtDenNeuerenEintragÜberDemÄlteren(
    bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, boyz, warboss
):
    boyÜberDenWarbossÜbergehen(schlachtInDerBewegungsphase, boyz)
    warbossÜberDieBoyzÜbergehen(schlachtInDerBewegungsphase, warboss)

    seite = seiteDerSchlachtMitEingabe(
        bildschirm, beendeteAufstellung, schlachtInDerBewegungsphase, "maus"
    )

    expect(protokollEinträge(seite)).to_have_count(2)
    älterer = eintragDerEinheit(seite, "Boyz").bounding_box()
    neuerer = eintragDerEinheit(seite, "Warboss").bounding_box()
    assert neuerer["y"] + neuerer["height"] <= älterer["y"]


def testQue5_5BeimBeendenDerBewegungsphaseOhneKohärenzBietetArbiterGemeinsamÜbergehenNichtAn(
    schlachtInDerBewegungsphase, boyz
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)

    sperre = sperreBei(schlachtInDerBewegungsphase.phaseBeenden)

    assert Grund.keineKohärenz in sperre.gründe
    assert sperre.übergehbar is False
    assert schlachtInDerBewegungsphase.phase is Phase.bewegungsphase


def testQue5_5BeimAufstellenDerEinheitBeendenOhneKohärenzBietetArbiterGemeinsamÜbergehenNichtAn(
    aufstellung, ersterSpieler, zweiterSpieler
):
    einheit = einheitOhneKohärenzSetzen(aufstellung, ersterSpieler, zweiterSpieler)

    sperre = sperreBei(aufstellung.aufstellenDerEinheitBeenden)

    assert Grund.keineKohärenz in sperre.gründe
    assert sperre.übergehbar is False
    assert not aufstellung.aufgestellt(einheit)


def testQue5_5DerDienstNenntBeimBeendenDerBewegungsphaseOhneKohärenzKeinÜbergehbar(
    dienstDerSchlacht, schlachtInDerBewegungsphase, boyz
):
    einModellAusDerKohärenzZiehen(schlachtInDerBewegungsphase, boyz)

    antwort = phaseBeenden(dienstDerSchlacht, 1, 1, Phase.bewegungsphase)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [Grund.keineKohärenz.value]
    assert "übergehbar" not in antwort.get_json()


def testQue5_5DerDienstNenntBeimAufstellenDerEinheitBeendenOhneKohärenzKeinÜbergehbar(
    aufstellung, ersterSpieler, zweiterSpieler
):
    einheitOhneKohärenzSetzen(aufstellung, ersterSpieler, zweiterSpieler)
    dienst = dienstFür(aufstellung)

    antwort = aufstellenDerEinheitBeenden(dienst)

    assert antwort.status_code == HTTPStatus.CONFLICT
    assert antwort.get_json()["gründe"] == [Grund.keineKohärenz.value]
    assert "übergehbar" not in antwort.get_json()


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
