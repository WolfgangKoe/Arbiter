"""AUF-3 · Sperren beim Setzen."""

from fractions import Fraction

import pytest

from arbiter.domaene.sperre import Grund
from tests.akzeptanz.handgriffe import sperrgründe

# Regel: Richtung als Anteile von x und y; 3-4-5 hält die Entfernung exakt
gerade = (1, 0)
schräg = (Fraction(3, 5), Fraction(4, 5))


@pytest.mark.parametrize(
    "lageInRadien",
    [(0, 1), (30, 1), (57, 1)],
    ids=["überDieSpielfeldkante", "mitteDesSpielfelds", "zoneDesAnderenSpielers"],
)
def testAuf3_2LiegtDieBaseNichtGanzInDerZoneSeinesSpielersIstSieGesperrt(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, lageInRadien, platz
):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    tiefeInRadien, längeInRadien = lageInRadien
    stelle = platz.stelle(
        tiefeInRadien * platz.radius - platz.millionstel, längeInRadien * platz.radius
    )

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, stelle)

    assert gründe == {Grund.nichtGanzInDerZone}
    assert not aufstellung.gesetzt(erstesModell)
    assert aufstellung.stelle(erstesModell) is None


def testAuf3_2ÜberDieKurzeKanteAmAnfangIstGesperrt(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    stelle = platz.stelle(3, platz.radius - platz.millionstel)

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, stelle)

    assert gründe == {Grund.nichtGanzInDerZone}
    assert not aufstellung.gesetzt(erstesModell)


def testAuf3_2ÜberDieKurzeKanteAmEndeIstGesperrt(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    stelle = platz.stelle(3, platz.längeDerSpielfeldkante - platz.radius + platz.millionstel)

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, stelle)

    assert gründe == {Grund.nichtGanzInDerZone}
    assert not aufstellung.gesetzt(erstesModell)


@pytest.mark.parametrize(
    "lage",
    [(1, gerade), (1, schräg), (Fraction(1, 2), gerade), (0, gerade), (-Fraction(1, 2), gerade)],
    ids=["einZoll", "einZollSchräg", "halberZoll", "berührend", "überdeckend"],
)
def testAuf3_4InNahkampfreichweiteEinesGesetztenModellsDesAnderenSpielersIstGesperrt(
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
def testAuf3_4JenseitsVonEinemZollIstNichtInNahkampfreichweite(
    aufstellung, einheitNachDemAnderenSpieler, richtung, platz
):
    (modell,) = einheitNachDemAnderenSpieler.modelle
    mittelpunkte = 2 * platz.radius + 1 + platz.millionstel
    stelle = platz.stelleBeimAnderenSpieler(mittelpunkte, richtung)

    gründe = sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert Grund.nahkampfreichweite not in gründe


def testAuf3_4EinModellDesEigenenSpielersSperrtNichtInNahkampfreichweite(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, zweitesModell = ersteEinheitDesSpielersAnDerReihe.modelle
    aufstellung.modellSetzen(erstesModell, platz.stelle(2, platz.radius))
    stelle = platz.stelle(2, 3 * platz.radius + Fraction(1, 2))

    aufstellung.modellSetzen(zweitesModell, stelle)

    assert aufstellung.gesetzt(zweitesModell)


def testAuf3_5ZweiGründeAnEinerStelleNenntArbiterBeide(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, zweitesModell = ersteEinheitDesSpielersAnDerReihe.modelle
    aufstellung.modellSetzen(
        erstesModell, platz.stelle(platz.tiefeDerZone - platz.radius, platz.radius)
    )
    stelle = platz.stelle(platz.tiefeDerZone - platz.radius + platz.millionstel, platz.radius)

    gründe = sperrgründe(aufstellung.modellSetzen, zweitesModell, stelle)

    assert gründe == {Grund.nichtGanzInDerZone, Grund.baseÜberdeckt}
    assert not aufstellung.gesetzt(zweitesModell)


def testAuf3_5NichtGanzInDerZoneUndNahkampfreichweiteNenntArbiterBeide(
    aufstellung, einheitNachDemAnderenSpieler, platz
):
    (modell,) = einheitNachDemAnderenSpieler.modelle
    stelle = platz.stelleBeimAnderenSpieler(2 * platz.radius + Fraction(1, 2), gerade)

    gründe = sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert gründe == {Grund.nichtGanzInDerZone, Grund.nahkampfreichweite}
    assert not aufstellung.gesetzt(modell)


def testAuf3_5AufDemModellDesAnderenSpielersNenntArbiterBaseNahkampfreichweiteUndZone(
    aufstellung, einheitNachDemAnderenSpieler, platz
):
    (modell,) = einheitNachDemAnderenSpieler.modelle
    stelle = platz.stelleBeimAnderenSpieler(0, gerade)

    gründe = sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert gründe == {Grund.nichtGanzInDerZone, Grund.baseÜberdeckt, Grund.nahkampfreichweite}
    assert not aufstellung.gesetzt(modell)


@pytest.mark.usefixtures("ersteEinheitDesSpielersAnDerReihe")
def testAuf3_8BeiNichtWählbarPrüftArbiterDieStelleAußerhalbDerZoneNicht(
    aufstellung, zweiterSpieler, platz
):
    einheitDesSpielersNichtAnDerReihe, _ = zweiterSpieler.armee.einheiten
    modellDesSpielersNichtAnDerReihe, *_ = einheitDesSpielersNichtAnDerReihe.modelle
    stelle = platz.stelle(22, 30)

    gründe = sperrgründe(aufstellung.modellSetzen, modellDesSpielersNichtAnDerReihe, stelle)

    assert gründe == {Grund.nichtWählbar}


@pytest.mark.usefixtures("einheitNachDemAnderenSpieler")
def testAuf3_8BeiNichtWählbarPrüftArbiterDieStelleAufEinemModellNicht(
    aufstellung, ersterSpieler, zweiterSpieler
):
    aufgestellteEinheit, _ = ersterSpieler.armee.einheiten
    einheitDesAnderenSpielers, _ = zweiterSpieler.armee.einheiten
    aufgestelltesModell, *_ = aufgestellteEinheit.modelle
    modellDesAnderenSpielers, *_ = einheitDesAnderenSpielers.modelle
    stelle = aufstellung.stelle(modellDesAnderenSpielers)

    gründe = sperrgründe(aufstellung.modellSetzen, aufgestelltesModell, stelle)

    assert gründe == {Grund.nichtWählbar}


def testAuf3_8BeiEinheitBegonnenPrüftArbiterDieStelleAußerhalbDerZoneNicht(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, ersterSpieler, platz
):
    begonnenesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    _, andereEinheit = ersterSpieler.armee.einheiten
    (modellDerAnderenEinheit,) = andereEinheit.modelle
    aufstellung.modellSetzen(begonnenesModell, platz.stelle(2, platz.radius))
    stelle = platz.stelle(22, 30)

    gründe = sperrgründe(aufstellung.modellSetzen, modellDerAnderenEinheit, stelle)

    assert gründe == {Grund.einheitBegonnen}


def testAuf3_8BeiEinheitBegonnenPrüftArbiterDieStelleAufEinemModellNicht(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, ersterSpieler, platz
):
    begonnenesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    _, andereEinheit = ersterSpieler.armee.einheiten
    (modellDerAnderenEinheit,) = andereEinheit.modelle
    stelle = platz.stelle(2, platz.radius)
    aufstellung.modellSetzen(begonnenesModell, stelle)

    gründe = sperrgründe(aufstellung.modellSetzen, modellDerAnderenEinheit, stelle)

    assert gründe == {Grund.einheitBegonnen}


def testAuf3_7EinGesetztesModellLässtSichAnEineAndereStelleSetzen(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    aufstellung.modellSetzen(erstesModell, platz.stelle(2, platz.radius))
    neueStelle = platz.stelle(5, 4 * platz.radius)

    aufstellung.modellSetzen(erstesModell, neueStelle)

    assert aufstellung.stelle(erstesModell) == neueStelle


def testAuf3_7DieVorigeStelleDesModellsZähltNichtAlsÜberdeckung(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    aufstellung.modellSetzen(erstesModell, platz.stelle(2, platz.radius))
    verschobeneStelle = platz.stelle(2, 2 * platz.radius)

    aufstellung.modellSetzen(erstesModell, verschobeneStelle)

    assert aufstellung.stelle(erstesModell) == verschobeneStelle


def testAuf3_7NachDemÜberdeckenBleibtDasModellAnSeinerVorigenStelle(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, zweitesModell = ersteEinheitDesSpielersAnDerReihe.modelle
    vorigeStelle = platz.stelle(2, platz.radius)
    aufstellung.modellSetzen(erstesModell, vorigeStelle)
    aufstellung.modellSetzen(zweitesModell, platz.stelle(2, 3 * platz.radius))

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, platz.stelle(2, 2 * platz.radius))

    assert gründe == {Grund.baseÜberdeckt}
    assert aufstellung.stelle(erstesModell) == vorigeStelle


def testAuf3_7NachDemVerlassenDerZoneBleibtDasModellAnSeinerVorigenStelle(
    aufstellung, ersteEinheitDesSpielersAnDerReihe, platz
):
    erstesModell, _ = ersteEinheitDesSpielersAnDerReihe.modelle
    vorigeStelle = platz.stelle(2, platz.radius)
    aufstellung.modellSetzen(erstesModell, vorigeStelle)

    gründe = sperrgründe(aufstellung.modellSetzen, erstesModell, platz.stelle(22, 30))

    assert gründe == {Grund.nichtGanzInDerZone}
    assert aufstellung.stelle(erstesModell) == vorigeStelle


def testAuf3_7NachDerNahkampfreichweiteBleibtDasModellAnSeinerVorigenStelle(
    aufstellung, einheitNachDemAnderenSpieler, platz
):
    (modell,) = einheitNachDemAnderenSpieler.modelle
    vorigeStelle = platz.stelle(6, 20)
    aufstellung.modellSetzen(modell, vorigeStelle)
    stelle = platz.stelleBeimAnderenSpieler(2 * platz.radius + Fraction(1, 2), gerade)

    gründe = sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert Grund.nahkampfreichweite in gründe
    assert aufstellung.stelle(modell) == vorigeStelle
