import subprocess

import pytest

from agenten import darf_schreiben, schreibpfade
from schreibgrenze import entscheide

ROLLE = """---
name: probe
description: Probe.
schreibpfade:
  - prozess/
  - "*/CLAUDE.md"
  - handoff/retro.md
---
Text.
"""


@pytest.fixture
def wurzel(tmp_path):
    (tmp_path / ".claude" / "agents").mkdir(parents=True)
    (tmp_path / ".claude" / "agents" / "probe.md").write_text(ROLLE, encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    return tmp_path.resolve()


def schreiben(pfad, rolle="probe"):
    return {
        "hook_event_name": "PreToolUse",
        "agent_type": rolle,
        "tool_name": "Write",
        "tool_input": {"file_path": str(pfad)},
    }


def test_schreibpfade_kommen_aus_dem_kopf_der_agentendefinition(wurzel):
    assert schreibpfade("probe", wurzel) == ("prozess/", "*/CLAUDE.md", "handoff/retro.md")


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
def test_darf_schreiben(pfad, erlaubt):
    assert darf_schreiben(pfad, ("prozess/", "*/CLAUDE.md", "handoff/retro.md")) is erlaubt


def test_schreiben_in_fremde_perspektive_wird_gesperrt(wurzel):
    antwort = entscheide(schreiben(wurzel / "domaene" / "ziel.md"), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_schreiben_ausserhalb_des_repos_wird_gesperrt(wurzel):
    antwort = entscheide(schreiben("/tmp/irgendwo.md"), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_rolle_ohne_schreibpfade_darf_nichts(wurzel):
    antwort = entscheide(schreiben(wurzel / "prozess" / "x.md", rolle="unbekannt"), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_eigener_ordner_ist_frei(wurzel):
    assert entscheide(schreiben(wurzel / "prozess" / "ablauf.md"), wurzel) is None


def test_stakeholder_ohne_rolle_ist_frei(wurzel):
    assert entscheide(schreiben(wurzel / "domaene" / "ziel.md", rolle=None), wurzel) is None


def test_rolle_erfaehrt_beim_start_ihre_schreibpfade(wurzel):
    antwort = entscheide(
        {"hook_event_name": "SubagentStart", "agent_type": "probe", "agent_id": "a0"}, wurzel
    )
    assert "prozess/, */CLAUDE.md, handoff/retro.md" in (
        antwort["hookSpecificOutput"]["additionalContext"]
    )


def test_bash_aenderung_ausserhalb_wird_beim_ende_gemeldet(wurzel):
    (wurzel / "schon_vorher.txt").write_text("x")
    rahmen = {"agent_type": "probe", "agent_id": "a1"}
    entscheide({"hook_event_name": "SubagentStart", **rahmen}, wurzel)
    (wurzel / "domaene").mkdir()
    (wurzel / "domaene" / "ziel.md").write_text("per Bash geschrieben")
    (wurzel / "prozess").mkdir()
    (wurzel / "prozess" / "ok.md").write_text("erlaubt")

    antwort = entscheide({"hook_event_name": "SubagentStop", **rahmen}, wurzel)

    meldung = antwort["hookSpecificOutput"]["additionalContext"]
    assert "domaene/ziel.md" in meldung
    assert "prozess/ok.md" not in meldung
    assert "schon_vorher.txt" not in meldung


def test_commit_einer_rolle_wird_beim_ende_gemeldet(wurzel):
    def git(*args):
        subprocess.run(["git", *args], cwd=wurzel, check=True, capture_output=True)

    git("config", "user.email", "probe@example.invalid")
    git("config", "user.name", "probe")
    git("commit", "--allow-empty", "-qm", "vorher")
    rahmen = {"agent_type": "probe", "agent_id": "a2"}
    entscheide({"hook_event_name": "SubagentStart", **rahmen}, wurzel)
    git("commit", "--allow-empty", "-qm", "von der Rolle")

    antwort = entscheide({"hook_event_name": "SubagentStop", **rahmen}, wurzel)

    assert "hat probe committet" in antwort["hookSpecificOutput"]["additionalContext"]
