"""AUF-18 · Setzen per Klick."""

from fractions import Fraction
from http import HTTPStatus
from operator import attrgetter
from urllib.parse import urlparse

import pytest
from playwright.sync_api import expect

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Einheit, Stelle
from tests.akzeptanz.auswahl import ausgewählteEinheiten, klickenUndWarten
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    einheitenKarteVon,
    elementeDerSeite,
    seiteMitEingabe,
)
from tests.akzeptanz.dienst import (
    auswählen,
    karteAnklicken,
    kennungenDerEinheiten,
    spielstandVon,
    stelleImSpielstand,
)
from tests.akzeptanz.handgriffe import (
    anzahlGesetzterModelle,
    millionstel,
    modelleSetzen,
    radiusInZoll,
    reihenDerFormation,
    stelleInDerZoneVon,
    stellenAllerModelle,
)
from tests.akzeptanz.ziehen import (
    Bildpunkt,
    klickenMit,
    mitDerMausKlicken,
    mitMausUndFinger,
    mitteVon,
    punktAufDerKarte,
    ziehenOhneAnfrage,
    zollJePixel,
)

mitteDerZone = Fraction(9, 2)
abstandInDerFormation = Fraction(3, 2)
# Warum: Deutlich über der Zugschwelle von 4 px (V8), aber innerhalb von Karte und Einheitenkarte
weiteDesZugsInPixeln = 12


def modelleDerEinheitIm(spielstand: dict, einheitenname: str) -> list[dict]:
    spielernummer, einheitennummer = kennungenDerEinheiten[einheitenname]
    return [
        modell
        for modell in spielstand["modelle"]
        if (modell["spieler"], modell["einheit"]) == (spielernummer, einheitennummer)
    ]


def mitteDer(punkte: list[tuple[float, float]]) -> tuple[float, float]:
    xWerte = [punkt[0] for punkt in punkte]
    yWerte = [punkt[1] for punkt in punkte]
    return (min(xWerte) + max(xWerte)) / 2, (min(yWerte) + max(yWerte)) / 2


def gesetzteStellen(aufstellung, einheit: Einheit) -> list:
    return [stelle for modell in einheit.modelle if (stelle := aufstellung.stelle(modell))]


def mittelwert(werte: list[Fraction]) -> Fraction:
    return sum(werte) / len(werte)


def abstandDerReihen(vordere: list[Stelle], hintere: list[Stelle]) -> Fraction:
    ersteStelleVorn, *_ = vordere
    ersteStelleHinten, *_ = hintere
    return ersteStelleHinten.x - ersteStelleVorn.x


def reihenNachX(stellen: list[Stelle]) -> list[list[Stelle]]:
    xWerte = sorted({stelle.x for stelle in stellen})
    return [
        sorted((kandidat for kandidat in stellen if kandidat.x == wert), key=attrgetter("y"))
        for wert in xWerte
    ]


def testAuf18_1KeineAusgewählteEinheitLässtDenKlickAufDieKarteOhneFolge(
    aufstellungNachDerZonenwahl, spielerEins
):
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    aufstellungNachDerZonenwahl.karteAnklicken(stelle)

    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is None


def testAuf18_1DerKlickGiltDerAusgewähltenEinheitNichtDerAnderen(
    aufstellungNachDerZonenwahl, spielerEins, boyz, warboss
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    aufstellungNachDerZonenwahl.auswählen(warboss)
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    aufstellungNachDerZonenwahl.karteAnklicken(stelle)

    assert gesetzteStellen(aufstellungNachDerZonenwahl, warboss)
    assert not gesetzteStellen(aufstellungNachDerZonenwahl, boyz)


def testAuf18_1DerDienstLässtDenKlickOhneAusgewählteEinheitOhneFolge(
    dienst, aufstellungNachDerZonenwahl, spielerEins
):
    davor = spielstandVon(dienst)
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    antwort = karteAnklicken(dienst, stelle)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == davor


def testAuf18_1DerDienstSetztNurDieAusgewählteEinheit(
    dienst, aufstellungNachDerZonenwahl, spielerEins
):
    auswählen(dienst, "Boyz")
    auswählen(dienst, "Warboss")
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    antwort = karteAnklicken(dienst, stelle)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert len(modelleDerEinheitIm(spielstand, "Warboss")) == 1
    assert modelleDerEinheitIm(spielstand, "Boyz") == []


@mitMausUndFinger
def testAuf18_1EinKlickAufDieKarteSendetDenPunktInZollAnDenDienst(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins, eingabe
):
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)
    klickenUndWarten(seite, "Spieler 1", "Boyz")
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)
    punkt = punktAufDerKarte(seite, stelle)

    with aufDieHandlungWarten(seite) as antwort:
        klickenMit[eingabe](seite, punkt)

    anfrage = antwort.value.request
    gesendet = anfrage.post_data_json
    toleranz = zollJePixel(seite)
    assert (anfrage.method, urlparse(anfrage.url).path) == ("PUT", "/api/karteAnklicken")
    inX, inY = stelleImSpielstand(stelle)
    assert abs(gesendet["x"] - inX) <= toleranz
    assert abs(gesendet["y"] - inY) <= toleranz


def testAuf18_1EinKlickAufDieKarteOhneAusgewählteEinheitGehtAnDenDienstUndÄndertNichts(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins
):
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    with aufDieHandlungWarten(seite) as antwort:
        mitDerMausKlicken(seite, punktAufDerKarte(seite, stelle))

    assert antwort.value.status == HTTPStatus.OK
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor
    assert elementeDerSeite(seite, ".karte .modell") == ()


def testAuf18_1WelcherEinheitDerKlickGiltEntscheidetDieDomäneNichtDieSeite(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins, boyz
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    with aufDieHandlungWarten(seite) as antwort:
        mitDerMausKlicken(seite, punktAufDerKarte(seite, stelle))

    assert antwort.value.status == HTTPStatus.OK
    assert gesetzteStellen(aufstellungNachDerZonenwahl, boyz)


@mitMausUndFinger
def testAuf18_1EinKlickAufEinModellSetztDieAusgewählteEinheitNicht(
    bildschirm, aufstellungNachDerZonenwahl, boyz, warboss, eingabe
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, anzahlGesetzterModelle)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)
    klickenUndWarten(seite, "Spieler 1", "Warboss")
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    modell = mitteVon(seite.locator(".karte .modell").first)

    klickenMit[eingabe](seite, modell)
    seite.wait_for_load_state("networkidle")

    assert not gesetzteStellen(aufstellungNachDerZonenwahl, warboss)
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor


def testAuf18_1EinZugAufDerEinheitenkarteWähltDieEinheitNichtAus(
    bildschirm, aufstellungNachDerZonenwahl
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    start = mitteVon(einheitenKarteVon(seite, "Spieler 1", "Boyz"))
    ziel = Bildpunkt(start.links + weiteDesZugsInPixeln, start.oben)

    anfragen = ziehenOhneAnfrage(seite, start, ziel)

    assert anfragen == []
    assert ausgewählteEinheiten(seite) == frozenset()
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is None


def testAuf18_1EinZugAufDemSpielfeldSetztDieAusgewählteEinheitNicht(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    klickenUndWarten(seite, "Spieler 1", "Boyz")
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)
    start = punktAufDerKarte(seite, stelle)
    ziel = Bildpunkt(start.links, start.oben + weiteDesZugsInPixeln)

    anfragen = ziehenOhneAnfrage(seite, start, ziel)

    assert anfragen == []
    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor
    assert elementeDerSeite(seite, ".karte .modell") == ()
    assert ausgewählteEinheiten(seite) == {"Boyz"}


def testAuf18_2EineEinheitOhneGesetztesModellStehtNachDemKlickMittigAlsFormation(
    aufstellungNachDerZonenwahl, spielerEins, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    aufstellungNachDerZonenwahl.karteAnklicken(klick)

    stellen = gesetzteStellen(aufstellungNachDerZonenwahl, boyz)
    xWerte = [stelle.x for stelle in stellen]
    yWerte = [stelle.y for stelle in stellen]
    assert len(stellen) == len(boyz.modelle)
    assert (min(xWerte) + max(xWerte)) / 2 == klick.x
    assert (min(yWerte) + max(yWerte)) / 2 == klick.y
    assert aufstellungNachDerZonenwahl.einheitInAufstellung is boyz


def testAuf18_2DieReihenDerFormationLiegenParallelZurSpielfeldkanteDerZone(
    aufstellungNachDerZonenwahl, spielerEins, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    aufstellungNachDerZonenwahl.karteAnklicken(klick)

    reihen = reihenNachX(gesetzteStellen(aufstellungNachDerZonenwahl, boyz))
    assert [len(reihe) for reihe in reihen] == reihenDerFormation("Boyz")


def testAuf18_2JedeReiheDerFormationLiegtEntlangDerSpielfeldkanteMittigAmKlick(
    aufstellungNachDerZonenwahl, spielerEins, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    aufstellungNachDerZonenwahl.karteAnklicken(klick)

    reihen = reihenNachX(gesetzteStellen(aufstellungNachDerZonenwahl, boyz))
    mitten = [(reihe[0].y + reihe[-1].y) / 2 for reihe in reihen]
    assert mitten == [klick.y] * len(reihen)


def testAuf18_2BenachbarteBasesEinerReiheHabenDenAbstandEinsKommaFünfZoll(
    aufstellungNachDerZonenwahl, spielerEins, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)
    modell, *_ = boyz.modelle

    aufstellungNachDerZonenwahl.karteAnklicken(klick)

    reihen = reihenNachX(gesetzteStellen(aufstellungNachDerZonenwahl, boyz))
    paare = [
        (links, rechts) for reihe in reihen for links, rechts in zip(reihe, reihe[1:], strict=False)
    ]
    genau = [
        messen.abstandHöchstens(modell.base, links, modell.base, rechts, abstandInDerFormation)
        for links, rechts in paare
    ]
    zuNah = [
        messen.abstandHöchstens(
            modell.base, links, modell.base, rechts, abstandInDerFormation - millionstel
        )
        for links, rechts in paare
    ]
    assert all(genau)
    assert not any(zuNah)


def testAuf18_2SchrägBenachbarteBasesHabenMindestensEinsKommaFünfZollBeiReihenAufEinHundertstel(
    aufstellungNachDerZonenwahl, spielerEins, boyz
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)
    modell, *_ = boyz.modelle

    aufstellungNachDerZonenwahl.karteAnklicken(klick)

    reihen = reihenNachX(gesetzteStellen(aufstellungNachDerZonenwahl, boyz))
    paareJeNachbarreihen = [
        [(links, rechts) for links in vordere for rechts in hintere]
        for vordere, hintere in zip(reihen, reihen[1:], strict=False)
    ]
    unterschritten = [
        messen.abstandHöchstens(
            modell.base, links, modell.base, rechts, abstandInDerFormation - millionstel
        )
        for paare in paareJeNachbarreihen
        for links, rechts in paare
    ]
    zuWeit = [
        not any(
            messen.abstandHöchstens(
                modell.base, links, modell.base, rechts, abstandInDerFormation + Fraction(1, 100)
            )
            for links, rechts in paare
        )
        for paare in paareJeNachbarreihen
    ]
    reihenabstände = [
        abstandDerReihen(vordere, hintere)
        for vordere, hintere in zip(reihen, reihen[1:], strict=False)
    ]
    assert not any(unterschritten)
    assert not any(zuWeit)
    assert all((abstand * 100).denominator == 1 for abstand in reihenabstände)


def testAuf18_2EineEinheitAusEinemModellStehtAmKlick(
    aufstellungNachDerZonenwahl, spielerEins, warboss
):
    aufstellungNachDerZonenwahl.auswählen(warboss)
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    aufstellungNachDerZonenwahl.karteAnklicken(klick)

    assert gesetzteStellen(aufstellungNachDerZonenwahl, warboss) == [klick]


def testAuf18_2DerDienstSetztDieFormationMittigAnDenKlickUndAntwortetMitDemSpielstand(
    dienst, aufstellungNachDerZonenwahl, spielerEins, boyz
):
    auswählen(dienst, "Boyz")
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    antwort = karteAnklicken(dienst, klick)

    modelle = modelleDerEinheitIm(antwort.get_json(), "Boyz")
    mitteX, mitteY = mitteDer([(modell["x"], modell["y"]) for modell in modelle])
    assert antwort.status_code == HTTPStatus.OK
    assert len(modelle) == len(boyz.modelle)
    assert mitteX == pytest.approx(float(klick.x))
    assert mitteY == pytest.approx(float(klick.y))
    assert antwort.get_json() == spielstandVon(dienst)


def testAuf18_2DieSeiteZeigtDieFormationMittigAmKlick(
    bildschirm, aufstellungNachDerZonenwahl, spielerEins, boyz
):
    seite = bildschirm.seiteZu(aufstellungNachDerZonenwahl)
    klickenUndWarten(seite, "Spieler 1", "Boyz")
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 30)

    with aufDieHandlungWarten(seite):
        mitDerMausKlicken(seite, punktAufDerKarte(seite, klick))

    expect(seite.locator(".karte .modell")).to_have_count(len(boyz.modelle))
    kreise = elementeDerSeite(seite, ".karte .modell")
    mitteX, mitteY = mitteDer([(kreis.zahl("cx"), kreis.zahl("cy")) for kreis in kreise])
    assert abs(mitteX - float(klick.x)) <= zollJePixel(seite)
    assert abs(mitteY - float(klick.y)) <= zollJePixel(seite)


@pytest.mark.parametrize(
    ("klickstelle", "ändertSich"),
    [
        ((0, 30), "x"),
        ((20, 30), "x"),
        ((4, 0), "y"),
        ((4, 60), "y"),
    ],
    ids=["überDieSpielfeldkante", "zurSpielfeldmitteHin", "überDieKurzeKanteAmAnfang", "amEnde"],
)
def testAuf18_3RagtDieFormationAusDerZoneRücktSieAufKürzestemWegHinein(
    aufstellungNachDerZonenwahl, spielerEins, boyz, klickstelle, ändertSich
):
    aufstellungNachDerZonenwahl.auswählen(boyz)
    tiefe, länge = klickstelle
    klick = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, tiefe, länge)
    zone = aufstellungNachDerZonenwahl.aufstellungszone(spielerEins)
    grenzen = aufstellungNachDerZonenwahl.ausgangslage.grenzenDerZone(zone)
    grenzenInX, grenzenInY = grenzen
    erstesModell, *_ = boyz.modelle
    radius = radiusInZoll(erstesModell)

    aufstellungNachDerZonenwahl.karteAnklicken(klick)

    stellen = gesetzteStellen(aufstellungNachDerZonenwahl, boyz)
    ränder = [
        rand
        for stelle in stellen
        for rand in (stelle.x - radius, stelle.x + radius, stelle.y - radius, stelle.y + radius)
    ]
    unveränderteAchse = klick.y if ändertSich == "x" else klick.x
    entlangDerAchse = attrgetter("y" if ändertSich == "x" else "x")
    mittlereAchse = mittelwert([entlangDerAchse(stelle) for stelle in stellen])
    assert all(
        messen.ganzIn(modell.base, stelle, *grenzen)
        for modell, stelle in zip(boyz.modelle, stellen, strict=True)
    )
    assert mittlereAchse == unveränderteAchse
    # Warum: Auf kürzestem Weg heißt, eine Base berührt danach die Grenze der Zone
    assert {*grenzenInX, *grenzenInY} & set(ränder)


def testAuf18_5HatDieEinheitNurGesetzteModelleÄndertDerKlickNichtsUndNenntKeinenGrund(
    aufstellungNachDerZonenwahl, spielerEins, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, len(boyz.modelle))
    aufstellungNachDerZonenwahl.auswählen(boyz)
    davor = stellenAllerModelle(aufstellungNachDerZonenwahl)
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 50)

    aufstellungNachDerZonenwahl.karteAnklicken(stelle)

    assert stellenAllerModelle(aufstellungNachDerZonenwahl) == davor


def testAuf18_5DerDienstÄndertBeiNurGesetztenModellenNichtsUndNenntKeinenGrund(
    dienst, aufstellungNachDerZonenwahl, spielerEins, boyz
):
    modelleSetzen(aufstellungNachDerZonenwahl, boyz, len(boyz.modelle))
    auswählen(dienst, "Boyz")
    davor = spielstandVon(dienst)
    stelle = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, mitteDerZone, 50)

    antwort = karteAnklicken(dienst, stelle)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == davor
