"""Aufrufe von ruff und complexipy im Repo und die Konfiguration aus `pyproject.toml`."""

import shutil
import subprocess
import tomllib
from pathlib import Path

from gemeinsam.pfade import wurzel


def pyproject() -> dict:
    return tomllib.loads((wurzel / "pyproject.toml").read_text(encoding="utf-8"))


def ruffAufrufen(
    *argumente: str, cwd: Path = wurzel, config: Path = wurzel / "pyproject.toml"
) -> subprocess.CompletedProcess:
    """Rot, wenn ruff fehlt: `pyproject.toml` nennt es unter `dependency-groups`."""
    ruff = shutil.which("ruff") or shutil.which("ruff", path=str(wurzel / ".venv" / "bin"))
    assert ruff, "ruff ist nicht installiert (pyproject.toml, dependency-groups, entwicklung)"
    return subprocess.run(
        [ruff, "check", "--no-cache", "--config", str(config), *argumente],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def complexipyAufrufen(*pfade: str) -> subprocess.CompletedProcess:
    """Rot, wenn complexipy fehlt: `pyproject.toml` nennt es unter `dependency-groups`."""
    programm = shutil.which("complexipy") or shutil.which(
        "complexipy", path=str(wurzel / ".venv" / "bin")
    )
    assert programm, "complexipy ist nicht installiert (pyproject.toml, dependency-groups)"
    return subprocess.run(
        [programm, "--plain", "--failed", *pfade],
        cwd=wurzel,
        capture_output=True,
        text=True,
        check=False,
    )
