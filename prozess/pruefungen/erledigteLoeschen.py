"""Löscht jedes Anliegen mit Status `erledigt`; git ist das Archiv.

Läuft mit den übrigen Prüfungen: in `.pre-commit-config.yaml` und bei `SubagentStop`.
Wer den Status setzen darf, prüft `statusrecht.py`.
"""

import sys
from pathlib import Path

from agenten import projektordner
from anliegen import anliegenDateien, kopfLesen


def erledigteLöschen(wurzel: Path) -> list[str]:
    """Löscht die erledigten Anliegen und nennt deren Dateinamen."""
    gelöscht = []
    for datei in anliegenDateien(wurzel):
        gelesen = kopfLesen(datei)
        if gelesen is not None and gelesen.status == "erledigt":
            datei.unlink()
            gelöscht.append(datei.name)
    return gelöscht


if __name__ == "__main__":
    for name in erledigteLöschen(projektordner()):
        print(f"Anliegen {name} war erledigt und ist gelöscht.")
    sys.exit(0)
