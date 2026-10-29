import os
import re
import subprocess
from pathlib import Path

import pytest

from anliegenregeln.anliegen import kopfVerstöße
from anliegenregeln.anliegenDran import dran, nachprüfungen, wartende
from anliegenregeln.freieNummer import hauptprogramm
from gemeinsam.pfade import wurzel
from lesen.anliegenKopf import Status, Ziel, anliegenDateien, freieNummer, kopfLesen, kopfÄndern

guterKopf = "Form: Kritik\nVon: Architekt\nAn: Planer\nRunde: 1/3\nStatus: offen"


def wartetAuf(ziel):
    return f"{guterKopf}\nWartet auf: {ziel}"


def kopfVon(form, absender, empfänger, status, runde=1):
    return f"Form: {form}\nVon: {absender}\nAn: {empfänger}\nRunde: {runde}/3\nStatus: {status}"


def anliegenAnlegen(tmp_path: Path, name: str, kopf: str, titel: str = "# Titel") -> Path:
    rollen = tmp_path / ".claude" / "agents"
    rollen.mkdir(parents=True, exist_ok=True)
    for rolle in ("architekt", "planer", "fachkritiker"):
        (rollen / f"{rolle}.md").write_text("---\nname: x\n---\n", encoding="utf-8")
    datei = tmp_path / "handoff" / "anliegen" / name
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(f"{titel}\n\n{kopf}\n\n## Runde 1\n", encoding="utf-8")
    return datei


@pytest.mark.stand
@pytest.mark.parametrize(
    "datei", [pytest.param(pfad, id=pfad.name) for pfad in anliegenDateien(wurzel)]
)
def testJedesAnliegenHatEinenGültigenKopf(datei):
    assert kopfVerstöße(datei, wurzel) == []


def testKopfWirdGelesen(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    gelesen = kopfLesen(datei)
    assert (gelesen.nummer, gelesen.typ, gelesen.absender, gelesen.empfänger) == (
        12,
        "Kritik",
        "Architekt",
        "Planer",
    )
    assert (gelesen.runde, gelesen.status) == (1, "offen")


def testStakeholderAlsRolleIstErlaubt(tmp_path):
    kopf = kopfVon("Anliegen", "Stakeholder", "Planer", "beantwortet", runde=2)
    assert kopfVerstöße(anliegenAnlegen(tmp_path, "12-probe.md", kopf), tmp_path) == []


@pytest.mark.parametrize(
    "ersetzung, bis",
    [
        pytest.param("offen", "fertig", id="unbekannter Status"),
        pytest.param("Kritik", "Meinung", id="unbekannte Form"),
        pytest.param("1/3", "4/3", id="Runde über 3"),
        pytest.param("1/3", "0/3", id="Runde 0"),
        pytest.param("Architekt", "Gärtner", id="unbekannte Rolle"),
        pytest.param("Planer", "planer", id="Rolle klein geschrieben"),
        pytest.param(guterKopf, "Von Architekt an Planer · Runde 1/3", id="freier Text"),
        pytest.param("Runde: 1/3\n", "", id="Feld fehlt"),
    ],
)
def testFalscherKopfIstRot(tmp_path, ersetzung, bis):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace(ersetzung, bis))
    assert kopfVerstöße(datei, tmp_path) != []


def testRückfrageIstEinGültigerStatus(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "rückfrage"))
    assert kopfVerstöße(datei, tmp_path) == []


def testBeiRückfrageIstDerAbsenderDran(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "rückfrage"))
    assert dran(tmp_path) == {"Architekt": [12]}


def testAnliegenOhneTitelIstRot(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf, titel="Kein Titel")
    assert kopfVerstöße(datei, tmp_path) != []


def testNachprüfungenNenntenDenAbsenderDerAngenommenenAnliegen(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "angenommen"))
    anliegenAnlegen(tmp_path, "13-probe.md", guterKopf)
    fremder = kopfVon("Kritik", "Fachkritiker", "Planer", "angenommen")
    anliegenAnlegen(tmp_path, "14-probe.md", fremder)
    assert nachprüfungen(tmp_path) == {"Architekt": [12], "Fachkritiker": [14]}


def stakeholderFragen(tmp_path, status="offen"):
    kopf = kopfVon("Fragen", "Planer", "Stakeholder", status)
    return anliegenAnlegen(tmp_path, "12-probe.md", kopf)


def dranBei(tmp_path):
    return {rolle: nummern for rolle, nummern in dran(tmp_path).items() if nummern == [12]}


def testFragenVorDerFreigabeSindBeimAbsenderDran(tmp_path, gitRepo):
    stakeholderFragen(tmp_path)
    gitRepo.festhalten("Fragen")
    gitRepo.festhalten("Freigabe Plan 2")
    assert dranBei(tmp_path) == {"Planer": [12]}


def testFragenImFreigabeCommitSindBeimAbsenderDran(tmp_path, gitRepo):
    stakeholderFragen(tmp_path)
    gitRepo.festhalten("Freigabe Retro 3")
    assert dranBei(tmp_path) == {"Planer": [12]}


def testFragenImFreigabeCommitDesReviewsSindBeimAbsenderDran(tmp_path, gitRepo):
    stakeholderFragen(tmp_path)
    gitRepo.festhalten("Freigabe Review 3")
    assert dranBei(tmp_path) == {"Planer": [12]}


def testNeueRundeNachDerFreigabeIstBeimStakeholderDran(tmp_path, gitRepo):
    datei = stakeholderFragen(tmp_path)
    gitRepo.festhalten("Freigabe Plan 2")
    datei.write_text(
        datei.read_text(encoding="utf-8").replace("Runde: 1/3", "Runde: 2/3"), encoding="utf-8"
    )
    assert dranBei(tmp_path) == {"Stakeholder": [12]}
    gitRepo.festhalten("Nachgefragt")
    assert dranBei(tmp_path) == {"Stakeholder": [12]}


def testNotizNachDerFreigabeÄndertNichtsAmDran(tmp_path, gitRepo):
    datei = stakeholderFragen(tmp_path)
    gitRepo.festhalten("Freigabe Plan 2")
    datei.write_text(datei.read_text(encoding="utf-8") + "Notiz\n", encoding="utf-8")
    assert dranBei(tmp_path) == {"Planer": [12]}
    gitRepo.festhalten("Notiz")
    assert dranBei(tmp_path) == {"Planer": [12]}


def testNeueFragenNachDerFreigabeSindBeimStakeholderDran(tmp_path, gitRepo):
    gitRepo.festhalten("Freigabe Plan 2")
    stakeholderFragen(tmp_path)
    assert dranBei(tmp_path) == {"Stakeholder": [12]}


def testEskaliertVorDerFreigabeBleibtBeimStakeholder(tmp_path, gitRepo):
    stakeholderFragen(tmp_path, status="eskaliert")
    gitRepo.festhalten("Freigabe Plan 2")
    assert dranBei(tmp_path) == {"Stakeholder": [12]}


def testOhneFreigabeInGitBleibtDerStakeholderDran(tmp_path, gitRepo):
    stakeholderFragen(tmp_path)
    gitRepo.festhalten("Fragen")
    assert dranBei(tmp_path) == {"Stakeholder": [12]}


def testStatusIstEinWertDerAufzählungUnbekannterBleibtText(tmp_path):
    bekannt = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert kopfLesen(bekannt).status is Status.offen
    unbekannt = anliegenAnlegen(tmp_path, "13-probe.md", guterKopf.replace("offen", "fertig"))
    assert kopfLesen(unbekannt).status == "fertig"
    assert not isinstance(kopfLesen(unbekannt).status, Status)


@pytest.mark.parametrize(
    "zusatz",
    [
        pytest.param("13", id="wartet auf Nummer"),
        pytest.param("Prozessphase", id="wartet auf die Prozessphase"),
        pytest.param("Technikphase", id="wartet auf die Technikphase"),
        pytest.param("Domänenphase", id="wartet auf die Domänenphase"),
    ],
)
def testWartetAufImKopfIstGrün(tmp_path, zusatz):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", wartetAuf(zusatz))
    assert kopfVerstöße(datei, tmp_path) == []
    assert str(kopfLesen(datei).wartetAuf) == zusatz


def testWartetAufEinenUnbekanntenTextIstRot(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", wartetAuf("x"))
    assert kopfVerstöße(datei, tmp_path) != []


def testDieFormAuftragIstErlaubt(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("Kritik", "Auftrag"))
    assert kopfVerstöße(datei, tmp_path) == []


def testEinAnliegenAufEinVorhandenesWartetBisEsGelöschtIst(tmp_path):
    wartend = anliegenAnlegen(tmp_path, "12-probe.md", wartetAuf("13"))
    ziel = anliegenAnlegen(tmp_path, "13-probe.md", guterKopf)
    assert dran(tmp_path) == {"Planer": [13]}
    assert wartende(tmp_path) == {12: Ziel(nummer=13)}
    ziel.unlink()
    assert dran(tmp_path) == {"Planer": [12]}
    assert wartend.is_file()
    assert wartende(tmp_path) == {}


def testEinAnliegenAufDieTechnikphaseIstInDerDomänenphaseNichtDran(gitRepo):
    anliegenAnlegen(gitRepo.ordner, "12-probe.md", wartetAuf("Technikphase"))
    assert dran(gitRepo.ordner) == {}
    assert wartende(gitRepo.ordner) == {12: Ziel(phase="Technikphase")}
    (gitRepo.ordner / "handoff" / "plan.md").write_text("# Plan · Zyklus 3\n", encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 3")
    assert dran(gitRepo.ordner) == {"Planer": [12]}


def testEinAnliegenAufDieDomänenphaseIstInDerTechnikphaseNichtDran(gitRepo):
    anliegenAnlegen(gitRepo.ordner, "12-probe.md", wartetAuf("Domänenphase"))
    assert dran(gitRepo.ordner) == {"Planer": [12]}
    (gitRepo.ordner / "handoff" / "plan.md").write_text("# Plan · Zyklus 3\n", encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 3")
    assert dran(gitRepo.ordner) == {}


def testEinAnliegenAufDieProzessphaseIstDortDranSonstNicht(gitRepo):
    anliegenAnlegen(gitRepo.ordner, "12-probe.md", wartetAuf("Prozessphase"))
    assert dran(gitRepo.ordner) == {}
    assert wartende(gitRepo.ordner) == {12: Ziel(phase="Prozessphase")}
    plan = "# Plan · Zyklus 3\n"
    (gitRepo.ordner / "handoff" / "plan.md").write_text(plan, encoding="utf-8")
    (gitRepo.ordner / "handoff" / "review.md").write_text("# Review · Zyklus 3\n", encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 3")
    gitRepo.festhalten("Freigabe Review 3")
    assert dran(gitRepo.ordner) == {"Planer": [12]}
    assert wartende(gitRepo.ordner) == {}


def testEinAnliegenAufDiePhaseEinesSpäterenZyklusWartetBisDahin(gitRepo):
    datei = anliegenAnlegen(gitRepo.ordner, "12-probe.md", wartetAuf("Technikphase 4"))
    assert kopfVerstöße(datei, gitRepo.ordner) == []
    assert kopfLesen(datei).wartetAuf == Ziel(phase="Technikphase", zyklus=4)
    plan = gitRepo.ordner / "handoff" / "plan.md"
    plan.write_text("# Plan · Zyklus 3\n", encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 3")
    assert dran(gitRepo.ordner) == {}
    assert wartende(gitRepo.ordner) == {12: Ziel(phase="Technikphase", zyklus=4)}
    plan.write_text("# Plan · Zyklus 4\n", encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 4")
    assert dran(gitRepo.ordner) == {"Planer": [12]}


def testEineWartendeNachprüfungIstErstInDerProzessphaseFällig(gitRepo):
    kopf = wartetAuf("Prozessphase").replace("offen", "angenommen")
    anliegenAnlegen(gitRepo.ordner, "12-probe.md", kopf)
    assert nachprüfungen(gitRepo.ordner) == {}
    plan = "# Plan · Zyklus 3\n"
    (gitRepo.ordner / "handoff" / "plan.md").write_text(plan, encoding="utf-8")
    (gitRepo.ordner / "handoff" / "review.md").write_text("# Review · Zyklus 3\n", encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 3")
    gitRepo.festhalten("Freigabe Review 3")
    assert nachprüfungen(gitRepo.ordner) == {"Architekt": [12]}


def testEinErledigtesAnliegenWartetNicht(tmp_path):
    kopf = wartetAuf("13").replace("offen", "erledigt")
    anliegenAnlegen(tmp_path, "12-probe.md", kopf)
    assert wartende(tmp_path) == {}


def testKopfÄndernSchreibtDieFelderUndLässtDenRestStehen(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    neu = kopfÄndern(datei.read_text(encoding="utf-8"), {"Status": "angenommen"})
    assert neu == datei.read_text(encoding="utf-8").replace("Status: offen", "Status: angenommen")


@pytest.mark.parametrize(
    ("ziel", "text"),
    [
        (Ziel(nummer=7), "07"),
        (Ziel(nummer=6760), "6760"),
        (Ziel(phase="Prozessphase", zyklus=9), "die Prozessphase 9"),
    ],
)
def testZielBeschreibtNummerOderDiePhase(ziel, text):
    assert ziel.beschreibung == text


@pytest.mark.parametrize(
    ("text", "erwartet"),
    [
        ("13", Ziel(nummer=13)),
        ("Technikphase", Ziel(phase="Technikphase")),
        ("Prozessphase 9", Ziel(phase="Prozessphase", zyklus=9)),
    ],
)
def testWartetAufLegtDasZielGetrenntAb(tmp_path, text, erwartet):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", wartetAuf(text))
    assert kopfLesen(datei).wartetAuf == erwartet


def testKopfÄndernOhneKopfGibtNichtsZurück():
    assert kopfÄndern("# Titel\n\nText\n", {"Status": "offen"}) is None


def testFreieNummerNimmtDieErsteNochNieVergebeneImBereich(gitRepo):
    anliegenAnlegen(gitRepo.ordner, "1980-erste.md", guterKopf)
    anliegenAnlegen(gitRepo.ordner, "1981-zweite.md", guterKopf)
    gitRepo.festhalten("Anliegen")
    (gitRepo.ordner / "handoff" / "anliegen" / "1981-zweite.md").unlink()
    gitRepo.festhalten("Anliegen gelöscht")
    zweiteFreie = 1982
    assert freieNummer(gitRepo.ordner, range(1980, 1990)) == zweiteFreie


def testFreieNummerMeldetEinenVollenBereich(tmp_path):
    anliegenAnlegen(tmp_path, "1980-erste.md", guterKopf)
    assert freieNummer(tmp_path, range(1980, 1981)) is None


def testFreieNummerAlsBefehlNenntDieNummerOderScheitert(tmp_path, monkeypatch, capsys):
    anliegenAnlegen(tmp_path, "1980-erste.md", guterKopf)
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    assert hauptprogramm(["1980", "1981"]) == 0
    assert capsys.readouterr().out == "1981\n"
    assert hauptprogramm(["1980", "1980"]) == 1
    assert hauptprogramm(["x"]) == 1


def testDieHilfemeldungNenntDenBefehlAusDenRegeln(capsys):
    regeln = (wurzel / "prozess" / "regeln" / "anliegenregeln.md").read_text(encoding="utf-8")
    assert hauptprogramm([]) == 1
    aufruf = capsys.readouterr().err.removeprefix("Aufruf: ").strip()
    assert f"`{aufruf}`" in regeln


def testDerInRegelnGenannteBefehlFürFreieNummernLäuftAlsKindprozess():
    regeln = (wurzel / "prozess" / "regeln" / "anliegenregeln.md").read_text(encoding="utf-8")
    zeile = next(zeile for zeile in regeln.splitlines() if "anliegenregeln.freieNummer" in zeile)
    befehl = re.search(r"`(python3 [^`]*anliegenregeln\.freieNummer <erste> <letzte>)`", zeile)
    assert befehl, "Regeln nennen keinen Befehl mit <erste> <letzte>"
    lauf = subprocess.run(
        befehl.group(1).replace("<erste>", "9000").replace("<letzte>", "9001").split(),
        cwd=wurzel,
        env={name: wert for name, wert in os.environ.items() if name != "PYTHONPATH"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert lauf.returncode == 0, lauf.stderr
    assert lauf.stdout.strip() == "9000"
