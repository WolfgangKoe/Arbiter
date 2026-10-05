"""Scheiter-Test und Stand: Hook-Eingabe, git und der Ordner `handoff` haben je eine Stelle."""

from pathlib import Path

import pytest

from formregeln.einzelstellen import prüfskripteOrdner, verstöße
from gemeinsam.pfade import wurzel


def skriptAnlegen(ordner: Path, name: str, inhalt: str) -> None:
    datei = ordner / prüfskripteOrdner / name
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(inhalt, encoding="utf-8")


def testEinFeldDerEingabeLesenNurDieEingabeSelbst(tmp_path):
    skriptAnlegen(tmp_path, "gemeinsam/hookProtokoll.py", 'wert = eingabe.get("agent_type")\n')
    skriptAnlegen(tmp_path, "rollenregeln/hook.py", 'wert = eingabe.get("agent_type")\n')
    skriptAnlegen(tmp_path, "rollenregeln/zweiterHook.py", 'wert = eingabe["agent_id"]\n')
    meldungen = verstöße(tmp_path)
    assert all("HookEingabe" in meldung for meldung in meldungen)
    assert [meldung.split(" ")[0] for meldung in meldungen] == [
        "prozess/pruefungen/rollenregeln/hook.py:1",
        "prozess/pruefungen/rollenregeln/zweiterHook.py:1",
    ]


def testGitRufenNurDieGitAufrufeSelbstAuf(tmp_path):
    aufruf = 'import subprocess\nsubprocess.run(["git", "log"])\n'
    skriptAnlegen(tmp_path, "gemeinsam/gitAufruf.py", aufruf)
    skriptAnlegen(tmp_path, "rollenregeln/grenze.py", aufruf)
    meldungen = verstöße(tmp_path)
    assert len(meldungen) == 1
    assert "rollenregeln/grenze.py:2 " in meldungen[0]


def testEinAndererBefehlPerSubprocessIstKeinGitAufruf(tmp_path):
    skriptAnlegen(tmp_path, "formregeln/lauf.py", 'import subprocess\nsubprocess.run(["ruff"])\n')
    assert verstöße(tmp_path) == []


def testDenOrdnerHandoffNenntNurDiePfade(tmp_path):
    skriptAnlegen(tmp_path, "gemeinsam/pfade.py", 'handoffOrdner = "handoff"\n')
    skriptAnlegen(tmp_path, "standregeln/plan.py", 'plan = Path("handoff") / "plan.md"\n')
    skriptAnlegen(tmp_path, "standregeln/text.py", 'text = f"handoff/{name}"\n')
    assert [meldung.split(" ")[0] for meldung in verstöße(tmp_path)] == [
        "prozess/pruefungen/standregeln/plan.py:1",
        "prozess/pruefungen/standregeln/text.py:1",
    ]


def testTestsUndConftestSindAusgenommen(tmp_path):
    skriptAnlegen(tmp_path, "standregeln/planTest.py", 'ordner = "handoff"\n')
    skriptAnlegen(tmp_path, "conftest.py", 'ordner = "handoff"\n')
    assert verstöße(tmp_path) == []


@pytest.mark.stand
def testDieSkripteDesReposHaltenDieEinzelstellen():
    assert verstöße(wurzel) == []
