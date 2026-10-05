"""Kommentare und Freigabe des Stakeholders in Plan, Review und Retro, wie der Stand sie liest."""

import re
from collections import Counter
from pathlib import Path
from typing import NamedTuple

from gemeinsam.gitAufruf import freigaben
from gemeinsam.pfade import handoffOrdner
from standregeln.plan import planDatei, zyklus, zyklusAusText


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
freigabeAbschnitt = "Freigabe"
überschrift = re.compile(r"^## (.+)$")


def artefaktVon(gegenstand: str) -> Artefakt:
    return next(artefakt for artefakt in artefakte if artefakt.gegenstand == gegenstand)


def pfadDer(wurzel: Path, artefakt: Artefakt) -> Path:
    return wurzel / handoffOrdner / artefakt.datei


def zeilenDer(wurzel: Path, artefakt: Artefakt) -> list[str]:
    datei = pfadDer(wurzel, artefakt)
    if not datei.is_file():
        return []
    return [zeile.strip() for zeile in datei.read_text(encoding="utf-8").splitlines()]


def abschnitte(zeilen: list[str]) -> list[tuple[str, list[str]]]:
    """Paare (Überschrift, Zeilen), in Reihenfolge der Datei, auch bei wiederholter Überschrift."""
    gefunden: list[tuple[str, list[str]]] = []
    for zeile in zeilen:
        treffer = überschrift.match(zeile)
        if treffer:
            gefunden.append((treffer[1], []))
        elif gefunden:
            gefunden[-1][1].append(zeile)
    return gefunden


def freigabeZeilen(zeilen: list[str]) -> list[str]:
    """Die Zeilen unter `## Freigabe`; nur dort steht das Feld."""
    return [
        zeile
        for titel, inhalt in abschnitte(zeilen)
        if titel == freigabeAbschnitt
        for zeile in inhalt
    ]


def freigegebenerZyklus(wurzel: Path, artefakt: Artefakt) -> int | None:
    """Der Zyklus der Datei, wenn `## Freigabe` `Freigabe: ja` trägt, sonst `None`."""
    if freigabeJa not in freigabeZeilen(zeilenDer(wurzel, artefakt)):
        return None
    return zyklus(pfadDer(wurzel, artefakt))


def istStakeholderKommentar(zeile: str) -> bool:
    """Eine Zeile `Kommentar:` mit anderem Text als `.`; sie gehört dem Stakeholder."""
    return zeile.startswith(kommentarZeile) and zeile.removeprefix(kommentarZeile).strip() not in (
        "",
        ".",
    )


def hatKommentarOhneStellungnahme(zeilen: list[str]) -> bool:
    """Ein Kommentar des Stakeholders, auf den keine `Stellungnahme:` folgt."""
    for nummer, zeile in enumerate(zeilen):
        if not istStakeholderKommentar(zeile):
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
    vorhanden = {betreff for _, betreff in freigaben(wurzel)}
    for artefakt in artefakte:
        nummer = freigegebenerZyklus(wurzel, artefakt)
        betreff = f"Freigabe {artefakt.gegenstand} {nummer}"
        if nummer is not None and betreff not in vorhanden:
            return betreff
    return None


def geschützteZeilen(text: str) -> list[str]:
    """`Freigabe: ja` und Kommentare des Stakeholders; beide ändert nur er."""
    zeilen = [zeile.strip() for zeile in text.splitlines()]
    return [zeile for zeile in zeilen if zeile == freigabeJa or istStakeholderKommentar(zeile)]


def freigabeVerstoß(bisher: str, danach: str) -> str | None:
    """Warum eine Rolle Freigabe oder Kommentare nicht so ändern darf, sonst `None`."""
    alteZeilen = [zeile.strip() for zeile in bisher.splitlines()]
    neueZeilen = [zeile.strip() for zeile in danach.splitlines()]
    alt, neu = zyklusAusText(bisher), zyklusAusText(danach)
    if alt is None or (neu is not None and neu > alt):
        # Warum: Die Datei des nächsten Zyklus beginnt neu, aber nie schon freigegeben.
        return (
            "beginnt mit `Freigabe: ja`; das setzt nur der Stakeholder."
            if (freigabeJa in neueZeilen)
            else None
        )
    vorher, nachher = Counter(geschützteZeilen(bisher)), Counter(geschützteZeilen(danach))
    if nachher - vorher:
        return f"setzt `{next(iter(nachher - vorher))}`; das tut nur der Stakeholder."
    if vorher - nachher:
        fehlt = next(iter(vorher - nachher))
        return f"ändert oder entfernt `{fehlt}`; das tut nur der Stakeholder."
    if freigabeOffen in alteZeilen and freigabeOffen not in neueZeilen:
        return "ändert `Freigabe: offen`; das tut nur der Stakeholder."
    return None
