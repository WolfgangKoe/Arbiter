import pytest

from rollenregeln.schreibgrenze import entscheide

rollenkopf = """---
name: probe
description: Probe.
schreibpfade:
  - prozess/
  - handoff/anliegen/
  - ArbiterMap/
---
Text.
"""


@pytest.fixture
def wurzel(gitRepo):
    ordner = gitRepo.ordner
    (ordner / ".claude" / "agents").mkdir(parents=True)
    (ordner / ".claude" / "agents" / "probe.md").write_text(rollenkopf, encoding="utf-8")
    for pfad in (
        "prozess/alt.md",
        "prozess/unter/tief.md",
        "domaene/ziel.md",
        "ArbiterMap/karte.md",
        "handoff/anliegen/1-committet.md",
    ):
        (ordner / pfad).parent.mkdir(parents=True, exist_ok=True)
        (ordner / pfad).write_text("x", encoding="utf-8")
    gitRepo.festhalten()
    (ordner / "handoff" / "anliegen" / "2-neu.md").write_text("x", encoding="utf-8")
    return ordner.resolve()


def bash(befehl, rolle="probe"):
    return {
        "hook_event_name": "PreToolUse",
        "agent_type": rolle,
        "tool_name": "Bash",
        "tool_input": {"command": befehl},
    }


def gesperrt(wurzel, befehl):
    antwort = entscheide(bash(befehl), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"
    return antwort["hookSpecificOutput"]["permissionDecisionReason"]


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param("rm prozess/alt.md", id="rm im Schreibpfad"),
        pytest.param("rm -f prozess/alt.md", id="rm -f"),
        pytest.param("mv prozess/alt.md prozess/neu.md", id="mv im Schreibpfad"),
        pytest.param("mv prozess/alt.md prozess/unter/", id="mv in Unterordner"),
        pytest.param("rm handoff/anliegen/2-neu.md", id="rm eines nicht committeten Anliegens"),
        pytest.param(
            "mv handoff/anliegen/2-neu.md handoff/anliegen/3-neu.md", id="mv eines neuen Anliegens"
        ),
        pytest.param("rm prozess/alt.md prozess/unter/tief.md", id="rm mehrerer Pfade"),
        pytest.param("rm -- prozess/alt.md", id="rm nach --"),
    ],
)
def testRmUndMvInDenSchreibpfadenSindFrei(wurzel, befehl):
    assert entscheide(bash(befehl), wurzel) is None


@pytest.mark.parametrize(
    "befehl, grund",
    [
        pytest.param(
            "rm domaene/ziel.md", "darf domaene/ziel.md nicht schreiben", id="fremder Pfad"
        ),
        pytest.param("mv prozess/alt.md domaene/alt.md", "domaene/alt.md nicht", id="Ziel fremd"),
        pytest.param(
            "mv domaene/ziel.md prozess/ziel.md", "domaene/ziel.md nicht", id="Quelle fremd"
        ),
        pytest.param("rm ArbiterMap/karte.md", "nur lesbar", id="nur lesbar trotz Schreibpfad"),
        pytest.param(
            "rm handoff/anliegen/1-committet.md", "schon committet", id="Anliegen committet"
        ),
        pytest.param(
            "mv handoff/anliegen/1-committet.md prozess/x.md", "schon committet", id="mv committet"
        ),
        pytest.param(
            "mv handoff/anliegen/2-neu.md handoff/anliegen/1-committet.md",
            "schon committet",
            id="mv überschreibt Committetes",
        ),
        pytest.param("rm -r prozess/unter", "erlaubt sind nur", id="rekursiv"),
        pytest.param("rm prozess/unter", "ist ein Ordner", id="Ordner"),
        pytest.param("rm prozess/*.md", "Platzhalter", id="Platzhalter"),
        pytest.param("rm $HOME/x", "Platzhalter", id="Variable"),
        pytest.param("rm ../außen.md", "außerhalb", id="außerhalb des Projekts"),
        pytest.param("rm prozess/../domaene/ziel.md", "nicht schreiben", id="Umweg über .."),
        pytest.param(
            "rm /tmp/x prozess/../domaene/ziel.md", "nicht schreiben", id="tmp als Tarnung"
        ),
        pytest.param("cd prozess && rm alt.md", "nach cd", id="nach cd ins Projekt"),
        pytest.param("rm prozess/alt.md > prozess/x.md", "Umleitung", id="Umleitung"),
        pytest.param("rm", "ohne Pfade", id="ohne Pfade"),
        pytest.param("mv prozess/alt.md", "ohne Pfade", id="mv mit einem Pfad"),
        pytest.param("git rm prozess/alt.md", "git rm", id="git rm bleibt gesperrt"),
        pytest.param("git mv prozess/alt.md prozess/neu.md", "git mv", id="git mv bleibt gesperrt"),
        pytest.param("sudo rm domaene/ziel.md", "nicht schreiben", id="hinter sudo"),
    ],
)
def testRmUndMvAußerhalbDerSchreibpfadeBleibenGesperrt(wurzel, befehl, grund):
    assert grund in gesperrt(wurzel, befehl)


def testEineRolleOhneSchreibpfadeLöschtNichts(wurzel):
    antwort = entscheide(bash("rm prozess/alt.md", rolle="unbekannt"), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testRmInTmpBleibtFrei(wurzel):
    assert entscheide(bash("rm /tmp/probe.md"), wurzel) is None
