from fractions import Fraction
from pathlib import Path
from types import MappingProxyType

import yaml

from arbiter.domaene.phasen.aufstellen import Aufstellungszone, Ausgangslage
from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell, Spieler, Spielfeld

_datenordner = Path(__file__).parents[3] / "domaene" / "daten"


def _laden(dateiname: str) -> dict:
    with (_datenordner / dateiname).open(encoding="utf-8") as datei:
        return yaml.safe_load(datei)


def _durchmesserLesen(zahl: object) -> int:
    # Warum: gerechnet wird mit ganzen mm (technik/architektur.md, S2)
    if type(zahl) is not int or zahl <= 0:
        raise ValueError(f"Der Durchmesser muss eine ganze Zahl über 0 in mm sein: {zahl!r}")
    return zahl


def _armeeLesen(einheiten: list[dict]) -> Armee:
    return Armee(
        einheiten=tuple(
            Einheit(
                name=eintrag["Einheit"],
                modelle=tuple(
                    Modell(base=Base(durchmesser=_durchmesserLesen(zahl)))
                    for zahl in eintrag["durchmesser"]
                ),
            )
            for eintrag in einheiten
        )
    )


def ausgangslageLaden() -> Ausgangslage:
    return ausgangslageAus(_laden("ausgangslage.yaml"), _laden("onlyWar.yaml"))


def ausgangslageAus(ausgangslage: dict, onlyWar: dict) -> Ausgangslage:
    ersteArmee, zweiteArmee = ausgangslage["Armee"]
    breite, länge = onlyWar["Spielfeld"]
    tiefen = {}
    for name, zone in onlyWar["Aufstellungszone"].items():
        # Regel: Die Zonen liegen an den langen Kanten, entlang der zweiten Seitenlänge (S1)
        if zone["Spielfeldkante"] != länge:
            raise ValueError(f"Die Zone {name} liegt nicht an einer Kante der Länge {länge}")
        if name not in Aufstellungszone.__members__:
            raise ValueError(f"Die Aufstellungszone {name} gibt es nicht")
        tiefen[Aufstellungszone[name]] = Fraction(zone["Tiefe"])
    if set(tiefen) != set(Aufstellungszone):
        raise ValueError("Jede Aufstellungszone braucht eine Tiefe")
    return Ausgangslage(
        ersterSpieler=Spieler(armee=_armeeLesen(ersteArmee)),
        zweiterSpieler=Spieler(armee=_armeeLesen(zweiteArmee)),
        spielfeld=Spielfeld(seitenlängen=(Fraction(breite), Fraction(länge))),
        tiefen=MappingProxyType(tiefen),
    )
