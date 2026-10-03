import json
import subprocess
from pathlib import Path

import pytest

from phasenfolge import aktuelleEtappe, lage
from stand import stand


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
    repo.datei(
        "domaene/anforderungen/aufstellung.md", "### AU-1 · Modell setzen\n\n- AU-1.1 Eins.\n"
    )


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
    assert lage(repo.wurzel).schritt == "Etappe 1 wartet auf Kritik (Architekt) und Freigabe"


def testNachFreigabeDerEtappeIstDieErsteAnforderungDran(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    assert lage(repo.wurzel).schritt == "Anforderungsautor: Anforderungen zu Plan 1"


def testEineAnforderungGenügtFürDenPlan(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    assert lage(repo.wurzel).schritt.startswith("Planer: Plan 1 mit den Items, die bereit sind")


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


def planMitItem(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    repo.datei("domaene/items/probe.md", "# Probe\n")
    repo.datei("handoff/plan.md", "# Plan · Zyklus 1\n\n1. [Probe](../domaene/items/probe.md)\n")
    repo.freigabe("Plan", 1)
    repo.datei("technik/tests/akzeptanz/auTest.py", "def testAu1_1Probe(): ...\n")


def testSolangeEinItemOffenIstNenntDerStandDieAbnahmeAuchMitReview(repo):
    planMitItem(repo)
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    aktuelle = lage(repo.wurzel)
    assert aktuelle.phase == "Technikphase"
    assert "Fachkritiker: Abnahme" in aktuelle.schritt


def testGelöschtesItemOhneReviewNenntDenReviewer(repo):
    planMitItem(repo)
    repo.git("rm", "-q", "domaene/items/probe.md")
    repo.git("commit", "-qm", "Item gelöscht")
    assert lage(repo.wurzel) == (1, "Technikphase", "Reviewer: Review 1")


def testGelöschtesItemMitReviewWechseltInDenProzess(repo):
    planMitItem(repo)
    repo.git("rm", "-q", "domaene/items/probe.md")
    repo.git("commit", "-qm", "Item gelöscht")
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    assert lage(repo.wurzel) == (1, "Prozessphase", "Organisationsentwickler: Retro 1")


def testNachDenAkzeptanztestsOhneItemIstDerReviewerDran(repo):
    bisZurFreigabeVonPlan1(repo)
    repo.datei("technik/tests/akzeptanz/auTest.py", "def testAu1_1Probe(): ...\n")
    assert lage(repo.wurzel).schritt == "Reviewer: Review 1"


def testReviewWechseltInDenProzess(repo):
    bisZurFreigabeVonPlan1(repo)
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    assert lage(repo.wurzel) == (1, "Prozessphase", "Organisationsentwickler: Retro 1")


def testRetroOhneFreigabeWartet(repo):
    bisZurFreigabeVonPlan1(repo)
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    repo.datei("handoff/retro.md", "# Retro · Zyklus 1\n")
    assert lage(repo.wurzel).schritt == "Retro 1 wartet auf Kritik und Freigabe"


def testFreigabeDerRetroBeginntDenNächstenZyklus(repo):
    bisZurFreigabeVonPlan1(repo)
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    repo.datei("handoff/retro.md", "# Retro · Zyklus 1\n")
    repo.freigabe("Retro", 1)
    aktuelle = lage(repo.wurzel)
    assert (aktuelle.zyklus, aktuelle.phase) == (2, "Domänenphase")
    assert aktuelle.schritt.startswith("Planer: Plan 2")


def testFreigabeVonPlan12ZähltNichtFürPlan1(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    repo.datei("handoff/plan.md", "# Plan · Zyklus 1\n")
    repo.freigabe("Plan", 12)
    assert lage(repo.wurzel).phase == "Domänenphase"


def testAktuelleEtappeIstDieErsteDateiNachNamen(repo):
    repo.datei("domaene/etappen/02-bewegen.md", "# Etappe 2 · Bewegen\n")
    repo.datei("domaene/etappen/01-aufstellen.md", "# Etappe 1 · Aufstellen\n")
    assert aktuelleEtappe(repo.wurzel) == (1, "Etappe 1 · Aufstellen")


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


def testStandMeldetCodeCommitOhneKritik(repo):
    repo.datei("prozess/pruefungen/probe.py", "x = 1\n")
    kennung = subprocess.run(
        ["git", "rev-parse", "--short=7", "HEAD"], cwd=repo.wurzel, capture_output=True, text=True
    ).stdout.strip()
    assert f"Kritik am Code fällig: Reviewer ({kennung})" in stand(repo.wurzel)
    repo.git("commit", "-q", "--allow-empty", "-m", f"Kritik {kennung} ohne Befund")
    assert "Kritik am Code" not in stand(repo.wurzel)


def testDerPostToolUseHookAufAgentMeldetDenStand():
    einstellungen = json.loads(
        (Path(__file__).parents[2] / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    treffer = [
        eintrag
        for eintrag in einstellungen["hooks"]["PostToolUse"]
        if eintrag.get("matcher") == "Agent" and "stand.py" in str(eintrag)
    ]
    assert treffer


def testStandNenntEinKriteriumOhneTestAlsWartendAufDenTestautor(repo):
    text = "### AU-1 · A\n\n- AU-1.1 Eins.\n- AU-1.2 Zwei.\n"
    repo.datei("domaene/anforderungen/aufstellung.md", text)
    repo.datei("technik/tests/akzeptanz/aufstellungTest.py", "def testAu1_1Eins(): ...\n")
    assert "AU-1.2 wartet auf den Testautor" in stand(repo.wurzel)


def planOhneFreigabe(repo, itemzeile):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    repo.datei("handoff/plan.md", f"# Plan · Zyklus 1\n\n## Item\n{itemzeile}\n")


def testPlanMitItemOhneLinkVerlangtDenLinkVomPlaner(repo):
    planOhneFreigabe(repo, "1. *Reihenfolge der Aufstellung*")
    assert lage(repo.wurzel) == (
        1,
        "Domänenphase",
        "Planer: Items von Plan 1 als Link auf domaene/items/",
    )


def testPlanMitLinkAufEinGelöschtesItemWartetAufKritikUndFreigabe(repo):
    planOhneFreigabe(repo, "1. [Probe](../domaene/items/probe.md)")
    assert lage(repo.wurzel) == (
        1,
        "Domänenphase",
        "Plan 1 wartet auf Kritik (Architekt) und Freigabe",
    )


def kurzerHashVon(repo):
    return subprocess.run(
        ["git", "rev-parse", "--short=7", "HEAD"], cwd=repo.wurzel, capture_output=True, text=True
    ).stdout.strip()


def testStandNenntAlleKritikerDerGetroffenenPfade(repo):
    for pfad in ("prozess/pruefungen/probe.py", "pyproject.toml"):
        (repo.wurzel / pfad).parent.mkdir(parents=True, exist_ok=True)
        (repo.wurzel / pfad).write_text("x = 1\n", encoding="utf-8")
    repo.git("add", "-A")
    repo.git("commit", "-qm", "Regelumsetzer: Probe")
    assert "Kritik am Code fällig: Reviewer und Architekt" in stand(repo.wurzel)


def testCommitOhneBetreffLegtDenStandNichtLahm(repo):
    repo.datei("technik/arbiter/probe.py", "x = 1\n")
    repo.git("commit", "-q", "--allow-empty", "--allow-empty-message", "-m", "")
    assert "Kritik am Code fällig" in stand(repo.wurzel)


def testEinCodeCommitMitKritikImBetreffWirdTrotzdemGemeldet(repo):
    repo.datei("technik/arbiter/probe.py", "x = 1\n")
    erster = kurzerHashVon(repo)
    repo.git("commit", "-q", "--allow-empty", "-m", f"Kritik {erster} ohne Befund")
    (repo.wurzel / "technik/arbiter/probe2.py").write_text("y = 2\n", encoding="utf-8")
    repo.git("add", "-A")
    repo.git("commit", "-qm", f"Implementierer: Befund aus Kritik {erster}")
    zweiter = kurzerHashVon(repo)
    assert f"Kritik am Code fällig: Reviewer ({zweiter})" in stand(repo.wurzel)


def testEinKritikCommitDecktMehrereHashes(repo):
    repo.datei("technik/arbiter/probe.py", "x = 1\n")
    erster = kurzerHashVon(repo)
    repo.datei("technik/arbiter/probe2.py", "y = 2\n")
    zweiter = kurzerHashVon(repo)
    repo.git("commit", "-q", "--allow-empty", "-m", f"Kritik {erster} {zweiter}")
    assert "Kritik am Code" not in stand(repo.wurzel)


def retroFreigegebenMitAnforderung(repo, anforderungstext, testtext):
    bisZurFreigabeVonPlan1(repo)
    repo.datei("domaene/anforderungen/aufstellung.md", anforderungstext)
    if testtext:
        repo.datei("technik/tests/akzeptanz/aufstellungTest.py", testtext)
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    repo.datei("handoff/retro.md", "# Retro · Zyklus 1\n")
    repo.freigabe("Retro", 1)


def testNachRetroOhneKriteriumOhneTestIstDerAnforderungsautorDran(repo):
    retroFreigegebenMitAnforderung(
        repo, "### AU-1 · A\n\n- AU-1.1 Eins.\n", "def testAu1_1Eins(): ...\n"
    )
    assert lage(repo.wurzel).schritt == "Anforderungsautor: Anforderungen zu Plan 2"


def testNachRetroMitKriteriumOhneTestIstDerPlanerDran(repo):
    retroFreigegebenMitAnforderung(
        repo, "### AU-1 · A\n\n- AU-1.1 Eins.\n- AU-1.2 Zwei.\n", "def testAu1_1Eins(): ...\n"
    )
    assert lage(repo.wurzel).schritt.startswith("Planer: Plan 2")


def planMitItemtext(repo, anforderungstext, testtext, itemtext):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    repo.datei("domaene/anforderungen/aufstellung.md", anforderungstext)
    repo.datei("technik/tests/akzeptanz/aufstellungTest.py", testtext)
    repo.datei("domaene/items/probe.md", itemtext)
    repo.datei("handoff/plan.md", "# Plan · Zyklus 1\n\n1. [Probe](../domaene/items/probe.md)\n")


zweiKriterienEinsGetestet = "### AU-1 · A\n\n- AU-1.1 Eins.\n- AU-1.2 Zwei.\n"


def testPlanOhneKriteriumOhneTestVerlangtKriterienVomAnforderungsautor(repo):
    planMitItemtext(
        repo,
        "### AU-1 · A\n\n- AU-1.1 Eins.\n",
        "def testAu1_1Eins(): ...\n",
        "# Probe\n\nAU-1.\n",
    )
    assert lage(repo.wurzel).schritt == "Anforderungsautor: Kriterien zu den Items von Plan 1"


def testPlanDessenItemKeinFehlendesKriteriumNenntVerlangtKriterienIdsVomPlaner(repo):
    planMitItemtext(
        repo, zweiKriterienEinsGetestet, "def testAu1_1Eins(): ...\n", "# Probe\n\nAU-1.1.\n"
    )
    assert lage(repo.wurzel).schritt == "Planer: Kriterien-IDs in die Items von Plan 1"


def testPlanDessenItemsEinFehlendesKriteriumNennenWartetAufKritikUndFreigabe(repo):
    planMitItemtext(
        repo, zweiKriterienEinsGetestet, "def testAu1_1Eins(): ...\n", "# Probe\n\nAU-1.2.\n"
    )
    assert lage(repo.wurzel).schritt == "Plan 1 wartet auf Kritik (Architekt) und Freigabe"
