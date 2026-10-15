"""Etappe und belegte Kriterien in Worten: die erste Angabe des Stands."""

import re
from pathlib import Path

from gemeinsam.pfade import anforderungsOrdner, etappenOrdner
from kriterienregeln.kriterium import Kriterium, kriterien
from kriterienregeln.rueckverfolgung import fehlendeTests, itemTexteDesFreigegebenenPlans, umfasst
from standregeln.phasenfolge import Lage

etappenüberschrift = re.compile(r"Etappe\s+(\d+)\s*·\s*(.*)")


def etappenzahl(wurzel: Path) -> int:
    """Die größte Nummer in `domaene/etappen/`."""
    nummern = [
        int(datei.name.partition("-")[0])
        for datei in (wurzel / etappenOrdner).glob("*.md")
        if datei.name.partition("-")[0].isdigit()
    ]
    return max(nummern, default=0)


def kriterienZählen(wurzel: Path) -> tuple[int, int]:
    """Belegte und alle Kriterien: belegt hat einen Test und steht in keinem offenen Item."""
    itemTexte = itemTexteDesFreigegebenenPlans(wurzel)
    alle: set[Kriterium] = set()
    for datei in sorted((wurzel / anforderungsOrdner).rglob("*.md")):
        alle |= kriterien(datei)
    fehlende = fehlendeTests(wurzel, itemTexte)
    ohneTest = {kriterium for fehlend in fehlende for kriterium in fehlend.kriterien}
    inItems = {kriterium for kriterium in alle if umfasst(itemTexte, kriterium)}
    return len(alle - ohneTest - inItems), len(alle)


def produktstandAlsText(wurzel: Path, aktuell: Lage) -> str:
    """„Etappe 1 von 7 (Aufstellen), Zyklus 5; 74 von 94 Kriterien belegt“."""
    belegt, alle = kriterienZählen(wurzel)
    treffer = etappenüberschrift.match(aktuell.etappe)
    etappe = aktuell.etappe
    if treffer:
        etappe = f"Etappe {treffer[1]} von {etappenzahl(wurzel)} ({treffer[2]})"
    return f"{etappe}, Zyklus {aktuell.zyklus}; {belegt} von {alle} Kriterien belegt"
