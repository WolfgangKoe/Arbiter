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


def testRolleBekommtIhreOffenenSchritteUndDenBefehlZumAbhaken(wurzel, gitRepo):
    rolle(wurzel, "reviewer", "handoff/review.md")
    (wurzel / "handoff").mkdir()
    (wurzel / "domaene" / "items").mkdir()
    (wurzel / "domaene" / "items" / "eins.md").write_text("# Eins\n")
    (wurzel / "handoff" / "plan.md").write_text(
        "# Plan · Zyklus 1\n\n## Items\n1. [E](../domaene/items/eins.md)\n\n## Freigabe\nx\n"
    )
    gitRepo.festhalten("Freigabe Plan 1")
    ergebnis = kontext("reviewer", wurzel)
    assert "- Kritik am Code zu Item eins" in ergebnis
    assert "standregeln.abhaken reviewer <Schritt>" in ergebnis
    assert "Item eins abgenommen" not in ergebnis
