"""Liest Angaben aus den Agentendefinitionen in `.claude/agents/`."""

from __future__ import annotations

import os
from fnmatch import fnmatch
from pathlib import Path


def projektordner() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()


def kopfzeilen(agent_typ: str, wurzel: Path) -> list[str] | None:
    datei = wurzel / ".claude" / "agents" / f"{agent_typ}.md"
    if not datei.is_file():
        return None
    zeilen = datei.read_text(encoding="utf-8").splitlines()
    if not zeilen or zeilen[0].strip() != "---":
        return []
    ende = next((i for i, z in enumerate(zeilen[1:], 1) if z.strip() == "---"), len(zeilen))
    return zeilen[1:ende]


def schreibpfade(agent_typ: str, wurzel: Path) -> tuple[str, ...]:
    """Die Muster unter `schreibpfade:`; ohne Eintrag darf die Rolle nichts schreiben."""
    zeilen = kopfzeilen(agent_typ, wurzel) or []
    muster: list[str] = []
    in_liste = False
    for zeile in zeilen:
        if zeile.startswith("schreibpfade:"):
            in_liste = True
        elif in_liste and zeile.strip().startswith("- "):
            muster.append(zeile.strip()[2:].strip().strip('"'))
        elif in_liste and zeile.strip():
            in_liste = False
    return tuple(muster)


def darf_schreiben(relativer_pfad: str, muster: tuple[str, ...]) -> bool:
    """Ein Muster mit `/` am Ende erlaubt den ganzen Ordner, sonst gilt `fnmatch`."""
    return any(
        relativer_pfad.startswith(m) if m.endswith("/") else fnmatch(relativer_pfad, m)
        for m in muster
    )
