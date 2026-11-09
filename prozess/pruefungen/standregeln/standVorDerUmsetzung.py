import shutil
import subprocess
import tempfile
from pathlib import Path

produktordner = ("technik/arbiter", "technik/frontend")
nichtKopiert = (".git", ".venv", "node_modules", "Arbiter-old", "ArbiterMap", "__pycache__")


def git(wurzel: Path, *teile: str) -> str:
    lauf = subprocess.run(
        ["git", *teile], cwd=wurzel, capture_output=True, text=True, check=False
    )
    return lauf.stdout if lauf.returncode == 0 else ""


def commits(wurzel: Path, *auswahl: str) -> list[str]:
    return git(wurzel, "log", "--reverse", "--format=%H", *auswahl).split()


def ersterCommitMit(wurzel: Path, zeile: str) -> str:
    for commit in commits(wurzel, "-S", zeile, "--", "handoff/plan.md"):
        if zeile in git(wurzel, "show", f"{commit}:handoff/plan.md").splitlines():
            return commit
    return ""


def ersteUmsetzung(wurzel: Path, item: str) -> str:
    getestet = ersterCommitMit(wurzel, f"- [x] Testautor: Tests zu Item {item}")
    grün = ersterCommitMit(wurzel, f"- [x] Implementierer: Tests zu Item {item} grün")
    if not getestet:
        return grün
    for produkt in commits(wurzel, f"{getestet}..HEAD", "--", *produktordner):
        if not grün or commits(wurzel, f"{produkt}..{grün}"):
            return produkt
        break
    return grün


def standVorDerUmsetzung(wurzel: Path, itemName: str) -> str:
    umsetzung = ersteUmsetzung(wurzel, itemName.removesuffix(".md"))
    return f"{umsetzung}^" if umsetzung else "HEAD"


def standJeTest(wurzel: Path, itemName: str, kennungen: list[str]) -> dict[str, list[str]]:
    umsetzung = ersteUmsetzung(wurzel, itemName.removesuffix(".md"))
    nachgereicht = set(commits(wurzel, f"{umsetzung}..HEAD")) if umsetzung else set()
    vorher = f"{umsetzung}^" if umsetzung else "HEAD"
    gruppen: dict[str, list[str]] = {}
    for kennung in kennungen:
        pfad, _, name = kennung.partition("::")
        hinzugefügt = commits(wurzel, "-S", f"def {name}", "--", pfad)
        stand = vorher
        if umsetzung and not hinzugefügt:
            stand = "HEAD"
        elif hinzugefügt and hinzugefügt[0] in nachgereicht:
            stand = hinzugefügt[0]
        gruppen.setdefault(stand, []).append(kennung)
    return gruppen


def produktEinsetzen(wurzel: Path, kopie: Path, stand: str) -> None:
    for ordner in produktordner:
        shutil.rmtree(kopie / ordner, ignore_errors=True)
    vorhanden = [
        ordner
        for ordner in produktordner
        if git(wurzel, "ls-tree", "-d", "--name-only", stand, ordner).strip()
    ]
    if not vorhanden:
        return
    archiv = subprocess.run(
        ["git", "archive", stand, *vorhanden], cwd=wurzel, capture_output=True, check=True
    ).stdout
    subprocess.run(["tar", "-x", "-C", str(kopie)], input=archiv, check=True)


def mitKopie(wurzel: Path, stand: str) -> tuple[tempfile.TemporaryDirectory, Path]:
    ordner = tempfile.TemporaryDirectory(prefix="vorDerUmsetzung")
    kopie = Path(ordner.name) / "kopie"
    shutil.copytree(
        wurzel, kopie, ignore=shutil.ignore_patterns(*nichtKopiert), symlinks=True
    )
    produktEinsetzen(wurzel, kopie, stand)
    return ordner, kopie
