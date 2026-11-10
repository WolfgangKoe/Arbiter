import subprocess

import pytest

from gemeinsam.commitImArbeitsbaum import commitImArbeitsbaum, committen

hook = "#!/bin/sh\n[ -e verboten.txt ] && { echo 'Hook rot'; exit 1; }\nexit 0\n"


@pytest.fixture
def repo(gitRepo, monkeypatch):
    for name in ("AUTHOR", "COMMITTER"):
        monkeypatch.setenv(f"GIT_{name}_NAME", "t")
        monkeypatch.setenv(f"GIT_{name}_EMAIL", "t@t")
    (gitRepo.ordner / "alt.txt").write_text("alt\n", encoding="utf-8")
    (gitRepo.ordner / "fremd.txt").write_text("fremd\n", encoding="utf-8")
    gitRepo.festhalten("Start")
    gitRepo.git("checkout", "-q", "-B", "dev")
    ziel = gitRepo.ordner / ".git" / "hooks" / "pre-commit"
    ziel.write_text(hook, encoding="utf-8")
    ziel.chmod(0o755)
    return gitRepo


def ausgabe(repo, *argumente):
    return subprocess.run(
        ["git", *argumente], cwd=repo.ordner, capture_output=True, text=True, check=True
    ).stdout


def testCommitÜbernimmtNurDiePfadeUndLässtAlleAnderenÄnderungenStehen(repo):
    (repo.ordner / "neu.txt").write_text("neu\n", encoding="utf-8")
    (repo.ordner / "fremd.txt").write_text("eine Rolle schreibt noch\n", encoding="utf-8")
    ergebnis = commitImArbeitsbaum(repo.ordner, "Neu: eine Datei", ["neu.txt"])
    assert ergebnis.erfolg
    assert ausgabe(repo, "log", "-1", "--format=%s") == "Neu: eine Datei\n"
    assert ausgabe(repo, "show", "--name-only", "--format=", "HEAD") == "neu.txt\n"
    assert ausgabe(repo, "status", "--porcelain") == " M fremd.txt\n"
    assert (repo.ordner / "fremd.txt").read_text(encoding="utf-8") == "eine Rolle schreibt noch\n"


def testEinGelöschterPfadWirdCommittet(repo):
    (repo.ordner / "alt.txt").unlink()
    assert commitImArbeitsbaum(repo.ordner, "Weg", ["alt.txt"]).erfolg
    assert ausgabe(repo, "ls-files") == "fremd.txt\n"
    assert ausgabe(repo, "status", "--porcelain") == ""


def testEineFreigabeOhnePfadIstEinLeererCommit(repo):
    assert commitImArbeitsbaum(repo.ordner, "Freigabe Plan 1", []).erfolg
    assert ausgabe(repo, "log", "-1", "--format=%s") == "Freigabe Plan 1\n"


def testScheitertDerHookBleibtAllesStehenUndDevUnverändert(repo):
    vorher = ausgabe(repo, "rev-parse", "dev")
    (repo.ordner / "neu.txt").write_text("neu\n", encoding="utf-8")
    (repo.ordner / "verboten.txt").write_text("x\n", encoding="utf-8")
    ergebnis = commitImArbeitsbaum(repo.ordner, "Rot", ["neu.txt", "verboten.txt"])
    assert not ergebnis.erfolg
    assert "Hook rot" in ergebnis.meldung
    assert ausgabe(repo, "rev-parse", "dev") == vorher
    assert ausgabe(repo, "status", "--porcelain") == "?? neu.txt\n?? verboten.txt\n"


def testBewegtSichDevWährendDesCommitsScheitertDerBefehl(repo, monkeypatch):
    (repo.ordner / "neu.txt").write_text("neu\n", encoding="utf-8")
    echt = committen

    def mitFremdemCommit(arbeitsbaum, nachricht, pfade):
        ergebnis = echt(arbeitsbaum, nachricht, pfade)
        repo.git("commit", "-q", "--allow-empty", "-m", "anderer")
        return ergebnis

    monkeypatch.setattr("gemeinsam.commitImArbeitsbaum.committen", mitFremdemCommit)
    ergebnis = commitImArbeitsbaum(repo.ordner, "Neu", ["neu.txt"])
    assert not ergebnis.erfolg
    assert "bewegte sich" in ergebnis.meldung
    assert ausgabe(repo, "log", "-1", "--format=%s") == "anderer\n"


def testCommitNimmtDiePfadeAusDemArbeitsbaumDerRolleUndNichtAusDemProjektordner(repo, tmp_path):
    rolle = tmp_path / "rolle"
    repo.git("worktree", "add", "-q", "-b", "rolle", str(rolle), "dev")
    (rolle / "neu.txt").write_text("aus der Rolle\n", encoding="utf-8")
    (repo.ordner / "neu.txt").write_text("aus dem Projektordner\n", encoding="utf-8")
    ergebnis = commitImArbeitsbaum(repo.ordner, "Aus der Rolle", ["neu.txt"], rolle)
    assert ergebnis.erfolg
    assert ausgabe(repo, "show", "dev:neu.txt") == "aus der Rolle\n"


def testDerArbeitsbaumIstDanachEntfernt(repo):
    (repo.ordner / "neu.txt").write_text("neu\n", encoding="utf-8")
    commitImArbeitsbaum(repo.ordner, "Neu", ["neu.txt"])
    assert len(ausgabe(repo, "worktree", "list").splitlines()) == 1
