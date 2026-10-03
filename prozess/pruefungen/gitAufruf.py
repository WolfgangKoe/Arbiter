"""Ein lesender Aufruf von git im Projektordner."""

import subprocess
from pathlib import Path


def gitAusgabe(wurzel: Path, *argumente: str) -> str:
    return subprocess.run(
        ["git", *argumente], cwd=wurzel, capture_output=True, text=True, check=False
    ).stdout
