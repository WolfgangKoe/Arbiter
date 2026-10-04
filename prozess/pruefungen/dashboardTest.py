import json
from datetime import UTC, datetime

import pytest

from dashboard import dashboardSchreiben, kilo, legende, modellName, seiteErzeugen, zeitText
from laufLog import eintragAnhängen, jetzt, laufEintrag, logPfad, läufeLesen

höchstwörter = 5
zeitpunkt = datetime(2026, 10, 4, 12, 30, tzinfo=UTC)


def transkript(ordner, belegung):
    datei = ordner / "agent-a1.jsonl"
    auftrag = {
        "message": {"role": "user", "content": "Ziel: Erstellung des Dashboards\nEingang: x"}
    }
    antwort = {
        "message": {
            "role": "assistant",
            "model": "claude-opus-5-5",
            "usage": {"cache_read_input_tokens": belegung},
        }
    }
    zeilen = [json.dumps(auftrag), "kaputt", json.dumps(antwort)]
    datei.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
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
        "ziel": "Erstellung des Dashboards",
        "modell": "claude-opus-5-5",
        "koordinator": None,
    }


def testKoordinatorStandKommtAusDemHauptTranskript(tmp_path):
    hauptstand = 61_000
    haupt = tmp_path / "haupt.jsonl"
    haupt.write_text(
        json.dumps({"message": {"usage": {"cache_read_input_tokens": hauptstand}}}),
        encoding="utf-8",
    )
    eingabe = stopp(transkript(tmp_path, 80_000)) | {"transcript_path": str(haupt)}
    assert laufEintrag(eingabe, zeitpunkt)["koordinator"] == hauptstand


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
    assert "130k" in seite and "90k" in seite and "38.000" not in seite and "--bg:#0f0e0c" in seite
    assert "saeule warnung" in seite and "Sperrschwelle 150k" in seite and "Median" in seite
    assert zeitText("2026-10-04T12:30:00") in seite


def testLeeresLogZeigtHinweis():
    assert "Noch kein Lauf" in seiteErzeugen([])


def testRolleWirdMaskiert():
    seite = seiteErzeugen([{"zeit": "2026-10-04T12:30:00", "rolle": "<b>", "belegung": 1}])
    assert "<b>" not in seite.split("bericht-zeile")[1]


def testJedeLegendeNenntHöchstensFünfWörter():
    zuLang = [
        eintrag
        for eintrag in [text for _, text, _ in legende]
        if len(eintrag.split()) > höchstwörter
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


def testJetztHatDieOrtszone():
    assert jetzt().tzinfo == datetime.now().astimezone().tzinfo


def testEintragOhnePflichtfeldWirdÜbersprungen(tmp_path):
    eintragAnhängen(tmp_path, {"rolle": "planer", "belegung": 1})
    eintragAnhängen(tmp_path, {"zeit": "a", "rolle": "planer"})
    eintragAnhängen(tmp_path, {"zeit": "a", "rolle": "planer", "belegung": 1})
    assert len(läufeLesen(tmp_path)) == 1
    assert dashboardSchreiben(tmp_path).is_file()


def testAltbestandOhneSitzungHatLesbarenTitel(tmp_path):
    eintragAnhängen(tmp_path, {"zeit": "2026-10-04T12:17:11+00:00", "rolle": "a", "belegung": 1})
    seite = dashboardSchreiben(tmp_path).read_text(encoding="utf-8")
    assert "<h3>ohne Sitzung</h3>" in seite
    assert zeitText("2026-10-04T12:17:11+00:00") in seite
    assert zeitText("unlesbar") == "unlesbar"


def testTabelleNenntModellAuftragUndRundetAufKilo(tmp_path):
    eintragAnhängen(
        tmp_path,
        {
            "zeit": "2026-10-04T12:30:00+00:00",
            "rolle": "planer",
            "belegung": 38_247,
            "ziel": "Erstellung des Dashboards",
            "modell": "claude-sonnet-5-5",
            "koordinator": 61_000,
        },
    )
    seite = dashboardSchreiben(tmp_path).read_text(encoding="utf-8")
    assert "Sonnet" in seite and "Erstellung des Dashboards" in seite and "38k" in seite
    assert "<th>Ende</th>" in seite and "<th>Kontextfenster</th>" in seite
    assert "saeule orchestrator" in seite and "61k" in seite
    assert "50k</text>" in seite


def testKiloUndModellName():
    assert kilo(38_247) == "38k" and kilo(150_000) == "150k"
    assert modellName("claude-opus-5-5") == "Opus" and modellName("") == ""


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
