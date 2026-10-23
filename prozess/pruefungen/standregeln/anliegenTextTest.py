from anliegenregeln.anliegenTest import anliegenAnlegen, guterKopf
from standregeln.anliegenText import nachprüfungenAlsText


def testNachprüfungenAlsTextNenntRolleUndNummern(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "angenommen"))
    anliegenAnlegen(
        tmp_path,
        "14-probe.md",
        guterKopf.replace("Architekt", "Fachkritiker").replace("offen", "angenommen"),
    )
    assert nachprüfungenAlsText(tmp_path) == "Nachprüfung fällig: Architekt (12), Fachkritiker (14)"


def testOhneAngenommeneAnliegenIstDerTextLeer(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert nachprüfungenAlsText(tmp_path) == ""
