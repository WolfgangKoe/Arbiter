import subprocess

import pytest

from rollenkontext import kontext


def rolle(wurzel, name, *pfade):
    ordner = wurzel / ".claude" / "agents"
    ordner.mkdir(parents=True, exist_ok=True)
    kopf = "".join(f"  - {p}\n" for p in pfade)
    (ordner / f"{name}.md").write_text(f"---\nname: {name}\nschreibpfade:\n{kopf}---\nText.\n")


@pytest.fixture
def wurzel(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "domaene").mkdir()
    (tmp_path / "domaene" / "CLAUDE.md").write_text("DOMAENENREGELN\n")
    (tmp_path / "prozess").mkdir()
    (tmp_path / "prozess" / "CLAUDE.md").write_text("PROZESSREGELN\n")
    return tmp_path


def test_planer_bekommt_stand_und_domaenen_claude_md(wurzel):
    rolle(wurzel, "planer", "domaene/etappen/", "handoff/plan.md")
    ergebnis = kontext("planer", wurzel)
    assert "Stand: " in ergebnis
    assert "DOMAENENREGELN" in ergebnis
    assert "PROZESSREGELN" not in ergebnis


def test_rolle_ohne_passenden_schreibpfad_bekommt_keine_ordner_claude_md(wurzel):
    rolle(wurzel, "kritiker", "handoff/anliegen/")
    ergebnis = kontext("kritiker", wurzel)
    assert "Stand: " in ergebnis
    assert "REGELN" not in ergebnis


def test_rolle_ohne_schreibpfade_bekommt_keine_ordner_claude_md(wurzel):
    rolle(wurzel, "leser")
    assert "REGELN" not in kontext("leser", wurzel)
