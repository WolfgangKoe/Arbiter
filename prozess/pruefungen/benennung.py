"""Prüft die Benennung nach `prozess/praemissen/wir.md`."""

import ast
import re
import sys
from collections.abc import Iterator
from pathlib import Path

from agenten import projektordner

camelCase = re.compile(r"^[a-zäöü][a-zA-Z0-9äöüÄÖÜß]*$")
pascalCase = re.compile(r"^[A-ZÄÖÜ][a-zA-Z0-9äöüÄÖÜß]*$")
testName = re.compile(r"^test[A-ZÄÖÜ][a-zA-Z0-9äöüÄÖÜß]*$")
akzeptanzTestName = re.compile(r"^test[A-ZÄÖÜ][a-zäöüß]*\d+_\d+[A-ZÄÖÜ][a-zA-Z0-9äöüÄÖÜß]*$")
pythonDatei = re.compile(r"^[a-z][a-zA-Z0-9]*\.py$")
markdownDatei = re.compile(r"^[a-z][a-zA-Z0-9]*\.md$")
geteilterTest = re.compile(r"^(?P<kürzel>[a-z]+)(?P<nummer>\d+)Test\.py$")
anliegenDatei = re.compile(r"^\d+-[a-z][a-zA-Z0-9]*\.md$")

mindestlänge = 3
achsen = {"x", "y"}
typgenerika = {"tuple", "list", "dict", "set", "frozenset", "Callable", "Literal", "Union"}
ersteBenannteAnliegenNummer = 28
werkzeugnamen = {"tmp_path", "tmp_path_factory"}
# Warum: In conftest.py gibt pytest die Hooks `pytest_<hook>` vor.
werkzeugdateien = {"conftest.py", "__init__.py", "__main__.py", "CLAUDE.md", "README.md"}
ausgeschlosseneOrdner = {
    "Arbiter",
    "ArbiterMap",
    ".git",
    "__pycache__",
    ".venv",
    ".pytest_cache",
    ".ruff_cache",
}
nummerierteOrdner = ("domaene/etappen", "domaene/items", "handoff")
akzeptanzOrdner = "technik/tests/akzeptanz"


def nameVerstoß(name: str, *, istKlasse: bool = False) -> str | None:
    if name in werkzeugnamen or (name.startswith("__") and name.endswith("__")):
        return None
    kern = name.lstrip("_")
    if not kern:
        return None
    if len(kern) < mindestlänge:
        return f"{name}: weniger als {mindestlänge} Zeichen"
    if not (pascalCase if istKlasse else camelCase).match(kern):
        return f"{name}: nicht in {'PascalCase' if istKlasse else 'camelCase'}"
    return None


def typaliase(baum: ast.AST) -> dict[int, str]:
    """Zeile und Name der Typaliase auf Modulebene (`Name = tuple[…]`, `type Name = …`)."""
    gefunden = {}
    for knoten in getattr(baum, "body", []):
        if isinstance(knoten, ast.TypeAlias) and isinstance(knoten.name, ast.Name):
            gefunden[knoten.lineno] = knoten.name.id
        elif (
            isinstance(knoten, ast.Assign)
            and len(knoten.targets) == 1
            and isinstance(knoten.targets[0], ast.Name)
            and isinstance(knoten.value, ast.Subscript)
            and isinstance(knoten.value.value, ast.Name)
            and knoten.value.value.id in typgenerika
        ):
            gefunden[knoten.lineno] = knoten.targets[0].id
    return gefunden


def koordinatenfelder(baum: ast.AST) -> set[tuple[int, str]]:
    """Zeile und Name der Achsen `x`, `y` als Felder von `Stelle` (Architektur S1)."""
    felder = set()
    for klasse in ast.walk(baum):
        if isinstance(klasse, ast.ClassDef) and klasse.name == "Stelle":
            felder |= {
                (feld.lineno, feld.target.id)
                for feld in klasse.body
                if isinstance(feld, ast.AnnAssign)
                and isinstance(feld.target, ast.Name)
                and feld.target.id in achsen
            }
    return felder


def selbstDefinierteNamen(baum: ast.AST) -> Iterator[tuple[int, str, bool]]:
    """Zeile, Name und ob es eine Klasse ist, für jeden Namen, den der Code selbst festlegt."""
    aliase = typaliase(baum)
    yield from ((zeile, name, True) for zeile, name in aliase.items())
    achsenfelder = koordinatenfelder(baum)
    for zeile, name, istKlasse in einzelneNamen(baum):
        if aliase.get(zeile) != name and (zeile, name) not in achsenfelder:
            yield zeile, name, istKlasse


def einzelneNamen(baum: ast.AST) -> Iterator[tuple[int, str, bool]]:
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.ClassDef):
            yield knoten.lineno, knoten.name, True
        elif isinstance(knoten, ast.FunctionDef | ast.AsyncFunctionDef):
            yield knoten.lineno, knoten.name, False
        elif isinstance(knoten, ast.arg):
            yield knoten.lineno, knoten.arg, False
        elif isinstance(knoten, ast.Name) and isinstance(knoten.ctx, ast.Store):
            yield knoten.lineno, knoten.id, False
        elif isinstance(knoten, ast.ExceptHandler) and knoten.name:
            yield knoten.lineno, knoten.name, False
        elif isinstance(knoten, ast.alias) and knoten.asname:
            yield knoten.lineno, knoten.asname, False
        elif isinstance(knoten, ast.Global | ast.Nonlocal):
            yield from ((knoten.lineno, name, False) for name in knoten.names)
        elif (
            isinstance(knoten, ast.Attribute)
            and isinstance(knoten.ctx, ast.Store)
            and isinstance(knoten.value, ast.Name)
            and knoten.value.id == "self"
        ):
            yield knoten.lineno, knoten.attr, False


def testfunktionen(baum: ast.AST) -> Iterator[ast.FunctionDef | ast.AsyncFunctionDef]:
    for knoten in ast.walk(baum):
        istFunktion = isinstance(knoten, ast.FunctionDef | ast.AsyncFunctionDef)
        if istFunktion and knoten.name.startswith("test"):
            yield knoten


def istTestdatei(name: str) -> bool:
    return name.endswith("Test.py") or name.startswith("test_")


def quelltextVerstöße(
    quelltext: str, dateiname: str, *, imAkzeptanzordner: bool = False
) -> list[str]:
    baum = ast.parse(quelltext)
    verstöße = [
        f"Zeile {zeile}: {grund}"
        for zeile, name, istKlasse in selbstDefinierteNamen(baum)
        if (grund := nameVerstoß(name, istKlasse=istKlasse))
        and not (istTestdatei(dateiname) and name.startswith("test"))
        and not (dateiname == "conftest.py" and name.startswith("pytest_"))
    ]
    if istTestdatei(dateiname):
        muster = akzeptanzTestName if imAkzeptanzordner else testName
        verstöße += [
            f"Zeile {funktion.lineno}: {funktion.name}: passt nicht zu `{muster.pattern}`"
            for funktion in testfunktionen(baum)
            if not muster.match(funktion.name)
        ]
    return verstöße


def dateinamenVerstoß(pfad: Path, wurzel: Path) -> str | None:
    relativ = pfad.relative_to(wurzel).as_posix()
    if pfad.name in werkzeugdateien:
        return None
    if pfad.suffix == ".py":
        return None if pythonDatei.match(pfad.name) else "Dateiname nicht in camelCase, ASCII"
    if relativ.startswith("handoff/anliegen/"):
        nummer = pfad.name.partition("-")[0]
        zuPrüfen = nummer.isdigit() and int(nummer) >= ersteBenannteAnliegenNummer
        if zuPrüfen and not anliegenDatei.match(pfad.name):
            return "Anliegen: `<nr>-<camelCase>.md` erwartet"
        return None
    if relativ.startswith(nummerierteOrdner):
        return None
    return None if markdownDatei.match(pfad.name) else "Dateiname nicht in camelCase, ASCII"


def spiegelVerstoß(pfad: Path, wurzel: Path) -> str | None:
    """Akzeptanztest `<anforderung>Test.py`, geteilt `<kürzel><n>Test.py` im Ordner `<datei>/`."""
    ordner = wurzel / akzeptanzOrdner
    if not pfad.is_relative_to(ordner) or pfad.name in werkzeugdateien:
        return None
    if not pfad.name.endswith("Test.py"):
        return "Akzeptanztest muss `<anforderung>Test.py` heißen"
    anforderungen = wurzel / "domaene" / "anforderungen"
    anforderung = (
        anforderungen / pfad.parent.relative_to(ordner) / f"{pfad.name.removesuffix('Test.py')}.md"
    )
    if anforderung.is_file():
        return None
    geteilt = geteilterTest.match(pfad.name)
    gebündelt = anforderungen / pfad.parent.relative_to(ordner).with_suffix(".md")
    if geteilt and gebündelt.is_file():
        kennung = f"{geteilt['kürzel'].upper()}-{geteilt['nummer']}"
        if re.search(rf"^#+ {kennung}\b", gebündelt.read_text(encoding="utf-8"), re.MULTILINE):
            return None
        datei = gebündelt.relative_to(wurzel).as_posix()
        return f"keine Anforderung {kennung} in {datei} zum Spiegeln"
    return f"keine Anforderung {anforderung.relative_to(wurzel).as_posix()} zum Spiegeln"


def geprüfteDateien(wurzel: Path) -> Iterator[Path]:
    for endung in ("*.py", "*.md"):
        for pfad in sorted(wurzel.rglob(endung)):
            relativ = pfad.relative_to(wurzel)
            if ausgeschlosseneOrdner.isdisjoint(relativ.parts) and (
                endung == "*.py" or relativ.parts[0] in ("domaene", "technik", "prozess", "handoff")
            ):
                yield pfad


def dateiVerstöße(pfad: Path, wurzel: Path) -> list[str]:
    gründe = (dateinamenVerstoß(pfad, wurzel), spiegelVerstoß(pfad, wurzel))
    verstöße = [grund for grund in gründe if grund]
    if pfad.suffix == ".py":
        imAkzeptanzordner = pfad.is_relative_to(wurzel / akzeptanzOrdner)
        verstöße += quelltextVerstöße(
            pfad.read_text(encoding="utf-8"), pfad.name, imAkzeptanzordner=imAkzeptanzordner
        )
    return verstöße


def verstöße(wurzel: Path) -> list[str]:
    meldungen = []
    for pfad in geprüfteDateien(wurzel):
        relativ = pfad.relative_to(wurzel).as_posix()
        meldungen += [f"{relativ}: {grund}" for grund in dateiVerstöße(pfad, wurzel)]
    return meldungen


if __name__ == "__main__":
    gefunden = verstöße(projektordner())
    print("\n".join(gefunden))
    sys.exit(1 if gefunden else 0)
