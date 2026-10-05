"""Zeichnet die SVG-Diagramme des Dashboards: Säulen je Lauf und Histogramm der Belegung."""

import html
import statistics

from standregeln.belegung import sperrschwelle, warnschwelle

klassenbreite = 25_000
säulenbreite = 30
säulenabstand = 14
diagrammhöhe = 200
randLinks = 44
randOben = 20
randUnten = 70
achsenschritt = 50_000
histogrammBreite = 290
histogrammRand = 30
histogrammMarken = 4
achsenhöhe = 1.1 * sperrschwelle


def kilo(zahl: float) -> str:
    return f"{round(zahl / 1000)}k"


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


def histogramm(läufe: list[dict]) -> str:
    werte = [lauf["belegung"] for lauf in läufe]
    klassen = int(achsenhöhe // klassenbreite) + 1
    anzahl = [0] * klassen
    for wert in werte:
        anzahl[min(wert // klassenbreite, klassen - 1)] += 1
    höchste = max(anzahl)
    spalte = (histogrammBreite - histogrammRand) / klassen

    def oben(menge: float) -> float:
        return 100 - 90 * menge / höchste

    achse = "".join(
        f'<line class="gitter" x1="{histogrammRand - 4}" x2="{histogrammRand}" '
        f'y1="{oben(marke):.1f}" y2="{oben(marke):.1f}"/>'
        f'<text class="achse-text" text-anchor="end" x="{histogrammRand - 6}" '
        f'y="{oben(marke) + 3:.1f}">{marke}</text>'
        for marke in range(0, höchste + 1, max(1, höchste // histogrammMarken))
    )
    säulen = "".join(
        f'<rect class="saeule" x="{histogrammRand + nummer * spalte + 2:.1f}" '
        f'y="{oben(wert):.1f}" width="{spalte - 4:.1f}" height="{100 - oben(wert):.1f}"/>'
        f'<text class="wert-text" text-anchor="middle" '
        f'x="{histogrammRand + nummer * spalte + spalte / 2:.1f}" y="{oben(wert) - 3:.1f}">'
        f"{wert}</text>"
        f'<text class="achse-text" text-anchor="middle" '
        f'x="{histogrammRand + nummer * spalte + spalte / 2:.1f}" y="112">'
        f"{nummer * klassenbreite // 1000}k</text>"
        for nummer, wert in enumerate(anzahl)
    )
    median = statistics.median(werte)
    mitteMedian = histogrammRand + min(median, achsenhöhe) / klassenbreite * spalte
    return (
        f'<svg viewBox="0 0 {histogrammBreite} 120" width="{histogrammBreite}" height="120">'
        f'<line class="gitter" x1="{histogrammRand}" x2="{histogrammRand}" y1="0" y2="100"/>'
        f"{achse}{säulen}"
        f'<line class="vert-median" x1="{mitteMedian:.1f}" x2="{mitteMedian:.1f}" y1="0" y2="100"/>'
        f'</svg><p class="muted">Median {kilo(median)}, '
        f"je Klasse {klassenbreite // 1000}k, Zahl über dem Balken: Läufe</p>"
    )
