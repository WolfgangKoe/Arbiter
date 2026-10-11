"""AUF-14 · Rest einer Einheit."""

import pytest

from tests.akzeptanz.handgriffe import modelleSetzen, stelleInDerZoneVon


@pytest.mark.parametrize("gesetzt", [1, 9], ids=["einsGesetzt", "nurEinsFehlt"])
def testAuf14_1EineEinheitMitGesetztemUndNichtGesetztemModellBekommtGenauEinModellDazu(
    aufstellungNachDerZonenwahl, boyz, spielerEins, gesetzt
):
    davor = modelleSetzen(aufstellungNachDerZonenwahl, boyz, gesetzt)
    gesetzteModelle = {modell for modell, _ in davor}
    stelleDesLoslassens = stelleInDerZoneVon(aufstellungNachDerZonenwahl, spielerEins, 8, 50)

    aufstellungNachDerZonenwahl.einheitLoslassen(boyz, stelleDesLoslassens)

    danach = {modell for modell in boyz.modelle if aufstellungNachDerZonenwahl.gesetzt(modell)}
    (neuesModell,) = danach - gesetzteModelle
    assert gesetzteModelle < danach
    assert aufstellungNachDerZonenwahl.stelle(neuesModell) == stelleDesLoslassens
    assert all(aufstellungNachDerZonenwahl.stelle(modell) == stelle for modell, stelle in davor)
