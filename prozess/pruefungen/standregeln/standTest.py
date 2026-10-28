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
    kopf = f"Form: Kritik\nVon: {absender}\nAn: {empfänger}\nRunde: 1/3\nStatus: {status}"
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
    kopf = "Form: Kritik\nVon: Architekt\nAn: Planer\nRunde: 1/3\nStatus: offen"
    repo.datei("handoff/anliegen/15-probe.md", f"# Probe\n\n{kopf}\n\nwartet auf 16\n")
    assert "Dran: Planer (15)" in stand(repo.wurzel)


def testStandZähltWartendeNichtUnterDran(repo):
    kopf = "Form: Kritik\nVon: Architekt\nAn: Planer\nRunde: 1/3\nStatus: offen\nWartet auf: 16"
    repo.datei("handoff/anliegen/15-probe.md", f"# Probe\n\n{kopf}\n")
    anliegen(repo, "16", "offen", absender="Architekt", empfänger="Regelumsetzer")
    text = stand(repo.wurzel)
    assert "Dran: Regelumsetzer (16)" in text
    assert "Planer" not in text.partition("Wartet")[0].partition("Dran")[2]
    assert "Wartet: 15 (auf 16)" in text


def testStandBeginntMitEtappeUndBelegtenKriterien(repo):
    repo.datei("domaene/etappen/01-aufstellen.md", "# Etappe 1 · Aufstellen\n")
    repo.datei("domaene/etappen/02-bewegen.md", "# Etappe 2 · Bewegen\n")
    text = "### AU-1 · A\n\n- AU-1.1 Eins.\n- AU-1.2 Zwei.\n"
    repo.datei("domaene/anforderungen/aufstellung.md", text)
    repo.datei("technik/tests/akzeptanz/aufstellungTest.py", "def testAu1_1Eins(): ...\n")
    assert stand(repo.wurzel).startswith(
        "Stand: Etappe 1 von 2 (Aufstellen), Zyklus 1; 1 von 2 Kriterien belegt, "
        "davon Etappe 1: 0 von 0 · "
    )


def testStandNenntDieBelegtenKriterienDerEtappeNebenAllen(repo):
    repo.datei("domaene/etappen/02-bewegen.md", "# Etappe 2 · Bewegen\n")
    text = (
        "### AU-1 · A\n\nEtappe: 2\n\n- AU-1.1 Eins.\n- AU-1.2 Zwei.\n- AU-1.3 Drei. (Etappe 3)\n\n"
        "### AU-2 · B\n\n- AU-2.1 Vier.\n"
    )
    repo.datei("domaene/anforderungen/aufstellung.md", text)
    repo.datei("technik/tests/akzeptanz/aufstellungTest.py", "def testAu1_1Eins(): ...\n")
    assert "; 1 von 4 Kriterien belegt, davon Etappe 2: 1 von 2 · " in stand(repo.wurzel)


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
