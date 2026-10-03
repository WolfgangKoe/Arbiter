"""Fällige Kritik am Code (`prozess/ablauf.md`, Kritik am Code), für den Stand.

Ein Commit, der Code ändert, braucht den Kritiker der Tabelle. Seine Kritik ist ein Commit,
dessen Betreff `Kritik <kurzer Hash>` des geprüften Commits enthält. Geprüft werden die
Commits seit der letzten Freigabe; der Stand meldet den ersten ohne Kritik.
"""

import re
from pathlib import Path

from gitAufruf import gitAusgabe

kritikerJePfad = (
    ("technik/tests/akzeptanz/", "Fachkritiker und Architekt"),
    ("technik/arbiter/", "Reviewer"),
    ("technik/tests/einheit/", "Reviewer"),
    ("prozess/pruefungen/", "Reviewer"),
    (".claude/settings.json", "Reviewer"),
    ("pyproject.toml", "Architekt und Reviewer"),
    ("ruff.toml", "Architekt und Reviewer"),
)
kritikImBetreff = re.compile(r"\bKritik ([0-9a-f]{7,40})\b")


def kritikerDesCommits(geändertePfade: list[str]) -> str | None:
    for präfix, kritiker in kritikerJePfad:
        if any(pfad.startswith(präfix) for pfad in geändertePfade):
            return kritiker
    return None


def commitsSeitDerFreigabe(wurzel: Path) -> list[tuple[str, str]]:
    """Kennung und Betreff, älteste zuerst, ab dem Commit nach der letzten Freigabe."""
    commits = []
    for zeile in gitAusgabe(wurzel, "log", "--format=%H %s").splitlines():
        kennung, _, betreff = zeile.partition(" ")
        if betreff.startswith("Freigabe "):
            break
        commits.append((kennung, betreff))
    return commits[::-1]


def ersteFälligeKritik(wurzel: Path) -> tuple[str, str] | None:
    """Kurzer Hash und Kritiker des ersten Code-Commits ohne Kritik."""
    commits = commitsSeitDerFreigabe(wurzel)
    geprüft = {
        treffer[1] for _, betreff in commits for treffer in kritikImBetreff.finditer(betreff)
    }
    for kennung, betreff in commits:
        if kritikImBetreff.search(betreff):
            continue
        pfade = gitAusgabe(wurzel, "show", "--format=", "--name-only", kennung).splitlines()
        kritiker = kritikerDesCommits(pfade)
        if kritiker and not any(kennung.startswith(hash) for hash in geprüft):
            return kennung[:7], kritiker
    return None


def fälligeKritikAlsText(wurzel: Path) -> str:
    fällig = ersteFälligeKritik(wurzel)
    return f"Kritik am Code fällig: {fällig[1]} ({fällig[0]})" if fällig else ""
