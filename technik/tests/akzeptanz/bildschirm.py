"""Bildschirm der Akzeptanztests: Browser, Server und das Lesen der Seite."""

import re
from dataclasses import dataclass
from urllib.parse import unquote

from playwright.sync_api import Browser, Locator, Page, Response, expect

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.sperre import Grund
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


def inhaltDerSeite(seite: Page) -> str:
    """Kopfzeile, Ablagen und Karte, wie der Browser sie zeigt."""
    return seite.evaluate(
        "() => ['.kopfzeile', '.spielbereich'].map(a => document.querySelector(a).innerHTML).join()"
    )


_strichLesen = """element => {
    const stil = getComputedStyle(element)
    return [stil.stroke, stil.strokeWidth].join(' ')
}"""


def strichVon(element: Locator) -> str:
    """Farbe und Breite des Rands eines Kreises, wie der Browser ihn zeichnet."""
    return element.evaluate(_strichLesen)


def einheitenKarteVon(seite: Page, spielername: str, einheitenname: str) -> Locator:
    return ablageVon(seite, spielername).locator(".einheitenKarte", has_text=einheitenname)


def spielerAnDerReihe(seite: Page) -> Locator:
    """Die Kopfzeile des Spielers, die „an der Reihe“ zeigt."""
    return seite.locator(".kopfzeileSpieler").filter(has=seite.locator(".kopfzeileAnDerReihe"))


def neuLaden(seite: Page) -> None:
    seite.reload()
    _aufDasSpielfeldWarten(seite)


def _aufDasSpielfeldWarten(seite: Page) -> None:
    seite.wait_for_selector(".karte .spielfeld")


def ablageVon(seite: Page, spielername: str) -> Locator:
    name = seite.locator(".armeeKartenName", has_text=spielername)
    return seite.locator(".armeeKarte").filter(has=name)


def istHandlung(antwort: Response) -> bool:
    """Eine Antwort auf eine Handlung: ändernde Anfrage, die kein Auswählen ist."""
    anfrage = antwort.request
    return anfrage.method in ("PUT", "DELETE") and "/ausgewählt" not in unquote(anfrage.url)


def aufDieHandlungWarten(seite: Page):
    return seite.expect_response(istHandlung)


def gesperrteModelle(seite: Page) -> frozenset[tuple[float, float]]:
    """Die Stellen der Kreise auf der Karte, die als gesperrt gekennzeichnet sind."""
    kreise = elementeDerSeite(seite, ".karte .modell.gesperrt")
    return frozenset((kreis.zahl("cx"), kreis.zahl("cy")) for kreis in kreise)


def kennzeichenDesKreises(seite: Page, auswahl: str) -> tuple[str, str]:
    """Füllung und Strich des ersten Kreises der Auswahl, wie der Browser sie zeichnet."""
    kreis = seite.locator(auswahl).first
    return elementeDerSeite(seite, auswahl)[0].fill, strichVon(kreis)


def gründeAlsText(gründe) -> frozenset[str]:
    return frozenset(grund.value for grund in gründe)


def sperrmeldungWarten(seite: Page, gründe: frozenset[Grund]) -> frozenset[str]:
    """Wartet, bis die Seite so viele Gründe nennt, wie erwartet, und gibt ihren Text zurück."""
    meldungen = seite.locator(".sperrmeldung .sperrmeldungGrund")
    expect(meldungen).to_have_count(len(gründe))
    return frozenset(text.strip() for text in meldungen.all_text_contents())


def sperrmeldungenDerSeite(seite: Page) -> list[str]:
    meldungen = seite.locator(".sperrmeldung .sperrmeldungGrund")
    return [text.strip() for text in meldungen.all_text_contents()]


def knopfDerSeite(seite: Page, text: str) -> Locator:
    gleicherText = re.compile(rf"^\s*{re.escape(text)}\s*$")
    return seite.locator(".knopfGruppe .knopf").filter(has_text=gleicherText)


def seiteMitEingabe(bildschirm: "Bildschirm", aufstellung: Aufstellung, eingabe: str) -> Page:
    return bildschirm.seiteZu(aufstellung, berührbar=eingabe == "finger")


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
        seite = self._neueSeite(berührbar=berührbar)
        seite.goto(adresse)
        _aufDasSpielfeldWarten(seite)
        return seite

    def seiteMitSpielstand(self, aufstellung: Aufstellung, spielstand: dict) -> Page:
        """Öffnet die Seite des Servers, der Spielstand kommt statt vom Dienst aus dem Argument."""
        seite = self._neueSeite(berührbar=False)

        def spielstandLiefern(anfrage) -> None:
            anfrage.fulfill(json=spielstand)

        seite.route("**/api/spielstand", spielstandLiefern)
        server = serverStarten(aufstellung)
        self._server.append(server)
        seite.goto(server.adresse)
        _aufDasSpielfeldWarten(seite)
        return seite

    def _neueSeite(self, *, berührbar: bool) -> Page:
        seite = self._browser.new_context(has_touch=berührbar).new_page()
        self._seiten.append(seite)
        seite.set_default_timeout(wartezeitInMillisekunden)
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
