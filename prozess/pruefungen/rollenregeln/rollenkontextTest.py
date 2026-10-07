import pytest

from rollenregeln.rollenkontext import kontext


def rolle(wurzel, name, *pfade):
    ordner = wurzel / ".claude" / "agents"
    ordner.mkdir(parents=True, exist_ok=True)
    kopf = "".join(f"  - {pfad}\n" for pfad in pfade)
    (ordner / f"{name}.md").write_text(f"---\nname: {name}\nschreibpfade:\n{kopf}---\nText.\n")


@pytest.fixture
def wurzel(gitRepo):
    (gitRepo.ordner / "domaene").mkdir()
    (gitRepo.ordner / "domaene" / "CLAUDE.md").write_text("DOMAENENREGELN\n")
    (gitRepo.ordner / "prozess").mkdir()
    (gitRepo.ordner / "prozess" / "CLAUDE.md").write_text("PROZESSREGELN\n")
    return gitRepo.ordner


def testPlanerBekommtStandUndDomänenClaudeMd(wurzel):
    rolle(wurzel, "planer", "domaene/etappen/", "handoff/plan.md")
    ergebnis = kontext("planer", wurzel)
    assert "Stand: " in ergebnis
    assert "DOMAENENREGELN" in ergebnis
    assert "PROZESSREGELN" not in ergebnis


def testRolleOhnePassendenSchreibpfadBekommtKeineOrdnerClaudeMd(wurzel):
    rolle(wurzel, "kritiker", "handoff/anliegen/")
    ergebnis = kontext("kritiker", wurzel)
    assert "Stand: " in ergebnis
    assert "REGELN" not in ergebnis


def testRolleOhneSchreibpfadeBekommtKeineOrdnerClaudeMd(wurzel):
    rolle(wurzel, "leser")
    assert "REGELN" not in kontext("leser", wurzel)
