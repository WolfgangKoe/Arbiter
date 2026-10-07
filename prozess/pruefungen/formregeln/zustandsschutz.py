"""Zustandsschutz D3 (`technik/architektur.md`): frozen, kein `_`-Zugriff, kein Schreiben."""

import ast
import sys
from pathlib import Path

from formregeln.glossar import domaeneOrdner
from gemeinsam.pfade import katalogOrdner, projektordner, webOrdner

lesenGesperrtOrdner = (webOrdner, katalogOrdner)
schreibenGesperrtOrdner = webOrdner
eigenerName = "self"
schreibFunktionen = ("setattr", "delattr", "__setattr__", "__delattr__")
anSelfErlaubt = ("setattr", "delattr")


def dateien(wurzel: Path, ordner: str) -> list[tuple[Path, ast.AST]]:
    return [
        (datei, ast.parse(datei.read_text(encoding="utf-8")))
        for datei in sorted((wurzel / ordner).rglob("*.py"))
    ]


def istDunder(name: str) -> bool:
    return name.startswith("__") and name.endswith("__")


def istDataclassOhneFrozen(dekorator: ast.expr) -> bool:
    if isinstance(dekorator, ast.Name):
        return dekorator.id == "dataclass"
    if isinstance(dekorator, ast.Attribute):
        return dekorator.attr == "dataclass"
    if isinstance(dekorator, ast.Call) and istDataclassOhneFrozen(dekorator.func):
        return not any(
            schlüssel.arg == "frozen"
            and isinstance(schlüssel.value, ast.Constant)
            and schlüssel.value.value is True
            for schlüssel in dekorator.keywords
        )
    return False


def anSelf(zugriff: ast.Attribute) -> bool:
    return isinstance(zugriff.value, ast.Name) and zugriff.value.id == eigenerName


def veränderbareDataclasses(wurzel: Path) -> list[str]:
    gefunden = []
    for datei, baum in dateien(wurzel, domaeneOrdner):
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.ClassDef) and any(
                map(istDataclassOhneFrozen, knoten.decorator_list)
            ):
                gefunden.append(
                    f"{datei.relative_to(wurzel)}:{knoten.lineno} {knoten.name} ohne frozen=True"
                )
    return gefunden


def attributzugriffe(wurzel: Path, ordner: str) -> list[tuple[str, ast.Attribute]]:
    """Alle Attributzugriffe unter `ordner`, außer an `self`, mit ihrem Pfad."""
    return [
        (str(datei.relative_to(wurzel)), knoten)
        for datei, baum in dateien(wurzel, ordner)
        for knoten in ast.walk(baum)
        if isinstance(knoten, ast.Attribute) and not anSelf(knoten)
    ]


def lesenVerstöße(wurzel: Path) -> list[str]:
    return [
        f"{pfad}:{zugriff.lineno} greift auf {zugriff.attr} zu"
        for ordner in lesenGesperrtOrdner
        for pfad, zugriff in attributzugriffe(wurzel, ordner)
        if zugriff.attr.startswith("_") and not istDunder(zugriff.attr)
    ]


def schreibenVerstöße(wurzel: Path) -> list[str]:
    return [
        f"{pfad}:{zugriff.lineno} weist {zugriff.attr} zu"
        for pfad, zugriff in attributzugriffe(wurzel, schreibenGesperrtOrdner)
        if not isinstance(zugriff.ctx, ast.Load)
    ]


def aufrufName(aufruf: ast.Call) -> str | None:
    if isinstance(aufruf.func, ast.Name):
        return aufruf.func.id
    if isinstance(aufruf.func, ast.Attribute):
        return aufruf.func.attr
    return None


def anSelfGerichtet(aufruf: ast.Call) -> bool:
    ziel = aufruf.args[0] if aufruf.args else None
    return isinstance(ziel, ast.Name) and ziel.id == eigenerName


def schreibAufrufVerstöße(wurzel: Path) -> list[str]:
    """`setattr`, `delattr`, `object.__setattr__` umgehen die Zuweisung; nur an `self` erlaubt."""
    return [
        f"{datei.relative_to(wurzel)}:{knoten.lineno} ruft {aufrufName(knoten)} auf"
        for datei, baum in dateien(wurzel, schreibenGesperrtOrdner)
        for knoten in ast.walk(baum)
        if isinstance(knoten, ast.Call)
        and aufrufName(knoten) in schreibFunktionen
        and not (aufrufName(knoten) in anSelfErlaubt and anSelfGerichtet(knoten))
    ]


def textKonstante(knoten: ast.expr | None) -> str:
    wert = knoten.value if isinstance(knoten, ast.Constant) else None
    return wert if isinstance(wert, str) else ""


def versteckterZugriff(aufruf: ast.Call) -> bool:
    """`getattr`/`hasattr` mit `_name` und `vars(x)` umgehen den `_`-Zugriff; `self` ist erlaubt."""
    name = aufrufName(aufruf)
    if name == "vars":
        return not anSelfGerichtet(aufruf)
    zweites = aufruf.args[1] if len(aufruf.args) > 1 else None
    versteckt = textKonstante(zweites)
    return name in ("getattr", "hasattr") and versteckt.startswith("_") and not istDunder(versteckt)


def umwegVerstöße(wurzel: Path) -> list[str]:
    """Lesen von `_`-Attributen ohne Punktzugriff: `getattr`, `hasattr`, `__dict__`, `vars`."""
    gefunden = []
    for ordner in lesenGesperrtOrdner:
        for datei, baum in dateien(wurzel, ordner):
            for knoten in ast.walk(baum):
                umweg = isinstance(knoten, ast.Call) and versteckterZugriff(knoten)
                wörterbuch = (
                    isinstance(knoten, ast.Attribute)
                    and knoten.attr == "__dict__"
                    and not anSelf(knoten)
                )
                if umweg or wörterbuch:
                    gefunden.append(
                        f"{datei.relative_to(wurzel)}:{knoten.lineno} umgeht den _-Zugriff"
                    )
    return gefunden


def verstöße(wurzel: Path) -> list[str]:
    return (
        veränderbareDataclasses(wurzel)
        + lesenVerstöße(wurzel)
        + schreibenVerstöße(wurzel)
        + schreibAufrufVerstöße(wurzel)
        + umwegVerstöße(wurzel)
    )


if __name__ == "__main__":
    meldungen = verstöße(projektordner())
    print("\n".join(meldungen))
    sys.exit(1 if meldungen else 0)
