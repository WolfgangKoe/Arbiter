import re
from pathlib import Path

from kriterienregeln.kriterium import Kriterium, anforderungZeile, kriteriumZeile, zeilen

etappeDerAnforderung = re.compile(r"^Etappe: (\d+)\s*$")
etappeAmSatzende = re.compile(r"\(Etappe (\d+)\)\s*$")


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
