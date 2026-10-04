"""Erzeugt `dashboard.html` aus dem Lauf-Log, im Aussehen der Vorlage in `ArbiterMap`."""

import html
import statistics
import sys
from pathlib import Path

from belegung import sperrschwelle, warnschwelle
from laufLog import läufeLesen
from pfade import wurzel

dashboardDatei = "dashboard.html"
sichtbareSitzungen = 5
klassenbreite = 25_000
säulenbreite = 30
säulenabstand = 14
diagrammhöhe = 200
randLinks = 44
randOben = 20
randUnten = 70
achsenschritt = 50_000
minute = 60
achsenhöhe = 1.1 * sperrschwelle
ohneSitzung = "ohne Sitzung"
fehlt = "–"  # Warum: Wert fehlt im Eintrag
legende = (
    ("var(--c-orchestrator)", "Gold: Koordinator", False),
    ("var(--c-subagent)", "Grau: Rolle", False),
    ("var(--c-warnung)", "Rot: ab Warnschwelle", False),
    ("var(--c-winddown)", "Gestrichelt: Warnschwelle", True),
    ("var(--c-korridor)", "Gestrichelt: Sperrschwelle", True),
    ("var(--c-peak)", "Gestrichelt: Median", True),
)

stil = """
:root{--bg:#0f0e0c;--panel:#1c1a14;--panel-2:#23201a;--text:#e6dcc4;--text-muted:#a89a72;
--border:#3a3526;--accent-text:#c9a869;--c-subagent:#7c8ba1;--c-orchestrator:#c9a869;--c-warnung:#f43f5e;
--c-peak:#fbbf24;--c-winddown:#d946ef;--c-korridor:#f97316}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--text);
font-family:"Segoe UI",system-ui,Roboto,Arial,sans-serif;
margin:0;padding:20px 28px 56px;line-height:1.5}
h1{color:var(--accent-text);font-size:1.5rem;margin:0 0 4px}
h3{color:var(--text);font-size:.98rem;margin:0 0 8px}
.muted{color:var(--text-muted);font-size:.86rem}
.bericht-zeile{display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap}
.karten-spalte{flex:3 1 620px;min-width:320px}
.seiten-spalte{flex:1 1 280px;min-width:260px}
.kasten,.sitzungs-karte{background:var(--panel);border:1px solid var(--border);
border-radius:10px;padding:12px 14px;margin-bottom:14px;font-size:.84rem}
.sitzungs-karte>h3{color:var(--accent-text);margin:0 0 2px;font-size:1rem}
.karten-kopf{color:var(--text-muted);font-size:.8rem;margin:0 0 8px}
.karten-diagramm{overflow-x:auto}
svg{display:block;max-width:100%;height:auto;background:var(--panel-2);border-radius:6px}
.gitter{stroke:var(--border);stroke-width:1}
.achse-text{fill:var(--text-muted);font-size:10px}
.schwelle-winddown{stroke:var(--c-winddown);stroke-width:1.5;stroke-dasharray:5 4}
.schwelle-korridor{stroke:var(--c-korridor);stroke-width:1.5;stroke-dasharray:5 4}
.schwelle-text{font-size:9px}
.schwelle-text.winddown{fill:var(--c-winddown)}.schwelle-text.korridor{fill:var(--c-korridor)}
.saeule{fill:var(--c-subagent)}.saeule.warnung{fill:var(--c-warnung)}.saeule.orchestrator{fill:var(--c-orchestrator)}
.vert-median{stroke:var(--c-peak);stroke-width:1.5;stroke-dasharray:4 3}
.wert-text{fill:var(--text);font-size:9px;font-weight:600}
.rollen-text{fill:var(--text-muted);font-size:8.5px}
table.auftraege{border-collapse:collapse;width:100%;font-size:.82rem;margin-top:10px}
table.auftraege th,table.auftraege td{border:1px solid var(--border);
padding:4px 8px;text-align:left}
table.auftraege th{background:var(--panel-2);color:var(--accent-text);font-weight:600}
table.auftraege td.rolle{color:var(--c-subagent)}
table.auftraege td.stand{text-align:right;font-variant-numeric:tabular-nums}
.legende ul{list-style:none;margin:0;padding:0}
.legende li{display:flex;gap:8px;margin-bottom:9px}
.legende .marke{flex:0 0 18px;height:12px;margin-top:3px;border-radius:2px}
.legende .marke.linie{height:0;border-top:2px dashed;margin-top:8px}
"""


def kilo(zahl: float) -> str:
    return f"{round(zahl / 1000)}k"


def dauerText(sekunden: int | None) -> str:
    if sekunden is None:
        return fehlt
    return f"{sekunden} s" if sekunden < minute else f"{round(sekunden / minute)} min"


def modellName(modell: str) -> str:
    teile = modell.split("-")
    return teile[1].capitalize() if teile[0] == "claude" and len(teile) > 1 else modell


def stufe(belegung: float) -> str:
    return "warnung" if belegung >= warnschwelle else ""


def höhe(belegung: float) -> float:
    return diagrammhöhe * min(belegung, achsenhöhe) / achsenhöhe


def linieMitText(wert: int, klasse: str, text: str, breite: float) -> str:
    höhenlage = randOben + diagrammhöhe - höhe(wert)
    return (
        f'<line class="schwelle-{klasse}" x1="{randLinks}" x2="{breite}" '
        f'y1="{höhenlage}" y2="{höhenlage}"/>'
        f'<text class="schwelle-text {klasse}" '
        f'x="{randLinks + 4}" y="{höhenlage - 3}">{text}</text>'
    )


def achsenmarke(wert: int) -> str:
    lage = randOben + diagrammhöhe - höhe(wert)
    return (
        f'<line class="gitter" x1="{randLinks - 4}" x2="{randLinks}" y1="{lage}" y2="{lage}"/>'
        f'<text class="achse-text" text-anchor="end" x="{randLinks - 6}" '
        f'y="{lage + 3}">{kilo(wert)}</text>'
    )


def achse() -> str:
    linie = (
        f'<line class="gitter" x1="{randLinks}" x2="{randLinks}" '
        f'y1="{randOben}" y2="{randOben + diagrammhöhe}"/>'
    )
    return linie + "".join(achsenmarke(wert) for wert in range(0, int(achsenhöhe), achsenschritt))


def säule(nummer: int, beschriftung: str, belegung: int, klasse: str) -> str:
    links = randLinks + säulenabstand + nummer * (säulenbreite + säulenabstand)
    oben = randOben + diagrammhöhe - höhe(belegung)
    mitte = links + säulenbreite / 2
    unten = randOben + diagrammhöhe + 10
    return (
        f'<rect class="saeule {klasse}" x="{links}" y="{oben:.1f}" '
        f'width="{säulenbreite}" height="{höhe(belegung):.1f}"/>'
        f'<text class="wert-text" text-anchor="middle" x="{mitte}" y="{oben - 3:.1f}">'
        f"{kilo(belegung)}</text>"
        f'<text class="rollen-text" text-anchor="end" x="{mitte}" y="{unten}" '
        f'transform="rotate(-40 {mitte} {unten})">{html.escape(beschriftung)}</text>'
    )


def säulenListe(läufe: list[dict]) -> list[tuple[str, int, str]]:
    stände = [lauf["koordinator"] for lauf in läufe if lauf.get("koordinator")]
    liste = [("Koordinator", stände[-1], "orchestrator")] if stände else []
    return liste + [(lauf["rolle"], lauf["belegung"], stufe(lauf["belegung"])) for lauf in läufe]


def säulendiagramm(läufe: list[dict]) -> str:
    säulen = säulenListe(läufe)
    breite = randLinks + säulenabstand + len(säulen) * (säulenbreite + säulenabstand)
    gesamt = randOben + diagrammhöhe + randUnten
    inhalt = "".join(säule(nummer, *angaben) for nummer, angaben in enumerate(säulen))
    inhalt += linieMitText(warnschwelle, "winddown", f"Warnschwelle {kilo(warnschwelle)}", breite)
    inhalt += linieMitText(
        sperrschwelle, "korridor", f"Sperrschwelle {kilo(sperrschwelle)}", breite
    )
    return (
        f'<svg viewBox="0 0 {breite} {gesamt}" width="{breite}" height="{gesamt}">'
        f'<line class="gitter" x1="{randLinks}" x2="{breite}" y1="{randOben + diagrammhöhe}" '
        f'y2="{randOben + diagrammhöhe}"/>{achse()}{inhalt}</svg>'
    )


def tabelle(läufe: list[dict]) -> str:
    zeilen = "".join(
        f'<tr><td class="rolle">{html.escape(lauf["rolle"])}</td>'
        f"<td>{html.escape(modellName(lauf.get('modell') or fehlt))}</td>"
        f"<td>{html.escape(lauf.get('ziel') or fehlt)}</td>"
        f'<td class="stand">{dauerText(lauf.get("dauer"))}</td>'
        f'<td class="stand">{kilo(lauf["belegung"])}</td></tr>'
        for lauf in läufe
    )
    return (
        '<table class="auftraege"><tr><th>Agent</th><th>Modell</th><th>Auftrag</th>'
        f"<th>Dauer</th><th>Kontextfenster</th></tr>{zeilen}</table>"
    )


def nachSitzung(läufe: list[dict]) -> dict[str, list[dict]]:
    gruppen: dict[str, list[dict]] = {}
    for lauf in läufe:
        kennung = lauf.get("sitzung")
        gruppen.setdefault(kennung[:8] if kennung else ohneSitzung, []).append(lauf)
    return gruppen


def sitzungsTitel(sitzung: str, läufe: list[dict]) -> str:
    """„Zyklus 3 Prozessphase“; wechselt die Sitzung die Phase, „Zyklus 3 Domänenphase bis …“."""
    if sitzung == ohneSitzung:
        return f"Altbestand, {ohneSitzung}"
    benannt = [(lauf["zyklus"], lauf["phase"]) for lauf in läufe if lauf.get("zyklus")]
    if not benannt:
        return f"Sitzung {sitzung} (vor Zyklus und Phase im Log)"
    (zyklusVon, phaseVon), (zyklusBis, phaseBis) = benannt[0], benannt[-1]
    if (zyklusVon, phaseVon) == (zyklusBis, phaseBis):
        name = f"Zyklus {zyklusVon} {phaseVon}"
    elif zyklusVon == zyklusBis:
        name = f"Zyklus {zyklusVon} {phaseVon} bis {phaseBis}"
    else:
        name = f"Zyklus {zyklusVon} {phaseVon} bis Zyklus {zyklusBis} {phaseBis}"
    return f"{name} · Sitzung {sitzung}"


def sitzungsKarte(sitzung: str, läufe: list[dict]) -> str:
    kopf = f"{len(läufe)} Läufe · Höchststand {kilo(max(lauf['belegung'] for lauf in läufe))}"
    titel = sitzungsTitel(sitzung, läufe)
    return (
        f'<div class="sitzungs-karte"><h3>{html.escape(titel)}</h3>'
        f'<p class="karten-kopf">{kopf}</p>'
        f'<div class="karten-diagramm">{säulendiagramm(läufe)}</div>{tabelle(läufe)}</div>'
    )


def rollenZeilen(läufe: list[dict]) -> str:
    nachRolle: dict[str, list[int]] = {}
    for lauf in läufe:
        nachRolle.setdefault(lauf["rolle"], []).append(lauf["belegung"])
    zeilen = "".join(
        f'<tr><td class="rolle">{html.escape(rolle)} ({len(werte)})</td>'
        f'<td class="stand">{kilo(sum(werte) / len(werte))}</td>'
        f'<td class="stand">{kilo(max(werte))}</td></tr>'
        for rolle, werte in sorted(nachRolle.items())
    )
    return (
        '<table class="auftraege"><tr><th>Rolle</th><th>Mittel</th><th>Höchst</th></tr>'
        f"{zeilen}</table>"
    )


def histogramm(läufe: list[dict]) -> str:
    werte = [lauf["belegung"] for lauf in läufe]
    klassen = int(achsenhöhe // klassenbreite) + 1
    anzahl = [0] * klassen
    for wert in werte:
        anzahl[min(wert // klassenbreite, klassen - 1)] += 1
    breite, höchste, spalte = 260, max(anzahl), 260 / klassen
    säulen = "".join(
        f'<rect class="saeule" x="{nummer * spalte + 2:.1f}" y="{100 - 90 * wert / höchste:.1f}" '
        f'width="{spalte - 4:.1f}" height="{90 * wert / höchste:.1f}"/>'
        f'<text class="achse-text" text-anchor="middle" '
        f'x="{nummer * spalte + spalte / 2:.1f}" y="112">'
        f"{nummer * klassenbreite // 1000}k</text>"
        for nummer, wert in enumerate(anzahl)
    )
    median = statistics.median(werte)
    mitteMedian = min(median, achsenhöhe) / klassenbreite * spalte
    return (
        f'<svg viewBox="0 0 {breite} 120" width="{breite}" height="120">{säulen}'
        f'<line class="vert-median" x1="{mitteMedian:.1f}" x2="{mitteMedian:.1f}" y1="0" y2="100"/>'
        f'</svg><p class="muted">Median {kilo(median)}, '
        f"je Klasse {klassenbreite // 1000}k</p>"
    )


def legendeErzeugen() -> str:
    punktListe = "".join(
        f'<li style="color:{farbe}"><span class="marke{" linie" if linie else ""}" '
        f'style="background:{"none" if linie else farbe}"></span>'
        f'<span style="color:var(--text)">{html.escape(text)}</span></li>'
        for farbe, text, linie in legende
    )
    return f'<section class="kasten legende"><h3>Legende</h3><ul>{punktListe}</ul></section>'


def seiteErzeugen(läufe: list[dict]) -> str:
    if läufe:
        sitzungen = list(nachSitzung(läufe).items())[-sichtbareSitzungen:]
        karten = "".join(sitzungsKarte(name, gruppe) for name, gruppe in reversed(sitzungen))
        verteilung = histogramm(läufe) + rollenZeilen(läufe)
    else:
        karten = verteilung = "<p>Noch kein Lauf protokolliert.</p>"
    return (
        '<!doctype html><html lang="de"><head><meta charset="utf-8">'
        "<title>Arbiter · Prozess-Dashboard</title>"
        f"<style>{stil}</style></head><body><h1>Prozess-Dashboard</h1>"
        '<p class="muted">Belegung je Lauf und Sitzung.</p><div class="bericht-zeile">'
        f'<div class="karten-spalte">{karten}</div><aside class="seiten-spalte">'
        f'<section class="kasten"><h3>Verteilung der Tokenstände</h3>{verteilung}</section>'
        f"{legendeErzeugen()}</aside></div></body></html>\n"
    )


def dashboardSchreiben(ordner: Path) -> Path:
    ziel = ordner / dashboardDatei
    ziel.write_text(seiteErzeugen(läufeLesen(ordner)), encoding="utf-8")
    return ziel


def hauptlauf(argumente: list[str]) -> int:
    try:
        ziel = dashboardSchreiben(wurzel)
    except Exception:  # Warum: als Hook bei SubagentStart darf ein Fehler keinen Start stören
        return 0 if "--still" in argumente else 1
    if "--still" not in argumente:  # Warum: Hook-Ausgabe ginge in den Kontext des Agenten
        print(ziel)
    return 0


if __name__ == "__main__":
    sys.exit(hauptlauf(sys.argv[1:]))
