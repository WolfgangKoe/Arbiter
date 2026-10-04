"""Vor dem Sammeln der Tests löschen: erledigte Anliegen verschwinden mit jedem Prüflauf."""

from pathlib import Path

from anliegenregeln.erledigteLoeschen import erledigteLöschen


def pytest_configure():
    erledigteLöschen(Path(__file__).resolve().parents[2])
