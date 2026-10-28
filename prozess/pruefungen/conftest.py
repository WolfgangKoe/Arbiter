import subprocess
from pathlib import Path

import pytest

identität = ("-c", "user.name=t", "-c", "user.email=t@t")


class GitRepo:
    def __init__(self, ordner: Path):
        self.ordner = ordner
        self.git("init", "-q")

    def git(self, *argumente: str) -> None:
        subprocess.run(
            ["git", *identität, *argumente], cwd=self.ordner, check=True, capture_output=True
        )

    def festhalten(self, betreff: str = "x", *zusatz: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", betreff, *zusatz)


@pytest.fixture
def gitRepo(tmp_path):
    return GitRepo(tmp_path)
