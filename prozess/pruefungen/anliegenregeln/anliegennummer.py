"""Hook (PreToolUse, Write): Eine neue Anliegen-Datei trägt eine noch nie vergebene Nummer."""

import sys
from pathlib import Path

from anliegenregeln.anliegen import nummerAusDateiname, nächsteFreieNummer, vergebeneNummern
from gemeinsam.hookProtokoll import antwortAusgeben, eingabeLesen, verweigerung, werkzeugAngaben
from gemeinsam.pfade import anliegenOrdner
from rollenregeln.agenten import projektordner


def entscheide(eingabe: dict, wurzel: Path) -> dict | None:
    angaben = werkzeugAngaben(eingabe)
    if eingabe.get("tool_name") != "Write" or not angaben.get("file_path"):
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
