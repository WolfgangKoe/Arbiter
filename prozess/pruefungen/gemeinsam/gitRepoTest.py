import os
import subprocess
import sys
from pathlib import Path

from gemeinsam.gitAufruf import gitAusgabe


def testFestgehaltenesLiegtImLog(gitRepo):
    (gitRepo.ordner / "datei.md").write_text("Stand", encoding="utf-8")
    gitRepo.festhalten("Probe")
    assert gitAusgabe(gitRepo.ordner, "log", "--format=%s").splitlines() == ["Probe"]


def testDerTestklonBleibtVonDerGitUmgebungDesHooksUnberührt(gitRepo, tmp_path, monkeypatch):
    fremderIndex = tmp_path / "fremderIndex"
    monkeypatch.setenv("GIT_INDEX_FILE", str(fremderIndex))
    (gitRepo.ordner / "datei.md").write_text("Stand", encoding="utf-8")
    gitRepo.festhalten("Probe")
    assert not fremderIndex.exists()


def testDieTestsLesenKeineGitUmgebungDesHooks():
    pruefungen = Path(__file__).resolve().parents[1]
    ausgabe = subprocess.run(
        [sys.executable, "-c", "import conftest, os; print(os.environ.get('GIT_INDEX_FILE'))"],
        cwd=pruefungen,
        env={**os.environ, "GIT_INDEX_FILE": "/nirgends/index"},
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert ausgabe.strip() == "None"


def testFestgehaltenOhneÄnderungBleibtMöglich(gitRepo):
    gitRepo.festhalten("Erster")
    gitRepo.festhalten("Zweiter")
    assert gitAusgabe(gitRepo.ordner, "log", "--format=%s").splitlines() == ["Zweiter", "Erster"]
