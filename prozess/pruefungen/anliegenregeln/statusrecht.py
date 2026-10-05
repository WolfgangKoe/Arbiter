"""Hook (PreToolUse, Write und Edit): Statusrecht und Absender eines Anliegens."""

import sys
from pathlib import Path

from anliegenregeln.anliegen import Anliegen, höchstRunde, kopfAusText, nächsteFreieNummer
from anliegenregeln.freigabeVerstoss import freigabeVerstoß
from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, verweigerung
from gemeinsam.pfade import anliegenOrdner, projektordner
from lesen.artefakt import artefakte, pfadDer

letzteRunde = "Runde 3/3 ist die letzte; setze `eskaliert`, der Stakeholder entscheidet."


def neuerInhalt(werkzeug: str, angaben: dict, bisher: str) -> str | None:
    if werkzeug == "Write":
        return angaben.get("content")
    if werkzeug == "Edit":
        alt, neu = angaben.get("old_string"), angaben.get("new_string")
        if alt is None or neu is None:
            return None
        anzahl = -1 if angaben.get("replace_all") else 1
        return bisher.replace(alt, neu, anzahl)
    return None


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    # Warum: Ohne Rolle spricht die Hauptsitzung, für sie gilt keine Grenze.
    rolle, werkzeug, angaben = eingabe.rolle, eingabe.werkzeug, eingabe.angaben
    if not rolle or werkzeug not in ("Write", "Edit") or not angaben.get("file_path"):
        return None
    ziel = Path(angaben["file_path"])
    ziel = ziel if ziel.is_absolute() else wurzel / ziel
    ziel = ziel.resolve()
    istArtefakt = ziel in {pfadDer(wurzel, artefakt).resolve() for artefakt in artefakte}
    istAnliegen = ziel.parent == (wurzel / anliegenOrdner).resolve() and ziel.suffix == ".md"
    if not (istArtefakt or istAnliegen):
        return None
    try:
        bisher = ziel.read_text(encoding="utf-8") if ziel.is_file() else ""
    except UnicodeDecodeError:
        return None
    danach = neuerInhalt(werkzeug, angaben, bisher)
    if istArtefakt:
        return freigabeAntwort(ziel, bisher, danach)
    neu = kopfAusText(danach, ziel) if danach is not None else None
    alt = kopfAusText(bisher, ziel)
    if neu is None:
        return None
    grund = (
        absenderVerstoß(alt, neu, nächsteFreieNummer(wurzel))
        or erledigtVerstoß(alt, neu, rolle)
        or rundenVerstoß(alt, neu)
    )
    if grund is None:
        return None
    return verweigerung(f"Statusrecht: {ziel.name} {grund}")


def freigabeAntwort(ziel: Path, bisher: str, danach: str | None) -> dict | None:
    grund = freigabeVerstoß(bisher, danach) if danach is not None else None
    return verweigerung(f"Freigabe und Kommentare: {ziel.name} {grund}") if grund else None


def absenderVerstoß(alt: Anliegen | None, neu: Anliegen, freieNummer: int) -> str | None:
    """Der Absender eines Anliegens ändert sich nie, sonst ersetzt ein Lauf ein fremdes."""
    if alt is None or alt.absender.lower() == neu.absender.lower():
        return None
    return (
        f"gehört {alt.absender}, nicht {neu.absender}. Das ist ein anderes Anliegen: "
        f"nächste freie Nummer {freieNummer}, Kopf und Dateiname ändern, neu schreiben."
    )


def erledigtVerstoß(alt: Anliegen | None, neu: Anliegen, rolle: str) -> str | None:
    if neu.status != "erledigt" or neu.absender.lower() == rolle.lower():
        return None
    if alt is not None and alt.status == "erledigt":
        return None
    return (
        f"setzt auf `erledigt` nur der Absender ({neu.absender}), nicht {rolle}. "
        "Setze `angenommen`, `abgelehnt` oder `beantwortet`."
    )


def rundenVerstoß(alt: Anliegen | None, neu: Anliegen) -> str | None:
    """Senken der Runde und Ändern von `eskaliert` bleibt dem Stakeholder."""
    if alt is None:
        return None
    if neu.runde < alt.runde:
        return f"senkt die Runde von {alt.runde}/3 auf {neu.runde}/3. {letzteRunde}"
    if alt.status == "eskaliert" and neu.status != "eskaliert":
        return f"ändert `eskaliert` zu `{neu.status}`. Der Stakeholder entscheidet."
    if (
        alt.runde == höchstRunde
        and alt.status == "abgelehnt"
        and neu.status not in ("abgelehnt", "eskaliert", "erledigt")
    ):
        return f"setzt in Runde 3/3 nach `abgelehnt` `{neu.status}`. {letzteRunde}"
    return None


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
    sys.exit(0)
