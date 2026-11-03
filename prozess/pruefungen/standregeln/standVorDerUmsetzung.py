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


def standVorDerUmsetzung(wurzel: Path, itemName: str) -> str:
    zeile = f"- [x] Implementierer: Tests zu Item {itemName.removesuffix('.md')} grün"
    if zeile not in git(wurzel, "show", "HEAD:handoff/plan.md"):
        return "HEAD"
    for commit in git(wurzel, "log", "--format=%H", "-S", zeile, "--", "handoff/plan.md").split():
        if zeile in git(wurzel, "show", f"{commit}:handoff/plan.md"):
            return f"{commit}^"
    return "HEAD"


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


def mitKopie(wurzel: Path, itemName: str) -> tuple[tempfile.TemporaryDirectory, Path]:
    ordner = tempfile.TemporaryDirectory(prefix="vorDerUmsetzung")
    kopie = Path(ordner.name) / "kopie"
    shutil.copytree(
        wurzel, kopie, ignore=shutil.ignore_patterns(*nichtKopiert), symlinks=True
    )
    produktEinsetzen(wurzel, kopie, standVorDerUmsetzung(wurzel, itemName))
    return ordner, kopie
