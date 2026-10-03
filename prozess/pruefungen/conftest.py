"""Vor dem Sammeln der Tests löschen: erledigte Anliegen verschwinden mit jedem Prüflauf.

Pytest lädt diese Datei vor dem Sammeln; ein Hook mit dem Namen `pytest_configure` wäre
nicht in camelCase.
"""

from pathlib import Path

from erledigteLoeschen import erledigteLöschen

erledigteLöschen(Path(__file__).resolve().parents[2])
