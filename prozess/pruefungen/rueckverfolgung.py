"""Kriterium ↔ Akzeptanztest: Jedes Kriterium hat einen Test, jeder Test ein Kriterium.

Kriterium `- AUF-1.4 …` in `domaene/anforderungen/<ordner>/<name>.md` gehört zu
`testAuf1_4…` in `technik/tests/akzeptanz/<ordner>/<name>Test.py`. Geprüft wird, wo die
Testdatei schon existiert; eine Anforderung ohne Testdatei wartet auf den Testautor.
"""

import ast
import re
import sys
from pathlib import Path

from agenten import projektordner

kriteriumZeile = re.compile(r"^- ([A-ZÄÖÜ]+)-(\d+)\.(\d+)\b")
testKriterium = re.compile(r"^test([A-ZÄÖÜ][a-zäöüß]*)(\d+)_(\d+)")
akzeptanzOrdner = "technik/tests/akzeptanz"


def kriterien(anforderung: Path) -> set[tuple[str, int, int]]:
    gefunden = set()
    for zeile in anforderung.read_text(encoding="utf-8").splitlines():
        treffer = kriteriumZeile.match(zeile)
        if treffer:
            gefunden.add((treffer[1], int(treffer[2]), int(treffer[3])))
    return gefunden


def getesteKriterien(testdatei: Path) -> set[tuple[str, int, int]]:
    gefunden = set()
    for knoten in ast.walk(ast.parse(testdatei.read_text(encoding="utf-8"))):
        if isinstance(knoten, ast.FunctionDef | ast.AsyncFunctionDef):
            treffer = testKriterium.match(knoten.name)
            if treffer:
                gefunden.add((treffer[1].upper(), int(treffer[2]), int(treffer[3])))
    return gefunden


def kennung(kriterium: tuple[str, int, int]) -> str:
    kürzel, hauptnummer, unternummer = kriterium
    return f"{kürzel}-{hauptnummer}.{unternummer}"


def verstöße(wurzel: Path) -> list[str]:
    meldungen = []
    ordner = wurzel / "domaene" / "anforderungen"
    for anforderung in sorted(ordner.rglob("*.md")):
        unterordner = anforderung.parent.relative_to(ordner)
        testdatei = wurzel / akzeptanzOrdner / unterordner / f"{anforderung.stem}Test.py"
        if not testdatei.is_file():
            continue
        verlangt, getestet = kriterien(anforderung), getesteKriterien(testdatei)
        meldungen += [
            f"{testdatei.relative_to(wurzel).as_posix()}: {kennung(kriterium)} hat keinen Test"
            for kriterium in sorted(verlangt - getestet)
        ]
        meldungen += [
            f"{testdatei.relative_to(wurzel).as_posix()}: Test zu {kennung(kriterium)}, "
            f"das in {anforderung.relative_to(wurzel).as_posix()} fehlt"
            for kriterium in sorted(getestet - verlangt)
        ]
    return meldungen


if __name__ == "__main__":
    gefunden = verstöße(projektordner())
    print("\n".join(gefunden))
    sys.exit(1 if gefunden else 0)
