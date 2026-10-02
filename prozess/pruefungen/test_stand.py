import json
import subprocess

import pytest

from stand import aktuelle_etappe, lage, protokoll, stand


class Repo:
    def __init__(self, wurzel):
        self.wurzel = wurzel
        self.git("init", "-q")

    def git(self, *argumente):
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@t", *argumente],
            cwd=self.wurzel, check=True, capture_output=True,
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


def bis_zur_freigabe_von_plan_1(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    repo.datei("handoff/plan.md", "# Plan · Zyklus 1\n")
    repo.freigabe("Plan", 1)


def test_ohne_etappe_leitet_der_planer_sie_ab(repo):
    assert lage(repo.wurzel) == (1, "Domänenphase", "Planer: Etappen aus dem Ziel ableiten")


def test_etappe_ohne_freigabe_wartet(repo):
    etappe(repo)
    assert lage(repo.wurzel)[2] == "Etappe 1 wartet auf Kritik (Architekt) und Freigabe"


def test_nach_freigabe_der_etappe_ist_die_erste_anforderung_dran(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    assert lage(repo.wurzel)[2] == "Anforderungsautor: erste Anforderung zu Etappe 1"


def test_eine_anforderung_genuegt_fuer_den_plan(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    assert lage(repo.wurzel)[2].startswith("Planer: Plan 1 mit den Items, die bereit sind")


def test_plan_ohne_freigabe_wartet(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    repo.datei("handoff/plan.md", "# Plan · Zyklus 1\n")
    assert lage(repo.wurzel) == (
        1, "Domänenphase", "Plan 1 wartet auf Kritik (Architekt) und Freigabe"
    )


def test_freigabe_des_plans_wechselt_in_die_technik(repo):
    bis_zur_freigabe_von_plan_1(repo)
    assert lage(repo.wurzel) == (
        1, "Technikphase", "Testautor: Akzeptanztests zu den Items von Plan 1"
    )


def test_nach_den_akzeptanztests_ist_der_implementierer_dran(repo):
    bis_zur_freigabe_von_plan_1(repo)
    repo.datei("technik/tests/akzeptanz/test_au_1.py", "def test_au_1_1(): ...\n")
    assert lage(repo.wurzel)[2] == "Implementierer, dann Reviewer: Tests grün, Review 1"


def test_review_wechselt_in_den_prozess(repo):
    bis_zur_freigabe_von_plan_1(repo)
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    assert lage(repo.wurzel) == (1, "Prozessphase", "Organisationsentwickler: Retro 1")


def test_retro_ohne_freigabe_wartet(repo):
    bis_zur_freigabe_von_plan_1(repo)
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    repo.datei("handoff/retro.md", "# Retro · Zyklus 1\n")
    assert lage(repo.wurzel)[2] == "Retro 1 wartet auf Kritik und Freigabe"


def test_freigabe_der_retro_beginnt_den_naechsten_zyklus(repo):
    bis_zur_freigabe_von_plan_1(repo)
    repo.datei("handoff/review.md", "# Review · Zyklus 1\n")
    repo.datei("handoff/retro.md", "# Retro · Zyklus 1\n")
    repo.freigabe("Retro", 1)
    assert lage(repo.wurzel)[:2] == (2, "Domänenphase")
    assert lage(repo.wurzel)[2].startswith("Planer: Plan 2")


def test_freigabe_von_plan_12_zaehlt_nicht_fuer_plan_1(repo):
    etappe(repo)
    repo.freigabe("Etappe", 1)
    anforderung(repo)
    repo.datei("handoff/plan.md", "# Plan · Zyklus 1\n")
    repo.freigabe("Plan", 12)
    assert lage(repo.wurzel)[1] == "Domänenphase"


def test_aktuelle_etappe_ist_die_erste_datei_nach_namen(repo):
    repo.datei("domaene/etappen/02-bewegen.md", "# Etappe 2 · Bewegen\n")
    repo.datei("domaene/etappen/01-aufstellen.md", "# Etappe 1 · Aufstellen\n")
    assert aktuelle_etappe(repo.wurzel) == (1, "Etappe 1 · Aufstellen")


def test_budget_steht_im_stand_und_meldet_ueberschreitung(repo):
    datei = protokoll(repo.wurzel)
    datei.parent.mkdir(parents=True)
    eintrag = json.dumps({"phase": "Zyklus 1 · Domänenphase", "rolle": "planer"})
    datei.write_text((eintrag + "\n") * 3, encoding="utf-8")
    assert "Budget 3/8 Rollenläufe" in stand(repo.wurzel)
    datei.write_text((eintrag + "\n") * 9, encoding="utf-8")
    assert "über Budget (9/8 Rollenläufe)" in stand(repo.wurzel)
