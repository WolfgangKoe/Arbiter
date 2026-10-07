from gemeinsam.gitAufruf import freigaben

kennungLänge = 40


def testFreigabeNenntKennungUndBetreff(gitRepo):
    gitRepo.festhalten("Anderes")
    gitRepo.festhalten("Freigabe Plan 2")
    gefunden = freigaben(gitRepo.ordner)
    assert [freigabe.betreff for freigabe in gefunden] == ["Freigabe Plan 2"]
    assert len(gefunden[0].kennung) == kennungLänge
