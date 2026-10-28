import hashlib
import re
from pathlib import Path

from gemeinsam.pfade import handoffOrdner
from lesen.plan import zyklus

merkzettelOrdner = Path(".git") / "arbiter"
merkzettelName = "planFassung.txt"
anliegenLink = re.compile(r"\[[^\]]*\]\((?:\.\./)?(?:handoff/)?anliegen/(\d+)-[^)\s]*\)")
abschnittNachDemPlan = re.compile(r"^## (?:Fortschritt|Freigabe)", re.MULTILINE)


def fassungVon(wurzel: Path, zyklusNummer: int) -> str | None:
    plan = wurzel / handoffOrdner / "plan.md"
    if not plan.is_file() or zyklus(plan) != zyklusNummer:
        return None
    text = plan.read_text(encoding="utf-8")
    ende = abschnittNachDemPlan.search(text)
    inhalt = text[: ende.start()] if ende else text
    inhalt = anliegenLink.sub(r"Anliegen \1", inhalt)
    return f"{zyklusNummer}:{hashlib.sha256(inhalt.encode('utf-8')).hexdigest()}"


def neuGefasst(wurzel: Path, zyklusNummer: int) -> bool:
    fassung = fassungVon(wurzel, zyklusNummer)
    zettel = wurzel / merkzettelOrdner / merkzettelName
    if fassung is None or not (wurzel / ".git").is_dir():
        return False
    gemerkt = zettel.read_text(encoding="utf-8") if zettel.is_file() else None
    if gemerkt != fassung:
        zettel.parent.mkdir(parents=True, exist_ok=True)
        zettel.write_text(fassung, encoding="utf-8")
    return gemerkt is not None and gemerkt.startswith(f"{zyklusNummer}:") and gemerkt != fassung
