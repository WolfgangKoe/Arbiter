import json
from datetime import UTC, datetime

import pytest

import dashboard
from dashboard import (
    dashboardSchreiben,
    kilo,
    legende,
    modellName,
    seiteErzeugen,
    sitzungsTitel,
)
from laufLog import (
    dauerSekunden,
    dauerSumme,
    eintragAnhängen,
    jetzt,
    laufEintrag,
    logPfad,
    läufeLesen,
    protokollieren,
    transkriptEinträge,
    zielLänge,
)

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
    eintrag = laufEintrag(stopp(transkript(tmp_path, 80_000)), zeitpunkt, tmp_path)
    assert eintrag == {
        "zeit": "2026-10-04T12:30:00+00:00",
        "rolle": "planer",
        "agent_id": "a1",
        "sitzung": None,
        "belegung": 80_000,
        "ziel": "Erstellung des Dashboards",
        "modell": "claude-opus-5-5",
        "koordinator": None,
        "dauer": None,
        "zyklus": 1,
        "phase": "Domänenphase",
        "stopp_wiederholt": False,
    }


def testKoordinatorStandKommtAusDemHauptTranskript(tmp_path):
    hauptstand = 61_000
    haupt = tmp_path / "haupt.jsonl"
    haupt.write_text(
        json.dumps({"message": {"usage": {"cache_read_input_tokens": hauptstand}}}),
        encoding="utf-8",
    )
    eingabe = stopp(transkript(tmp_path, 80_000)) | {"transcript_path": str(haupt)}
    assert laufEintrag(eingabe, zeitpunkt, tmp_path)["koordinator"] == hauptstand


@pytest.mark.parametrize(
    "eingabe", [{}, {"agent_type": "planer"}, {"agent_type": "planer", "agent_id": "a1"}]
)
def testLaufOhneRolleOderBelegungBleibtUnprotokolliert(eingabe, tmp_path):
    assert laufEintrag(eingabe, zeitpunkt, tmp_path) is None


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


def testWiederholterStoppDesselbenLaufsZähltEinmal(tmp_path):
    for belegung, wiederholt in ((10, False), (20, True)):
        eintragAnhängen(
            tmp_path,
            {"zeit": "a", "rolle": "planer", "agent_id": "a1", "belegung": belegung}
            | {"stopp_wiederholt": wiederholt},
        )
    eintragAnhängen(tmp_path, {"zeit": "b", "rolle": "planer", "agent_id": None, "belegung": 5})
    eintragAnhängen(tmp_path, {"zeit": "c", "rolle": "planer", "agent_id": None, "belegung": 6})
    assert [lauf["belegung"] for lauf in läufeLesen(tmp_path)] == [20, 5, 6]


def testGeblocktesStoppWirdVerworfenFortgesetzterLaufBleibt(tmp_path):
    folge = [("a1", "erst", False), ("a1", "zweiter Auftrag", False), ("a1", "Rückmeldung", True)]
    for laufId, ziel, wiederholt in folge:
        eintragAnhängen(
            tmp_path,
            {"zeit": "a", "rolle": "r", "agent_id": laufId, "belegung": 1, "ziel": ziel}
            | {"stopp_wiederholt": wiederholt},
        )
    assert [lauf["ziel"] for lauf in läufeLesen(tmp_path)] == ["erst", "zweiter Auftrag"]


def testJüngsterAuftragImTranskriptGiltUndKürztAmWort(tmp_path):
    datei = tmp_path / "agent-a1.jsonl"
    langer = "Ziel: " + "wort " * 30
    zeilen = [
        {"message": {"role": "user", "content": "Ziel: erster"}},
        {"message": {"role": "assistant", "usage": {"cache_read_input_tokens": 1}}},
        {"message": {"role": "user", "content": langer}},
    ]
    datei.write_text("\n".join(json.dumps(zeile) for zeile in zeilen), encoding="utf-8")
    ziel = laufEintrag(stopp(datei), zeitpunkt, tmp_path)["ziel"]
    assert ziel.endswith("wort…") and len(ziel) <= zielLänge + 1


def testHinweiseUndVorspannSindKeinAuftrag(tmp_path):
    datei = tmp_path / "agent-a1.jsonl"
    vorspann = "The coordinator sent a message while you were working:"
    hinweis = "<system-reminder>\nviel Text\n</system-reminder>"
    zeilen = [
        {"message": {"role": "user", "content": f"{hinweis}\nZiel: erster"}},
        {"isMeta": True, "message": {"role": "user", "content": hinweis}},
        {
            "isMeta": True,
            "message": {
                "role": "user",
                "content": f"{vorspann}\nNeuer Auftrag: zweiter",
            },
        },
        {"isMeta": True, "message": {"role": "user", "content": hinweis}},
        {"message": {"role": "assistant", "usage": {"cache_read_input_tokens": 1}}},
    ]
    datei.write_text("\n".join(json.dumps(zeile) for zeile in zeilen), encoding="utf-8")
    assert laufEintrag(stopp(datei), zeitpunkt, tmp_path)["ziel"] == "Neuer Auftrag: zweiter"


def testKetteWiederholterStoppsGibtDenAuftragDesErstenWeiter(tmp_path):
    folge = [("erst", False), ("Rück1", True), ("Rück2", True)]
    for ziel, wiederholt in folge:
        eintragAnhängen(
            tmp_path,
            {"zeit": "a", "rolle": "r", "agent_id": "a1", "belegung": 1, "ziel": ziel}
            | {"stopp_wiederholt": wiederholt},
        )
    assert [lauf["ziel"] for lauf in läufeLesen(tmp_path)] == ["erst"]


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
    assert "<h3>Altbestand, ohne Sitzung</h3>" in seite
    assert '<td>–</td><td>–</td><td class="stand">–</td>' in seite


def testTitelNenntZyklusUndPhase(tmp_path):
    eintragAnhängen(
        tmp_path,
        {"zeit": "a", "rolle": "r", "belegung": 1, "sitzung": "f8ebd61f-0000"}
        | {"zyklus": 3, "phase": "Prozessphase"},
    )
    seite = dashboardSchreiben(tmp_path).read_text(encoding="utf-8")
    assert "<h3>Zyklus 3 Prozessphase · Sitzung f8ebd61f</h3>" in seite
    assert "<th>Ende</th>" not in seite and "<th>Dauer</th>" in seite


def testDauerReichtVomJüngstenAuftragBisZurLetztenZeile(tmp_path):
    datei = tmp_path / "agent-a1.jsonl"
    zeilen = [
        {"timestamp": "2026-10-04T12:00:00Z", "message": {"role": "user", "content": "Ziel: eins"}},
        {"timestamp": "2026-10-04T12:10:00Z", "message": {"role": "user", "content": "Ziel: zwei"}},
        {"timestamp": "2026-10-04T12:12:30Z", "message": {"role": "assistant"}},
    ]
    datei.write_text("\n".join(json.dumps(zeile) for zeile in zeilen), encoding="utf-8")
    assert dauerSekunden(transkriptEinträge(datei)) == 150  # noqa: PLR2004
    assert "3 min" in seiteErzeugen([{"zeit": "a", "rolle": "r", "belegung": 1, "dauer": 180}])
    assert "45 s" in seiteErzeugen([{"zeit": "a", "rolle": "r", "belegung": 1, "dauer": 45}])


def testZyklusUndPhaseKommenAusDerLage(tmp_path, monkeypatch):
    import laufLog

    monkeypatch.setattr(laufLog, "zyklusUndPhase", lambda _ordner: (3, "Prozessphase"))
    eintrag = laufEintrag(stopp(transkript(tmp_path, 80_000)), zeitpunkt, tmp_path)
    assert (eintrag["zyklus"], eintrag["phase"]) == (3, "Prozessphase")


def testZyklusUndPhaseLiestPhasenfolge(monkeypatch):
    import laufLog
    import phasenfolge

    monkeypatch.setattr(
        phasenfolge, "lage", lambda _ordner: phasenfolge.Lage(3, phasenfolge.Phase.prozessphase, "")
    )
    assert laufLog.zyklusUndPhase(None) == (3, "Prozessphase")


def testDauerOhneZeitstempelIstLeer(tmp_path):
    assert dauerSekunden(transkriptEinträge(transkript(tmp_path, 1))) is None


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
    assert "<th>Dauer</th>" in seite and "<th>Kontextfenster</th>" in seite
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


def testTitelNenntAllePhasenDerSitzung(tmp_path):
    for zyklus, phase in ((3, "Domänenphase"), (3, "Technikphase"), (4, "Domänenphase")):
        eintragAnhängen(
            tmp_path,
            {"zeit": "a", "rolle": "r", "belegung": 1, "sitzung": "f8ebd61f-0"}
            | {"zyklus": zyklus, "phase": phase},
        )
    seite = dashboardSchreiben(tmp_path).read_text(encoding="utf-8")
    assert "Zyklus 3 Domänenphase bis Zyklus 4 Domänenphase · Sitzung f8ebd61f" in seite
    läufe = [{"zyklus": 3, "phase": "Domänenphase"}, {"zyklus": 3, "phase": "Technikphase"}]
    assert "Zyklus 3 Domänenphase bis Technikphase" in sitzungsTitel("f8ebd61f", läufe)


def testLaufOhneSitzungMitZyklusHeißtAltbestand():
    läufe = [{"zyklus": 3, "phase": "Prozessphase"}]
    assert sitzungsTitel("ohne Sitzung", läufe) == "Altbestand, ohne Sitzung"


def testDauerBeimZusammenführenSummiertBeideTeile(tmp_path):
    folge = [(600, False), (60, True)]
    for dauer, wiederholt in folge:
        eintragAnhängen(
            tmp_path,
            {"zeit": "a", "rolle": "r", "agent_id": "a1", "belegung": 1, "dauer": dauer}
            | {"stopp_wiederholt": wiederholt},
        )
    assert [lauf["dauer"] for lauf in läufeLesen(tmp_path)] == [660]
    assert dauerSumme({"dauer": None}, {"dauer": 5}) is None


def testFehlerInDerLageKostetDenEintragNicht(tmp_path, monkeypatch):
    import phasenfolge

    def wirft(_ordner):
        raise RuntimeError

    monkeypatch.setattr(phasenfolge, "lage", wirft)
    eintrag = laufEintrag(stopp(transkript(tmp_path, 80_000)), zeitpunkt, tmp_path)
    assert eintrag["belegung"] and eintrag["zyklus"] is None


def testHookWegTrägtZyklusEin(tmp_path):
    protokollieren(stopp(transkript(tmp_path, 80_000)), tmp_path)
    assert läufeLesen(tmp_path)[0]["zyklus"] == 1
    assert (tmp_path / "dashboard.html").is_file()


def testStillSchreibtDieSeiteOhneAusgabe(capsys, monkeypatch):
    geschrieben = []
    monkeypatch.setattr(dashboard, "dashboardSchreiben", lambda ordner: geschrieben.append(ordner))
    assert dashboard.hauptlauf(["--still"]) == 0
    assert capsys.readouterr().out == "" and geschrieben
    assert dashboard.hauptlauf([]) == 0
    assert capsys.readouterr().out.strip() == "None"


def testFehlerBeimSchreibenIstMitStillStill(monkeypatch):
    def wirft(_ordner):
        raise OSError

    monkeypatch.setattr(dashboard, "dashboardSchreiben", wirft)
    assert dashboard.hauptlauf(["--still"]) == 0
    with pytest.raises(OSError):
        dashboard.hauptlauf([])
