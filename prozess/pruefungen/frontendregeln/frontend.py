"""eslint und stylelint über `technik/frontend/` (`prozess/ablauf/werkzeuge.md`; wir.md 1, 5, 8)."""

import subprocess
import sys
from pathlib import Path

from formregeln.technikphase import technikGeprüft
from gemeinsam.pfade import frontendOrdner, projektordner


def werkzeugAufrufen(wurzel: Path, werkzeug: str, *argumente: str) -> str:
    """Ausgabe des Werkzeugs, wenn es Verstöße oder Fehler meldet, sonst leer; fehlt es, rot."""
    programm = wurzel / "node_modules" / ".bin" / werkzeug
    assert programm.exists(), f"{werkzeug} fehlt: `npm install` in der Wurzel (package.json)"
    lauf = subprocess.run(
        [programm, *argumente], cwd=wurzel, capture_output=True, text=True, check=False
    )
    return f"{lauf.stdout}{lauf.stderr}" if lauf.returncode else ""


def eslintVerstöße(wurzel: Path, kommentareGeprüft: bool = True) -> str:  # noqa: FBT001, FBT002
    ziel = f"{frontendOrdner}/**/*.js"
    ohneKommentarregel = [] if kommentareGeprüft else ["--rule", "arbiter/kommentare: off"]
    return werkzeugAufrufen(
        wurzel, "eslint", "--no-error-on-unmatched-pattern", *ohneKommentarregel, ziel
    )


def stylelintVerstöße(wurzel: Path) -> str:
    ziel = f"{frontendOrdner}/**/*.css"
    return werkzeugAufrufen(wurzel, "stylelint", "--allow-empty-input", ziel)


def verstöße(wurzel: Path) -> list[str]:
    meldungen = (eslintVerstöße(wurzel, technikGeprüft(wurzel)), stylelintVerstöße(wurzel))
    return [meldung for meldung in meldungen if meldung]


if __name__ == "__main__":
    gefunden = verstöße(projektordner())
    print("\n".join(gefunden))
    sys.exit(1 if gefunden else 0)
