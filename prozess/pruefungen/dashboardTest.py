import json
from datetime import UTC, datetime

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
    assert eintrag == {"zeit": "2026-10-04T12:30:00+00:00", "rolle": "planer", "belegung": 80_000}


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
    assert "130.000" in seite and "90.000" in seite
    assert "balken warnung" in seite and "balken sperre" in seite
    assert "10-04 12:30 planer" in seite


def testLeeresLogZeigtHinweis():
    assert "Noch kein Lauf" in seiteErzeugen([])


def testRolleWirdMaskiert():
    seite = seiteErzeugen([{"zeit": "2026-10-04T12:30:00", "rolle": "<b>", "belegung": 1}])
    assert "<b>" not in seite.split("<main>")[1]


def testJedeLegendeNenntHöchstensFünfWörter():
    zuLang = [eintrag for eintrag in legende if len(eintrag.split()) > höchstwörter]
    assert not zuLang
