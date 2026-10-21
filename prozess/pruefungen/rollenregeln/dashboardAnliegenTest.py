from pathlib import Path

import pytest

from rollenregeln.dashboardAnliegen import anliegenAbschnitt, zuständige

agenten = ("planer", "architekt")


@pytest.fixture
def ordner(tmp_path):
    (tmp_path / "handoff" / "anliegen").mkdir(parents=True)
    (tmp_path / ".claude" / "agents").mkdir(parents=True)
    for name in agenten:
        (tmp_path / ".claude" / "agents" / f"{name}.md").write_text("---\n---\n")
    return tmp_path


def anliegenAnlegen(ordner: Path, nummer, form, richtung, status, titel="Titel"):  # noqa: PLR0913
    absender, empfänger = richtung
    kopf = f"{nummer} · {form} · von {absender} → {empfänger} · Runde 2/3 · {status}"
    datei = ordner / "handoff" / "anliegen" / f"{nummer}-titel.md"
    datei.write_text(f"# {titel}\n\n{kopf}\n", encoding="utf-8")


def testSpalteJeZuständigemNachAblaufUndNachprüfungDesAbsenders(ordner):
    anliegenAnlegen(ordner, 10, "Kritik", ("architekt", "planer"), "offen")
    anliegenAnlegen(ordner, 11, "Fragen", ("architekt", "planer"), "angenommen")
    anliegenAnlegen(ordner, 12, "Kritik", ("planer", "architekt"), "erledigt")
    assert zuständige(ordner) == {"planer": [10], "architekt": [11]}


def testKarteNenntNummerAlsLinkTitelFormUndRunde(ordner):
    anliegenAnlegen(ordner, 10, "Kritik", ("architekt", "planer"), "offen", "Zu <viel>")
    abschnitt = anliegenAbschnitt(ordner)
    assert '<a href="handoff/anliegen/10-titel.md">10</a>' in abschnitt
    assert "Zu &lt;viel&gt;" in abschnitt and "Kritik · Runde 2" in abschnitt
    assert "planer (1)" in abschnitt


def testKarteNenntAbsenderUndEmpfängerUndMarkiertAnliegenAnDenStakeholder(ordner):
    anliegenAnlegen(ordner, 10, "Fragen", ("planer", "Stakeholder"), "offen")
    anliegenAnlegen(ordner, 11, "Kritik", ("architekt", "planer"), "offen")
    abschnitt = anliegenAbschnitt(ordner)
    assert "planer → Stakeholder (an dich)" in abschnitt
    assert "architekt → planer</p>" in abschnitt
    assert abschnitt.count("an-stakeholder") == 1


def testFilterNachRolleUndFormBieteteNurVorhandeneWerteAn(ordner):
    anliegenAnlegen(ordner, 10, "Kritik", ("architekt", "planer"), "offen")
    anliegenAnlegen(ordner, 11, "Fragen", ("planer", "architekt"), "offen")
    abschnitt = anliegenAbschnitt(ordner)
    assert 'id="filterRolle"' in abschnitt and 'id="filterForm"' in abschnitt
    assert 'data-rolle="planer" data-form="Kritik"' in abschnitt
    assert '<option value="Fragen">' in abschnitt and '<option value="Auftrag">' not in abschnitt


def wartendesAnlegen(ordner: Path, nummer, wartetAuf, status="offen"):
    kopf = f"Form: Kritik\nVon: architekt\nAn: planer\nRunde: 1/3\nStatus: {status}"
    kopf += f"\nWartet auf: {wartetAuf}"
    datei = ordner / "handoff" / "anliegen" / f"{nummer}-titel.md"
    datei.write_text(f"# Titel {nummer}\n\n{kopf}\n", encoding="utf-8")


def testWartendeStehenInEigenenBereichenOhneKommentarfeld(ordner):
    anliegenAnlegen(ordner, 10, "Kritik", ("architekt", "planer"), "offen")
    wartendesAnlegen(ordner, 11, "10")
    abschnitt = anliegenAbschnitt(ordner)
    assert "Jetzt dran" in abschnitt
    assert "Wartet auf ein anderes Anliegen (1)" in abschnitt
    assert "Titel 11" in abschnitt and "wartet auf 10" in abschnitt
    assert 'name="kommentar"' not in abschnitt and "<textarea" not in abschnitt


@pytest.mark.usefixtures("gitRepo")
def testVorgemerktesStehtJeFolgendePhaseInDerReihenfolgeDerRotation(ordner):
    wartendesAnlegen(ordner, 11, "Prozessphase")
    wartendesAnlegen(ordner, 12, "Technikphase")
    wartendesAnlegen(ordner, 13, "Domänenphase")
    abschnitt = anliegenAbschnitt(ordner)
    reihenfolge = [abschnitt.index(f"Titel {nummer}") for nummer in (12, 11)]
    assert reihenfolge == sorted(reihenfolge)
    assert "Vorgemerkt für die Technikphase (1)" in abschnitt
    assert "Vorgemerkt für die Prozessphase (1)" in abschnitt
    assert "Titel 13" in abschnitt


def testErledigtesAnliegenStehtNichtImBoard(ordner):
    wartendesAnlegen(ordner, 11, "10", status="erledigt")
    assert "Kein Anliegen offen" in anliegenAbschnitt(ordner)


def testOhneOffenesAnliegenSteheHinweis(ordner):
    assert "Kein Anliegen offen" in anliegenAbschnitt(ordner)
