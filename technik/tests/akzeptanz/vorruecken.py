import pytest

from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle
from tests.akzeptanz.grenzen import stelleNurImGrenzkreisDesWurfs
from tests.akzeptanz.handgriffe import modellZurEbeneMachen
from tests.akzeptanz.schlacht import jetzigeStellen


def ganzeEinheitAuswählen(schlacht, einheit: Einheit) -> dict[Modell, Stelle]:
    schlacht.auswählen(einheit)
    return jetzigeStellen(schlacht, einheit)


def letztesModellZurEbeneMachen(schlacht, einheit: Einheit) -> dict[Modell, Stelle]:
    *_, letztes = einheit.modelle
    modellZurEbeneMachen(schlacht, einheit, letztes)
    return {letztes: schlacht.stelle(letztes)}


ebenen = {"ganzeEinheit": ganzeEinheitAuswählen, "einModell": letztesModellZurEbeneMachen}
mitJederEbene = pytest.mark.parametrize("ebene", list(ebenen), ids=list(ebenen))


def wartetAufDenVorrückwurf(schlacht, einheit: Einheit, ebene: str) -> dict[Modell, Stelle]:
    stellen = ebenen[ebene](schlacht, einheit)
    schlacht.vorrücken()
    return stellen


def vorgerücktMit(
    schlacht, einheit: Einheit, wurf: int, ebene: str = "ganzeEinheit"
) -> dict[Modell, Stelle]:
    stellen = wartetAufDenVorrückwurf(schlacht, einheit, ebene)
    schlacht.karteAnklicken(stelleNurImGrenzkreisDesWurfs(schlacht, einheit, wurf))
    return stellen
