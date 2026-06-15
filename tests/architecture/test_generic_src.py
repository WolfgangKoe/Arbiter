"""Guard: src/ stays faction-generic.

No faction-specific decision logic belongs in src/. Every Necron/Ork/Custodes
choice must come from the YAML data layer. This guard flags faction names that
appear as *string literals in code* (not comments, not docstrings) — the usual
shape of an accidental hardcoded faction branch or default.

DEBT LEDGER: the allowlist below enumerates every faction string that exists in
src/ today, each with a reason. Entries marked LEGIT are permanent (external
label normalisation). Entries marked DEBT are tracked cleanup items in
docs/goals/backlog.md — they keep the build green while making the drift visible.

Any *new* faction string in a non-allowlisted file (or a new token in an
allowlisted file) fails this test.

Status: holds today (allowlist == current debt). See architecture_invariants.md (INV-4).
"""

from __future__ import annotations

import re

from tests.architecture._arch import parse, py_files, rel, string_constants

# token -> compiled pattern. "ork" needs a leading word boundary so it does not
# match "work"/"fork"/"network"; the others are unambiguous substrings.
FACTION_PATTERNS: dict[str, re.Pattern[str]] = {
    "necron": re.compile(r"necron", re.IGNORECASE),
    "ork": re.compile(r"\bork", re.IGNORECASE),
    "custodes": re.compile(r"custodes", re.IGNORECASE),
    "szarekh": re.compile(r"szarekh", re.IGNORECASE),
    "nephrekh": re.compile(r"nephrekh", re.IGNORECASE),
    "waaagh": re.compile(r"waaagh", re.IGNORECASE),
}

# file (relative to src/) -> set of faction tokens permitted in that file.
ALLOWLIST: dict[str, set[str]] = {
    # LEGIT — maps external BattleScribe faction labels to internal slugs.
    # This is I/O normalisation at the import boundary, not game logic.
    "gameObjects/rosz_importer.py": {"necron", "ork", "custodes"},
    # DEBT — hardcoded default rosters / default faction. Should derive from the
    # selected armies instead. Tracked: docs/goals/backlog.md (generic-src).
    "gameMechanic/game_state.py": {"necron"},
    "gameObjects/loader.py": {"necron"},
    # DEBT — default player labels "Necrons"/"Orks" as session_state fallbacks.
    "uiLayout/gameHeader.py": {"necron", "ork"},
    "uiLayout/gameProtocoll.py": {"necron", "ork"},
    # DEBT — faction-specific caption text in the setup screen.
    "uiLayout/setupScreen.py": {"necron"},
}


def test_no_unlisted_faction_strings_in_src() -> None:
    violations = []
    for path in py_files():
        allowed = ALLOWLIST.get(rel(path), set())
        for node in string_constants(parse(path)):
            for token, pattern in FACTION_PATTERNS.items():
                if pattern.search(node.value) and token not in allowed:
                    snippet = node.value if len(node.value) <= 60 else node.value[:57] + "..."
                    violations.append(f"{rel(path)}:{node.lineno} {token!r} in {snippet!r}")
    assert not violations, (
        "Faction-specific string literals in src/ (Generic-src rule). "
        "If legitimate, add to ALLOWLIST with a reason; otherwise move the "
        "decision into YAML data:\n" + "\n".join(violations)
    )
