from standregeln.frei import auftrag, freieZeilen
from standregeln.stand import stand

technik = """## Fortschritt
- [x] Architekt: Vertrag zu Item a, bei beiden Hälften
- [ ] Testautor: Tests zu Item a
- [x] Architekt: Vertrag zu Item b, bei beiden Hälften
- [x] Testautor: Tests zu Item b
- [ ] Fachkritiker: Kritik an den Tests zu Item b
- [ ] Architekt: Kritik an den Tests zu Item b
- [ ] Implementierer: Tests zu Item b grün
- [ ] Reviewer: DoD über das Inkrement
- [ ] Stakeholder: Freigabe Review 1
"""


def testJedesItemIstFürSichFreiUndParalleleKritikerSindBeideFrei():
    assert freieZeilen(technik) == {
        "Testautor": ["Tests zu Item a"],
        "Fachkritiker": ["Kritik an den Tests zu Item b"],
        "Architekt": ["Kritik an den Tests zu Item b"],
    }


def testEinOffenesHindernisHältDieZeileAuf():
    text = technik.replace(
        "- [ ] Testautor: Tests zu Item a\n",
        "- [ ] Testautor: Tests zu Item a\n  - [ ] Hindernis 12 Frage\n",
    )
    assert "Testautor" not in freieZeilen(text)


def testEinBeseitigtesHindernisHältNichtAuf():
    text = technik.replace(
        "- [ ] Testautor: Tests zu Item a\n",
        "- [ ] Testautor: Tests zu Item a\n  - [x] Hindernis 12 Frage\n",
    )
    assert freieZeilen(text)["Testautor"] == ["Tests zu Item a"]


def testDieDoDWartetAufAlleItemsUndDerStakeholderIstNieFrei():
    frei = freieZeilen(technik)
    assert "Reviewer" not in frei
    assert "Stakeholder" not in frei


def testProzessItemsSindNachDerFreigabeAlleGleichzeitigFrei():
    retro = (
        "## Fortschritt\n- [x] Stakeholder: Freigabe Retro 1\n"
        "- [ ] Regelumsetzer: P2\n- [ ] Organisationsentwickler: P3\n"
        "- [ ] Koordinator: nach dev gepusht\n"
    )
    assert freieZeilen(retro) == {"Regelumsetzer": ["P2"], "Organisationsentwickler": ["P3"]}


def testStandNenntWasFreiIstMitDemAuftrag(gitRepo):
    plan = "# Plan · Zyklus 1\n\n## Items\n1. [A](../domaene/items/a.md)\n\n" + technik
    (gitRepo.ordner / "handoff").mkdir()
    (gitRepo.ordner / "handoff/plan.md").write_text(plan, encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 1")
    text = stand(gitRepo.ordner)
    assert "Frei: " in text
    assert auftrag in text
