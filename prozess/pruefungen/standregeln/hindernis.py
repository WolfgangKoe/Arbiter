"""Befehl: Eine Rolle meldet ein Hindernis; es wird ein Anliegen und eine Zeile im Fortschritt."""

import re
import sys
from pathlib import Path

from gemeinsam.pfade import anliegenOrdner, projektordner
from lesen.agenten import rollennamen
from lesen.anliegenKopf import (
    anliegenDateien,
    belegteNummern,
    freieNummer,
    höchstRunde,
    nummerAusDatei,
    stakeholder,
)
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

aufrufteileRolleSchrittBeseitigerTextZiel = 5
bereichsmuster = re.compile(r"(\d+)-(\d+)")
längeDesNamens = 40
umlaute = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})
vorlage = """# Hindernis: {schritt}

Form: {form}
Von: {rolle}
An: {beseitiger}
Runde: 1/{höchstRunde}
Status: offen

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


def dateiname(nummer: int, schritt: str, vorsilbe: str = "hindernis") -> str:
    """`<nr>-<vorsilbe><Schritt>.md` in ASCII und camelCase, wie die Benennung es verlangt."""
    wörter = re.findall(r"[a-z0-9]+", schritt.casefold().translate(umlaute))
    name = vorsilbe + "".join(wort.capitalize() for wort in wörter)
    return f"{nummer:02d}-{name[:längeDesNamens]}.md"


def nächsteNummer(wurzel: Path) -> int:
    """Die nächste freie Nummer: größer als jede im Ordner und in der Geschichte."""
    return max(belegteNummern(wurzel), default=0) + 1


def beseitigerName(wurzel: Path, genannt: str) -> str | None:
    if genannt.casefold() == stakeholder.casefold():
        return stakeholder
    bekannt = {name.casefold(): name.capitalize() for name in rollennamen(wurzel)}
    return bekannt.get(genannt.casefold())


def anliegenSchreiben(wurzel: Path, zeile: Zeile, beseitiger: str, text: str, nummer: int) -> Path:
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


def anliegenVorhanden(wurzel: Path, nummer: int) -> bool:
    return any(nummerAusDatei(datei) == nummer for datei in anliegenDateien(wurzel))


def hindernisMelden(  # noqa: PLR0913
    wurzel: Path, rolle: str, schritt: str, beseitiger: str, text: str, ziel: range | int
) -> int | None:
    """Schreibt `Hindernis:` unter die Zeile; neues Anliegen aus dem Bereich oder vorhandenes."""
    fortschrittSchreiben(wurzel)
    gefunden = eigeneZeile(wurzel, rolle, schritt)
    name = beseitigerName(wurzel, beseitiger)
    if gefunden is None or name is None:
        return None
    datei, zeilen, zeile = gefunden
    if isinstance(ziel, int):
        nummer = ziel if anliegenVorhanden(wurzel, ziel) else None
    else:
        nummer = freieNummer(wurzel, ziel)
        if nummer is not None:
            anliegenSchreiben(wurzel, zeile, name, einzeiler(text), nummer)
    if nummer is None:
        return None
    inhalt = datei.read_text(encoding="utf-8")
    bisher = bisherigeZeilen(inhalt)
    abgehakt, zusatz = bisher.get(zeile.schlüssel, (False, []))
    zusatz.append(f"  Hindernis: {einzeiler(text)} (Anliegen {nummer})")
    bisher[zeile.schlüssel] = (abgehakt, zusatz)
    datei.write_text(abschnittEinsetzen(inhalt, abschnittBauen(zeilen, bisher)), encoding="utf-8")
    return nummer


def zielLesen(text: str) -> range | int | None:
    """`3940-3959` ist ein Bereich für ein neues Anliegen, `3941` ein vorhandenes."""
    bereich = bereichsmuster.fullmatch(text)
    if bereich:
        return range(int(bereich[1]), int(bereich[2]) + 1)
    return int(text) if text.isdigit() else None


def hauptprogramm(argumente: list[str]) -> int:
    ziel = zielLesen(argumente[-1]) if argumente else None
    if len(argumente) != aufrufteileRolleSchrittBeseitigerTextZiel or ziel is None:
        print(
            "Aufruf: python3 prozess/pruefungen/gemeinsam/lauf.py standregeln.hindernis"
            " <Rolle> <Schritt> <Beseitiger> <Text> <erste>-<letzte> | <Nummer>\n"
            "Der Bereich aus dem Auftrag legt ein neues Anliegen an; die Nummer nennt das"
            " Anliegen, das schon als Kritik besteht.",
            file=sys.stderr,
        )
        return 1
    rolle, schritt, beseitiger, text, _ = argumente
    nummer = hindernisMelden(projektordner(), rolle, schritt, beseitiger, text, ziel)
    if nummer is None:
        print(
            f"Kein einzelner Schritt von {rolle} passt zu „{schritt}“, {beseitiger} "
            "ist keine Rolle, der Bereich ist voll oder das Anliegen fehlt.",
            file=sys.stderr,
        )
        return 1
    print(f"Hindernis gemeldet: Anliegen {nummer} an {beseitiger}.")
    return 0


if __name__ == "__main__":
    sys.exit(hauptprogramm(sys.argv[1:]))
