from anliegenTest import anliegenAnlegen, guterKopf
from statusrecht import entscheide


def schreibung(datei, rolle, werkzeug="Edit", **angaben):
    return {
        "hook_event_name": "PreToolUse",
        "agent_type": rolle,
        "tool_name": werkzeug,
        "tool_input": {"file_path": str(datei), **angaben},
    }


def zuErledigt(datei, rolle):
    return schreibung(datei, rolle, old_string="· offen", new_string="· erledigt")


def testFremdeRolleDarfNichtAufErledigtSetzen(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    antwort = entscheide(zuErledigt(datei, "planer"), tmp_path)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testAbsenderDarfAufErledigtSetzen(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert entscheide(zuErledigt(datei, "architekt"), tmp_path) is None


def testFremdeRolleDarfMitWriteNichtAufErledigtSetzen(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    inhalt = datei.read_text(encoding="utf-8").replace("· offen", "· erledigt")
    antwort = entscheide(schreibung(datei, "planer", "Write", content=inhalt), tmp_path)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testAndereStatuswerteSindFrei(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    angaben = schreibung(datei, "planer", old_string="· offen", new_string="· angenommen")
    assert entscheide(angaben, tmp_path) is None


def testStakeholderOhneRolleIstNichtBeschränkt(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    eingabe = zuErledigt(datei, "planer")
    del eingabe["agent_type"]
    assert entscheide(eingabe, tmp_path) is None


def testAndereDateienBleibenUnberührt(tmp_path):
    datei = tmp_path / "notiz.md"
    datei.write_text("a", encoding="utf-8")
    eingabe = schreibung(datei, "planer", old_string="a", new_string="erledigt")
    assert entscheide(eingabe, tmp_path) is None
