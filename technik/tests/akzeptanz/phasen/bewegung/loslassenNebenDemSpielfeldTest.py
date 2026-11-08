"""BEW-20 · Loslassen neben dem Spielfeld."""

from fractions import Fraction

import pytest

from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.bildschirm import seiteDerSchlachtMitEingabe, sperrmeldungenDerSeite
from tests.akzeptanz.handgriffe import breiteDesSpielfelds, radiusInZoll
from tests.akzeptanz.schlacht import hältAnDerSpielfeldkante, stellenAlsZahlen
from tests.akzeptanz.ziehen import (
    alleinUndMitEinheitenebene,
    mitMausUndFinger,
    nebenDemSpielfeldLoslassen,
    punktAufDemSpielfeld,
)

einZoll = Fraction(1)


def anDerWestkante(stelle: Stelle, radius: Fraction) -> tuple[Stelle, Stelle]:
    über = Stelle(x=radius / 2, y=stelle.y)
    jenseits = Stelle(x=-einZoll, y=stelle.y)
    return über, jenseits


def anDerOstkante(stelle: Stelle, radius: Fraction) -> tuple[Stelle, Stelle]:
    über = Stelle(x=breiteDesSpielfelds - radius / 2, y=stelle.y)
    jenseits = Stelle(x=breiteDesSpielfelds + einZoll, y=stelle.y)
    return über, jenseits


@pytest.fixture
def boyzInDerBewegungsphase(schlachtInDerBewegungsphase, boyz):
    return schlachtInDerBewegungsphase, boyz


@alleinUndMitEinheitenebene
@mitMausUndFinger
def testBew20_1NebenDemSpielfeldLosgelassenStehtJedesModellWoDasSpielfeldEsZuletztZeigte(
    bildschirm, beendeteAufstellung, boyzInDerBewegungsphase, ebeneLegen, eingabe
):
    schlacht, boyz = boyzInDerBewegungsphase
    ebeneLegen(schlacht, boyz)
    *_, modell = boyz.modelle
    davor = schlacht.stelle(modell)
    überDerKante, jenseits = anDerWestkante(davor, radiusInZoll(modell))
    stellenDavor = stellenAlsZahlen(schlacht)
    seite = seiteDerSchlachtMitEingabe(bildschirm, beendeteAufstellung, schlacht, eingabe)
    daneben = punktAufDemSpielfeld(seite, jenseits)

    gezeigt = nebenDemSpielfeldLoslassen(seite, davor, überDerKante, daneben, eingabe)

    assert gezeigt != stellenDavor
    assert stellenAlsZahlen(schlacht) == gezeigt
    assert hältAnDerSpielfeldkante(schlacht.stelle(modell), modell)


def außerhalbDerBewegungsphase(_schlacht, boyz, _necronWarriors):
    *_, modell = boyz.modelle
    return modell, anDerWestkante


def modellDesAnderenSpielers(schlacht, _boyz, necronWarriors):
    schlacht.phaseBeenden()
    *_, modell = necronWarriors.modelle
    return modell, anDerOstkante


@pytest.fixture(
    params=[außerhalbDerBewegungsphase, modellDesAnderenSpielers],
    ids=["außerhalbDerBewegungsphase", "modellDesAnderenSpielers"],
)
def zugOhneBewegung(request, schlachtNachDerWahlDesErstenZugs, boyz, necronWarriors):
    schlacht = schlachtNachDerWahlDesErstenZugs
    modell, kante = request.param(schlacht, boyz, necronWarriors)
    return schlacht, modell, kante


@mitMausUndFinger
def testBew20_1OhneBewegungStehtNebenDemSpielfeldLosgelassenJedesModellWieDavorOhneGrund(
    bildschirm, beendeteAufstellung, zugOhneBewegung, eingabe
):
    schlacht, modell, kante = zugOhneBewegung
    davor = schlacht.stelle(modell)
    überDerKante, jenseits = kante(davor, radiusInZoll(modell))
    stellenDavor = stellenAlsZahlen(schlacht)
    seite = seiteDerSchlachtMitEingabe(bildschirm, beendeteAufstellung, schlacht, eingabe)
    daneben = punktAufDemSpielfeld(seite, jenseits)

    nebenDemSpielfeldLoslassen(seite, davor, überDerKante, daneben, eingabe)

    assert stellenAlsZahlen(schlacht) == stellenDavor
    assert sperrmeldungenDerSeite(seite) == []
