"""Fällige Kritik am Code (`prozess/ablauf.md`, Kritik am Code), für den Stand.

Ein Commit, der Code ändert, braucht die Kritiker der Tabelle, alle getroffenen. Kritik ist ein
Commit, dessen Betreff mit `Kritik ` beginnt und die kurzen Hashes der geprüften Commits nennt
(`Kritik <a> <b>`). Jeder andere Commit, der Code ändert, wird geprüft, auch einer, dessen
Betreff „Kritik“ enthält. Geprüft werden die Commits seit der letzten Freigabe; der Stand
meldet den ersten ohne Kritik.
"""

import re
from pathlib import Path

from gitAufruf import gitAusgabe

kritikerJePfad = (
    ("technik/tests/akzeptanz/", ("Fachkritiker", "Architekt")),
    ("technik/arbiter/", ("Reviewer",)),
    ("technik/tests/einheit/", ("Reviewer",)),
    ("prozess/pruefungen/", ("Reviewer",)),
    (".claude/settings.json", ("Reviewer",)),
    ("pyproject.toml", ("Architekt", "Reviewer")),
    ("ruff.toml", ("Architekt", "Reviewer")),
)
kurzerHash = re.compile(r"\b[0-9a-f]{7,40}\b")


def kritikerDesCommits(geändertePfade: list[str]) -> str | None:
    """Alle Kritiker der getroffenen Pfade, ohne Doppelte, in der Reihenfolge der Tabelle."""
    kritiker: list[str] = []
    for präfix, rollen in kritikerJePfad:
        if any(pfad.startswith(präfix) for pfad in geändertePfade):
            kritiker += [rolle for rolle in rollen if rolle not in kritiker]
    return " und ".join(kritiker) if kritiker else None


def geprüfteHashes(betreff: str) -> set[str]:
    """Die Hashes, die ein Kritik-Commit (`Kritik <a> <b> …`) nennt."""
    return set(kurzerHash.findall(betreff)) if betreff.startswith("Kritik ") else set()


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
    geprüft = {hash for _, betreff in commits for hash in geprüfteHashes(betreff)}
    for kennung, _ in commits:
        pfade = gitAusgabe(wurzel, "show", "--format=", "--name-only", kennung).splitlines()
        kritiker = kritikerDesCommits(pfade)
        if kritiker and not any(kennung.startswith(hash) for hash in geprüft):
            return kennung[:7], kritiker
    return None


def fälligeKritikAlsText(wurzel: Path) -> str:
    fällig = ersteFälligeKritik(wurzel)
    return f"Kritik am Code fällig: {fällig[1]} ({fällig[0]})" if fällig else ""
