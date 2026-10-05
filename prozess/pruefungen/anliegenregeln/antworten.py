"""Prüft, dass unter jeder Frage an den Stakeholder eine Zeile `Antwort:` steht."""

import re

from lesen.anliegenKopf import Anliegen, stakeholder

frage = re.compile(r"^\*\*F(\d+)\b")
antwortZeile = re.compile(r"^Antwort:")


def antwortVerstöße(text: str, anliegen: Anliegen) -> list[str]:
    """Unter jeder Frage an den Stakeholder steht eine Zeile `Antwort:`."""
    if anliegen.empfänger != stakeholder or anliegen.status != "offen":
        return []
    verstöße = []
    nummer = None
    beantwortet = True
    for zeile in [*text.splitlines(), "## Ende"]:
        neueFrage = frage.match(zeile)
        if neueFrage or zeile.startswith("## "):
            if not beantwortet:
                verstöße.append(f"Frage F{nummer} hat keine Zeile `Antwort:`")
            nummer, beantwortet = (neueFrage[1], False) if neueFrage else (None, True)
        elif antwortZeile.match(zeile):
            beantwortet = True
    return verstöße
