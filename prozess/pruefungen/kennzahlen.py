"""Kennzahlen für die Retro (`prozess/kennzahlen.md`): Rollenläufe und offene Anliegen.

Aufruf: `python3 prozess/pruefungen/kennzahlen.py`. Rollenläufe je Phase und Rolle aus dem
Protokoll von `rollenzaehler.py`; offene Anliegen je Rolle, die dran ist, mit Alter in Tagen
seit dem Anlegen in git.
"""

import json
from collections import Counter
from datetime import UTC, date, datetime
from pathlib import Path

from agenten import projektordner
from anliegen import Anliegen, gelesene, wartetAuf
from gitAufruf import gitAusgabe
from stand import protokoll


def rollenläufeJePhaseUndRolle(wurzel: Path) -> dict[str, Counter[str]]:
    datei = protokoll(wurzel)
    läufe: dict[str, Counter[str]] = {}
    if not datei.is_file():
        return läufe
    for zeile in datei.read_text(encoding="utf-8").splitlines():
        if zeile.strip():
            eintrag = json.loads(zeile)
            läufe.setdefault(eintrag["phase"], Counter())[eintrag["rolle"]] += 1
    return läufe


def alterInTagen(wurzel: Path, anliegen: Anliegen, heute: date) -> int:
    """Tage seit dem Commit, der die Datei angelegt hat; 0, wenn sie noch nicht committet ist."""
    ausgabe = gitAusgabe(
        wurzel, "log", "--diff-filter=A", "--format=%aI", "--", str(anliegen.datei)
    ).split()
    if not ausgabe:
        return 0
    return (heute - datetime.fromisoformat(ausgabe[-1]).date()).days


def offeneAnliegenJeRolle(wurzel: Path, heute: date) -> dict[str, list[tuple[int, int]]]:
    """Rolle → (Nummer, Alter in Tagen) der Anliegen, bei denen sie dran ist."""
    jeRolle: dict[str, list[tuple[int, int]]] = {}
    for anliegen in gelesene(wurzel):
        rolle = wartetAuf(anliegen)
        if rolle:
            jeRolle.setdefault(rolle, []).append(
                (anliegen.nummer, alterInTagen(wurzel, anliegen, heute))
            )
    return jeRolle


def kennzahlen(wurzel: Path, heute: date) -> str:
    zeilen = ["Rollenläufe je Phase und Rolle"]
    for phase, rollen in sorted(rollenläufeJePhaseUndRolle(wurzel).items()):
        verteilung = ", ".join(f"{rolle} {anzahl}" for rolle, anzahl in sorted(rollen.items()))
        zeilen.append(f"- {phase}: {sum(rollen.values())} ({verteilung})")
    zeilen.append("Offene Anliegen je Rolle, die dran ist (Nummer, Alter in Tagen)")
    for rolle, anliegen in sorted(offeneAnliegenJeRolle(wurzel, heute).items()):
        liste = ", ".join(f"{nummer:02d} ({alter} T)" for nummer, alter in sorted(anliegen))
        zeilen.append(f"- {rolle}: {len(anliegen)}: {liste}")
    return "\n".join(zeilen)


if __name__ == "__main__":
    print(kennzahlen(projektordner(), datetime.now(UTC).date()))
