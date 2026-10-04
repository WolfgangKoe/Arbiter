"""Code → Glossar: Klassen und Enum-Werte der Domäne stehen im Glossar oder als Grund."""

import ast
import re
import sys
from pathlib import Path

from gemeinsam.pfade import anforderungsOrdner
from rollenregeln.agenten import projektordner

bezeichnerZelle = re.compile(r"^(\w+)(?: \(([^)]*)\))?$")
grundText = re.compile(r"‚([^‘]+)‘")
domaeneOrdner = "technik/arbiter/domaene"
spalteCodeBezeichner = 2


def glossarBezeichner(glossar: str) -> dict[str, set[str]]:
    """Klasse → ihre Enum-Werte, wie die Spalte *Code-Bezeichner* sie nennt."""
    bezeichner: dict[str, set[str]] = {}
    for zeile in glossar.splitlines():
        zellen = [zelle.strip() for zelle in zeile.split("|")]
        treffer = (
            bezeichnerZelle.match(zellen[spalteCodeBezeichner])
            if len(zellen) > spalteCodeBezeichner
            else None
        )
        if treffer:
            werte = treffer[2] or ""
            bezeichner[treffer[1]] = {wert.strip() for wert in werte.split(",") if wert.strip()}
    return bezeichner


def gründe(anforderungen: str) -> set[str]:
    return set(grundText.findall(anforderungen))


def enumWerte(klasse: ast.ClassDef) -> list[tuple[str, str | None]]:
    """Name und, falls ein Text, der Wert jedes Enum-Werts der Klasse, auch mit Annotation."""
    werte = []
    for anweisung in klasse.body:
        if isinstance(anweisung, ast.Assign) and isinstance(anweisung.targets[0], ast.Name):
            name, inhalt = anweisung.targets[0].id, anweisung.value
        elif (
            isinstance(anweisung, ast.AnnAssign)
            and isinstance(anweisung.target, ast.Name)
            and anweisung.value is not None
        ):
            name, inhalt = anweisung.target.id, anweisung.value
        else:
            continue
        text = inhalt.value if isinstance(inhalt, ast.Constant) else None
        werte.append((name, text if isinstance(text, str) else None))
    return werte


def basisName(basis: ast.expr) -> str:
    if isinstance(basis, ast.Name):
        return basis.id
    return basis.attr if isinstance(basis, ast.Attribute) else ""


def istEnum(klasse: ast.ClassDef) -> bool:
    return any(basisName(basis).endswith(("Enum", "Flag")) for basis in klasse.bases)


def quelltextVerstöße(
    quelltext: str, dateiname: str, glossar: dict[str, set[str]], gründeDerAnforderungen: set[str]
) -> list[str]:
    meldungen = []
    weg = "ein Anliegen an den Anforderungsautor, damit der Begriff erst im Glossar steht"
    for knoten in ast.walk(ast.parse(quelltext)):
        if not isinstance(knoten, ast.ClassDef):
            continue
        if knoten.name not in glossar:
            meldungen.append(f"{dateiname}: Klasse {knoten.name} steht nicht im Glossar; {weg}")
            continue
        if not istEnum(knoten):
            continue
        for name, text in enumWerte(knoten):
            if name not in glossar[knoten.name] and text not in gründeDerAnforderungen:
                meldungen.append(
                    f"{dateiname}: Enum-Wert {knoten.name}.{name} steht weder im Glossar "
                    f"noch als Grund in einer Anforderung; {weg}"
                )
    return meldungen


def verstöße(wurzel: Path) -> list[str]:
    glossar = glossarBezeichner((wurzel / "domaene" / "glossar.md").read_text(encoding="utf-8"))
    gründeDerAnforderungen = gründe(
        "\n".join(
            datei.read_text(encoding="utf-8")
            for datei in (wurzel / anforderungsOrdner).rglob("*.md")
        )
    )
    meldungen = []
    for datei in sorted((wurzel / domaeneOrdner).rglob("*.py")):
        meldungen += quelltextVerstöße(
            datei.read_text(encoding="utf-8"),
            datei.relative_to(wurzel).as_posix(),
            glossar,
            gründeDerAnforderungen,
        )
    return meldungen


if __name__ == "__main__":
    gefunden = verstöße(projektordner())
    print("\n".join(gefunden))
    sys.exit(1 if gefunden else 0)
