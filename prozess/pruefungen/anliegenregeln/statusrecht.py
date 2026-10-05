"""Hook (PreToolUse, Write und Edit): Statusrecht und Absender eines Anliegens."""

import sys
from pathlib import Path

from anliegenregeln.anliegenNummern import nächsteFreieNummer
from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, verweigerung
from gemeinsam.pfade import anliegenOrdner, projektordner
from gemeinsam.schreibvorgang import bisherigerInhalt, neuerInhalt, schreibZiel
from lesen.anliegenKopf import Anliegen, Status, höchstRunde, kopfAusText

letzteRunde = (
    f"Runde {höchstRunde}/{höchstRunde} ist die letzte; "
    "setze `eskaliert`, der Stakeholder entscheidet."
)


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    # Warum: Ohne Rolle spricht die Hauptsitzung, für sie gilt keine Grenze.
    rolle = eingabe.rolle
    ziel = schreibZiel(eingabe, wurzel) if rolle else None
    if ziel is None or ziel.parent != (wurzel / anliegenOrdner).resolve() or ziel.suffix != ".md":
        return None
    bisher = bisherigerInhalt(ziel)
    danach = neuerInhalt(eingabe, bisher) if bisher is not None else None
    if bisher is None or danach is None:
        return None
    neu = kopfAusText(danach, ziel)
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


def absenderVerstoß(alt: Anliegen | None, neu: Anliegen, freieNummer: int) -> str | None:
    """Der Absender eines Anliegens ändert sich nie, sonst ersetzt ein Lauf ein fremdes."""
    if alt is None or alt.absender.lower() == neu.absender.lower():
        return None
    return (
        f"gehört {alt.absender}, nicht {neu.absender}. Das ist ein anderes Anliegen: "
        f"nächste freie Nummer {freieNummer}, Kopf und Dateiname ändern, neu schreiben."
    )


def erledigtVerstoß(alt: Anliegen | None, neu: Anliegen, rolle: str) -> str | None:
    if neu.status != Status.erledigt or neu.absender.lower() == rolle.lower():
        return None
    if alt is not None and alt.status == Status.erledigt:
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
        return (
            f"senkt die Runde von {alt.runde}/{höchstRunde} auf {neu.runde}/{höchstRunde}. "
            f"{letzteRunde}"
        )
    if alt.status == Status.eskaliert and neu.status != Status.eskaliert:
        return f"ändert `eskaliert` zu `{neu.status}`. Der Stakeholder entscheidet."
    if (
        alt.runde == höchstRunde
        and alt.status == Status.abgelehnt
        and neu.status not in (Status.abgelehnt, Status.eskaliert, Status.erledigt)
    ):
        return (
            f"setzt in Runde {höchstRunde}/{höchstRunde} nach `abgelehnt` "
            f"`{neu.status}`. {letzteRunde}"
        )
    return None


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
    sys.exit(0)
