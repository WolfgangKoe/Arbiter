"""Bildschirm der Akzeptanztests: Browser, Server und was die Seite zeigt."""

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
    }
})"""


# Warum: Länger als das wartet Playwright nicht; dann antwortet der Server nicht
wartezeitInMillisekunden = 5000


class Bildschirm:
    """Browser und Server der Bildschirmtests; schließt, was er geöffnet hat."""

    def __init__(self, browser: Browser) -> None:
        self._browser = browser
        self._seiten: list[Page] = []
        self._server: list = []

    def seiteBei(self, adresse: str) -> Page:
        """Öffnet die Adresse und wartet auf das Spielfeld, erst dann gilt, was die Seite zeigt."""
        seite = self._browser.new_page()
        self._seiten.append(seite)
        seite.set_default_timeout(wartezeitInMillisekunden)
        seite.goto(adresse)
        seite.wait_for_selector(".karte .spielfeld")
        return seite

    def seiteZu(self, aufstellung: Aufstellung) -> Page:
        """Startet den Server mit dem Spielstand im selben Prozess und öffnet seine Seite."""
        server = serverStarten(aufstellung)
        self._server.append(server)
        return self.seiteBei(server.adresse)

    def elementeDerSeite(self, seite: Page, auswahl: str) -> tuple[Element, ...]:
        gelesen = seite.locator(auswahl).evaluate_all(_elementeLesen)
        return tuple(Element(**eintrag) for eintrag in gelesen)

    def modellfarben(
        self, seite: Page, aufstellung: Aufstellung, spieler: Spieler
    ) -> frozenset[str]:
        """Die Füllfarben der Kreise an den Stellen der gesetzten Modelle des Spielers."""
        farbeJeStelle = {
            (kreis.zahl("cx"), kreis.zahl("cy")): kreis.fill
            for kreis in self.elementeDerSeite(seite, ".karte .modell")
        }
        return frozenset(
            farbeJeStelle[float(stelle.x), float(stelle.y)]
            for modell in spieler.armee.modelle
            if (stelle := aufstellung.stelle(modell)) is not None
        )

    def ablageVon(self, seite: Page, spielername: str) -> Locator:
        name = seite.locator(".armeeKartenName", has_text=spielername)
        return seite.locator(".armeeKarte").filter(has=name)

    def beenden(self) -> None:
        for seite in self._seiten:
            seite.close()
        for server in self._server:
            server.beenden()
