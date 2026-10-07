"""Ordner des Repos und Pfade, die mehrere Prüfungen kennen."""

import os
from pathlib import Path

wurzel = Path(__file__).resolve().parents[3]

perspektiven = ("domaene", "technik", "prozess")
akzeptanzOrdner = "technik/tests/akzeptanz"
anforderungsOrdner = "domaene/anforderungen"
handoffOrdner = "handoff"
anliegenOrdner = f"{handoffOrdner}/anliegen"
frontendOrdner = "technik/frontend"
webOrdner = "technik/arbiter/web"
etappenOrdner = "domaene/etappen"
itemsOrdner = "domaene/items"

nurLesbar = ("VORGEHEN.md", f"{handoffOrdner}/kritik-entwickler.md", "Arbiter-old/", "ArbiterMap/")
# Warum: Ordner unter `nurLesbar` (Eintrag mit `/` am Ende) sind der Altbestand; ihn prüft nichts.
altbestandOrdner = tuple(eintrag.rstrip("/") for eintrag in nurLesbar if eintrag.endswith("/"))


def projektordner() -> Path:
    """Das Repo: `CLAUDE_PROJECT_DIR`, sonst die Wurzel nach dem Ort der Prüfskripte."""
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or wurzel).resolve()


def relativZurWurzel(pfad: Path, ordner: Path) -> str | None:
    """Der Pfad mit `/` ab `ordner` (relative Pfade gelten ab dort); `None` außerhalb."""
    absolut = pfad if pfad.is_absolute() else ordner / pfad
    try:
        return absolut.resolve().relative_to(ordner.resolve()).as_posix()
    except ValueError:
        return None


def istNurLesbar(relativerPfad: str) -> bool:
    """Für alle Rollen und den Koordinator nur lesbar; löschen tut nur der Stakeholder."""
    return any(
        f"{relativerPfad.rstrip('/')}/".startswith(eintrag)
        if eintrag.endswith("/")
        else relativerPfad == eintrag
        for eintrag in nurLesbar
    )
