"""Guard (INV-4b): no faction *vocabulary* leaks into src/ — data-driven.

Where ``test_generic_src.py`` checks a hand-written list of faction *names*, this
guard derives the forbidden vocabulary from the YAML database itself
(``tests/architecture/_vocab.py``): every proper noun unique to one faction —
'overlord', 'klaw', 'irongob', 'reanimation', the faction names — plus a small
seed of faction concept-words. Any such token appearing in a src/ identifier or
string literal (not docstrings) is a leak.

DEBT LEDGER: ``LEDGER`` below enumerates every faction token in src/ today.
- LEGIT: I/O label normalisation at the import boundary (roszImporter).
- DEBT: faction-specific logic/strings that should move into the YAML data layer
  (tracked in docs/goals/backlog.md). The ledger keeps the build green while
  making the drift measurable and preventing NEW leaks.

A new faction token in a non-ledgered file fails the build. A ledger entry that
no longer leaks also fails — that is the ratchet: clean the code, shrink the
ledger. See docs/spec/architecture_invariants.md (INV-4b).
"""

from __future__ import annotations

from collections import defaultdict

from tests.architecture._vocab import src_vocab_hits

# rel-path (posix, under src/) -> set of faction tokens permitted in that file.
LEDGER: dict[str, set[str]] = {
    # --- LEGIT: maps external BattleScribe faction labels to internal slugs ---
    "gameObjects/roszImporter.py": {"adeptus", "custodes", "necrons", "ork", "orks"},
    # --- LEGIT: Python typing.Protocol (structural type), collides with the seed word ---
    "gameMechanic/phaseHandler.py": {"protocol"},
    # --- LEGIT: get_active_protocol_effects — generic helper for any round_choice faction;
    #     'protocol' here is the round_choice concept (Command Protocols, Ka'tah, …),
    #     not a Necron-specific string. Function name, not a faction decision. ---
    "gameMechanic/abilityEngine.py": {"protocol"},
}


def _hits_by_file() -> dict[str, set[str]]:
    by_file: dict[str, set[str]] = defaultdict(set)
    for rel, _lineno, token, _faction in src_vocab_hits():
        by_file[rel].add(token)
    return by_file


def test_no_unledgered_faction_vocab_in_src() -> None:
    by_file = _hits_by_file()
    new = []
    for rel, tokens in sorted(by_file.items()):
        unlisted = tokens - LEDGER.get(rel, set())
        for token in sorted(unlisted):
            new.append(f"{rel}: {token!r}")
    assert not new, (
        "New faction vocabulary in src/ (Generic-src rule INV-4b). Move the "
        "decision into the YAML data layer, or — if legitimate I/O normalisation "
        "— add it to LEDGER with a reason:\n" + "\n".join(new)
    )


def test_ledger_has_no_stale_entries() -> None:
    by_file = _hits_by_file()
    stale = []
    for rel, tokens in sorted(LEDGER.items()):
        gone = tokens - by_file.get(rel, set())
        for token in sorted(gone):
            stale.append(f"{rel}: {token!r}")
    assert not stale, (
        "LEDGER lists faction tokens that no longer leak — the debt was cleaned. "
        "Remove these entries to ratchet the guard tighter:\n" + "\n".join(stale)
    )
