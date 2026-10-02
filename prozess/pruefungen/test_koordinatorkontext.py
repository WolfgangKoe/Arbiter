import lesegrenze
import schlussantwort


def handback(text, rolle="planer"):
    return {"agent_type": rolle, "tool_name": "SubagentHandback", "tool_input": {"message": text}}


def test_lange_schlussantwort_wird_zurueckgeschickt():
    antwort = schlussantwort.entscheide(handback("x" * 4714))
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_kurze_schlussantwort_mit_pfaden_geht_durch():
    assert schlussantwort.entscheide(handback("Fertig: handoff/anliegen/09-x.md")) is None


def test_ohne_rolle_prueft_der_hook_die_schlussantwort_nicht():
    assert schlussantwort.entscheide(handback("x" * 5000, rolle=None)) is None


def stop(text, aktiv=False):
    return {
        "hook_event_name": "SubagentStop",
        "agent_type": "regelumsetzer",
        "last_assistant_message": text,
        "stop_hook_active": aktiv,
    }


def test_lange_letzte_nachricht_schickt_die_rolle_zurueck():
    assert schlussantwort.entscheide(stop("x" * 2246))["decision"] == "block"


def test_beim_zweiten_stopp_wird_nicht_erneut_gesperrt():
    assert schlussantwort.entscheide(stop("x" * 2246, aktiv=True)) is None


def lesen(pfad, rolle="koordinator"):
    return {"agent_type": rolle, "tool_name": "Read", "tool_input": {"file_path": str(pfad)}}


def test_koordinator_liest_keine_langen_dateien(tmp_path):
    (tmp_path / "VORGEHEN.md").write_text("ä" * 25000, encoding="utf-8")
    antwort = lesegrenze.entscheide(lesen(tmp_path / "VORGEHEN.md"), tmp_path)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_koordinator_liest_kurze_dateien(tmp_path):
    (tmp_path / "kurz.md").write_text("Stand", encoding="utf-8")
    assert lesegrenze.entscheide(lesen(tmp_path / "kurz.md"), tmp_path) is None


def test_rollen_lesen_auch_lange_dateien(tmp_path):
    (tmp_path / "lang.md").write_text("x" * 25000, encoding="utf-8")
    assert lesegrenze.entscheide(lesen(tmp_path / "lang.md", rolle="planer"), tmp_path) is None
