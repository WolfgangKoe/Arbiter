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
