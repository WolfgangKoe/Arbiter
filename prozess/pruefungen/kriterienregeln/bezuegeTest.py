from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe
from kriterienregeln.bezuege import befunde, grundZu, hinweisZu

anforderungenPfad = "domaene/anforderungen/phasen/probe.md"


def eingabeFür(datei: Path) -> HookEingabe:
    return HookEingabe.aus({"tool_input": {"file_path": str(datei)}})


def probeDatei(wurzel: Path, zeilen: str) -> Path:
    datei = wurzel / anforderungenPfad
    datei.parent.mkdir(parents=True)
    datei.write_text(zeilen, encoding="utf-8")
    return datei


def testEineKennungAußerhalbVonKlammernIstRot():
    assert grundZu("**Gegeben** eine *Sperre* nach QUE-1.2, **dann** ist es gesperrt")


def testEineKurzformAußerhalbVonKlammernIstRot():
    assert grundZu("**Gegeben** 18.1, **wenn** der *Spieler* zieht, **dann** passiert es")


def testEinBezugInKlammernNebenEinemSatzIstGrün():
    text = "**Gegeben** die *Sperre* ‚Base überdeckt‘ (QUE-1.2), **dann** ist es gesperrt"
    assert grundZu(text) is None


def testEinGeschachtelterBezugInKlammernIstGrün():
    assert grundZu("**Wenn** der *Spieler* zieht (siehe (QUE-1.2)), **dann** gilt es") is None


def testEinBezugAlleinStattEinesSatzteilsIstRot():
    grund = grundZu("**Gegeben** (18.1), **wenn** der *Spieler* zieht, **dann** gilt es")
    assert grund and "Satzteil" in grund


def testMaßeUndFundstellenInBackticksZählenNicht():
    text = "**Wenn** die Strecke 1/100″ und 2″ beträgt (`domaene/ziel.md`), **dann** gilt `18.1`"
    assert grundZu(text) is None


def testDieDateiMeldetKennungUndZeileDerRotenKriterien(tmp_path):
    datei = probeDatei(
        tmp_path,
        "# Probe\n\n- QUE-1.1 **Wenn** es zieht, **dann** gilt es.\n"
        "- QUE-1.2 **Wenn** es nach QUE-1.1 zieht, **dann** gilt es.\n",
    )
    assert [(befund.kennung, befund.zeile) for befund in befunde(datei)] == [("QUE-1.2", 4)]


def testDerHookMeldetDieRotenKriterienDerGeschriebenenAnforderungsdatei(tmp_path):
    datei = probeDatei(tmp_path, "- QUE-1.2 **Wenn** es nach QUE-1.1 zieht, **dann** gilt es.\n")
    antwort = hinweisZu(eingabeFür(datei), tmp_path)
    assert antwort and "QUE-1.2" in antwort["hookSpecificOutput"]["additionalContext"]


def testDerHookSchweigtBeiGrünenKriterienUndAnderenDateien(tmp_path):
    grün = probeDatei(tmp_path, "- QUE-1.1 **Wenn** es zieht, **dann** gilt es (QUE-1.2).\n")
    assert hinweisZu(eingabeFür(grün), tmp_path) is None
    fremd = tmp_path / "anderes.md"
    fremd.write_text("- QUE-1.2 **Wenn** es nach QUE-1.1 zieht\n", encoding="utf-8")
    assert hinweisZu(eingabeFür(fremd), tmp_path) is None
