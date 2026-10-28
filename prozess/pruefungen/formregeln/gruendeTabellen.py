import ast
import sys
from pathlib import Path

from gemeinsam.pfade import projektordner

domaeneOrdner = "technik/arbiter/domaene"


def grundName(knoten: ast.expr) -> str | None:
    if (
        isinstance(knoten, ast.Attribute)
        and isinstance(knoten.value, ast.Name)
        and knoten.value.id == "Grund"
    ):
        return knoten.attr
    return None


def sperreWurf(knoten: ast.AST) -> ast.Call | None:
    if not isinstance(knoten, ast.Raise):
        return None
    aufruf = knoten.exc
    if isinstance(aufruf, ast.Call) and isinstance(aufruf.func, ast.Name):
        return aufruf if aufruf.func.id == "Sperre" else None
    return None


def wächterGründe(baum: ast.AST, dateiname: str, meldungen: list[str]) -> set[str]:
    wächter: set[str] = set()
    for knoten in ast.walk(baum):
        aufruf = sperreWurf(knoten)
        if aufruf is None:
            continue
        argumente = aufruf.args
        if len(argumente) == 1 and isinstance(argumente[0], ast.Starred):
            continue
        grund = grundName(argumente[0]) if len(argumente) == 1 else None
        if grund is None:
            meldungen.append(
                f"{dateiname}:{aufruf.lineno}: raise Sperre braucht genau einen Grund.<wert> "
                "(Wächter) oder genau ein *gründe (eingesammelt)"
            )
        else:
            wächter.add(grund)
    return wächter


def tabellenSchlüssel(baum: ast.AST) -> list[set[str]]:
    tabellen = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Assign | ast.AnnAssign) and isinstance(knoten.value, ast.Dict):
            namen = {grundName(schlüssel) for schlüssel in knoten.value.keys if schlüssel}
            gründe = {name for name in namen if name is not None}
            if gründe:
                tabellen.append(gründe)
    return tabellen


def quelltextVerstöße(quelltexte: dict[str, str]) -> list[str]:
    meldungen: list[str] = []
    wächter: set[str] = set()
    tabellen: list[tuple[str, set[str]]] = []
    for dateiname, quelltext in quelltexte.items():
        baum = ast.parse(quelltext)
        wächter |= wächterGründe(baum, dateiname, meldungen)
        tabellen += [(dateiname, gründe) for gründe in tabellenSchlüssel(baum)]
    gesehen: set[str] = set()
    for dateiname, gründe in tabellen:
        meldungen += [
            f"{dateiname}: Grund.{grund} ist Wächter und Tabellenschlüssel zugleich"
            for grund in sorted(gründe & wächter)
        ]
        meldungen += [
            f"{dateiname}: Grund.{grund} steht in zwei Tabellen"
            for grund in sorted(gründe & gesehen)
        ]
        gesehen |= gründe
    return meldungen


def verstöße(wurzel: Path) -> list[str]:
    quelltexte = {
        datei.relative_to(wurzel).as_posix(): datei.read_text(encoding="utf-8")
        for datei in sorted((wurzel / domaeneOrdner).rglob("*.py"))
    }
    return quelltextVerstöße(quelltexte)


if __name__ == "__main__":
    gefunden = verstöße(projektordner())
    print("\n".join(gefunden))
    sys.exit(1 if gefunden else 0)
