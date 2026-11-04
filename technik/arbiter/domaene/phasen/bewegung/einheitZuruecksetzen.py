from collections.abc import Mapping

from arbiter.domaene.querschnitt.setzen import gesetzteModelle
from arbiter.domaene.spielobjekte import Einheit, Modell, Stelle


def stehtNichtWieZuBeginn(
    einheit: Einheit, stellen: Mapping[Modell, Stelle], stellenZuBeginn: Mapping[Modell, Stelle]
) -> bool:
    return gesetzteModelle(einheit, stellen) != gesetzteModelle(einheit, stellenZuBeginn)
