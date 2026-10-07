import pytest

from standregeln.phasenfolge import lage
from standregeln.stand import stand

planKopf = "# Plan · Zyklus 3\n\n## Items\n"
etappe = "# Etappe 1 · Aufstellen\n"


@pytest.fixture
def repo(gitRepo):
    def datei(pfad, text):
        ziel = gitRepo.ordner / pfad
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(text, encoding="utf-8")

    datei("domaene/etappen/01-aufstellen.md", etappe)
    gitRepo.datei = datei
    return gitRepo


def schritt(repo):
    return lage(repo.ordner).schritt


def testOhnePlanFolgtDerPlanerImErstenZyklus(repo):
    gefunden = lage(repo.ordner)
    assert (gefunden.etappe, gefunden.zyklus, gefunden.phase.value) == (
        "Etappe 1 · Aufstellen",
        1,
        "Domänenphase",
    )
    assert gefunden.schritt == "Planer: Plan 1"


def testPlanOhneFreigabeWartetAufKritikUndFreigabe(repo):
    repo.datei("handoff/plan.md", planKopf)
    assert schritt(repo) == "Plan 3 wartet auf Kritik und Freigabe"


def testNachFreigabeDesPlansArbeitenDieItemsInDerTechnikphase(repo):
    repo.datei("handoff/plan.md", planKopf + "1. [A](../domaene/items/a.md)\n")
    repo.datei("domaene/items/a.md", "# A\n")
    repo.festhalten("Freigabe Plan 3")
    gefunden = lage(repo.ordner)
    assert gefunden.phase.value == "Technikphase"
    assert gefunden.schritt == "Items von Plan 3: Tests, Umsetzung, Abnahme"


def testOhneOffeneItemsFolgtDerReviewer(repo):
    repo.datei("handoff/plan.md", planKopf)
    repo.festhalten("Freigabe Plan 3")
    assert schritt(repo) == "Reviewer: Review 3"


def testNachFreigabeDesReviewsFolgtDieRetro(repo):
    repo.datei("handoff/plan.md", planKopf)
    repo.datei("handoff/review.md", "# Review · Zyklus 3\n")
    repo.festhalten("Freigabe Plan 3")
    repo.festhalten("Freigabe Review 3")
    gefunden = lage(repo.ordner)
    assert gefunden.phase.value == "Prozessphase"
    assert gefunden.schritt == "Organisationsentwickler: Retro 3"


def testProzessItemOhneCommitIstDerNächsteSchritt(repo):
    repo.datei("handoff/plan.md", planKopf)
    repo.datei("handoff/review.md", "# Review · Zyklus 3\n")
    repo.datei("handoff/retro.md", "# Retro · Zyklus 3\n\n## Prozess-Items\n- P1 Eins\n- P2 Zwei\n")
    repo.festhalten("Freigabe Plan 3")
    repo.festhalten("Freigabe Review 3")
    repo.festhalten("Freigabe Retro 3")
    repo.festhalten("P1: Eins")
    assert schritt(repo) == "Regelumsetzer: Prozess-Item P2 aus Retro 3"


def testSindAlleProzessItemsErledigtBeginntDerNächsteZyklus(repo):
    repo.datei("handoff/plan.md", planKopf)
    repo.datei("handoff/review.md", "# Review · Zyklus 3\n")
    repo.datei("handoff/retro.md", "# Retro · Zyklus 3\n\n## Prozess-Items\nKeine.\n")
    for betreff in ("Freigabe Plan 3", "Freigabe Review 3", "Freigabe Retro 3"):
        repo.festhalten(betreff)
    gefunden = lage(repo.ordner)
    assert (gefunden.zyklus, gefunden.phase.value) == (4, "Domänenphase")
    assert gefunden.schritt == "Anforderungsautor, dann Planer: Plan 4"


def testDerStandNenntEtappeZyklusPhaseUndNächstenSchritt(repo):
    repo.datei("handoff/plan.md", planKopf)
    assert stand(repo.ordner).startswith(
        "Stand: Etappe 1 · Aufstellen · Zyklus 3 · Domänenphase · "
        "Nächster Schritt: Plan 3 wartet auf Kritik und Freigabe"
    )
