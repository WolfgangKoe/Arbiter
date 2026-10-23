"""QUE-8 · Feste Adresse."""

from urllib.parse import urlparse

from arbiter.__main__ import portDesBefehls
from arbiter.web.server import adresseMitPort


def testQue8_1OhneAngabeStartetArbiterUnterDerFestenAdresse():
    adresse = adresseMitPort(portDesBefehls([]))

    assert adresse == "http://127.0.0.1:8040/"


def testQue8_2IstDieAdresseBelegtStartetArbiterNichtUndNenntKeineAndere(adresseDesBefehls, befehl):
    belegterPort = urlparse(adresseDesBefehls).port

    ende = befehl.startenBisZumEnde(belegterPort)

    assert ende.exitCode == 1
    assert ende.ausgabe == ""


def testQue8_2IstDieAdresseBelegtMeldetArbiterDieseAdresseAlsBelegt(adresseDesBefehls, befehl):
    belegterPort = urlparse(adresseDesBefehls).port

    ende = befehl.startenBisZumEnde(belegterPort)

    meldung = ende.fehlerausgabe.rstrip("\n")
    assert "\n" not in meldung
    assert adresseMitPort(belegterPort) in meldung
    assert "belegt" in meldung
