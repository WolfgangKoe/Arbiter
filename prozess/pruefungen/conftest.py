"""Legt die Themenordner in den Importpfad und stellt das git-Archiv für Tests bereit."""

import subprocess
from pathlib import Path

import pytest

identität = ("-c", "user.name=t", "-c", "user.email=t@t")


class GitRepo:
    """Ein frisches git-Archiv im Ordner `ordner`, auf das die Tests schreiben."""

    def __init__(self, ordner: Path):
        self.ordner = ordner
        self.git("init", "-q")

    def git(self, *argumente: str) -> None:
        subprocess.run(
            ["git", *identität, *argumente], cwd=self.ordner, check=True, capture_output=True
        )

    def festhalten(self, betreff: str = "x", *zusatz: str) -> None:
        """Nimmt alle Dateien auf und committet, auch ohne Änderung."""
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", betreff, *zusatz)


@pytest.fixture
def gitRepo(tmp_path):
    return GitRepo(tmp_path)
