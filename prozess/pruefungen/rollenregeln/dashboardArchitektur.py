from pathlib import Path

from rollenregeln.architekturMessung import (
    Kasten,
    Pfeil,
    kästenMessen,
    pfeileMessen,
    übersichtUndVertrag,
)

kastenBreite = 120
kastenHöhe = 62
spaltenabstand = 135
zeilenabstand = 105
rand = 14
keineDatei = "keine Datei"
httpPfeil = ("seite", "web")

kastenLage = {
    "start": (4, 0),
    "seite": (0, 1),
    "web": (1, 1),
    "anwendung": (2, 1),
    "speicher": (3, 1),
    "katalog": (5, 1),
    "domaene": (4, 2),
}
titel = {
    "start": "Start",
    "seite": "Seite",
    "web": "Web",
    "anwendung": "Anwendung",
    "speicher": "Speicher",
    "katalog": "Katalog",
    "domaene": "Domäne",
}
breite = rand * 2 + 5 * spaltenabstand + kastenBreite
höhe = rand * 2 + 2 * zeilenabstand + kastenHöhe

kartenStil = """
.karte-kasten{fill:var(--panel);stroke:var(--c-subagent);stroke-width:1.5}
.karte-kasten.leer{stroke-dasharray:5 4;fill:none}
.karte-name{fill:var(--accent-text);font-size:12px;font-weight:600}
.karte-zahl{fill:var(--text-muted);font-size:9.5px}
.pfeil{stroke:var(--text-muted);stroke-width:1.5;fill:none}
.pfeil.verboten{stroke:var(--c-warnung);stroke-width:2.5}
.pfeil-spitze{fill:var(--text-muted)}.pfeil-spitze.verboten{fill:var(--c-warnung)}
.pfeil-text{fill:var(--text);font-size:10px;font-weight:600}
.pfeil-text.verboten{fill:var(--c-warnung)}
"""


def tausender(zahl: int) -> str:
    return f"{zahl:,}".replace(",", ".")


def mitte(name: str) -> tuple[float, float]:
    spalte, zeile = kastenLage[name]
    return (
        rand + spalte * spaltenabstand + kastenBreite / 2,
        rand + zeile * zeilenabstand + kastenHöhe / 2,
    )


def randpunkt(name: str, richtungX: float, richtungY: float) -> tuple[float, float]:
    mitteX, mitteY = mitte(name)
    faktorX = (kastenBreite / 2) / abs(richtungX) if richtungX else float("inf")
    faktorY = (kastenHöhe / 2) / abs(richtungY) if richtungY else float("inf")
    faktor = min(faktorX, faktorY)
    return mitteX + richtungX * faktor, mitteY + richtungY * faktor


def pfeilZeichnen(von: str, nach: str, text: str, *, verboten: bool) -> str:
    vonX, vonY = mitte(von)
    nachX, nachY = mitte(nach)
    anfangX, anfangY = randpunkt(von, nachX - vonX, nachY - vonY)
    endeX, endeY = randpunkt(nach, vonX - nachX, vonY - nachY)
    klasse = "pfeil verboten" if verboten else "pfeil"
    spitze = "spitzeVerboten" if verboten else "spitze"
    textKlasse = "pfeil-text verboten" if verboten else "pfeil-text"
    labelX = anfangX + (endeX - anfangX) * 0.35
    labelY = anfangY + (endeY - anfangY) * 0.35 - 4
    return (
        f'<line class="{klasse}" x1="{anfangX:.1f}" y1="{anfangY:.1f}" '
        f'x2="{endeX:.1f}" y2="{endeY:.1f}" marker-end="url(#{spitze})"/>'
        f'<text class="{textKlasse}" text-anchor="middle" x="{labelX:.1f}" '
        f'y="{labelY:.1f}">{text}</text>'
    )


def kastenZeichnen(kasten: Kasten) -> str:
    spalte, zeile = kastenLage[kasten.name]
    links = rand + spalte * spaltenabstand
    oben = rand + zeile * zeilenabstand
    mitteX = links + kastenBreite / 2
    architektur = (
        f"Architektur {tausender(kasten.architekturZeichen)}"
        if kasten.architekturZeichen is not None
        else keineDatei
    )
    zahlen = [f"Code {tausender(kasten.codeZeichen)}"]
    if kasten.name != "start":
        zahlen.append(architektur)
    klasse = "karte-kasten" if kasten.codeZeichen else "karte-kasten leer"
    zeilen = "".join(
        f'<text class="karte-zahl" text-anchor="middle" x="{mitteX}" '
        f'y="{oben + 38 + nummer * 12}">{text}</text>'
        for nummer, text in enumerate(zahlen)
    )
    return (
        f'<g data-kasten="{kasten.name}"><rect class="{klasse}" x="{links}" y="{oben}" '
        f'width="{kastenBreite}" height="{kastenHöhe}" rx="6"/>'
        f'<text class="karte-name" text-anchor="middle" x="{mitteX}" y="{oben + 20}">'
        f"{titel[kasten.name]}</text>{zeilen}</g>"
    )


def spitzen() -> str:
    def spitze(kennung: str, klasse: str) -> str:
        return (
            f'<marker id="{kennung}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto"><path class="{klasse}" d="M0 0L10 5L0 10z"/></marker>'
        )

    return (
        "<defs>"
        + spitze("spitze", "pfeil-spitze")
        + spitze("spitzeVerboten", "pfeil-spitze verboten")
        + "</defs>"
    )


def kartenBild(kästen: list[Kasten], pfeile: list[Pfeil]) -> str:
    gemessen = "".join(
        pfeilZeichnen(pfeil.von, pfeil.nach, str(pfeil.anzahl), verboten=not pfeil.erlaubt)
        for pfeil in pfeile
    )
    fest = pfeilZeichnen(*httpPfeil, "HTTP", verboten=False)
    inhalt = "".join(kastenZeichnen(kasten) for kasten in kästen)
    return (
        f'<svg class="architekturkarte" viewBox="0 0 {breite} {höhe}" width="{breite}" '
        f'height="{höhe}">{spitzen()}{gemessen}{fest}{inhalt}</svg>'
    )


def architekturKarte(wurzel: Path) -> str:
    kästen = kästenMessen(wurzel)
    pfeile = pfeileMessen(wurzel, kästen)
    übersicht, vertrag = übersichtUndVertrag(wurzel)
    verboten = [pfeil for pfeil in pfeile if not pfeil.erlaubt]
    urteil = (
        "Verbotene Pfeile: "
        + ", ".join(f"{titel[pfeil.von]} → {titel[pfeil.nach]}" for pfeil in verboten)
        if verboten
        else "Kein verbotener Pfeil."
    )
    return (
        '<section class="kasten"><h3>Architektur</h3>'
        f'<div class="karten-diagramm">{kartenBild(kästen, pfeile)}</div>'
        f'<p class="muted">{urteil} Zahlen an Pfeilen: Importzeilen. Zeichen: Übersicht '
        f"{tausender(übersicht)} und Vertrag {tausender(vertrag)}.</p></section>"
    )
