"""AUF-3 · Sperren beim Setzen."""

from fractions import Fraction

import pytest

from arbiter.domaene.sperre import Grund

# Regel: Breite des Spielfelds 44″, erste Reihe der Testeinheiten 3/2″ tief (conftest.py)
breiteDesSpielfelds = 44
tiefeDerErstenReihe = Fraction(3, 2)
# Regel: Richtung als Anteile von x und y; 3-4-5 hält die Entfernung exakt
gerade = (1, 0)
schräg = (Fraction(3, 5), Fraction(4, 5))


def stelleBeimGegner(platz, abstandDerMittelpunkte, richtung):
    """Eine Stelle, deren Mittelpunkt so weit von der ersten Stelle des Gegners liegt."""
    anteilX, anteilY = richtung
    tiefe = breiteDesSpielfelds - tiefeDerErstenReihe - abstandDerMittelpunkte * anteilX
    return platz.stelle(tiefe, platz.radius + abstandDerMittelpunkte * anteilY)


@pytest.mark.parametrize(
    ("tiefeInRadien", "längeInRadien"),
    [(0, 1), (30, 1), (11, 1), (1, 0)],
    ids=["überDieSpielfeldkante", "mitteDesSpielfelds", "zoneDesGegners", "überDieKurzeKante"],
)
def testAuf3_2LiegtDieBaseNichtGanzInDerZoneSeinesSpielersIstSieGesperrt(
    aufstellung, einheitInAufstellung, tiefeInRadien, längeInRadien, platz
):
    erstesModell, _ = einheitInAufstellung.modelle
    stelle = platz.stelle(
        tiefeInRadien * platz.radius - platz.millionstel, längeInRadien * platz.radius
    )

    gründe = platz.sperrgründe(aufstellung.modellSetzen, erstesModell, stelle)

    assert gründe == {Grund.nichtGanzInDerZone}
    assert not aufstellung.gesetzt(erstesModell)
    assert aufstellung.stelle(erstesModell) is None


@pytest.mark.parametrize(
    ("abstand", "richtung"),
    [(1, gerade), (1, schräg), (Fraction(1, 2), gerade), (0, gerade), (-Fraction(1, 2), gerade)],
    ids=["einZoll", "einZollSchräg", "halberZoll", "berührend", "überdeckend"],
)
def testAuf3_4InNahkampfreichweiteEinesGesetztenModellsDesGegnersIstGesperrt(
    aufstellung, einheitNachDemGegner, abstand, richtung, platz
):
    (modell,) = einheitNachDemGegner.modelle
    mittelpunkte = 2 * platz.radius + abstand
    stelle = stelleBeimGegner(platz, mittelpunkte, richtung)

    gründe = platz.sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert Grund.nahkampfreichweite in gründe
    assert not aufstellung.gesetzt(modell)


@pytest.mark.parametrize("richtung", [gerade, schräg], ids=["gerade", "schräg"])
def testAuf3_4JenseitsVonEinemZollIstNichtInNahkampfreichweite(
    aufstellung, einheitNachDemGegner, richtung, platz
):
    (modell,) = einheitNachDemGegner.modelle
    mittelpunkte = 2 * platz.radius + 1 + platz.millionstel
    stelle = stelleBeimGegner(platz, mittelpunkte, richtung)

    gründe = platz.sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert Grund.nahkampfreichweite not in gründe


def testAuf3_4EinModellDesEigenenSpielersSperrtNichtInNahkampfreichweite(
    aufstellung, einheitInAufstellung, platz
):
    erstesModell, zweitesModell = einheitInAufstellung.modelle
    aufstellung.modellSetzen(erstesModell, platz.stelle(2, platz.radius))
    stelle = platz.stelle(2, 3 * platz.radius + Fraction(1, 2))

    aufstellung.modellSetzen(zweitesModell, stelle)

    assert aufstellung.gesetzt(zweitesModell)


def testAuf3_5ZweiGründeAnEinerStelleNenntArbiterBeide(aufstellung, einheitInAufstellung, platz):
    erstesModell, zweitesModell = einheitInAufstellung.modelle
    aufstellung.modellSetzen(erstesModell, platz.stelle(9 - platz.radius, platz.radius))
    stelle = platz.stelle(9 - platz.radius + platz.millionstel, platz.radius)

    gründe = platz.sperrgründe(aufstellung.modellSetzen, zweitesModell, stelle)

    assert gründe == {Grund.nichtGanzInDerZone, Grund.baseÜberdeckt}
    assert not aufstellung.gesetzt(zweitesModell)


def testAuf3_5NichtGanzInDerZoneUndNahkampfreichweiteNenntArbiterBeide(
    aufstellung, einheitNachDemGegner, platz
):
    (modell,) = einheitNachDemGegner.modelle
    stelle = stelleBeimGegner(platz, 2 * platz.radius + Fraction(1, 2), gerade)

    gründe = platz.sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert gründe == {Grund.nichtGanzInDerZone, Grund.nahkampfreichweite}
    assert not aufstellung.gesetzt(modell)


def testAuf3_5AufDemModellDesGegnersNenntArbiterAlleDreiGründe(
    aufstellung, einheitNachDemGegner, platz
):
    (modell,) = einheitNachDemGegner.modelle
    stelle = stelleBeimGegner(platz, 0, gerade)

    gründe = platz.sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert gründe == {Grund.nichtGanzInDerZone, Grund.baseÜberdeckt, Grund.nahkampfreichweite}
    assert not aufstellung.gesetzt(modell)


@pytest.mark.usefixtures("einheitInAufstellung")
def testAuf3_6AußerhalbDerZoneNenntArbiterNurNichtInAufstellung(aufstellung, ersterSpieler, platz):
    _, andereEinheit = ersterSpieler.armee.einheiten
    (modellDerAnderenEinheit,) = andereEinheit.modelle
    stelle = platz.stelle(22, 30)

    gründe = platz.sperrgründe(aufstellung.modellSetzen, modellDerAnderenEinheit, stelle)

    assert gründe == {Grund.nichtInAufstellung}


@pytest.mark.usefixtures("einheitNachDemGegner")
def testAuf3_6AufDemModellDesGegnersNenntArbiterNurNichtInAufstellung(
    aufstellung, ersterSpieler, zweiterSpieler, platz
):
    aufgestellteEinheit, _ = ersterSpieler.armee.einheiten
    gegnerischeEinheit, _ = zweiterSpieler.armee.einheiten
    aufgestelltesModell, *_ = aufgestellteEinheit.modelle
    gegnerischesModell, *_ = gegnerischeEinheit.modelle
    stelle = aufstellung.stelle(gegnerischesModell)

    gründe = platz.sperrgründe(aufstellung.modellSetzen, aufgestelltesModell, stelle)

    assert gründe == {Grund.nichtInAufstellung}


def testAuf3_7EinGesetztesModellLässtSichAnEineAndereStelleSetzen(
    aufstellung, einheitInAufstellung, platz
):
    erstesModell, _ = einheitInAufstellung.modelle
    aufstellung.modellSetzen(erstesModell, platz.stelle(2, platz.radius))
    neueStelle = platz.stelle(5, 4 * platz.radius)

    aufstellung.modellSetzen(erstesModell, neueStelle)

    assert aufstellung.stelle(erstesModell) == neueStelle


def testAuf3_7DieVorigeStelleDesModellsZähltNichtAlsÜberdeckung(
    aufstellung, einheitInAufstellung, platz
):
    erstesModell, _ = einheitInAufstellung.modelle
    aufstellung.modellSetzen(erstesModell, platz.stelle(2, platz.radius))
    verschobeneStelle = platz.stelle(2, 2 * platz.radius)

    aufstellung.modellSetzen(erstesModell, verschobeneStelle)

    assert aufstellung.stelle(erstesModell) == verschobeneStelle


def testAuf3_7NachDemÜberdeckenBleibtDasModellAnSeinerVorigenStelle(
    aufstellung, einheitInAufstellung, platz
):
    erstesModell, zweitesModell = einheitInAufstellung.modelle
    vorigeStelle = platz.stelle(2, platz.radius)
    aufstellung.modellSetzen(erstesModell, vorigeStelle)
    aufstellung.modellSetzen(zweitesModell, platz.stelle(2, 3 * platz.radius))

    gründe = platz.sperrgründe(
        aufstellung.modellSetzen, erstesModell, platz.stelle(2, 2 * platz.radius)
    )

    assert gründe == {Grund.baseÜberdeckt}
    assert aufstellung.stelle(erstesModell) == vorigeStelle


def testAuf3_7NachDemVerlassenDerZoneBleibtDasModellAnSeinerVorigenStelle(
    aufstellung, einheitInAufstellung, platz
):
    erstesModell, _ = einheitInAufstellung.modelle
    vorigeStelle = platz.stelle(2, platz.radius)
    aufstellung.modellSetzen(erstesModell, vorigeStelle)

    gründe = platz.sperrgründe(aufstellung.modellSetzen, erstesModell, platz.stelle(22, 30))

    assert gründe == {Grund.nichtGanzInDerZone}
    assert aufstellung.stelle(erstesModell) == vorigeStelle


def testAuf3_7NachDerNahkampfreichweiteBleibtDasModellAnSeinerVorigenStelle(
    aufstellung, einheitNachDemGegner, platz
):
    (modell,) = einheitNachDemGegner.modelle
    vorigeStelle = platz.stelle(6, 20)
    aufstellung.modellSetzen(modell, vorigeStelle)
    stelle = stelleBeimGegner(platz, 2 * platz.radius + Fraction(1, 2), gerade)

    gründe = platz.sperrgründe(aufstellung.modellSetzen, modell, stelle)

    assert Grund.nahkampfreichweite in gründe
    assert aufstellung.stelle(modell) == vorigeStelle
