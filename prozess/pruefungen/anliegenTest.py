from pathlib import Path

import pytest

from anliegen import anliegenDateien, kopfLesen, kopfVerstöße, nachprüfungen, nachprüfungenAlsText

wurzel = Path(__file__).resolve().parents[2]
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


@pytest.mark.parametrize(
    "datei", [pytest.param(pfad, id=pfad.name) for pfad in anliegenDateien(wurzel)]
)
def testJedesAnliegenHatEinenGültigenKopf(datei):
    assert kopfVerstöße(datei, wurzel) == []


def testKopfWirdGelesen(tmp_path):
    datei = anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    gelesen = kopfLesen(datei)
    assert (gelesen.nummer, gelesen.typ, gelesen.absender, gelesen.empfänger) == (
        12, "Kritik", "Architekt", "Planer",
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
    assert nachprüfungenAlsText(tmp_path) == "Nachprüfung fällig: Architekt (12), Fachkritiker (14)"


def testOhneAngenommeneAnliegenIstDerTextLeer(tmp_path):
    anliegenAnlegen(tmp_path, "12-probe.md", guterKopf)
    assert nachprüfungenAlsText(tmp_path) == ""
