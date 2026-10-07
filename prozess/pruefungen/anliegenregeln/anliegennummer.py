"""Hook (PreToolUse): Eine neue Anliegen-Datei trägt eine noch nie vergebene Nummer."""

import sys
from pathlib import Path

from anliegenregeln.anliegenNummern import (
    nummerAusDateiname,
    nächsteFreieNummer,
    vergebeneNummern,
)
from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, verweigerung
from gemeinsam.pfade import anliegenOrdner, projektordner


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    angaben = eingabe.angaben
    if eingabe.werkzeug != "Write" or not angaben.get("file_path"):
        return None
    ziel = Path(angaben["file_path"])
    ziel = (ziel if ziel.is_absolute() else wurzel / ziel).resolve()
    if ziel.parent != (wurzel / anliegenOrdner).resolve() or ziel.suffix != ".md":
        return None
    nummer = nummerAusDateiname(ziel.name)
    if ziel.is_file() or nummer is None or nummer not in vergebeneNummern(wurzel):
        return None
    return verweigerung(
        f"Die Nummer {nummer} ist vergeben. Die nächste freie ist "
        f"{nächsteFreieNummer(wurzel)}: Kopf und Dateiname ändern, neu schreiben."
    )


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
    sys.exit(0)
