import subprocess

import pytest

from lesen.agenten import darfSchreiben, schreibpfade
from rollenregeln.schreibgrenze import entscheide

rollenkopf = """---
name: probe
description: Probe.
schreibpfade:
  - prozess/
  - "*/CLAUDE.md"
  - handoff/retro.md
  - ArbiterMap/neu.md
---
Text.
"""
probeMuster = ("prozess/", "*/CLAUDE.md", "handoff/retro.md", "ArbiterMap/neu.md")


@pytest.fixture
def wurzel(tmp_path):
    (tmp_path / ".claude" / "agents").mkdir(parents=True)
    (tmp_path / ".claude" / "agents" / "probe.md").write_text(rollenkopf, encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    return tmp_path.resolve()


def schreiben(pfad, rolle="probe"):
    return {
        "hook_event_name": "PreToolUse",
        "agent_type": rolle,
        "tool_name": "Write",
        "tool_input": {"file_path": str(pfad)},
    }


def testSchreibpfadeKommenAusDemKopfDerAgentendefinition(wurzel):
    assert schreibpfade("probe", wurzel) == probeMuster


@pytest.mark.parametrize(
    "pfad, erlaubt",
    [
        pytest.param("prozess/ablauf.md", True, id="eigener Ordner"),
        pytest.param("domaene/CLAUDE.md", True, id="Muster"),
        pytest.param("handoff/retro.md", True, id="einzelne Datei"),
        pytest.param("handoff/plan.md", False, id="fremdes Handoff"),
        pytest.param("domaene/ziel.md", False, id="fremde Perspektive"),
    ],
)
def testDarfSchreiben(pfad, erlaubt):
    assert darfSchreiben(pfad, probeMuster) is erlaubt


def testSchreibenInFremdePerspektiveWirdGesperrt(wurzel):
    antwort = entscheide(schreiben(wurzel / "domaene" / "ziel.md"), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testSchreibenAußerhalbDesReposWirdGesperrt(wurzel):
    antwort = entscheide(schreiben("/tmp/irgendwo.md"), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testRolleOhneSchreibpfadeDarfNichts(wurzel):
    antwort = entscheide(schreiben(wurzel / "prozess" / "x.md", rolle="unbekannt"), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testEigenerOrdnerIstFrei(wurzel):
    assert entscheide(schreiben(wurzel / "prozess" / "ablauf.md"), wurzel) is None


def testStakeholderOhneRolleIstFrei(wurzel):
    assert entscheide(schreiben(wurzel / "domaene" / "ziel.md", rolle=None), wurzel) is None


@pytest.mark.parametrize(
    "pfad",
    [
        pytest.param("VORGEHEN.md", id="Vorgehen"),
        pytest.param("handoff/kritik-entwickler.md", id="Kritik des Entwicklers"),
        pytest.param("Arbiter-old/alt.py", id="Arbiter-old"),
        pytest.param("ArbiterMap/neu.md", id="ArbiterMap, trotz Schreibpfad"),
    ],
)
def testNurLesbaresSperrtJedeRolleAuchMitSchreibpfad(wurzel, pfad):
    antwort = entscheide(schreiben(wurzel / pfad), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "nur lesbar" in antwort["hookSpecificOutput"]["permissionDecisionReason"]


def testNurLesbaresSperrtAuchDenKoordinator(wurzel):
    antwort = entscheide(schreiben(wurzel / "VORGEHEN.md", rolle="koordinator"), wurzel)
    assert "nur lesbar" in antwort["hookSpecificOutput"]["permissionDecisionReason"]


def testNurLesbaresGiltNichtFürDenStakeholder(wurzel):
    assert entscheide(schreiben(wurzel / "VORGEHEN.md", rolle=None), wurzel) is None


def testSchreibpfadeEndenBeimNächstenSchlüsselDesKopfs(wurzel):
    kopf = rollenkopf.replace("---\nText.", "danach: x\n---\nText.")
    (wurzel / ".claude" / "agents" / "probe.md").write_text(kopf, encoding="utf-8")
    assert schreibpfade("probe", wurzel) == probeMuster


def testEineRolleOhneKopfHatKeineSchreibpfade(wurzel):
    (wurzel / ".claude" / "agents" / "probe.md").write_text("Text ohne Kopf.\n", encoding="utf-8")
    assert schreibpfade("probe", wurzel) == ()
