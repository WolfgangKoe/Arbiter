import os
import subprocess
from pathlib import Path

import pytest

identität = ("-c", "user.name=t", "-c", "user.email=t@t")


def umgebungOhneGit() -> dict[str, str]:
    return {name: wert for name, wert in os.environ.items() if not name.startswith("GIT_")}


for gitName in [name for name in os.environ if name.startswith("GIT_")]:
    del os.environ[gitName]


class GitRepo:
    def __init__(self, ordner: Path):
        self.ordner = ordner
        self.git("init", "-q")

    def git(self, *argumente: str) -> None:
        subprocess.run(
            ["git", *identität, *argumente],
            cwd=self.ordner,
            check=True,
            capture_output=True,
            env=umgebungOhneGit(),
        )

    def festhalten(self, betreff: str = "x", *zusatz: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", betreff, *zusatz)


@pytest.fixture
def gitRepo(tmp_path):
    return GitRepo(tmp_path)
