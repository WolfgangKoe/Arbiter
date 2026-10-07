"""Scheiter-Test und Stand: Hook-Eingabe, git und der Ordner `handoff` haben je eine Stelle."""

from pathlib import Path

import pytest

from formregeln.einzelstellen import prüfskripteOrdner, verstöße
from gemeinsam.pfade import wurzel


def skriptAnlegen(ordner: Path, name: str, inhalt: str) -> None:
    datei = ordner / prüfskripteOrdner / name
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(inhalt, encoding="utf-8")


def zeilenDerMeldungen(wurzel: Path) -> list[str]:
    return [meldung.split(" ")[0] for meldung in verstöße(wurzel)]


@pytest.mark.parametrize(
    "zeile",
    [
        'wert = eingabe.get("agent_type")',
        'wert = daten.get("agent_type")',
        'wert = eingabe["agent_id"]',
        'wert = json.load(sys.stdin)["tool_name"]',
    ],
)
def testEinFeldDerEingabeLesenNurDieEingabeSelbst(tmp_path, zeile):
    skriptAnlegen(tmp_path, "gemeinsam/hookProtokoll.py", zeile + "\n")
    skriptAnlegen(tmp_path, "rollenregeln/hook.py", zeile + "\n")
    meldungen = verstöße(tmp_path)
    assert len(meldungen) == 1
    assert meldungen[0].startswith("prozess/pruefungen/rollenregeln/hook.py:1 ")
    assert "HookEingabe" in meldungen[0]


def testEinAnderesFeldMitGetIstKeinFeldDerEingabe(tmp_path):
    skriptAnlegen(tmp_path, "rollenregeln/hook.py", 'wert = angaben.get("command")\n')
    assert verstöße(tmp_path) == []


@pytest.mark.parametrize(
    "aufruf",
    [
        'import subprocess\nsubprocess.run(["git", "log"])\n',
        'from subprocess import run\nrun(["git", "status"])\n',
        'import subprocess\nbefehl = ["git", "log"]\nsubprocess.run(befehl)\n',
        'import subprocess\nsubprocess.run("git log", shell=True)\n',
    ],
)
def testGitRufenNurDieGitAufrufeSelbstAuf(tmp_path, aufruf):
    skriptAnlegen(tmp_path, "gemeinsam/gitAufruf.py", aufruf)
    skriptAnlegen(tmp_path, "rollenregeln/grenze.py", aufruf)
    meldungen = verstöße(tmp_path)
    assert len(meldungen) == 1
    assert "rollenregeln/grenze.py:" in meldungen[0]


def testEinAndererBefehlPerSubprocessUndEinTextMitGitSindKeinGitAufruf(tmp_path):
    skriptAnlegen(tmp_path, "formregeln/lauf.py", 'import subprocess\nsubprocess.run(["ruff"])\n')
    skriptAnlegen(tmp_path, "rollenregeln/liste.py", 'erlaubt = ("git status", "ls")\n')
    assert verstöße(tmp_path) == []


@pytest.mark.parametrize(
    "zeile",
    [
        'plan = Path("handoff") / "plan.md"',
        'text = f"handoff/{name}"',
        'text = f"{wurzel}/handoff/plan.md"',
        'text = "../handoff/plan.md"',
    ],
)
def testDenOrdnerHandoffNenntNurDiePfade(tmp_path, zeile):
    skriptAnlegen(tmp_path, "gemeinsam/pfade.py", 'handoffOrdner = "handoff"\n')
    skriptAnlegen(tmp_path, "standregeln/plan.py", zeile + "\n")
    assert zeilenDerMeldungen(tmp_path) == ["prozess/pruefungen/standregeln/plan.py:1"]


def testKommentareDocstringsUndNamenMitHandoffSindKeinePfadangabe(tmp_path):
    skriptAnlegen(
        tmp_path,
        "standregeln/plan.py",
        '"""Liest handoff/plan.md."""\n# siehe "handoff/plan.md"\nname = "handoffOrdner"\n',
    )
    assert verstöße(tmp_path) == []


def testTestsUndConftestSindAusgenommen(tmp_path):
    skriptAnlegen(tmp_path, "standregeln/planTest.py", 'ordner = "handoff"\n')
    skriptAnlegen(tmp_path, "conftest.py", 'ordner = "handoff"\n')
    assert verstöße(tmp_path) == []


@pytest.mark.stand
def testDieSkripteDesReposHaltenDieEinzelstellen():
    assert verstöße(wurzel) == []


@pytest.mark.parametrize(
    "inhalt",
    [
        'def f():\n    os.system("git add -A")\n',
        'subprocess.run("git status", shell=True)\n',
    ],
)
def testErsteAnweisungMitGitAufrufIstKeinDocstring(tmp_path, inhalt):
    skriptAnlegen(tmp_path, "rollenregeln/grenze.py", inhalt)
    assert len(verstöße(tmp_path)) == 1
