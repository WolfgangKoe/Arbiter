"""Game state — phase definitions, army loading, init / reset / next_phase."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

import streamlit as st

from gameObjects.loader import (
    load_faction_display_name,
    load_roster,
    load_roster_metadata,
    load_round_choice_abilities,
    load_subfaction_meta,
    load_unit_catalog,
    load_yaml,
)
from gameObjects.unit import Unit


@dataclass
class TargetSelectionRequest:
    """A pending target-selection request placed in st.session_state.pending_target_request.

    Exactly one slot exists; a new request overwrites any previous one.
    Set to None to cancel.
    """

    ability_id: str  # unique identifier (used as widget key suffix)
    required_keywords: list[str] = field(default_factory=list)  # [] = all eligible
    exclude_uid: str | None = None  # exclude this state_key (e.g. the bearer)
    faction_filter: str | None = None  # "own" | "enemy" | None
    multi: bool = False  # whether multiple targets are allowed
    badge_label: str = ""  # button label shown on the unit card
    effect_type: str = ""  # "buff_roll" | "reroll_hit_1" | "" (revive/wargear)


PHASES: list[tuple[str, str]] = [
    ("Setup", "setup"),
    ("Command", "command"),
    ("Movement", "movement"),
    ("Psychic", "psychic"),
    ("Shooting", "shooting"),
    ("Charge", "charge"),
    ("Fight", "fight"),
    ("Morale", "morale"),
]

_ROSTER_DIR = Path(__file__).parent.parent.parent / "data" / "rosters"

CP_BY_GAME_SIZE: dict[str, int] = {
    "Combat Patrol": 3,
    "Incursion": 6,
    "Strike Force": 12,
    "Onslaught": 18,
}

PTS_LIMIT_BY_GAME_SIZE: dict[str, int] = {
    "Combat Patrol": 500,
    "Incursion": 1000,
    "Strike Force": 2000,
    "Onslaught": 3000,
}

_DATA_ROOT = Path(__file__).parent.parent.parent / "data"


# ---------------------------------------------------------------------------
# Roster loading helper
# ---------------------------------------------------------------------------


def _load_roster_for(
    roster_file: str,
    fallback_faction: str,
) -> tuple[list[tuple[Unit, int]], list[str], str, str, str | None, list[str] | None]:
    """Load a roster; fall back to full catalog if file is missing.

    Returns (matched_entries, unmatched_ids, display_name, faction_dir, subfaction,
    round_choice_order). subfaction is the roster's subfaction choice read via the
    faction's declared field (generic — no faction-specific vocabulary in src/);
    round_choice_order is the optional roster-defined round-choice ability order.
    """
    path = _ROSTER_DIR / roster_file
    meta = load_roster_metadata(path)
    faction_dir = meta.get("faction_dir") or fallback_faction
    display_name = meta.get("display_name") or roster_file
    subfaction: str | None = meta.get("subfaction")
    round_choice_order: list[str] | None = meta.get("round_choice_order")

    catalog = load_unit_catalog(faction_dir)
    if path.exists():
        matched, unmatched = load_roster(path, catalog)
    else:
        matched = [(u, u.models_max) for u in catalog.values()]
        unmatched = []
    return matched, unmatched, display_name, faction_dir, subfaction, round_choice_order


def list_available_rosters() -> list[str]:
    """Return all .yaml filenames in the rosters directory."""
    return sorted(p.name for p in _ROSTER_DIR.glob("*.yaml"))


def compute_roster_total_pts(roster_file: str) -> int:
    """Return the total points cost for a roster file. Returns 0 on error.

    Handles per_unit (flat cost) and per_model (cost × model_count) entries.
    """
    roster_path = _ROSTER_DIR / roster_file
    meta = load_roster_metadata(roster_path)
    faction_dir = meta.get("faction_dir", "")
    if not faction_dir:
        return 0
    pts_path = _DATA_ROOT / "wh40k_9e" / faction_dir / "points.yaml"
    if not pts_path.exists():
        return 0
    pts_data = load_yaml(pts_path) or {}
    units_pts: dict[str, dict] = pts_data.get("units") or {}
    roster_data = load_yaml(roster_path) or {}
    total = 0
    for entry in roster_data.get("units", []):
        uid = entry["id"]
        models = int(entry.get("models", 1))
        cost_entry = units_pts.get(uid)
        if not cost_entry:
            continue
        if "per_model" in cost_entry:
            total += int(cost_entry["per_model"]) * models
        else:
            total += int(cost_entry.get("per_unit", 0))
    return total


# ---------------------------------------------------------------------------
# Player-slot helpers  (require Streamlit session state to be active)
# ---------------------------------------------------------------------------


def units_key_for(player: str) -> str:
    """Return the session_state key that holds a player's unit states."""
    return "p1_units" if player == st.session_state.get("first_player") else "p2_units"


def faction_dir_for(player: str) -> str:
    """Return the data-directory name for a player's faction."""
    if player == st.session_state.get("first_player"):
        return st.session_state["p1_faction_dir"]
    return st.session_state["p2_faction_dir"]


def subfaction_value_for(player: str) -> str | None:
    """Return a player's raw subfaction tag (from the roster), or None.

    Generic: the value is whatever the roster declared (e.g. 'szarekhan',
    'bad_moons'); used for subfaction-affinity comparisons. Armies that made no
    subfaction choice return None.
    """
    if player == st.session_state.get("first_player"):
        return st.session_state.get("p1_subfaction")
    return st.session_state.get("p2_subfaction")


def faction_display_name_for(player: str) -> str:
    """Human-readable faction name for a player's armyCard badge (e.g. 'Necrons')."""
    try:
        return load_faction_display_name(faction_dir_for(player))
    except KeyError:
        return str(player)


class SubfactionBadge(NamedTuple):
    """Resolved subfaction badge for the armyCard. Always renders (never hidden)."""

    text: str
    # "set"     → a valid subfaction was chosen; buffs may apply
    # "missing" → roster is valid but made no choice → no buffs, visible placeholder
    # "error"   → faction declares no subfaction field (data gap) → visible error
    state: str


def subfaction_badge_for(player: str) -> SubfactionBadge:
    """Resolve a player's subfaction badge generically from faction + roster data.

    Mandatory & always visible: a missing choice shows a 'No <Label>' placeholder
    (no buffs), a missing faction binding shows a 'No Subfaction' error — never an
    empty/invisible badge.
    """
    try:
        faction_dir = faction_dir_for(player)
    except KeyError:
        return SubfactionBadge("No Subfaction", "error")
    field, label = load_subfaction_meta(faction_dir)
    if not field:
        return SubfactionBadge("No Subfaction", "error")
    slot = "p1_subfaction" if player == st.session_state.get("first_player") else "p2_subfaction"
    value = st.session_state.get(slot)
    if not value:
        return SubfactionBadge(f"No {label}", "missing")
    return SubfactionBadge(str(value).replace("_", " ").title(), "set")


def short_round_choice_label(name_en: str) -> str:
    """Drop a leading '<Type> of the ' qualifier → 'Undying Legions' (Finding 7).

    Generic string transform — no faction names. Names without the marker are
    returned unchanged (e.g. Custodes Ka'tah stances).
    """
    marker = " of the "
    idx = name_en.find(marker)
    return name_en[idx + len(marker) :] if idx != -1 else name_en


def active_round_choice_buff_labels(player: str) -> list[str]:
    """Short labels for the player's currently-active round-choice directives.

    Derived from session state at render time (no stored buff to expire). Covers
    the round-assigned ability and the always-active 6th ability (incl. the
    subfaction-affinity bonus where both directives apply). Empty for factions
    without a round-choice ability file — gated on data, not on faction names.
    """
    try:
        faction_dir = faction_dir_for(player)
    except KeyError:
        return []
    round_choices = load_round_choice_abilities(faction_dir)
    if not round_choices:
        return []

    labels: list[str] = []
    by_id = {p.id: p for p in round_choices}

    active_id = st.session_state.get(f"round_choice_active_{faction_dir}")
    if active_id and st.session_state.get(f"round_choice_directive_{faction_dir}"):
        p = by_id.get(active_id)
        if p:
            labels.append(short_round_choice_label(p.name_en))

    # 6th (always-active) ability: the single one not assigned to any round.
    assignments = st.session_state.get("round_choice_assignments", {}).get(player, {})
    assigned_ids = set(assignments.values())
    if len(assigned_ids) >= 5:
        extras = [p for p in round_choices if p.id not in assigned_ids]
        if len(extras) == 1:
            extra = extras[0]
            subfaction = subfaction_value_for(player)
            affinity_bonus = bool(subfaction and subfaction == extra.subfaction_affinity)
            if affinity_bonus or st.session_state.get(
                f"round_choice_extra_directive_{faction_dir}"
            ):
                labels.append(short_round_choice_label(extra.name_en))
    return labels


def units_list_for(player: str) -> list[Unit]:
    """Return the Unit-definition list for a player (for stats / name lookups)."""
    if player == st.session_state.get("first_player"):
        return st.session_state.get("p1_units_list", [])
    return st.session_state.get("p2_units_list", [])


def unit_keys_for(player: str) -> list[str]:
    """Return the ordered list of state-dict keys for a player's units.

    Matches the order of units_list_for(). For duplicate unit IDs a '#N' suffix
    is appended (e.g. 'wh40k_9e.necrons.unit.warriors#1' for the second squad).
    """
    if player == st.session_state.get("first_player"):
        return st.session_state.get("p1_unit_keys", [])
    return st.session_state.get("p2_unit_keys", [])


def unit_id_from_state_key(state_key: str) -> str:
    """Strip the deduplication suffix from a state key to get the canonical unit ID.

    'wh40k_9e.necrons.unit.warriors#1' → 'wh40k_9e.necrons.unit.warriors'
    """
    return state_key.split("#")[0]


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------


def _make_unit_state_dict(
    matched: list[tuple[Unit, int]],
) -> tuple[dict, list[str]]:  # type: ignore[type-arg]
    """Build the state dict and ordered key list for a matched unit list.

    Duplicate unit IDs are disambiguated with a '#N' suffix so each unit
    instance has its own independent state.
    """
    counts: dict[str, int] = {}
    state_dict: dict[str, dict] = {}  # type: ignore[type-arg]
    keys: list[str] = []
    for u, m in matched:
        n = counts.get(u.id, 0)
        counts[u.id] = n + 1
        key = u.id if n == 0 else f"{u.id}#{n}"
        state_dict[key] = _unit_state(u, m)
        keys.append(key)
    return state_dict, keys


def _unit_state(u: Unit, models: int | None = None) -> dict:  # type: ignore[type-arg]
    count = min(models, u.models_max) if models is not None else u.models_max
    # model_groups counts are already resolved from the roster in load_roster
    group_models: dict[str, int] = {g.id: g.count for g in u.model_groups} if u.model_groups else {}
    # group_wounds is the single canonical per-group HP pool for EVERY unit with
    # model groups — mixed-wound units (Szarekh 16 + Triarchal Menhirs 7) and
    # homogeneous squads (e.g. Nobz) alike. current_wounds is their sum and stays
    # identical to wounds × models for homogeneous groups (group_wound_value falls
    # back to unit.wounds, sum(group counts) == count).
    if u.model_groups:
        group_wounds: dict[str, int] = {
            g.id: g.count * u.group_wound_value(g) for g in u.model_groups
        }
        current_wounds = sum(group_wounds.values())
    else:
        group_wounds = {}
        current_wounds = u.wounds * count
    return {
        "current_wounds": current_wounds,
        "models": count,
        "models_initial": count,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "stationary",
        "lost_models_this_turn": 0,
        "fled_models_this_turn": 0,
        "movement_choice": "stationary",
        "movement_chosen": False,
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
            "cast": False,
            "heroic_intervened": False,
            "morale_tested": False,
            "movement_locked": False,
            "mortal_effect_applied": False,
        },
        "active_buffs": [],
        "models_lost_since_last_rp": 0,
        "group_models": group_models,
        "group_wounds": group_wounds,
        "damage_active_group_id": None,
    }


def init_state(
    roster_p1: str = "necrons_alpha.yaml",
    roster_p2: str = "necrons_beta.yaml",
    game_size: str = "Incursion",
    vp_phase: str = "Morale",
    vp_from_round: int = 1,
    game_mode: str = "matched",
    mission: str | None = None,
    attacker: str | None = None,
    use_secondaries: bool = False,
    secondaries: dict | None = None,  # type: ignore[type-arg]
    secondary_vp: dict | None = None,  # type: ignore[type-arg]
) -> None:
    if "initialized" in st.session_state:
        return

    p1_matched, p1_unmatched, p1_name, p1_faction_dir, p1_subfaction, p1_proto_order = (
        _load_roster_for(roster_p1, "necrons")
    )
    p2_matched, p2_unmatched, p2_name, p2_faction_dir, p2_subfaction, p2_proto_order = (
        _load_roster_for(roster_p2, "necrons")
    )

    if attacker == "p2":
        p1_matched, p2_matched = p2_matched, p1_matched
        p1_name, p2_name = p2_name, p1_name
        p1_faction_dir, p2_faction_dir = p2_faction_dir, p1_faction_dir
        p1_subfaction, p2_subfaction = p2_subfaction, p1_subfaction
        p1_proto_order, p2_proto_order = p2_proto_order, p1_proto_order
        p1_unmatched, p2_unmatched = p2_unmatched, p1_unmatched

    starting_cp = CP_BY_GAME_SIZE.get(game_size, 3) if game_mode == "matched" else 3

    st.session_state.initialized = True
    st.session_state.round = 1
    st.session_state.phase_idx = 0
    st.session_state.first_player = p1_name
    st.session_state.second_player = p2_name
    st.session_state.player_slots = (p1_name, p2_name)
    st.session_state.active = p1_name
    st.session_state.cp = {p1_name: starting_cp, p2_name: starting_cp}
    st.session_state.vp = {p1_name: 0, p2_name: 0}
    st.session_state.selected_unit = None
    st.session_state.selected_targets = []
    st.session_state.phase_stage = "active"
    st.session_state.active_effect = None
    st.session_state.cp_granted_this_phase = False
    st.session_state.used_stratagem_ids: set[str] = set()
    st.session_state.active_modifiers: list[dict] = []
    st.session_state.command_ability_state: dict = {}
    # Round-choice state is keyed per faction_dir (set on demand in armyCard)
    st.session_state.pending_target_request: TargetSelectionRequest | None = None
    st.session_state.revive_wargear_target_uid: dict[str, str] = {}
    st.session_state.wargear_used: dict[str, bool] = {}
    st.session_state.mortal_target_uid: str | None = None
    st.session_state.relic_triggered_used: dict[str, bool] = {}
    st.session_state.morgog_cap_rolled_this_phase = False
    st.session_state.pending_triggered_relic: dict | None = None
    st.session_state.veil_awaiting_confirm: bool = False
    st.session_state.veil_core_target_uid: str | None = None

    # Unit lists for stat/name lookups (indexed by player slot, not faction)
    st.session_state.p1_units_list = [u for u, _ in p1_matched]
    st.session_state.p2_units_list = [u for u, _ in p2_matched]
    st.session_state.p1_faction_dir = p1_faction_dir
    st.session_state.p2_faction_dir = p2_faction_dir
    st.session_state.p1_subfaction = p1_subfaction
    st.session_state.p2_subfaction = p2_subfaction

    # Optional roster-defined round-choice ability order (round 1..5 → ability id),
    # keyed by player name; the setup UI uses these as defaults (overridable).
    round_choice_assignments: dict = {}
    for pname, order in ((p1_name, p1_proto_order), (p2_name, p2_proto_order)):
        if order:
            round_choice_assignments[pname] = {i + 1: pid for i, pid in enumerate(order[:5])}
    st.session_state.round_choice_assignments = round_choice_assignments

    p1_states, p1_keys = _make_unit_state_dict(p1_matched)
    p2_states, p2_keys = _make_unit_state_dict(p2_matched)
    st.session_state.p1_units = p1_states
    st.session_state.p2_units = p2_states
    st.session_state.p1_unit_keys = p1_keys
    st.session_state.p2_unit_keys = p2_keys

    st.session_state.vp_phase = vp_phase
    st.session_state.vp_from_round = vp_from_round

    # Game configuration
    st.session_state.game_mode = game_mode
    st.session_state.game_size = game_size
    st.session_state.mission = mission
    st.session_state.attacker = attacker
    st.session_state.use_secondaries = use_secondaries
    st.session_state.secondaries = secondaries
    st.session_state.secondary_vp = secondary_vp

    # Round-choice per-faction keys are not pre-initialized; armyCard sets them on demand
    st.session_state.activated_abilities: dict = (
        {}
    )  # {player_name: {"ability_id": str, "round_activated": int}}
    st.session_state.psi_attempts_this_phase = 0
    st.session_state.fight_current_player: str | None = None
    st.session_state.attack_declaration: dict = {"active": False, "entries": []}
    st.session_state.charge_phase_step: int = 1
    st.session_state.pending_hi: tuple | None = None
    st.session_state.hi_targets: list = []
    if p1_unmatched or p2_unmatched:
        st.session_state.roster_warnings = {
            p1_name: p1_unmatched,
            p2_name: p2_unmatched,
        }
    else:
        st.session_state.roster_warnings = {}

    from gameMechanic.game_log import set_log_players  # noqa: PLC0415

    set_log_players(p1_name, p2_name)


def swap_players() -> None:
    """Swap first_player / second_player and all associated p1/p2 session state.

    Called from the in-game setup phase when the user chooses who goes first.
    Keeps CP, VP, and game config consistent because those are keyed by display name.
    """
    ss = st.session_state
    ss.first_player, ss.second_player = ss.second_player, ss.first_player
    ss.p1_units, ss.p2_units = ss.p2_units, ss.p1_units
    ss.p1_units_list, ss.p2_units_list = ss.p2_units_list, ss.p1_units_list
    ss.p1_unit_keys, ss.p2_unit_keys = ss.p2_unit_keys, ss.p1_unit_keys
    ss.p1_faction_dir, ss.p2_faction_dir = ss.p2_faction_dir, ss.p1_faction_dir
    ss.p1_subfaction, ss.p2_subfaction = ss.p2_subfaction, ss.p1_subfaction


def reset_game() -> None:
    from gameMechanic.game_log import archive_and_reset_log  # noqa: PLC0415

    archive_and_reset_log()
    for k in list(st.session_state.keys()):
        del st.session_state[k]


def _reset_phase_state() -> None:
    st.session_state.cp_granted_this_phase = False
    st.session_state.morgog_cap_rolled_this_phase = False
    st.session_state.pending_triggered_relic = None
    st.session_state.pending_target_request = None
    st.session_state.mortal_target_uid = None
    st.session_state.veil_awaiting_confirm = False
    st.session_state.veil_core_target_uid = None
    for k in list(st.session_state.keys()):
        if k.startswith("applied_triggered_"):
            del st.session_state[k]
    st.session_state.used_stratagem_ids = set()
    st.session_state.fight_current_player = None
    st.session_state.attack_declaration = {"active": False, "entries": []}
    st.session_state.selected_model_group = None
    st.session_state.group_targets = {}
    st.session_state.group_decl = {}
    st.session_state.charge_phase_step = 1
    st.session_state.pending_hi = None
    st.session_state.hi_targets = []
    current_phase = PHASES[st.session_state.get("phase_idx", 0)][1]
    current_round = st.session_state.get("round", 1)
    st.session_state.active_modifiers = [
        m
        for m in st.session_state.get("active_modifiers", [])
        if not (
            m.get("expires_at_phase") == current_phase
            or (m.get("expires_at_round") is not None and m["expires_at_round"] <= current_round)
        )
    ]


def _reset_turn_state() -> None:
    st.session_state.pending_mortal_undo = None
    current_round = st.session_state.get("round", 1)
    for key in ("p1_units", "p2_units"):
        for state in st.session_state[key].values():
            flags = state["turn_flags"]
            for flag in flags:
                flags[flag] = False
            state["lost_models_this_turn"] = 0
            state["fled_models_this_turn"] = 0
            state["movement_choice"] = "stationary"
            state["movement_chosen"] = False
            state["active_buffs"] = []
    for slot in ("p1_faction_dir", "p2_faction_dir"):
        fdir = st.session_state.get(slot)
        if fdir:
            st.session_state[f"round_choice_active_{fdir}"] = None
            st.session_state[f"round_choice_directive_{fdir}"] = None
            st.session_state[f"round_choice_extra_directive_{fdir}"] = None
    # Stage transition: if the active ability has a next_stage_id and a new round began, advance
    from gameObjects.loader import load_faction_abilities  # noqa: PLC0415

    activated = st.session_state.get("activated_abilities", {})
    for player, entry in activated.items():
        ability_id = entry.get("ability_id")
        round_activated = entry.get("round_activated", current_round)
        if ability_id and round_activated < current_round:
            try:
                fdir = faction_dir_for(player)
            except KeyError:
                continue
            abilities = load_faction_abilities(fdir)
            ability = next((a for a in abilities if a.id == ability_id), None)
            if ability and ability.next_stage_id:
                activated[player] = {**entry, "ability_id": ability.next_stage_id}
    st.session_state.activated_abilities = activated


def next_phase() -> None:
    idx = st.session_state.phase_idx
    num = len(PHASES)
    first = st.session_state.first_player
    second = st.session_state.second_player

    if idx == 0:  # Setup → first Command phase
        st.session_state.phase_idx = 1
        _reset_phase_state()
    elif idx >= num - 1:  # Morale done → switch player
        st.session_state.active = second if st.session_state.active == first else first
        st.session_state.round += 1 if st.session_state.active == first else 0
        _reset_turn_state()
        _reset_phase_state()
        st.session_state.phase_idx = 1
    else:
        st.session_state.phase_idx = idx + 1
        _reset_phase_state()

    st.session_state.selected_unit = None
    st.session_state.selected_targets = []
    st.session_state.psi_result = None
    st.session_state.psychic_denies_used = {}
    st.session_state.psi_attempts_this_phase = 0
