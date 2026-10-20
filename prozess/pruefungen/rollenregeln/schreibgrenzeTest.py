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
def wurzel(gitRepo):
    (gitRepo.ordner / ".claude" / "agents").mkdir(parents=True)
    (gitRepo.ordner / ".claude" / "agents" / "probe.md").write_text(rollenkopf, encoding="utf-8")
    return gitRepo.ordner.resolve()


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
    antwort = entscheide(schreiben("/etc/irgendwo.md"), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testWriteUndEditInTmpSindFrei(wurzel):
    assert entscheide(schreiben("/tmp/irgendwo.md"), wurzel) is None


def testWriteInTmpMitUmwegWirdGesperrt(wurzel):
    antwort = entscheide(schreiben("/tmp/../etc/irgendwo.md"), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testWriteInsProjektBleibtGesperrt(wurzel):
    antwort = entscheide(schreiben(wurzel / "technik" / "x.py"), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testNichtLesbarerBefehlNenntDenAusweg(wurzel):
    antwort = entscheide(bash("echo 'offen"), wurzel)
    grund = antwort["hookSpecificOutput"]["permissionDecisionReason"]
    assert "ohne verschachtelte Anführung" in grund


def testRolleOhneSchreibpfadeDarfNichts(wurzel):
    antwort = entscheide(schreiben(wurzel / "prozess" / "x.md", rolle="unbekannt"), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testEigenerOrdnerIstFrei(wurzel):
    assert entscheide(schreiben(wurzel / "prozess" / "pruefungen" / "x.py"), wurzel) is None


def testBacklogIstInJederPhaseFrei(wurzel):
    assert entscheide(schreiben(wurzel / "prozess" / "backlog.md"), wurzel) is None


@pytest.mark.parametrize(
    "pfad",
    [
        "prozess/ablauf.md",
        "prozess/praemissen/ich.md",
        ".claude/agents/probe.md",
        ".claude/skills/x/SKILL.md",
        "domaene/CLAUDE.md",
        "CLAUDE.md",
    ],
)
def testRegelnRollenUndPrämissenSindInDerTechnikphaseGesperrt(wurzel, gitRepo, pfad):
    (wurzel / "handoff").mkdir()
    (wurzel / "handoff" / "plan.md").write_text("# Plan · Zyklus 3\n", encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 3")
    antwort = entscheide(schreiben(wurzel / pfad), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "Prozessphase" in antwort["hookSpecificOutput"]["permissionDecisionReason"]


def testRegelnSindInDerProzessphaseErstNachDerFreigabeDerRetroFrei(wurzel, gitRepo):
    (wurzel / "handoff").mkdir()
    (wurzel / "handoff" / "plan.md").write_text("# Plan · Zyklus 3\n", encoding="utf-8")
    (wurzel / "handoff" / "review.md").write_text("# Review · Zyklus 3\n", encoding="utf-8")
    retro = "# Retro · Zyklus 3\n\n## Prozess-Items\n- P1 Eins\n"
    (wurzel / "handoff" / "retro.md").write_text(retro, encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 3")
    gitRepo.festhalten("Freigabe Review 3")
    ablauf = schreiben(wurzel / "prozess" / "ablauf.md")
    antwort = entscheide(ablauf, wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"
    gitRepo.festhalten("Freigabe Retro 3")
    assert entscheide(ablauf, wurzel) is None


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


def bash(befehl, rolle="probe"):
    return {
        "hook_event_name": "PreToolUse",
        "agent_type": rolle,
        "tool_name": "Bash",
        "tool_input": {"command": befehl},
    }


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param("sed -i 's/a/b/' domaene/ziel.md", id="sed -i"),
        pytest.param("sed -n 1p x.md | tee prozess/x.md", id="tee"),
        pytest.param("echo a > prozess/x.md", id="Umleitung"),
        pytest.param("echo a >> prozess/x.md", id="Anhängen"),
        pytest.param("rm handoff/anliegen/1-a.md", id="rm"),
        pytest.param("mv a.md b.md", id="mv"),
        pytest.param("cp a.md b.md", id="cp"),
        pytest.param("touch prozess/neu.md", id="touch"),
        pytest.param("rm -rf technik/", id="rm -rf im Projekt"),
        pytest.param("rm -rf /tmp/probe technik/x", id="rm -rf gemischt"),
        pytest.param("python3 -c 'print(1)' > technik/x.py", id="python3 -c mit Umleitung"),
        pytest.param("python3 - > technik/x.py <<EOF\nprint(1)\nEOF", id="python3 - mit Umleitung"),
        pytest.param("git add prozess/x.md", id="git add"),
        pytest.param("ls && git commit -m x", id="git commit nach &&"),
        pytest.param("git checkout -- prozess/x.md", id="git checkout"),
        pytest.param("git restore x", id="git restore"),
        pytest.param("git reset --hard", id="git reset"),
        pytest.param("git stash", id="git stash"),
        pytest.param("git rm x", id="git rm"),
        pytest.param("git mv x y", id="git mv"),
        pytest.param("echo a > /tmp/../prozess/x.md", id="Umweg über /tmp/.."),
    ],
)
def testBashSchreibenInsProjektWirdGesperrt(wurzel, befehl):
    antwort = entscheide(bash(befehl), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "Write und Edit" in antwort["hookSpecificOutput"]["permissionDecisionReason"]


@pytest.mark.parametrize(
    "befehl",
    [
        pytest.param("python3 -m pytest prozess/pruefungen", id="pytest"),
        pytest.param("python3 prozess/pruefungen/gemeinsam/lauf.py x.y", id="Prüfskript"),
        pytest.param("git log --oneline", id="git log"),
        pytest.param("git status", id="git status"),
        pytest.param("git diff | head", id="git diff"),
        pytest.param("echo a > /tmp/probe.md", id="Umleitung nach /tmp"),
        pytest.param("ls 2>/dev/null", id="nach /dev/null"),
        pytest.param("ls 2>&1 | grep a", id="Fehlerkanal"),
        pytest.param("grep '>' prozess/ablauf.md", id="Größerzeichen in Anführungszeichen"),
        pytest.param("sed -n 1,5p prozess/ablauf.md", id="sed lesend"),
        pytest.param("rm /tmp/probe.md", id="rm in /tmp"),
        pytest.param("rm -rf /tmp/kopie /tmp/probe", id="rm -rf in /tmp"),
        pytest.param("mv -T /tmp/a /tmp/b", id="mv in /tmp mit jeder Option"),
        pytest.param("python3 -c 'print(1)'", id="python3 -c"),
        pytest.param("python3 - <<EOF\nprint(1)\nEOF", id="python3 -"),
        pytest.param("cp prozess/ablauf.md /tmp/ablauf.md", id="cp nach /tmp"),
        pytest.param("git -C /tmp/repo commit -m x", id="git -C /tmp"),
        pytest.param("cd /tmp/repo && git add x", id="cd /tmp"),
    ],
)
def testBashLesenPrüfenUndTmpBleibenFrei(wurzel, befehl):
    assert entscheide(bash(befehl), wurzel) is None


abhakenBefehl = "python3 prozess/pruefungen/gemeinsam/lauf.py standregeln.abhaken {} Schritt"


def testEineRolleHaktMitDemBefehlEigeneZeilenAb(wurzel):
    assert entscheide(bash(abhakenBefehl.format("Probe")), wurzel) is None


@pytest.mark.parametrize("genannt", ["Reviewer", "Stakeholder", "''"])
def testEineRolleHaktKeineFremdeZeileAb(wurzel, genannt):
    antwort = entscheide(bash(abhakenBefehl.format(genannt)), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "eigene Zeilen" in antwort["hookSpecificOutput"]["permissionDecisionReason"]


hindernisBefehl = (
    "python3 prozess/pruefungen/gemeinsam/lauf.py standregeln.hindernis {} Schritt Planer Text"
)


def testEineRolleMeldetEinHindernisNurFürEigeneZeilen(wurzel):
    assert entscheide(bash(hindernisBefehl.format("Probe")), wurzel) is None
    antwort = entscheide(bash(hindernisBefehl.format("Reviewer")), wurzel)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "eigene Zeilen" in antwort["hookSpecificOutput"]["permissionDecisionReason"]


def testBashGiltNichtFürDenKoordinator(wurzel):
    assert entscheide(bash("git commit -m x", rolle=None), wurzel) is None


def testDerHauptchatKoordinatorDarfPerBashAddenUndCommitten(wurzel):
    befehl = "git add prozess/x.md && git commit -m x && git push"
    assert entscheide(bash(befehl, rolle="koordinator"), wurzel) is None
