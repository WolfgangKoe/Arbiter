from lesen.plan import offeneItems


def planSchreiben(wurzel, text):
    (wurzel / "handoff").mkdir()
    (wurzel / "handoff" / "plan.md").write_text(text, encoding="utf-8")


def testOhnePlanGibtEsKeineOffenenItems(tmp_path):
    assert offeneItems(tmp_path) == []


def testEinOffenesItemIstDasMitDateiInItems(tmp_path):
    planSchreiben(tmp_path, "## Items\n[a](../domaene/items/a.md) [b](../domaene/items/b.md)\n")
    (tmp_path / "domaene" / "items").mkdir(parents=True)
    (tmp_path / "domaene" / "items" / "a.md").write_text("x", encoding="utf-8")
    assert offeneItems(tmp_path) == ["a.md"]
