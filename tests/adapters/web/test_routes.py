import pytest
from flask import Flask
from flask.testing import FlaskClient

from src.adapters.web import create_app


@pytest.fixture()
def app() -> Flask:
    return create_app()


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


# ── Phase navigation ──────────────────────────────────────────────────────────


def test_first_phase_has_no_prev(client: FlaskClient) -> None:
    response = client.get("/?phase=0&round=1")
    html = response.data.decode()
    assert response.status_code == 200
    assert 'class="nav-btn disabled">←' in html


def test_first_phase_has_next(client: FlaskClient) -> None:
    response = client.get("/?phase=0&round=1")
    html = response.data.decode()
    assert 'href="/?phase=1&amp;round=1' in html


def test_last_phase_has_no_next_on_last_round(client: FlaskClient) -> None:
    response = client.get("/?phase=6&round=5&max_rounds=5")
    html = response.data.decode()
    assert 'class="nav-btn disabled">→' not in html  # next leads to game over, not disabled
    assert "round=6" in html


def test_last_phase_transitions_to_next_round(client: FlaskClient) -> None:
    response = client.get("/?phase=6&round=2&max_rounds=5")
    html = response.data.decode()
    assert 'href="/?phase=0&amp;round=3' in html


def test_first_phase_not_round_one_has_prev_to_last_phase(client: FlaskClient) -> None:
    response = client.get("/?phase=0&round=3&max_rounds=5")
    html = response.data.decode()
    assert 'href="/?phase=6&amp;round=2' in html


def test_invalid_phase_clamps_to_last(client: FlaskClient) -> None:
    response = client.get("/?phase=99")
    html = response.data.decode()
    assert response.status_code == 200
    assert "Moralphase" in html


def test_invalid_phase_string_clamps_to_zero(client: FlaskClient) -> None:
    response = client.get("/?phase=abc")
    html = response.data.decode()
    assert "Befehlsphase" in html


def test_round_counter_shown_in_header(client: FlaskClient) -> None:
    response = client.get("/?phase=0&round=3&max_rounds=5")
    html = response.data.decode()
    assert "Runde 3" in html


# ── Game over ─────────────────────────────────────────────────────────────────


def test_game_over_screen_after_max_rounds(client: FlaskClient) -> None:
    response = client.get("/?round=6&phase=0&max_rounds=5")
    html = response.data.decode()
    assert "Spiel beendet" in html


def test_game_over_restart_link(client: FlaskClient) -> None:
    response = client.get("/?round=6&phase=0&max_rounds=5")
    html = response.data.decode()
    assert "phase=0&amp;round=1&amp;max_rounds=5" in html


def test_custom_max_rounds_respected(client: FlaskClient) -> None:
    response = client.get("/?round=4&phase=0&max_rounds=3")
    html = response.data.decode()
    assert "Spiel beendet" in html


def test_custom_max_rounds_not_over_early(client: FlaskClient) -> None:
    response = client.get("/?round=3&phase=0&max_rounds=3")
    html = response.data.decode()
    assert "Spiel beendet" not in html


# ── End game button ───────────────────────────────────────────────────────────


def test_end_game_button_present_during_play(client: FlaskClient) -> None:
    response = client.get("/?phase=3&round=2&max_rounds=5")
    html = response.data.decode()
    assert "Spiel beenden" in html


def test_end_game_button_links_to_game_over_with_from_round_and_phase(
    client: FlaskClient,
) -> None:
    response = client.get("/?phase=3&round=2&max_rounds=5")
    html = response.data.decode()
    assert "from_round=2" in html
    assert "from_phase=3" in html


def test_game_over_back_link_goes_to_exact_phase_and_round(client: FlaskClient) -> None:
    response = client.get("/?round=6&phase=0&from_round=3&from_phase=3&max_rounds=5")
    html = response.data.decode()
    assert "phase=3&amp;round=3" in html


def test_game_over_back_link_shows_phase_name(client: FlaskClient) -> None:
    response = client.get("/?round=6&phase=0&from_round=3&from_phase=3&max_rounds=5")
    html = response.data.decode()
    assert "Fernkampfphase" in html


def test_game_over_back_link_defaults_to_last_phase_of_max_rounds(client: FlaskClient) -> None:
    response = client.get("/?round=6&phase=0&max_rounds=5")
    html = response.data.decode()
    assert "phase=6&amp;round=5" in html


def test_natural_end_passes_from_round_and_phase(client: FlaskClient) -> None:
    response = client.get("/?phase=6&round=5&max_rounds=5")
    html = response.data.decode()
    assert "from_round=5" in html
    assert "from_phase=6" in html
