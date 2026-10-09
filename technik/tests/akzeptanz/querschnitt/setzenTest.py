"""QUE-1 · Setzen."""

from fractions import Fraction

import pytest

from arbiter.domaene.sperre import Grund
from tests.akzeptanz.handgriffe import gerade, schräg, sperrgründe


def testQue1_1VorDemSetzenIstDasModellNichtGesetzt(aufstellung, ersteEinheitDesSpielersAnDerReihe):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle

    assert not aufstellung.gesetzt(erstesModell)
    assert aufstellung.stelle(erstesModell) is None


def testQue1_1OhneSperreIstDasModellDanachAnDerStelleGesetzt(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    stelle = platz.stelle(3, platz.radius)

    aufstellung.modellSetzen(erstesModell, stelle)

    assert aufstellung.gesetzt(erstesModell)
    assert aufstellung.stelle(erstesModell) == stelle


@pytest.mark.parametrize(
    "anteile",
    [(0, 0), (Fraction(1, 2), 0), (0, Fraction(99, 100)), (Fraction(297, 500), Fraction(99, 125))],
    ids=["dieselbeStelle", "halbVersetzt", "knappInDerLänge", "knappSchräg"],
)
def testQue1_2ÜberdecktDieBaseDieEinesGesetztenModellsIstSieGesperrt(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, anteile, platz
):
    erstesModell, zweitesModell = ersteEinheitDesSpielersAnDerReihe.modelle
    anteilX, anteilY = anteile
    aufstellung.modellSetzen(erstesModell, platz.stelle(3, platz.radius))
    stelle = platz.stelle(3 + 2 * platz.radius * anteilX, platz.radius + 2 * platz.radius * anteilY)

    gründe = sperrgründe(aufstellung.modellSetzen, zweitesModell, stelle)

    assert gründe == {Grund.baseÜberdeckt}
    assert not aufstellung.gesetzt(zweitesModell)


@pytest.mark.parametrize(
    ("anteilX", "anteilY"),
    [(1, 0), (0, 1), (Fraction(3, 5), Fraction(4, 5))],
    ids=["berührendGerade", "berührendLängs", "berührendSchräg"],
)
def testQue1_2BerührenSichDieBasesIstDasSetzenNichtGesperrt(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, anteilX, anteilY, platz
):
    erstesModell, zweitesModell = ersteEinheitDesSpielersAnDerReihe.modelle
    aufstellung.modellSetzen(erstesModell, platz.stelle(3, platz.radius))
    stelle = platz.stelle(3 + 2 * platz.radius * anteilX, platz.radius + 2 * platz.radius * anteilY)

    aufstellung.modellSetzen(zweitesModell, stelle)

    assert aufstellung.gesetzt(zweitesModell)


def testQue1_2EinMillionstelZollZuNahIstGesperrt(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, zweitesModell = ersteEinheitDesSpielersAnDerReihe.modelle
    aufstellung.modellSetzen(erstesModell, platz.stelle(3, platz.radius))
    stelle = platz.stelle(3, 3 * platz.radius - platz.millionstel)

    gründe = sperrgründe(aufstellung.modellSetzen, zweitesModell, stelle)

    assert gründe == {Grund.baseÜberdeckt}


def testQue1_2AuchDasModellEinerAufgestelltenEinheitWirdÜberdeckt(
    aufstellung, einheitNachDemAnderenSpieler, ersterSpieler
):
    aufgestellteEinheit, _ = ersterSpieler.armee.einheiten
    aufgestelltesModell, *_ = aufgestellteEinheit.modelle
    (modell,) = einheitNachDemAnderenSpieler.modelle
    stelle = aufstellung.stelle(aufgestelltesModell)

    gründe = sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert gründe == {Grund.baseÜberdeckt}
    assert not aufstellung.gesetzt(modell)


@pytest.mark.parametrize(
    "lage",
    [(1, gerade), (1, schräg), (Fraction(1, 2), gerade), (0, gerade), (-Fraction(1, 2), gerade)],
    ids=["einZoll", "einZollSchräg", "halberZoll", "berührend", "überdeckend"],
)
def testQue1_3InNahkampfreichweiteEinesGesetztenModellsDesAnderenSpielersIstGesperrt(
    aufstellung, einheitNachDemAnderenSpieler, lage, platz
):
    (modell,) = einheitNachDemAnderenSpieler.modelle
    abstand, richtung = lage
    mittelpunkte = 2 * platz.radius + abstand
    stelle = platz.stelleBeimAnderenSpieler(mittelpunkte, richtung)

    gründe = sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert Grund.nahkampfreichweite in gründe
    assert not aufstellung.gesetzt(modell)


@pytest.mark.parametrize("richtung", [gerade, schräg], ids=["gerade", "schräg"])
def testQue1_3JenseitsVonEinemZollIstNichtInNahkampfreichweite(
    aufstellung, einheitNachDemAnderenSpieler, richtung, platz
):
    (modell,) = einheitNachDemAnderenSpieler.modelle
    mittelpunkte = 2 * platz.radius + 1 + platz.millionstel
    stelle = platz.stelleBeimAnderenSpieler(mittelpunkte, richtung)

    gründe = sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert Grund.nahkampfreichweite not in gründe


def testQue1_3EinModellDesEigenenSpielersSperrtNichtInNahkampfreichweite(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, zweitesModell = ersteEinheitDesSpielersAnDerReihe.modelle
    aufstellung.modellSetzen(erstesModell, platz.stelle(2, platz.radius))
    stelle = platz.stelle(2, 3 * platz.radius + Fraction(1, 2))

    aufstellung.modellSetzen(zweitesModell, stelle)

    assert aufstellung.gesetzt(zweitesModell)
