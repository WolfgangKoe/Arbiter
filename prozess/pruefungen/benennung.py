"""Prüft die Benennung nach `prozess/praemissen/wir.md` und Anliegen 28.

Bezeichner (Funktionen, Parameter, Variablen, Konstanten, Enum-Werte, Fixtures, Attribute von
`self`) in camelCase, Klassen in PascalCase, mindestens 3 Zeichen. Dateinamen in camelCase,
ASCII. Akzeptanztests: `<anforderung>Test.py` im gespiegelten Ordner, Testfunktionen
`test<Kürzel><n>_<m><Satz>`. Anliegen ab Nummer 28: `<nr>-<camelCase>.md`.

Rückstand: Dateien, die vor der Prämisse entstanden und noch nicht umbenannt sind (nur unter
`technik/`), stehen mit ihrem Fingerabdruck in `benennungRueckstand.txt`. Der Eintrag gilt für
die unveränderte Datei; wer sie anfasst oder umbenennt, wird vollständig geprüft. Neue Dateien
sind nie ausgenommen.
"""

import ast
import hashlib
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
anliegenDatei = re.compile(r"^\d+-[a-z][a-zA-Z0-9]*\.md$")

mindestlänge = 3
ersteBenannteAnliegenNummer = 28
werkzeugnamen = {"tmp_path", "tmp_path_factory"}
werkzeugdateien = {"conftest.py", "__init__.py", "__main__.py", "CLAUDE.md", "README.md"}
ausgeschlosseneOrdner = {
    "Arbiter", "ArbiterMap", ".git", "__pycache__", ".venv", ".pytest_cache", ".ruff_cache",
}
nummerierteOrdner = ("domaene/etappen", "domaene/items", "handoff")
akzeptanzOrdner = "technik/tests/akzeptanz"
rückstandsdatei = Path(__file__).with_name("benennungRueckstand.txt")


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


def selbstDefinierteNamen(baum: ast.AST) -> Iterator[tuple[int, str, bool]]:
    """Zeile, Name und ob es eine Klasse ist, für jeden Namen, den der Code selbst festlegt."""
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
    """Ein Akzeptanztest heißt `<anforderung>Test.py` und liegt im Ordner der Anforderung."""
    ordner = wurzel / akzeptanzOrdner
    if not pfad.is_relative_to(ordner) or pfad.name in werkzeugdateien:
        return None
    if not pfad.name.endswith("Test.py"):
        return "Akzeptanztest muss `<anforderung>Test.py` heißen"
    anforderung = wurzel / "domaene" / "anforderungen" / pfad.parent.relative_to(ordner)
    anforderung = anforderung / f"{pfad.name.removesuffix('Test.py')}.md"
    if not anforderung.is_file():
        return f"keine Anforderung {anforderung.relative_to(wurzel).as_posix()} zum Spiegeln"
    return None


def fingerabdruck(datei: Path) -> str:
    return hashlib.sha256(datei.read_bytes()).hexdigest()[:16]


def rückstand(wurzel: Path) -> set[str]:
    """Pfade unter `technik/`, deren Datei noch unverändert dem Fingerabdruck entspricht."""
    if not rückstandsdatei.is_file():
        return set()
    ausgenommen = set()
    for zeile in rückstandsdatei.read_text(encoding="utf-8").splitlines():
        if not zeile.strip() or zeile.startswith("#"):
            continue
        abdruck, _, pfad = zeile.partition(" ")
        datei = wurzel / pfad
        if pfad.startswith("technik/") and datei.is_file() and fingerabdruck(datei) == abdruck:
            ausgenommen.add(pfad)
    return ausgenommen


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
    ausgenommen = rückstand(wurzel)
    meldungen = []
    for pfad in geprüfteDateien(wurzel):
        relativ = pfad.relative_to(wurzel).as_posix()
        if relativ not in ausgenommen:
            meldungen += [f"{relativ}: {grund}" for grund in dateiVerstöße(pfad, wurzel)]
    return meldungen


def rückstandZeilen(wurzel: Path) -> list[str]:
    """Die Zeilen für `benennungRueckstand.txt`: alle verstoßenden Dateien unter `technik/`."""
    zeilen = []
    for pfad in geprüfteDateien(wurzel):
        relativ = pfad.relative_to(wurzel).as_posix()
        if relativ.startswith("technik/") and dateiVerstöße(pfad, wurzel):
            zeilen.append(f"{fingerabdruck(pfad)} {relativ}")
    return zeilen


if __name__ == "__main__":
    ordner = projektordner()
    if "--rückstand" in sys.argv:
        print("\n".join(rückstandZeilen(ordner)))
        sys.exit(0)
    gefunden = verstöße(ordner)
    print("\n".join(gefunden))
    sys.exit(1 if gefunden else 0)
