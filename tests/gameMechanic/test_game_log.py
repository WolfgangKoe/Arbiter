"""Tests for game_log.py — log writing, reading, archiving.

game_log.py has no Streamlit dependency; all functions are pure I/O.
Tests use monkeypatch to redirect _LOG_FILE and _ARCHIVE_DIR to tmp_path.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.game_log as _gl  # noqa: E402

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _patch_paths(monkeypatch, tmp_path: Path) -> tuple[str, str]:  # type: ignore[no-untyped-def]
    log_file = str(tmp_path / "game_log.json")
    archive_dir = str(tmp_path / "archive")
    monkeypatch.setattr(_gl, "_LOG_FILE", log_file)
    monkeypatch.setattr(_gl, "_ARCHIVE_DIR", archive_dir)
    return log_file, archive_dir


# ---------------------------------------------------------------------------
# _find_or_create_phase (internal helper)
# ---------------------------------------------------------------------------


class TestFindOrCreatePhase:
    def test_creates_first_round_and_phase(self) -> None:
        data: dict = {"rounds": []}
        phase = _gl._find_or_create_phase(data, 1, "shooting", "Necrons")
        assert len(data["rounds"]) == 1
        assert data["rounds"][0]["round"] == 1
        assert phase["phase"] == "shooting"
        assert phase["active"] == "Necrons"
        assert phase["events"] == []

    def test_finds_existing_phase_without_adding_duplicate(self) -> None:
        existing: dict = {"phase": "command", "active": "Necrons", "events": [{"type": "x"}]}
        data = {"rounds": [{"round": 1, "phases": [existing]}]}
        phase = _gl._find_or_create_phase(data, 1, "command", "Necrons")
        assert phase is existing
        assert len(data["rounds"][0]["phases"]) == 1

    def test_creates_new_phase_in_existing_round(self) -> None:
        data = {
            "rounds": [
                {"round": 1, "phases": [{"phase": "command", "active": "Necrons", "events": []}]}
            ]
        }
        phase = _gl._find_or_create_phase(data, 1, "shooting", "Necrons")
        assert len(data["rounds"][0]["phases"]) == 2
        assert phase["phase"] == "shooting"

    def test_creates_new_round_when_round_number_differs(self) -> None:
        data = {"rounds": [{"round": 1, "phases": []}]}
        _gl._find_or_create_phase(data, 2, "command", "Orks")
        assert len(data["rounds"]) == 2
        assert data["rounds"][1]["round"] == 2

    def test_active_discriminates_phases_with_same_name(self) -> None:
        data = {
            "rounds": [
                {"round": 1, "phases": [{"phase": "shoot", "active": "Necrons", "events": []}]}
            ]
        }
        phase = _gl._find_or_create_phase(data, 1, "shoot", "Orks")
        assert phase["active"] == "Orks"
        assert len(data["rounds"][0]["phases"]) == 2


# ---------------------------------------------------------------------------
# _read_log  (internal — exercised indirectly and directly)
# ---------------------------------------------------------------------------


class TestReadLog:
    def test_returns_empty_structure_when_file_missing(
        self, tmp_path: Path, monkeypatch
    ) -> None:  # type: ignore[no-untyped-def]
        _patch_paths(monkeypatch, tmp_path)
        data = _gl._read_log()
        assert data["rounds"] == []
        assert "game_id" in data

    def test_returns_empty_structure_for_corrupted_json(
        self, tmp_path: Path, monkeypatch
    ) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        Path(log_file).write_text("not { valid json >>>")
        data = _gl._read_log()
        assert data["rounds"] == []

    def test_returns_empty_structure_when_rounds_key_missing(
        self, tmp_path: Path, monkeypatch
    ) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        Path(log_file).write_text('{"game_id": "abc"}')
        data = _gl._read_log()
        assert "rounds" in data

    def test_reads_valid_existing_log(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        content = {"game_id": "test", "players": {}, "rounds": [{"round": 1, "phases": []}]}
        Path(log_file).write_text(json.dumps(content))
        data = _gl._read_log()
        assert data["game_id"] == "test"
        assert len(data["rounds"]) == 1


# ---------------------------------------------------------------------------
# log_action
# ---------------------------------------------------------------------------


class TestLogAction:
    def test_creates_log_file_on_first_call(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        _gl.log_action(1, "shooting", "Overlord", "fired")
        assert Path(log_file).exists()

    def test_event_unit_and_action_stored(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        _gl.log_action(1, "shooting", "Overlord", "fired 3 shots")
        data = json.loads(Path(log_file).read_text())
        event = data["rounds"][0]["phases"][0]["events"][0]
        assert event["unit"] == "Overlord"
        assert event["action"] == "fired 3 shots"
        assert event["type"] == "action"

    def test_multiple_actions_in_same_phase_accumulate(
        self, tmp_path: Path, monkeypatch
    ) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        _gl.log_action(1, "shooting", "Overlord", "first")
        _gl.log_action(1, "shooting", "Overlord", "second")
        data = json.loads(Path(log_file).read_text())
        events = data["rounds"][0]["phases"][0]["events"]
        assert len(events) == 2

    def test_different_rounds_create_separate_round_entries(
        self, tmp_path: Path, monkeypatch
    ) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        _gl.log_action(1, "command", "Necrons", "cp")
        _gl.log_action(2, "command", "Necrons", "cp")
        data = json.loads(Path(log_file).read_text())
        assert len(data["rounds"]) == 2


# ---------------------------------------------------------------------------
# set_log_players
# ---------------------------------------------------------------------------


class TestSetLogPlayers:
    def test_records_first_and_second_player(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        _gl.set_log_players("Necrons", "Orks")
        data = json.loads(Path(log_file).read_text())
        assert data["players"]["first"] == "Necrons"
        assert data["players"]["second"] == "Orks"

    def test_does_not_clear_existing_rounds(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        _gl.log_action(1, "command", "Necrons", "cp")
        _gl.set_log_players("Necrons", "Orks")
        data = json.loads(Path(log_file).read_text())
        assert len(data["rounds"]) == 1


# ---------------------------------------------------------------------------
# clear_game_log
# ---------------------------------------------------------------------------


class TestClearGameLog:
    def test_resets_rounds_to_empty(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        _gl.log_action(1, "shooting", "Necrons", "fired")
        _gl.clear_game_log()
        data = json.loads(Path(log_file).read_text())
        assert data["rounds"] == []

    def test_clears_players(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        _gl.set_log_players("Necrons", "Orks")
        _gl.clear_game_log()
        data = json.loads(Path(log_file).read_text())
        assert data["players"] == {}

    def test_new_game_id_written(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, _ = _patch_paths(monkeypatch, tmp_path)
        _gl.clear_game_log()
        data = json.loads(Path(log_file).read_text())
        assert "game_id" in data
        assert data["game_id"]  # non-empty


# ---------------------------------------------------------------------------
# archive_and_reset_log
# ---------------------------------------------------------------------------


class TestArchiveAndResetLog:
    def test_archive_file_created(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, archive_dir = _patch_paths(monkeypatch, tmp_path)
        _gl.log_action(1, "command", "Necrons", "cp")
        _gl.archive_and_reset_log()
        archived = list(Path(archive_dir).glob("*.json"))
        assert len(archived) == 1

    def test_log_rounds_empty_after_archive(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, archive_dir = _patch_paths(monkeypatch, tmp_path)
        _gl.log_action(1, "command", "Necrons", "cp")
        _gl.archive_and_reset_log()
        data = json.loads(Path(log_file).read_text())
        assert data["rounds"] == []

    def test_works_when_no_log_file_exists(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, archive_dir = _patch_paths(monkeypatch, tmp_path)
        _gl.archive_and_reset_log()
        assert Path(log_file).exists()
        assert list(Path(archive_dir).glob("*.json")) == []  # no log to archive

    def test_archived_file_contains_original_data(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        log_file, archive_dir = _patch_paths(monkeypatch, tmp_path)
        _gl.set_log_players("Necrons", "Orks")
        _gl.log_action(1, "command", "Necrons", "cp")
        _gl.archive_and_reset_log()
        archived = list(Path(archive_dir).glob("*.json"))[0]
        data = json.loads(archived.read_text())
        assert data["players"]["first"] == "Necrons"


# ---------------------------------------------------------------------------
# list_archived_logs
# ---------------------------------------------------------------------------


class TestListArchivedLogs:
    def test_empty_list_when_archive_dir_missing(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        _patch_paths(monkeypatch, tmp_path)
        assert _gl.list_archived_logs() == []

    def test_returns_metadata_for_modern_format(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        _, archive_dir = _patch_paths(monkeypatch, tmp_path)
        Path(archive_dir).mkdir()
        payload = {
            "game_id": "2026-01-01T12-00-00",
            "players": {"first": "Necrons", "second": "Orks"},
            "rounds": [{"round": 1, "phases": []}, {"round": 2, "phases": []}],
        }
        (Path(archive_dir) / "2026-01-01T12-00-00.json").write_text(json.dumps(payload))
        results = _gl.list_archived_logs()
        assert len(results) == 1
        r = results[0]
        assert r["first"] == "Necrons"
        assert r["second"] == "Orks"
        assert r["rounds"] == 2
        assert r["warning"] is None

    def test_handles_legacy_list_format(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        _, archive_dir = _patch_paths(monkeypatch, tmp_path)
        Path(archive_dir).mkdir()
        (Path(archive_dir) / "legacy.json").write_text(json.dumps([{"round": 1}]))
        results = _gl.list_archived_logs()
        assert len(results) == 1
        assert results[0]["warning"] is not None
        assert "Legacy" in results[0]["warning"]

    def test_handles_unexpected_type_format(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        _, archive_dir = _patch_paths(monkeypatch, tmp_path)
        Path(archive_dir).mkdir()
        (Path(archive_dir) / "weird.json").write_text('"just a string"')
        results = _gl.list_archived_logs()
        assert len(results) == 1
        assert results[0]["warning"] is not None

    def test_skips_non_json_files(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        _, archive_dir = _patch_paths(monkeypatch, tmp_path)
        Path(archive_dir).mkdir()
        (Path(archive_dir) / "readme.txt").write_text("ignore me")
        assert _gl.list_archived_logs() == []

    def test_multiple_logs_sorted_newest_first(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        _, archive_dir = _patch_paths(monkeypatch, tmp_path)
        Path(archive_dir).mkdir()
        modern = {"game_id": "z", "players": {}, "rounds": []}
        for name in ("aaa.json", "zzz.json"):
            (Path(archive_dir) / name).write_text(json.dumps(modern))
        results = _gl.list_archived_logs()
        assert len(results) == 2
        assert results[0]["filename"] == "zzz.json"

    def test_skips_corrupt_json_without_crashing(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        _, archive_dir = _patch_paths(monkeypatch, tmp_path)
        Path(archive_dir).mkdir()
        (Path(archive_dir) / "corrupt.json").write_text("{not valid json >>>")
        modern = {"game_id": "good", "players": {}, "rounds": []}
        (Path(archive_dir) / "good.json").write_text(json.dumps(modern))
        results = _gl.list_archived_logs()
        assert len(results) == 1
        assert results[0]["game_id"] == "good"
