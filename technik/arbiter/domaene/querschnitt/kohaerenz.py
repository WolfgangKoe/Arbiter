"""Die Kohärenz einer Einheit (QUE-4)."""

from collections.abc import Mapping
from fractions import Fraction

from arbiter.domaene import messen
from arbiter.domaene.spielobjekte import Modell, Stelle

# Regel: QUE-4.2, Kohärenz heißt ein Abstand von höchstens 2″ (core_rules.txt:434)
_kohärenzabstand = Fraction(2)
_größteEinheitMitEinemPartner = 5


# Regel: QUE-4, die gesetzten Modelle einer Einheit stehen beisammen (core_rules.txt:434)
def inKohärenz(stellen: Mapping[Modell, Stelle]) -> bool:
    if len(stellen) <= 1:
        return True
    partner = {
        modell: {
            anderes
            for anderes, andereStelle in stellen.items()
            if anderes is not modell
            and messen.abstandHöchstens(
                modell.base, stelle, anderes.base, andereStelle, _kohärenzabstand
            )
        }
        for modell, stelle in stellen.items()
    }
    verlangt = 1 if len(stellen) <= _größteEinheitMitEinemPartner else 2
    return all(len(gefundene) >= verlangt for gefundene in partner.values()) and _zusammenhängend(
        partner
    )


def _zusammenhängend(partner: Mapping[Modell, set[Modell]]) -> bool:
    start, *_ = partner
    erreicht = {start}
    offen = [start]
    while offen:
        aktuelles = offen.pop()
        neue = partner[aktuelles] - erreicht
        erreicht |= neue
        offen.extend(neue)
    return len(erreicht) == len(partner)
