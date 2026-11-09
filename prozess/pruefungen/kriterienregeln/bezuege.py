import re
import sys
from pathlib import Path
from typing import NamedTuple

from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, zusatzkontext
from gemeinsam.pfade import projektordner
from kriterienregeln.kriterium import kriteriumZeile, pfadVon, zeilen

anforderungenOrdner = "domaene/anforderungen"
kriteriumKopf = re.compile(r"^- ([A-ZÄÖÜ]+-\d+\.\d+) (.*)$")
fundstelle = re.compile(r"`[^`]*`")
maß = re.compile(r"\d[\d.,/]*+″")
kennungBezug = re.compile(r"\b[A-ZÄÖÜ]{2,}-\d+(?:\.\d+)?\b")
kurzformBezug = re.compile(r"(?<![\w/.])\d{1,3}\.\d{1,3}(?![\w″/.])")
satzteilMarke = re.compile(r"\*\*(?:Gegeben|Wenn|wenn|dann)\*\*")
wort = re.compile(r"[A-Za-zÄÖÜäöüß]{2,}")


class Befund(NamedTuple):
    kennung: str
    zeile: int
    grund: str


def ohneKlammern(text: str) -> str:
    tiefe = 0
    rest = []
    for zeichen in text:
        if zeichen == "(":
            tiefe += 1
        elif zeichen == ")":
            tiefe = max(0, tiefe - 1)
        elif tiefe == 0:
            rest.append(zeichen)
    return "".join(rest)


def sichtbarerText(text: str) -> str:
    return ohneKlammern(maß.sub("", fundstelle.sub("", text)))


def grundZu(text: str) -> str | None:
    sichtbar = sichtbarerText(text)
    treffer = kennungBezug.search(sichtbar) or kurzformBezug.search(sichtbar)
    if treffer:
        return f"Bezug {treffer[0]} außerhalb von Klammern"
    teile = satzteilMarke.split(sichtbar)[1:]
    if any(not wort.search(teil) for teil in teile):
        return "ein Satzteil (Gegeben, wenn, dann) hat kein Wort außerhalb von Klammern"
    return None


def befunde(datei: Path) -> list[Befund]:
    gefunden = []
    for nummer, zeile in enumerate(zeilen(datei), 1):
        treffer = kriteriumKopf.match(zeile)
        grund = grundZu(treffer[2]) if treffer else None
        if treffer and grund:
            gefunden.append(Befund(treffer[1], nummer, grund))
    return gefunden


def anzahlKriterien(datei: Path) -> int:
    return sum(1 for zeile in zeilen(datei) if kriteriumZeile.match(zeile))


def hinweisZu(eingabe: HookEingabe, wurzel: Path) -> dict | None:
    pfad = eingabe.angaben.get("file_path")
    if not pfad or not Path(pfad).is_relative_to(wurzel / anforderungenOrdner):
        return None
    datei = Path(pfad)
    rot = befunde(datei) if datei.is_file() and datei.suffix == ".md" else []
    if not rot:
        return None
    zeilenText = "; ".join(f"{befund.kennung}: {befund.grund}" for befund in rot)
    return zusatzkontext(
        "PostToolUse",
        f"{pfadVon(wurzel, datei)}: {len(rot)} Kriterien mit Bezug statt Satz: {zeilenText}",
    )


def bestandAusgeben(ordner: Path, wurzel: Path) -> None:
    dateien = sorted(ordner.rglob("*.md"))
    gesamt = sum(anzahlKriterien(datei) for datei in dateien)
    rot = [(datei, befunde(datei)) for datei in dateien]
    rot = [(datei, liste) for datei, liste in rot if liste]
    print(f"{sum(len(liste) for _, liste in rot)} von {gesamt} Kriterien in {len(rot)} Dateien rot")
    for datei, liste in rot:
        for befund in liste:
            print(f"{pfadVon(wurzel, datei)}:{befund.zeile} {befund.kennung}: {befund.grund}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        bestandAusgeben(Path(sys.argv[1]).resolve(), projektordner())
    else:
        antwortAusgeben(hinweisZu(HookEingabe.aus(eingabeLesen()), projektordner()))
    sys.exit(0)
