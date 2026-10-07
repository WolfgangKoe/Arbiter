import pytest

from anliegenregeln.anliegennummer import entscheide
from anliegenregeln.anliegenNummern import doppelteNummern, nächsteFreieNummer
from anliegenregeln.anliegenTest import anliegenAnlegen, guterKopf
from gemeinsam.pfade import wurzel


def schreibung(datei):
    return {"tool_name": "Write", "tool_input": {"file_path": str(datei), "content": "x"}}


def testNeueDateiMitVergebenerNummerIstGesperrtUndNenntDieNächsteFreie(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    anliegenAnlegen(tmp_path, "13-andere.md", guterKopf)
    neu = tmp_path / "handoff" / "anliegen" / "12-zweite.md"
    antwort = entscheide(schreibung(neu), tmp_path)
    assert antwort["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "nächste freie ist 14" in antwort["hookSpecificOutput"]["permissionDecisionReason"]


def testFreieNummerIstErlaubt(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert entscheide(schreibung(tmp_path / "handoff" / "anliegen" / "13-neu.md"), tmp_path) is None


def testBestehendeDateiDarfNeuGeschriebenWerden(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert entscheide(schreibung(datei), tmp_path) is None


def testGelöschteNummerWirdNichtNeuVergeben(tmp_path, gitRepo):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    gitRepo.festhalten()
    datei.unlink()
    assert nächsteFreieNummer(tmp_path) > int(datei.name[:2])
    assert entscheide(schreibung(datei), tmp_path) is not None


def testZweiDateienMitDerselbenNummerSindRot(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    anliegenAnlegen(tmp_path, "12-zweite.md", guterKopf)
    assert doppelteNummern(tmp_path) == {12: ["12-probe.md", "12-zweite.md"]}


@pytest.mark.stand
def testKeinePaarMitDerselbenNummerImRepo():
    assert doppelteNummern(wurzel) == {}


def testEinAndererWerkzeugaufrufAlsWriteIstFrei(tmp_path):
    eingabe = {**schreibung(tmp_path / "handoff" / "anliegen" / "12-x.md"), "tool_name": "Read"}
    assert entscheide(eingabe, tmp_path) is None


def testEineDateiAußerhalbDerAnliegenOderOhneMdIstFrei(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert entscheide(schreibung(tmp_path / "prozess" / "12-x.md"), tmp_path) is None
    assert entscheide(schreibung(tmp_path / "handoff" / "anliegen" / "12-x.txt"), tmp_path) is None
