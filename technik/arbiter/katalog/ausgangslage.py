from fractions import Fraction
from pathlib import Path

import yaml

from arbiter.domaene.phasen.aufstellen import Ausgangslage
from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell, Spieler, Spielfeld

_datenordner = Path(__file__).parents[3] / "domaene" / "daten"


def _laden(dateiname: str) -> dict:
    with (_datenordner / dateiname).open(encoding="utf-8") as datei:
        return yaml.safe_load(datei)


def _armeeLesen(einheiten: list[dict]) -> Armee:
    return Armee(
        einheiten=tuple(
            Einheit(
                modelle=tuple(
                    Modell(base=Base(durchmesser=zahl)) for zahl in eintrag["durchmesser"]
                )
            )
            for eintrag in einheiten
        )
    )


def ausgangslageLaden() -> Ausgangslage:
    ausgangslage = _laden("ausgangslage.yaml")
    onlyWar = _laden("onlyWar.yaml")
    ersteArmee, zweiteArmee = ausgangslage["Armee"]
    breite, länge = onlyWar["Spielfeld"]
    zonen = onlyWar["Aufstellungszone"]
    return Ausgangslage(
        ersterSpieler=Spieler(armee=_armeeLesen(ersteArmee)),
        zweiterSpieler=Spieler(armee=_armeeLesen(zweiteArmee)),
        spielfeld=Spielfeld(seitenlängen=(Fraction(breite), Fraction(länge))),
        tiefen=(Fraction(zonen["erste"]["Tiefe"]), Fraction(zonen["zweite"]["Tiefe"])),
    )
