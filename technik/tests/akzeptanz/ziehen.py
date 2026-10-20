"""Bedienung der Akzeptanztests: Klicken und Ziehen mit Maus und Finger, mit und ohne Antwort."""

from dataclasses import dataclass

import pytest
from playwright.sync_api import Locator, Page, Request, Response

from arbiter.domaene.spielobjekte import Stelle
from tests.akzeptanz.bildschirm import ablageVon, aufDieHandlungWarten


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


def mitDerMausZiehen(seite: Page, von: Bildpunkt, nach: Bildpunkt) -> None:
    seite.mouse.move(von.links, von.oben)
    seite.mouse.down()
    seite.mouse.move(nach.links, nach.oben, steps=10)
    seite.mouse.up()


_schritteDesFingers = 10


def mitDemFingerZiehen(seite: Page, von: Bildpunkt, nach: Bildpunkt) -> None:
    """Berührt, wischt und hebt ab über CDP `Input.dispatchTouchEvent` (Web, B5)."""
    sitzung = seite.context.new_cdp_session(seite)

    def berührung(art: str, ort: Bildpunkt | None) -> None:
        punkte = [] if ort is None else [{"x": ort.links, "y": ort.oben}]
        sitzung.send("Input.dispatchTouchEvent", {"type": art, "touchPoints": punkte})

    berührung("touchStart", von)
    for schritt in range(1, _schritteDesFingers + 1):
        anteil = schritt / _schritteDesFingers
        unterwegs = Bildpunkt(
            von.links + (nach.links - von.links) * anteil,
            von.oben + (nach.oben - von.oben) * anteil,
        )
        berührung("touchMove", unterwegs)
    berührung("touchEnd", None)


eingaben = {"maus": mitDerMausZiehen, "finger": mitDemFingerZiehen}


def _ziehenBisZurAntwort(seite: Page, eingabe: str, von: Bildpunkt, nach: Bildpunkt) -> Response:
    with aufDieHandlungWarten(seite) as antwort:
        eingaben[eingabe](seite, von, nach)
    return antwort.value


def modellZiehen(seite: Page, von: Stelle, nach: Stelle, eingabe: str = "maus") -> Response:
    """Zieht das Modell an der Stelle auf die Karte und wartet auf die Antwort."""
    return _ziehenBisZurAntwort(
        seite, eingabe, punktAufDerKarte(seite, von), punktAufDerKarte(seite, nach)
    )


def modellAufDieAblageZiehen(
    seite: Page, von: Stelle, spielername: str, eingabe: str = "maus"
) -> Response:
    ziel = mitteVon(ablageVon(seite, spielername))
    return _ziehenBisZurAntwort(seite, eingabe, punktAufDerKarte(seite, von), ziel)


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


def amKopfDerSeite(seite: Page) -> Bildpunkt:
    """Ein Punkt neben Karte und Ablagen: die Kopfzeile."""
    return mitteVon(seite.locator(".kopfzeile"))


def mitDerMausKlicken(seite: Page, punkt: Bildpunkt) -> None:
    seite.mouse.click(punkt.links, punkt.oben)


def mitDemFingerTippen(seite: Page, punkt: Bildpunkt) -> None:
    seite.touchscreen.tap(punkt.links, punkt.oben)


klickenMit = {"maus": mitDerMausKlicken, "finger": mitDemFingerTippen}
mitMausUndFinger = pytest.mark.parametrize("eingabe", list(klickenMit), ids=list(klickenMit))


def aufDieEbeneWarten(seite: Page):
    """Wartet auf die Antwort des Dienstes auf das Anklicken eines Modells (V9)."""
    return seite.expect_response("**/ebene")
