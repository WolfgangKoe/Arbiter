"""AUF-16 · Loslassen ohne Ziel."""

from http import HTTPStatus

import pytest

from tests.akzeptanz.bildschirm import (
    armeelisteVon,
    kreiseDerKarte,
    seiteMitEingabe,
    sperrmeldungenDerSeite,
)
from tests.akzeptanz.dienst import (
    auswählen,
    keineStelleBeimLoslassenDesVertrags,
    spielstandVon,
    zurückgelegtDesVertrags,
    zurücklegen,
)
from tests.akzeptanz.handgriffe import (
    einheitAufstellen,
    modelleSetzen,
    stelleInDerZoneDesSpielersAnDerReihe,
    stelleInDerZoneVon,
    stellenAllerModelle,
)
from tests.akzeptanz.ziehen import (
    bildaufbauAbwarten,
    haltenUndLosslassen,
    mitMausUndFinger,
    mitteVon,
    nebenDerKarteLoslassen,
    punktAufDerKarte,
    ziehenOhneAnfrage,
)

pfadDesGezogenenImBeispiel = "/api/spieler/2/einheiten/1/modelle/1"
punktDesLoslassensImBeispiel = {"x": 35, "y": 28}
einenZollJenseitsDerKante = -1
längeDesHaltens = 20


def nurZurücklegen(aufstellung, warboss): ...


def danachDenWarbossBeginnen(aufstellung, warboss):
    modelleSetzen(aufstellung, warboss, 1)


einheitInAufstellungNachDemZurücklegen = pytest.mark.parametrize(
    "danach",
    [nurZurücklegen, danachDenWarbossBeginnen],
    ids=["keineEinheitInAufstellung", "andereEinheitInAufstellung"],
)


def zurückgelegterBoy(aufstellung, boyz, warboss, danach):
    [(modell, _), *_] = modelleSetzen(aufstellung, boyz, 3)
    aufstellung.zurücklegen()
    danach(aufstellung, warboss)
    return modell


@einheitInAufstellungNachDemZurücklegen
def testAuf16_7DieStellenBeimLoslassenEinesNichtGesetztenModellsSindLeer(
    aufstellungNachDerZonenwahl, boyz, warboss, danach
):
    aufstellung = aufstellungNachDerZonenwahl
    modell = zurückgelegterBoy(aufstellung, boyz, warboss, danach)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 4, längeDesHaltens)

    abfrage = aufstellung.stellenBeimLoslassen(modell, ziel)

    assert abfrage == {}


@einheitInAufstellungNachDemZurücklegen
def testAuf16_7EinNichtGesetztesModellLoslassenÄndertNichtsOhneGrund(
    aufstellungNachDerZonenwahl, boyz, warboss, danach
):
    aufstellung = aufstellungNachDerZonenwahl
    modell = zurückgelegterBoy(aufstellung, boyz, warboss, danach)
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 4, längeDesHaltens)
    davor = stellenAllerModelle(aufstellung)
    einheitInAufstellungDavor = aufstellung.einheitInAufstellung

    aufstellung.modellLoslassen(modell, ziel)

    assert stellenAllerModelle(aufstellung) == davor
    assert aufstellung.einheitInAufstellung is einheitInAufstellungDavor


def testAuf16_7DerDienstNenntNachDemZurücklegenKeineStelleWieDasBeispielImVertrag(
    dienstDesBeispiels,
):
    auswählen(dienstDesBeispiels, "Necron Warriors")
    zurücklegen(dienstDesBeispiels)

    antwort = dienstDesBeispiels.get(
        f"{pfadDesGezogenenImBeispiel}/stelleBeimLoslassen",
        query_string=punktDesLoslassensImBeispiel,
    )

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == keineStelleBeimLoslassenDesVertrags()
    assert spielstandVon(dienstDesBeispiels) == zurückgelegtDesVertrags()


@pytest.mark.parametrize(
    "punkt",
    [punktDesLoslassensImBeispiel, {"x": 5, "y": 28}],
    ids=["amPunktDesBeispiels", "inDerZoneDesAnderenSpielers"],
)
def testAuf16_7DerDienstSetztNachDemZurücklegenNichtsWieDasBeispielImVertrag(
    dienstDesBeispiels, punkt
):
    auswählen(dienstDesBeispiels, "Necron Warriors")
    zurücklegen(dienstDesBeispiels)

    antwort = dienstDesBeispiels.put(f"{pfadDesGezogenenImBeispiel}/stelle", json=punkt)

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == zurückgelegtDesVertrags()


def aufDerKarteLoslassen(seite, aufstellung, davor, eingabe):
    ziel = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 4, längeDesHaltens)
    return haltenUndLosslassen(seite, davor, ziel, eingabe)


def überDieKanteLoslassen(seite, aufstellung, davor, eingabe):
    aufDerKarte = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 4, längeDesHaltens)
    jenseits = stelleInDerZoneDesSpielersAnDerReihe(
        aufstellung, einenZollJenseitsDerKante, längeDesHaltens
    )
    daneben = punktAufDerKarte(seite, jenseits)
    return nebenDerKarteLoslassen(seite, davor, aufDerKarte, daneben, eingabe)


@pytest.mark.parametrize(
    "loslassen",
    [aufDerKarteLoslassen, überDieKanteLoslassen],
    ids=["aufDerKarte", "nebenDerKarte"],
)
@mitMausUndFinger
def testAuf16_7EineSeiteVonVorDemZurücklegenZeigtNachDemLoslassenKeinModellUndKeinenGrund(
    bildschirm, aufstellungNachDerZonenwahl, boyz, loslassen, eingabe
):
    aufstellung = aufstellungNachDerZonenwahl
    [(_, davor), *_] = modelleSetzen(aufstellung, boyz, 3)
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)
    aufstellung.zurücklegen()

    loslassen(seite, aufstellung, davor, eingabe)

    bildaufbauAbwarten(seite)
    assert kreiseDerKarte(seite) == frozenset()
    assert set(stellenAllerModelle(aufstellung).values()) == {None}
    assert sperrmeldungenDerSeite(seite) == []


zieleNebenDerKarte = pytest.mark.parametrize(
    "ziel",
    ["Spieler 1", "Spieler 2", "nebenDerKarte"],
    ids=["aufDerArmeelisteVonSpielerEins", "aufDerArmeelisteVonSpielerZwei", "nebenDerKarte"],
)


def punktNebenDerKarte(seite, aufstellung, spieler, ziel: str):
    if ziel == "nebenDerKarte":
        jenseits = stelleInDerZoneVon(
            aufstellung, spieler, einenZollJenseitsDerKante, längeDesHaltens
        )
        return punktAufDerKarte(seite, jenseits)
    return mitteVon(armeelisteVon(seite, ziel))


@pytest.fixture
def aufgestellteBoyz(aufstellungNachDerZonenwahl, spielerEins, boyz):
    einheitAufstellen(aufstellungNachDerZonenwahl, boyz)
    return aufstellungNachDerZonenwahl, spielerEins, boyz


@zieleNebenDerKarte
@mitMausUndFinger
def testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor(
    bildschirm, aufgestellteBoyz, ziel, eingabe
):
    aufstellung, spielerEins, boyz = aufgestellteBoyz
    erstesModell, *_ = boyz.modelle
    stellenDavor = stellenAllerModelle(aufstellung)
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)
    kreiseDavor = kreiseDerKarte(seite)
    von = punktAufDerKarte(seite, aufstellung.stelle(erstesModell))
    daneben = punktNebenDerKarte(seite, aufstellung, spielerEins, ziel)

    anfragen = ziehenOhneAnfrage(seite, von, daneben, eingabe)

    assert anfragen == []
    assert kreiseDerKarte(seite) == kreiseDavor
    assert stellenAllerModelle(aufstellung) == stellenDavor
    assert sperrmeldungenDerSeite(seite) == []
