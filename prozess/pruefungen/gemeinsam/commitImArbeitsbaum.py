import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

from gemeinsam.pfade import projektordner

befehlsmodul = "gemeinsam.commitImArbeitsbaum"
zweig = "dev"


class Ergebnis(NamedTuple):
    erfolg: bool
    meldung: str


def git(ordner: Path, *argumente: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *argumente], cwd=ordner, capture_output=True, text=True, check=False
    )


def geänderteDateien(wurzel: Path, pfade: list[str]) -> list[tuple[str, bool]]:
    ausgabe = git(wurzel, "status", "--porcelain=v1", "-z", "--no-renames", "-uall", "--", *pfade)
    einträge = [eintrag for eintrag in ausgabe.stdout.split("\0") if eintrag]
    return [(eintrag[3:], (wurzel / eintrag[3:]).exists()) for eintrag in einträge]


def übernehmen(quelle: Path, arbeitsbaum: Path, pfade: list[str]) -> None:
    for datei, existiert in geänderteDateien(quelle, pfade):
        ziel = arbeitsbaum / datei
        if existiert:
            ziel.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(quelle / datei, ziel, follow_symlinks=False)
        else:
            ziel.unlink(missing_ok=True)


def knotenModulesVerlinken(wurzel: Path, arbeitsbaum: Path) -> None:
    if (wurzel / "node_modules").exists():
        (arbeitsbaum / "node_modules").symlink_to(wurzel / "node_modules")


def committen(arbeitsbaum: Path, nachricht: str, pfade: list[str]) -> subprocess.CompletedProcess:
    if pfade:
        git(arbeitsbaum, "add", "-A", "--", *pfade)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8") as datei:
        datei.write(nachricht)
        datei.flush()
        leer = [] if pfade else ["--allow-empty"]
        return git(arbeitsbaum, "commit", "-q", *leer, "-F", datei.name)


def festschreiben(
    wurzel: Path, quelle: Path, arbeitsbaum: Path, alt: str, pfade: list[str]
) -> Ergebnis:
    neu = git(arbeitsbaum, "rev-parse", "HEAD").stdout.strip()
    setzen = git(wurzel, "update-ref", f"refs/heads/{zweig}", neu, alt)
    if setzen.returncode != 0:
        return Ergebnis(
            erfolg=False, meldung=f"{zweig} bewegte sich seit dem Start, Befehl erneut ausführen."
        )
    if pfade:
        git(quelle, "reset", "-q", "--", *pfade)
    return Ergebnis(erfolg=True, meldung=f"Commit {neu[:7]} auf {zweig}")


def commitImArbeitsbaum(
    wurzel: Path, nachricht: str, pfade: list[str], quelle: Path | None = None
) -> Ergebnis:
    quelle = quelle or wurzel
    alt = git(wurzel, "rev-parse", zweig).stdout.strip()
    arbeitsbaum = Path(tempfile.mkdtemp(prefix="arbiterCommit"))
    try:
        git(wurzel, "worktree", "add", "-q", "--detach", str(arbeitsbaum), alt)
        knotenModulesVerlinken(wurzel, arbeitsbaum)
        übernehmen(quelle, arbeitsbaum, pfade)
        ergebnis = committen(arbeitsbaum, nachricht, pfade)
        if ergebnis.returncode != 0:
            return Ergebnis(erfolg=False, meldung=(ergebnis.stdout + ergebnis.stderr).strip())
        return festschreiben(wurzel, quelle, arbeitsbaum, alt, pfade)
    finally:
        git(wurzel, "worktree", "remove", "--force", str(arbeitsbaum))
        shutil.rmtree(arbeitsbaum, ignore_errors=True)
        git(wurzel, "worktree", "prune")


if __name__ == "__main__":
    argumente = sys.argv[1:]
    quelle = None
    if argumente[:1] == ["--aus"]:
        quelle = Path(argumente[1]).resolve()
        argumente = argumente[2:]
    ergebnis = commitImArbeitsbaum(projektordner(), argumente[0], argumente[1:], quelle)
    print(ergebnis.meldung)
    sys.exit(0 if ergebnis.erfolg else 1)
