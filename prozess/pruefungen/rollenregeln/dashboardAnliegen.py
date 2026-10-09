"""Sicht auf die Anliegen im Dashboard: Spalte je Zuständigem, Karten, Filter im Browser."""

import html
from pathlib import Path

from anliegenregeln.anliegenDran import dran, nachprüfungen
from lesen.anliegenKopf import Anliegen, gelesene

filterStil = """
.anliegen-filter{display:flex;gap:12px;flex-wrap:wrap;margin:6px 0 10px}
.anliegen-filter select{background:var(--panel-2);color:var(--text);border:1px solid var(--border);
border-radius:5px;padding:4px 8px;font-family:inherit}
.anliegen-spalten{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-start}
.anliegen-spalte{flex:1 1 200px;min-width:200px}
.anliegen-spalte h3{color:var(--accent-text)}
.anliegen-karte{background:var(--panel-2);border:1px solid var(--border);border-radius:6px;
padding:6px 8px;margin-bottom:8px;font-size:.82rem}
.anliegen-karte a{color:var(--accent-text);font-weight:600}
.anliegen-karte p{margin:2px 0 0;color:var(--text-muted)}
"""

filterSkript = """
(function () {
  var auswahl = document.querySelectorAll(".anliegen-filter select");
  var karten = document.querySelectorAll(".anliegen-karte");
  function filtern() {
    var rolle = document.getElementById("filterRolle").value;
    var form = document.getElementById("filterForm").value;
    karten.forEach(function (karte) {
      karte.hidden = (rolle !== "" && karte.dataset.rolle !== rolle) ||
        (form !== "" && karte.dataset.form !== form);
    });
  }
  auswahl.forEach(function (element) { element.addEventListener("change", filtern); });
})();
"""


def titelLesen(datei: Path) -> str:
    erste = datei.read_text(encoding="utf-8").splitlines()[0]
    return erste.removeprefix("# ")


def zuständige(ordner: Path) -> dict[str, list[int]]:
    """Je Rolle die Nummern, bei denen sie dran ist, samt ihren Nachprüfungen."""
    spalten = {rolle: list(nummern) for rolle, nummern in dran(ordner).items()}
    for rolle, nummern in nachprüfungen(ordner).items():
        spalten.setdefault(rolle, []).extend(nummern)
    return spalten


def anliegenKarte(anliegen: Anliegen, rolle: str, ordner: Path) -> str:
    pfad = anliegen.datei.relative_to(ordner).as_posix()
    return (
        f'<div class="anliegen-karte" data-rolle="{html.escape(rolle)}" '
        f'data-form="{html.escape(anliegen.typ)}">'
        f'<a href="{html.escape(pfad)}">{anliegen.nummer}</a> '
        f"{html.escape(titelLesen(anliegen.datei))}"
        f"<p>{html.escape(anliegen.typ)} · Runde {anliegen.runde}</p></div>"
    )


def optionen(werte: list[str]) -> str:
    return '<option value="">alle</option>' + "".join(
        f'<option value="{html.escape(wert)}">{html.escape(wert)}</option>' for wert in werte
    )


def anliegenAbschnitt(ordner: Path) -> str:
    nachNummer = {anliegen.nummer: anliegen for anliegen in gelesene(ordner)}
    spalten = zuständige(ordner)
    if not spalten:
        return '<section class="kasten"><h3>Anliegen</h3><p>Kein Anliegen offen.</p></section>'
    formen = sorted({nachNummer[nummer].typ for nummern in spalten.values() for nummer in nummern})
    spaltenHtml = "".join(
        f'<div class="anliegen-spalte"><h3>{html.escape(rolle)} ({len(nummern)})</h3>'
        + "".join(anliegenKarte(nachNummer[nummer], rolle, ordner) for nummer in sorted(nummern))
        + "</div>"
        for rolle, nummern in sorted(spalten.items())
    )
    filterHtml = (
        '<div class="anliegen-filter"><label>Rolle <select id="filterRolle">'
        f'{optionen(sorted(spalten))}</select></label><label>Form <select id="filterForm">'
        f"{optionen(formen)}</select></label></div>"
    )
    return (
        f'<section class="kasten"><h3>Anliegen</h3>{filterHtml}'
        f'<div class="anliegen-spalten">{spaltenHtml}</div></section>'
        f"<script>{filterSkript}</script>"
    )
