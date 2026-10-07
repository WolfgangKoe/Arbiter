import pytest

from rollenregeln.schreibBilanz import entscheide
from rollenregeln.schreibgrenzeTest import rollenkopf


@pytest.fixture
def wurzel(gitRepo):
    (gitRepo.ordner / ".claude" / "agents").mkdir(parents=True)
    (gitRepo.ordner / ".claude" / "agents" / "probe.md").write_text(rollenkopf, encoding="utf-8")
    return gitRepo.ordner.resolve()


def testRolleErfährtBeimStartIhreSchreibpfade(wurzel):
    antwort = entscheide(
        {"hook_event_name": "SubagentStart", "agent_type": "probe", "agent_id": "a0"}, wurzel
    )
    kontext = antwort["hookSpecificOutput"]["additionalContext"]
    assert "prozess/, */CLAUDE.md, handoff/retro.md" in kontext
    assert "VORGEHEN.md" in kontext


def testBashÄnderungAußerhalbWirdBeimEndeGemeldet(wurzel):
    (wurzel / "schonVorher.txt").write_text("x")
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
    assert "schonVorher.txt" not in meldung


def testBashÄnderungInNurLesbaremWirdTrotzSchreibpfadGemeldet(wurzel):
    rahmen = {"agent_type": "probe", "agent_id": "a3"}
    entscheide({"hook_event_name": "SubagentStart", **rahmen}, wurzel)
    (wurzel / "ArbiterMap").mkdir()
    (wurzel / "ArbiterMap" / "neu.md").write_text("per Bash geschrieben")

    antwort = entscheide({"hook_event_name": "SubagentStop", **rahmen}, wurzel)

    assert "ArbiterMap/neu.md" in antwort["hookSpecificOutput"]["additionalContext"]


def testCommitEinerRolleWirdBeimEndeGemeldet(wurzel, gitRepo):
    gitRepo.festhalten("vorher")
    rahmen = {"agent_type": "probe", "agent_id": "a2"}
    entscheide({"hook_event_name": "SubagentStart", **rahmen}, wurzel)
    gitRepo.festhalten("von der Rolle")

    antwort = entscheide({"hook_event_name": "SubagentStop", **rahmen}, wurzel)

    assert "hat probe committet" in antwort["hookSpecificOutput"]["additionalContext"]


@pytest.mark.parametrize("ereignis", ["SubagentStart", "SubagentStop"])
def testOhneRolleMeldetDerHookNichts(wurzel, ereignis):
    assert entscheide({"hook_event_name": ereignis, "agent_id": "a9"}, wurzel) is None
