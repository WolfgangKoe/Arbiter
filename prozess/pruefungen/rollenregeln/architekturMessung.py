from dataclasses import dataclass
from pathlib import Path

from formregeln.erlaubteImporte import kastenNamen

produktOrdner = "technik/arbiter"
seiteOrdner = "technik/frontend"
seiteEndungen = (".html", ".css", ".js")
architekturOrdner = "technik/architektur"
übersichtDatei = "technik/architektur.md"
vertragOrdner = "technik/architektur/vertrag"
startDatei = "__main__.py"
paketDatei = "__init__.py"
architekturDateien = {"seite": "frontend"}
nichtGemessen = ("__pycache__",)


@dataclass(frozen=True)
class Knoten:
    pfad: str
    name: str
    zeichen: int
    istOrdner: bool
    kinder: tuple["Knoten", ...] = ()


@dataclass(frozen=True)
class Kasten:
    name: str
    bekannt: bool
    wurzel: Knoten | None
    architekturZeichen: int | None

    @property
    def codeZeichen(self) -> int:
        return self.wurzel.zeichen if self.wurzel else 0


def zeichen(dateien: list[Path]) -> int:
    return sum(len(datei.read_text(encoding="utf-8")) for datei in dateien if datei.is_file())


def leerePaketDatei(datei: Path) -> bool:
    return datei.name == paketDatei and not datei.read_text(encoding="utf-8").strip()


def dateiKnoten(datei: Path, wurzel: Path) -> Knoten:
    text = datei.read_text(encoding="utf-8")
    return Knoten(datei.relative_to(wurzel).as_posix(), datei.name, len(text), istOrdner=False)


def ordnerKnoten(ordner: Path, wurzel: Path, endungen: tuple[str, ...]) -> Knoten:
    kinder = []
    for eintrag in sorted(ordner.iterdir()):
        if eintrag.name in nichtGemessen:
            continue
        if eintrag.is_dir():
            kinder.append(ordnerKnoten(eintrag, wurzel, endungen))
        elif eintrag.suffix in endungen and not leerePaketDatei(eintrag):
            kinder.append(dateiKnoten(eintrag, wurzel))
    summe = sum(kind.zeichen for kind in kinder)
    pfad = ordner.relative_to(wurzel).as_posix()
    return Knoten(pfad, ordner.name, summe, istOrdner=True, kinder=tuple(kinder))


def architekturZeichen(wurzel: Path, kasten: str) -> int | None:
    if kasten == "start":
        return None
    datei = wurzel / architekturOrdner / f"{architekturDateien.get(kasten, kasten)}.md"
    return zeichen([datei]) if datei.is_file() else None


def wurzelKnoten(wurzel: Path, name: str) -> Knoten | None:
    produkt = wurzel / produktOrdner
    if name == "seite":
        ordner = wurzel / seiteOrdner
        return ordnerKnoten(ordner, wurzel, seiteEndungen) if ordner.is_dir() else None
    if name == "start":
        datei = produkt / startDatei
        return dateiKnoten(datei, wurzel) if datei.is_file() else None
    ordner = produkt / name
    if ordner.is_dir():
        return ordnerKnoten(ordner, wurzel, (".py",))
    datei = produkt / f"{name}.py"
    return dateiKnoten(datei, wurzel) if datei.is_file() else None


def unbekannteNamen(wurzel: Path) -> list[str]:
    produkt = wurzel / produktOrdner
    if not produkt.is_dir():
        return []
    namen = []
    for eintrag in sorted(produkt.iterdir()):
        name = eintrag.stem if eintrag.is_file() else eintrag.name
        gemeint = eintrag.suffix == ".py" or eintrag.is_dir()
        if gemeint and eintrag.name not in (*nichtGemessen, paketDatei, startDatei):
            if name not in kastenNamen:
                namen.append(name)
    return namen


def kästenMessen(wurzel: Path) -> list[Kasten]:
    bekannte = [
        Kasten(
            name,
            bekannt=True,
            wurzel=wurzelKnoten(wurzel, name),
            architekturZeichen=architekturZeichen(wurzel, name),
        )
        for name in kastenNamen
    ]
    fremde = [
        Kasten(name, bekannt=False, wurzel=wurzelKnoten(wurzel, name), architekturZeichen=None)
        for name in unbekannteNamen(wurzel)
    ]
    return bekannte + fremde


def übersichtUndVertrag(wurzel: Path) -> tuple[int, int]:
    vertrag = [datei for datei in (wurzel / vertragOrdner).rglob("*") if datei.is_file()]
    return zeichen([wurzel / übersichtDatei]), zeichen(vertrag)
