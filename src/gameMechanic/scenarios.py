"""Scenario loading for quick-start testing and dev fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

_SCENARIOS_DIR = Path(__file__).parent.parent.parent / "data" / "scenarios"


def get_scenario_data(name: str) -> dict[str, Any] | None:
    """Return parsed scenario JSON or None if not found."""
    path = _SCENARIOS_DIR / f"{name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())  # type: ignore[no-any-return]


def apply_scenario(data: dict[str, Any], state: dict[str, Any]) -> None:
    """Patch a state dict with scenario data. Pure function — safe for tests."""
    for key in ("round", "phase_idx", "active", "phase_stage", "cp", "vp"):
        if key in data:
            state[key] = data[key]

    unit_patches: dict[str, dict[str, Any]] = data.get("unit_patches", {})
    for faction_key, patches in unit_patches.items():
        if faction_key not in state:
            continue
        for uid, patch in patches.items():
            if uid not in state[faction_key]:
                continue
            unit = state[faction_key][uid]
            # Deep-merge turn_flags so only specified flags are overridden
            if "turn_flags" in patch:
                unit["turn_flags"].update(patch.pop("turn_flags"))
            unit.update(patch)
            # Keep in_melee consistent with melee_with
            if "melee_with" in patch:
                unit["in_melee"] = bool(unit["melee_with"])


def load_scenario(name: str) -> bool:
    """Load a scenario by name into st.session_state. Returns True if found."""
    data = get_scenario_data(name)
    if data is None:
        return False
    # Build a plain dict view of session_state for apply_scenario
    state: dict[str, Any] = {
        k: st.session_state[k] for k in st.session_state if not k.startswith("_")
    }
    apply_scenario(data, state)
    for key, value in state.items():
        st.session_state[key] = value
    return True


def save_scenario(name: str) -> None:
    """Snapshot the current game state to data/scenarios/<name>.json."""
    necron_units = {uid: dict(s) for uid, s in st.session_state.get("necron_units", {}).items()}
    ork_units = {uid: dict(s) for uid, s in st.session_state.get("ork_units", {}).items()}
    data: dict[str, Any] = {
        "description": f"Snapshot — round {st.session_state.get('round', 1)}, phase {st.session_state.get('phase_idx', 0)}",
        "round": st.session_state.get("round", 1),
        "phase_idx": st.session_state.get("phase_idx", 0),
        "active": st.session_state.get("active", "Necrons"),
        "phase_stage": st.session_state.get("phase_stage", "active"),
        "cp": dict(st.session_state.get("cp", {})),
        "vp": dict(st.session_state.get("vp", {})),
        "unit_patches": {
            "necron_units": necron_units,
            "ork_units": ork_units,
        },
    }
    _SCENARIOS_DIR.mkdir(parents=True, exist_ok=True)
    (_SCENARIOS_DIR / f"{name}.json").write_text(json.dumps(data, indent=2))
