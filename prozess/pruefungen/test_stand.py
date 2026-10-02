import pytest

from stand import phase


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
    assert phase(handoff_mit(tmp_path, **zyklen)) == erwartet
