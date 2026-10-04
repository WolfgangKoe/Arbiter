"""Messdateien von coverage und die Dashboard-Ausgaben stehen in .gitignore."""

import pytest

from gemeinsam.gitAufruf import gitAusgabe
from gemeinsam.pfade import wurzel


@pytest.mark.stand
@pytest.mark.parametrize("datei", [".coverage", ".coverage.rechner.1234"])
def testEineMessdateiVonCoverageIstIgnoriert(datei):
    assert gitAusgabe(wurzel, "check-ignore", datei).strip() == datei


@pytest.mark.stand
@pytest.mark.parametrize("datei", ["dashboard.html", "prozess/dashboard/laeufe.jsonl"])
def testEineDashboardDateiIstIgnoriert(datei):
    assert gitAusgabe(wurzel, "check-ignore", "--no-index", datei).strip() == datei
