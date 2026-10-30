import pytest

from arbiter.web.kennungen import kennungenDerEinheit
from tests.akzeptanz.handgriffe import aufstellungVon, spielerMit


def testEineEinheitAußerhalbDerAufstellungIstEineVorbedingungsverletzung():
    aufstellung = aufstellungVon(spielerMit(1), spielerMit(1))
    fremderSpieler = spielerMit(1)
    (fremdeEinheit,) = fremderSpieler.armee.einheiten

    with pytest.raises(ValueError):
        kennungenDerEinheit(aufstellung, fremdeEinheit)
