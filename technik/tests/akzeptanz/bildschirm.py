import re
from collections.abc import Mapping
from dataclasses import dataclass
from functools import partial
from urllib.parse import unquote

from playwright.sync_api import Browser, Locator, Page, Response, Route, expect

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.sperre import Grund
from arbiter.domaene.spielobjekte import Spieler
from arbiter.web.server import serverStarten


@dataclass(frozen=True)
class Element:
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
    farbeJeStelle = {
        (kreis.zahl("cx"), kreis.zahl("cy")): kreis.fill
        for kreis in elementeDerSeite(seite, ".karte .modell")
    }
    return frozenset(
        farbeJeStelle[float(stelle.x), float(stelle.y)]
        for modell in spieler.armee.modelle
        if (stelle := aufstellung.stelle(modell)) is not None
    )


def kreiseDerKarte(seite: Page) -> frozenset[tuple[float, float]]:
    kreise = elementeDerSeite(seite, ".karte .modell")
    return frozenset((kreis.zahl("cx"), kreis.zahl("cy")) for kreis in kreise)


def inhaltDerSeite(seite: Page) -> str:
    return seite.evaluate(
        "() => ['.kopfzeile', '.spielbereich'].map(a => document.querySelector(a).innerHTML).join()"
    )


_strichLesen = """element => {
    const stil = getComputedStyle(element)
    return [stil.stroke, stil.strokeWidth].join(' ')
}"""


def strichVon(element: Locator) -> str:
    return element.evaluate(_strichLesen)


def einheitenKarteVon(seite: Page, spielername: str, einheitenname: str) -> Locator:
    return armeelisteVon(seite, spielername).locator(".einheitenKarte", has_text=einheitenname)


def spielerAnDerReihe(seite: Page) -> Locator:
    return seite.locator(".kopfzeileSpieler").filter(has=seite.locator(".kopfzeileAnDerReihe"))


def neuLaden(seite: Page) -> None:
    seite.reload()
    _aufDasSpielfeldWarten(seite)


def _aufDasSpielfeldWarten(seite: Page) -> None:
    seite.wait_for_selector(".karte .spielfeld")


def armeelisteVon(seite: Page, spielername: str) -> Locator:
    name = seite.locator(".armeeKartenName", has_text=spielername)
    return seite.locator(".armeeKarte").filter(has=name)


pfadeDesAuswählens = ("/ausgewählt", "/anklicken")


def istHandlung(antwort: Response) -> bool:
    anfrage = antwort.request
    pfad = unquote(anfrage.url)
    return anfrage.method in ("PUT", "DELETE") and not any(
        teil in pfad for teil in pfadeDesAuswählens
    )


def aufDieHandlungWarten(seite: Page):
    return seite.expect_response(istHandlung)


def gründeAlsText(gründe) -> frozenset[str]:
    return frozenset(grund.value for grund in gründe)


def sperrmeldungWarten(seite: Page, gründe: frozenset[Grund]) -> frozenset[str]:
    meldungen = seite.locator(".sperrmeldung .sperrmeldungGrund")
    expect(meldungen).to_have_count(len(gründe))
    return frozenset(text.strip() for text in meldungen.all_text_contents())


def sperrmeldungenDerSeite(seite: Page) -> list[str]:
    meldungen = seite.locator(".sperrmeldung .sperrmeldungGrund")
    return [text.strip() for text in meldungen.all_text_contents()]


beendenKnopf = "Aufstellen der Einheit beenden"
phaseBeendenKnopf = "Phase beenden"
zurücklegenKnopf = "Einheit zurücklegen"


def knopfDerSeite(seite: Page, text: str) -> Locator:
    gleicherText = re.compile(rf"^\s*{re.escape(text)}\s*$")
    return seite.locator(".knopfGruppe .knopf").filter(has_text=gleicherText)


def knopfDerArmeeliste(seite: Page, spielername: str, text: str) -> Locator:
    gleicherText = re.compile(rf"^\s*{re.escape(text)}\s*$")
    knöpfe = armeelisteVon(seite, spielername).locator(".knopfGruppe .knopf")
    return knöpfe.filter(has_text=gleicherText)


übergehenKnopf = "gemeinsam übergehen"


def leisteVon(seite: Page, inhalt: str) -> Locator:
    return seite.get_by_role("complementary", name=inhalt, exact=True)


def griffVon(seite: Page, inhalt: str) -> Locator:
    return seite.get_by_role("button", name=f"{inhalt} ein- und ausfahren", exact=True)


def protokollEinträge(seite: Page) -> Locator:
    return leisteVon(seite, "Protokoll").locator(".protokollEintrag")


def eintragDerEinheit(seite: Page, einheitenname: str) -> Locator:
    einheit = seite.locator(".protokollEinheit", has_text=einheitenname)
    return protokollEinträge(seite).filter(has=einheit)


def textDesEintrags(eintrag: Locator) -> tuple[str, str, frozenset[str]]:
    einheit = eintrag.locator(".protokollEinheit").text_content().strip()
    spieler = eintrag.locator(".protokollSpieler").text_content().strip()
    gründe = eintrag.locator(".protokollGrund").all_text_contents()
    return einheit, spieler, frozenset(grund.strip() for grund in gründe)


def protokollDerSeite(seite: Page) -> frozenset[tuple[str, str, frozenset[str]]]:
    return frozenset(textDesEintrags(eintrag) for eintrag in protokollEinträge(seite).all())


def kopfzeileVon(seite: Page, spielername: str) -> Locator:
    return seite.locator(".kopfzeileSpieler", has_text=spielername)


def spielerAmZug(seite: Page) -> Locator:
    return seite.locator(".kopfzeileSpieler.amZug")


amZugGekennzeichnet = re.compile(r"\bamZug\b")


def seiteMitEingabe(bildschirm: "Bildschirm", aufstellung: Aufstellung, eingabe: str) -> Page:
    return bildschirm.seiteZu(aufstellung, berührbar=eingabe == "finger")


def seiteDerSchlachtMitEingabe(
    bildschirm: "Bildschirm", aufstellung: Aufstellung, schlacht, eingabe: str
) -> Page:
    return bildschirm.seiteZuSchlacht(aufstellung, schlacht, berührbar=eingabe == "finger")


def _liefern(antwort: dict, anfrage: Route) -> None:
    anfrage.fulfill(json=antwort)


wartezeitInMillisekunden = 5000


class Bildschirm:
    def __init__(self, browser: Browser) -> None:
        self._browser = browser
        self._seiten: list[Page] = []
        self._server: list = []

    def seiteBei(self, adresse: str, *, berührbar: bool = False) -> Page:
        seite = self._neueSeite(berührbar=berührbar)
        seite.goto(adresse)
        _aufDasSpielfeldWarten(seite)
        return seite

    def seiteMitSpielstand(
        self, aufstellung: Aufstellung, spielstand: dict, weitere: Mapping[str, dict] | None = None
    ) -> Page:
        seite = self._neueSeite(berührbar=False)

        for muster, antwort in {"**/api/spielstand": spielstand, **(weitere or {})}.items():
            seite.route(muster, partial(_liefern, antwort))
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
        server = serverStarten(aufstellung)
        self._server.append(server)
        return self.seiteBei(server.adresse, berührbar=berührbar)

    def seiteZuSchlacht(
        self, aufstellung: Aufstellung, schlacht, *, berührbar: bool = False
    ) -> Page:
        server = serverStarten(aufstellung, schlacht=schlacht)
        self._server.append(server)
        return self.seiteBei(server.adresse, berührbar=berührbar)

    def beenden(self) -> None:
        for seite in self._seiten:
            seite.context.close()
        for server in self._server:
            server.beenden()
