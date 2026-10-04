"""Kommentare und Freigabe des Stakeholders in Plan, Review und Retro, wie der Stand sie liest."""

from collections import Counter
from pathlib import Path
from typing import NamedTuple

from gitAufruf import freigaben
from plan import planDatei, zyklus, zyklusAusText


class Artefakt(NamedTuple):
    datei: str
    gegenstand: str
    autor: str


artefakte = (
    Artefakt(planDatei.name, "Plan", "Planer"),
    Artefakt("review.md", "Review", "Reviewer"),
    Artefakt("retro.md", "Retro", "Organisationsentwickler"),
)
kommentarZeile = "Kommentar:"
stellungnahmeZeile = "Stellungnahme:"
freigabeJa = "Freigabe: ja"
freigabeOffen = "Freigabe: offen"


def zeilenDer(wurzel: Path, artefakt: Artefakt) -> list[str]:
    datei = wurzel / "handoff" / artefakt.datei
    if not datei.is_file():
        return []
    return [zeile.strip() for zeile in datei.read_text(encoding="utf-8").splitlines()]


def hatKommentarOhneStellungnahme(zeilen: list[str]) -> bool:
    """Eine Zeile `Kommentar:` mit anderem Text als `.`, auf die keine `Stellungnahme:` folgt."""
    for nummer, zeile in enumerate(zeilen):
        text = zeile.removeprefix(kommentarZeile).strip()
        if not zeile.startswith(kommentarZeile) or text in ("", "."):
            continue
        folgende = [spätere for spätere in zeilen[nummer + 1 :] if spätere]
        if not folgende or not folgende[0].startswith(stellungnahmeZeile):
            return True
    return False


def autorenDran(wurzel: Path) -> dict[str, list[str]]:
    """Autor → Dateien mit einem Kommentar ohne Stellungnahme."""
    dran: dict[str, list[str]] = {}
    for artefakt in artefakte:
        if hatKommentarOhneStellungnahme(zeilenDer(wurzel, artefakt)):
            dran.setdefault(artefakt.autor, []).append(artefakt.datei)
    return dran


def freigabeZuCommitten(wurzel: Path) -> str | None:
    """Der Commit-Betreff `Freigabe <Gegenstand> <n>`, wenn die Datei `Freigabe: ja` trägt."""
    betreffs = {betreff for _, betreff in freigaben(wurzel)}
    for artefakt in artefakte:
        nummer = zyklus(wurzel / "handoff" / artefakt.datei)
        if nummer is None or freigabeJa not in zeilenDer(wurzel, artefakt):
            continue
        if f"Freigabe {artefakt.gegenstand} {nummer}" not in betreffs:
            return f"Freigabe {artefakt.gegenstand} {nummer}"
    return None


def stakeholderZeilen(text: str) -> list[str]:
    """Zeilen `Kommentar:` mit anderem Text als `.`; sie gehören dem Stakeholder."""
    zeilen = [zeile.strip() for zeile in text.splitlines()]
    return [
        zeile
        for zeile in zeilen
        if zeile.startswith(kommentarZeile)
        and zeile.removeprefix(kommentarZeile).strip() not in ("", ".")
    ]


def freigabeVerstoß(bisher: str, danach: str) -> str | None:
    """Warum eine Rolle Freigabe oder Kommentare nicht so ändern darf, sonst `None`."""
    neueZeilen = [zeile.strip() for zeile in danach.splitlines()]
    if zyklusAusText(bisher) != zyklusAusText(danach):
        # Warum: Die Datei des nächsten Zyklus beginnt neu, aber nie schon freigegeben.
        return "beginnt mit `Freigabe: ja`; das setzt nur der Stakeholder." if (
            freigabeJa in neueZeilen
        ) else None
    alteZeilen = [zeile.strip() for zeile in bisher.splitlines()]
    if freigabeJa in neueZeilen and freigabeJa not in alteZeilen:
        return "setzt `Freigabe: ja`; das tut nur der Stakeholder."
    if freigabeOffen in alteZeilen and freigabeOffen not in neueZeilen:
        return "ändert `Freigabe: offen`; das tut nur der Stakeholder."
    verloren = Counter(stakeholderZeilen(bisher)) - Counter(stakeholderZeilen(danach))
    if verloren:
        return f"ändert oder entfernt `{next(iter(verloren))}`; Kommentare bleiben dem Stakeholder."
    return None
