import re
from collections.abc import Callable

from playwright.sync_api import Locator, Page, expect

from tests.akzeptanz.bildschirm import einheitenKarteVon, elementeDerSeite


def ausgewählteEinheiten(seite: Page) -> frozenset[str]:
    namen = seite.locator(".einheitenKarte.ausgewählt .einheitenKartenName span:first-child")
    return frozenset(namen.all_text_contents())


def ausgewählteModelle(seite: Page) -> frozenset[tuple[float, float]]:
    kreise = elementeDerSeite(seite, ".spielfeld .modell.ausgewählt")
    return frozenset((kreis.zahl("cx"), kreis.zahl("cy")) for kreis in kreise)


ausgewähltGekennzeichnet = re.compile(r"\bausgewählt\b")


def _berührenUndWarten(
    seite: Page, spielername: str, einheitenname: str, berühren: Callable[[Locator], None]
) -> None:
    karte = einheitenKarteVon(seite, spielername, einheitenname)
    warAusgewählt = einheitenname in ausgewählteEinheiten(seite)
    berühren(karte)
    if warAusgewählt:
        expect(karte).not_to_have_class(ausgewähltGekennzeichnet)
    else:
        expect(karte).to_have_class(ausgewähltGekennzeichnet)


def klickenUndWarten(seite: Page, spielername: str, einheitenname: str) -> None:
    _berührenUndWarten(seite, spielername, einheitenname, Locator.click)


def tippenUndWarten(seite: Page, spielername: str, einheitenname: str) -> None:
    _berührenUndWarten(seite, spielername, einheitenname, Locator.tap)


auswählenMit = {"maus": klickenUndWarten, "finger": tippenUndWarten}
