import hashlib
import json
from pathlib import Path
from typing import NamedTuple

standQuellen = ("technik", "pyproject.toml", "domaene/daten")
mutantenbauer = "prozess/pruefungen/mutationsregeln/mutanten.py"
ohneStand = ("__pycache__", "node_modules", ".egg-info")
gleichwertigDatei = Path(__file__).with_name("gleichwertig.json")


class Gleichwertig(NamedTuple):
    datei: str
    quelle: str
    fehler: str


def dateienDes(wurzel: Path, name: str) -> list[Path]:
    pfad = wurzel / name
    if pfad.is_file():
        return [pfad]
    return sorted(
        datei
        for datei in pfad.rglob("*")
        if datei.is_file() and not any(teil in datei.as_posix() for teil in ohneStand)
    )


def standKennung(wurzel: Path) -> str:
    summe = hashlib.sha256()
    for name in (*standQuellen, mutantenbauer):
        for datei in dateienDes(wurzel, name):
            summe.update(datei.relative_to(wurzel).as_posix().encode())
            summe.update(datei.read_bytes())
    return summe.hexdigest()


def gemerkt(ablage: Path | None, stand: str) -> dict[str, bool]:
    if ablage is None or not ablage.is_file():
        return {}
    try:
        inhalt = json.loads(ablage.read_text(encoding="utf-8"))
    except ValueError:
        return {}
    return inhalt["ergebnisse"] if inhalt.get("stand") == stand else {}


def merken(ablage: Path | None, stand: str, ergebnisse: dict[str, bool]) -> None:
    if ablage is None:
        return
    ablage.parent.mkdir(parents=True, exist_ok=True)
    ablage.write_text(
        json.dumps({"stand": stand, "ergebnisse": ergebnisse}, indent=1), encoding="utf-8"
    )


def gleichwertigeLesen(datei: Path = gleichwertigDatei) -> set[Gleichwertig]:
    if not datei.is_file():
        return set()
    return {
        Gleichwertig(eintrag["datei"], eintrag["quelle"], eintrag["fehler"])
        for eintrag in json.loads(datei.read_text(encoding="utf-8"))
        if eintrag["grund"].strip()
    }
