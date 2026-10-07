from gemeinsam.gitAufruf import gitAusgabe


def testFestgehaltenesLiegtImLog(gitRepo):
    (gitRepo.ordner / "datei.md").write_text("Stand", encoding="utf-8")
    gitRepo.festhalten("Probe")
    assert gitAusgabe(gitRepo.ordner, "log", "--format=%s").splitlines() == ["Probe"]


def testFestgehaltenOhneÄnderungBleibtMöglich(gitRepo):
    gitRepo.festhalten("Erster")
    gitRepo.festhalten("Zweiter")
    assert gitAusgabe(gitRepo.ordner, "log", "--format=%s").splitlines() == ["Zweiter", "Erster"]
