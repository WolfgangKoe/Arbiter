import json
import os
import time

import pytest

from rollenregeln.schreibBilanz import entscheide, meldungsOrdner, standDatei
from rollenregeln.schreibgrenzeTest import rollenkopf


@pytest.fixture
def wurzel(gitRepo):
    (gitRepo.ordner / ".claude" / "agents").mkdir(parents=True)
    (gitRepo.ordner / ".claude" / "agents" / "probe.md").write_text(rollenkopf, encoding="utf-8")
    return gitRepo.ordner.resolve()


def meldungVon(wurzel, agentId):
    return (meldungsOrdner(wurzel) / f"{agentId}.txt").read_text(encoding="utf-8")


def transkriptMit(ordner, *aufrufe):
    datei = ordner / "rolle.jsonl"
    zeilen = [
        json.dumps({"message": {"content": [{"type": "tool_use", "name": name, "input": eingabe}]}})
        for name, eingabe in aufrufe
    ]
    datei.write_text("\n".join(zeilen), encoding="utf-8")
    return datei


def testPfadenDieDieRolleNichtAnfasstSteheUnterUnklarStattUnterVerletzt(wurzel, tmp_path):
    rahmen = {"agent_type": "probe", "agent_id": "a5"}
    entscheide({"hook_event_name": "SubagentStart", **rahmen}, wurzel)
    (wurzel / "domaene").mkdir()
    (wurzel / "domaene" / "ziel.md").write_text("von der Rolle")
    (wurzel / "handoff").mkdir()
    (wurzel / "handoff" / "plan.md").write_text("von einem anderen")
    transkript = transkriptMit(
        tmp_path, ("Bash", {"command": "echo x > domaene/ziel.md"}), ("Read", {})
    )

    entscheide(
        {"hook_event_name": "SubagentStop", "agent_transcript_path": str(transkript), **rahmen},
        wurzel,
    )

    verletzt, _, unklar = meldungVon(wurzel, "a5").partition("unklar, wer")
    assert "domaene/ziel.md" in verletzt
    assert "handoff/plan.md" not in verletzt
    assert "handoff/plan.md" in unklar


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

    meldung = meldungVon(wurzel, "a1")
    assert antwort is None
    assert "domaene/ziel.md" in meldung
    assert "prozess/ok.md" not in meldung
    assert "schonVorher.txt" not in meldung


def testBashÄnderungInNurLesbaremWirdTrotzSchreibpfadGemeldet(wurzel):
    rahmen = {"agent_type": "probe", "agent_id": "a3"}
    entscheide({"hook_event_name": "SubagentStart", **rahmen}, wurzel)
    (wurzel / "ArbiterMap").mkdir()
    (wurzel / "ArbiterMap" / "neu.md").write_text("per Bash geschrieben")

    entscheide({"hook_event_name": "SubagentStop", **rahmen}, wurzel)

    assert "ArbiterMap/neu.md" in meldungVon(wurzel, "a3")


def testCommitEinerRolleWirdBeimEndeGemeldet(wurzel, gitRepo):
    gitRepo.festhalten("vorher")
    rahmen = {"agent_type": "probe", "agent_id": "a2"}
    entscheide({"hook_event_name": "SubagentStart", **rahmen}, wurzel)
    gitRepo.festhalten("von der Rolle")

    entscheide({"hook_event_name": "SubagentStop", **rahmen}, wurzel)

    assert "hat probe committet" in meldungVon(wurzel, "a2")


@pytest.mark.parametrize("ereignis", ["SubagentStart", "SubagentStop"])
def testOhneRolleMeldetDerHookNichts(wurzel, ereignis):
    assert entscheide({"hook_event_name": ereignis, "agent_id": "a9"}, wurzel) is None


def testGelesenerOrdnerMachtFremdeÄnderungDarinNichtZurVerletzung(wurzel, tmp_path):
    rahmen = {"agent_type": "probe", "agent_id": "a6"}
    entscheide({"hook_event_name": "SubagentStart", **rahmen}, wurzel)
    (wurzel / "domaene").mkdir()
    (wurzel / "domaene" / "b.md").write_text("von einem anderen")
    transkript = transkriptMit(tmp_path, ("Bash", {"command": "cat domaene/a.md"}))

    entscheide(
        {"hook_event_name": "SubagentStop", "agent_transcript_path": str(transkript), **rahmen},
        wurzel,
    )

    verletzt, _, unklar = meldungVon(wurzel, "a6").partition("unklar, wer")
    assert "domaene/b.md" not in verletzt
    assert "domaene/b.md" in unklar


def testZweiterStoppMeldetNeueDateiAußerhalb(wurzel):
    rahmen = {"agent_type": "probe", "agent_id": "a7"}
    entscheide({"hook_event_name": "SubagentStart", **rahmen}, wurzel)
    entscheide({"hook_event_name": "SubagentStop", **rahmen}, wurzel)
    (wurzel / "domaene").mkdir()
    (wurzel / "domaene" / "neu.md").write_text("nach dem ersten Stopp")

    entscheide({"hook_event_name": "SubagentStop", **rahmen}, wurzel)

    assert "domaene/neu.md" in meldungVon(wurzel, "a7")


def testZweiterStoppMeldetDateiVorDemStartNicht(wurzel):
    (wurzel / "schonVorher.txt").write_text("x")
    rahmen = {"agent_type": "probe", "agent_id": "a8"}
    entscheide({"hook_event_name": "SubagentStart", **rahmen}, wurzel)
    entscheide({"hook_event_name": "SubagentStop", **rahmen}, wurzel)
    entscheide({"hook_event_name": "SubagentStop", **rahmen}, wurzel)

    assert not (meldungsOrdner(wurzel) / "a8.txt").exists()


def testBashHeredocSchreibenAnDieDateiIstVerletzt(wurzel, tmp_path):
    rahmen = {"agent_type": "probe", "agent_id": "a10"}
    entscheide({"hook_event_name": "SubagentStart", **rahmen}, wurzel)
    (wurzel / "domaene").mkdir()
    (wurzel / "domaene" / "a.md").write_text("geschrieben")
    befehl = "cat > domaene/a.md <<'EOF'\ngeht's nicht\nEOF"
    transkript = transkriptMit(tmp_path, ("Bash", {"command": befehl}))

    entscheide(
        {"hook_event_name": "SubagentStop", "agent_transcript_path": str(transkript), **rahmen},
        wurzel,
    )

    verletzt, _, _ = meldungVon(wurzel, "a10").partition("unklar, wer")
    assert "domaene/a.md" in verletzt


def testStartRäumtStandDateienÄlterAlsEinTag(wurzel):
    alt = standDatei(wurzel, "uralt")
    alt.parent.mkdir(parents=True)
    alt.write_text("HEAD x")
    vorgestern = time.time() - 2 * 24 * 60 * 60
    os.utime(alt, (vorgestern, vorgestern))

    entscheide(
        {"hook_event_name": "SubagentStart", "agent_type": "probe", "agent_id": "a11"}, wurzel
    )

    assert not alt.exists()
    assert standDatei(wurzel, "a11").exists()
