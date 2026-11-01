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


Belegung = dict[Kriterium, tuple[int | None, bool]]


def belegungJeKriterium(wurzel: Path) -> Belegung:
    itemTexte = itemTexteDesFreigegebenenPlans(wurzel)
    etappen: dict[Kriterium, int | None] = {}
    for datei in sorted((wurzel / anforderungsOrdner).rglob("*.md")):
        etappen |= etappeJeKriterium(datei)
    ohneTest = {
        kriterium
        for fehlend in fehlendeTests(wurzel, itemTexte)
        for kriterium in fehlend.kriterien
    }
    return {
        kriterium: (nummer, kriterium not in ohneTest and not umfasst(itemTexte, kriterium))
        for kriterium, nummer in etappen.items()
    }


def zählen(belegung: Belegung, etappe: int | None) -> tuple[int, int]:
    gezählt = [belegt for nummer, belegt in belegung.values() if etappe in (None, nummer)]
    return sum(gezählt), len(gezählt)


def belegungAlsText(wurzel: Path, aktuell: Lage) -> str:
    belegung = belegungJeKriterium(wurzel)
    belegt, alle = zählen(belegung, None)
    text = f"{belegt} von {alle} Kriterien belegt"
    treffer = etappenüberschrift.match(aktuell.etappe)
    if not treffer:
        return text
    belegtInEtappe, alleInEtappe = zählen(belegung, int(treffer[1]))
    return f"{text}, davon Etappe {treffer[1]}: {belegtInEtappe} von {alleInEtappe}"


def produktstandAlsText(wurzel: Path, aktuell: Lage) -> str:
    treffer = etappenüberschrift.match(aktuell.etappe)
    etappe = aktuell.etappe
    if treffer:
        etappe = f"Etappe {treffer[1]} von {etappenzahl(wurzel)} ({treffer[2]})"
    return f"{etappe}, Zyklus {aktuell.zyklus}; {belegungAlsText(wurzel, aktuell)}"
