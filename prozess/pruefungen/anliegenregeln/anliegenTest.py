from pathlib import Path

import pytest

from anliegenregeln.anliegen import kopfVerstöße
from anliegenregeln.anliegenDran import dran, nachprüfungen
from gemeinsam.pfade import wurzel
from lesen.anliegenKopf import Status, anliegenDateien, kopfLesen

guterKopf = "12 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · offen"


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
    kopf = "12 · Anliegen · von Stakeholder → Planer · Runde 2/3 · beantwortet"
    assert kopfVerstöße(anliegenAnlegen(tmp_path, "12-probe.md", kopf), tmp_path) == []


@pytest.mark.parametrize(
    "ersetzung, bis",
    [
        pytest.param("offen", "fertig", id="unbekannter Status"),
        pytest.param("Kritik", "Meinung", id="unbekannter Typ"),
        pytest.param("Runde 1/3", "Runde 4/3", id="Runde über 3"),
        pytest.param("Runde 1/3", "Runde 0/3", id="Runde 0"),
        pytest.param("Architekt (Technik)", "Gärtner", id="unbekannte Rolle"),
        pytest.param("12 ·", "13 ·", id="falsche Nummer"),
        pytest.param(guterKopf, "Von Architekt an Planer · Runde 1/3", id="freier Text"),
    ],
)
def testFalscherKopfIstRot(tmp_path, ersetzung, bis):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace(ersetzung, bis))
    assert kopfVerstöße(datei, tmp_path) != []


def testAnliegenOhneTitelIstRot(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf, titel="Kein Titel")
    assert kopfVerstöße(datei, tmp_path) != []


def testNachprüfungenNenntenDenAbsenderDerAngenommenenAnliegen(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf.replace("offen", "angenommen"))
    anliegenAnlegen(tmp_path, "13-probe.md", guterKopf.replace("12 ", "13 "))
    anliegenAnlegen(
        tmp_path, "14-probe.md", "14 · Kritik · von Fachkritiker → Planer · Runde 1/3 · angenommen"
    )
    assert nachprüfungen(tmp_path) == {"Architekt": [12], "Fachkritiker": [14]}


def stakeholderFragen(tmp_path, status="offen"):
    kopf = f"12 · Fragen · von Planer → Stakeholder · Runde 1/3 · {status}"
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
        datei.read_text(encoding="utf-8").replace("Runde 1/3", "Runde 2/3"), encoding="utf-8"
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
