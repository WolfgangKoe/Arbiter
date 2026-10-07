from rollenregeln import lesegrenze


def lesen(pfad, rolle="koordinator"):
    return {"agent_type": rolle, "tool_name": "Read", "tool_input": {"file_path": str(pfad)}}


def repoMitDatei(gitRepo, name, text):
    (gitRepo.ordner / name).write_text(text, encoding="utf-8")
    gitRepo.festhalten()


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


def testGitShowMitStatIstErlaubt(tmp_path, gitRepo):
    repoMitDatei(gitRepo, "lang.md", "x" * 9000)
    assert lesegrenze.gitShowZulässig(["git", "show", "--stat", "HEAD"], tmp_path)


def testGitShowOhneStatZeigtDenGanzenDiffUndIstGesperrt(tmp_path, gitRepo):
    repoMitDatei(gitRepo, "lang.md", "x" * 9000)
    assert not lesegrenze.gitShowZulässig(["git", "show", "HEAD"], tmp_path)


def testGitShowEinerKurzenDateiIstErlaubt(tmp_path, gitRepo):
    repoMitDatei(gitRepo, "kurz.md", "Stand")
    assert lesegrenze.gitShowZulässig(["git", "show", "HEAD:kurz.md"], tmp_path)


def testGitShowEinerLangenDateiIstGesperrt(tmp_path, gitRepo):
    repoMitDatei(gitRepo, "lang.md", "x" * 9000)
    assert not lesegrenze.gitShowZulässig(["git", "show", "HEAD:lang.md"], tmp_path)


def testGitShowOhneAngabeIstGesperrt(tmp_path, gitRepo):
    repoMitDatei(gitRepo, "kurz.md", "Stand")
    assert not lesegrenze.gitShowZulässig(["git", "show"], tmp_path)


def testEineFehlendeDateiWirdNichtGesperrt(tmp_path):
    assert lesegrenze.entscheide(lesen(tmp_path / "gibtsNicht.md"), tmp_path) is None


def testEineDateiOhneTextWirdNichtGesperrt(tmp_path):
    (tmp_path / "bild.bin").write_bytes(b"\xff\xfe\x00" * 5000)
    assert lesegrenze.entscheide(lesen(tmp_path / "bild.bin"), tmp_path) is None
