import subprocess
from pathlib import Path

import pytest

from bashPositivliste import entscheide, ohneHeredocText
from pfade import wurzel


def bash(befehl: str, rolle: str | None = "koordinator") -> dict:
    return {"agent_type": rolle, "tool_name": "Bash", "tool_input": {"command": befehl}}


def gesperrt(befehl: str, rolle: str | None = "koordinator", ordner: Path = wurzel) -> bool:
    antwort = entscheide(bash(befehl, rolle), ordner)
    return antwort is not None and antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "kurz.md").write_text("Stand", encoding="utf-8")
    (tmp_path / "lang.md").write_text("x" * 9000, encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "x"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    return tmp_path


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param("git status", id="git status"),
        pytest.param('git commit -m "Ziel: a > b; c"', id="Operatoren in Anführungszeichen"),
        pytest.param("python3 prozess/pruefungen/stand.py", id="Prüfskript"),
        pytest.param("python3 -m pytest prozess/pruefungen -q", id="Prüftests"),
    ],
)
def testErlaubteBefehleLaufen(befehl):
    assert not gesperrt(befehl)


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param('echo "test" > x.txt', id="Schreiben per Umleitung (Probe)"),
        pytest.param("git status && rm -rf domaene", id="Verkettung"),
        pytest.param("git status; touch x", id="Semikolon"),
        pytest.param('git commit -m "$(cat datei)"', id="Befehlsersetzung"),
        pytest.param("git -C ../ArbiterMap status", id="fremdes Repo"),
        pytest.param('python3 -c \'open("x","w")\'', id="beliebiges Python"),
        pytest.param("sed -i s/a/b/ CLAUDE.md", id="nicht gelistet"),
    ],
)
def testAllesAndereWirdGesperrt(befehl):
    assert gesperrt(befehl)


def testAndereRollenPrüftDieseListeNicht():
    assert not gesperrt('echo "x" > y', rolle="regelumsetzer")


def testKoordinatorLiestMitGitShowNurMitStat(repo):
    assert not gesperrt("git show --stat HEAD", ordner=repo)
    assert gesperrt("git show HEAD", ordner=repo)


def testKoordinatorLiestMitGitShowNurKurzeDateien(repo):
    assert not gesperrt("git show HEAD:kurz.md", ordner=repo)
    assert gesperrt("git show HEAD:lang.md", ordner=repo)


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param("git status --short && git log --oneline -5", id="lesen"),
        pytest.param("cd /repo; git diff HEAD --stat", id="nach cd"),
        pytest.param("git -C /repo show 4542bd1 --stat", id="mit -C"),
        pytest.param("rm handoff/x.md", id="Datei löschen"),
        pytest.param('grep -rn "git commit" .', id="Text git commit"),
        pytest.param("cat ArbiterMap/CLAUDE.md VORGEHEN.md", id="nur lesbare Pfade lesen"),
        pytest.param("cp ArbiterMap/README.md technik/alt.md", id="aus ArbiterMap kopieren"),
        pytest.param("cat > prozess/x.py <<'EOF'\ndef git(a):\nEOF", id="Heredoc mit Text git"),
    ],
)
def testRollenDürfenGitLesenUndAnderesTun(befehl):
    assert not gesperrt(befehl, rolle="architekt")


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
def testRollenDürfenGitNichtSchreiben(befehl):
    assert gesperrt(befehl, rolle="planer")


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param("rm VORGEHEN.md", id="Vorgehen löschen"),
        pytest.param("rm -r ArbiterMap", id="ArbiterMap löschen"),
        pytest.param("rm -rf ./Arbiter-old/backend", id="Arbiter-old löschen"),
        pytest.param("mv ArbiterMap/README.md technik/", id="aus ArbiterMap verschieben"),
        pytest.param("rm handoff/kritik-entwickler.md", id="Kritik des Entwicklers löschen"),
        pytest.param("echo x >> VORGEHEN.md", id="anhängen"),
        pytest.param("cp technik/x.md ArbiterMap/x.md", id="nach ArbiterMap kopieren"),
        pytest.param("sed -i s/a/b/ VORGEHEN.md", id="sed -i"),
        pytest.param(f"ls && rm ../{wurzel.name}/VORGEHEN.md", id="verkettet, Umweg"),
        pytest.param(f"rm {wurzel}/VORGEHEN.md", id="absoluter Pfad"),
    ],
)
def testNurLesbaresÄndertKeineRolleAuchNichtPerBash(befehl):
    assert gesperrt(befehl, rolle="regelumsetzer")


def testStakeholderOhneRolleIstFrei():
    assert not gesperrt("git commit -m x", rolle=None)
    assert not gesperrt("rm VORGEHEN.md", rolle=None)


def testHeredocTextWirdEntferntAußerFürEineShell():
    assert "git" not in ohneHeredocText("cat > x <<'EOF'\ngit push\nEOF")
    assert "git push" in ohneHeredocText("bash <<EOF\ngit push\nEOF")


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param("echo x >> handoff/anliegen/12-probe.md", id="anhängen"),
        pytest.param("sed -i s/offen/erledigt/ handoff/anliegen/12-probe.md", id="sed -i"),
        pytest.param("rm handoff/anliegen/12-probe.md", id="löschen"),
        pytest.param("cp x.md handoff/anliegen/99-neu.md", id="kopieren"),
        pytest.param("tee handoff/anliegen/12-probe.md", id="tee"),
        pytest.param(f"mv x.md {wurzel}/handoff/anliegen/99-neu.md", id="absoluter Pfad"),
        pytest.param("cat > handoff/anliegen/99-neu.md <<EOF\n# Titel\nEOF", id="Heredoc"),
    ],
)
def testKeineRolleSchreibtAnliegenPerBash(befehl):
    assert gesperrt(befehl, rolle="regelumsetzer")


def testAnliegenLesenPerBashBleibtErlaubt():
    assert not gesperrt("cat handoff/anliegen/12-probe.md", rolle="regelumsetzer")
    assert not gesperrt("grep -l offen handoff/anliegen/12-probe.md", rolle="regelumsetzer")


def freigabeRepo(tmp_path, freigabe, zyklus=3):
    datei = tmp_path / "handoff" / "plan.md"
    datei.parent.mkdir(parents=True)
    inhalt = f"# Plan · Zyklus {zyklus}\n\n## Freigabe\nFreigabe: {freigabe}\n"
    datei.write_text(inhalt, encoding="utf-8")
    return tmp_path


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param('git commit -m "Freigabe Plan 3"', id="-m"),
        pytest.param('git commit -qm "Freigabe Plan 3"', id="-qm"),
        pytest.param('git commit -m"Freigabe Plan 3"', id="-m ohne Leerzeichen"),
        pytest.param('git commit --message="Freigabe Plan 3"', id="--message="),
        pytest.param('git commit --message "Freigabe Plan 3"', id="--message"),
    ],
)
def testFreigabeCommitBeiOffenIstGesperrt(tmp_path, befehl):
    assert gesperrt(befehl, ordner=freigabeRepo(tmp_path, "offen"))


def testFreigabeCommitBeiJaIstErlaubt(tmp_path):
    assert not gesperrt('git commit -m "Freigabe Plan 3"', ordner=freigabeRepo(tmp_path, "ja"))


def testFreigabeCommitMitFalscherZyklusnummerIstGesperrt(tmp_path):
    assert gesperrt('git commit -m "Freigabe Plan 4"', ordner=freigabeRepo(tmp_path, "ja"))


def testFreigabeCommitOhneDateiIstGesperrt(tmp_path):
    assert gesperrt('git commit -m "Freigabe Review 2"', ordner=tmp_path)


def testFreigabeEtappeUndAndereCommitsBleibenFrei(tmp_path):
    ordner = freigabeRepo(tmp_path, "offen")
    assert not gesperrt('git commit -m "Freigabe Etappe 1"', ordner=ordner)
    assert not gesperrt('git commit -m "Plan 3"', ordner=ordner)
    assert not gesperrt("git commit", ordner=ordner)
    assert not gesperrt("git commit -m", ordner=ordner)
    assert not gesperrt("git status", ordner=ordner)
