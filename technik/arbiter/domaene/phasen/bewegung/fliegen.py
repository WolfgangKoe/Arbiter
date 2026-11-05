from collections.abc import Mapping
from dataclasses import dataclass, field
from fractions import Fraction
from functools import partial

from arbiter.domaene import messen
from arbiter.domaene.messen import Geradenrand, Kreisrand, Rand
from arbiter.domaene.querschnitt.setzen import inNahkampfreichweite, nahkampfreichweite
from arbiter.domaene.spielobjekte import Modell, Spielfeld, Stelle

type Stellen = Mapping[Modell, Stelle]


@dataclass(frozen=True)
class Weite:
    anfang: Stelle
    zoll: Fraction


@dataclass(frozen=True)
class Umgebung:
    fremde: Stellen
    gegner: Stellen
    spielfeld: Spielfeld
    weiten: Mapping[Modell, Weite] = field(default_factory=dict)


def anteilBisZurNahkampfreichweite(
    vorige: Stellen, weg: messen.Weg, gegner: Stellen, ende: Fraction
) -> Fraction:
    bewegte = [(modell.base, stelle) for modell, stelle in vorige.items()]
    hindernisse = [(modell.base, stelle) for modell, stelle in gegner.items()]
    inReichweite = partial(messen.abstandHöchstens, zoll=nahkampfreichweite)
    return messen.anteilVorDerLetztenBerührung(bewegte, hindernisse, weg, ende, inReichweite)


def nachFremdenBasesGerückt(gesetzt: Stellen, zurück: messen.Weg, umgebung: Umgebung) -> Stellen:
    if not _überdecktFremde(gesetzt, umgebung):
        return gesetzt
    weg = messen.wegInDieFreieFläche(
        _ränder(gesetzt, umgebung), partial(_frei, gesetzt, umgebung), zurück
    )
    if weg is None:
        return gesetzt
    return {modell: messen.verschoben(stelle, weg) for modell, stelle in gesetzt.items()}


def _hindernisse(umgebung: Umgebung) -> Stellen:
    return {**umgebung.fremde, **umgebung.gegner}


def _überdecktFremde(stellen: Stellen, umgebung: Umgebung) -> bool:
    return any(
        messen.überdecken(modell.base, stelle, hindernis.base, ort)
        for modell, stelle in stellen.items()
        for hindernis, ort in _hindernisse(umgebung).items()
    )


def _frei(gesetzt: Stellen, umgebung: Umgebung, weg: messen.Weg) -> bool:
    verschoben = {modell: messen.verschoben(stelle, weg) for modell, stelle in gesetzt.items()}
    breite, länge = umgebung.spielfeld.seitenlängen
    grenzenInX, grenzenInY = (Fraction(0), breite), (Fraction(0), länge)
    return not _überdecktFremde(verschoben, umgebung) and all(
        messen.ganzIn(modell.base, stelle, grenzenInX, grenzenInY)
        and not inNahkampfreichweite(modell, stelle, umgebung.gegner, eigene=())
        and _inDerWeite(umgebung.weiten.get(modell), stelle)
        for modell, stelle in verschoben.items()
    )


def _inDerWeite(weite: Weite | None, stelle: Stelle) -> bool:
    return weite is None or messen.abstandImQuadrat(weite.anfang, stelle) <= weite.zoll**2


def _ränder(gesetzt: Stellen, umgebung: Umgebung) -> list[Rand]:
    ränder: list[Rand] = []
    for modell, stelle in gesetzt.items():
        ränder.extend(_gemiedeneKreise(modell, stelle, umgebung))
        ränder.extend(_randDesSpielfelds(modell, stelle, umgebung.spielfeld))
        weite = umgebung.weiten.get(modell)
        if weite is not None:
            ränder.append(_kreisDerWeite(stelle, weite))
    return ränder


def _gemiedeneKreise(modell: Modell, stelle: Stelle, umgebung: Umgebung) -> list[Rand]:
    return [
        Kreisrand(
            mitte=(float(ort.x - stelle.x), float(ort.y - stelle.y)),
            radius=float(_gemiedenerRadius(modell, hindernis, umgebung)),
            darin=False,
        )
        for hindernis, ort in _hindernisse(umgebung).items()
    ]


def _gemiedenerRadius(modell: Modell, hindernis: Modell, umgebung: Umgebung) -> Fraction:
    radien = messen.radiusInZoll(modell.base) + messen.radiusInZoll(hindernis.base)
    return radien + nahkampfreichweite if hindernis in umgebung.gegner else radien


def _randDesSpielfelds(modell: Modell, stelle: Stelle, spielfeld: Spielfeld) -> list[Rand]:
    breite, länge = spielfeld.seitenlängen
    radius = messen.radiusInZoll(modell.base)
    return [
        Geradenrand(inX=True, wert=float(radius - stelle.x), aufwärts=True),
        Geradenrand(inX=True, wert=float(breite - radius - stelle.x), aufwärts=False),
        Geradenrand(inX=False, wert=float(radius - stelle.y), aufwärts=True),
        Geradenrand(inX=False, wert=float(länge - radius - stelle.y), aufwärts=False),
    ]


def _kreisDerWeite(stelle: Stelle, weite: Weite) -> Kreisrand:
    return Kreisrand(
        mitte=(float(weite.anfang.x - stelle.x), float(weite.anfang.y - stelle.y)),
        radius=float(weite.zoll),
        darin=True,
    )
