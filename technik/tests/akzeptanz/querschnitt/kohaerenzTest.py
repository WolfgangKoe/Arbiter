"""QUE-4 · Kohärenz."""

from fractions import Fraction

import pytest

from tests.akzeptanz.handgriffe import (
    aufstellungVon,
    nachDerWahlDerAufstellungszone,
    radiusInZoll,
    spielerMit,
    stelleInDerZoneVon,
)

# Warum: Schon ein Millionstel Zoll entscheidet, damit Grenzfälle ohne Toleranz gelten.
millionstel = Fraction(1, 1_000_000)


def aufstellungMitEinheitVon(modellzahl: int):
    anderer, beginner = spielerMit(1), spielerMit(modellzahl)
    aufstellung = aufstellungVon(anderer, beginner)
    nachDerWahlDerAufstellungszone(aufstellung, gewinner=anderer)
    (einheit,) = beginner.armee.einheiten
    return aufstellung, beginner, einheit


def modelleMitAbständen(aufstellung, beginner, einheit, abstände: list[Fraction]) -> None:
    """Setzt die ersten Modelle in einer Reihe; der erste Abstand ist null, danach je Base."""
    erstesModell, *_ = einheit.modelle
    länge = radiusInZoll(erstesModell)
    for modell, abstand in zip(einheit.modelle, abstände, strict=False):
        länge += abstand
        aufstellung.modellSetzen(modell, stelleInDerZoneVon(aufstellung, beginner, 4, länge))
        länge += 2 * radiusInZoll(modell)


@pytest.mark.parametrize("gesetzte", [0, 1], ids=["keinsGesetzt", "einsGesetzt"])
def testQue4_1EineEinheitMitHöchstensEinemGesetztenModellIstInKohärenz(gesetzte):
    aufstellung, beginner, einheit = aufstellungMitEinheitVon(3)
    modelleMitAbständen(aufstellung, beginner, einheit, [Fraction(0)] * gesetzte)

    assert aufstellung.inKohärenz(einheit)


@pytest.mark.parametrize(
    ("modellzahl", "abstände"),
    [
        (2, [0, 3]),
        (3, [0, 0, 3]),
        (5, [0, 0, 0, 0, 5]),
        (2, [0, 2 + millionstel]),
    ],
    ids=["zweiModelle", "dreiModelle", "fünfModelle", "einMillionstelÜberZwei"],
)
def testQue4_2EinModellOhnePartnerImAbstandVonZweiZollMachtDieEinheitInkohärent(
    modellzahl, abstände
):
    aufstellung, beginner, einheit = aufstellungMitEinheitVon(modellzahl)
    modelleMitAbständen(aufstellung, beginner, einheit, [Fraction(wert) for wert in abstände])

    assert not aufstellung.inKohärenz(einheit)


def testQue4_3EinModellMitNurEinemPartnerBeiSechsModellenMachtDieEinheitInkohärent():
    aufstellung, beginner, einheit = aufstellungMitEinheitVon(6)
    modelleMitAbständen(
        aufstellung, beginner, einheit, [Fraction(wert) for wert in (0, 0, 0, 0, 0, 2)]
    )

    assert not aufstellung.inKohärenz(einheit)


@pytest.mark.parametrize(
    ("modellzahl", "abstände"),
    [
        (4, [0, 0, 2 + millionstel, 0]),
        (6, [0, 0, 0, 2 + millionstel, 0, 0]),
    ],
    ids=["zweiPaare", "zweiDreiergruppen"],
)
def testQue4_4ZweiGruppenOhneModellImAbstandVonZweiZollMachenDieEinheitInkohärent(
    modellzahl, abstände
):
    aufstellung, beginner, einheit = aufstellungMitEinheitVon(modellzahl)
    modelleMitAbständen(aufstellung, beginner, einheit, [Fraction(wert) for wert in abstände])

    assert not aufstellung.inKohärenz(einheit)


@pytest.mark.parametrize(
    ("modellzahl", "abstände"),
    [
        (2, [0, 2]),
        (3, [0, 0, 0]),
        (4, [0, 0, 2, 0]),
        (6, [0, 0, 0, 0, 0, 0]),
        (6, [0, 0, 0, 2, 0, 0]),
    ],
    ids=[
        "zweiModelleImAbstandVonGenauZweiZoll",
        "dreiModelleInEinerReihe",
        "zweiPaareImAbstandVonGenauZweiZoll",
        "sechsModelleInEinerReihe",
        "zweiDreiergruppenImAbstandVonGenauZweiZoll",
    ],
)
def testQue4_5EineEinheitOhneEinenDerFälleVierZweiBisVierVierIstInKohärenz(modellzahl, abstände):
    aufstellung, beginner, einheit = aufstellungMitEinheitVon(modellzahl)
    modelleMitAbständen(aufstellung, beginner, einheit, [Fraction(wert) for wert in abstände])

    assert aufstellung.inKohärenz(einheit)
