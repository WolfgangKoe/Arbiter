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


def anliegenInRunde(tmp_path, runde, status):
    kopf = guterKopf.replace("Runde 1/3 · offen", f"Runde {runde}/3 · {status}")
    return anliegenAnlegen(tmp_path, "12-probe.md", kopf)


def ändere(datei, rolle, alt, neu):
    return schreibung(datei, rolle, old_string=alt, new_string=neu)


def sperre(antwort):
    return antwort["hookSpecificOutput"]["permissionDecisionReason"]


def testRolleDarfDieRundeNichtSenken(tmp_path):
    datei = anliegenInRunde(tmp_path, 3, "offen")
    antwort = entscheide(ändere(datei, "planer", "Runde 3/3", "Runde 1/3"), tmp_path)
    assert "Runde 3/3 ist die letzte" in sperre(antwort)


def testRolleDarfDieRundeErhöhen(tmp_path):
    datei = anliegenInRunde(tmp_path, 1, "abgelehnt")
    angaben = ändere(datei, "architekt", "Runde 1/3 · abgelehnt", "Runde 2/3 · offen")
    assert entscheide(angaben, tmp_path) is None


def testRolleDarfEskaliertNichtZurücknehmen(tmp_path):
    datei = anliegenInRunde(tmp_path, 3, "eskaliert")
    antwort = entscheide(ändere(datei, "architekt", "· eskaliert", "· offen"), tmp_path)
    assert "Der Stakeholder entscheidet" in sperre(antwort)


def testStakeholderDarfEskaliertZurücksetzen(tmp_path):
    datei = anliegenInRunde(tmp_path, 3, "eskaliert")
    eingabe = ändere(datei, "architekt", "Runde 3/3 · eskaliert", "Runde 1/3 · offen")
    del eingabe["agent_type"]
    assert entscheide(eingabe, tmp_path) is None


def testInRunde3AufOffenNachAbgelehntIstGesperrt(tmp_path):
    datei = anliegenInRunde(tmp_path, 3, "abgelehnt")
    antwort = entscheide(ändere(datei, "architekt", "· abgelehnt", "· offen"), tmp_path)
    assert "Runde 3/3 ist die letzte" in sperre(antwort)


def testInRunde3VonAbgelehntAufEskaliertIstErlaubt(tmp_path):
    datei = anliegenInRunde(tmp_path, 3, "abgelehnt")
    assert entscheide(ändere(datei, "architekt", "· abgelehnt", "· eskaliert"), tmp_path) is None
