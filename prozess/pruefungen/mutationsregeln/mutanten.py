"""Baut aus dem Quelltext eines Moduls Mutanten: je einer mit genau einem eingebauten Fehler."""

import ast
from typing import NamedTuple

vergleichTausch: dict[type, type] = {
    ast.Lt: ast.LtE,
    ast.LtE: ast.Lt,
    ast.Gt: ast.GtE,
    ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
    ast.In: ast.NotIn,
    ast.NotIn: ast.In,
    ast.Is: ast.IsNot,
    ast.IsNot: ast.Is,
}
rechenTausch: dict[type, type] = {
    ast.Add: ast.Sub,
    ast.Sub: ast.Add,
    ast.Mult: ast.FloorDiv,
    ast.FloorDiv: ast.Mult,
    ast.Pow: ast.Mult,
}
verknüpfungTausch: dict[type, type] = {ast.And: ast.Or, ast.Or: ast.And}


class Mutant(NamedTuple):
    zeile: int
    beschreibung: str
    quelle: str


def tauschText(alt: object, neu: type) -> str:
    return f"{type(alt).__name__} wird {neu.__name__}"


class Einbauer(ast.NodeTransformer):
    """Zählt die Stellen, an denen ein Fehler möglich ist, und baut an der `ziel`-ten einen ein."""

    def __init__(self, ziel: int) -> None:
        self.ziel = ziel
        self.gezählt = 0
        self.zeile = 0
        self.beschreibung = ""

    def treffer(self, knoten: ast.AST, beschreibung: str) -> bool:
        stelle = self.gezählt
        self.gezählt += 1
        if stelle != self.ziel:
            return False
        self.zeile = getattr(knoten, "lineno", 0)
        self.beschreibung = beschreibung
        return True

    def visit(self, knoten: ast.AST) -> ast.AST:
        besucher = getattr(self, f"besuche{type(knoten).__name__}", self.generic_visit)
        return besucher(knoten)

    def besucheCompare(self, knoten: ast.Compare) -> ast.AST:
        self.generic_visit(knoten)
        for platz, vergleich in enumerate(knoten.ops):
            gegenteil = vergleichTausch.get(type(vergleich))
            if gegenteil and self.treffer(knoten, tauschText(vergleich, gegenteil)):
                knoten.ops[platz] = gegenteil()
        return knoten

    def besucheBoolOp(self, knoten: ast.BoolOp) -> ast.AST:
        self.generic_visit(knoten)
        gegenteil = verknüpfungTausch[type(knoten.op)]
        if self.treffer(knoten, tauschText(knoten.op, gegenteil)):
            knoten.op = gegenteil()
        return knoten

    def besucheBinOp(self, knoten: ast.BinOp) -> ast.AST:
        self.generic_visit(knoten)
        gegenteil = rechenTausch.get(type(knoten.op))
        if gegenteil and self.treffer(knoten, tauschText(knoten.op, gegenteil)):
            knoten.op = gegenteil()
        return knoten

    def besucheUnaryOp(self, knoten: ast.UnaryOp) -> ast.AST:
        self.generic_visit(knoten)
        if isinstance(knoten.op, ast.Not) and self.treffer(knoten, "not entfällt"):
            return knoten.operand
        return knoten

    def besucheConstant(self, knoten: ast.Constant) -> ast.AST:
        wert = knoten.value
        if isinstance(wert, bool):
            if self.treffer(knoten, f"{wert} wird {not wert}"):
                knoten.value = not wert
        elif isinstance(wert, int) and self.treffer(knoten, f"{wert} wird {wert + 1}"):
            knoten.value = wert + 1
        return knoten

    def besucheReturn(self, knoten: ast.Return) -> ast.AST:
        self.generic_visit(knoten)
        ohneWert = knoten.value is None or (
            isinstance(knoten.value, ast.Constant) and knoten.value.value is None
        )
        if not ohneWert and self.treffer(knoten, "Rückgabe wird None"):
            knoten.value = ast.Constant(value=None)
        return knoten

    def besucheRaise(self, knoten: ast.Raise) -> ast.AST:
        if self.treffer(knoten, "raise entfällt"):
            return ast.copy_location(ast.Pass(), knoten)
        return knoten

    def besucheAnnAssign(self, knoten: ast.AnnAssign) -> ast.AST:
        if knoten.value is not None:
            knoten.value = self.visit(knoten.value)
        return knoten


def eingebaut(quelle: str, ziel: int) -> tuple[Einbauer, str]:
    einbauer = Einbauer(ziel)
    baum = einbauer.visit(ast.parse(quelle))
    ast.fix_missing_locations(baum)
    return einbauer, ast.unparse(baum)


def mutantenVon(quelle: str) -> list[Mutant]:
    """Alle Mutanten des Quelltexts, in der Reihenfolge der Stellen."""
    stellen = eingebaut(quelle, -1)[0].gezählt
    gefunden = []
    for ziel in range(stellen):
        einbauer, geändert = eingebaut(quelle, ziel)
        gefunden.append(Mutant(einbauer.zeile, einbauer.beschreibung, geändert))
    return gefunden
