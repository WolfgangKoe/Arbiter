"""Seiten des Dashboard-Servers: Anliegen, ein Anliegen mit Formular, Reiter, Neuladen."""

import hashlib
import html
import re
from pathlib import Path

from anliegenregeln.anliegenDran import dran, nachprüfungen
from gemeinsam.pfade import handoffOrdner
from lesen.anliegenKopf import Anliegen, Status, gelesene, stakeholder
from rollenregeln.dashboardAnliegen import anliegenAbschnitt, filterStil, titelLesen
from rollenregeln.dashboardStil import stil
from rollenregeln.eingang import eingangDatei, verworfenDatei, verworfene, vorgemerkte
from rollenregeln.zuegeUebernehmen import dateiZu, fragtStakeholder, zulässigeStatus

frageKopf = re.compile(r"^\*\*(F\d+) ·", re.MULTILINE)
neuladenIntervall = 3000

seitenStil = """
.reiter{display:flex;gap:6px;margin:8px 0 14px}
.reiter a{color:var(--text);background:var(--panel-2);border:1px solid var(--border);
border-radius:5px;padding:5px 12px;text-decoration:none}
.reiter a[aria-current="page"]{background:var(--accent-text);color:var(--bg);font-weight:700}
.zaehler{font-size:1.05rem;color:var(--accent-text);margin:4px 0 10px}
.vorgemerkt{border-left:3px solid var(--c-peak);padding-left:8px;margin:4px 0}
.verworfen{border-left:3px solid var(--c-warnung);padding-left:8px;margin:4px 0}
pre.anliegen-text{white-space:pre-wrap;background:var(--panel);border:1px solid var(--border);
border-radius:8px;padding:10px 12px;font-size:.84rem}
form.zug label{display:block;margin:8px 0 2px}
form.zug input[type=text],form.zug textarea,form.zug select{width:100%;background:var(--panel-2);
color:var(--text);border:1px solid var(--border);border-radius:5px;padding:5px 8px;
font-family:inherit}
form.zug button,.knopf{background:var(--accent-text);color:var(--bg);border:0;border-radius:5px;
padding:6px 14px;font-weight:700;cursor:pointer;margin-top:10px}
"""

neuladenSkript = """
(function () {
  var stand = null;
  var geaendert = false;
  document.addEventListener("input", function () { geaendert = true; });
  function pruefen() {
    fetch("/stand").then(function (antwort) { return antwort.text(); }).then(function (neu) {
      if (stand !== null && neu !== stand && !geaendert) location.reload();
      if (stand === null) stand = neu;
    }).catch(function () {});
  }
  setInterval(pruefen, __INTERVALL__);
  pruefen();
})();
""".replace("__INTERVALL__", str(neuladenIntervall))

reiter = (("Anliegen", "/"), ("Fortschritt", "/fortschritt"), ("Tokenbericht", "/tokens"))


def navigation(aktiv: str) -> str:
    aktuell = ' aria-current="page"'
    verweise = "".join(
        f'<a href="{adresse}"{aktuell if name == aktiv else ""}>{name}</a>'
        for name, adresse in reiter
    )
    return f'<nav class="reiter">{verweise}</nav>'


def seite(titel: str, aktiv: str, inhalt: str) -> str:
    return (
        '<!doctype html><html lang="de"><head><meta charset="utf-8">'
        f"<title>Arbiter · {html.escape(titel)}</title>"
        f"<style>{stil}{filterStil}{seitenStil}</style></head><body>"
        f"<h1>{html.escape(titel)}</h1>{navigation(aktiv)}{inhalt}"
        f"<script>{neuladenSkript}</script></body></html>\n"
    )


def stand(ordner: Path) -> str:
    """Ein Fingerabdruck von `handoff/` und den Zügen; ändert er sich, lädt die Seite neu."""
    dateien = sorted((ordner / handoffOrdner).rglob("*"))
    dateien += [ordner / eingangDatei, ordner / verworfenDatei]
    summe = hashlib.sha1(usedforsecurity=False)
    for datei in dateien:
        if datei.is_file():
            angaben = datei.stat()
            summe.update(f"{datei}{angaben.st_mtime_ns}{angaben.st_size}".encode())
    return summe.hexdigest()


def zähler(ordner: Path) -> int:
    offen = len(dran(ordner).get(stakeholder, []))
    return offen + len(nachprüfungen(ordner).get(stakeholder, []))


def vermerke(ordner: Path) -> str:
    gemerkt = "".join(
        f'<div class="vorgemerkt">vorgemerkt · {html.escape(zug.beschreibung())}</div>'
        for zug in vorgemerkte(ordner)
    )
    abgelehnt = "".join(
        f'<div class="verworfen">nicht übernommen · {html.escape(eintrag.zug.beschreibung())}: '
        f"{html.escape(eintrag.grund)}</div>"
        for eintrag in verworfene(ordner)
    )
    gelesen = (
        '<form method="post" action="/verworfeneLeeren">'
        '<button class="knopf">Gelesen</button></form>'
        if abgelehnt
        else ""
    )
    return gemerkt + abgelehnt + gelesen


def seitenVerweis(anliegen: Anliegen, ordner: Path) -> str:  # noqa: ARG001
    return f"/anliegen/{anliegen.nummer}"


def kommentarFeld(anliegen: Anliegen) -> str:
    return (
        f'<form class="zug" method="post" action="/anliegen/{anliegen.nummer}">'
        '<textarea name="kommentar" rows="2" placeholder="Kommentar"></textarea>'
        '<button type="submit">Kommentieren</button></form>'
    )


def anliegenSeite(ordner: Path) -> str:
    inhalt = (
        f'<p class="zaehler">Du bist dran: {zähler(ordner)}</p>{vermerke(ordner)}'
        f"{anliegenAbschnitt(ordner, seitenVerweis, kommentarFeld)}"
    )
    return seite("Anliegen", "Anliegen", inhalt)


def anliegenNach(ordner: Path, nummer: int) -> Anliegen | None:
    return next((anliegen for anliegen in gelesene(ordner) if anliegen.nummer == nummer), None)


def formular(anliegen: Anliegen, text: str) -> str:
    felder = []
    status = sorted(zulässigeStatus(anliegen))
    if status:
        optionen = '<option value="">keine Änderung</option>' + "".join(
            f'<option value="{html.escape(wert)}">{html.escape(wert)}</option>' for wert in status
        )
        felder.append(f'<label>Status<select name="status">{optionen}</select></label>')
    if anliegen.status == Status.eskaliert and anliegen.runde > 1:
        felder.append(
            '<label><input type="checkbox" name="runde" value="senken"> Runde senken</label>'
        )
    if fragtStakeholder(anliegen):
        felder += [
            f'<label>Antwort auf {frage}<input type="text" name="antwort_{frage}"></label>'
            for frage in frageKopf.findall(text)
        ]
    felder.append('<label>Kommentar<textarea name="kommentar" rows="3"></textarea></label>')
    return (
        f'<form class="zug" method="post" action="/anliegen/{anliegen.nummer}">'
        f'{"".join(felder)}<button type="submit">Abschicken</button></form>'
    )


def einzelSeite(ordner: Path, nummer: int) -> str | None:
    anliegen = anliegenNach(ordner, nummer)
    datei = dateiZu(ordner, nummer)
    if anliegen is None or datei is None:
        return None
    text = datei.read_text(encoding="utf-8")
    inhalt = (
        '<p><a href="/">‹ Dashboard</a></p>'
        f"{vermerke(ordner)}{formular(anliegen, text)}"
        f'<pre class="anliegen-text">{html.escape(text)}</pre>'
    )
    return seite(f"{nummer} · {titelLesen(datei)}", "Anliegen", inhalt)
