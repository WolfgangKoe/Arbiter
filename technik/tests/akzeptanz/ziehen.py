import json
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction
from math import hypot
from urllib.parse import parse_qs, urlparse

import pytest
from playwright.sync_api import Locator, Page, Request, Response, Route

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from tests.akzeptanz.bildschirm import armeelisteVon, aufDieHandlungWarten, kreiseDesSpielfelds
from tests.akzeptanz.handgriffe import radiusInZoll, stelleInDerZoneVon
from tests.akzeptanz.schlacht import hundertstelZoll


@dataclass(frozen=True)
class Bildpunkt:
    links: float
    oben: float


def mitteVon(element: Locator) -> Bildpunkt:
    element.scroll_into_view_if_needed()
    rahmen = element.bounding_box()
    return Bildpunkt(rahmen["x"] + rahmen["width"] / 2, rahmen["y"] + rahmen["height"] / 2)


_punktAufDemSpielfeldLesen = """(spielfeld, ort) => {
    const punkt = spielfeld.createSVGPoint()
    punkt.x = ort[0]
    punkt.y = ort[1]
    const bild = punkt.matrixTransform(spielfeld.getScreenCTM())
    return [bild.x, bild.y]
}"""


def punktAufDemSpielfeld(seite: Page, stelle: Stelle) -> Bildpunkt:
    links, oben = seite.locator("svg.spielfeld").evaluate(
        _punktAufDemSpielfeldLesen, [float(stelle.x), float(stelle.y)]
    )
    return Bildpunkt(links, oben)


def zollJePixel(seite: Page) -> float:
    return seite.locator("svg.spielfeld").evaluate("spielfeld => 1 / spielfeld.getScreenCTM().a")


def liegtEinPixelGenauAn(seite: Page, ist: Stelle, soll: Stelle) -> bool:
    toleranz = zollJePixel(seite)
    abweichungInX = abs(float(ist.x) - float(soll.x))
    abweichungInY = abs(float(ist.y) - float(soll.y))
    return abweichungInX <= toleranz and abweichungInY <= toleranz


zugschwelleInPixeln = 4
anteilDesRadius = 0.8


def griffAbseitsDerMitte(seite: Page, modell: Modell, mitte: Bildpunkt) -> Bildpunkt:
    versatzInPixeln = float(radiusInZoll(modell)) / zollJePixel(seite) * anteilDesRadius
    assert versatzInPixeln > zugschwelleInPixeln
    return Bildpunkt(mitte.links + versatzInPixeln, mitte.oben)


def hältAnDerBewegungsweiteAufEinenPixelGenau(
    seite: Page, davor: Stelle, gezeigt: tuple[float, float], bewegungsweite: Fraction
) -> bool:
    gezeigtInX, gezeigtInY = gezeigt
    abstand = hypot(gezeigtInX - float(davor.x), gezeigtInY - float(davor.y))
    toleranz = zollJePixel(seite)
    weite = float(bewegungsweite)
    return weite - float(hundertstelZoll) - toleranz <= abstand <= weite + toleranz


class Maus:
    def __init__(self, seite: Page) -> None:
        self._seite = seite

    def drücken(self, ort: Bildpunkt) -> None:
        self._seite.mouse.move(ort.links, ort.oben)
        self._seite.mouse.down()

    def bewegen(self, ort: Bildpunkt) -> None:
        self._seite.mouse.move(ort.links, ort.oben, steps=10)

    def loslassen(self, _ort: Bildpunkt) -> None:
        self._seite.mouse.up()


class Finger:
    def __init__(self, seite: Page) -> None:
        self._sitzung = seite.context.new_cdp_session(seite)
        self._ort: Bildpunkt | None = None

    def _senden(self, art: str, ort: Bildpunkt | None) -> None:
        punkte = [] if ort is None else [{"x": ort.links, "y": ort.oben}]
        self._sitzung.send("Input.dispatchTouchEvent", {"type": art, "touchPoints": punkte})

    def drücken(self, ort: Bildpunkt) -> None:
        self._ort = ort
        self._senden("touchStart", ort)

    def bewegen(self, ort: Bildpunkt) -> None:
        start = self._ort
        for schritt in range(1, 11):
            anteil = schritt / 10
            unterwegs = Bildpunkt(
                start.links + (ort.links - start.links) * anteil,
                start.oben + (ort.oben - start.oben) * anteil,
            )
            self._senden("touchMove", unterwegs)
        self._ort = ort

    def loslassen(self, _ort: Bildpunkt) -> None:
        self._senden("touchEnd", None)


zeigerArten = {"maus": Maus, "finger": Finger}


def _ziehenMit(zeiger: Maus | Finger, von: Bildpunkt, nach: Bildpunkt) -> None:
    zeiger.drücken(von)
    zeiger.bewegen(nach)
    zeiger.loslassen(nach)


def mitDerMausZiehen(seite: Page, von: Bildpunkt, nach: Bildpunkt) -> None:
    _ziehenMit(Maus(seite), von, nach)


def mitDemFingerZiehen(seite: Page, von: Bildpunkt, nach: Bildpunkt) -> None:
    _ziehenMit(Finger(seite), von, nach)


eingaben = {"maus": mitDerMausZiehen, "finger": mitDemFingerZiehen}


def modellZiehen(seite: Page, von: Stelle, nach: Stelle, eingabe: str = "maus") -> Response:
    return modellAmPunktZiehen(
        seite, punktAufDemSpielfeld(seite, von), punktAufDemSpielfeld(seite, nach), eingabe
    )


def modellAmPunktZiehen(seite: Page, von: Bildpunkt, nach: Bildpunkt, eingabe: str) -> Response:
    with aufDieHandlungWarten(seite) as antwort:
        eingaben[eingabe](seite, von, nach)
    return antwort.value


_bildaufbauAbwarten = "() => new Promise(fertig => requestAnimationFrame(() => fertig()))"


def ziehenOhneAnfrage(
    seite: Page, von: Bildpunkt, nach: Bildpunkt, eingabe: str = "maus"
) -> list[Request]:
    anfragen: list[Request] = []

    def merken(anfrage: Request) -> None:
        if anfrage.method != "GET":
            anfragen.append(anfrage)

    seite.on("request", merken)
    eingaben[eingabe](seite, von, nach)
    bildaufbauAbwarten(seite)
    seite.remove_listener("request", merken)
    return anfragen


def bildaufbauAbwarten(seite: Page) -> None:
    seite.evaluate(_bildaufbauAbwarten)
    seite.evaluate(_bildaufbauAbwarten)


def mitDerMausKlicken(seite: Page, punkt: Bildpunkt) -> None:
    seite.mouse.click(punkt.links, punkt.oben)


def mitDemFingerTippen(seite: Page, punkt: Bildpunkt) -> None:
    seite.touchscreen.tap(punkt.links, punkt.oben)


klickenMit = {"maus": mitDerMausKlicken, "finger": mitDemFingerTippen}
mitMausUndFinger = pytest.mark.parametrize("eingabe", list(klickenMit), ids=list(klickenMit))


class Abfragen:
    def __init__(self, seite: Page) -> None:
        self.gestellt = 0
        self.erledigt = 0
        self._gezählte: set[Request] = set()
        seite.on("request", self._gestellt)
        seite.on("requestfinished", self._erledigt)
        seite.on("requestfailed", self._erledigt)

    @staticmethod
    def _istAbfrage(anfrage: Request) -> bool:
        return "/stelleBeimLoslassen" in anfrage.url

    def _gestellt(self, anfrage: Request) -> None:
        if self._istAbfrage(anfrage):
            self._gezählte.add(anfrage)
            self.gestellt += 1

    def _erledigt(self, anfrage: Request) -> None:
        if anfrage in self._gezählte:
            self.erledigt += 1

    def beantwortet(self) -> bool:
        return self.gestellt == self.erledigt

    def ruhig(self) -> bool:
        return self.gestellt > 0 and self.beantwortet()


_pausenInMillisekunden = 50
_ruhigeProben = 4
_höchstensProben = 200


def _wartenBis(seite: Page, bedingung: Callable[[], bool]) -> bool:
    ruhige = 0
    for _ in range(_höchstensProben):
        seite.wait_for_timeout(_pausenInMillisekunden)
        ruhige = ruhige + 1 if bedingung() else 0
        if ruhige == _ruhigeProben:
            return True
    return False


def aufDieAntwortenWarten(seite: Page, abfragen: Abfragen) -> None:
    if not _wartenBis(seite, abfragen.ruhig):
        raise TimeoutError(
            "Die Seite fragt nicht nach der Stelle beim Loslassen oder antwortet nicht"
        )


def offeneAbfragenAbwarten(seite: Page, abfragen: Abfragen) -> None:
    if not _wartenBis(seite, abfragen.beantwortet):
        raise TimeoutError("Die Seite bekommt keine Antwort auf die Stelle beim Loslassen")


def halten(seite: Page, von: Stelle, nach: Stelle, eingabe: str) -> Maus | Finger:
    zeiger = zeigerArten[eingabe](seite)
    abfragen = Abfragen(seite)
    zeiger.drücken(punktAufDemSpielfeld(seite, von))
    zeiger.bewegen(punktAufDemSpielfeld(seite, nach))
    aufDieAntwortenWarten(seite, abfragen)
    return zeiger


def haltenUndLosslassen(
    seite: Page, von: Stelle, nach: Stelle, eingabe: str
) -> frozenset[tuple[float, float]]:
    zeiger = halten(seite, von, nach, eingabe)
    gezeigt = kreiseDesSpielfelds(seite)
    with aufDieHandlungWarten(seite):
        zeiger.loslassen(punktAufDemSpielfeld(seite, nach))
    return gezeigt


def alleinZiehen(spiel, einheit: Einheit) -> None: ...


def mitEinheitenebeneZiehen(spiel, einheit: Einheit) -> None:
    spiel.auswählen(einheit)


alleinUndMitEinheitenebene = pytest.mark.parametrize(
    "ebeneLegen", [alleinZiehen, mitEinheitenebeneZiehen], ids=["einModell", "einheitenebene"]
)


def nebenDemSpielfeldLoslassen(
    seite: Page, von: Stelle, aufDemSpielfeld: Stelle, daneben: Bildpunkt, eingabe: str
) -> frozenset[tuple[float, float]]:
    zeiger = halten(seite, von, aufDemSpielfeld, eingabe)
    abfragen = Abfragen(seite)
    zeiger.bewegen(daneben)
    offeneAbfragenAbwarten(seite, abfragen)
    gezeigt = kreiseDesSpielfelds(seite)
    with aufDieHandlungWarten(seite):
        zeiger.loslassen(daneben)
    return gezeigt


class WeitergereichteAbfragen:
    def __init__(self, seite: Page) -> None:
        self.eingaben: list[dict[str, str]] = []
        self._antworten: list[dict | None] = []
        seite.route("**/stelleBeimLoslassen*", self._weiterreichen)

    def _weiterreichen(self, anfrage: Route) -> None:
        abfrage = parse_qs(urlparse(anfrage.request.url).query)
        self.eingaben.append({name: wert for name, (wert,) in abfrage.items()})
        antwort = anfrage.fetch()
        self._antworten.append(antwort.json() if antwort.ok else None)
        anfrage.fulfill(response=antwort)

    def letzte200VorJederAbfrage(self) -> list[dict | None]:
        letzte: dict | None = None
        vorJeder = []
        for antwort in self._antworten:
            vorJeder.append(letzte)
            if antwort is not None:
                letzte = antwort
        return vorJeder


def zuvorDerEingaben(eingaben: dict[str, str]) -> tuple[float, ...]:
    return tuple(float(eingaben[name]) for name in ("zuvorX", "zuvorY") if name in eingaben)


def alsKörper(eingaben: dict[str, str]) -> dict:
    return {name: json.loads(wert) for name, wert in eingaben.items()}


def überEinenPunktZiehenUndLoslassen(seite: Page, von: Stelle, über: Stelle, nach: Stelle) -> dict:
    zeiger = halten(seite, von, über, "maus")
    abfragen = Abfragen(seite)
    zeiger.bewegen(punktAufDemSpielfeld(seite, nach))
    aufDieAntwortenWarten(seite, abfragen)
    with aufDieHandlungWarten(seite) as antwort:
        zeiger.loslassen(punktAufDemSpielfeld(seite, nach))
    return antwort.value.request.post_data_json


einenZollJenseitsDerKante = -1
längeDesHaltens = 20


def aufDerArmeelisteVonSpielerEins(
    seite: Page, _aufstellung: Aufstellung, _spieler: Spieler
) -> Bildpunkt:
    return mitteVon(armeelisteVon(seite, "Spieler 1"))


def aufDerArmeelisteVonSpielerZwei(
    seite: Page, _aufstellung: Aufstellung, _spieler: Spieler
) -> Bildpunkt:
    return mitteVon(armeelisteVon(seite, "Spieler 2"))


def jenseitsDerKante(seite: Page, aufstellung: Aufstellung, spieler: Spieler) -> Bildpunkt:
    jenseits = stelleInDerZoneVon(aufstellung, spieler, einenZollJenseitsDerKante, längeDesHaltens)
    return punktAufDemSpielfeld(seite, jenseits)


zieleNebenDemSpielfeld = pytest.mark.parametrize(
    "ziel",
    [aufDerArmeelisteVonSpielerEins, aufDerArmeelisteVonSpielerZwei, jenseitsDerKante],
    ids=["aufDerArmeelisteVonSpielerEins", "aufDerArmeelisteVonSpielerZwei", "nebenDemSpielfeld"],
)


def aufDasAnklickenWarten(seite: Page):
    return seite.expect_response("**/anklicken")
