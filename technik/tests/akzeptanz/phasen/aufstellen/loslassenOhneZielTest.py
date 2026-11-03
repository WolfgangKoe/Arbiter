"""AUF-16 · Loslassen ohne Ziel."""

from fractions import Fraction
from http import HTTPStatus

import pytest

from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.bildschirm import (
    kreiseDerKarte,
    seiteMitEingabe,
    sperrmeldungenDerSeite,
)
from tests.akzeptanz.dienst import (
    auswählen,
    imUmfangDes,
    keineStelleBeimLoslassenDesVertrags,
    körperDerStelle,
    pfadDesGezogenenImBeispiel,
    spielstandVon,
    stelleDesLoslassensImBeispiel,
    zurückgelegtDesVertrags,
    zurücklegen,
)
from tests.akzeptanz.handgriffe import (
    einheitAufstellen,
    modelleSetzen,
    stelleInDerZoneDesSpielersAnDerReihe,
    stellenAllerModelle,
)
from tests.akzeptanz.ziehen import (
    bildaufbauAbwarten,
    einenZollJenseitsDerKante,
    haltenUndLosslassen,
    längeDesHaltens,
    mitMausUndFinger,
    nebenDerKarteLoslassen,
    punktAufDerKarte,
    ziehenOhneAnfrage,
    zieleNebenDerKarte,
)


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

    abfrage = aufstellung.stellenBeimLoslassen(modell, ziel).stellen

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
        query_string=körperDerStelle(stelleDesLoslassensImBeispiel),
    )

    assert antwort.status_code == HTTPStatus.OK
    assert antwort.get_json() == keineStelleBeimLoslassenDesVertrags()
    beispiel = zurückgelegtDesVertrags()
    assert imUmfangDes(beispiel, spielstandVon(dienstDesBeispiels)) == beispiel


@pytest.mark.parametrize(
    "stelle",
    [stelleDesLoslassensImBeispiel, Stelle(x=Fraction(5), y=Fraction(28))],
    ids=["amPunktDesBeispiels", "inDerZoneDesAnderenSpielers"],
)
def testAuf16_7DerDienstSetztNachDemZurücklegenNichtsWieDasBeispielImVertrag(
    dienstDesBeispiels, stelle
):
    auswählen(dienstDesBeispiels, "Necron Warriors")
    zurücklegen(dienstDesBeispiels)

    antwort = dienstDesBeispiels.put(
        f"{pfadDesGezogenenImBeispiel}/stelle", json=körperDerStelle(stelle)
    )

    assert antwort.status_code == HTTPStatus.OK
    beispiel = zurückgelegtDesVertrags()
    assert imUmfangDes(beispiel, antwort.get_json()) == beispiel


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
    daneben = ziel(seite, aufstellung, spielerEins)

    anfragen = ziehenOhneAnfrage(seite, von, daneben, eingabe)

    assert anfragen == []
    assert kreiseDerKarte(seite) == kreiseDavor
    assert stellenAllerModelle(aufstellung) == stellenDavor
    assert sperrmeldungenDerSeite(seite) == []
