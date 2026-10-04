from anliegenregeln.anliegenTest import anliegenAnlegen, guterKopf
from anliegenregeln.statusrecht import entscheide


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


def testEineAndereDateiAlsEinAnliegenIstFrei(tmp_path):
    datei = tmp_path / "notiz.md"
    datei.write_text("x", encoding="utf-8")
    assert entscheide(schreibung(datei, "planer", "Write", content="y"), tmp_path) is None


def testEinEditOhneNeuenTextIstFrei(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert entscheide(schreibung(datei, "planer", old_string="· offen"), tmp_path) is None


def testEinAnderesWerkzeugAlsWriteOderEditIstFrei(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert entscheide(schreibung(datei, "planer", "Read"), tmp_path) is None


def testEinNeuesAnliegenOhneKopfIstFrei(tmp_path):
    datei = tmp_path / "handoff" / "anliegen" / "12-neu.md"
    datei.parent.mkdir(parents=True)
    assert entscheide(schreibung(datei, "planer", "Write", content="kein Kopf"), tmp_path) is None


def testEinNeuesErledigtesAnliegenOhneVorgängerIstDemAbsenderVorbehalten(tmp_path):
    datei = tmp_path / "handoff" / "anliegen" / "12-neu.md"
    datei.parent.mkdir(parents=True)
    kopf = guterKopf.replace("· offen", "· erledigt")
    inhalt = f"# Titel\n\n{kopf}\n"
    for rolle in ("architekt", "planer", "fachkritiker"):
        (tmp_path / ".claude" / "agents").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".claude" / "agents" / f"{rolle}.md").write_text("x", encoding="utf-8")
    antwort = entscheide(schreibung(datei, "planer", "Write", content=inhalt), tmp_path)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"


def testEinSchonErledigtesAnliegenDarfJederWeiterschreiben(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("· offen", "· erledigt"))
    angaben = schreibung(datei, "planer", old_string="## Runde 1", new_string="## Runde 1\nx")
    assert entscheide(angaben, tmp_path) is None


def testWriteEinesAnderenAbsendersAufEinBestehendesAnliegenIstGesperrt(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    inhalt = datei.read_text(encoding="utf-8").replace("von Architekt", "von Reviewer")
    antwort = entscheide(schreibung(datei, "reviewer", "Write", content=inhalt), tmp_path)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "nächste freie Nummer 13" in antwort["hookSpecificOutput"]["permissionDecisionReason"]


def testWriteMitGleichemAbsenderNeueRundeIstFrei(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    inhalt = datei.read_text(encoding="utf-8").replace("Runde 1/3", "Runde 2/3")
    assert entscheide(schreibung(datei, "architekt", "Write", content=inhalt), tmp_path) is None


vorlage = (
    "# Plan · Zyklus 3\n\nText\nKommentar: warum so?\nStellungnahme: erledigt\n\n"
    "## Freigabe\nFreigabe: offen\nKommentar: .\n"
)


def planAnlegen(tmp_path, inhalt=vorlage):
    datei = tmp_path / "handoff" / "plan.md"
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(inhalt, encoding="utf-8")
    return datei


def testRolleDarfFreigabeNichtAufJaSetzen(tmp_path):
    datei = planAnlegen(tmp_path)
    antwort = entscheide(ändere(datei, "planer", "Freigabe: offen", "Freigabe: ja"), tmp_path)
    assert "Freigabe: ja" in sperre(antwort)


def testRolleDarfEinenKommentarNichtEntfernen(tmp_path):
    datei = planAnlegen(tmp_path)
    antwort = entscheide(ändere(datei, "planer", "Kommentar: warum so?\n", ""), tmp_path)
    assert "Kommentar: warum so?" in sperre(antwort)


def testRolleDarfEinenKommentarNichtUmschreiben(tmp_path):
    datei = planAnlegen(tmp_path)
    angaben = ändere(datei, "planer", "Kommentar: warum so?", "Kommentar: .")
    assert "Kommentar: warum so?" in sperre(entscheide(angaben, tmp_path))


def testRolleDarfFreigabeOffenNichtLöschen(tmp_path):
    datei = planAnlegen(tmp_path)
    antwort = entscheide(ändere(datei, "planer", "Freigabe: offen\n", ""), tmp_path)
    assert "Freigabe: offen" in sperre(antwort)


def testEineStellungnahmeIstFrei(tmp_path):
    datei = planAnlegen(tmp_path)
    angaben = ändere(datei, "planer", "Text\n", "Text\nStellungnahme: geändert in Item 2\n")
    assert entscheide(angaben, tmp_path) is None


def testDerPunktKommentarIstFrei(tmp_path):
    datei = planAnlegen(tmp_path)
    assert entscheide(ändere(datei, "planer", "Kommentar: .", "Kommentar: ."), tmp_path) is None


def testDerNächsteZyklusDarfKommentareAblösen(tmp_path):
    datei = planAnlegen(tmp_path)
    inhalt = vorlage.replace("Zyklus 3", "Zyklus 4").replace("Kommentar: warum so?\n", "")
    angaben = schreibung(datei, "planer", "Write", content=inhalt)
    assert entscheide(angaben, tmp_path) is None


def testDerNächsteZyklusBeginntNichtMitJa(tmp_path):
    datei = planAnlegen(tmp_path)
    inhalt = vorlage.replace("Zyklus 3", "Zyklus 4").replace("offen", "ja")
    antwort = entscheide(schreibung(datei, "planer", "Write", content=inhalt), tmp_path)
    assert "beginnt mit" in sperre(antwort)


def testDerStakeholderÄndertFreigabeUndKommentareFrei(tmp_path):
    datei = planAnlegen(tmp_path)
    eingabe = ändere(datei, "planer", "Freigabe: offen", "Freigabe: ja")
    del eingabe["agent_type"]
    assert entscheide(eingabe, tmp_path) is None


def testEinEditOhneNeuenTextAmPlanIstFrei(tmp_path):
    datei = planAnlegen(tmp_path)
    assert entscheide(schreibung(datei, "planer", old_string="Text"), tmp_path) is None


def testZyklusnummerEntfernenLöstNichtAb(tmp_path):
    datei = planAnlegen(tmp_path)
    angaben = ändere(
        datei, "planer", "Zyklus 3\n\nText\nKommentar: warum so?\n", "Zyklus\n\nText\n"
    )
    assert "Kommentar: warum so?" in sperre(entscheide(angaben, tmp_path))


def testZyklusnummerSenkenLöstNichtAb(tmp_path):
    datei = planAnlegen(tmp_path)
    angaben = ändere(
        datei, "planer", "Zyklus 3\n\nText\nKommentar: warum so?\n", "Zyklus 2\n\nText\n"
    )
    assert "Kommentar: warum so?" in sperre(entscheide(angaben, tmp_path))


def testNeuerKommentarEinerRolleIstGesperrt(tmp_path):
    datei = planAnlegen(tmp_path)
    angaben = ändere(datei, "planer", "Text\n", "Text\nKommentar: Rolle schreibt\n")
    assert "Kommentar: Rolle schreibt" in sperre(entscheide(angaben, tmp_path))


def testFreigabeJaWiederEntfernenIstGesperrt(tmp_path):
    datei = planAnlegen(tmp_path, vorlage.replace("offen", "ja"))
    angaben = ändere(datei, "planer", "Freigabe: ja", "Freigabe: offen")
    assert "Freigabe: ja" in sperre(entscheide(angaben, tmp_path))


def testDateiOhneUtf8IstFreiUndBrichtNichtAb(tmp_path):
    datei = tmp_path / "handoff" / "plan.md"
    datei.parent.mkdir(parents=True)
    datei.write_bytes(b"\xff\xfe\x00")
    assert entscheide(schreibung(datei, "planer", old_string="a", new_string="b"), tmp_path) is None


def testEineFremdeDateiWirdNichtGelesen(tmp_path):
    datei = tmp_path / "technik" / "bild.bin"
    datei.parent.mkdir(parents=True)
    datei.write_bytes(b"\xff\xfe\x00")
    assert entscheide(schreibung(datei, "planer", old_string="a", new_string="b"), tmp_path) is None
