"""Harvest faction-discriminating vocabulary from the YAML data layer.

Powers the data-driven Generic-src guard (INV-4b): a word that is unique to one
faction's data — a proper noun like 'overlord', 'waaagh', 'szarekhan', or a
faction name — must not appear in src/ identifiers or string values. The
vocabulary is *derived from the database*, so adding a faction automatically
extends the guard; nothing is hand-maintained except the small STOPWORDS set and
the per-file debt ledger.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import yaml

_ROOT = Path(__file__).resolve().parents[2]
_DATA = _ROOT / "data"
_SRC = _ROOT / "src"

# A token is an alphabetic run of length >= 3, lowercased. snake_case and
# CamelCase identifiers are split first so 'pending_camelCase' -> {pending, camel, case}.
_WORD = re.compile(r"[a-z]{3,}")
_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")

# Short faction tokens (< 3 chars or that collide with English) handled explicitly.
_ALWAYS_FACTION = {"ork": "orks", "orks": "orks"}

# Generic vocabulary that happens to be faction-unique in the data but is NOT a
# faction marker (rules terms, common English, shared structure words). Keep tight
# and justified — every entry here is a word the guard will deliberately ignore.
STOPWORDS: frozenset[str] = frozenset(
    {
        # --- generic English riding in on id/stratagem segments ---
        "the",
        "and",
        "with",
        "per",
        "all",
        "any",
        "one",
        "two",
        "until",
        "each",
        "this",
        "that",
        "from",
        "into",
        "your",
        "they",
        "their",
        "when",
        "then",
        "are",
        "but",
        "for",
        "than",
        "will",
        "off",
        "old",
        "down",
        "back",
        "out",
        "get",
        "call",
        "show",
        "hide",
        "done",
        "close",
        "deny",
        "change",
        "chosen",
        "best",
        "auto",
        "self",
        "field",
        "form",
        "force",
        "pair",
        "option",
        "multi",
        "extra",
        "number",
        "light",
        "lost",
        "shared",
        "special",
        "style",
        "variant",
        "rapid",
        "right",
        "feel",
        "pain",
        "body",
        "cap",
        "repair",
        "bad",
        "schema",
        # CSS colour names (constants/colors.py), not faction words
        "blue",
        "red",
        "green",
        # generic architecture term that deliberately REPLACES faction vocabulary
        "subfaction",
        # --- core-rules / generic 40k vocabulary (appears across factions) ---
        "roll",
        "rolls",
        "hit",
        "wound",
        "save",
        "saving",
        "throws",
        "model",
        "models",
        "unit",
        "units",
        "phase",
        "turn",
        "attack",
        "attacks",
        "range",
        "melee",
        "ranged",
        "damage",
        "strength",
        "move",
        "advance",
        "charge",
        "fight",
        "morale",
        "command",
        "stratagem",
        "ability",
        "weapon",
        "weapons",
        "keyword",
        "keywords",
        "core",
        "rule",
        "rules",
        "primary",
        "secondary",
        "improve",
        "reroll",
        "bonus",
        "modifier",
        "leadership",
        "objective",
        "armour",
        "heroic",
        "intervention",
        "overwatch",
        "patrol",
        "onslaught",
        "shooting",
        "warp",
        "psyker",
        "witch",
        "perils",
        "glory",
        "sweep",
        "combat",
        "fire",
        "power",
        "stage",
        "strike",
        "smite",
        "patrol",
        # --- generic weapon descriptors used by several factions ---
        "spear",
        "sword",
        "blade",
        "guard",
        "boss",
        "nob",
    }
)


def _tokens(text: str) -> set[str]:
    spaced = _CAMEL.sub(" ", text)
    return set(_WORD.findall(spaced.lower()))


# Machine identifiers (id segments) + keywords + subfaction tags carry faction
# proper nouns ('overlord', 'klaw', 'szarekhan') while structural segments
# ('unit', 'weapon', 'faction') appear in every faction and self-cancel. Prose
# fields (name_en, rule_text) are deliberately EXCLUDED — they are generic
# English and would flood the vocabulary with false positives.
NAME_KEYS: frozenset[str] = frozenset(
    {
        "id",
        "keywords",
        "faction",
        "subfaction",
        "subfaction_affinity",
        "dynasty",
        "clan",
        "shield_host",
    }
)

# Faction concept-words that are real faction vocabulary but may not appear in
# id/keyword data (they live in prose). Seed them explicitly so the guard still
# catches them in src/. Extend this list to make the guard stricter.
FACTION_CONCEPT_SEEDS: dict[str, str] = {
    "dynasty": "necrons",
    "dynastic": "necrons",
    "reanimation": "necrons",
    "protocol": "necrons",
    "protocols": "necrons",
    "waaagh": "orks",
    "kultur": "orks",
    "katah": "adeptus_custodes",
    "shield": "adeptus_custodes",
}


def _harvest(obj: object, under_name_key: bool = False) -> set[str]:
    """Tokens from strings that sit under a NAME_KEYS field (proper nouns only)."""
    toks: set[str] = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            toks |= _harvest(value, under_name_key or str(key) in NAME_KEYS)
    elif isinstance(obj, list):
        for value in obj:
            toks |= _harvest(value, under_name_key)
    elif isinstance(obj, str) and under_name_key:
        toks |= _tokens(obj)
    return toks


def _faction_dirs() -> list[str]:
    # Skip non-faction helper dirs like '_schema' (templates, not a faction).
    return sorted(
        p.name for p in (_DATA / "wh40k_9e").iterdir() if p.is_dir() and not p.name.startswith("_")
    )


def faction_tokens() -> dict[str, set[str]]:
    """faction_dir -> proper-noun tokens from name/id fields of that faction's data."""
    result: dict[str, set[str]] = {}
    for fdir in _faction_dirs():
        toks: set[str] = set(_tokens(fdir))
        for yml in (_DATA / "wh40k_9e" / fdir).rglob("*.yaml"):
            data = yaml.safe_load(yml.read_text(encoding="utf-8"))
            toks |= _harvest(data)
        result[fdir] = toks
    for yml in (_DATA / "rosters").glob("*.yaml"):
        data = yaml.safe_load(yml.read_text(encoding="utf-8"))
        fdir = (data or {}).get("faction_dir")
        if fdir in result:
            result[fdir] |= _harvest(data)
    return result


def discriminating_vocab() -> dict[str, str]:
    """token -> faction_dir, for tokens unique to exactly one faction (minus stopwords)."""
    tokens = faction_tokens()
    owners: dict[str, set[str]] = {}
    for fdir, toks in tokens.items():
        for tok in toks:
            owners.setdefault(tok, set()).add(fdir)
    vocab: dict[str, str] = {}
    for tok, fdirs in owners.items():
        if len(fdirs) == 1 and tok not in STOPWORDS:
            vocab[tok] = next(iter(fdirs))
    vocab.update(FACTION_CONCEPT_SEEDS)
    vocab.update(_ALWAYS_FACTION)
    return vocab


def _identifier_tokens(tree: ast.Module) -> list[tuple[str, int]]:
    """(token, lineno) for every identifier token used in a module."""
    out: list[tuple[str, int]] = []

    def add(name: str, lineno: int) -> None:
        for tok in _tokens(_CAMEL.sub(" ", name).replace("_", " ")):
            out.append((tok, lineno))

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            add(node.id, node.lineno)
        elif isinstance(node, ast.Attribute):
            add(node.attr, node.lineno)
        elif isinstance(node, ast.arg):
            add(node.arg, node.lineno)
        elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            add(node.name, node.lineno)
        elif isinstance(node, ast.keyword) and node.arg:
            add(node.arg, node.lineno)
    return out


def src_vocab_hits() -> list[tuple[str, int, str, str]]:
    """(rel_path, lineno, token, faction_dir) for every faction word leaking into src/.

    Scans identifiers AND non-docstring string constants. Docstrings/comments are
    documentation and are exempt.
    """
    from tests.architecture._arch import docstring_node_ids

    vocab = discriminating_vocab()
    hits: list[tuple[str, int, str, str]] = []
    for path in sorted(p for p in _SRC.rglob("*.py") if "__pycache__" not in p.parts):
        rel = path.relative_to(_SRC).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        skip = docstring_node_ids(tree)
        for tok, lineno in _identifier_tokens(tree):
            if tok in vocab:
                hits.append((rel, lineno, tok, vocab[tok]))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and id(node) not in skip
            ):
                for tok in _tokens(node.value):
                    if tok in vocab:
                        hits.append((rel, node.lineno, tok, vocab[tok]))
    return hits
