from anliegenregeln.freigabeSperre import entscheide


def schreibung(datei, rolle, werkzeug="Edit", **angaben):
    return {
        "hook_event_name": "PreToolUse",
        "agent_type": rolle,
        "tool_name": werkzeug,
        "tool_input": {"file_path": str(datei), **angaben},
    }


def ändere(datei, rolle, alt, neu):
    return schreibung(datei, rolle, old_string=alt, new_string=neu)


def sperre(antwort):
    return antwort["hookSpecificOutput"]["permissionDecisionReason"]


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
