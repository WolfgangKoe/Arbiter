"""Liest Angaben aus den Agentendefinitionen in `.claude/agents/`."""

from fnmatch import fnmatch
from pathlib import Path


def rollennamen(wurzel: Path) -> list[str]:
    return sorted(datei.stem for datei in (wurzel / ".claude" / "agents").glob("*.md"))


def kopfzeilen(agentTyp: str, wurzel: Path) -> list[str] | None:
    datei = wurzel / ".claude" / "agents" / f"{agentTyp}.md"
    if not datei.is_file():
        return None
    zeilen = datei.read_text(encoding="utf-8").splitlines()
    if not zeilen or zeilen[0].strip() != "---":
        return []
    ende = next(
        (nummer for nummer, zeile in enumerate(zeilen[1:], 1) if zeile.strip() == "---"),
        len(zeilen),
    )
    return zeilen[1:ende]


def schreibpfade(agentTyp: str, wurzel: Path) -> tuple[str, ...]:
    """Die Muster unter `schreibpfade:`; ohne Eintrag darf die Rolle nichts schreiben."""
    zeilen = kopfzeilen(agentTyp, wurzel) or []
    muster: list[str] = []
    inListe = False
    for zeile in zeilen:
        if zeile.startswith("schreibpfade:"):
            inListe = True
        elif inListe and zeile.strip().startswith("- "):
            muster.append(zeile.strip()[2:].strip().strip('"'))
        elif inListe and zeile.strip():
            inListe = False
    return tuple(muster)


def darfSchreiben(relativerPfad: str, muster: tuple[str, ...]) -> bool:
    """Ein Muster mit `/` am Ende erlaubt den ganzen Ordner, sonst gilt `fnmatch`."""
    return any(
        relativerPfad.startswith(eintrag)
        if eintrag.endswith("/")
        else fnmatch(relativerPfad, eintrag)
        for eintrag in muster
    )
