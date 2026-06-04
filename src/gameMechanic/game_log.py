"""Persistent action log for the current battle.

Format (data/log/game_log.json):
  {
    "game_id": "<ISO timestamp>",
    "players": {"first": "<name>", "second": "<name>"},
    "rounds": [
      {
        "round": 1,
        "phases": [
          {
            "phase": "shooting",
            "active": "<player>",
            "events": [{"type": "action", "unit": "<name>", "action": "<text>"}]
          }
        ]
      }
    ]
  }
"""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime

_LOG_FILE = os.path.join("data", "log", "game_log.json")
_ARCHIVE_DIR = os.path.join("data", "log", "archive")


def _read_log() -> dict:
    if os.path.exists(_LOG_FILE):
        with open(_LOG_FILE) as f:
            try:
                data = json.load(f)
                if isinstance(data, dict) and "rounds" in data:
                    return data
            except json.JSONDecodeError:
                pass
    return {"game_id": datetime.now().isoformat(), "players": {}, "rounds": []}


def _write_log(data: dict) -> None:
    os.makedirs("data/log", exist_ok=True)
    with open(_LOG_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _find_or_create_phase(data: dict, round_num: int, phase: str, active: str) -> dict:
    for r in data["rounds"]:
        if r["round"] == round_num:
            for p in r["phases"]:
                if p["phase"] == phase and p["active"] == active:
                    return p
            new_phase: dict = {"phase": phase, "active": active, "events": []}
            r["phases"].append(new_phase)
            return new_phase
    new_round: dict = {
        "round": round_num,
        "phases": [{"phase": phase, "active": active, "events": []}],
    }
    data["rounds"].append(new_round)
    return new_round["phases"][0]


def log_action(round_num: int, phase: str, unit_name: str, action: str) -> None:
    data = _read_log()
    active = unit_name  # unit_name doubles as the active player/faction in generic calls
    phase_entry = _find_or_create_phase(data, round_num, phase, active)
    phase_entry["events"].append({"type": "action", "unit": unit_name, "action": action})
    _write_log(data)


def set_log_players(first: str, second: str) -> None:
    """Record player names in the log header. Call once after game init."""
    data = _read_log()
    data["players"] = {"first": first, "second": second}
    _write_log(data)


def archive_and_reset_log() -> None:
    """Move the current log to the archive directory, then start a fresh log."""
    os.makedirs(_ARCHIVE_DIR, exist_ok=True)
    if os.path.exists(_LOG_FILE):
        data = _read_log()
        game_id = data.get("game_id", datetime.now().isoformat()).replace(":", "-")
        archive_path = os.path.join(_ARCHIVE_DIR, f"{game_id}.json")
        shutil.move(_LOG_FILE, archive_path)
    _write_log({"game_id": datetime.now().isoformat(), "players": {}, "rounds": []})


def clear_game_log() -> None:
    _write_log({"game_id": datetime.now().isoformat(), "players": {}, "rounds": []})


def list_archived_logs() -> list[dict]:
    """Return metadata for each archived log, newest first."""
    if not os.path.exists(_ARCHIVE_DIR):
        return []
    results = []
    for fname in sorted(os.listdir(_ARCHIVE_DIR), reverse=True):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(_ARCHIVE_DIR, fname)
        try:
            with open(path) as f:
                data = json.load(f)
            if isinstance(data, list):
                round_count = len({e.get("round") for e in data if isinstance(e, dict)})
                results.append(
                    {
                        "filename": fname,
                        "path": path,
                        "game_id": fname.replace(".json", ""),
                        "first": "?",
                        "second": "?",
                        "rounds": round_count,
                        "warning": "Legacy format (list) — player data unavailable",
                    }
                )
                continue
            if not isinstance(data, dict):
                results.append(
                    {
                        "filename": fname,
                        "path": path,
                        "game_id": fname.replace(".json", ""),
                        "first": "?",
                        "second": "?",
                        "rounds": 0,
                        "warning": f"Unexpected format ({type(data).__name__})",
                    }
                )
                continue
            players = data.get("players", {})
            rounds = data.get("rounds", [])
            results.append(
                {
                    "filename": fname,
                    "path": path,
                    "game_id": data.get("game_id", fname),
                    "first": players.get("first", "?"),
                    "second": players.get("second", "?"),
                    "rounds": len(rounds),
                    "warning": None,
                }
            )
        except (json.JSONDecodeError, OSError):
            continue
    return results
