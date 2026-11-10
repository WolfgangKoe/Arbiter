import subprocess
from pathlib import Path
from typing import NamedTuple

from gemeinsam.pfade import relativZurWurzel


class Freigabe(NamedTuple):
    kennung: str
    betreff: str


def gitAusgabe(wurzel: Path, *argumente: str) -> str:
    return subprocess.run(
        ["git", *argumente], cwd=wurzel, capture_output=True, text=True, check=False
    ).stdout


def indexGesperrt(wurzel: Path) -> bool:
    sperre = gitAusgabe(wurzel, "rev-parse", "--git-path", "index.lock").strip()
    return bool(sperre) and (wurzel / sperre).exists()


freigabenJeStand: dict[tuple[Path, str], list[Freigabe]] = {}


def freigabenLesen(wurzel: Path) -> list[Freigabe]:
    gefunden = []
    for zeile in gitAusgabe(wurzel, "log", "--format=%H %s").splitlines():
        kennung, _, betreff = zeile.partition(" ")
        if betreff.startswith("Freigabe "):
            gefunden.append(Freigabe(kennung, betreff))
    return gefunden


def gitOrdner(wurzel: Path) -> Path:
    punktGit = wurzel / ".git"
    if punktGit.is_file():
        verweis = punktGit.read_text(encoding="utf-8").removeprefix("gitdir:").strip()
        return wurzel / verweis
    return punktGit


def kopfKennung(wurzel: Path) -> str:
    ordner = gitOrdner(wurzel)
    kopf = (ordner / "HEAD").read_text(encoding="utf-8").strip() if ordner.is_dir() else ""
    if not kopf.startswith("ref: "):
        return kopf or gitAusgabe(wurzel, "rev-parse", "HEAD").strip()
    zweig = kopf.removeprefix("ref: ")
    gemeinsamerOrdner = ordner
    if (ordner / "commondir").is_file():
        gemeinsamerOrdner = ordner / (ordner / "commondir").read_text(encoding="utf-8").strip()
    zweigDatei = gemeinsamerOrdner / zweig
    if zweigDatei.is_file():
        return zweigDatei.read_text(encoding="utf-8").strip()
    return gitAusgabe(wurzel, "rev-parse", "HEAD").strip()


def freigaben(wurzel: Path) -> list[Freigabe]:
    stand = (wurzel.resolve(), kopfKennung(wurzel))
    if stand not in freigabenJeStand:
        freigabenJeStand[stand] = freigabenLesen(wurzel)
    return freigabenJeStand[stand]


def freigabeCommit(wurzel: Path, gegenstand: str, nummer: int) -> str | None:
    for freigabe in freigaben(wurzel):
        if freigabe.betreff == f"Freigabe {gegenstand} {nummer}":
            return freigabe.kennung
    return None


def letzteFreigabe(wurzel: Path) -> str | None:
    alle = freigaben(wurzel)
    return alle[0].kennung if alle else None


def dateiBeiCommit(wurzel: Path, kennung: str, datei: Path) -> str:
    pfad = relativZurWurzel(datei, wurzel)
    assert pfad is not None, f"{datei} liegt außerhalb von {wurzel}"
    return gitAusgabe(wurzel, "show", f"{kennung}:{pfad}")


betreffeJeStand: dict[tuple[Path, str, str], list[str]] = {}


def betreffeSeit(wurzel: Path, kennung: str) -> list[str]:
    stand = (wurzel.resolve(), kopfKennung(wurzel), kennung)
    if stand not in betreffeJeStand:
        betreffeJeStand[stand] = gitAusgabe(
            wurzel, "log", "--format=%s", f"{kennung}..HEAD"
        ).splitlines()
    return betreffeJeStand[stand]
