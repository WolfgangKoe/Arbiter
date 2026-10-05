"""eslint und stylelint über `technik/frontend/` (ablauf.md, Werkzeuge; wir.md 1, 5, 8)."""

import subprocess
import sys
from pathlib import Path

from gemeinsam.pfade import frontendOrdner
from rollenregeln.agenten import projektordner


def werkzeugAufrufen(wurzel: Path, werkzeug: str, *argumente: str) -> str:
    """Ausgabe des Werkzeugs, wenn es Verstöße oder Fehler meldet, sonst leer; fehlt es, rot."""
    programm = wurzel / "node_modules" / ".bin" / werkzeug
    assert programm.exists(), f"{werkzeug} fehlt: `npm install` in der Wurzel (package.json)"
    lauf = subprocess.run(
        [programm, *argumente], cwd=wurzel, capture_output=True, text=True, check=False
    )
    return f"{lauf.stdout}{lauf.stderr}" if lauf.returncode else ""


def eslintVerstöße(wurzel: Path) -> str:
    ziel = f"{frontendOrdner}/**/*.js"
    return werkzeugAufrufen(wurzel, "eslint", "--no-error-on-unmatched-pattern", ziel)


def stylelintVerstöße(wurzel: Path) -> str:
    ziel = f"{frontendOrdner}/**/*.css"
    return werkzeugAufrufen(wurzel, "stylelint", "--allow-empty-input", ziel)


def verstöße(wurzel: Path) -> list[str]:
    meldungen = (eslintVerstöße(wurzel), stylelintVerstöße(wurzel))
    return [meldung for meldung in meldungen if meldung]


if __name__ == "__main__":
    gefunden = verstöße(projektordner())
    print("\n".join(gefunden))
    sys.exit(1 if gefunden else 0)
