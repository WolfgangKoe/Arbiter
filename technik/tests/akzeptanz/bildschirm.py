"""Bildschirm der Akzeptanztests: Browser, Server und das Lesen der Seite."""

from dataclasses import dataclass

from playwright.sync_api import Browser, Locator, Page

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Spieler
from arbiter.web.server import serverStarten


@dataclass(frozen=True)
class Element:
    """Ein Element der Seite, wie der Browser es zeigt."""

    art: str
    attribute: dict[str, str]
    fill: str
    farbe: str
    text: str
    breiteInPixeln: float
    höheInPixeln: float
    mitteInPixeln: float

    def zahl(self, name: str) -> float:
        return float(self.attribute[name])


_elementeLesen = """elemente => elemente.map(element => {
    const stil = getComputedStyle(element)
    const rahmen = element.getBoundingClientRect()
    return {
        art: element.tagName.toLowerCase(),
        attribute: Object.fromEntries([...element.attributes].map(att => [att.name, att.value])),
        fill: stil.fill,
        farbe: stil.color,
        text: element.textContent.trim(),
        breiteInPixeln: rahmen.width,
        höheInPixeln: rahmen.height,
        mitteInPixeln: rahmen.left + rahmen.width / 2,
    }
})"""


def elementeDerSeite(seite: Page, auswahl: str) -> tuple[Element, ...]:
    gelesen = seite.locator(auswahl).evaluate_all(_elementeLesen)
    return tuple(Element(**eintrag) for eintrag in gelesen)


def modellfarben(seite: Page, aufstellung: Aufstellung, spieler: Spieler) -> frozenset[str]:
    """Die Füllfarben der Kreise an den Stellen der gesetzten Modelle des Spielers."""
    farbeJeStelle = {
        (kreis.zahl("cx"), kreis.zahl("cy")): kreis.fill
        for kreis in elementeDerSeite(seite, ".karte .modell")
    }
    return frozenset(
        farbeJeStelle[float(stelle.x), float(stelle.y)]
        for modell in spieler.armee.modelle
        if (stelle := aufstellung.stelle(modell)) is not None
    )


def ausgewählteEinheiten(seite: Page) -> frozenset[str]:
    """Die Namen der Einheiten, deren Karte in einer Ablage als ausgewählt gekennzeichnet ist."""
    namen = seite.locator(".einheitenKarte.ausgewählt .einheitenKartenName span:first-child")
    return frozenset(namen.all_text_contents())


def ausgewählteModelle(seite: Page) -> frozenset[tuple[float, float]]:
    """Die Stellen der Kreise auf der Karte, die als ausgewählt gekennzeichnet sind."""
    kreise = elementeDerSeite(seite, ".karte .modell.ausgewählt")
    return frozenset((kreis.zahl("cx"), kreis.zahl("cy")) for kreis in kreise)


def inhaltDerSeite(seite: Page) -> str:
    """Kopfzeile, Ablagen und Karte, wie der Browser sie zeigt."""
    return seite.evaluate(
        "() => ['.kopfzeile', '.spielbereich'].map(a => document.querySelector(a).innerHTML).join()"
    )


_umrissLesen = """element => {
    const stil = getComputedStyle(element)
    return [stil.outlineStyle, stil.outlineWidth, stil.outlineColor].join(' ')
}"""


def umrissVon(element: Locator) -> str:
    """Art, Breite und Farbe des Umrisses, wie der Browser ihn zeichnet."""
    return element.evaluate(_umrissLesen)


_strichLesen = """element => {
    const stil = getComputedStyle(element)
    return [stil.stroke, stil.strokeWidth].join(' ')
}"""


def strichVon(element: Locator) -> str:
    """Farbe und Breite des Rands eines Kreises, wie der Browser ihn zeichnet."""
    return element.evaluate(_strichLesen)


def einheitenKarteVon(seite: Page, spielername: str, einheitenname: str) -> Locator:
    return ablageVon(seite, spielername).locator(".einheitenKarte", has_text=einheitenname)


def ablageVon(seite: Page, spielername: str) -> Locator:
    name = seite.locator(".armeeKartenName", has_text=spielername)
    return seite.locator(".armeeKarte").filter(has=name)


# Warum: Länger als das wartet Playwright nicht; dann antwortet der Server nicht
wartezeitInMillisekunden = 5000


class Bildschirm:
    """Browser und Server der Bildschirmtests; schließt, was er geöffnet hat."""

    def __init__(self, browser: Browser) -> None:
        self._browser = browser
        self._seiten: list[Page] = []
        self._server: list = []

    def seiteBei(self, adresse: str, *, berührbar: bool = False) -> Page:
        """Öffnet die Adresse und wartet auf das Spielfeld, erst dann gilt, was die Seite zeigt."""
        seite = self._browser.new_context(has_touch=berührbar).new_page()
        self._seiten.append(seite)
        seite.set_default_timeout(wartezeitInMillisekunden)
        seite.goto(adresse)
        seite.wait_for_selector(".karte .spielfeld")
        return seite

    def seiteZu(self, aufstellung: Aufstellung, *, berührbar: bool = False) -> Page:
        """Startet den Server mit dem Spielstand im selben Prozess und öffnet seine Seite."""
        server = serverStarten(aufstellung)
        self._server.append(server)
        return self.seiteBei(server.adresse, berührbar=berührbar)

    def beenden(self) -> None:
        for seite in self._seiten:
            seite.context.close()
        for server in self._server:
            server.beenden()
