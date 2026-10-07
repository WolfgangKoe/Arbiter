"""Prüft komponenten.html gegen komponenten.css und die Klassen der Seiten."""

import re
from pathlib import Path

from gemeinsam.pfade import frontendOrdner, mockupOrdner, wurzel

stilDatei = "komponenten.css"
seitenDatei = "komponenten.html"
klasseImSelektor = re.compile(r"\.([A-Za-zÄÖÜäöüß]\w*)")
klassenAttribut = re.compile(r"""\bclass\s*=\s*["']([^"']*)["']""", re.IGNORECASE)
verlinkterStil = re.compile(
    r"""<link\b[^>]*\bhref\s*=\s*["'](?:[^"']*/)?komponenten\.css["']""", re.IGNORECASE
)


def selektorTexte(css: str) -> list[str]:
    """Der Text vor jeder öffnenden Klammer, also Selektoren und At-Regeln ohne Deklarationen."""
    texte: list[str] = []
    anfang = 0
    for position, zeichen in enumerate(css):
        if zeichen in "{};":
            if zeichen == "{":
                texte.append(css[anfang:position])
            anfang = position + 1
    return texte


def klassenImStil(css: str) -> set[str]:
    return {klasse for text in selektorTexte(css) for klasse in klasseImSelektor.findall(text)}


def klassenInSeite(html: str) -> set[str]:
    return {klasse for wert in klassenAttribut.findall(html) for klasse in wert.split()}


def klassenSeiten(wurzelOrdner: Path) -> list[Path]:
    ordner = [wurzelOrdner / frontendOrdner, wurzelOrdner / mockupOrdner]
    return [datei for eins in ordner if eins.is_dir() for datei in sorted(eins.glob("*.html"))]


def verstöße(wurzelOrdner: Path = wurzel) -> list[str]:
    stil = wurzelOrdner / frontendOrdner / stilDatei
    if not stil.is_file():
        return []
    seite = stil.with_name(seitenDatei)
    bekannt = klassenImStil(stil.read_text(encoding="utf-8"))
    ergebnis = klassenDerKomponentenseite(seite, bekannt, wurzelOrdner)
    for datei in klassenSeiten(wurzelOrdner):
        neu = klassenInSeite(datei.read_text(encoding="utf-8")) - bekannt
        name = datei.relative_to(wurzelOrdner).as_posix()
        ergebnis += [
            f"{name}: Klasse {klasse} fehlt in {stilDatei}, sie ist neu" for klasse in sorted(neu)
        ]
    return ergebnis


def klassenDerKomponentenseite(seite: Path, bekannt: set[str], wurzelOrdner: Path) -> list[str]:
    name = seite.relative_to(wurzelOrdner).as_posix()
    if not seite.is_file():
        return [f"{name}: fehlt neben {stilDatei}"]
    text = seite.read_text(encoding="utf-8")
    ergebnis = [] if verlinkterStil.search(text) else [f"{name}: verlinkt {stilDatei} nicht"]
    tot = sorted(bekannt - klassenInSeite(text))
    return ergebnis + [
        f"{name}: Klasse {klasse} aus {stilDatei} steht nicht in einem class=, sie ist tot"
        for klasse in tot
    ]
