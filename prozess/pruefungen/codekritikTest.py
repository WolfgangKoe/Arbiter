from pathlib import Path

import codekritik
from codekritik import Commit, FälligeKritik, ersteFälligeKritik, fälligeKritikAlsText


def testFälligeKritikTrägtBenannteFelder(monkeypatch):
    monkeypatch.setattr(
        codekritik, "commitsSeitDerFreigabe", lambda _wurzel: [Commit("abc1234f", "x")]
    )
    monkeypatch.setattr(codekritik, "gitAusgabe", lambda *_argumente: "pyproject.toml")
    fällig = ersteFälligeKritik(Path("."))
    assert fällig == FälligeKritik("abc1234", "Architekt und Reviewer")
    assert (fällig.kurzerHash, fällig.kritiker) == ("abc1234", "Architekt und Reviewer")
    assert (
        fälligeKritikAlsText(Path(".")) == "Kritik am Code fällig: Architekt und Reviewer (abc1234)"
    )
