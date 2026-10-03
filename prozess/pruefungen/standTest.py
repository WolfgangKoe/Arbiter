import json
import subprocess

import pytest

from stand import aktuelleEtappe, lage, protokoll, stand


class Repo:
    def __init__(self, wurzel):
        self.wurzel = wurzel
        self.git("init", "-q")

    def git(self, *argumente):
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@t", *argumente],
            cwd=self.wurzel,
            check=True,
            capture_output=True,
        )

    def datei(self, pfad, text):
        ziel = self.wurzel / pfad
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(text, encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-qm", f"{pfad} geschrieben")

    def freigabe(self, gegenstand, nummer):
        self.git("commit", "-q", "--allow-empty", "-m", f"Freigabe {gegenstand} {nummer}")


@pytest.fixture
def repo(tmp_path):
    return Repo(tmp_path)


def etappe(repo):
    repo.datei("domaene/etappen/01-aufstellen.md", "# Etappe 1 · Aufstellen\nZweck.\n")


def anforderung(repo):
    repo.datei("domaene/anforderungen/aufstellung.md", "### AU-1 · Modell setzen\n")


def bisZurFreigabeVonPlan1(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    repo.datei("handoff/plan.md", "# Plan · Zyklus 1\n")
    repo.freigabe("Plan", 1)


def anliegen(repo, nummer, status, absender="Architekt", empfänger="Planer"):
    kopf = f"{nummer} · Kritik · von {absender} (Technik) → {empfänger} · Runde 1/3 · {status}"
    repo.datei(f"handoff/anliegen/{nummer}-probe.md", f"# Probe\n\n{kopf}\n")


def testOhneEtappeLeitetDerPlanerSieAb(repo):
    assert lage(repo.wurzel) == (1, "Domänenphase", "Planer: Etappen aus dem Ziel ableiten")


def testEtappeOhneFreigabeWartet(repo):
    etappe(repo)
    assert lage(repo.wurzel)[2] == "Etappe 1 wartet auf Kritik (Architekt) und Freigabe"


def testNachFreigabeDerEtappeIstDieErsteAnforderungDran(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    assert lage(repo.wurzel)[2] == "Anforderungsautor: erste Anforderung zu Etappe 1"


def testEineAnforderungGenügtFürDenPlan(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    assert lage(repo.wurzel)[2].startswith("Planer: Plan 1 mit den Items, die bereit sind")


def testPlanOhneFreigabeWartet(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    repo.datei("handoff/plan.md", "# Plan · Zyklus 1\n")
    assert lage(repo.wurzel) == (
        1,
        "Domänenphase",
        "Plan 1 wartet auf Kritik (Architekt) und Freigabe",
    )


def testFreigabeDesPlansWechseltInDieTechnik(repo):
    bisZurFreigabeVonPlan1(repo)
    assert lage(repo.wurzel) == (
        1,
        "Technikphase",
        "Testautor: Akzeptanztests zu den Items von Plan 1",
    )


def testNachDenAkzeptanztestsIstDerImplementiererDran(repo):
    bisZurFreigabeVonPlan1(repo)
    repo.datei("technik/tests/akzeptanz/auTest.py", "def testAu1_1Probe(): ...\n")
    assert lage(repo.wurzel)[2] == "Implementierer, dann Reviewer: Tests grün, Review 1"


def testReviewWechseltInDenProzess(repo):
    bisZurFreigabeVonPlan1(repo)
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    assert lage(repo.wurzel) == (1, "Prozessphase", "Organisationsentwickler: Retro 1")


def testRetroOhneFreigabeWartet(repo):
    bisZurFreigabeVonPlan1(repo)
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    repo.datei("handoff/retro.md", "# Retro · Zyklus 1\n")
    assert lage(repo.wurzel)[2] == "Retro 1 wartet auf Kritik und Freigabe"


def testFreigabeDerRetroBeginntDenNächstenZyklus(repo):
    bisZurFreigabeVonPlan1(repo)
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    repo.datei("handoff/retro.md", "# Retro · Zyklus 1\n")
    repo.freigabe("Retro", 1)
    assert lage(repo.wurzel)[:2] == (2, "Domänenphase")
    assert lage(repo.wurzel)[2].startswith("Planer: Plan 2")


def testFreigabeVonPlan12ZähltNichtFürPlan1(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    repo.datei("handoff/plan.md", "# Plan · Zyklus 1\n")
    repo.freigabe("Plan", 12)
    assert lage(repo.wurzel)[1] == "Domänenphase"


def testAktuelleEtappeIstDieErsteDateiNachNamen(repo):
    repo.datei("domaene/etappen/02-bewegen.md", "# Etappe 2 · Bewegen\n")
    repo.datei("domaene/etappen/01-aufstellen.md", "# Etappe 1 · Aufstellen\n")
    assert aktuelleEtappe(repo.wurzel) == (1, "Etappe 1 · Aufstellen")


def testRollenläufeStehenAlsKennzahlImStand(repo):
    datei = protokoll(repo.wurzel)
    datei.parent.mkdir(parents=True)
    eintrag = json.dumps({"phase": "Zyklus 1 · Domänenphase", "rolle": "planer"})
    datei.write_text((eintrag + "\n") * 3, encoding="utf-8")
    assert "Rollenläufe 3/8" in stand(repo.wurzel)


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
