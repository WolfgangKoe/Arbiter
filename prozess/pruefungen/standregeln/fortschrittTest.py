import json
from pathlib import Path

from standregeln.fortschritt import fortschrittSchreiben

freigabeAbschnitt = "## Freigabe\nFreigabe: offen\nKommentar: .\n"
anforderung = "### AUF-1 Stellen\n\n- AUF-1.1 Ein Modell steht.\n"
test = '"""Stellen."""\n\n\ndef testAuf1_1EinModellSteht():\n    pass\n'


def schreiben(wurzel: Path, pfad: str, text: str) -> Path:
    datei = wurzel / pfad
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(text, encoding="utf-8")
    return datei


def planMitItem(wurzel: Path, gitRepo) -> Path:
    plan = schreiben(
        wurzel,
        "handoff/plan.md",
        "# Plan · Zyklus 1\n\n## Items\n1. [Stellen](../domaene/items/stellen.md)\n\n"
        + freigabeAbschnitt,
    )
    schreiben(wurzel, "domaene/items/stellen.md", "# Stellen\n\nAUF-1.1\n")
    schreiben(wurzel, "domaene/anforderungen/auf.md", anforderung)
    gitRepo.festhalten("Freigabe Plan 1")
    return plan


def testDieTechnikphaseSchreibtDenAbschnittVorDieFreigabeUndLässtDenRestStehen(tmp_path, gitRepo):
    plan = planMitItem(tmp_path, gitRepo)
    vorher = plan.read_text(encoding="utf-8")
    assert fortschrittSchreiben(tmp_path) == "handoff/plan.md"
    text = plan.read_text(encoding="utf-8")
    kopf, _, rest = text.partition("## Fortschritt\n")
    assert kopf == vorher.partition("## Freigabe")[0]
    assert rest.endswith(freigabeAbschnitt)
    assert "- [ ] Testautor: Tests zu Item stellen\n" in rest
    assert "- [ ] Stakeholder: Freigabe Review 1\n" in rest


def testEinFaktHaktSelbstAb(tmp_path, gitRepo):
    plan = planMitItem(tmp_path, gitRepo)
    fortschrittSchreiben(tmp_path)
    schreiben(tmp_path, "technik/tests/akzeptanz/aufTest.py", test)
    (tmp_path / "domaene/items/stellen.md").unlink()
    fortschrittSchreiben(tmp_path)
    text = plan.read_text(encoding="utf-8")
    assert "- [x] Testautor: Tests zu Item stellen\n" in text
    assert "- [x] Planer: Item stellen gelöscht\n" in text
    for zeile in (
        "Fachkritiker: Kritik an den Tests zu Item stellen",
        "Architekt: Kritik an den Tests zu Item stellen",
        "Implementierer: Tests zu Item stellen grün",
        "Reviewer: Kritik am Code zu Item stellen",
        "Fachkritiker: Item stellen abgenommen",
        "Reviewer: DoD über das Inkrement",
    ):
        assert f"- [x] {zeile}\n" in text


def testEinOffenesItemLässtDieSchritteDavorOffen(tmp_path, gitRepo):
    plan = planMitItem(tmp_path, gitRepo)
    fortschrittSchreiben(tmp_path)
    text = plan.read_text(encoding="utf-8")
    assert "- [ ] Fachkritiker: Item stellen abgenommen\n" in text
    assert "- [ ] Reviewer: DoD über das Inkrement\n" in text


def testEinKriteriumOhneTestLässtDieZeileOffen(tmp_path, gitRepo):
    plan = planMitItem(tmp_path, gitRepo)
    schreiben(tmp_path, "technik/tests/akzeptanz/aufTest.py", '"""Stellen."""\n')
    fortschrittSchreiben(tmp_path)
    assert "- [ ] Testautor: Tests zu Item stellen\n" in plan.read_text(encoding="utf-8")


def testHakenUndHindernisBleibenBeimNeuschreibenStehen(tmp_path, gitRepo):
    plan = planMitItem(tmp_path, gitRepo)
    fortschrittSchreiben(tmp_path)
    text = plan.read_text(encoding="utf-8")
    zeile = "Implementierer: Tests zu Item stellen grün\n"
    text = text.replace(
        f"- [ ] {zeile}", f"- [x] {zeile}  Hindernis: Pfad gesperrt (Anliegen 560)\n"
    )
    plan.write_text(text, encoding="utf-8")
    assert fortschrittSchreiben(tmp_path) is None
    assert plan.read_text(encoding="utf-8") == text


def testEinZweiterLaufÄndertNichts(tmp_path, gitRepo):
    plan = planMitItem(tmp_path, gitRepo)
    fortschrittSchreiben(tmp_path)
    erster = plan.read_text(encoding="utf-8")
    assert fortschrittSchreiben(tmp_path) is None
    assert plan.read_text(encoding="utf-8") == erster


def testDieDomänenphaseSchreibtInsReviewUndHaktDenPlanAb(tmp_path, gitRepo):
    review = schreiben(tmp_path, "handoff/review.md", "# Review · Zyklus 1\n\n" + freigabeAbschnitt)
    schreiben(tmp_path, "handoff/plan.md", "# Plan · Zyklus 1\n")
    schreiben(tmp_path, "handoff/retro.md", "# Retro · Zyklus 1\n\n## Prozess-Items\n")
    gitRepo.festhalten("Freigabe Plan 1")
    gitRepo.festhalten("Freigabe Review 1")
    gitRepo.festhalten("Freigabe Retro 1")
    fortschrittSchreiben(tmp_path)
    assert "- [ ] Planer: Plan geschrieben\n" in review.read_text(encoding="utf-8")
    schreiben(tmp_path, "handoff/plan.md", "# Plan · Zyklus 2\n")
    fortschrittSchreiben(tmp_path)
    text = review.read_text(encoding="utf-8")
    assert "- [x] Planer: Plan geschrieben\n" in text
    assert "- [ ] Stakeholder: Freigabe Plan 2\n" in text


def testInZyklusEinsGibtEsKeinReviewAbschnittNurDenDesPlans(tmp_path):
    assert fortschrittSchreiben(tmp_path) is None
    plan = schreiben(tmp_path, "handoff/plan.md", "# Plan · Zyklus 1\n")
    assert fortschrittSchreiben(tmp_path) == "handoff/plan.md"
    assert "- [ ] Reviewer: Review geschrieben\n" in plan.read_text(encoding="utf-8")
    assert not (tmp_path / "handoff/review.md").exists()


def testDieProzessphaseHaktEinProzessItemMitSeinemCommitAb(tmp_path, gitRepo):
    schreiben(tmp_path, "handoff/plan.md", "# Plan · Zyklus 1\n")
    schreiben(tmp_path, "handoff/review.md", "# Review · Zyklus 1\n")
    retro = schreiben(
        tmp_path,
        "handoff/retro.md",
        "# Retro · Zyklus 1\n\n## Prozess-Items\n- P1 Eins\n- P2 Zwei\n\n" + freigabeAbschnitt,
    )
    gitRepo.festhalten("Freigabe Plan 1")
    gitRepo.festhalten("Freigabe Review 1")
    gitRepo.festhalten("Freigabe Retro 1")
    gitRepo.festhalten("P1: Eins umgesetzt")
    fortschrittSchreiben(tmp_path)
    text = retro.read_text(encoding="utf-8")
    assert "- [x] Regelumsetzer: P1\n" in text
    assert "- [ ] Regelumsetzer: P2\n" in text
    assert "- [x] Stakeholder: Freigabe Retro 1\n" in text
    assert "- [ ] Koordinator: nach dev gepusht\n" in text


def testBeginntDieNächstePhaseErhältDieRetroIhrenEndstand(tmp_path, gitRepo):
    schreiben(tmp_path, "handoff/plan.md", "# Plan · Zyklus 1\n")
    schreiben(tmp_path, "handoff/review.md", "# Review · Zyklus 1\n")
    retro = schreiben(
        tmp_path, "handoff/retro.md", "# Retro · Zyklus 1\n\n## Prozess-Items\n- P1 Eins\n\n"
    )
    for betreff in ("Freigabe Plan 1", "Freigabe Review 1", "Freigabe Retro 1", "P1: Eins"):
        gitRepo.festhalten(betreff)
    assert "handoff/retro.md" in fortschrittSchreiben(tmp_path)
    assert "- [x] Regelumsetzer: P1\n" in retro.read_text(encoding="utf-8")


def testEinProzessItemTrägtDieRolleAusSeinerKlammer(tmp_path, gitRepo):
    schreiben(tmp_path, ".claude/agents/organisationsentwickler.md", "---\nname: x\n---\n")
    schreiben(tmp_path, "handoff/plan.md", "# Plan · Zyklus 1\n")
    schreiben(tmp_path, "handoff/review.md", "# Review · Zyklus 1\n")
    retro = schreiben(
        tmp_path,
        "handoff/retro.md",
        "# Retro · Zyklus 1\n\n## Prozess-Items\n- P1 Ablauf (Organisationsentwickler): neu\n"
        "- P2 Werkzeug (Regelumsetzer, 692): neu\n- P3 Ohne Klammer\n\n" + freigabeAbschnitt,
    )
    for betreff in ("Freigabe Plan 1", "Freigabe Review 1", "Freigabe Retro 1"):
        gitRepo.festhalten(betreff)
    fortschrittSchreiben(tmp_path)
    text = retro.read_text(encoding="utf-8")
    assert "- [ ] Organisationsentwickler: P1\n" in text
    assert "- [ ] Regelumsetzer: P2\n" in text
    assert "- [ ] Regelumsetzer: P3\n" in text
    assert "- [ ] Architekt: Kritik an der Retro\n" in text


def testJederKritikerStehtJeItemBeiDerKritikAmCode(tmp_path, gitRepo):
    plan = planMitItem(tmp_path, gitRepo)
    fortschrittSchreiben(tmp_path)
    text = plan.read_text(encoding="utf-8")
    assert "- [ ] Architekt: Kritik am Code zu Item stellen\n" in text
    assert "- [ ] Reviewer: Kritik am Code zu Item stellen\n" in text


def testDieDomänenzeilenFolgenDerTabelle(tmp_path, gitRepo):
    review = schreiben(tmp_path, "handoff/review.md", "# Review · Zyklus 1\n\n" + freigabeAbschnitt)
    schreiben(tmp_path, "handoff/plan.md", "# Plan · Zyklus 1\n")
    schreiben(tmp_path, "handoff/retro.md", "# Retro · Zyklus 1\n\n## Prozess-Items\n")
    for betreff in ("Freigabe Plan 1", "Freigabe Review 1", "Freigabe Retro 1"):
        gitRepo.festhalten(betreff)
    fortschrittSchreiben(tmp_path)
    text = review.read_text(encoding="utf-8")
    for zeile in (
        "Anforderungsautor: Happy Paths zum Zyklusziel",
        "Fachkritiker: Kritik an Anforderungen und Mockups",
        "Fachkritiker: Kritik am Plan",
        "Architekt: Kritik am Plan",
    ):
        assert f"- [ ] {zeile}\n" in text


def testDerPlanTrägtVorDerFreigabeDieTechnikzeilenAlleOffen(tmp_path, gitRepo):
    schreiben(tmp_path, "handoff/review.md", "# Review · Zyklus 1\n")
    plan = schreiben(
        tmp_path,
        "handoff/plan.md",
        "# Plan · Zyklus 2\n\n## Items\n1. [Stellen](../domaene/items/stellen.md)\n\n"
        + freigabeAbschnitt,
    )
    schreiben(tmp_path, "handoff/retro.md", "# Retro · Zyklus 1\n\n## Prozess-Items\n")
    schreiben(tmp_path, "domaene/items/stellen.md", "# Stellen\n\nAUF-1.1\n")
    schreiben(tmp_path, "domaene/anforderungen/auf.md", anforderung)
    schreiben(tmp_path, "technik/tests/akzeptanz/aufTest.py", test)
    for betreff in ("Freigabe Plan 1", "Freigabe Review 1", "Freigabe Retro 1"):
        gitRepo.festhalten(betreff)
    fortschrittSchreiben(tmp_path)
    text = plan.read_text(encoding="utf-8")
    assert "- [ ] Testautor: Tests zu Item stellen\n" in text
    assert "- [ ] Reviewer: Review geschrieben\n" in text
    assert "- [x]" not in text


def testDasReviewTrägtVorDerFreigabeDieDomänenzeilenDesFolgezyklusOffen(tmp_path, gitRepo):
    schreiben(tmp_path, "handoff/plan.md", "# Plan · Zyklus 1\n")
    review = schreiben(
        tmp_path,
        "handoff/review.md",
        "# Review · Zyklus 1\n\n## Fortschritt\n- [x] Anforderungsautor: Happy Paths zum"
        " Zyklusziel\n- [x] Stakeholder: Freigabe Plan 1\n\n" + freigabeAbschnitt,
    )
    gitRepo.festhalten("Freigabe Plan 1")
    fortschrittSchreiben(tmp_path)
    text = review.read_text(encoding="utf-8")
    assert "- [ ] Anforderungsautor: Happy Paths zum Zyklusziel\n" in text
    assert "- [ ] Stakeholder: Freigabe Plan 2\n" in text
    assert "- [x]" not in text


def testJedesItemHatVorDenTestsDieVertragszeileDesArchitekten(tmp_path, gitRepo):
    plan = planMitItem(tmp_path, gitRepo)
    fortschrittSchreiben(tmp_path)
    text = plan.read_text(encoding="utf-8")
    vertrag = "- [ ] Architekt: Vertrag zu Item stellen, bei beiden Hälften\n"
    assert vertrag + "- [ ] Testautor: Tests zu Item stellen\n" in text


def testHooksStartenDasSkriptNachJedemRollenlaufUndNachBashBefehlen():
    einstellungen = json.loads(
        (Path(__file__).parents[3] / ".claude" / "settings.json").read_text(encoding="utf-8")
    )["hooks"]
    nachTool = einstellungen["PostToolUse"]
    nachBash = [eintrag for eintrag in nachTool if eintrag.get("matcher") == "Bash"]
    assert any("standregeln.fortschritt" in str(eintrag) for eintrag in nachBash)
    nachRolle = einstellungen["SubagentStop"]
    assert any("standregeln.fortschritt" in str(eintrag) for eintrag in nachRolle)
