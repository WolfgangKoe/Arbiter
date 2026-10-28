import re
from pathlib import Path

from gemeinsam.pfade import anforderungsOrdner, etappenOrdner
from kriterienregeln.kriterienEtappe import etappeJeKriterium
from kriterienregeln.kriterium import Kriterium
from kriterienregeln.rueckverfolgung import fehlendeTests, itemTexteDesFreigegebenenPlans, umfasst
from standregeln.phasenfolge import Lage

etappenüberschrift = re.compile(r"Etappe\s+(\d+)\s*·\s*(.*)")


def etappenzahl(wurzel: Path) -> int:
    nummern = [
        int(datei.name.partition("-")[0])
        for datei in (wurzel / etappenOrdner).glob("*.md")
        if datei.name.partition("-")[0].isdigit()
    ]
    return max(nummern, default=0)


def kriterienZählen(wurzel: Path, etappe: int | None = None) -> tuple[int, int]:
    itemTexte = itemTexteDesFreigegebenenPlans(wurzel)
    alle: dict[Kriterium, int | None] = {}
    for datei in sorted((wurzel / anforderungsOrdner).rglob("*.md")):
        alle |= etappeJeKriterium(datei)
    gezählt = {kriterium for kriterium, nummer in alle.items() if etappe in (None, nummer)}
    fehlende = fehlendeTests(wurzel, itemTexte)
    ohneTest = {kriterium for fehlend in fehlende for kriterium in fehlend.kriterien}
    inItems = {kriterium for kriterium in gezählt if umfasst(itemTexte, kriterium)}
    return len(gezählt - ohneTest - inItems), len(gezählt)


def belegungAlsText(wurzel: Path, aktuell: Lage) -> str:
    belegt, alle = kriterienZählen(wurzel)
    text = f"{belegt} von {alle} Kriterien belegt"
    treffer = etappenüberschrift.match(aktuell.etappe)
    if not treffer:
        return text
    belegtInEtappe, alleInEtappe = kriterienZählen(wurzel, int(treffer[1]))
    return f"{text}, davon Etappe {treffer[1]}: {belegtInEtappe} von {alleInEtappe}"


def produktstandAlsText(wurzel: Path, aktuell: Lage) -> str:
    treffer = etappenüberschrift.match(aktuell.etappe)
    etappe = aktuell.etappe
    if treffer:
        etappe = f"Etappe {treffer[1]} von {etappenzahl(wurzel)} ({treffer[2]})"
    return f"{etappe}, Zyklus {aktuell.zyklus}; {belegungAlsText(wurzel, aktuell)}"
