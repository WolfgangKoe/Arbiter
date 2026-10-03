"""Löscht erledigte, committete Anliegen; Links darauf werden zu „Anliegen <nr>“."""

import re
import sys
from pathlib import Path

from agenten import istNurLesbar, projektordner
from anliegen import anliegenDateien, kopfLesen
from gitAufruf import gitAusgabe

link = re.compile(r"\[[^\]]*\]\(([^)\s#]+)(?:#[^)\s]*)?\)")
suchOrdner = ("domaene", "technik", "prozess", "handoff", ".claude", "doku")


def markdownDateien(wurzel: Path) -> list[Path]:
    dateien = [wurzel / "CLAUDE.md"]
    for ordner in suchOrdner:
        dateien += sorted((wurzel / ordner).rglob("*.md"))
    return [
        datei
        for datei in dateien
        if datei.is_file() and not istNurLesbar(datei.relative_to(wurzel).as_posix())
    ]


def linksErsetzen(wurzel: Path, gelöscht: dict[Path, str]) -> list[str]:
    """Ersetzt Links auf gelöschte Anliegen durch „Anliegen <nr>“; nennt die geänderten Dateien."""
    geändert = []
    for datei in markdownDateien(wurzel):
        text = datei.read_text(encoding="utf-8")

        def ersetzen(treffer: re.Match, datei: Path = datei) -> str:
            ziel = (datei.parent / treffer[1]).resolve()
            return f"Anliegen {gelöscht[ziel]}" if ziel in gelöscht else treffer[0]

        neu = link.sub(ersetzen, text)
        if neu != text:
            datei.write_text(neu, encoding="utf-8")
            geändert.append(datei.relative_to(wurzel).as_posix())
    return geändert


def erledigteLöschen(wurzel: Path) -> list[str]:
    """Löscht erledigte Anliegen, die unverändert im letzten Commit stehen; nennt die Dateinamen."""
    gelöscht: dict[Path, str] = {}
    # Warum: `ls-files` nennt den Index; `ls-tree HEAD` nennt, was git sicher bewahrt.
    bekannt = set(
        gitAusgabe(
            wurzel, "ls-tree", "-r", "--name-only", "HEAD", "--", "handoff/anliegen"
        ).splitlines()
    )
    geändert = set(
        gitAusgabe(wurzel, "diff", "--name-only", "HEAD", "--", "handoff/anliegen").splitlines()
    )
    for datei in anliegenDateien(wurzel):
        gelesen = kopfLesen(datei)
        if gelesen is None or gelesen.status != "erledigt":
            continue
        pfad = datei.relative_to(wurzel).as_posix()
        if pfad in bekannt and pfad not in geändert:
            datei.unlink()
            gelöscht[datei.resolve()] = f"{gelesen.nummer:02d}"
    if gelöscht:
        linksErsetzen(wurzel, gelöscht)
    return [datei.name for datei in gelöscht]


if __name__ == "__main__":
    for name in erledigteLöschen(projektordner()):
        print(f"Anliegen {name} war erledigt und ist gelöscht.")
    sys.exit(0)
