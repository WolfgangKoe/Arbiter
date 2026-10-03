"""Kennzahlen für die Retro (`prozess/kennzahlen.md`): offene Anliegen je Rolle."""

from datetime import UTC, date, datetime
from pathlib import Path

from agenten import projektordner
from anliegen import Anliegen, gelesene, wartetAuf
from gitAufruf import gitAusgabe, letzteFreigabe


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
    freigabe = letzteFreigabe(wurzel)
    for anliegen in gelesene(wurzel):
        rolle = wartetAuf(wurzel, anliegen, freigabe)
        if rolle:
            jeRolle.setdefault(rolle, []).append(
                (anliegen.nummer, alterInTagen(wurzel, anliegen, heute))
            )
    return jeRolle


def kennzahlen(wurzel: Path, heute: date) -> str:
    zeilen = ["Offene Anliegen je Rolle, die dran ist (Nummer, Alter in Tagen)"]
    for rolle, anliegen in sorted(offeneAnliegenJeRolle(wurzel, heute).items()):
        liste = ", ".join(f"{nummer:02d} ({alter} T)" for nummer, alter in sorted(anliegen))
        zeilen.append(f"- {rolle}: {len(anliegen)}: {liste}")
    return "\n".join(zeilen)


if __name__ == "__main__":
    print(kennzahlen(projektordner(), datetime.now(UTC).date()))
