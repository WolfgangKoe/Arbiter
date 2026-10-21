"""Seite Fortschritt des Dashboards: Haken und Kommentarfeld je Zeile der laufenden Phase."""

import html
from pathlib import Path
from urllib.parse import parse_qs

from rollenregeln.dashboardAnliegenSeiten import seite
from rollenregeln.eingang import Zug
from standregeln.fortschritt import bisherigeZeilen, zielUndZeilen
from standregeln.phasenfolge import lage
from standregeln.zeilenZug import abgehaktWert, hakenArt, kommentarArt

fortschrittPfad = "/fortschritt"
keinAbschnitt = "<p>In dieser Phase gibt es keinen Fortschritt.</p>"


def zeileHtml(schlüssel: str, *, abgehakt: bool, zusatz: list[str], vonFakt: bool) -> str:
    schlüsselText = html.escape(schlüssel, quote=True)
    gesperrt = " disabled" if vonFakt else ""
    markiert = " checked" if abgehakt else ""
    vermerke = "".join(f"<p>{html.escape(zeile.strip())}</p>" for zeile in zusatz)
    return (
        f'<form class="zug" method="post" action="{fortschrittPfad}">'
        f'<input type="hidden" name="zeile" value="{schlüsselText}">'
        '<input type="hidden" name="haken" value="">'
        f'<label><input type="checkbox" name="haken" value="{abgehaktWert}"{markiert}{gesperrt}>'
        f" {html.escape(schlüssel)}</label>{vermerke}"
        '<input type="text" name="kommentar" placeholder="Kommentar">'
        '<button type="submit">Abschicken</button></form>'
    )


def fortschrittSeite(ordner: Path) -> str:
    ziel = zielUndZeilen(ordner, lage(ordner))
    if ziel is None:
        return seite("Fortschritt", "Fortschritt", keinAbschnitt)
    datei, zeilen = ziel
    bisher = bisherigeZeilen(datei.read_text(encoding="utf-8"))
    inhalt = ""
    for zeile in zeilen:
        abgehakt, zusatz = bisher.get(zeile.schlüssel, (False, []))
        inhalt += zeileHtml(
            zeile.schlüssel, abgehakt=abgehakt, zusatz=zusatz, vonFakt=zeile.fakt is True
        )
    return seite("Fortschritt", "Fortschritt", inhalt or keinAbschnitt)


def zügeAusFortschrittFormular(körper: bytes) -> list[Zug]:
    """Haken (der letzte Wert gilt) und Kommentar der Zeile; ein leeres Feld entfällt."""
    felder = parse_qs(körper.decode("utf-8"), keep_blank_values=True)
    schlüssel = (felder.get("zeile") or [""])[0]
    if not schlüssel:
        return []
    züge = []
    haken = felder.get("haken")
    if haken:
        züge.append(Zug(0, hakenArt, haken[-1], zeile=schlüssel))
    kommentar = (felder.get("kommentar") or [""])[0].strip()
    if kommentar:
        züge.append(Zug(0, kommentarArt, kommentar, zeile=schlüssel))
    return züge
