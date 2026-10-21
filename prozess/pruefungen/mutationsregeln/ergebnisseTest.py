import json

from mutationsregeln.ergebnisse import (
    Gleichwertig,
    gemerkt,
    gleichwertigeLesen,
    merken,
    standKennung,
)


def projekt(tmp_path):
    (tmp_path / "technik").mkdir()
    (tmp_path / "technik" / "modul.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("a = 1\n", encoding="utf-8")
    (tmp_path / "domaene" / "daten").mkdir(parents=True)
    (tmp_path / "domaene" / "daten" / "karte.yaml").write_text("a: 1\n", encoding="utf-8")
    return tmp_path


def testDerStandÄndertSichMitTechnikPyprojectUndDaten(tmp_path):
    wurzel = projekt(tmp_path)
    anfang = standKennung(wurzel)
    assert standKennung(wurzel) == anfang
    for datei in ("technik/modul.py", "pyproject.toml", "domaene/daten/karte.yaml"):
        (wurzel / datei).write_text("neu\n", encoding="utf-8")
        assert standKennung(wurzel) != anfang
        (wurzel / datei).write_text("x = 1\n", encoding="utf-8")
        anfang = standKennung(wurzel)


def testEineAndereDateiÄndertDenStandNicht(tmp_path):
    wurzel = projekt(tmp_path)
    anfang = standKennung(wurzel)
    (wurzel / "handoff").mkdir()
    (wurzel / "handoff" / "retro.md").write_text("x\n", encoding="utf-8")
    assert standKennung(wurzel) == anfang


def testGemerktesGiltNurZumGleichenStand(tmp_path):
    ablage = tmp_path / "ordner" / "merkzettel.json"
    merken(ablage, "stand1", {"a.py#0": True})
    assert gemerkt(ablage, "stand1") == {"a.py#0": True}
    assert gemerkt(ablage, "stand2") == {}


def testOhneAblageOderMitDefekterAblageIstNichtsGemerkt(tmp_path):
    assert gemerkt(None, "x") == {}
    assert gemerkt(tmp_path / "fehlt.json", "x") == {}
    kaputt = tmp_path / "kaputt.json"
    kaputt.write_text("{", encoding="utf-8")
    assert gemerkt(kaputt, "x") == {}
    merken(None, "x", {"a": True})


def testNurGleichwertigeMitBegründungZählen(tmp_path):
    datei = tmp_path / "gleichwertig.json"
    eintrag = {"datei": "a.py", "quelle": "x = 1", "fehler": "1 wird 2"}
    datei.write_text(
        json.dumps([{**eintrag, "grund": "Wert wird nie gelesen"}, {**eintrag, "grund": " "}]),
        encoding="utf-8",
    )
    assert gleichwertigeLesen(datei) == {Gleichwertig("a.py", "x = 1", "1 wird 2")}
    assert gleichwertigeLesen(tmp_path / "fehlt.json") == set()
