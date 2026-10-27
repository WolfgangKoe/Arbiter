"""Bedienung der Akzeptanztests: Klicken, Ziehen und Halten mit Maus und Finger."""

from dataclasses import dataclass
from fractions import Fraction
from math import hypot

import pytest
from playwright.sync_api import Locator, Page, Request, Response

from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.bildschirm import aufDieHandlungWarten, kreiseDerKarte
from tests.akzeptanz.schlacht import hundertstelZoll


@dataclass(frozen=True)
class Bildpunkt:
    """Ein Punkt der Seite in Pixeln."""

    links: float
    oben: float


def mitteVon(element: Locator) -> Bildpunkt:
    element.scroll_into_view_if_needed()
    rahmen = element.bounding_box()
    return Bildpunkt(rahmen["x"] + rahmen["width"] / 2, rahmen["y"] + rahmen["height"] / 2)


_punktAufDerKarteLesen = """(karte, ort) => {
    const punkt = karte.createSVGPoint()
    punkt.x = ort[0]
    punkt.y = ort[1]
    const bild = punkt.matrixTransform(karte.getScreenCTM())
    return [bild.x, bild.y]
}"""


def punktAufDerKarte(seite: Page, stelle: Stelle) -> Bildpunkt:
    """Wo die Stelle in Zoll auf dem Bildschirm liegt, über `getScreenCTM()` der Karte."""
    links, oben = seite.locator("svg.karte").evaluate(
        _punktAufDerKarteLesen, [float(stelle.x), float(stelle.y)]
    )
    return Bildpunkt(links, oben)


def zollJePixel(seite: Page) -> float:
    """So viele Zoll der Karte hat ein Pixel; der Zeiger kennt nur Pixel (Web, B5)."""
    return seite.locator("svg.karte").evaluate("karte => 1 / karte.getScreenCTM().a")


def liegtEinPixelGenauAn(seite: Page, ist: Stelle, soll: Stelle) -> bool:
    toleranz = zollJePixel(seite)
    abweichungInX = abs(float(ist.x) - float(soll.x))
    abweichungInY = abs(float(ist.y) - float(soll.y))
    return abweichungInX <= toleranz and abweichungInY <= toleranz


def hältAnDerBewegungsweiteAufEinenPixelGenau(
    seite: Page, davor: Stelle, gezeigt: tuple[float, float], bewegungsweite: Fraction
) -> bool:
    """Der gezeigte Punkt liegt höchstens die Bewegungsweite und 1/100″ davor von `davor`."""
    gezeigtInX, gezeigtInY = gezeigt
    abstand = hypot(gezeigtInX - float(davor.x), gezeigtInY - float(davor.y))
    toleranz = zollJePixel(seite)
    weite = float(bewegungsweite)
    return weite - float(hundertstelZoll) - toleranz <= abstand <= weite + toleranz


class Maus:
    """Drücken, Bewegen und Loslassen mit `page.mouse` (Web, B5)."""

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
    """Berühren, Wischen und Abheben über CDP `Input.dispatchTouchEvent` (Web, B5)."""

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
    """Zieht das Modell an der Stelle auf die Karte und wartet auf die Antwort."""
    anfang = punktAufDerKarte(seite, von)
    ende = punktAufDerKarte(seite, nach)
    with aufDieHandlungWarten(seite) as antwort:
        eingaben[eingabe](seite, anfang, ende)
    return antwort.value


_bildaufbauAbwarten = "() => new Promise(fertig => requestAnimationFrame(() => fertig()))"


def ziehenOhneAnfrage(
    seite: Page, von: Bildpunkt, nach: Bildpunkt, eingabe: str = "maus"
) -> list[Request]:
    """Zieht und lässt los; gibt die ändernden Anfragen zurück, die dabei die Seite verließen."""
    anfragen: list[Request] = []

    def merken(anfrage: Request) -> None:
        if anfrage.method != "GET":
            anfragen.append(anfrage)

    seite.on("request", merken)
    eingaben[eingabe](seite, von, nach)
    seite.evaluate(_bildaufbauAbwarten)
    seite.evaluate(_bildaufbauAbwarten)
    seite.remove_listener("request", merken)
    return anfragen


def mitDerMausKlicken(seite: Page, punkt: Bildpunkt) -> None:
    seite.mouse.click(punkt.links, punkt.oben)


def mitDemFingerTippen(seite: Page, punkt: Bildpunkt) -> None:
    seite.touchscreen.tap(punkt.links, punkt.oben)


klickenMit = {"maus": mitDerMausKlicken, "finger": mitDemFingerTippen}
mitMausUndFinger = pytest.mark.parametrize("eingabe", list(klickenMit), ids=list(klickenMit))


class Abfragen:
    """Zählt die Anfragen der Seite nach der Stelle beim Loslassen und deren Antworten."""

    def __init__(self, seite: Page) -> None:
        self.gestellt = 0
        self.erledigt = 0
        seite.on("request", self._gestellt)
        seite.on("requestfinished", self._erledigt)
        seite.on("requestfailed", self._erledigt)

    @staticmethod
    def _istAbfrage(anfrage: Request) -> bool:
        return "/stelleBeimLoslassen" in anfrage.url

    def _gestellt(self, anfrage: Request) -> None:
        if self._istAbfrage(anfrage):
            self.gestellt += 1

    def _erledigt(self, anfrage: Request) -> None:
        if self._istAbfrage(anfrage):
            self.erledigt += 1

    def ruhig(self) -> bool:
        return self.gestellt > 0 and self.gestellt == self.erledigt


_pausenInMillisekunden = 50
_ruhigeProben = 4
_höchstensProben = 200


def aufDieAntwortenWarten(seite: Page, abfragen: Abfragen) -> None:
    """Wartet, bis die Abfragen eine Weile ruhen; erst dann zeigt die Karte den Zeigerpunkt."""
    ruhige = 0
    for _ in range(_höchstensProben):
        seite.wait_for_timeout(_pausenInMillisekunden)
        ruhige = ruhige + 1 if abfragen.ruhig() else 0
        if ruhige == _ruhigeProben:
            return
    raise TimeoutError("Die Seite fragt nicht nach der Stelle beim Loslassen oder antwortet nicht")


def halten(seite: Page, von: Stelle, nach: Stelle, eingabe: str) -> Maus | Finger:
    """Drückt an `von`, bewegt nach `nach` und wartet auf die Antworten, ohne loszulassen."""
    zeiger = zeigerArten[eingabe](seite)
    abfragen = Abfragen(seite)
    zeiger.drücken(punktAufDerKarte(seite, von))
    zeiger.bewegen(punktAufDerKarte(seite, nach))
    aufDieAntwortenWarten(seite, abfragen)
    return zeiger


def haltenUndLosslassen(
    seite: Page, von: Stelle, nach: Stelle, eingabe: str
) -> frozenset[tuple[float, float]]:
    """Hält am Ziel, liest die Kreise der Karte und lässt am selben Punkt los."""
    zeiger = halten(seite, von, nach, eingabe)
    gezeigt = kreiseDerKarte(seite)
    with aufDieHandlungWarten(seite):
        zeiger.loslassen(punktAufDerKarte(seite, nach))
    return gezeigt


def aufDieEbeneWarten(seite: Page):
    """Wartet auf die Antwort des Dienstes auf das Anklicken eines Modells (V9)."""
    return seite.expect_response("**/ebene")
