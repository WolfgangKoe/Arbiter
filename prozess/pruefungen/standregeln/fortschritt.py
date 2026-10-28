"""Hook: Schreibt den Abschnitt `## Fortschritt` der laufenden Phase und hakt Fakten selbst ab."""

import re
import sys
from pathlib import Path
from typing import NamedTuple

from gemeinsam.gitAufruf import betreffeSeit, freigabeCommit, gitAusgabe
from gemeinsam.pfade import anforderungsOrdner, handoffOrdner, itemsOrdner, projektordner
from kriterienregeln.kriterium import Kriterium, getesteKriterien
from kriterienregeln.rueckverfolgung import Zuordnung, anforderungUmfasst, umfasst, zuordnungen
from lesen.plan import itemNamen, zyklus
from standregeln.beseitigt import beseitigtErgänzen
from standregeln.phasenfolge import Lage, Phase, hatItemCommit, itemRollen, lage
from standregeln.planFassung import neuGefasst

planName, reviewName, retroName = "plan.md", "review.md", "retro.md"
kritiker = ("Fachkritiker", "Architekt")
codekritiker = ("Architekt", "Reviewer")
reviewkritiker = ("Fachkritiker", "Organisationsentwickler")
kritikAmPlan = "Kritik am Plan"
stakeholderRolle = "Stakeholder"
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


def kriterienZuordnungen(wurzel: Path, text: str) -> list[Zuordnung]:
    """Die Zuordnungen der Anforderungsdateien, deren Kriterien der Text des Items nennt."""
    return [
        zuordnung
        for anforderungsdatei in sorted((wurzel / anforderungsOrdner).rglob("*.md"))
        for zuordnung in zuordnungen(wurzel, anforderungsdatei, [text])
        if anforderungUmfasst([text], zuordnung.verlangt)
    ]


def hatKriterium(wurzel: Path, itemName: str) -> bool:
    """Der Text des Items nennt ein Kriterium; ein gelöschtes Item gilt als mit Kriterium."""
    datei = wurzel / itemsOrdner / itemName
    if not datei.is_file():
        return True
    return bool(kriterienZuordnungen(wurzel, datei.read_text(encoding="utf-8")))


def itemKriterienGetestet(wurzel: Path, itemName: str) -> bool:
    """Jedes Kriterium im Text des Items hat einen Test; ein gelöschtes Item gilt als getestet."""
    datei = wurzel / itemsOrdner / itemName
    if not datei.is_file():
        return True
    text = datei.read_text(encoding="utf-8")
    gefunden = kriterienZuordnungen(wurzel, text)
    return bool(gefunden) and not any(
        ungetestete(text, zuordnung.verlangt, zuordnung.testdatei) for zuordnung in gefunden
    )


def domänenzeilen(wurzel: Path, aktuell: Lage) -> list[Zeile]:
    planFertig = zyklus(wurzel / handoffOrdner / planName) == aktuell.zyklus
    freigegeben = freigabeCommit(wurzel, "Plan", aktuell.zyklus) is not None
    return [
        Zeile("Anforderungsautor", "Happy Paths zum Zyklusziel"),
        Zeile("UX", "Mockups, bei einer Oberfläche"),
        Zeile("Fachkritiker", "Kritik an Anforderungen und Mockups"),
        Zeile("Planer", "Plan geschrieben", planFertig),
        *(Zeile(rolle, kritikAmPlan) for rolle in kritiker),
        Zeile("Stakeholder", f"Freigabe Plan {aktuell.zyklus}", freigegeben),
    ]


def itemzeilen(wurzel: Path, itemName: str) -> list[Zeile]:
    name = itemName.removesuffix(".md")
    gelöscht = not (wurzel / itemsOrdner / itemName).is_file()
    folge = gelöscht or None
    vertrag = Zeile("Architekt", f"Vertrag zu Item {name}, bei beiden Hälften", folge)
    tests = Zeile("Testautor", f"Tests zu Item {name}", itemKriterienGetestet(wurzel, itemName))
    kritikTests = [Zeile(rolle, f"Kritik an den Tests zu Item {name}", folge) for rolle in kritiker]
    testsGrün = Zeile("Implementierer", f"Tests zu Item {name} grün", folge)
    mitTests = [vertrag, tests, *kritikTests, testsGrün] if hatKriterium(wurzel, itemName) else []
    return [
        *mitTests,
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
        Zeile("Reviewer", "DoD über das Inkrement"),
        Zeile("Reviewer", "Review geschrieben", review),
        *(Zeile(rolle, "Kritik am Review") for rolle in reviewkritiker),
        Zeile("Stakeholder", f"Freigabe Review {aktuell.zyklus}", freigegeben),
    ]


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


def vorherigeLage(aktuell: Lage) -> Lage:
    """Die Phase davor: nach der Domänenphase die Prozessphase des Vorzyklus."""
    if aktuell.phase == Phase.technikphase:
        return aktuell._replace(phase=Phase.domänenphase)
    if aktuell.phase == Phase.prozessphase:
        return aktuell._replace(phase=Phase.technikphase)
    return aktuell._replace(zyklus=aktuell.zyklus - 1, phase=Phase.prozessphase)


def nächsteLage(aktuell: Lage) -> Lage:
    """Die Phase danach: nach der Domänenphase die Technikphase, sonst die Domänenphase danach."""
    if aktuell.phase == Phase.domänenphase:
        return aktuell._replace(phase=Phase.technikphase)
    return aktuell._replace(zyklus=aktuell.zyklus + 1, phase=Phase.domänenphase)


def alleOffen(ziel: tuple[Path, list[Zeile]]) -> tuple[Path, list[Zeile]]:
    """Vor Beginn der Phase hakt kein Fakt ab."""
    datei, zeilen = ziel
    return datei, [Zeile(zeile.rolle, zeile.schritt) for zeile in zeilen]


def fürDiesenZyklusGeschrieben(ziel: tuple[Path, list[Zeile]]) -> bool:
    """Der Abschnitt trägt schon die Freigabezeile dieses Zyklus; sonst ist er der eines älteren."""
    datei, zeilen = ziel
    freigaben = [zeile.schlüssel for zeile in zeilen if zeile.rolle == stakeholderRolle]
    return any(name in bisherigeZeilen(datei.read_text(encoding="utf-8")) for name in freigaben)


def kritikAmPlanÖffnen(bisher: Bisher) -> Bisher:
    """Die Haken der Kritik am Plan fallen; Hindernis und Kommentar darunter bleiben."""
    return {
        schlüssel: (abgehakt and not schlüssel.endswith(f": {kritikAmPlan}"), zusatz)
        for schlüssel, (abgehakt, zusatz) in bisher.items()
    }


def abschnittSchreiben(
    wurzel: Path,
    ziel: tuple[Path, list[Zeile]],
    *,
    bisherAusDatei: bool = True,
    planNeuGefasst: bool = False,
) -> str | None:
    datei, zeilen = ziel
    text = datei.read_text(encoding="utf-8")
    bisher = bisherigeZeilen(text) if bisherAusDatei else {}
    bisher = {
        schlüssel: (abgehakt, beseitigtErgänzen(wurzel, zusatz))
        for schlüssel, (abgehakt, zusatz) in bisher.items()
    }
    if planNeuGefasst:
        bisher = kritikAmPlanÖffnen(bisher)
    neu = abschnittEinsetzen(text, abschnittBauen(zeilen, bisher))
    if neu == text:
        return None
    datei.write_text(neu, encoding="utf-8")
    return datei.relative_to(wurzel).as_posix()


def fortschrittSchreiben(wurzel: Path) -> str | None:
    """Schreibt den Abschnitt für die Phase davor, die laufende und die nächste; nennt geänderte."""
    aktuell = lage(wurzel)
    neu = aktuell.phase == Phase.domänenphase and neuGefasst(wurzel, aktuell.zyklus)
    ziele = [zielUndZeilen(wurzel, phase) for phase in (aktuell, vorherigeLage(aktuell))]
    folgendes = zielUndZeilen(wurzel, nächsteLage(aktuell))
    geschrieben = [
        abschnittSchreiben(wurzel, ziel, planNeuGefasst=neu) for ziel in ziele if ziel is not None
    ]
    if folgendes is not None:
        bleibt = fürDiesenZyklusGeschrieben(folgendes)
        geschrieben.append(abschnittSchreiben(wurzel, alleOffen(folgendes), bisherAusDatei=bleibt))
    änderungen = [name for name in geschrieben if name]
    return ", ".join(änderungen) if änderungen else None


if __name__ == "__main__":
    geschrieben = fortschrittSchreiben(projektordner())
    if geschrieben:
        print(f"Fortschritt in {geschrieben} aktualisiert.")
    sys.exit(0)
