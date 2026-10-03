"""Kriterium ↔ Akzeptanztest: Jedes Kriterium hat einen Test, jeder Test ein Kriterium."""

import ast
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import NamedTuple

from agenten import projektordner
from plan import freigegebenerPlan, offeneItemTexte

anforderungsnummer = tuple[str, int]
kriteriumsnummer = tuple[str, int, int]
fundstelle = tuple[str, str, int]  # Art, Pfad, Zeile


class Fehlend(NamedTuple):
    """Ein Kriterium ohne Test oder (ohne `kriterium`) eine Anforderung ohne Testdatei."""

    kennung: str
    anforderung: anforderungsnummer
    kriterium: kriteriumsnummer | None


class Zuordnung(NamedTuple):
    anforderung: anforderungsnummer
    testdatei: Path
    verlangt: set[kriteriumsnummer]


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
    kürzel, nummer = anforderung
    return f"{kürzel}-{nummer}"


def anforderungVon(kriterium: kriteriumsnummer) -> anforderungsnummer:
    kürzel, hauptnummer, _ = kriterium
    return kürzel, hauptnummer


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
    gefunden |= {anforderungVon(kriterium) for kriterium in kriterien(anforderungsdatei)}
    return sorted(gefunden)


def sammeldateiZu(wurzel: Path, anforderungsdatei: Path) -> Path:
    pfad = anforderungsdatei.relative_to(wurzel / anforderungsOrdner).with_suffix("")
    return wurzel / akzeptanzOrdner / pfad.parent / f"{pfad.name}Test.py"


def einzeldateiZu(wurzel: Path, anforderungsdatei: Path, anforderung: anforderungsnummer) -> Path:
    pfad = anforderungsdatei.relative_to(wurzel / anforderungsOrdner).with_suffix("")
    kürzel, nummer = anforderung
    return wurzel / akzeptanzOrdner / pfad / f"{kürzel.lower()}{nummer}Test.py"


def nennt(text: str, kriterium: kriteriumsnummer) -> bool:
    """Der Text nennt das Kriterium (`AUF-1.8`) oder seine Anforderung (`AUF-1`)."""
    kürzel, haupt, unter = kriterium
    muster = rf"\b{kürzel}-{haupt}(?:\.{unter}(?!\d)|(?!\d)(?!\.\d))"
    return re.search(muster, text) is not None


def umfasst(itemTexte: list[str], kriterium: kriteriumsnummer) -> bool:
    """Ein Itemtext nennt das Kriterium (`AUF-1.8`) oder seine Anforderung (`AUF-1`)."""
    return any(nennt(text, kriterium) for text in itemTexte)


def itemTexteDesFreigegebenenPlans(wurzel: Path) -> list[str]:
    return offeneItemTexte(wurzel) if freigegebenerPlan(wurzel) is not None else []


def pfadVon(wurzel: Path, datei: Path) -> str:
    return datei.relative_to(wurzel).as_posix()


def testdateiVerstöße(
    wurzel: Path,
    anforderungsdatei: Path,
    zuordnung: Zuordnung,
    itemTexte: list[str],
) -> list[str]:
    meldungen = []
    getestet = getesteKriterien(zuordnung.testdatei)
    pfad = pfadVon(wurzel, zuordnung.testdatei)
    meldungen += [
        f"{pfad}: {kennung(kriterium)} hat keinen Test"
        for kriterium in sorted(zuordnung.verlangt - getestet)
        if umfasst(itemTexte, kriterium)
    ]
    meldungen += [
        f"{pfad}: Test zu {kennung(kriterium)}, das in {pfadVon(wurzel, anforderungsdatei)} "
        "fehlt oder zu einer anderen Anforderung gehört"
        for kriterium in sorted(getestet - zuordnung.verlangt)
    ]
    return meldungen


def anforderungUmfasst(itemTexte: list[str], verlangt: set[kriteriumsnummer]) -> bool:
    return any(umfasst(itemTexte, kriterium) for kriterium in verlangt)


def sammeldateiGilt(
    sammeldatei: Path, spätereVerlangt: list[set[kriteriumsnummer]], itemTexte: list[str]
) -> bool:
    """Die Sammeldatei liegt vor, und kein Plan umfasst eine spätere Anforderung."""
    return sammeldatei.is_file() and not any(
        anforderungUmfasst(itemTexte, verlangt) for verlangt in spätereVerlangt
    )


def testdateiWählen(
    wurzel: Path,
    anforderungsdatei: Path,
    anforderung: anforderungsnummer,
    *,
    gilt: bool,
) -> Path:
    """Die Sammeldatei, wenn sie für die erste Anforderung gilt, sonst die Einzeldatei."""
    if gilt:
        return sammeldateiZu(wurzel, anforderungsdatei)
    return einzeldateiZu(wurzel, anforderungsdatei, anforderung)


def zuordnungen(wurzel: Path, anforderungsdatei: Path, itemTexte: list[str]) -> list[Zuordnung]:
    """Je Anforderung der Datei die Testdatei, die für sie gilt, und ihre Kriterien."""
    # Regel: Architektur T1
    anforderungen = anforderungenDerDatei(anforderungsdatei)
    if not anforderungen:
        return []
    erste, *spätere = anforderungen
    verlangt: dict[anforderungsnummer, set[kriteriumsnummer]] = {
        anforderung: set() for anforderung in anforderungen
    }
    for kriterium in kriterien(anforderungsdatei):
        verlangt[anforderungVon(kriterium)].add(kriterium)
    späterVerlangt = [verlangt[nummer] for nummer in spätere]
    gilt = sammeldateiGilt(sammeldateiZu(wurzel, anforderungsdatei), späterVerlangt, itemTexte)
    return [
        Zuordnung(
            anforderung,
            testdateiWählen(
                wurzel, anforderungsdatei, anforderung, gilt=gilt and anforderung == erste
            ),
            verlangt[anforderung],
        )
        for anforderung in anforderungen
    ]


def doppelteKennungen(anforderungsdatei: Path) -> list[str]:
    return doppelte(
        [kennung(kriterium) for kriterium, _ in kriterienMitZeile(anforderungsdatei)]
        + [anforderungKennung(nummer) for nummer, _ in anforderungenMitZeile(anforderungsdatei)]
    )


def sammeldateiNebenEinzeldatei(
    wurzel: Path, anforderungsdatei: Path, zuordnung: Zuordnung, itemTexte: list[str]
) -> list[str]:
    """Eine vorhandene Einzeldatei wird geprüft, auch wenn die Sammeldatei gilt."""
    einzeldatei = einzeldateiZu(wurzel, anforderungsdatei, zuordnung.anforderung)
    if not einzeldatei.is_file() or einzeldatei == zuordnung.testdatei:
        return []
    meldungen = [
        f"{pfadVon(wurzel, einzeldatei)}: neben {pfadVon(wurzel, zuordnung.testdatei)}, "
        "je Anforderung eine Testdatei"
    ]
    einzelne = Zuordnung(zuordnung.anforderung, einzeldatei, zuordnung.verlangt)
    return meldungen + testdateiVerstöße(wurzel, anforderungsdatei, einzelne, itemTexte)


def anforderungsVerstöße(wurzel: Path, anforderungsdatei: Path, itemTexte: list[str]) -> list[str]:
    pfad = pfadVon(wurzel, anforderungsdatei)
    meldungen = [f"{pfad}: {name} steht zweimal" for name in doppelteKennungen(anforderungsdatei)]
    sammeldatei = sammeldateiZu(wurzel, anforderungsdatei)
    zugeordnet = zuordnungen(wurzel, anforderungsdatei, itemTexte)
    if sammeldatei.is_file() and not zugeordnet:
        getestet = sorted(getesteKriterien(sammeldatei))
        gefunden = ", ".join(kennung(kriterium) for kriterium in getestet)
        meldungen.append(f"{pfadVon(wurzel, sammeldatei)}: Tests ohne Anforderung: {gefunden}")
    elif sammeldatei.is_file() and sammeldatei not in {eintrag.testdatei for eintrag in zugeordnet}:
        meldungen.append(
            f"{pfadVon(wurzel, sammeldatei)}: teilen nach Anforderung, "
            f"je Anforderung eine Datei {sammeldatei.stem.removesuffix('Test')}/<kürzel><n>Test.py"
        )
    for zuordnung in zugeordnet:
        if zuordnung.testdatei.is_file():
            meldungen += testdateiVerstöße(wurzel, anforderungsdatei, zuordnung, itemTexte)
        elif anforderungUmfasst(itemTexte, zuordnung.verlangt):
            meldungen.append(f"{pfadVon(wurzel, zuordnung.testdatei)} fehlt")
        meldungen += sammeldateiNebenEinzeldatei(wurzel, anforderungsdatei, zuordnung, itemTexte)
    return meldungen


def verstöße(wurzel: Path) -> list[str]:
    itemTexte = itemTexteDesFreigegebenenPlans(wurzel)
    meldungen = []
    for anforderungsdatei in sorted((wurzel / anforderungsOrdner).rglob("*.md")):
        meldungen += anforderungsVerstöße(wurzel, anforderungsdatei, itemTexte)
    return meldungen


def nenntFehlendes(itemTexte: list[str], fehlend: Fehlend) -> bool:
    """Ein Itemtext nennt das Kriterium oder die Anforderung (`AUF-1`, auch als `AUF-1.8`)."""
    if fehlend.kriterium is not None:
        return umfasst(itemTexte, fehlend.kriterium)
    kürzel, nummer = fehlend.anforderung
    return any(re.search(rf"\b{kürzel}-{nummer}(?!\d)", text) for text in itemTexte)


def fehlendeTests(wurzel: Path, itemTexte: list[str]) -> list[Fehlend]:
    """Kriterien ohne Test und Anforderungen ohne Testdatei, unabhängig vom Plan."""
    gefunden = []
    for anforderungsdatei in sorted((wurzel / anforderungsOrdner).rglob("*.md")):
        for zuordnung in zuordnungen(wurzel, anforderungsdatei, itemTexte):
            if not zuordnung.testdatei.is_file():
                gefunden.append(
                    Fehlend(anforderungKennung(zuordnung.anforderung), zuordnung.anforderung, None)
                )
                continue
            fehlend = zuordnung.verlangt - getesteKriterien(zuordnung.testdatei)
            gefunden += [
                Fehlend(kennung(kriterium), zuordnung.anforderung, kriterium)
                for kriterium in sorted(fehlend)
            ]
    return gefunden


def wartende(wurzel: Path) -> list[str]:
    """Fehlendes, das kein offenes Item eines freigegebenen Plans nennt."""
    itemTexte = itemTexteDesFreigegebenenPlans(wurzel)
    return [
        fehlend.kennung
        for fehlend in fehlendeTests(wurzel, itemTexte)
        if not nenntFehlendes(itemTexte, fehlend)
    ]


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
