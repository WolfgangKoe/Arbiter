"""Kriterium ↔ Akzeptanztest: Jedes Kriterium hat einen Test, jeder Test ein Kriterium.

Kriterium `- AUF-1.4 …` unter `### AUF-1 · …` in `domaene/anforderungen/<pfad>.md` gehört zu
`testAuf1_4…`. Der Test steht in `technik/tests/akzeptanz/<pfad>Test.py`, solange die Datei
nur eine Anforderung hat, sonst je Anforderung in `<pfad>/<kürzel><n>Test.py`, etwa
`<pfad>/auf1Test.py` (Anliegen 52, Architektur T1). Geprüft wird, wo die Testdatei schon
existiert; eine Anforderung ohne Testdatei wartet auf den Testautor.

Ein Kriterium ohne Test ist erst rot, wenn ein offenes Item eines freigegebenen Plans es
nennt (`AUF-1` oder `AUF-1.8`); vorher wartet es auf den Testautor (Anliegen 62). Eine
Kennung steht in einer Anforderungsdatei nur einmal (Anliegen 60).

Spur (Anliegen 53, Architektur T2): `rueckverfolgung.py AUF-1.4` nennt das Kriterium und jeden
seiner Tests als `pfad:zeile`; statt der Kennung geht ein Testname oder `pfad:zeile`;
`--json` liefert eine Liste von Objekten.
"""

import ast
import json
import re
import sys
from collections import Counter
from pathlib import Path

from agenten import projektordner
from plan import freigegebenerPlan, offeneItemTexte

anforderungsnummer = tuple[str, int]
kriteriumsnummer = tuple[str, int, int]
fundstelle = tuple[str, str, int]  # Art, Pfad, Zeile

anforderungZeile = re.compile(r"^### ([A-ZÄÖÜ]+)-(\d+)\b")
kriteriumZeile = re.compile(r"^- ([A-ZÄÖÜ]+)-(\d+)\.(\d+)\b")
kriteriumKennung = re.compile(r"^([A-ZÄÖÜ]+)-(\d+)\.(\d+)$")
testKriterium = re.compile(r"^test([A-ZÄÖÜ][a-zäöüß]*)(\d+)_(\d+)")
stellenAngabe = re.compile(r"^(.+):(\d+)$")
akzeptanzOrdner = "technik/tests/akzeptanz"
anforderungsOrdner = "domaene/anforderungen"


def kennung(kriterium: kriteriumsnummer) -> str:
    kürzel, hauptnummer, unternummer = kriterium
    return f"{kürzel}-{hauptnummer}.{unternummer}"


def anforderungKennung(anforderung: anforderungsnummer) -> str:
    return f"{anforderung[0]}-{anforderung[1]}"


def zeilen(datei: Path) -> list[str]:
    return datei.read_text(encoding="utf-8").splitlines()


def anforderungenMitZeile(anforderungsdatei: Path) -> list[tuple[anforderungsnummer, int]]:
    return [
        ((treffer[1], int(treffer[2])), nummer)
        for nummer, zeile in enumerate(zeilen(anforderungsdatei), 1)
        if (treffer := anforderungZeile.match(zeile))
    ]


def kriterienMitZeile(anforderungsdatei: Path) -> list[tuple[kriteriumsnummer, int]]:
    return [
        ((treffer[1], int(treffer[2]), int(treffer[3])), nummer)
        for nummer, zeile in enumerate(zeilen(anforderungsdatei), 1)
        if (treffer := kriteriumZeile.match(zeile))
    ]


def kriterien(anforderungsdatei: Path) -> set[kriteriumsnummer]:
    return {kriterium for kriterium, _ in kriterienMitZeile(anforderungsdatei)}


def testsMitZeile(testdatei: Path) -> list[tuple[kriteriumsnummer, int, int]]:
    """Kriterium, erste und letzte Zeile jeder Testfunktion mit Kennung im Namen."""
    gefunden = []
    for knoten in ast.walk(ast.parse(testdatei.read_text(encoding="utf-8"))):
        if isinstance(knoten, ast.FunctionDef | ast.AsyncFunctionDef):
            treffer = testKriterium.match(knoten.name)
            if treffer:
                kriterium = (treffer[1].upper(), int(treffer[2]), int(treffer[3]))
                gefunden.append((kriterium, knoten.lineno, knoten.end_lineno or knoten.lineno))
    return gefunden


def getesteKriterien(testdatei: Path) -> set[kriteriumsnummer]:
    return {kriterium for kriterium, _, _ in testsMitZeile(testdatei)}


def doppelte(kennungen: list[str]) -> list[str]:
    return sorted(name for name, anzahl in Counter(kennungen).items() if anzahl > 1)


def anforderungenDerDatei(anforderungsdatei: Path) -> list[anforderungsnummer]:
    """Die Anforderungen der Datei, auch die, von denen nur Kriterien da sind."""
    gefunden = {anforderung for anforderung, _ in anforderungenMitZeile(anforderungsdatei)}
    gefunden |= {(kürzel, haupt) for (kürzel, haupt, _), _ in kriterienMitZeile(anforderungsdatei)}
    return sorted(gefunden)


def testdateiZu(
    wurzel: Path, anforderungsdatei: Path, anforderung: anforderungsnummer | None
) -> Path:
    """Die Testdatei der Anforderung; `None` steht für die Datei mit nur einer Anforderung."""
    ordner = wurzel / anforderungsOrdner
    pfad = anforderungsdatei.relative_to(ordner).with_suffix("")
    wurzelTests = wurzel / akzeptanzOrdner
    if anforderung is None:
        return wurzelTests / pfad.parent / f"{pfad.name}Test.py"
    kürzel, nummer = anforderung
    return wurzelTests / pfad / f"{kürzel.lower()}{nummer}Test.py"


def nennt(text: str, kriterium: kriteriumsnummer) -> bool:
    """Der Text nennt das Kriterium (`AUF-1.8`) oder seine Anforderung (`AUF-1`)."""
    kürzel, haupt, unter = kriterium
    muster = rf"\b{kürzel}-{haupt}(?:\.{unter}(?!\d)|(?!\d)(?!\.\d))"
    return re.search(muster, text) is not None


def umfasst(wurzel: Path, kriterium: kriteriumsnummer) -> bool:
    """Ein offenes Item des freigegebenen Plans nennt das Kriterium oder seine Anforderung."""
    if freigegebenerPlan(wurzel) is None:
        return False
    return any(nennt(text, kriterium) for text in offeneItemTexte(wurzel))


def pfadVon(wurzel: Path, datei: Path) -> str:
    return datei.relative_to(wurzel).as_posix()


def testdateiVerstöße(
    wurzel: Path, anforderungsdatei: Path, testdatei: Path, verlangt: set[kriteriumsnummer]
) -> list[str]:
    meldungen = []
    getestet = getesteKriterien(testdatei)
    pfad = pfadVon(wurzel, testdatei)
    meldungen += [
        f"{pfad}: {kennung(kriterium)} hat keinen Test"
        for kriterium in sorted(verlangt - getestet)
        if umfasst(wurzel, kriterium)
    ]
    meldungen += [
        f"{pfad}: Test zu {kennung(kriterium)}, das in {pfadVon(wurzel, anforderungsdatei)} "
        "fehlt oder zu einer anderen Anforderung gehört"
        for kriterium in sorted(getestet - verlangt)
    ]
    return meldungen


def anforderungenMitTestdatei(
    wurzel: Path, anforderungsdatei: Path
) -> list[tuple[Path, set[kriteriumsnummer]]]:
    """Je Anforderung mit vorhandener Testdatei: die Datei und die Kriterien, die sie testet."""
    anforderungen = anforderungenDerDatei(anforderungsdatei)
    einzige = len(anforderungen) == 1
    gefunden = []
    for anforderung in anforderungen:
        testdatei = testdateiZu(wurzel, anforderungsdatei, None if einzige else anforderung)
        if testdatei.is_file():
            alle = kriterien(anforderungsdatei)
            verlangt = {kriterium for kriterium in alle if kriterium[:2] == anforderung}
            gefunden.append((testdatei, verlangt))
    return gefunden


def doppelteKennungen(anforderungsdatei: Path) -> list[str]:
    return doppelte(
        [kennung(kriterium) for kriterium, _ in kriterienMitZeile(anforderungsdatei)]
        + [anforderungKennung(nummer) for nummer, _ in anforderungenMitZeile(anforderungsdatei)]
    )


def anforderungsVerstöße(wurzel: Path, anforderungsdatei: Path) -> list[str]:
    pfad = pfadVon(wurzel, anforderungsdatei)
    meldungen = [f"{pfad}: {name} steht zweimal" for name in doppelteKennungen(anforderungsdatei)]
    sammeldatei = testdateiZu(wurzel, anforderungsdatei, None)
    if len(anforderungenDerDatei(anforderungsdatei)) > 1 and sammeldatei.is_file():
        meldungen.append(
            f"{pfadVon(wurzel, sammeldatei)}: teilen nach Anforderung, "
            f"je Anforderung eine Datei {sammeldatei.stem.removesuffix('Test')}/<kürzel><n>Test.py"
        )
    for testdatei, verlangt in anforderungenMitTestdatei(wurzel, anforderungsdatei):
        meldungen += testdateiVerstöße(wurzel, anforderungsdatei, testdatei, verlangt)
    return meldungen


def verstöße(wurzel: Path) -> list[str]:
    meldungen = []
    for anforderungsdatei in sorted((wurzel / anforderungsOrdner).rglob("*.md")):
        meldungen += anforderungsVerstöße(wurzel, anforderungsdatei)
    return meldungen


def wartende(wurzel: Path) -> list[str]:
    """Kriterien ohne Test, deren Testdatei da ist und die kein freigegebener Plan umfasst."""
    gefunden = []
    for anforderungsdatei in sorted((wurzel / anforderungsOrdner).rglob("*.md")):
        for testdatei, verlangt in anforderungenMitTestdatei(wurzel, anforderungsdatei):
            fehlend = verlangt - getesteKriterien(testdatei)
            gefunden += [
                kennung(kriterium)
                for kriterium in sorted(fehlend)
                if not umfasst(wurzel, kriterium)
            ]
    return gefunden


def wartendeAlsText(wurzel: Path) -> str:
    gefunden = wartende(wurzel)
    return f"{', '.join(gefunden)} wartet auf den Testautor" if gefunden else ""


def kriteriumsstellen(wurzel: Path) -> dict[kriteriumsnummer, list[fundstelle]]:
    stellen: dict[kriteriumsnummer, list[fundstelle]] = {}
    for datei in sorted((wurzel / anforderungsOrdner).rglob("*.md")):
        for kriterium, zeile in kriterienMitZeile(datei):
            stellen.setdefault(kriterium, []).append(("Kriterium", pfadVon(wurzel, datei), zeile))
    return stellen


def teststellen(wurzel: Path) -> dict[kriteriumsnummer, list[fundstelle]]:
    stellen: dict[kriteriumsnummer, list[fundstelle]] = {}
    for datei in sorted((wurzel / akzeptanzOrdner).rglob("*Test.py")):
        for kriterium, zeile, _ in testsMitZeile(datei):
            stellen.setdefault(kriterium, []).append(("Test", pfadVon(wurzel, datei), zeile))
    return stellen


def kriteriumZuStelle(wurzel: Path, pfad: str, zeile: int) -> kriteriumsnummer | None:
    """Das Kriterium, das in der Zeile der Datei steht oder dessen Testfunktion sie enthält."""
    datei = wurzel / pfad
    if not datei.is_file():
        return None
    if datei.suffix == ".md":
        stellen = kriterienMitZeile(datei)
        return next((kriterium for kriterium, nummer in stellen if nummer == zeile), None)
    return next(
        (kriterium for kriterium, anfang, ende in testsMitZeile(datei) if anfang <= zeile <= ende),
        None,
    )


def kriteriumZuEingabe(wurzel: Path, eingabe: str) -> kriteriumsnummer | None:
    treffer = kriteriumKennung.match(eingabe.upper())
    if treffer:
        return treffer[1], int(treffer[2]), int(treffer[3])
    treffer = testKriterium.match(eingabe)
    if treffer:
        return treffer[1].upper(), int(treffer[2]), int(treffer[3])
    stelle = stellenAngabe.match(eingabe)
    return kriteriumZuStelle(wurzel, stelle[1], int(stelle[2])) if stelle else None


def spur(wurzel: Path, eingabe: str) -> list[fundstelle] | None:
    """Kriterium und seine Tests; `None`, wenn die Eingabe kein bekanntes Kriterium nennt."""
    kriterium = kriteriumZuEingabe(wurzel, eingabe)
    stellen = kriteriumsstellen(wurzel).get(kriterium, []) if kriterium else []
    if not stellen:
        return None
    return stellen + teststellen(wurzel).get(kriterium, [])


def spurAlsText(stellen: list[fundstelle], *, alsJson: bool) -> str:
    if alsJson:
        return json.dumps(
            [{"art": art, "pfad": pfad, "zeile": zeile} for art, pfad, zeile in stellen],
            ensure_ascii=False,
        )
    return "\n".join(f"{pfad}:{zeile}" for _, pfad, zeile in stellen)


def hauptprogramm(argumente: list[str]) -> int:
    wurzel = projektordner()
    eingaben = [argument for argument in argumente if argument != "--json"]
    if not eingaben:
        gefunden = verstöße(wurzel)
        print("\n".join(gefunden))
        return 1 if gefunden else 0
    stellen = spur(wurzel, eingaben[0])
    if stellen is None:
        print(f"Unbekanntes Kriterium: {eingaben[0]}", file=sys.stderr)
        return 1
    print(spurAlsText(stellen, alsJson="--json" in argumente))
    return 0


if __name__ == "__main__":
    sys.exit(hauptprogramm(sys.argv[1:]))
