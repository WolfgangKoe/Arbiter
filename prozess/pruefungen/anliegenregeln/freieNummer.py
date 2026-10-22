"""Befehl: Nennt die erste freie Anliegen-Nummer im Bereich, den der Auftrag zuteilt."""

import sys

from gemeinsam.pfade import projektordner
from lesen.anliegenKopf import freieNummer

aufrufteileErsteUndLetzteNummer = 2
aufruf = "python3 prozess/pruefungen/gemeinsam/lauf.py anliegenregeln.freieNummer <erste> <letzte>"


def hauptprogramm(argumente: list[str]) -> int:
    if len(argumente) != aufrufteileErsteUndLetzteNummer or not all(
        teil.isdigit() for teil in argumente
    ):
        print(f"Aufruf: {aufruf}", file=sys.stderr)
        return 1
    erste, letzte = (int(teil) for teil in argumente)
    nummer = freieNummer(projektordner(), range(erste, letzte + 1))
    if nummer is None:
        print(f"Im Bereich {erste} bis {letzte} ist keine Nummer mehr frei.", file=sys.stderr)
        return 1
    print(nummer)
    return 0


if __name__ == "__main__":
    sys.exit(hauptprogramm(sys.argv[1:]))
