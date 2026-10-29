import html
from collections.abc import Callable
from operator import attrgetter
from pathlib import Path

from anliegenregeln.anliegenDran import dran, nachprüfungen, wartende, wartetAuf
from lesen.anliegenKopf import Anliegen, gelesene, stakeholder
from standregeln.phasenfolge import Phase, lage

Verweis = Callable[[Anliegen, Path], str]

filterStil = """
.anliegen-filter{display:flex;gap:12px;flex-wrap:wrap;margin:6px 0 10px}
.anliegen-filter select{background:var(--panel-2);color:var(--text);border:1px solid var(--border);
border-radius:5px;padding:4px 8px;font-family:inherit}
.anliegen-spalten{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-start}
.anliegen-spalte{flex:1 1 200px;min-width:200px}
.anliegen-spalte h3,.anliegen-bereich h3{color:var(--accent-text)}
.anliegen-bereich{margin-top:12px}
.anliegen-karte{background:var(--panel-2);border:1px solid var(--border);border-radius:6px;
padding:6px 8px;margin-bottom:8px;font-size:.82rem}
.anliegen-karte.an-stakeholder{border-left:3px solid var(--c-peak)}
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
    spalten = {rolle: list(nummern) for rolle, nummern in dran(ordner).items()}
    for rolle, nummern in nachprüfungen(ordner).items():
        spalten.setdefault(rolle, []).extend(nummern)
    return spalten


def dateiVerweis(anliegen: Anliegen, ordner: Path) -> str:
    return anliegen.datei.relative_to(ordner).as_posix()


def vorgemerkte(ordner: Path) -> list[tuple[str, list[Anliegen]]]:
    nachNummer = {anliegen.nummer: anliegen for anliegen in gelesene(ordner)}
    aufAnliegen: list[Anliegen] = []
    aufPhase: dict[str, list[Anliegen]] = {}
    for nummer, ziel in wartende(ordner).items():
        if ziel.phase is None:
            aufAnliegen.append(nachNummer[nummer])
        else:
            aufPhase.setdefault(ziel.phase, []).append(nachNummer[nummer])
    bereiche = [("Wartet auf ein anderes Anliegen", aufAnliegen)] if aufAnliegen else []
    if aufPhase:
        bereiche += vorgemerktJePhase(ordner, aufPhase)
    return bereiche


def vorgemerktJePhase(
    ordner: Path, auf: dict[str, list[Anliegen]]
) -> list[tuple[str, list[Anliegen]]]:
    phasen = list(Phase)
    nächste = phasen.index(lage(ordner).phase) + 1
    versetzt = phasen[nächste:] + phasen[:nächste]
    folge = [str(phase) for phase in versetzt]
    return [(f"Vorgemerkt für die {ziel}", auf[ziel]) for ziel in folge if ziel in auf]


def wartetAufText(anliegen: Anliegen) -> str:
    if anliegen.wartetAuf is None:
        return ""
    return f" · wartet auf {anliegen.wartetAuf.beschreibung}"


def anliegenKarte(anliegen: Anliegen, rolle: str, ordner: Path, verweis: Verweis) -> str:
    pfad = verweis(anliegen, ordner)
    anDich = anliegen.empfänger == stakeholder
    klasse = "anliegen-karte an-stakeholder" if anDich else "anliegen-karte"
    richtung = f"{anliegen.absender} → {anliegen.empfänger}" + (" (an dich)" if anDich else "")
    return (
        f'<div class="{klasse}" data-rolle="{html.escape(rolle)}" '
        f'data-form="{html.escape(anliegen.typ)}">'
        f'<a href="{html.escape(pfad)}">{anliegen.nummer}</a> '
        f"{html.escape(titelLesen(anliegen.datei))}"
        f"<p>{html.escape(anliegen.typ)} · Runde {anliegen.runde} · "
        f"{html.escape(richtung)}{html.escape(wartetAufText(anliegen))}</p></div>"
    )


def optionen(werte: list[str]) -> str:
    return '<option value="">alle</option>' + "".join(
        f'<option value="{html.escape(wert)}">{html.escape(wert)}</option>' for wert in werte
    )


def wartendeHtml(ordner: Path, bereiche: list[tuple[str, list[Anliegen]]], verweis: Verweis) -> str:
    return "".join(
        f'<div class="anliegen-bereich"><h3>{html.escape(titel)} ({len(anliegen)})</h3>'
        + "".join(
            anliegenKarte(eines, wartetAuf(ordner, eines, None) or stakeholder, ordner, verweis)
            for eines in sorted(anliegen, key=attrgetter("nummer"))
        )
        + "</div>"
        for titel, anliegen in bereiche
    )


def anliegenAbschnitt(ordner: Path, verweis: Verweis = dateiVerweis) -> str:
    nachNummer = {anliegen.nummer: anliegen for anliegen in gelesene(ordner)}
    spalten = zuständige(ordner)
    bereiche = vorgemerkte(ordner)
    if not spalten and not bereiche:
        return '<section class="kasten"><h3>Anliegen</h3><p>Kein Anliegen offen.</p></section>'
    gezeigt = [nachNummer[nummer] for nummern in spalten.values() for nummer in nummern]
    gezeigt += [anliegen for _, liste in bereiche for anliegen in liste]
    rollen = set(spalten) | {wartetAuf(ordner, eines, None) or stakeholder for eines in gezeigt}
    spaltenHtml = "".join(
        f'<div class="anliegen-spalte"><h3>{html.escape(rolle)} ({len(nummern)})</h3>'
        + "".join(
            anliegenKarte(nachNummer[nummer], rolle, ordner, verweis) for nummer in sorted(nummern)
        )
        + "</div>"
        for rolle, nummern in sorted(spalten.items())
    )
    filterHtml = (
        '<div class="anliegen-filter"><label>Rolle <select id="filterRolle">'
        f'{optionen(sorted(rollen))}</select></label><label>Form <select id="filterForm">'
        f"{optionen(sorted({anliegen.typ for anliegen in gezeigt}))}</select></label></div>"
    )
    jetzt = ""
    if spalten:
        jetzt = f'<h3>Jetzt dran</h3><div class="anliegen-spalten">{spaltenHtml}</div>'
    return (
        f'<section class="kasten"><h3>Anliegen</h3>{filterHtml}{jetzt}'
        f"{wartendeHtml(ordner, bereiche, verweis)}</section>"
        f"<script>{filterSkript}</script>"
    )
