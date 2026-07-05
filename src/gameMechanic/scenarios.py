"""Scenario loading for quick-start testing and dev fixtures."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import streamlit as st

_SCENARIOS_DIR = Path(__file__).parent.parent.parent / "data" / "scenarios"
_VALID_NAME = re.compile(r"^[A-Za-z0-9_-]+$")


def get_scenario_data(name: str) -> dict[str, Any] | None:
    """Return parsed scenario JSON or None if not found."""
    if not _VALID_NAME.fullmatch(name):
        return None
    path = _SCENARIOS_DIR / f"{name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())  # type: ignore[no-any-return]


def apply_scenario(data: dict[str, Any], state: dict[str, Any]) -> None:
    """Patch a state dict with scenario data. Pure function — safe for tests."""
    for key in ("round", "phase_idx"):
        if key in data:
            state[key] = data[key]

    # Re-map faction-keyed dicts positionally so loading a scenario saved with
    # different player names never causes a KeyError in gameHeader.
    first = state.get("first_player", "")
    second = state.get("second_player", "")
    for dict_key in ("cp", "vp"):
        if dict_key not in data:
            continue
        src: dict[str, Any] = data[dict_key]
        src_keys = list(src.keys())
        mapped: dict[str, Any] = dict(state.get(dict_key) or {})
        if first and len(src_keys) >= 1:
            mapped[first] = src[src_keys[0]]
        if second and len(src_keys) >= 2:
            mapped[second] = src[src_keys[1]]
        state[dict_key] = mapped

    # Map "active" player positionally using the cp key order from the scenario.
    if "active" in data:
        src_cp_keys = list((data.get("cp") or {}).keys())
        src_active = data["active"]
        if first and src_cp_keys and src_active == src_cp_keys[0]:
            state["active"] = first
        elif second and len(src_cp_keys) >= 2 and src_active == src_cp_keys[1]:
            state["active"] = second
        else:
            state["active"] = src_active

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
    if not _VALID_NAME.fullmatch(name):
        raise ValueError(f"Invalid scenario name {name!r}: only [A-Za-z0-9_-] allowed.")
    p1_units = {uid: dict(s) for uid, s in st.session_state.get("p1_units", {}).items()}
    p2_units = {uid: dict(s) for uid, s in st.session_state.get("p2_units", {}).items()}
    data: dict[str, Any] = {
        "description": f"Snapshot — round {st.session_state.get('round', 1)}, phase {st.session_state.get('phase_idx', 0)}",
        "round": st.session_state.get("round", 1),
        "phase_idx": st.session_state.get("phase_idx", 0),
        "active": st.session_state.get("active", ""),
        "cp": dict(st.session_state.get("cp", {})),
        "vp": dict(st.session_state.get("vp", {})),
        "unit_patches": {
            "p1_units": p1_units,
            "p2_units": p2_units,
        },
    }
    _SCENARIOS_DIR.mkdir(parents=True, exist_ok=True)
    (_SCENARIOS_DIR / f"{name}.json").write_text(json.dumps(data, indent=2))
