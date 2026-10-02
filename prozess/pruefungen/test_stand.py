import subprocess

import pytest

from stand import etappe, phase


def freigeben(wurzel, *nummern):
    subprocess.run(["git", "init", "-q"], cwd=wurzel, check=True)
    for nummer in nummern:
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q",
             "--allow-empty", "-m", f"Freigabe Plan {nummer}"],
            cwd=wurzel, check=True,
        )


def handoff_mit(tmp_path, **zyklen):
    for name, nummer in zyklen.items():
        (tmp_path / f"{name}.md").write_text(f"# {name.title()} · Zyklus {nummer}\n")
    return tmp_path


@pytest.mark.parametrize(
    "zyklen, erwartet",
    [
        pytest.param({}, "Noch kein Zyklus begonnen → Domänenphase, Plan 1", id="leer"),
        pytest.param({"plan": 3}, "Zyklus 3: Review 3 fehlt → Technikphase", id="nach Plan"),
        pytest.param(
            {"plan": 3, "review": 3, "retro": 2},
            "Zyklus 3: Retro 3 fehlt → Prozessphase",
            id="nach Review",
        ),
        pytest.param(
            {"plan": 3, "review": 3, "retro": 3},
            "Zyklus 3 abgeschlossen → Domänenphase, Plan 4",
            id="nach Retro",
        ),
    ],
)
def test_phase_folgt_aus_den_zyklusnummern(tmp_path, zyklen, erwartet):
    if zyklen:
        freigeben(tmp_path, zyklen["plan"])
    else:
        subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    assert phase(handoff_mit(tmp_path, **zyklen), tmp_path) == erwartet


def test_ohne_freigabe_bleibt_es_die_domaenenphase(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    assert (
        phase(handoff_mit(tmp_path, plan=1), tmp_path)
        == "Zyklus 1: Plan 1 wartet auf Kritik und Freigabe → Domänenphase"
    )


def test_freigabe_von_plan_12_zaehlt_nicht_fuer_plan_1(tmp_path):
    freigeben(tmp_path, 12)
    assert phase(handoff_mit(tmp_path, plan=1), tmp_path).endswith("→ Domänenphase")


def test_etappe_ist_die_erste_etappen_ueberschrift(tmp_path):
    (tmp_path / "domaene").mkdir()
    (tmp_path / "domaene" / "etappen.md").write_text(
        "# Etappen\n\n## Etappe 2 · Nahkampf\nText\n\n## Etappe 3 · Fernkampf\n"
    )
    assert etappe(tmp_path) == "Etappe 2 · Nahkampf"


def test_ohne_etappe_leitet_die_domaene_sie_aus_dem_ziel_ab(tmp_path):
    assert etappe(tmp_path) == "Keine Etappe → aus dem Ziel ableiten"
