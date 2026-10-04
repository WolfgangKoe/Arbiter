import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from dashboard import dashboardSchreiben, legende, seiteErzeugen
from laufLog import eintragAnhängen, laufEintrag, logPfad, läufeLesen

höchstwörter = 5
zeitpunkt = datetime(2026, 10, 4, 12, 30, tzinfo=UTC)


def transkript(ordner, belegung):
    datei = ordner / "agent-a1.jsonl"
    zeile = {"message": {"usage": {"cache_read_input_tokens": belegung}}}
    datei.write_text(json.dumps(zeile) + "\n", encoding="utf-8")
    return datei


def stopp(datei, rolle="planer"):
    return {"agent_type": rolle, "agent_id": "a1", "agent_transcript_path": str(datei)}


def testLaufMitRolleUndBelegungWirdEingetragen(tmp_path):
    eintrag = laufEintrag(stopp(transkript(tmp_path, 80_000)), zeitpunkt)
    assert eintrag == {
        "zeit": "2026-10-04T12:30:00+00:00",
        "rolle": "planer",
        "agent_id": "a1",
        "sitzung": None,
        "belegung": 80_000,
    }


@pytest.mark.parametrize(
    "eingabe", [{}, {"agent_type": "planer"}, {"agent_type": "planer", "agent_id": "a1"}]
)
def testLaufOhneRolleOderBelegungBleibtUnprotokolliert(eingabe):
    assert laufEintrag(eingabe, zeitpunkt) is None


def testLogWächstUndLässtSichLesen(tmp_path):
    assert läufeLesen(tmp_path) == []
    eintragAnhängen(tmp_path, {"zeit": "a", "rolle": "planer", "belegung": 1})
    eintragAnhängen(tmp_path, {"zeit": "b", "rolle": "architekt", "belegung": 2})
    logPfad(tmp_path).write_text(
        logPfad(tmp_path).read_text(encoding="utf-8") + "\n", encoding="utf-8"
    )
    assert [lauf["rolle"] for lauf in läufeLesen(tmp_path)] == ["planer", "architekt"]


def testDashboardNenntRolleBelegungUndStufen(tmp_path):
    for rolle, belegung in (("planer", 50_000), ("planer", 130_000), ("architekt", 155_000)):
        eintragAnhängen(
            tmp_path, {"zeit": "2026-10-04T12:30:00", "rolle": rolle, "belegung": belegung}
        )
    seite = dashboardSchreiben(tmp_path).read_text(encoding="utf-8")
    assert "planer (2)" in seite and "architekt (1)" in seite
    assert "130.000" in seite and "90.000" in seite and "--bg:#0f0e0c" in seite
    assert "saeule warnung" in seite and "Sperrschwelle 150k" in seite and "Median" in seite
    assert "10-04 12:30" in seite


def testLeeresLogZeigtHinweis():
    assert "Noch kein Lauf" in seiteErzeugen([])


def testRolleWirdMaskiert():
    seite = seiteErzeugen([{"zeit": "2026-10-04T12:30:00", "rolle": "<b>", "belegung": 1}])
    assert "<b>" not in seite.split("bericht-zeile")[1]


def testJedeLegendeNenntHöchstensFünfWörter():
    zuLang = [
        eintrag for eintrag in [text for _, text in legende] if len(eintrag.split()) > höchstwörter
    ]
    assert not zuLang


def testZweiterEintragDesselbenLaufsZähltEinmal(tmp_path):
    for belegung in (10, 20):
        eintragAnhängen(
            tmp_path, {"zeit": "a", "rolle": "planer", "agent_id": "a1", "belegung": belegung}
        )
    eintragAnhängen(tmp_path, {"zeit": "b", "rolle": "planer", "agent_id": None, "belegung": 5})
    eintragAnhängen(tmp_path, {"zeit": "c", "rolle": "planer", "agent_id": None, "belegung": 6})
    assert [lauf["belegung"] for lauf in läufeLesen(tmp_path)] == [20, 5, 6]


def testKaputteZeileWirdÜbersprungen(tmp_path):
    eintragAnhängen(tmp_path, {"zeit": "a", "rolle": "planer", "belegung": 1})
    with logPfad(tmp_path).open("a", encoding="utf-8") as ziel:
        ziel.write('{"zeit": "b", "rol\n[1]\n')
    eintragAnhängen(tmp_path, {"zeit": "c", "rolle": "architekt", "belegung": 2})
    assert [lauf["rolle"] for lauf in läufeLesen(tmp_path)] == ["planer", "architekt"]
    assert dashboardSchreiben(tmp_path).is_file()


def testHookTrägtOrtszoneEin():
    quelle = (Path(__file__).parent / "laufLog.py").read_text(encoding="utf-8")
    assert "astimezone()" in quelle and "UTC" not in quelle


def testJedeSitzungBekommtEineKarteMitTabelle(tmp_path):
    sitzungen = ("aaaaaaaa-1", "bbbbbbbb-2")
    for sitzung in sitzungen:
        eintragAnhängen(
            tmp_path,
            {"zeit": "2026-10-04T12:30:00", "rolle": "planer", "sitzung": sitzung, "belegung": 5},
        )
    seite = dashboardSchreiben(tmp_path).read_text(encoding="utf-8")
    assert seite.count('class="sitzungs-karte"') == len(sitzungen)
    assert "Sitzung aaaaaaaa" in seite and "Sitzung bbbbbbbb" in seite
    assert "<th>Agent</th>" in seite and "<svg" in seite
