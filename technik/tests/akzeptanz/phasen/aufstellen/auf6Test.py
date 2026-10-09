"""AUF-6 · Vorläufig: Start mit gewähltem Gewinner und gewählter Zone."""

from tests.akzeptanz.bildschirm import Element, elementeDerSeite, spielerAnDerReihe


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

    markierte = spielerAnDerReihe(seite)
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
