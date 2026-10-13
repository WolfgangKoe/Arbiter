"""AUF-9 · Gesperrtes Modell."""

from http import HTTPStatus

from playwright.sync_api import expect

from arbiter.domaene.sperre import Grund
from tests.akzeptanz.bildschirm import (
    gesperrteModelle,
    gründeAlsText,
    kennzeichenDesKreises,
    klickenUndWarten,
    sperrmeldungWarten,
)
from tests.akzeptanz.dienst import dienstFür, modellLoslassen
from tests.akzeptanz.handgriffe import (
    eineGesperrteFormation,
    einGesperrtesModell,
    einheitAufstellen,
    nachDerWahlDerAufstellungszone,
    stelleInDerZoneVon,
    stellenDerEinheit,
)
from tests.akzeptanz.ziehen import liegtEinPixelGenauAn, modellZiehen


def testAuf9_1EinModellAufEinerBaseIstNachDemLoslassenGesperrtMitDemGrund(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)

    _, gesperrtesModell, stelle = einGesperrtesModell(aufstellung, zweiterSpieler)

    assert aufstellung.gesperrt(gesperrtesModell)
    assert not aufstellung.gesetzt(gesperrtesModell)
    assert aufstellung.stelleDesGesperrten(gesperrtesModell) == stelle
    assert aufstellung.gründeDesGesperrten(gesperrtesModell) == {Grund.baseÜberdeckt}


def testAuf9_1EinModellAußerhalbDerZoneIstNachDemLoslassenGesperrtMitDemGrund(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    modell, _ = einheit.modelle
    außerhalb = stelleInDerZoneVon(aufstellung, zweiterSpieler, 10, 20)

    aufstellung.modellLoslassen(modell, außerhalb)

    assert aufstellung.gesperrt(modell)
    assert not aufstellung.gesetzt(modell)
    assert aufstellung.gründeDesGesperrten(modell) == {Grund.nichtGanzInDerZone}


def testAuf9_1EinModellAufDemModellDesAnderenSpielersNenntJedenGrund(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheitDesAnderen, _ = zweiterSpieler.armee.einheiten
    einheit, _ = ersterSpieler.armee.einheiten
    modell, _ = einheit.modelle
    einheitAufstellen(aufstellung, einheitDesAnderen)
    (_, stelleDesAnderen), _ = stellenDerEinheit(aufstellung, zweiterSpieler, einheitDesAnderen)

    aufstellung.modellLoslassen(modell, stelleDesAnderen)

    assert aufstellung.gesperrt(modell)
    assert aufstellung.gründeDesGesperrten(modell) == {
        Grund.baseÜberdeckt,
        Grund.nahkampfreichweite,
        Grund.nichtGanzInDerZone,
    }


def testAuf9_1EinModellDerFormationAufEinerBaseIstGesperrt(
    aufstellungNachDerZonenwahl, boyz, warboss
):
    eineGesperrteFormation(aufstellungNachDerZonenwahl, (boyz, warboss))

    gesperrte = [modell for modell in boyz.modelle if aufstellungNachDerZonenwahl.gesperrt(modell)]
    assert gesperrte
    assert all(
        aufstellungNachDerZonenwahl.gründeDesGesperrten(modell) == {Grund.baseÜberdeckt}
        for modell in gesperrte
    )


def zweiGesetzteModelle(aufstellung, ersterSpieler, zweiterSpieler):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, zweitesModell = einheit.modelle
    (_, ersteStelle), (_, zweiteStelle) = stellenDerEinheit(aufstellung, zweiterSpieler, einheit)
    aufstellung.modellSetzen(erstesModell, ersteStelle)
    aufstellung.modellSetzen(zweitesModell, zweiteStelle)
    return einheit, zweitesModell, ersteStelle, zweiteStelle


def testAuf9_1DerDienstMeldetEinModellAufEinerBaseAlsGesperrtMitDemGrund(
    aufstellung, ersterSpieler, zweiterSpieler
):
    einheit, zweitesModell, ersteStelle, _ = zweiGesetzteModelle(
        aufstellung, ersterSpieler, zweiterSpieler
    )
    dienst = dienstFür(aufstellung)

    antwort = modellLoslassen(dienst, aufstellung, einheit, zweitesModell, ersteStelle)

    stand = antwort.get_json()
    (gesperrtes,) = [modell for modell in stand["modelle"] if modell["gesperrt"]]
    assert antwort.status_code == HTTPStatus.OK
    assert (gesperrtes["spieler"], gesperrtes["einheit"], gesperrtes["nummer"]) == (2, 1, 2)
    assert (gesperrtes["x"], gesperrtes["y"]) == (float(ersteStelle.x), float(ersteStelle.y))
    assert stand["gründeDerGesperrten"] == [Grund.baseÜberdeckt.value]


def testAuf9_1DasLoslassenAufEinerBaseKennzeichnetDasModellAmBildschirmAlsGesperrt(
    bildschirm, aufstellung, ersterSpieler, zweiterSpieler
):
    _, zweitesModell, ersteStelle, zweiteStelle = zweiGesetzteModelle(
        aufstellung, ersterSpieler, zweiterSpieler
    )
    seite = bildschirm.seiteZu(aufstellung)
    klickenUndWarten(seite, "Spieler 2", "Einheit 1")

    modellZiehen(seite, zweiteStelle, ersteStelle)

    expect(seite.locator(".karte .modell.gesperrt")).to_have_count(1)
    stelleDesGesperrten = aufstellung.stelleDesGesperrten(zweitesModell)
    assert liegtEinPixelGenauAn(seite, stelleDesGesperrten, ersteStelle)
    assert gesperrteModelle(seite) == {(float(stelleDesGesperrten.x), float(stelleDesGesperrten.y))}
    gesperrt = kennzeichenDesKreises(seite, ".karte .modell.gesperrt")
    ausgewählt = kennzeichenDesKreises(seite, ".karte .modell.ausgewählt:not(.gesperrt)")
    assert gesperrt != ausgewählt


def testAuf9_1DieSeiteNenntBeiEinemModellAufEinerBaseDenGrund(
    bildschirm, aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einGesperrtesModell(aufstellung, zweiterSpieler)
    seite = bildschirm.seiteZu(aufstellung)

    genannt = sperrmeldungWarten(seite, {Grund.baseÜberdeckt})

    assert genannt == gründeAlsText({Grund.baseÜberdeckt})


def testAuf9_1DieSeiteNenntBeiEinemModellAufDemModellDesAnderenSpielersJedenGrund(
    bildschirm, aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheitDesAnderen, _ = zweiterSpieler.armee.einheiten
    einheit, _ = ersterSpieler.armee.einheiten
    modell, _ = einheit.modelle
    einheitAufstellen(aufstellung, einheitDesAnderen)
    (_, stelleDesAnderen), _ = stellenDerEinheit(aufstellung, zweiterSpieler, einheitDesAnderen)
    aufstellung.modellLoslassen(modell, stelleDesAnderen)
    seite = bildschirm.seiteZu(aufstellung)
    gründe = {Grund.baseÜberdeckt, Grund.nahkampfreichweite, Grund.nichtGanzInDerZone}

    genannt = sperrmeldungWarten(seite, gründe)

    assert genannt == gründeAlsText(gründe)


def testAuf9_3EinGesperrtesModellKommtMitZurückAnSeineVorigeStelle(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    einheit, _ = zweiterSpieler.armee.einheiten
    erstesModell, zweitesModell = einheit.modelle
    vorigeStelle = stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 20)
    aufstellung.modellSetzen(erstesModell, vorigeStelle)
    aufstellung.modellSetzen(zweitesModell, stelleInDerZoneVon(aufstellung, zweiterSpieler, 4, 25))
    aufstellung.modellLoslassen(erstesModell, aufstellung.stelle(zweitesModell))

    aufstellung.zurück()

    assert aufstellung.gesetzt(erstesModell)
    assert aufstellung.stelle(erstesModell) == vorigeStelle
    assert not aufstellung.gesperrt(erstesModell)


def testAuf9_4EinGesperrtesModellAusDerAblageIstMitZurückNichtGesetztUndNichtGesperrt(
    aufstellung, ersterSpieler, zweiterSpieler
):
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=ersterSpieler)
    gesetztesModell, gesperrtesModell, stelle = einGesperrtesModell(aufstellung, zweiterSpieler)

    aufstellung.zurück()

    assert not aufstellung.gesetzt(gesperrtesModell)
    assert not aufstellung.gesperrt(gesperrtesModell)
    assert aufstellung.stelle(gesetztesModell) == stelle
