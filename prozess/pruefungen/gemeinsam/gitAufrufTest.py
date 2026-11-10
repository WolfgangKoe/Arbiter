from gemeinsam import gitAufruf
from gemeinsam.gitAufruf import betreffeSeit, freigabeCommit, freigaben, indexGesperrt

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


def testDieFreigabenWerdenJeStandNurEinmalGelesen(gitRepo, monkeypatch):
    gitRepo.festhalten("Freigabe Plan 1")
    aufrufe = []
    echterAufruf = gitAufruf.gitAusgabe

    def aufgerufen(wurzel, *argumente):
        aufrufe.append(argumente[0])
        return echterAufruf(wurzel, *argumente)

    monkeypatch.setattr(gitAufruf, "gitAusgabe", aufgerufen)
    for _ in range(5):
        assert freigabeCommit(gitRepo.ordner, "Plan", 1) is not None
    assert aufrufe.count("log") == 1


def testDieBetreffeSeitEinerFreigabeWerdenJeStandNurEinmalGelesen(gitRepo, monkeypatch):
    gitRepo.festhalten("Freigabe Plan 1")
    kennung = freigabeCommit(gitRepo.ordner, "Plan", 1)
    gitRepo.festhalten("Danach")
    aufrufe = []
    echterAufruf = gitAufruf.gitAusgabe

    def aufgerufen(wurzel, *argumente):
        aufrufe.append(argumente[0])
        return echterAufruf(wurzel, *argumente)

    monkeypatch.setattr(gitAufruf, "gitAusgabe", aufgerufen)
    for _ in range(5):
        assert betreffeSeit(gitRepo.ordner, kennung) == ["Danach"]
    assert aufrufe.count("log") == 1
    gitRepo.festhalten("Noch mehr")
    assert betreffeSeit(gitRepo.ordner, kennung) == ["Noch mehr", "Danach"]


def testEineNeueFreigabeNachEinemCommitWirdGefunden(gitRepo):
    assert freigabeCommit(gitRepo.ordner, "Plan", 2) is None
    gitRepo.festhalten("Freigabe Plan 2")
    assert freigabeCommit(gitRepo.ordner, "Plan", 2) is not None
