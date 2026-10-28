import pytest

from anliegenregeln.anliegenLaenge import grenze, hinweisZu, länge, längeBefund
from anliegenregeln.anliegenTest import anliegenAnlegen, kopfVon
from gemeinsam.hookProtokoll import HookEingabe
from gemeinsam.pfade import wurzel
from lesen.anliegenKopf import anliegenDateien


def anliegenMitLänge(tmp_path, runde, zeichen):
    datei = anliegenAnlegen(
        tmp_path, "12-probe.md", kopfVon("Kritik", "Architekt", "Planer", "offen", runde)
    )
    fehlend = zeichen - länge(datei.read_text(encoding="utf-8"))
    datei.write_text(datei.read_text(encoding="utf-8") + "x" * fehlend, encoding="utf-8")
    return datei


@pytest.mark.stand
@pytest.mark.parametrize(
    "datei", [pytest.param(pfad, id=pfad.name) for pfad in anliegenDateien(wurzel)]
)
def testKeinAnliegenIstLängerAlsSeineGrenze(datei):
    befund = längeBefund(datei)
    assert befund is None or befund[0] != "rot"


@pytest.mark.parametrize("runde", [1, 2, 3])
def testDieGrenzeWächstMitDerRunde(tmp_path, runde):
    datei = anliegenMitLänge(tmp_path, runde, grenze(runde) + 1)
    assert längeBefund(datei)[0] == "rot"


@pytest.mark.parametrize("runde", [1, 2, 3])
def testBeiDerGrenzeIstEsNurEinHinweis(tmp_path, runde):
    datei = anliegenMitLänge(tmp_path, runde, grenze(runde))
    assert längeBefund(datei)[0] == "hinweis"


@pytest.mark.parametrize("runde, zeichen", [(1, 3900), (1, 3901), (2, 7901), (3, 11901)])
def testAb100ZeichenUnterDerGrenzeKommtEinHinweis(tmp_path, runde, zeichen):
    assert längeBefund(anliegenMitLänge(tmp_path, runde, zeichen))[0] == "hinweis"


@pytest.mark.parametrize("runde, zeichen", [(1, 3899), (2, 7899), (3, 11899)])
def testDarunterKommtNichts(tmp_path, runde, zeichen):
    assert längeBefund(anliegenMitLänge(tmp_path, runde, zeichen)) is None


def testEineAntwortZeileZähltAlsAntwortPunkt():
    assert länge("a\nAntwort: Bitte ausführlich\nAntwort:\n") == len("a\nAntwort: .\nAntwort: .\n")


def testDerHookMeldetDenHinweisNachWriteAufEinAnliegen(tmp_path):
    datei = anliegenMitLänge(tmp_path, 1, 3950)
    eingabe = HookEingabe.aus({"tool_input": {"file_path": str(datei)}})
    antwort = hinweisZu(eingabe, tmp_path)
    assert "3950 von 4000" in antwort["hookSpecificOutput"]["additionalContext"]


def testDerHookSchweigtBeiAndererDateiOderKurzemAnliegen(tmp_path):
    kurz = anliegenMitLänge(tmp_path, 1, 500)
    assert hinweisZu(HookEingabe.aus({"tool_input": {"file_path": str(kurz)}}), tmp_path) is None
    fremd = tmp_path / "prozess" / "x.md"
    assert hinweisZu(HookEingabe.aus({"tool_input": {"file_path": str(fremd)}}), tmp_path) is None
