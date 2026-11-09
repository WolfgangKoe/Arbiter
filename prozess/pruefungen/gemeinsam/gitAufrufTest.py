from gemeinsam.gitAufruf import freigaben, indexGesperrt

kennungLänge = 40


def testDerIndexIstNurMitSperrdateiGesperrt(gitRepo):
    assert not indexGesperrt(gitRepo.ordner)
    (gitRepo.ordner / ".git" / "index.lock").write_text("", encoding="utf-8")
    assert indexGesperrt(gitRepo.ordner)


def testFreigabeNenntKennungUndBetreff(gitRepo):
    gitRepo.festhalten("Anderes")
    gitRepo.festhalten("Freigabe Plan 2")
    gefunden = freigaben(gitRepo.ordner)
    assert [freigabe.betreff for freigabe in gefunden] == ["Freigabe Plan 2"]
    assert len(gefunden[0].kennung) == kennungLänge
