"""Fortschrittsliste des Dashboards: Haken per Klick, Kommentarfeld je Zeile hinter einem Klick."""

import html
import re
from pathlib import Path
from urllib.parse import parse_qs

from rollenregeln.eingang import Zug
from standregeln.fortschritt import bisherigeZeilen, zielUndZeilen
from standregeln.phasenfolge import lage
from standregeln.zeilenZug import abgehaktWert, hakenArt, kommentarArt

fortschrittPfad = "/fortschritt"
anliegenNummer = re.compile(r"Anliegen (\d+)")
keinAbschnitt = "<p>In dieser Phase gibt es keinen Fortschritt.</p>"

fortschrittStil = """
.startseite{display:grid;grid-template-columns:minmax(0,3fr) minmax(260px,1fr);gap:16px;
align-items:start}
@media (max-width:800px){.startseite{grid-template-columns:1fr}}
ul.fortschritt{list-style:none;margin:0;padding:0;font-size:.82rem}
ul.fortschritt li{padding:2px 0;border-bottom:1px solid var(--border)}
ul.fortschritt form{display:flex;flex-wrap:wrap;gap:6px;align-items:flex-start}
ul.fortschritt details{flex:1 1 0;min-width:0}
ul.fortschritt input[type=checkbox]{accent-color:var(--accent-text);opacity:1}
ul.fortschritt summary{cursor:pointer}
ul.fortschritt details input[type=text]{width:100%;box-sizing:border-box}
ul.fortschritt .vermerk{flex-basis:100%;margin-left:22px;color:var(--text-muted)}
"""


def vermerkHtml(zeile: str) -> str:
    """Der Vermerk unter einer Zeile; die Nummer eines Anliegens ist ein Link auf seine Seite."""
    maskiert = html.escape(zeile.strip())
    verlinkt = anliegenNummer.sub(r'<a href="/anliegen/\1">Anliegen \1</a>', maskiert)
    return f'<div class="vermerk">{verlinkt}</div>'


def zeileHtml(schlüssel: str, *, abgehakt: bool, zusatz: list[str], vonFakt: bool) -> str:
    schlüsselText = html.escape(schlüssel, quote=True)
    gesperrt = " disabled" if vonFakt or abgehakt else ""
    markiert = " checked" if abgehakt else ""
    vermerke = "".join(vermerkHtml(zeile) for zeile in zusatz)
    return (
        f'<li><form method="post" action="{fortschrittPfad}">'
        f'<input type="hidden" name="zeile" value="{schlüsselText}">'
        f'<input type="checkbox" name="haken" value="{abgehaktWert}"{markiert}{gesperrt} '
        'onchange="this.form.submit()">'
        f"<details><summary>{html.escape(schlüssel)}</summary>"
        '<input type="text" name="kommentar" placeholder="Kommentar">'
        f'<button type="submit">Kommentieren</button></details>{vermerke}</form></li>'
    )


def fortschrittListe(ordner: Path) -> str:
    """Der Fortschritt der laufenden Phase als kompakte Liste, eine Zeile je Schritt."""
    ziel = zielUndZeilen(ordner, lage(ordner))
    if ziel is None:
        return keinAbschnitt
    datei, zeilen = ziel
    bisher = bisherigeZeilen(datei.read_text(encoding="utf-8"))
    punkte = ""
    for zeile in zeilen:
        abgehakt, zusatz = bisher.get(zeile.schlüssel, (False, []))
        punkte += zeileHtml(
            zeile.schlüssel, abgehakt=abgehakt, zusatz=zusatz, vonFakt=zeile.fakt is True
        )
    return f'<ul class="fortschritt">{punkte}</ul>' if punkte else keinAbschnitt


def zügeAusFortschrittFormular(körper: bytes) -> list[Zug]:
    """Haken (nur setzen, nie entfernen) und Kommentar der Zeile; ein leeres Feld entfällt."""
    felder = parse_qs(körper.decode("utf-8"), keep_blank_values=True)
    schlüssel = (felder.get("zeile") or [""])[0]
    if not schlüssel:
        return []
    züge = []
    if abgehaktWert in felder.get("haken", []):
        züge.append(Zug(0, hakenArt, abgehaktWert, zeile=schlüssel))
    kommentar = (felder.get("kommentar") or [""])[0].strip()
    if kommentar:
        züge.append(Zug(0, kommentarArt, kommentar, zeile=schlüssel))
    return züge
