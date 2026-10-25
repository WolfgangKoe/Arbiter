"""Erzeugt den Tokenbericht `dashboard.html` aus dem Lauf-Log, im Aussehen der `ArbiterMap`."""

import html
import sys
from pathlib import Path

from gemeinsam.pfade import wurzel
from rollenregeln.dashboardArchitektur import architekturKarte, kartenStil
from rollenregeln.dashboardDiagramm import histogramm, kilo, säulendiagramm
from rollenregeln.dashboardGruppen import belegungNachRolle, nachSitzung, sitzungsTitel
from rollenregeln.dashboardHinweise import hinweise, hinweisStil
from rollenregeln.dashboardSeiten import schalterSkriptFür, schalterStil, seitenschalter
from rollenregeln.dashboardStil import legende, stil
from rollenregeln.laufLesen import Lauf, läufeLesen
from standregeln.phasenfolge import lage

dashboardDatei = "dashboard.html"
minute = 60
fehlt = "–"


def dauerText(sekunden: int | None) -> str:
    if sekunden is None:
        return fehlt
    return f"{sekunden} s" if sekunden < minute else f"{round(sekunden / minute)} min"


def modellName(modell: str) -> str:
    teile = modell.split("-")
    return teile[1].capitalize() if teile[0] == "claude" and len(teile) > 1 else modell


def tabelle(läufe: list[Lauf]) -> str:
    zeilen = "".join(
        f'<tr><td class="rolle">{html.escape(lauf.rolle)}</td>'
        f"<td>{html.escape(modellName(lauf.modell or fehlt))}</td>"
        f'<td class="auftrag">{html.escape(lauf.ziel or fehlt)}</td>'
        f'<td class="stand">{dauerText(lauf.dauer)}</td>'
        f'<td class="stand">{kilo(lauf.belegung)}</td></tr>'
        for lauf in läufe
    )
    return (
        '<table class="auftraege"><tr><th>Agent</th><th>Modell</th><th>Auftrag</th>'
        f"<th>Dauer</th><th>Kontextfenster</th></tr>{zeilen}</table>"
    )


def sitzungsKarte(sitzung: str, läufe: list[Lauf]) -> str:
    kopf = f"{len(läufe)} Läufe · Höchststand {kilo(max(lauf.belegung for lauf in läufe))}"
    titel = sitzungsTitel(sitzung, läufe)
    return (
        f'<div class="sitzungs-karte"><h3>{html.escape(titel)}</h3>'
        f'<p class="karten-kopf">{kopf}</p>'
        f'<div class="karten-diagramm">{säulendiagramm(läufe)}</div>{tabelle(läufe)}</div>'
    )


def rollenZeilen(läufe: list[Lauf]) -> str:
    zeilen = "".join(
        f'<tr><td class="rolle">{html.escape(rolle)} ({len(werte)})</td>'
        f'<td class="stand">{kilo(sum(werte) / len(werte))}</td>'
        f'<td class="stand">{kilo(max(werte))}</td></tr>'
        for rolle, werte in sorted(belegungNachRolle(läufe).items())
    )
    return (
        '<table class="auftraege"><tr><th>Rolle</th><th>Mittel</th><th>Höchst</th></tr>'
        f"{zeilen}</table>"
    )


def legendeErzeugen() -> str:
    punktListe = "".join(
        f'<li style="color:{farbe}"><span class="marke{" linie" if linie else ""}" '
        f'style="background:{"none" if linie else farbe}"></span>'
        f'<span style="color:var(--text)">{html.escape(text)}</span></li>'
        for farbe, text, linie in legende
    )
    return f'<section class="kasten legende"><h3>Legende</h3><ul>{punktListe}</ul></section>'


def seiteErzeugen(
    läufe: list[Lauf], lageText: str = "", hinweisText: str = "", kartenText: str = ""
) -> str:
    if läufe:
        sitzungen = list(nachSitzung(läufe).items())
        neuesteZuerst = reversed(sitzungen)
        karten = seitenschalter(len(sitzungen)) + "".join(
            sitzungsKarte(name, gruppe) for name, gruppe in neuesteZuerst
        )
        verteilung = histogramm(läufe) + rollenZeilen(läufe)
    else:
        sitzungen = []
        karten = verteilung = "<p>Noch kein Lauf protokolliert.</p>"
    return (
        '<!doctype html><html lang="de"><head><meta charset="utf-8">'
        "<title>Arbiter · Prozess-Dashboard</title>"
        f"<style>{stil}{schalterStil}{hinweisStil}{kartenStil}</style></head>"
        "<body><h1>Prozess-Dashboard</h1>"
        f'<p class="muted">{html.escape(lageText)}</p>{hinweisText}{kartenText}'
        '<p class="muted">Belegung je Lauf und Sitzung.</p><div class="bericht-zeile">'
        f'<div class="karten-spalte">{karten}</div><aside class="seiten-spalte">'
        f'<section class="kasten"><h3>Verteilung der Tokenstände</h3>{verteilung}</section>'
        f"{legendeErzeugen()}</aside></div>{schalterSkriptFür(len(sitzungen))}</body></html>\n"
    )


def dashboardSchreiben(ordner: Path) -> Path:
    ziel = ordner / dashboardDatei
    seite = seiteErzeugen(
        läufeLesen(ordner), lage(ordner).alsText(), hinweise(ordner), architekturKarte(ordner)
    )
    ziel.write_text(seite, encoding="utf-8")
    return ziel


def hauptlauf(argumente: list[str]) -> int:
    try:
        ziel = dashboardSchreiben(wurzel)
    except Exception:
        if "--still" in argumente:
            return 0
        raise
    if "--still" not in argumente:
        print(ziel)
    return 0


if __name__ == "__main__":
    sys.exit(hauptlauf(sys.argv[1:]))
