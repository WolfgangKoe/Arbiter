"""Befehl: Schreibt die Köpfe der Anliegen von der alten Zeile auf Felder um."""

import sys
from pathlib import Path

from gemeinsam.pfade import projektordner
from lesen.anliegenKopf import anliegenDateien, felderLesen, kopfLesen, kopfÄndern


def köpfeUmschreiben(wurzel: Path) -> list[str]:
    """Schreibt jede Datei mit alter Kopfzeile um; nennt die Dateinamen."""
    umgeschrieben = []
    for datei in anliegenDateien(wurzel):
        text = datei.read_text(encoding="utf-8")
        anliegen = kopfLesen(datei)
        if felderLesen(text.splitlines()) or anliegen is None:
            continue
        neu = kopfÄndern(text, {})
        if neu is not None:
            datei.write_text(neu, encoding="utf-8")
            umgeschrieben.append(datei.name)
    return umgeschrieben


if __name__ == "__main__":
    for name in köpfeUmschreiben(projektordner()):
        print(f"Kopf umgeschrieben: {name}")
    sys.exit(0)
