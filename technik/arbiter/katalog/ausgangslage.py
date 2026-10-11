"""Die Ausgangslage aus den YAML-Dateien in `domaene/daten/` (MIV-1)."""

from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path
from types import MappingProxyType

import yaml

from arbiter.domaene.missionsvorbereitung.ausgangslage import Aufstellungszone, Ausgangslage
from arbiter.domaene.phasen.aufstellen.ziehen import Formation
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
    return ausgangslageAus(
        _laden("ausgangslage.yaml"), _laden("onlyWar.yaml"), _laden("formation.yaml")
    )


def _formationenLesen(formation: dict) -> Mapping[str, Formation]:
    abstand = Fraction(str(formation["abstand"]))
    return MappingProxyType(
        {
            name: Formation(reihen=tuple(reihen), abstand=abstand)
            for name, reihen in formation["formation"].items()
        }
    )


def _formationenPrüfen(armee: Armee, formationen: Mapping[str, Formation]) -> None:
    for einheit in armee.einheiten:
        formation = formationen.get(einheit.name)
        if formation is None:
            raise ValueError(f"Die Einheit {einheit.name} hat keine Formation")
        if sum(formation.reihen) != len(einheit.modelle):
            raise ValueError(f"Die Reihen der Formation von {einheit.name} zählen andere Modelle")


def ausgangslageAus(ausgangslage: dict, onlyWar: dict, formation: dict) -> Ausgangslage:
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
    formationen = _formationenLesen(formation)
    ersterSpieler = Spieler(armee=_armeeLesen(ersteArmee))
    zweiterSpieler = Spieler(armee=_armeeLesen(zweiteArmee))
    _formationenPrüfen(ersterSpieler.armee, formationen)
    _formationenPrüfen(zweiterSpieler.armee, formationen)
    return Ausgangslage(
        ersterSpieler=ersterSpieler,
        zweiterSpieler=zweiterSpieler,
        spielfeld=Spielfeld(seitenlängen=(Fraction(breite), Fraction(länge))),
        tiefen=MappingProxyType(tiefen),
        formationen=formationen,
    )
