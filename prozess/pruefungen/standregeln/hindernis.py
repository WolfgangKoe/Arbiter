"""Befehl: Eine Rolle meldet ein Hindernis; es wird ein Anliegen und eine Zeile im Fortschritt."""

import re
import sys
from pathlib import Path

from gemeinsam.gitAufruf import gitAusgabe
from gemeinsam.pfade import anliegenOrdner, projektordner
from lesen.agenten import rollennamen
from lesen.anliegenKopf import höchstRunde, stakeholder
from standregeln.abhaken import gleicheRolle
from standregeln.fortschritt import (
    Zeile,
    abschnittBauen,
    abschnittEinsetzen,
    bisherigeZeilen,
    fortschrittSchreiben,
    zielUndZeilen,
)
from standregeln.phasenfolge import lage

aufrufteile = 4  # Warum: Rolle, Schritt, Beseitiger und Text
dateinummer = re.compile(rf"{anliegenOrdner}/(\d+)-")
längeDesNamens = 40
umlaute = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})
vorlage = """# Hindernis: {schritt}

{nummer} · {form} · von {rolle} → {beseitiger} · Runde 1/{höchstRunde} · offen

## Runde 1
**Befund.** {text} Das hält den Schritt „{schritt}“ von {rolle} im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** {gegenvorschlag}

{frage}**Stellungnahme.**
"""
frageVorlage = """**F1 · Beseitigst du das Hindernis?**
A: Ja, wie im Gegenvorschlag. B: Nein, der Schritt entfällt.
Empfehlung: A.
Antwort: .

"""


def einzeiler(text: str) -> str:
    return " ".join(text.split())


def dateiname(nummer: int, schritt: str) -> str:
    """`<nr>-hindernis<Schritt>.md` in ASCII und camelCase, wie die Benennung es verlangt."""
    wörter = re.findall(r"[a-z0-9]+", schritt.casefold().translate(umlaute))
    name = "hindernis" + "".join(wort.capitalize() for wort in wörter)
    return f"{nummer:02d}-{name[:längeDesNamens]}.md"


def nächsteNummer(wurzel: Path) -> int:
    """Die nächste freie Nummer: größer als jede im Ordner und in der Geschichte."""
    log = ("log", "--all", "--format=", "--name-only", "--", anliegenOrdner)
    geschichte = gitAusgabe(wurzel, *log)
    dateien = (wurzel / anliegenOrdner).glob("*.md")
    vorhandene = [datei.name.partition("-")[0] for datei in dateien]
    nummern = [int(nummer) for nummer in vorhandene if nummer.isdigit()]
    nummern += [int(nummer) for nummer in dateinummer.findall(geschichte)]
    return max(nummern, default=0) + 1


def beseitigerName(wurzel: Path, genannt: str) -> str | None:
    if genannt.casefold() == stakeholder.casefold():
        return stakeholder
    bekannt = {name.casefold(): name.capitalize() for name in rollennamen(wurzel)}
    return bekannt.get(genannt.casefold())


def anliegenSchreiben(
    wurzel: Path, zeile: Zeile, beseitiger: str, text: str, nummer: int
) -> Path:
    fragt = beseitiger == stakeholder
    inhalt = vorlage.format(
        schritt=zeile.schritt,
        nummer=nummer,
        form="Fragen" if fragt else "Kritik",
        rolle=zeile.rolle,
        beseitiger=beseitiger,
        höchstRunde=höchstRunde,
        text=text,
        gegenvorschlag=f"{beseitiger} beseitigt das Hindernis.",
        frage=frageVorlage if fragt else "",
    )
    datei = wurzel / anliegenOrdner / dateiname(nummer, zeile.schritt)
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(inhalt, encoding="utf-8")
    return datei


def eigeneZeile(wurzel: Path, rolle: str, schritt: str) -> tuple[Path, list[Zeile], Zeile] | None:
    """Die Datei, ihre Zeilen und die eine Zeile der Rolle, deren Schritt den Text enthält."""
    ziel = zielUndZeilen(wurzel, lage(wurzel))
    if ziel is None:
        return None
    datei, zeilen = ziel
    treffer = [
        zeile
        for zeile in zeilen
        if gleicheRolle(zeile, rolle) and schritt.casefold() in zeile.schritt.casefold()
    ]
    return (datei, zeilen, treffer[0]) if len(treffer) == 1 else None


def hindernisMelden(
    wurzel: Path, rolle: str, schritt: str, beseitiger: str, text: str
) -> int | None:
    """Legt das Anliegen an, schreibt `Hindernis:` unter die Zeile; nennt die Nummer."""
    fortschrittSchreiben(wurzel)
    gefunden = eigeneZeile(wurzel, rolle, schritt)
    name = beseitigerName(wurzel, beseitiger)
    if gefunden is None or name is None:
        return None
    datei, zeilen, zeile = gefunden
    nummer = nächsteNummer(wurzel)
    anliegenSchreiben(wurzel, zeile, name, einzeiler(text), nummer)
    inhalt = datei.read_text(encoding="utf-8")
    bisher = bisherigeZeilen(inhalt)
    abgehakt, zusatz = bisher.get(zeile.schlüssel, (False, []))
    zusatz.append(f"  Hindernis: {einzeiler(text)} (Anliegen {nummer})")
    bisher[zeile.schlüssel] = (abgehakt, zusatz)
    datei.write_text(abschnittEinsetzen(inhalt, abschnittBauen(zeilen, bisher)), encoding="utf-8")
    return nummer


def hauptprogramm(argumente: list[str]) -> int:
    if len(argumente) != aufrufteile:
        print("Aufruf: hindernis.py <Rolle> <Schritt> <Beseitiger> <Text>", file=sys.stderr)
        return 1
    rolle, schritt, beseitiger, text = argumente
    nummer = hindernisMelden(projektordner(), rolle, schritt, beseitiger, text)
    if nummer is None:
        print(
            f"Kein einzelner Schritt von {rolle} passt zu „{schritt}“, oder {beseitiger} "
            "ist keine Rolle.",
            file=sys.stderr,
        )
        return 1
    print(f"Hindernis gemeldet: Anliegen {nummer} an {beseitiger}.")
    return 0


if __name__ == "__main__":
    sys.exit(hauptprogramm(sys.argv[1:]))
