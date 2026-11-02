"""AUF-28 · Loslassen, wo die Karte zeigt."""

from fractions import Fraction
from http import HTTPStatus
from urllib.parse import parse_qs, urlparse

import pytest
from playwright.sync_api import Route

from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.anhalten import stellenAlsZahlen
from tests.akzeptanz.bildschirm import (
    aufDieHandlungWarten,
    kreiseDerKarte,
    seiteMitEingabe,
)
from tests.akzeptanz.dienst import (
    auswählen,
    imUmfangDes,
    körperDerStelle,
    losgelassenDesVertrags,
    pfadDesGezogenenImBeispiel,
    sperreDesVertrags,
    spielstandDesVertrags,
    stelleBeimLoslassenDesVertrags,
    stelleDesLoslassensImBeispiel,
    stellenDesVertrags,
)
from tests.akzeptanz.handgriffe import (
    breiteDesSpielfelds,
    modelleSetzen,
    stelleInDerZoneDesSpielersAnDerReihe,
)
from tests.akzeptanz.ziehen import (
    Abfragen,
    alleinUndAlsEbene,
    aufDieAntwortenWarten,
    bildaufbauAbwarten,
    halten,
    längeDesHaltens,
    mitMausUndFinger,
    nebenDerKarteLoslassen,
    offeneAbfragenAbwarten,
    punktAufDerKarte,
    zieleNebenDerKarte,
)

gesperrteStelleImBeispiel = Stelle(x=Fraction(38), y=Fraction(28))
stelleNebenDerKarteImBeispiel = Stelle(x=Fraction(breiteDesSpielfelds + 2), y=Fraction(28))


@pytest.fixture
def dreiGesetzteBoyz(aufstellungNachDerZonenwahl, spielerEins, boyz):
    [(_, davor), *_] = modelleSetzen(aufstellungNachDerZonenwahl, boyz, 3)
    return aufstellungNachDerZonenwahl, spielerEins, boyz, davor


@zieleNebenDerKarte
@alleinUndAlsEbene
@mitMausUndFinger
def testAuf28_1NebenDerKarteLosgelassenStehtJedesModellWoDieKarteEsZuletztZeigte(
    bildschirm, dreiGesetzteBoyz, ziel, ebeneLegen, eingabe
):
    aufstellung, spielerEins, boyz, davor = dreiGesetzteBoyz
    ebeneLegen(aufstellung, boyz)
    stellenDavor = stellenAlsZahlen(aufstellung)
    seite = seiteMitEingabe(bildschirm, aufstellung, eingabe)
    aufDerKarte = stelleInDerZoneDesSpielersAnDerReihe(aufstellung, 4, längeDesHaltens)
    daneben = ziel(seite, aufstellung, spielerEins)

    gezeigt = nebenDerKarteLoslassen(seite, davor, aufDerKarte, daneben, eingabe)

    assert gezeigt != stellenDavor
    assert stellenAlsZahlen(aufstellung) == gezeigt


def testAuf28_1DerDienstSetztAmPunktDerLetztenStelleWieDasBeispielImVertrag(dienstDesBeispiels):
    punkt = körperDerStelle(stelleDesLoslassensImBeispiel)
    auswählen(dienstDesBeispiels, "Necron Warriors")
    dienstDesBeispiels.get(f"{pfadDesGezogenenImBeispiel}/stelleBeimLoslassen", query_string=punkt)

    antwort = dienstDesBeispiels.put(f"{pfadDesGezogenenImBeispiel}/stelle", json=punkt)

    assert antwort.status_code == HTTPStatus.OK
    beispiel = losgelassenDesVertrags()
    assert imUmfangDes(beispiel, antwort.get_json()) == beispiel


class AbfrageMitSperre:
    def __init__(self) -> None:
        self.gesperrt = False
        self.punkteMitStelle: list[dict[str, float]] = []

    def beantworten(self, anfrage: Route) -> None:
        if self.gesperrt:
            anfrage.fulfill(status=HTTPStatus.CONFLICT, json=sperreDesVertrags())
            return
        abfrage = parse_qs(urlparse(anfrage.request.url).query)
        self.punkteMitStelle.append({name: float(wert) for name, (wert,) in abfrage.items()})
        anfrage.fulfill(json=stelleBeimLoslassenDesVertrags())


def testAuf28_1DieSeiteSendetNebenDerKarteDenPunktDerLetztenStelleAuchNachEinerSperre(
    bildschirm, ausgangsaufstellung
):
    abfrage = AbfrageMitSperre()
    seite = bildschirm.seiteMitSpielstand(
        ausgangsaufstellung,
        spielstandDesVertrags(),
        {f"**{pfadDesGezogenenImBeispiel}/stelle": losgelassenDesVertrags()},
    )
    seite.route("**/stelleBeimLoslassen*", abfrage.beantworten)
    gehaltenes, _, _ = stellenDesVertrags(2)
    zeiger = halten(seite, gehaltenes, stelleDesLoslassensImBeispiel, "maus")
    abfrage.gesperrt = True
    gesperrte = Abfragen(seite)
    zeiger.bewegen(punktAufDerKarte(seite, gesperrteStelleImBeispiel))
    aufDieAntwortenWarten(seite, gesperrte)
    daneben = punktAufDerKarte(seite, stelleNebenDerKarteImBeispiel)
    zeiger.bewegen(daneben)
    offeneAbfragenAbwarten(seite, gesperrte)

    with aufDieHandlungWarten(seite) as antwort:
        zeiger.loslassen(daneben)

    anfrage = antwort.value.request
    *_, punktDerLetztenStelle = abfrage.punkteMitStelle
    bildaufbauAbwarten(seite)
    modelle = losgelassenDesVertrags()["modelle"]
    assert (anfrage.method, urlparse(anfrage.url).path) == (
        "PUT",
        f"{pfadDesGezogenenImBeispiel}/stelle",
    )
    assert anfrage.post_data_json == punktDerLetztenStelle
    assert kreiseDerKarte(seite) == {(modell["x"], modell["y"]) for modell in modelle}
