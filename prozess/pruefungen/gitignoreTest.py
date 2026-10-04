"""Messdateien von coverage stehen in .gitignore."""

import pytest

from gitAufruf import gitAusgabe
from pfade import wurzel


@pytest.mark.stand
@pytest.mark.parametrize("datei", [".coverage", ".coverage.rechner.1234"])
def testEineMessdateiVonCoverageIstIgnoriert(datei):
    assert gitAusgabe(wurzel, "check-ignore", datei).strip() == datei
