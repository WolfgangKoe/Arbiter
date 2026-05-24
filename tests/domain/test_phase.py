from src.domain.models.phase import PHASES


def test_phases_count() -> None:
    assert len(PHASES) == 7


def test_phases_order() -> None:
    names = [p.name for p in PHASES]
    assert names == [
        "Befehlsphase",
        "Bewegungsphase",
        "Psiphase",
        "Fernkampfphase",
        "Angriffphase",
        "Nahkampfphase",
        "Moralphase",
    ]


def test_phases_index_matches_position() -> None:
    for i, phase in enumerate(PHASES):
        assert phase.index == i
