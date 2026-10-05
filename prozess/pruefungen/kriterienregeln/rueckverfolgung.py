"""Kriterium ↔ Akzeptanztest: Jedes Kriterium hat einen Test, jeder Test ein Kriterium."""

import re
import sys
from pathlib import Path
from typing import NamedTuple

from gemeinsam.pfade import akzeptanzOrdner, anforderungsOrdner, projektordner
from kriterienregeln.kriterium import (
    Anforderungsnummer,
    Kriteriumsnummer,
    anforderungenMitZeile,
    anforderungKennung,
    anforderungVon,
    doppelte,
    getesteKriterien,
    kennung,
    kriterien,
    kriterienMitZeile,
    pfadVon,
)
from kriterienregeln.spur import spur, spurAlsText
from lesen.plan import freigegebenerPlan, offeneItemTexte


class Fehlend(NamedTuple):
    """Ein Kriterium ohne Test oder eine Anforderung ohne Testdatei, mit allen ihren Kriterien."""

    kennung: str
    kriterien: set[Kriteriumsnummer]


class Zuordnung(NamedTuple):
    anforderung: Anforderungsnummer
    testdatei: Path
    verlangt: set[Kriteriumsnummer]


def anforderungenDerDatei(anforderungsdatei: Path) -> list[Anforderungsnummer]:
    """Die Anforderungen der Datei, auch die, von denen nur Kriterien da sind."""
    gefunden = {anforderung for anforderung, _ in anforderungenMitZeile(anforderungsdatei)}
    gefunden |= {anforderungVon(kriterium) for kriterium in kriterien(anforderungsdatei)}
    return sorted(gefunden)


def sammeldateiZu(wurzel: Path, anforderungsdatei: Path) -> Path:
    pfad = anforderungsdatei.relative_to(wurzel / anforderungsOrdner).with_suffix("")
    return wurzel / akzeptanzOrdner / pfad.parent / f"{pfad.name}Test.py"


def einzeldateiZu(wurzel: Path, anforderungsdatei: Path, anforderung: Anforderungsnummer) -> Path:
    pfad = anforderungsdatei.relative_to(wurzel / anforderungsOrdner).with_suffix("")
    kürzel, nummer = anforderung
    return wurzel / akzeptanzOrdner / pfad / f"{kürzel.lower()}{nummer}Test.py"


def nennt(text: str, kriterium: Kriteriumsnummer) -> bool:
    """Der Text nennt das Kriterium (`AUF-1.8`) oder seine Anforderung (`AUF-1`)."""
    kürzel, haupt, unter = kriterium
    muster = rf"\b{kürzel}-{haupt}(?:\.{unter}(?!\d)|(?!\d)(?!\.\d))"
    return re.search(muster, text) is not None


def umfasst(itemTexte: list[str], kriterium: Kriteriumsnummer) -> bool:
    """Ein Itemtext nennt das Kriterium (`AUF-1.8`) oder seine Anforderung (`AUF-1`)."""
    return any(nennt(text, kriterium) for text in itemTexte)


def itemTexteDesFreigegebenenPlans(wurzel: Path) -> list[str]:
    return offeneItemTexte(wurzel) if freigegebenerPlan(wurzel) is not None else []


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


def anforderungUmfasst(itemTexte: list[str], verlangt: set[Kriteriumsnummer]) -> bool:
    return any(umfasst(itemTexte, kriterium) for kriterium in verlangt)


def sammeldateiGilt(
    sammeldatei: Path, spätereVerlangt: list[set[Kriteriumsnummer]], itemTexte: list[str]
) -> bool:
    """Die Sammeldatei liegt vor, und kein Plan umfasst eine spätere Anforderung."""
    return sammeldatei.is_file() and not any(
        anforderungUmfasst(itemTexte, verlangt) for verlangt in spätereVerlangt
    )


def testdateiWählen(
    wurzel: Path,
    anforderungsdatei: Path,
    anforderung: Anforderungsnummer,
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
    verlangt: dict[Anforderungsnummer, set[Kriteriumsnummer]] = {
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
        if getestet:
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
    return anforderungUmfasst(itemTexte, fehlend.kriterien)


def fehlendeTests(wurzel: Path, itemTexte: list[str]) -> list[Fehlend]:
    """Kriterien ohne Test und Anforderungen ohne Testdatei; die Itemtexte wählen die Testdatei."""
    gefunden = []
    for anforderungsdatei in sorted((wurzel / anforderungsOrdner).rglob("*.md")):
        for zuordnung in zuordnungen(wurzel, anforderungsdatei, itemTexte):
            if not zuordnung.verlangt:
                continue
            if not zuordnung.testdatei.is_file():
                kennungDerAnforderung = anforderungKennung(zuordnung.anforderung)
                gefunden.append(Fehlend(kennungDerAnforderung, zuordnung.verlangt))
                continue
            fehlend = zuordnung.verlangt - getesteKriterien(zuordnung.testdatei)
            gefunden += [Fehlend(kennung(kriterium), {kriterium}) for kriterium in sorted(fehlend)]
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


def hauptprogramm(argumente: list[str]) -> int:
    wurzel = projektordner()
    if not argumente:
        gefunden = verstöße(wurzel)
        print("\n".join(gefunden))
        return 1 if gefunden else 0
    stellen = spur(wurzel, argumente[0])
    if stellen is None:
        print(f"Unbekanntes Kriterium: {argumente[0]}", file=sys.stderr)
        return 1
    print(spurAlsText(stellen))
    return 0


if __name__ == "__main__":
    sys.exit(hauptprogramm(sys.argv[1:]))
