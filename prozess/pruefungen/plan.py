"""Der Plan in `handoff/plan.md` und seine Items in `domaene/items/`."""

import re
from pathlib import Path

from gitAufruf import freigabeCommit
from pfade import itemsOrdner

planDatei = Path("handoff") / "plan.md"


def zyklus(datei: Path) -> int | None:
    if not datei.is_file():
        return None
    ersteZeile = datei.read_text(encoding="utf-8").partition("\n")[0]
    treffer = re.search(r"Zyklus\s+(\d+)", ersteZeile)
    return int(treffer.group(1)) if treffer else None


def offeneItems(wurzel: Path) -> list[str]:
    """Items des Plans (Links in `handoff/plan.md`), deren Datei in `domaene/items/` existiert."""
    plan = wurzel / planDatei
    if not plan.is_file():
        return []
    muster = rf"\]\(\.\./{re.escape(itemsOrdner)}/([^)#\s]+\.md)"
    links = re.findall(muster, plan.read_text(encoding="utf-8"))
    return [name for name in links if (wurzel / itemsOrdner / name).is_file()]


def freigegebenerPlan(wurzel: Path) -> int | None:
    """Nummer des Plans, wenn `Freigabe Plan <n>` committet ist, sonst `None`."""
    nummer = zyklus(wurzel / planDatei)
    if nummer is None or freigabeCommit(wurzel, "Plan", nummer) is None:
        return None
    return nummer


def offeneItemTexte(wurzel: Path) -> list[str]:
    """Texte der offenen Items des Plans."""
    return [
        (wurzel / itemsOrdner / name).read_text(encoding="utf-8") for name in offeneItems(wurzel)
    ]


def itemsOhneLink(wurzel: Path) -> bool:
    """Der Plan hat einen Abschnitt `## Item(s)`, aber keinen Link auf `domaene/items/`."""
    plan = wurzel / planDatei
    if not plan.is_file():
        return False
    text = plan.read_text(encoding="utf-8")
    nenntItems = re.search(r"^## Items?\s*$", text, flags=re.MULTILINE) is not None
    return nenntItems and f"](../{itemsOrdner}/" not in text
