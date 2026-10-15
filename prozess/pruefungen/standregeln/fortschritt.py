"""Hook: Schreibt den Abschnitt `## Fortschritt` der laufenden Phase und hakt Fakten selbst ab."""

import re
import sys
from pathlib import Path
from typing import NamedTuple

from gemeinsam.gitAufruf import betreffeSeit, freigabeCommit, gitAusgabe
from gemeinsam.pfade import anforderungsOrdner, handoffOrdner, itemsOrdner, projektordner
from kriterienregeln.kriterium import Kriterium, getesteKriterien
from kriterienregeln.rueckverfolgung import anforderungUmfasst, umfasst, zuordnungen
from lesen.agenten import rollennamen
from lesen.plan import itemNamen, offeneItems, zyklus
from standregeln.phasenfolge import Lage, Phase, hatItemCommit, lage, prozessItems

planName, reviewName, retroName = "plan.md", "review.md", "retro.md"
kritiker = ("Fachkritiker", "Architekt")
codekritiker = ("Architekt", "Reviewer")
umsetzer = "Regelumsetzer"
itemzeile = re.compile(r"^- (P\d+) [^\n(]*\(([^),:]+)", re.MULTILINE)
zeilenmuster = re.compile(r"^- \[([ x])\] (.+)$")
abschnittsmuster = re.compile(r"^## Fortschritt\n(?:(?!## )[^\n]*\n)*", re.MULTILINE)
Bisher = dict[str, tuple[bool, list[str]]]


class Zeile(NamedTuple):
    """Ein Schritt; `fakt` ist `None`, wo nur ein Befehl oder der Stakeholder abhakt."""

    rolle: str
    schritt: str
    fakt: bool | None = None

    @property
    def schlüssel(self) -> str:
        return f"{self.rolle}: {self.schritt}"


def ungetestete(text: str, verlangt: set[Kriterium], testdatei: Path) -> list[Kriterium]:
    getestet = getesteKriterien(testdatei) if testdatei.is_file() else set()
    return [
        kriterium
        for kriterium in verlangt
        if umfasst([text], kriterium) and kriterium not in getestet
    ]


def itemKriterienGetestet(wurzel: Path, itemName: str) -> bool:
    """Jedes Kriterium im Text des Items hat einen Test; ein gelöschtes Item gilt als getestet."""
    datei = wurzel / itemsOrdner / itemName
    if not datei.is_file():
        return True
    text = datei.read_text(encoding="utf-8")
    gefunden = False
    for anforderungsdatei in sorted((wurzel / anforderungsOrdner).rglob("*.md")):
        for zuordnung in zuordnungen(wurzel, anforderungsdatei, [text]):
            if not anforderungUmfasst([text], zuordnung.verlangt):
                continue
            gefunden = True
            if ungetestete(text, zuordnung.verlangt, zuordnung.testdatei):
                return False
    return gefunden


def domänenzeilen(wurzel: Path, aktuell: Lage) -> list[Zeile]:
    planFertig = zyklus(wurzel / handoffOrdner / planName) == aktuell.zyklus
    freigegeben = freigabeCommit(wurzel, "Plan", aktuell.zyklus) is not None
    return [
        Zeile("Anforderungsautor", "Happy Paths zum Zyklusziel"),
        Zeile("UX", "Mockups, bei einer Oberfläche"),
        Zeile("Fachkritiker", "Kritik an Anforderungen und Mockups"),
        Zeile("Planer", "Plan geschrieben", planFertig),
        *(Zeile(rolle, "Kritik am Plan") for rolle in kritiker),
        Zeile("Stakeholder", f"Freigabe Plan {aktuell.zyklus}", freigegeben),
    ]


def itemzeilen(wurzel: Path, itemName: str) -> list[Zeile]:
    name = itemName.removesuffix(".md")
    gelöscht = not (wurzel / itemsOrdner / itemName).is_file()
    # Regel: Ablauf, Technikphase 5 (gelöscht wird erst nach der Abnahme)
    folge = gelöscht or None
    return [
        Zeile("Testautor", f"Tests zu Item {name}", itemKriterienGetestet(wurzel, itemName)),
        *(Zeile(rolle, f"Kritik an den Tests zu Item {name}", folge) for rolle in kritiker),
        Zeile("Implementierer", f"Tests zu Item {name} grün", folge),
        *(Zeile(rolle, f"Kritik am Code zu Item {name}", folge) for rolle in codekritiker),
        Zeile("Fachkritiker", f"Item {name} abgenommen", folge),
        Zeile("Planer", f"Item {name} gelöscht", gelöscht),
    ]


def technikzeilen(wurzel: Path, aktuell: Lage) -> list[Zeile]:
    review = zyklus(wurzel / handoffOrdner / reviewName) == aktuell.zyklus
    freigegeben = freigabeCommit(wurzel, "Review", aktuell.zyklus) is not None
    zeilen = [zeile for name in itemNamen(wurzel) for zeile in itemzeilen(wurzel, name)]
    return [
        *zeilen,
        Zeile("Reviewer", "DoD über das Inkrement", review or not offeneItems(wurzel)),
        Zeile("Reviewer", "Review geschrieben", review),
        Zeile("Stakeholder", f"Freigabe Review {aktuell.zyklus}", freigegeben),
    ]


def itemRollen(wurzel: Path) -> dict[str, str]:
    """Die Rolle je `P<k>` aus der Klammer `- P<k> <Titel> (<Rolle>): …`; sonst Regelumsetzer."""
    text = (wurzel / handoffOrdner / retroName).read_text(encoding="utf-8")
    abschnitt = text.partition("## Prozess-Items")[2].partition("\n## ")[0]
    bekannt = {name.casefold(): name.capitalize() for name in rollennamen(wurzel)}
    genannt = {kennung: rolle.strip().casefold() for kennung, rolle in itemzeile.findall(abschnitt)}
    return {
        kennung: bekannt.get(genannt.get(kennung, ""), umsetzer) for kennung in prozessItems(wurzel)
    }


def prozesszeilen(wurzel: Path, aktuell: Lage) -> list[Zeile]:
    freigabe = freigabeCommit(wurzel, "Retro", aktuell.zyklus)
    betreffe = betreffeSeit(wurzel, freigabe) if freigabe else []
    gepusht = "origin/dev" in gitAusgabe(wurzel, "branch", "-r", "--contains", "HEAD")
    return [
        Zeile("Organisationsentwickler", "Retro geschrieben", fakt=True),
        *(Zeile(rolle, "Kritik an der Retro") for rolle in kritiker),
        Zeile("Organisationsentwickler", "Nachkorrektur"),
        Zeile("Stakeholder", f"Freigabe Retro {aktuell.zyklus}", freigabe is not None),
        *(
            Zeile(rolle, kennung, hatItemCommit(betreffe, aktuell.zyklus, kennung))
            for kennung, rolle in itemRollen(wurzel).items()
        ),
        Zeile("Koordinator", "nach dev gepusht", gepusht),
    ]


def zielUndZeilen(wurzel: Path, aktuell: Lage) -> tuple[Path, list[Zeile]] | None:
    """Die Datei der laufenden Phase und ihre Zeilen; `None`, wo es den Abschnitt nicht gibt."""
    handoff = wurzel / handoffOrdner
    if aktuell.phase == Phase.domänenphase:
        # Regel: Ablauf, Fortschritt (in Zyklus 1 gibt es kein Review)
        if zyklus(handoff / reviewName) != aktuell.zyklus - 1:
            return None
        return handoff / reviewName, domänenzeilen(wurzel, aktuell)
    if aktuell.phase == Phase.technikphase:
        if zyklus(handoff / planName) != aktuell.zyklus:
            return None
        return handoff / planName, technikzeilen(wurzel, aktuell)
    if zyklus(handoff / retroName) != aktuell.zyklus:
        return None
    return handoff / retroName, prozesszeilen(wurzel, aktuell)


def bisherigeZeilen(text: str) -> Bisher:
    """Haken und eingerückte Zeilen (Hindernis, Kommentar) je Zeile des vorhandenen Abschnitts."""
    treffer = abschnittsmuster.search(text)
    bisher: Bisher = {}
    schlüssel = ""
    for zeile in (treffer[0] if treffer else "").splitlines():
        gefunden = zeilenmuster.match(zeile)
        if gefunden:
            schlüssel = gefunden[2]
            bisher[schlüssel] = (gefunden[1] == "x", [])
        elif zeile.startswith("  ") and schlüssel:
            bisher[schlüssel][1].append(zeile)
    return bisher


def abschnittBauen(zeilen: list[Zeile], bisher: Bisher) -> str:
    ausgabe = ["## Fortschritt"]
    for zeile in zeilen:
        abgehakt, zusatz = bisher.get(zeile.schlüssel, (False, []))
        haken = "x" if zeile.fakt or abgehakt else " "
        ausgabe += [f"- [{haken}] {zeile.schlüssel}", *zusatz]
    return "\n".join(ausgabe) + "\n\n"


def abschnittEinsetzen(text: str, abschnitt: str) -> str:
    """Ersetzt den Abschnitt oder setzt ihn vor `## Freigabe`; der übrige Text bleibt."""
    vorhanden = abschnittsmuster.search(text)
    if vorhanden:
        return text[: vorhanden.start()] + abschnitt + text[vorhanden.end() :]
    freigabe = re.search(r"^## Freigabe", text, re.MULTILINE)
    if freigabe:
        return text[: freigabe.start()] + abschnitt + text[freigabe.start() :]
    return text.rstrip("\n") + "\n\n" + abschnitt


def fortschrittSchreiben(wurzel: Path) -> str | None:
    """Schreibt den Abschnitt in die Datei der Phase; nennt sie, wenn sich etwas änderte."""
    ziel = zielUndZeilen(wurzel, lage(wurzel))
    if ziel is None:
        return None
    datei, zeilen = ziel
    text = datei.read_text(encoding="utf-8")
    neu = abschnittEinsetzen(text, abschnittBauen(zeilen, bisherigeZeilen(text)))
    if neu == text:
        return None
    datei.write_text(neu, encoding="utf-8")
    return datei.relative_to(wurzel).as_posix()


if __name__ == "__main__":
    geschrieben = fortschrittSchreiben(projektordner())
    if geschrieben:
        print(f"Fortschritt in {geschrieben} aktualisiert.")
    sys.exit(0)
