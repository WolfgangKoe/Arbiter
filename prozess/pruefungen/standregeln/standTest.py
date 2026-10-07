import json
from pathlib import Path

import pytest

from standregeln.stand import stand


class Repo:
    def __init__(self, gitRepo):
        self.wurzel = gitRepo.ordner
        self.git = gitRepo.git
        self.festhalten = gitRepo.festhalten

    def datei(self, pfad, text):
        ziel = self.wurzel / pfad
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(text, encoding="utf-8")
        self.festhalten(f"{pfad} geschrieben")


@pytest.fixture
def repo(gitRepo):
    return Repo(gitRepo)


def anliegen(repo, nummer, status, absender="Architekt", empfänger="Planer"):
    kopf = f"{nummer} · Kritik · von {absender} (Technik) → {empfänger} · Runde 1/3 · {status}"
    repo.datei(f"handoff/anliegen/{nummer}-probe.md", f"# Probe\n\n{kopf}\n")


def testStandNenntKeineRollenläufeAuchMitAltemProtokoll(repo):
    datei = repo.wurzel / ".git" / "arbiter" / "rollenlaeufe.jsonl"
    datei.parent.mkdir(parents=True)
    eintrag = json.dumps({"phase": "Zyklus 1 · Domänenphase", "rolle": "planer"})
    datei.write_text((eintrag + "\n") * 3, encoding="utf-8")
    assert "Rollenläufe" not in stand(repo.wurzel)


def testStandNenntDieBelegungDesTranskripts(repo, tmp_path_factory):
    transkript = tmp_path_factory.mktemp("transkript") / "sitzung.jsonl"
    nutzung = {"input_tokens": 10, "cache_read_input_tokens": 59_990}
    transkript.write_text(json.dumps({"message": {"usage": nutzung}}) + "\n", encoding="utf-8")
    assert "Belegung 60.000/120.000 Token" in stand(repo.wurzel, transkript)


def testStandEmpfiehltAbDerWarnschwelleEinenNeuenChat(repo, tmp_path_factory):
    transkript = tmp_path_factory.mktemp("transkript") / "sitzung.jsonl"
    nutzung = {"cache_read_input_tokens": 125_000}
    transkript.write_text(json.dumps({"message": {"usage": nutzung}}) + "\n", encoding="utf-8")
    assert "neuer Chat empfohlen" in stand(repo.wurzel, transkript)


def testStandNenntFälligeNachprüfungenMitRolle(repo):
    anliegen(repo, "12", "angenommen", absender="Architekt")
    anliegen(repo, "13", "offen", absender="Architekt")
    anliegen(repo, "14", "angenommen", absender="Fachkritiker")
    assert "Nachprüfung fällig: Architekt (12), Fachkritiker (14)" in stand(repo.wurzel)


def testStandOhneAngenommeneAnliegenNenntKeineNachprüfung(repo):
    anliegen(repo, "13", "offen")
    assert "Nachprüfung" not in stand(repo.wurzel)


def testStandNenntJeOffenemAnliegenWerDranIst(repo):
    anliegen(repo, "12", "offen", absender="Architekt", empfänger="Planer")
    anliegen(repo, "13", "abgelehnt", absender="Architekt", empfänger="Planer")
    anliegen(repo, "14", "eskaliert", absender="Architekt", empfänger="Planer")
    assert "Dran: Architekt (13), Planer (12), Stakeholder (14)" in stand(repo.wurzel)


def testWartetAufÄndertNichtsAmDran(repo):
    kopf = "15 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · offen"
    repo.datei("handoff/anliegen/15-probe.md", f"# Probe\n\n{kopf}\n\nwartet auf 16\n")
    assert "Dran: Planer (15)" in stand(repo.wurzel)


@pytest.mark.stand
def testDerPostToolUseHookAufAgentMeldetDenStand():
    einstellungen = json.loads(
        (Path(__file__).parents[3] / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    treffer = [
        eintrag
        for eintrag in einstellungen["hooks"]["PostToolUse"]
        if eintrag.get("matcher") == "Agent" and "standregeln.stand" in str(eintrag)
    ]
    assert treffer


def testStandNenntEinKriteriumOhneTestAlsWartendAufDenTestautor(repo):
    text = "### AU-1 · A\n\n- AU-1.1 Eins.\n- AU-1.2 Zwei.\n"
    repo.datei("domaene/anforderungen/aufstellung.md", text)
    repo.datei("technik/tests/akzeptanz/aufstellungTest.py", "def testAu1_1Eins(): ...\n")
    assert "AU-1.2 wartet auf den Testautor" in stand(repo.wurzel)
