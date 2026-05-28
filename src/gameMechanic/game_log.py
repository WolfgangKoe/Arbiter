"""Persistent action log for the current battle."""

from __future__ import annotations

import json
import os
from datetime import datetime

_LOG_FILE = os.path.join("data", "log", "game_log.json")


def log_action(round_num: int, phase: str, unit_name: str, action: str) -> None:
    os.makedirs("data/log", exist_ok=True)
    entry = {
        "round": round_num,
        "phase": phase,
        "unit": unit_name,
        "action": action,
        "timestamp": datetime.now().isoformat(),
    }
    entries: list[dict] = []  # type: ignore[type-arg]
    if os.path.exists(_LOG_FILE):
        with open(_LOG_FILE) as f:
            try:
                entries = json.load(f)
            except json.JSONDecodeError:
                entries = []
    entries.append(entry)
    with open(_LOG_FILE, "w") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def clear_game_log() -> None:
    os.makedirs("data/log", exist_ok=True)
    with open(_LOG_FILE, "w") as f:
        json.dump([], f)
