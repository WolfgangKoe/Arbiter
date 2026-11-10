import re
from pathlib import Path

from gemeinsam.pfade import etappenOrdner
from kriterienregeln.kriterium import Kriterium, anforderungZeile, kriteriumZeile, zeilen

etappeDerAnforderung = re.compile(r"^Etappe: (\d+)\s*$")
etappeAmSatzende = re.compile(r"\(Etappe (\d+)\)\s*$")


def laufendeEtappe(wurzel: Path) -> int | None:
    nummern = [
        int(datei.name.partition("-")[0])
        for datei in (wurzel / etappenOrdner).glob("*.md")
        if datei.name.partition("-")[0].isdigit()
    ]
    return min(nummern, default=None)


def gehörtZuSpäterer(wurzel: Path, anforderungsdatei: Path, kriterium: Kriterium) -> bool:
    laufend = laufendeEtappe(wurzel)
    etappe = etappeJeKriterium(anforderungsdatei).get(kriterium)
    return laufend is not None and etappe is not None and etappe > laufend


def etappeJeKriterium(anforderungsdatei: Path) -> dict[Kriterium, int | None]:
    ergebnis: dict[Kriterium, int | None] = {}
    vorgabe: int | None = None
    for zeile in zeilen(anforderungsdatei):
        if anforderungZeile.match(zeile):
            vorgabe = None
        if treffer := etappeDerAnforderung.match(zeile):
            vorgabe = int(treffer[1])
        if kriterium := kriteriumZeile.match(zeile):
            amSatzende = etappeAmSatzende.search(zeile)
            ergebnis[Kriterium.aus(kriterium)] = int(amSatzende[1]) if amSatzende else vorgabe
    return ergebnis
