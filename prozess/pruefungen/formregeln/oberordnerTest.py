import pytest

from formregeln.oberordner import unbekannteOrdner
from gemeinsam.pfade import wurzel


@pytest.mark.stand
def testJederOrdnerDerWurzelIstPerspektiveOderAltbestand():
    assert unbekannteOrdner(wurzel) == [], (
        "Neuer Ordner: Perspektive oder Altbestand? Eintragen in pfade.perspektiven "
        "oder agenten.nurLesbar"
    )


def testEinNeuerOrdnerIstRot(tmp_path):
    (tmp_path / "Neu").mkdir()
    assert unbekannteOrdner(tmp_path) == ["Neu"]


def testEinOrdnerMitPunktUndEinePerspektiveSindGrün(tmp_path):
    for name in (".probe", "domaene", "handoff"):
        (tmp_path / name).mkdir()
    assert unbekannteOrdner(tmp_path) == []


def testEinFehlenderAltbestandOrdnerIstGrün(tmp_path):
    assert unbekannteOrdner(tmp_path) == []
