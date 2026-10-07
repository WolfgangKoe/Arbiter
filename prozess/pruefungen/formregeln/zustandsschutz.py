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


def verstöße(wurzel: Path) -> list[str]:
    return (
        veränderbareDataclasses(wurzel)
        + lesenVerstöße(wurzel)
        + schreibenVerstöße(wurzel)
        + schreibAufrufVerstöße(wurzel)
    )


if __name__ == "__main__":
    meldungen = verstöße(projektordner())
    print("\n".join(meldungen))
    sys.exit(1 if meldungen else 0)
