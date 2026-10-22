"""Züge des Stakeholders auf eine Zeile im Fortschritt: Haken setzen, Kommentar als Anliegen."""

from pathlib import Path

from gemeinsam.pfade import anliegenOrdner
from lesen.anliegenKopf import höchstRunde, stakeholder
from standregeln.fortschritt import (
    Zeile,
    abschnittBauen,
    abschnittEinsetzen,
    bisherigeZeilen,
    zielUndZeilen,
)
from standregeln.hindernis import beseitigerName, dateiname, einzeiler, nächsteNummer
from standregeln.phasenfolge import lage

hakenArt, kommentarArt = "haken", "kommentarZeile"
abgehaktWert = "x"
vorlage = """# Kommentar: {schritt}

Form: Kritik
Von: {stakeholder}
An: {rolle}
Runde: 1/{höchstRunde}
Status: offen

## Runde 1
**Befund.** Der Stakeholder kommentiert im Fortschritt den Schritt „{schritt}“ von {rolle}: {text}

**Kosten.** Der Schritt bleibt, wie er ist, bis die Rolle den Kommentar beantwortet.

**Gegenvorschlag.** {rolle} setzt den Kommentar um oder widerspricht.

**Stellungnahme.**
"""
keineZeile = "Die Zeile steht nicht mehr im Fortschritt."
keineRolle = "Die Zeile gehört keiner Rolle; kommentiere im Anliegen."
leer = "Der Kommentar war leer."
vonFakt = "Die Zeile hakt ein Fakt ab; sie lässt sich nicht von Hand setzen."


def zeileFinden(wurzel: Path, schlüssel: str) -> tuple[Path, list[Zeile], Zeile] | None:
    ziel = zielUndZeilen(wurzel, lage(wurzel))
    if ziel is None:
        return None
    datei, zeilen = ziel
    treffer = [zeile for zeile in zeilen if zeile.schlüssel == schlüssel]
    return (datei, zeilen, treffer[0]) if treffer else None


def anliegenAnlegen(wurzel: Path, zeile: Zeile, rolle: str, text: str) -> int:
    nummer = nächsteNummer(wurzel)
    inhalt = vorlage.format(
        schritt=zeile.schritt,
        nummer=nummer,
        stakeholder=stakeholder,
        rolle=rolle,
        höchstRunde=höchstRunde,
        text=text,
    )
    datei = wurzel / anliegenOrdner / dateiname(nummer, zeile.schritt, "kommentar")
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(inhalt, encoding="utf-8")
    return nummer


def zeilenzugÜbernehmen(wurzel: Path, schlüssel: str, art: str, wert: str) -> str | None:
    """Setzt Haken oder Kommentar der Zeile; nennt den Grund, wenn der Zug nicht passt."""
    gefunden = zeileFinden(wurzel, schlüssel)
    if gefunden is None:
        return keineZeile
    datei, zeilen, zeile = gefunden
    text = einzeiler(wert)
    rolle = beseitigerName(wurzel, zeile.rolle)
    if art == hakenArt and zeile.fakt is not None:
        return vonFakt
    if art == kommentarArt and not text:
        return leer
    if art == kommentarArt and rolle in (None, stakeholder):
        return keineRolle
    inhalt = datei.read_text(encoding="utf-8")
    bisher = bisherigeZeilen(inhalt)
    abgehakt, zusatz = bisher.get(schlüssel, (False, []))
    if art == hakenArt:
        abgehakt = abgehakt or wert == abgehaktWert
    else:
        nummer = anliegenAnlegen(wurzel, zeile, str(rolle), text)
        zusatz.append(f"  Kommentar: {text} (Anliegen {nummer})")
    bisher[schlüssel] = (abgehakt, zusatz)
    datei.write_text(abschnittEinsetzen(inhalt, abschnittBauen(zeilen, bisher)), encoding="utf-8")
    return None
