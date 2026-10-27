"""Die Ausgangslage aus den YAML-Dateien in `domaene/daten/` (MIV-1)."""

from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path
from types import MappingProxyType

import yaml

from arbiter.domaene.missionsvorbereitung.ausgangslage import (
    Aufstellungszone,
    Ausgangslage,
    Formation,
)
from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell, Spieler, Spielfeld

_datenordner = Path(__file__).parents[3] / "domaene" / "daten"


def _laden(dateiname: str) -> dict:
    with (_datenordner / dateiname).open(encoding="utf-8") as datei:
        return yaml.safe_load(datei)


def _ganzeZahlÜberNull(zahl: object, was: str) -> int:
    if type(zahl) is not int or zahl <= 0:
        raise ValueError(f"{was} muss eine ganze Zahl über 0 sein: {zahl!r}")
    return zahl


def _durchmesserLesen(zahl: object) -> int:
    return _ganzeZahlÜberNull(zahl, "Der Durchmesser in mm")


def _bewegungsweiteLesen(zahl: object) -> Fraction:
    return Fraction(_ganzeZahlÜberNull(zahl, "Die Bewegungsweite in Zoll"))


def _armeeLesen(einheiten: list[dict]) -> Armee:
    return Armee(
        einheiten=tuple(
            Einheit(
                name=eintrag["Einheit"],
                modelle=tuple(
                    Modell(
                        base=Base(durchmesser=_durchmesserLesen(zahl)),
                        bewegungsweite=_bewegungsweiteLesen(eintrag["bewegungsweite"]),
                    )
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
            name: Formation(
                reihen=tuple(_ganzeZahlÜberNull(reihe, "Die Reihe") for reihe in reihen),
                abstand=abstand,
            )
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
        if len({modell.base.durchmesser for modell in einheit.modelle}) > 1:
            raise ValueError(f"Die Modelle von {einheit.name} haben verschiedene Durchmesser")


def ausgangslageAus(ausgangslage: dict, onlyWar: dict, formation: dict) -> Ausgangslage:
    ersteArmee, zweiteArmee = ausgangslage["Armee"]
    breite, länge = onlyWar["Spielfeld"]
    tiefen = {}
    for name, zone in onlyWar["Aufstellungszone"].items():
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
        letzteSchlachtrunde=_ganzeZahlÜberNull(
            onlyWar["Schlacht"]["schlachtrunde"], "Die letzte Schlachtrunde"
        ),
    )
