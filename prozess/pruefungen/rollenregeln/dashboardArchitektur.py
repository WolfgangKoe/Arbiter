import html
import json
from pathlib import Path

from rollenregeln.architekturKanten import Kante, kantenMessen, kastenPfeile
from rollenregeln.architekturMessung import (
    Kasten,
    Knoten,
    kästenMessen,
    produktOrdner,
    seiteOrdner,
    übersichtUndVertrag,
)
from rollenregeln.dashboardArchitekturSkript import architekturSkript, architekturStil

keineDatei = "keine Datei"
nichtInArchitektur = "nicht in der Architektur"
httpKante = {"von": seiteOrdner, "nach": f"{produktOrdner}/web", "anzahl": 0, "erlaubt": True}
zeilen = (("start",), ("seite", "web", "anwendung", "speicher", "katalog"), ("domaene",))
titel = {
    "start": "Start",
    "seite": "Seite",
    "web": "Web",
    "anwendung": "Anwendung",
    "speicher": "Speicher",
    "katalog": "Katalog",
    "domaene": "Domäne",
}


def tausender(zahl: int) -> str:
    return f"{zahl:,}".replace(",", ".")


def kastenTitel(kasten: Kasten) -> str:
    if kasten.bekannt:
        return titel[kasten.name]
    return f"{kasten.name} · {nichtInArchitektur}"


def knotenZeichnen(knoten: Knoten) -> str:
    art = "ordner" if knoten.istOrdner else "datei"
    pfad = html.escape(knoten.pfad)
    pfadZeile = "" if knoten.istOrdner else f'<span class="ak-zahl">{pfad}</span>'
    kinder = "".join(knotenZeichnen(kind) for kind in knoten.kinder)
    return (
        f'<div class="ak {art}" data-pfad="{pfad}"><div class="ak-kopf">'
        f'<span class="ak-name">{html.escape(knoten.name)}</span>{pfadZeile}'
        f'<span class="ak-zahl">{tausender(knoten.zeichen)} Zeichen</span></div>'
        f'<div class="ak-kinder">{kinder}</div></div>'
    )


def kastenZeichnen(kasten: Kasten) -> str:
    wurzel = kasten.wurzel
    architektur = (
        f"Architektur {tausender(kasten.architekturZeichen)}"
        if kasten.architekturZeichen is not None
        else keineDatei
    )
    zahlen = f'<span class="ak-zahl">Code {tausender(kasten.codeZeichen)}</span>'
    if kasten.name != "start" and kasten.bekannt:
        zahlen += f'<span class="ak-zahl">{architektur}</span>'
    klassen = ["ak", "ordner" if wurzel and wurzel.istOrdner else "datei"]
    if not kasten.codeZeichen:
        klassen.append("leer")
    if not kasten.bekannt:
        klassen.append("unbekannt")
    pfad = html.escape(wurzel.pfad) if wurzel else f"{produktOrdner}/{kasten.name}"
    kinder = "".join(knotenZeichnen(kind) for kind in wurzel.kinder) if wurzel else ""
    return (
        f'<div class="{" ".join(klassen)}" data-kasten="{kasten.name}" data-pfad="{pfad}">'
        f'<div class="ak-kopf"><span class="ak-name">{html.escape(kastenTitel(kasten))}</span>'
        f'{zahlen}</div><div class="ak-kinder">{kinder}</div></div>'
    )


def zeilenZeichnen(kästen: list[Kasten]) -> str:
    nachName = {kasten.name: kasten for kasten in kästen}
    fremde = [kasten for kasten in kästen if not kasten.bekannt]
    gruppen = [[nachName[name] for name in zeile] for zeile in zeilen] + [fremde]
    return "".join(
        '<div class="ak-zeile">' + "".join(kastenZeichnen(kasten) for kasten in gruppe) + "</div>"
        for gruppe in gruppen
        if gruppe
    )


def kantenAlsJson(kanten: list[Kante]) -> str:
    daten = [kante._asdict() | {"text": None} for kante in kanten] + [httpKante | {"text": "HTTP"}]
    return json.dumps(daten).replace("</", "<\\/")


def urteil(kästen: list[Kasten], kanten: list[Kante]) -> str:
    namen = {kasten.name: kastenTitel(kasten) for kasten in kästen}
    verboten = [pfeil for pfeil in kastenPfeile(kanten) if not pfeil.erlaubt]
    if not verboten:
        return "Kein verbotener Pfeil."
    pfeile = ", ".join(
        f"{namen.get(pfeil.von, pfeil.von)} → {namen.get(pfeil.nach, pfeil.nach)}"
        for pfeil in verboten
    )
    return f"Verbotene Pfeile: {html.escape(pfeile)}"


def architekturSeite(wurzel: Path) -> str:
    kästen = kästenMessen(wurzel)
    kanten = kantenMessen(wurzel, kästen)
    übersicht, vertrag = übersichtUndVertrag(wurzel)
    return (
        f"<style>{architekturStil}</style>"
        f'<p class="muted">{urteil(kästen, kanten)} Ein Klick öffnet oder schließt einen Kasten. '
        "Zahlen an Pfeilen: Importzeilen. Zeichen: Übersicht "
        f"{tausender(übersicht)} und Vertrag {tausender(vertrag)}.</p>"
        f'<div class="architektur" id="architektur">{zeilenZeichnen(kästen)}</div>'
        f'<script type="application/json" id="architektur-kanten">{kantenAlsJson(kanten)}</script>'
        f"<script>{architekturSkript}</script>"
    )
