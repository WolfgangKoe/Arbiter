"""Hook (PreToolUse, Write und Edit): Freigabe und Kommentare in Plan, Review und Retro."""

from pathlib import Path

from anliegenregeln.freigabeVerstoss import freigabeVerstoß
from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, verweigerung
from gemeinsam.pfade import projektordner
from gemeinsam.schreibvorgang import bisherigerInhalt, neuerInhalt, schreibZiel
from lesen.artefakt import artefakte, pfadDer


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    # Warum: Ohne Rolle spricht die Hauptsitzung, für sie gilt keine Grenze.
    ziel = schreibZiel(eingabe, wurzel) if eingabe.rolle else None
    if ziel is None or ziel not in {pfadDer(wurzel, artefakt).resolve() for artefakt in artefakte}:
        return None
    bisher = bisherigerInhalt(ziel)
    danach = neuerInhalt(eingabe, bisher) if bisher is not None else None
    grund = freigabeVerstoß(bisher, danach) if bisher is not None and danach is not None else None
    return verweigerung(f"Freigabe und Kommentare: {ziel.name} {grund}") if grund else None


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
