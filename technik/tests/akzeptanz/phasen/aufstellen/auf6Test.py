"""AUF-6 · Vorläufig: Start mit gewähltem Gewinner und gewählter Zone."""

from arbiter.domaene.phasen.aufstellen import Aufstellungszone
from tests.akzeptanz.bildschirm import Element, elementeDerSeite
from tests.akzeptanz.handgriffe import dienstFür, spielstandVon


def farbeJeSpielername(seite) -> dict[str, str]:
    return {name.text: name.farbe for name in elementeDerSeite(seite, ".armeeKartenName")}


def mitteDerAblage(seite, spielername: str) -> float:
    namen = elementeDerSeite(seite, ".armeeKartenName")
    return next(name.mitteInPixeln for name in namen if name.text == spielername)


def zoneNebenDerAblage(seite, spielername: str) -> Element:
    """Die Zone der Karte, deren Mitte der Ablage des Spielers am nächsten liegt."""
    mitteDerAblageDesSpielers = mitteDerAblage(seite, spielername)
    abstandUndZone = [
        (abs(zone.mitteInPixeln - mitteDerAblageDesSpielers), index, zone)
        for index, zone in enumerate(elementeDerSeite(seite, ".karte .aufstellungszone"))
    ]
    _, _, nächste = min(abstandUndZone)
    return nächste


def testAuf6_1NachDemStartIstSpielerZweiAnDerReihe(adresseDesBefehls, bildschirm):
    seite = bildschirm.seiteBei(adresseDesBefehls)

    markierte = seite.locator(".kopfzeileSpieler").filter(has=seite.locator(".kopfzeileAnDerReihe"))
    assert markierte.count() == 1
    assert "Spieler 2" in markierte.text_content()
    assert seite.locator(".kopfzeileAnDerReihe").text_content() == "an der Reihe"


def testAuf6_1NachDemStartHatSpielerEinsDieZoneGewähltDieSeinerAblageAmNächstenLiegt(
    adresseDesBefehls, bildschirm
):
    seite = bildschirm.seiteBei(adresseDesBefehls)

    zone = zoneNebenDerAblage(seite, "Spieler 1")

    assert zone.fill == farbeJeSpielername(seite)["Spieler 1"]


def testAuf6_1NachDemStartGehörtSpielerZweiDieAndereZone(adresseDesBefehls, bildschirm):
    seite = bildschirm.seiteBei(adresseDesBefehls)

    zone = zoneNebenDerAblage(seite, "Spieler 2")

    assert zone.fill == farbeJeSpielername(seite)["Spieler 2"]


def testAuf6_1DerSpielstandNenntSpielerZweiAnDerReiheUndSpielerEinsDieErsteZone(
    ausgangsaufstellung, spielerEins
):
    ausgangsaufstellung.gewinnerWählen(spielerEins)
    ausgangsaufstellung.aufstellungszoneWählen(Aufstellungszone.erste)

    spielstand = spielstandVon(dienstFür(ausgangsaufstellung))

    anDerReihe = {einer["nummer"] for einer in spielstand["spieler"] if einer["anDerReihe"]}
    besitzerJeZone = {zone["x"]: zone["spieler"] for zone in spielstand["zonen"]}
    assert anDerReihe == {2}
    assert besitzerJeZone == {0.0: 1, 35.0: 2}
