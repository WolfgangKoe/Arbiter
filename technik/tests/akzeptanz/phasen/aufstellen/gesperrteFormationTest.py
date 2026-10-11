"""AUF-15 · Gesperrte Formation."""

from tests.akzeptanz.handgriffe import eineGesperrteFormation


def testAuf15_1MitZurückIstKeinModellDerFormationGesetztOderGesperrt(
    aufstellungNachDerZonenwahl, boyz, warboss
):
    modellDesWarboss, *_ = warboss.modelle
    mitteDerZone = eineGesperrteFormation(aufstellungNachDerZonenwahl, (boyz, warboss))

    aufstellungNachDerZonenwahl.zurück()

    gesetzte = [modell for modell in boyz.modelle if aufstellungNachDerZonenwahl.gesetzt(modell)]
    gesperrte = [modell for modell in boyz.modelle if aufstellungNachDerZonenwahl.gesperrt(modell)]
    assert gesetzte == []
    assert gesperrte == []
    assert aufstellungNachDerZonenwahl.stelle(modellDesWarboss) == mitteDerZone
