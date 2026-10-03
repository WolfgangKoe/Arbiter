import subprocess

import lesegrenze


def lesen(pfad, rolle="koordinator"):
    return {"agent_type": rolle, "tool_name": "Read", "tool_input": {"file_path": str(pfad)}}


def repoMitDatei(tmp_path, name, text):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / name).write_text(text, encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "x"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )


def testKoordinatorLiestKeineLangenDateien(tmp_path):
    (tmp_path / "VORGEHEN.md").write_text("ä" * 25000, encoding="utf-8")
    antwort = lesegrenze.entscheide(lesen(tmp_path / "VORGEHEN.md"), tmp_path)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testKoordinatorLiestKurzeDateien(tmp_path):
    (tmp_path / "kurz.md").write_text("Stand", encoding="utf-8")
    assert lesegrenze.entscheide(lesen(tmp_path / "kurz.md"), tmp_path) is None


def testRollenLesenAuchLangeDateien(tmp_path):
    (tmp_path / "lang.md").write_text("x" * 25000, encoding="utf-8")
    assert lesegrenze.entscheide(lesen(tmp_path / "lang.md", rolle="planer"), tmp_path) is None


def testGitShowMitStatIstErlaubt(tmp_path):
    repoMitDatei(tmp_path, "lang.md", "x" * 9000)
    assert lesegrenze.gitShowZulässig(["git", "show", "--stat", "HEAD"], tmp_path)


def testGitShowOhneStatZeigtDenGanzenDiffUndIstGesperrt(tmp_path):
    repoMitDatei(tmp_path, "lang.md", "x" * 9000)
    assert not lesegrenze.gitShowZulässig(["git", "show", "HEAD"], tmp_path)


def testGitShowEinerKurzenDateiIstErlaubt(tmp_path):
    repoMitDatei(tmp_path, "kurz.md", "Stand")
    assert lesegrenze.gitShowZulässig(["git", "show", "HEAD:kurz.md"], tmp_path)


def testGitShowEinerLangenDateiIstGesperrt(tmp_path):
    repoMitDatei(tmp_path, "lang.md", "x" * 9000)
    assert not lesegrenze.gitShowZulässig(["git", "show", "HEAD:lang.md"], tmp_path)


def testGitShowOhneAngabeIstGesperrt(tmp_path):
    repoMitDatei(tmp_path, "kurz.md", "Stand")
    assert not lesegrenze.gitShowZulässig(["git", "show"], tmp_path)
