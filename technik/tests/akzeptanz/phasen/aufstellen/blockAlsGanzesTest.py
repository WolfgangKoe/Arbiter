"""AUF-24 · Block als Ganzes."""

from fractions import Fraction
from http import HTTPStatus
from urllib.parse import urlparse

import pytest
from playwright.sync_api import expect

from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.anhalten import blockVorEinerFremdenBase, stellenAlsZahlen
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    kreiseDerKarte,
    seiteMitEingabe,
    sperrmeldungenDerSeite,
)
from tests.akzeptanz.dienst import (
    auswählen,
    modellLoslassen,
    spielstandDesVertrags,
    spielstandVon,
    stelleBeimLoslassenAbfragen,
    stelleBeimLoslassenDesVertrags,
    stelleImSpielstand,
    stellenDerAbfrage,
    stellenDerEinheitIm,
    stellenDesVertrags,
)
from tests.akzeptanz.handgriffe import (
    gezogenesUndRest,
    inZoll,
    modelleAnStellenSetzen,
    modelleSetzen,
    radiusInZoll,
    stelleInDerZoneDesSpielersAnDerReihe,
    tiefeDerZone,
    welchesGezogenWird,
)
from tests.akzeptanz.ziehen import (
    halten,
    haltenUndLosslassen,
    liegtEinPixelGenauAn,
    mitMausUndFinger,
    modellZiehen,
    punktAufDerKarte,
    zollJePixel,
)

# Warum: Radius und Durchmesser, vor und zurück, damit keine Prüfreihenfolge verschont bleibt
verschiebungenInRadien = pytest.mark.parametrize(
    "radien", [1, -1, 2, -2], ids=["umEinenRadiusVor", "umEinenRadiusZurück", "vor2", "zurück2"]
)
tiefeDerReihe = 4
längeDesErsten = 20


def stellenDerReihe(aufstellung, radius) -> list[Stelle]:
    """Zwei Bases Rand an Rand entlang y, weit genug von allen Rändern der Zone."""
    return [
        stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefeDerReihe, längeDesErsten),
        stelleInDerZoneDesSpielersAnDerReihe(
            aufstellung, tiefeDerReihe, längeDesErsten + 2 * radius
        ),
    ]


def verschobeneStelle(stelle: Stelle, radien: int, radius) -> Stelle:
    # Warum: Die Reihe liegt entlang y, die Tiefe x bleibt
    return Stelle(x=stelle.x, y=stelle.y + radien * radius)


# Warum: Ziel in Tiefe und Länge in Zoll; der Block aus drei Boyz verschiebt sich, rückt hinein
zieleDesBlocks = pytest.mark.parametrize(
    "ziel", [(4, 20), (12, 20)], ids=["verschieben", "hineinrücken"]
)


@zieleDesBlocks
def testAuf24_1DieAbfrageNenntJedesGesetzteModellDerEinheitUndSetztNichts(
    aufstellungNachDerZonenwahl, boyz, ziel
):
    aufstellung = aufstellungNachDerZonenwahl
    gesetzte = modelleSetzen(aufstellung, boyz, 3)
    [(gezogenes, _), *_] = gesetzte
    aufstellung.auswählen(boyz)
    tiefe, länge = ziel
    stelleDesLoslassens = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefe, länge)

    abfrage = aufstellung.stellenBeimLoslassen(gezogenes, stelleDesLoslassens)

    assert set(abfrage) == {modell for modell, _ in gesetzte}
    for modell, davor in gesetzte:
        assert aufstellung.stelle(modell) == davor


@zieleDesBlocks
def testAuf24_1BeimLoslassenStehtJedesModellDortWoDieAbfrageEsZeigte(
    aufstellungNachDerZonenwahl, boyz, ziel
):
    aufstellung = aufstellungNachDerZonenwahl
    gesetzte = modelleSetzen(aufstellung, boyz, 3)
    [(gezogenes, _), *_] = gesetzte
    aufstellung.auswählen(boyz)
    tiefe, länge = ziel
    stelleDesLoslassens = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefe, länge)
    gezeigt = aufstellung.stellenBeimLoslassen(gezogenes, stelleDesLoslassens)

    aufstellung.modellLoslassen(gezogenes, stelleDesLoslassens)

    for modell, _ in gesetzte:
        assert aufstellung.stelle(modell) == gezeigt[modell]


@welchesGezogenWird
def testAuf24_1VorEinerBaseEinerAnderenEinheitStehtJedesModellDortWoDieAbfrageEsZeigte(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, andereEinheitAufgestellt, zweitesGezogen
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    [fremdesModell] = andereEinheitAufgestellt.modelle
    zug = blockVorEinerFremdenBase(
        aufstellung, einheit, fremdesModell, zweitesGetroffen=False, zweitesGezogen=zweitesGezogen
    )
    gezeigt = aufstellung.stellenBeimLoslassen(zug.gezogenes, zug.ziel)

    aufstellung.modellLoslassen(zug.gezogenes, zug.ziel)

    for modell, _ in zug.gesetzte:
        assert aufstellung.stelle(modell) == gezeigt[modell]
    assert aufstellung.stelle(zug.gezogenes) != zug.ziel


def testAuf24_1DerDienstNenntDieStellenDesBlocksWieDasBeispielImVertrag(dienstDesBeispiels):
    auswählen(dienstDesBeispiels, "Necron Warriors")

    antwort = dienstDesBeispiels.get(
        "/api/spieler/2/einheiten/1/modelle/1/stelleBeimLoslassen", query_string={"x": 35, "y": 28}
    )

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == stelleBeimLoslassenDesVertrags()


def testAuf24_1DerDienstNenntJedesGesetzteModellDerEinheitUndVerändertNichts(
    dienst, aufstellungNachDerZonenwahl, boyz
):
    aufstellung = aufstellungNachDerZonenwahl
    [(gezogenes, _), *_] = modelleSetzen(aufstellung, boyz, 3)
    auswählen(dienst, "Boyz")
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 12, 20)
    erwartet = aufstellung.stellenBeimLoslassen(gezogenes, ziel)
    spielstandDavor = spielstandVon(dienst)

    antwort = stelleBeimLoslassenAbfragen(dienst, aufstellung, boyz, gezogenes, ziel)

    assert antwort.status_code == HTTPStatus.OK
    assert stellenDerEinheitIm(antwort.get_json(), "Boyz") == stellenDerAbfrage(boyz, erwartet)
    assert len(antwort.get_json()["modelle"]) == len(erwartet)
    assert spielstandVon(dienst) == spielstandDavor


@pytest.mark.parametrize("eingabe", ["maus", "finger"])
def testAuf24_1DieKarteZeigtBeimHaltenJedesModellDortWoEsBeimLoslassenStehtOhneSperre(
    bildschirm, aufstellungNachDerZonenwahl, boyz, eingabe
):
    aufstellung = aufstellungNachDerZonenwahl
    [(_, davor), *_] = modelleSetzen(aufstellung, boyz, 3)
    aufstellung.auswählen(boyz)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 12, 20)
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)

    gezeigt = haltenUndLosslassen(seite, davor, ziel, eingabe)

    assert gezeigt == stellenAlsZahlen(aufstellung)
    assert sperrmeldungenDerSeite(seite) == []


@mitMausUndFinger
def testAuf24_1DieKarteZeigtBeimHaltenDenBlockVorEinerFremdenBaseDortWoErBeimLoslassenSteht(
    bildschirm,
    aufstellung,
    ersteEinheitDesSpielersAnDerReihe,
    andereEinheitAufgestellt,
    eingabe,
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    [fremdesModell] = andereEinheitAufgestellt.modelle
    zug = blockVorEinerFremdenBase(
        aufstellung, einheit, fremdesModell, zweitesGetroffen=False, zweitesGezogen=False
    )
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)

    gezeigt = haltenUndLosslassen(seite, zug.davor, zug.ziel, eingabe)

    assert gezeigt == stellenAlsZahlen(aufstellung)
    assert aufstellung.stelle(zug.gezogenes) != zug.ziel
    assert sperrmeldungenDerSeite(seite) == []


def seiteMitDerAbfrageDesVertrags(bildschirm, ausgangsaufstellung):
    """Spielstand, Abfrage und Antwort aufs Loslassen liefern die Beispiele des Vertrags."""
    spielstand = spielstandDesVertrags()
    return bildschirm.seiteMitSpielstand(
        ausgangsaufstellung,
        spielstand,
        {
            "**/stelleBeimLoslassen*": stelleBeimLoslassenDesVertrags(),
            "**/modelle/1/stelle": spielstand,
        },
    )


# Regel: handlungen.md, V10, das Beispiel gilt für x=35 und y=28
stelleDesLoslassensImBeispiel = Stelle(x=Fraction(35), y=Fraction(28))


def testAuf24_1DieSeiteSetztBeimHaltenDieKreiseAnDieStellenDerAntwortImBeispiel(
    bildschirm, ausgangsaufstellung
):
    seite = seiteMitDerAbfrageDesVertrags(bildschirm, ausgangsaufstellung)
    gehaltenes, _, _ = stellenDesVertrags(2)

    halten(seite, gehaltenes, stelleDesLoslassensImBeispiel, "maus")

    modelle = stelleBeimLoslassenDesVertrags()["modelle"]
    assert kreiseDerKarte(seite) == {(modell["x"], modell["y"]) for modell in modelle}


def testAuf24_1DieSeiteSendetBeimLoslassenDenPunktDesZeigersNichtDenGezeigten(
    bildschirm, ausgangsaufstellung
):
    seite = seiteMitDerAbfrageDesVertrags(bildschirm, ausgangsaufstellung)
    gehaltenes, _, _ = stellenDesVertrags(2)
    zielPunkt = punktAufDerKarte(seite, stelleDesLoslassensImBeispiel)
    zeiger = halten(seite, gehaltenes, stelleDesLoslassensImBeispiel, "maus")

    with aufDieHandlungWarten(seite) as antwort:
        zeiger.loslassen(zielPunkt)

    anfrage = antwort.value.request
    gesendet = anfrage.post_data_json
    toleranz = zollJePixel(seite)
    assert (anfrage.method, urlparse(anfrage.url).path) == (
        "PUT",
        "/api/spieler/2/einheiten/1/modelle/1/stelle",
    )
    assert abs(gesendet["x"] - float(stelleDesLoslassensImBeispiel.x)) <= toleranz
    assert abs(gesendet["y"] - float(stelleDesLoslassensImBeispiel.y)) <= toleranz


@verschiebungenInRadien
@welchesGezogenWird
def testAuf24_2KeinModellDesBlocksIstWegenEinesModellsDerselbenEinheitGesperrt(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, radien, zweitesGezogen
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    erstes, _ = einheit.modelle
    radius = radiusInZoll(erstes)
    stellen = stellenDerReihe(aufstellung, radius)
    gesetzte = modelleAnStellenSetzen(aufstellung, einheit, stellen)
    aufstellung.auswählen(einheit)
    (erstes, stelleErstes), (zweites, stelleZweites) = gesetzte
    (gezogenes, davor), _ = gezogenesUndRest(gesetzte, zweitesGezogen=zweitesGezogen)

    aufstellung.modellLoslassen(gezogenes, verschobeneStelle(davor, radien, radius))

    assert aufstellung.stelle(erstes) == verschobeneStelle(stelleErstes, radien, radius)
    assert aufstellung.stelle(zweites) == verschobeneStelle(stelleZweites, radien, radius)


@verschiebungenInRadien
@welchesGezogenWird
def testAuf24_2DerDienstAntwortetOhneSperreUndSetztBeideModelleAnDieNeueStelle(
    dienst, aufstellungNachDerZonenwahl, boyz, radien, zweitesGezogen
):
    erstes, *_ = boyz.modelle
    radius = radiusInZoll(erstes)
    stellen = stellenDerReihe(aufstellungNachDerZonenwahl, radius)
    gesetzte = modelleAnStellenSetzen(aufstellungNachDerZonenwahl, boyz, stellen)
    auswählen(dienst, "Boyz")
    (gezogenes, davor), _ = gezogenesUndRest(gesetzte, zweitesGezogen=zweitesGezogen)

    antwort = modellLoslassen(
        dienst,
        aufstellungNachDerZonenwahl,
        boyz,
        gezogenes,
        verschobeneStelle(davor, radien, radius),
    )

    erwartet = {
        nummer: stelleImSpielstand(verschobeneStelle(stelle, radien, radius))
        for nummer, stelle in enumerate(stellen, start=1)
    }
    assert antwort.status_code == HTTPStatus.OK
    # Warum: der Dienst liest den Weg des Gezogenen wie gesendet (S2), ein Float-Schritt Abweichung.
    gemeldet = stellenDerEinheitIm(antwort.get_json(), "Boyz")
    assert gemeldet.keys() == erwartet.keys()
    assert gemeldet == {
        nummer: pytest.approx(stelle, abs=1e-9) for nummer, stelle in erwartet.items()
    }


@mitMausUndFinger
@pytest.mark.parametrize(
    "zugAufDenNachbarn",
    [(False, 2), (True, -2)],
    ids=["ersteZurStelleDesZweiten", "zweiteZurStelleDesErsten"],
)
def testAuf24_2DieSeiteNenntKeinenGrundWennDerBlockAufSeineVorigenStellenRückt(
    bildschirm, aufstellungNachDerZonenwahl, boyz, zugAufDenNachbarn, eingabe
):
    zweitesGezogen, radien = zugAufDenNachbarn
    erstes, *_ = boyz.modelle
    radius = radiusInZoll(erstes)
    stellen = stellenDerReihe(aufstellungNachDerZonenwahl, radius)
    gesetzte = modelleAnStellenSetzen(aufstellungNachDerZonenwahl, boyz, stellen)
    aufstellungNachDerZonenwahl.auswählen(boyz)
    (gezogenes, davor), _ = gezogenesUndRest(gesetzte, zweitesGezogen=zweitesGezogen)
    ziel = verschobeneStelle(davor, radien, radius)
    seite = seiteMitEingabe(bildschirm, aufstellungNachDerZonenwahl, eingabe)

    modellZiehen(seite, davor, ziel, eingabe)

    assert aufstellungNachDerZonenwahl.gesetzt(gezogenes)
    assert liegtEinPixelGenauAn(seite, aufstellungNachDerZonenwahl.stelle(gezogenes), ziel)
    expect(seite.locator(".karte .modell")).to_have_count(2)
    assert sperrmeldungenDerSeite(seite) == []


@welchesGezogenWird
def testAuf24_2KeinModellIstGesperrtWennBeimHineinrückenEinesAufDieVorigeStelleDesAnderenRückt(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, zweitesGezogen
):
    einheit = ersteEinheitDesSpielersAnDerReihe
    erstes, zweites = einheit.modelle
    radius = radiusInZoll(erstes)
    # Warum: Quer zur Grenze; 21.2 rückt um 2 Radien zurück, das erste auf das zweite
    tiefeErstes = inZoll((tiefeDerZone, -5), radius)
    tiefeZweites = inZoll((tiefeDerZone, -3), radius)
    stellen = [
        stelleInDerZoneDesSpielersAnDerReihe(aufstellung, tiefe, längeDesErsten)
        for tiefe in (tiefeErstes, tiefeZweites)
    ]
    gesetzte = modelleAnStellenSetzen(aufstellung, einheit, stellen)
    aufstellung.auswählen(einheit)
    (gezogenes, _), _ = gezogenesUndRest(gesetzte, zweitesGezogen=zweitesGezogen)
    tiefeDesGezogenen = tiefeZweites if zweitesGezogen else tiefeErstes
    ziel = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, tiefeDesGezogenen + 4 * radius, längeDesErsten
    )
    _, stelleDavorZweites = stellen
    nachDemHineinrücken = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, inZoll((tiefeDerZone, -1), radius), längeDesErsten
    )

    aufstellung.modellLoslassen(gezogenes, ziel)

    assert aufstellung.stelle(erstes) == stelleDavorZweites
    assert aufstellung.stelle(zweites) == nachDemHineinrücken
