from collections.abc import Callable, Mapping
from fractions import Fraction
from types import MappingProxyType

from arbiter.domaene.missionsvorbereitung.ausgangslage import (
    Aufstellungszone,
    Ausgangslage,
    Formation,
)
from arbiter.domaene.spielobjekte import Armee, Base, Einheit, Modell, Spieler, Spielfeld
from arbiter.katalog.datenblaetter import (
    Datenblatt,
    datenblätterLesen,
    ganzeZahlÜberNull,
    genauDieseSchlüsselLesen,
)
from arbiter.katalog.yamlLesen import yamlLesen

DatenblätterVon = Callable[[str], Mapping[str, Datenblatt]]


def _textLesen(text: object) -> str:
    if not isinstance(text, str):
        raise ValueError(f"Ein Name muss Text sein: {text!r}")
    return text


def _modellzahlenLesen(modelle: object) -> dict[str, int]:
    if not isinstance(modelle, dict) or not modelle:
        raise ValueError("Eine Einheit braucht mindestens eine Modellart")
    return {
        modellart: ganzeZahlÜberNull(anzahl, f"Die Zahl der Modelle von {modellart}")
        for modellart, anzahl in modelle.items()
    }


_einheitzeilen = {"fraktion": _textLesen, "datenblatt": _textLesen, "modelle": _modellzahlenLesen}


def _modellLesen(modellart: str, datenblatt: Datenblatt) -> Modell:
    if modellart not in datenblatt:
        raise ValueError(f"Das Datenblatt kennt keine Modellart {modellart}")
    werte = datenblatt[modellart]
    return Modell(
        modellart=modellart,
        base=Base(durchmesser=werte.durchmesser),
        bewegungsweite=werte.bewegungsweite,
    )


def _einheitLesen(eintrag: object, datenblätterVon: DatenblätterVon) -> Einheit:
    gelesen = genauDieseSchlüsselLesen(eintrag, _einheitzeilen, "Eine Einheit der Ausgangslage")
    datenblätter = datenblätterVon(gelesen["fraktion"])
    name = gelesen["datenblatt"]
    if name not in datenblätter:
        raise ValueError(f"Die Fraktion {gelesen['fraktion']} kennt kein Datenblatt {name}")
    return Einheit(
        name=name,
        modelle=tuple(
            _modellLesen(modellart, datenblätter[name])
            for modellart, anzahl in gelesen["modelle"].items()
            for _ in range(anzahl)
        ),
    )


def _armeeLesen(einheiten: list[dict], datenblätterVon: DatenblätterVon) -> Armee:
    return Armee(einheiten=tuple(_einheitLesen(eintrag, datenblätterVon) for eintrag in einheiten))


def ausgangslageLaden() -> Ausgangslage:
    return ausgangslageAus(
        yamlLesen("ausgangslage.yaml"),
        yamlLesen("onlyWar.yaml"),
        yamlLesen("formation.yaml"),
        datenblätterLesen,
    )


def _formationenLesen(formation: dict) -> Mapping[str, Formation]:
    abstand = Fraction(str(formation["abstand"]))
    return MappingProxyType(
        {
            name: Formation(
                reihen=tuple(ganzeZahlÜberNull(reihe, "Die Reihe") for reihe in reihen),
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


def ausgangslageAus(
    ausgangslage: dict, onlyWar: dict, formation: dict, datenblätterVon: DatenblätterVon
) -> Ausgangslage:
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
    ersterSpieler = Spieler(armee=_armeeLesen(ersteArmee, datenblätterVon))
    zweiterSpieler = Spieler(armee=_armeeLesen(zweiteArmee, datenblätterVon))
    _formationenPrüfen(ersterSpieler.armee, formationen)
    _formationenPrüfen(zweiterSpieler.armee, formationen)
    return Ausgangslage(
        ersterSpieler=ersterSpieler,
        zweiterSpieler=zweiterSpieler,
        spielfeld=Spielfeld(seitenlängen=(Fraction(breite), Fraction(länge))),
        tiefen=MappingProxyType(tiefen),
        formationen=formationen,
        letzteSchlachtrunde=ganzeZahlÜberNull(
            onlyWar["Schlacht"]["schlachtrunde"], "Die letzte Schlachtrunde"
        ),
    )
