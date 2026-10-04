"""Fällige Kritik am Code für den Stand."""

import re
from pathlib import Path
from typing import NamedTuple

from gitAufruf import gitAusgabe, letzteFreigabe
from pfade import akzeptanzOrdner

kritikerJePfad = (
    (f"{akzeptanzOrdner}/", ("Fachkritiker", "Architekt")),
    ("technik/arbiter/", ("Reviewer",)),
    ("technik/tests/einheit/", ("Reviewer",)),
    ("prozess/pruefungen/", ("Reviewer",)),
    (".claude/settings.json", ("Reviewer",)),
    ("pyproject.toml", ("Architekt", "Reviewer")),
    ("ruff.toml", ("Architekt", "Reviewer")),
)
kurzerHash = re.compile(r"\b[0-9a-f]{7,40}\b")


class Commit(NamedTuple):
    kennung: str
    betreff: str


class FälligeKritik(NamedTuple):
    kurzerHash: str
    kritiker: str


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


def commitsSeitDerFreigabe(wurzel: Path) -> list[Commit]:
    """Kennung und Betreff, älteste zuerst, ab dem Commit nach der letzten Freigabe."""
    freigabe = letzteFreigabe(wurzel)
    bereich = [f"{freigabe}..HEAD"] if freigabe else []
    zeilen = gitAusgabe(wurzel, "log", "--format=%H %s", *bereich).splitlines()
    commits = []
    for zeile in reversed(zeilen):
        kennung, _, betreff = zeile.partition(" ")
        commits.append(Commit(kennung, betreff))
    return commits


def ersteFälligeKritik(wurzel: Path) -> FälligeKritik | None:
    """Kurzer Hash und Kritiker des ersten Code-Commits ohne Kritik."""
    commits = commitsSeitDerFreigabe(wurzel)
    geprüft = {hash for commit in commits for hash in geprüfteHashes(commit.betreff)}
    for commit in commits:
        kennung = commit.kennung
        pfade = gitAusgabe(wurzel, "show", "--format=", "--name-only", kennung).splitlines()
        kritiker = kritikerDesCommits(pfade)
        if kritiker and not any(kennung.startswith(hash) for hash in geprüft):
            return FälligeKritik(kennung[:7], kritiker)
    return None


def fälligeKritikAlsText(wurzel: Path) -> str:
    fällig = ersteFälligeKritik(wurzel)
    return f"Kritik am Code fällig: {fällig.kritiker} ({fällig.kurzerHash})" if fällig else ""
