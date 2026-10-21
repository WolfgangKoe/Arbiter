"""AUF-26 · Klemmen beim Ziehen."""

from http import HTTPStatus

import pytest
from playwright.sync_api import expect

from tests.akzeptanz.anhalten import (
    anDerHineingerücktenStelle,
    blockVorEinerFremdenBase,
    ebeneAufDasModellLegen,
    freiesZiel,
    geradeAufDieBase,
    gesetzteMit,
    hineinrückenOhneBase,
    liegtAufDerStrecke,
    liegtNahAnDerStrecke,
    schrägAufDieBase,
    schrägÜberDieGrenze,
    stellenAlsZahlen,
    stellenDesZugs,
    stößtAn,
    überdecktEine,
)
from tests.akzeptanz.bildschirm import seiteMitEingabe, sperrmeldungenDerSeite
from tests.akzeptanz.dienst import (
    auswählen,
    modellLoslassen,
    spielstandVon,
    stelleBeimLoslassenAbfragen,
    stelleImSpielstand,
    stellenDerAbfrage,
    stellenDerEinheitIm,
)
from tests.akzeptanz.handgriffe import (
    einheitAufstellen,
    erwarteteStelle,
    gezogenesUndRest,
    inZoll,
    millionstel,
    modelleAnStellenSetzen,
    modelleSetzen,
    radiusInZoll,
    stelleInDerZoneDesSpielersAnDerReihe,
    tiefeDerZone,
    wegVon,
    welchesGezogenWird,
)
from tests.akzeptanz.ziehen import (
    haltenUndLosslassen,
    liegtEinPixelGenauAn,
    mitMausUndFinger,
    modellZiehen,
    zollJePixel,
)

# Warum: Der Dienst liest den gesendeten Weg als Dezimalzahl (S2), das weicht um Rundung ab
dezimalFehler = 1e-9

# Warum: Ziel in Zoll; erwartet als (Zoll, Radien) für Tiefe und Länge des Modells
hineinrücken = pytest.mark.parametrize(
    ("ziel", "erwartet"),
    [
        ((12, 20), ((9, -1), (20, 0))),
        ((-3, 20), ((0, 1), (20, 0))),
        ((4, -5), ((4, 0), (0, 1))),
        ((4, 65), ((4, 0), (60, -1))),
        ((12, 65), ((9, -1), (60, -1))),
        ((40, 20), ((9, -1), (20, 0))),
    ],
    ids=[
        "überDieInnenkante",
        "überDieSpielfeldkante",
        "amAnfang",
        "amEnde",
        "inDerEcke",
        "inDerZoneDesAnderen",
    ],
)


@hineinrücken
def testAuf26_1EinModellAußerhalbDerZoneRücktAufKürzestemWegHineinOhneGrund(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, ziel, erwartet
):
    [(modell, _)] = modelleSetzen(aufstellung, ersteEinheitDesSpielersAnDerReihe, 1)
    tiefe, länge = ziel
    stelleDesLoslassens = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefe, länge)
    stelleNachDemRücken = erwarteteStelle(aufstellung, radiusInZoll(modell), erwartet)

    aufstellung.modellLoslassen(modell, stelleDesLoslassens)

    assert aufstellung.gesetzt(modell)
    assert aufstellung.stelle(modell) == stelleNachDemRücken


def testAuf26_1EineBaseDieDieGrenzeDerZoneBerührtBleibtDortOhneGrund(
    aufstellung, ersteEinheitDesSpielersAnDerReihe
):
    [(modell, _)] = modelleSetzen(aufstellung, ersteEinheitDesSpielersAnDerReihe, 1)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, tiefeDerZone - radiusInZoll(modell), 20
    )

    aufstellung.modellLoslassen(modell, ziel)

    assert aufstellung.gesetzt(modell)
    assert aufstellung.stelle(modell) == ziel


def testAuf26_1EineBaseEinMillionstelZollJenseitsDerGrenzeRücktAnDieGrenzeOhneGrund(
    aufstellung, ersteEinheitDesSpielersAnDerReihe
):
    [(modell, _)] = modelleSetzen(aufstellung, ersteEinheitDesSpielersAnDerReihe, 1)
    radius = radiusInZoll(modell)
    grenze = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefeDerZone - radius, 20)
    knappDrüber = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, tiefeDerZone - radius + millionstel, 20
    )

    aufstellung.modellLoslassen(modell, knappDrüber)

    assert aufstellung.gesetzt(modell)
    assert aufstellung.stelle(modell) == grenze


@hineinrücken
def testAuf26_1DerDienstRücktDasModellHineinOhneGrund(
    dienst, aufstellungNachDerZonenwahl, boyz, ziel, erwartet
):
    aufstellung = aufstellungNachDerZonenwahl
    [(modell, _)] = modelleSetzen(aufstellung, boyz, 1)
    tiefe, länge = ziel
    stelleDesLoslassens = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefe, länge)
    stelleNachDemRücken = erwarteteStelle(aufstellung, radiusInZoll(modell), erwartet)

    antwort = modellLoslassen(dienst, aufstellung, boyz, modell, stelleDesLoslassens)

    spielstand = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(spielstand, "Boyz") == {1: stelleImSpielstand(stelleNachDemRücken)}


@mitMausUndFinger
def testAuf26_1DieSeiteRücktDasModellInnerhalbDerKarteHineinOhneGrund(
    bildschirm, aufstellungNachDerZonenwahl, boyz, eingabe
):
    aufstellung = aufstellungNachDerZonenwahl
    [(modell, davor)] = modelleSetzen(aufstellung, boyz, 1)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 12, 20)
    stelleNachDemRücken = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, tiefeDerZone - radiusInZoll(modell), 20
    )
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)

    modellZiehen(seite, davor, ziel, eingabe)

    assert aufstellung.gesetzt(modell)
    assert liegtEinPixelGenauAn(seite, aufstellung.stelle(modell), stelleNachDemRücken)
    expect(seite.locator(".karte .modell")).to_have_count(1)
    assert sperrmeldungenDerSeite(seite) == []


zügeZumAnhalten = pytest.mark.parametrize(
    "zug",
    [geradeAufDieBase, schrägAufDieBase, anDerHineingerücktenStelle],
    ids=["gerade", "schräg", "anDerHineingerücktenStelle"],
)
zügeFürDieAbfrage = pytest.mark.parametrize(
    "zug",
    [
        geradeAufDieBase,
        schrägAufDieBase,
        anDerHineingerücktenStelle,
        schrägÜberDieGrenze,
        freiesZiel,
        hineinrückenOhneBase,
    ],
    ids=[
        "gerade",
        "schräg",
        "anDerHineingerücktenStelle",
        "schrägÜberDieGrenze",
        "freiesZiel",
        "hineinrückenOhneBase",
    ],
)
welchesGetroffenWird = pytest.mark.parametrize(
    "zweitesGetroffen", [False, True], ids=["erstesGetroffen", "zweitesGetroffen"]
)


def nichtAuswählen(aufstellung, einheit, modell):
    """Die Einheit bleibt, wie sie ist: nicht ausgewählt."""


mitUndOhneEbene = pytest.mark.parametrize(
    "ebeneLegen",
    [nichtAuswählen, ebeneAufDasModellLegen],
    ids=["nichtAusgewählt", "ebeneIstEinModell"],
)


def warbossVorDenBoyz(aufstellung, warboss):
    """Der Warboss steht in der zweiten Reihe, sein Ziel 2″ tief überdeckt die Boyz der ersten."""
    [(modell, davor)] = modelleSetzen(aufstellung, warboss, 1)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 2, davor.y)
    return modell, davor, ziel


@zügeZumAnhalten
def testAuf26_2EinModellHältAufDerGeradenStreckeAnDerBaseAnOhneGrund(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, zug
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    modell, modellImWeg = einheit.modelle
    davor, stelleDesLoslassens, stelleImWeg, ende = stellenDesZugs(
        aufstellung, radiusInZoll(modell), zug
    )
    modelleAnStellenSetzen(aufstellung, einheit, [davor, stelleImWeg])

    aufstellung.modellLoslassen(modell, stelleDesLoslassens)

    stelle = aufstellung.stelle(modell)
    imWeg = [(modellImWeg, stelleImWeg)]
    assert liegtAufDerStrecke(davor, ende, stelle)
    assert not überdecktEine([(modell, stelle)], imWeg)
    assert stößtAn([(modell, stelle)], imWeg)
    assert aufstellung.stelle(modellImWeg) == stelleImWeg


def testAuf26_2AuchWennDieEbeneEinModellIstHältEsAnDerBaseAn(
    aufstellung, ersteEinheitDesSpielersAnDerReihe
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    modell, modellImWeg = einheit.modelle
    davor, stelleDesLoslassens, stelleImWeg, ende = stellenDesZugs(
        aufstellung, radiusInZoll(modell), geradeAufDieBase
    )
    modelleAnStellenSetzen(aufstellung, einheit, [davor, stelleImWeg])
    ebeneAufDasModellLegen(aufstellung, einheit, modell)

    aufstellung.modellLoslassen(modell, stelleDesLoslassens)

    stelle = aufstellung.stelle(modell)
    imWeg = [(modellImWeg, stelleImWeg)]
    assert liegtAufDerStrecke(davor, ende, stelle)
    assert not überdecktEine([(modell, stelle)], imWeg)
    assert stößtAn([(modell, stelle)], imWeg)


def testAuf26_2KreuztDieStreckeEineBaseUndÜberdecktDasZielEineAndereHältEsAnDerErstenAn(
    aufstellungNachDerZonenwahl, boyz
):
    aufstellung = aufstellungNachDerZonenwahl
    modell, ersteBase, zweiteBase, *_ = boyz.modelle
    radius = radiusInZoll(modell)
    davor = erwarteteStelle(aufstellung, radius, ((4, 0), (20, 0)))
    stelleDerErstenBase = erwarteteStelle(aufstellung, radius, ((4, 0), (26, 0)))
    stelleDerZweitenBase = erwarteteStelle(aufstellung, radius, ((4, 0), (32, 0)))
    ziel = erwarteteStelle(aufstellung, radius, ((4, 0), (33, 0)))
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleDerErstenBase, stelleDerZweitenBase])

    aufstellung.modellLoslassen(modell, ziel)

    stelle = aufstellung.stelle(modell)
    bases = [(ersteBase, stelleDerErstenBase), (zweiteBase, stelleDerZweitenBase)]
    assert liegtAufDerStrecke(davor, ziel, stelle)
    assert not überdecktEine([(modell, stelle)], bases)
    assert stößtAn([(modell, stelle)], [(ersteBase, stelleDerErstenBase)])


def testAuf26_2KreuztDieStreckeNurEineBaseUndLiegtDasZielFreiStehtDasModellAmZiel(
    aufstellung, ersteEinheitDesSpielersAnDerReihe
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    modell, _ = einheit.modelle
    radius = radiusInZoll(modell)
    davor = erwarteteStelle(aufstellung, radius, ((4, 0), (20, 0)))
    stelleImWeg = erwarteteStelle(aufstellung, radius, ((4, 0), (30, 0)))
    ziel = erwarteteStelle(aufstellung, radius, ((4, 0), (40, 0)))
    modelleAnStellenSetzen(aufstellung, einheit, [davor, stelleImWeg])

    aufstellung.modellLoslassen(modell, ziel)

    assert aufstellung.stelle(modell) == ziel


def testAuf26_2BerührtDieBaseAmZielDieEineAndereNurStehtDasModellAmZiel(
    aufstellung, ersteEinheitDesSpielersAnDerReihe
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    modell, _ = einheit.modelle
    radius = radiusInZoll(modell)
    davor = erwarteteStelle(aufstellung, radius, ((4, 0), (20, 0)))
    ziel = erwarteteStelle(aufstellung, radius, ((4, 0), (30, 0)))
    stelleImWeg = erwarteteStelle(aufstellung, radius, ((4, 2), (30, 0)))
    modelleAnStellenSetzen(aufstellung, einheit, [davor, stelleImWeg])

    aufstellung.modellLoslassen(modell, ziel)

    assert aufstellung.stelle(modell) == ziel


def testAuf26_2ÜberdecktDieBaseAmZielEineAndereUmEinMillionstelZollHältEsAnDerBaseAn(
    aufstellung, ersteEinheitDesSpielersAnDerReihe
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    modell, modellImWeg = einheit.modelle
    radius = radiusInZoll(modell)
    davor = erwarteteStelle(aufstellung, radius, ((4, 0), (20, 0)))
    ziel = erwarteteStelle(aufstellung, radius, ((4, 0), (30, 0)))
    stelleImWeg = erwarteteStelle(aufstellung, radius, ((4 - millionstel, 2), (30, 0)))
    modelleAnStellenSetzen(aufstellung, einheit, [davor, stelleImWeg])

    aufstellung.modellLoslassen(modell, ziel)

    stelle = aufstellung.stelle(modell)
    imWeg = [(modellImWeg, stelleImWeg)]
    assert liegtAufDerStrecke(davor, ziel, stelle)
    assert not überdecktEine([(modell, stelle)], imWeg)
    assert stößtAn([(modell, stelle)], imWeg)


@mitUndOhneEbene
def testAuf26_2EinModellHältAnDerBaseEinesModellsEinerAnderenEinheitAnOhneGrund(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, andereEinheitAufgestellt, ebeneLegen
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    modell, _ = einheit.modelle
    [fremdesModell] = andereEinheitAufgestellt.modelle
    stelleDesFremden = aufstellung.stelle(fremdesModell)
    davor = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 4, 10)
    modelleAnStellenSetzen(aufstellung, einheit, [davor])
    ebeneLegen(aufstellung, einheit, modell)

    aufstellung.modellLoslassen(modell, stelleDesFremden)

    stelle = aufstellung.stelle(modell)
    fremde = [(fremdesModell, stelleDesFremden)]
    assert liegtAufDerStrecke(davor, stelleDesFremden, stelle)
    assert not überdecktEine([(modell, stelle)], fremde)
    assert stößtAn([(modell, stelle)], fremde)
    assert aufstellung.stelle(fremdesModell) == stelleDesFremden


def testAuf26_2ZielDerStreckeIstDieHineingerückteStelleNichtDerPunktDesLoslassens(
    aufstellung, ersteEinheitDesSpielersAnDerReihe
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    modell, modellImWeg = einheit.modelle
    davor, stelleDesLoslassens, stelleImWeg, ende = stellenDesZugs(
        aufstellung, radiusInZoll(modell), schrägÜberDieGrenze
    )
    modelleAnStellenSetzen(aufstellung, einheit, [davor, stelleImWeg])

    aufstellung.modellLoslassen(modell, stelleDesLoslassens)

    stelle = aufstellung.stelle(modell)
    imWeg = [(modellImWeg, stelleImWeg)]
    assert liegtNahAnDerStrecke(davor, ende, stelle, dezimalFehler)
    assert not überdecktEine([(modell, stelle)], imWeg)
    assert stößtAn([(modell, stelle)], imWeg)


def testAuf26_2DerDienstSetztDasModellAnDieBaseAnOhneGrund(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    aufstellung = aufstellungNachDerZonenwahl
    modell, modellImWeg, *_ = boyz.modelle
    davor, stelleDesLoslassens, stelleImWeg, ende = stellenDesZugs(
        aufstellung, radiusInZoll(modell), geradeAufDieBase
    )
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleImWeg])

    antwort = modellLoslassen(dienst, aufstellung, boyz, modell, stelleDesLoslassens)

    stelle = aufstellung.stelle(modell)
    imWeg = [(modellImWeg, stelleImWeg)]
    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(antwort.get_json(), "Boyz") == {
        1: stelleImSpielstand(stelle),
        2: stelleImSpielstand(stelleImWeg),
    }
    assert liegtAufDerStrecke(davor, ende, stelle)
    assert not überdecktEine([(modell, stelle)], imWeg)
    assert stößtAn([(modell, stelle)], imWeg)


@mitMausUndFinger
def testAuf26_2DieSeiteSetztDasModellAnDieBaseAnOhneGrund(
    bildschirm, aufstellungNachDerZonenwahl, boyz, eingabe
):
    aufstellung = aufstellungNachDerZonenwahl
    modell, modellImWeg, *_ = boyz.modelle
    davor, stelleDesLoslassens, stelleImWeg, ende = stellenDesZugs(
        aufstellung, radiusInZoll(modell), geradeAufDieBase
    )
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleImWeg])
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)

    modellZiehen(seite, davor, stelleDesLoslassens, eingabe)

    stelle = aufstellung.stelle(modell)
    imWeg = [(modellImWeg, stelleImWeg)]
    assert aufstellung.gesetzt(modell)
    assert liegtNahAnDerStrecke(davor, ende, stelle, zollJePixel(seite))
    assert not überdecktEine([(modell, stelle)], imWeg)
    assert stößtAn([(modell, stelle)], imWeg)
    expect(seite.locator(".karte .modell")).to_have_count(2)
    assert sperrmeldungenDerSeite(seite) == []


@welchesGezogenWird
@welchesGetroffenWird
def testAuf26_3TrifftEinModellDerEinheitEineBaseEinerAnderenEinheitKürztDerBlockDenGemeinsamenWeg(
    aufstellung,
    ersteEinheitDesSpielersAnDerReihe,
    andereEinheitAufgestellt,
    zweitesGezogen,
    zweitesGetroffen,
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    [fremdesModell] = andereEinheitAufgestellt.modelle
    zug = blockVorEinerFremdenBase(
        aufstellung,
        einheit,
        fremdesModell,
        zweitesGetroffen=zweitesGetroffen,
        zweitesGezogen=zweitesGezogen,
    )
    fremde = gesetzteMit(aufstellung, [fremdesModell])

    aufstellung.modellLoslassen(zug.gezogenes, zug.ziel)

    block = gesetzteMit(aufstellung, einheit.modelle)
    wege = {
        wegVon(davor, danach) for (_, davor), (_, danach) in zip(zug.gesetzte, block, strict=True)
    }
    stelleDesGezogenen = aufstellung.stelle(zug.gezogenes)
    assert len(wege) == 1
    assert liegtAufDerStrecke(zug.davor, zug.ziel, stelleDesGezogenen)
    assert stelleDesGezogenen != zug.ziel
    assert not überdecktEine(block, fremde)
    assert stößtAn(block, fremde)


@welchesGezogenWird
@welchesGetroffenWird
def testAuf26_3BerührtDieBaseDerEinheitDieEinerAnderenNurRücktDerBlockGanzVor(
    aufstellung,
    ersteEinheitDesSpielersAnDerReihe,
    andereEinheitAufgestellt,
    zweitesGezogen,
    zweitesGetroffen,
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    [fremdesModell] = andereEinheitAufgestellt.modelle
    zug = blockVorEinerFremdenBase(
        aufstellung,
        einheit,
        fremdesModell,
        zweitesGetroffen=zweitesGetroffen,
        zweitesGezogen=zweitesGezogen,
    )
    radius = radiusInZoll(zug.gezogenes)
    ziel = erwarteteStelle(aufstellung, radius, ((4, 2), (zug.davor.y, 0)))

    aufstellung.modellLoslassen(zug.gezogenes, ziel)

    wege = {wegVon(davor, aufstellung.stelle(modell)) for modell, davor in zug.gesetzte}
    assert aufstellung.stelle(zug.gezogenes) == ziel
    assert wege == {wegVon(zug.davor, ziel)}


@welchesGezogenWird
@welchesGetroffenWird
def testAuf26_3ÜberdecktEineBaseDerEinheitDieEinerAnderenUmEinMillionstelZollKürztDerBlock(
    aufstellung,
    ersteEinheitDesSpielersAnDerReihe,
    andereEinheitAufgestellt,
    zweitesGezogen,
    zweitesGetroffen,
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    [fremdesModell] = andereEinheitAufgestellt.modelle
    zug = blockVorEinerFremdenBase(
        aufstellung,
        einheit,
        fremdesModell,
        zweitesGetroffen=zweitesGetroffen,
        zweitesGezogen=zweitesGezogen,
    )
    radius = radiusInZoll(zug.gezogenes)
    ziel = erwarteteStelle(aufstellung, radius, ((4 - millionstel, 2), (zug.davor.y, 0)))
    fremde = gesetzteMit(aufstellung, [fremdesModell])

    aufstellung.modellLoslassen(zug.gezogenes, ziel)

    block = gesetzteMit(aufstellung, einheit.modelle)
    stelleDesGezogenen = aufstellung.stelle(zug.gezogenes)
    assert liegtAufDerStrecke(zug.davor, ziel, stelleDesGezogenen)
    assert stelleDesGezogenen != ziel
    assert not überdecktEine(block, fremde)
    assert stößtAn(block, fremde)


def andereEinheitAnDerInnenkante(aufstellung, ersterSpieler, zweiterSpieler, länge):
    """Das Modell der zweiten Einheit steht an der hineingerückten Stelle; der erste ist dran."""
    _, andereEinheit = ersterSpieler.armee.einheiten
    einheitDesAnderenSpielers, _ = zweiterSpieler.armee.einheiten
    [fremdesModell] = andereEinheit.modelle
    tiefe = inZoll((tiefeDerZone, -1), radiusInZoll(fremdesModell))
    stelle = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefe, länge)
    aufstellung.modellSetzen(fremdesModell, stelle)
    aufstellung.aufstellenDerEinheitBeenden()
    einheitAufstellen(aufstellung, einheitDesAnderenSpielers)
    return fremdesModell


@welchesGezogenWird
def testAuf26_3NachDemHineinrückenKürztDerBlockDenWegVorEinerBaseAnDerHineingerücktenStelle(
    aufstellung,
    ersterSpieler,
    zweiterSpieler,
    ersteEinheitDesSpielersAnDerReihe,
    zweitesGezogen,
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    erstes, _ = einheit.modelle
    radius = radiusInZoll(erstes)
    längeDesGetroffenen = 20
    fremdesModell = andereEinheitAnDerInnenkante(
        aufstellung, ersterSpieler, zweiterSpieler, längeDesGetroffenen
    )
    stellen = [
        stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 5, länge)
        for länge in (längeDesGetroffenen, längeDesGetroffenen + 2 * radius)
    ]
    gesetzte = modelleAnStellenSetzen(aufstellung, einheit, stellen)
    aufstellung.auswählen(einheit)
    (gezogenes, davor), _ = gezogenesUndRest(gesetzte, zweitesGezogen=zweitesGezogen)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 12, davor.y)
    hineingerückt = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, inZoll((tiefeDerZone, -1), radius), davor.y
    )
    fremde = gesetzteMit(aufstellung, [fremdesModell])

    aufstellung.modellLoslassen(gezogenes, ziel)

    block = gesetzteMit(aufstellung, einheit.modelle)
    wege = {
        wegVon(vorher, danach) for (_, vorher), (_, danach) in zip(gesetzte, block, strict=True)
    }
    stelleDesGezogenen = aufstellung.stelle(gezogenes)
    assert len(wege) == 1
    assert liegtAufDerStrecke(davor, hineingerückt, stelleDesGezogenen)
    assert stelleDesGezogenen != hineingerückt
    assert not überdecktEine(block, fremde)
    assert stößtAn(block, fremde)


def testAuf26_3DerDienstKürztDenWegDerEinheitVorDerBaseEinerAnderenOhneGrund(
    aufstellungMitModellenBeiderSpieler, dienst, warboss, boyz
):
    aufstellung = aufstellungMitModellenBeiderSpieler
    modell, davor, ziel = warbossVorDenBoyz(aufstellung, warboss)
    auswählen(dienst, "Warboss")
    fremde = gesetzteMit(aufstellung, boyz.modelle)

    antwort = modellLoslassen(dienst, aufstellung, warboss, modell, ziel)

    stelle = aufstellung.stelle(modell)
    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(antwort.get_json(), "Warboss") == {1: stelleImSpielstand(stelle)}
    assert liegtNahAnDerStrecke(davor, ziel, stelle, dezimalFehler)
    assert stelle != ziel
    assert not überdecktEine([(modell, stelle)], fremde)
    assert stößtAn([(modell, stelle)], fremde)


@mitMausUndFinger
def testAuf26_3DieSeiteKürztDenWegDerEinheitVorDerBaseEinerAnderenOhneGrund(
    bildschirm, aufstellungMitModellenBeiderSpieler, warboss, boyz, eingabe
):
    aufstellung = aufstellungMitModellenBeiderSpieler
    modell, davor, ziel = warbossVorDenBoyz(aufstellung, warboss)
    aufstellung.auswählen(warboss)
    fremde = gesetzteMit(aufstellung, boyz.modelle)
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)

    modellZiehen(seite, davor, ziel, eingabe)

    stelle = aufstellung.stelle(modell)
    assert aufstellung.gesetzt(modell)
    assert not liegtEinPixelGenauAn(seite, stelle, ziel)
    assert not überdecktEine([(modell, stelle)], fremde)
    assert stößtAn([(modell, stelle)], fremde)
    assert sperrmeldungenDerSeite(seite) == []


@zügeFürDieAbfrage
@mitUndOhneEbene
def testAuf26_4DieAbfrageNenntNurDasAlleinGezogeneModellUndSetztNichts(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, zug, ebeneLegen
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    modell, modellImWeg = einheit.modelle
    davor, stelleDesLoslassens, stelleImWeg, _ = stellenDesZugs(
        aufstellung, radiusInZoll(modell), zug
    )
    modelleAnStellenSetzen(aufstellung, einheit, [davor, stelleImWeg])
    ebeneLegen(aufstellung, einheit, modell)

    abfrage = aufstellung.stellenBeimLoslassen(modell, stelleDesLoslassens)

    assert set(abfrage) == {modell}
    assert aufstellung.stelle(modell) == davor
    assert aufstellung.stelle(modellImWeg) == stelleImWeg


@zügeFürDieAbfrage
@mitUndOhneEbene
def testAuf26_4BeimLoslassenStehtDasModellDortWoDieAbfrageEsZeigte(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, zug, ebeneLegen
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    modell, _ = einheit.modelle
    davor, stelleDesLoslassens, stelleImWeg, _ = stellenDesZugs(
        aufstellung, radiusInZoll(modell), zug
    )
    modelleAnStellenSetzen(aufstellung, einheit, [davor, stelleImWeg])
    ebeneLegen(aufstellung, einheit, modell)
    gezeigt = aufstellung.stellenBeimLoslassen(modell, stelleDesLoslassens)

    aufstellung.modellLoslassen(modell, stelleDesLoslassens)

    assert aufstellung.stelle(modell) == gezeigt[modell]


@zügeFürDieAbfrage
def testAuf26_4DerDienstNenntDieStelleBeimLoslassenNurDesGezogenenModells(
    dienst, aufstellungNachDerZonenwahl, boyz, zug
):
    aufstellung = aufstellungNachDerZonenwahl
    modell, *_ = boyz.modelle
    davor, stelleDesLoslassens, stelleImWeg, _ = stellenDesZugs(
        aufstellung, radiusInZoll(modell), zug
    )
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleImWeg])
    erwartet = aufstellung.stellenBeimLoslassen(modell, stelleDesLoslassens)
    spielstandDavor = spielstandVon(dienst)

    antwort = stelleBeimLoslassenAbfragen(dienst, aufstellung, boyz, modell, stelleDesLoslassens)

    abgefragt = antwort.get_json()
    assert antwort.status_code == HTTPStatus.OK
    assert len(abgefragt["modelle"]) == 1
    assert stellenDerEinheitIm(abgefragt, "Boyz") == stellenDerAbfrage(boyz, erwartet)
    assert spielstandVon(dienst) == spielstandDavor


@mitMausUndFinger
@pytest.mark.parametrize(
    "zug",
    [geradeAufDieBase, anDerHineingerücktenStelle],
    ids=["gerade", "anDerHineingerücktenStelle"],
)
def testAuf26_4DieKarteZeigtBeimHaltenDasModellDortWoEsBeimLoslassenStehtNichtUnterDemZeiger(
    bildschirm, aufstellungNachDerZonenwahl, boyz, zug, eingabe
):
    aufstellung = aufstellungNachDerZonenwahl
    modell, *_ = boyz.modelle
    davor, stelleDesLoslassens, stelleImWeg, _ = stellenDesZugs(
        aufstellung, radiusInZoll(modell), zug
    )
    modelleAnStellenSetzen(aufstellung, boyz, [davor, stelleImWeg])
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)

    gezeigt = haltenUndLosslassen(seite, davor, stelleDesLoslassens, eingabe)

    assert gezeigt == stellenAlsZahlen(aufstellung)
    assert not liegtEinPixelGenauAn(seite, aufstellung.stelle(modell), stelleDesLoslassens)
