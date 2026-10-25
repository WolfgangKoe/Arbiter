"""Merkt sich die Fassung des Plans, damit ein neu gefasster Plan seine Kritik wieder öffnet."""

import hashlib
import re
from pathlib import Path

from gemeinsam.pfade import handoffOrdner
from lesen.plan import zyklus

merkzettelOrdner = Path(".git") / "arbiter"
merkzettelName = "planFassung.txt"
abschnittNachDemPlan = re.compile(r"^## (?:Fortschritt|Freigabe)", re.MULTILINE)


def fassungVon(wurzel: Path, zyklusNummer: int) -> str | None:
    """Zyklus und Prüfsumme des Plans ohne Fortschritt und Freigabe; `None` ohne diesen Plan."""
    plan = wurzel / handoffOrdner / "plan.md"
    if not plan.is_file() or zyklus(plan) != zyklusNummer:
        return None
    text = plan.read_text(encoding="utf-8")
    ende = abschnittNachDemPlan.search(text)
    inhalt = text[: ende.start()] if ende else text
    return f"{zyklusNummer}:{hashlib.sha256(inhalt.encode('utf-8')).hexdigest()}"


def neuGefasst(wurzel: Path, zyklusNummer: int) -> bool:
    """Der Plan dieses Zyklus unterscheidet sich von der Fassung, die zuletzt gemerkt wurde."""
    fassung = fassungVon(wurzel, zyklusNummer)
    zettel = wurzel / merkzettelOrdner / merkzettelName
    if fassung is None or not (wurzel / ".git").is_dir():
        return False
    gemerkt = zettel.read_text(encoding="utf-8") if zettel.is_file() else None
    if gemerkt != fassung:
        zettel.parent.mkdir(parents=True, exist_ok=True)
        zettel.write_text(fassung, encoding="utf-8")
    return gemerkt is not None and gemerkt.startswith(f"{zyklusNummer}:") and gemerkt != fassung
