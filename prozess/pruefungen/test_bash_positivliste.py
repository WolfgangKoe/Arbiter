import pytest

from bash_positivliste import entscheide


def bash(befehl: str, rolle: str | None = "koordinator") -> dict:
    return {"agent_type": rolle, "tool_name": "Bash", "tool_input": {"command": befehl}}


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param("git status", id="git status"),
        pytest.param('git commit -m "Ziel: a > b; c"', id="Operatoren in Anführungszeichen"),
        pytest.param("python3 prozess/pruefungen/stand.py", id="Prüfskript"),
        pytest.param("python3 -m pytest prozess/pruefungen -q", id="Prüftests"),
    ],
)
def test_erlaubte_befehle_laufen(befehl):
    assert entscheide(bash(befehl)) is None


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param('echo "test" > x.txt', id="Schreiben per Umleitung (Probe)"),
        pytest.param("git status && rm -rf domaene", id="Verkettung"),
        pytest.param("git status; touch x", id="Semikolon"),
        pytest.param('git commit -m "$(cat datei)"', id="Befehlsersetzung"),
        pytest.param("git -C ../ArbiterMap status", id="fremdes Repo"),
        pytest.param("python3 -c 'open(\"x\",\"w\")'", id="beliebiges Python"),
        pytest.param("sed -i s/a/b/ CLAUDE.md", id="nicht gelistet"),
    ],
)
def test_alles_andere_wird_gesperrt(befehl):
    antwort = entscheide(bash(befehl))
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_andere_rollen_prueft_diese_liste_nicht():
    assert entscheide(bash('echo "x" > y', rolle="regelumsetzer")) is None


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param("git status --short && git log --oneline -5", id="lesen"),
        pytest.param("cd /repo; git diff HEAD --stat", id="nach cd"),
        pytest.param("git -C /repo show 4542bd1 --stat", id="mit -C"),
        pytest.param("rm handoff/anliegen/08-x.md", id="Datei löschen"),
        pytest.param('grep -rn "git commit" .', id="Text git commit"),
    ],
)
def test_rollen_duerfen_git_lesen(befehl):
    assert entscheide(bash(befehl, rolle="architekt")) is None


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param(
            "git rm -q handoff/anliegen/08-x.md && git commit -qm x", id="Architekt Zyklus 1"
        ),
        pytest.param("git add -A", id="add"),
        pytest.param("cd /repo && git -C . commit -m x", id="commit mit -C"),
        pytest.param("ls; git reset --hard", id="reset"),
        pytest.param("/usr/bin/git push", id="voller Pfad"),
    ],
)
def test_rollen_duerfen_git_nicht_schreiben(befehl):
    antwort = entscheide(bash(befehl, rolle="planer"))
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_stakeholder_ohne_rolle_ist_frei():
    assert entscheide(bash("git commit -m x", rolle=None)) is None
