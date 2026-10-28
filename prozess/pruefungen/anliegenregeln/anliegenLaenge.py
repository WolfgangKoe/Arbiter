"""Misst die Länge eines Anliegens gegen seine Grenze (4.000 Zeichen je Runde)."""

import re
import sys
from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, zusatzkontext
from gemeinsam.pfade import anliegenOrdner, projektordner
from lesen.anliegenKopf import Status, kopfLesen

zeichenJeRunde = 4000
hinweisAbstand = 100
antwortZeile = re.compile(r"^Antwort:.*$", re.MULTILINE)


def länge(text: str) -> int:
    """Zeichen des Anliegens; jede Zeile `Antwort:` zählt als `Antwort: .`."""
    return len(antwortZeile.sub("Antwort: .", text))


def grenze(runde: int) -> int:
    return zeichenJeRunde * runde


def längeBefund(datei: Path) -> tuple[str, str] | None:
    """`("rot", Text)` über der Grenze, `("hinweis", Text)` im Hinweisbereich, sonst `None`."""
    anliegen = kopfLesen(datei)
    if anliegen is None or anliegen.status == Status.erledigt:
        return None
    zeichen = länge(datei.read_text(encoding="utf-8"))
    obergrenze = grenze(anliegen.runde)
    if zeichen > obergrenze:
        return "rot", (
            f"{datei.name} hat {zeichen} Zeichen, erlaubt sind {obergrenze} "
            f"(Runde {anliegen.runde}): kürzen"
        )
    if zeichen >= obergrenze - hinweisAbstand:
        return "hinweis", (
            f"{datei.name} hat {zeichen} von {obergrenze} Zeichen (Runde {anliegen.runde}): "
            "bald kürzen"
        )
    return None


def hinweisZu(eingabe: HookEingabe, wurzel: Path) -> dict | None:
    """Die Rückmeldung nach Write oder Edit eines Anliegens im Hinweisbereich oder darüber."""
    pfad = eingabe.angaben.get("file_path")
    if not pfad or not Path(pfad).is_relative_to(wurzel / anliegenOrdner):
        return None
    datei = Path(pfad)
    befund = längeBefund(datei) if datei.is_file() else None
    return zusatzkontext("PostToolUse", befund[1]) if befund else None


if __name__ == "__main__":
    antwortAusgeben(hinweisZu(HookEingabe.aus(eingabeLesen()), projektordner()))
    sys.exit(0)
