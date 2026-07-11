"""YAML data-quality guard — catches silently truncated rule text.

S137/S138 fand 44 abilities/rule_text-Felder, die von einem inzwischen
gefixten Scraper-Bug (tools/wahapedia_scraper.py, behoben in Commit
4dcc560) bei exakt 55 Zeichen mitten im Wort abgeschnitten worden waren
(z.B. "...it makes 2 additional atta" statt "...attacks..."). Die
betroffenen YAML-Dateien wurden nie neu gescraped, daher blieb der
Schaden nach dem Scraper-Fix bestehen. Dieser Test verhindert ein
Wiederauftreten unabhängig von Netzzugriff (reine YAML-Prüfung).

Konvention in diesem Codebase (siehe docs/handoff/S137_yaml_trunkierung_scan.md):
abilities/rule_text sind entweder leer oder vollständige Sätze, die auf
Interpunktion enden. Kurze Stichwort-Tags (z.B. "Blast") sind erlaubt und
bleiben unter der Mindestlänge. `active_text`-Felder (kurze Badge-Zusammen-
fassungen, z.B. "+1 Strength · +1 Attacks · 5+ invuln") folgen einer
eigenen Stil-Konvention und sind bewusst ausgenommen.
"""

from __future__ import annotations

import glob
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Ensure src/ is on the path — tests/gameObjects/conftest.py's autouse fixture
# imports gameObjects.loader at setup time and needs this when the file runs
# standalone (matches the convention in test_loader.py).
sys.path.insert(0, str(PROJECT_ROOT / "src"))

DATA_GLOB = str(PROJECT_ROOT / "data" / "wh40k_9e" / "**" / "*.yaml")

# Ability/rule text below this length is exempt (short keyword tags like
# "Blast" or "1×/game only." never trip the scraper truncation bug, whose
# signature was a hard cutoff at 54–55 characters).
MIN_SUSPECT_LENGTH = 20

# A complete sentence/phrase ends in one of these; anything else at
# MIN_SUSPECT_LENGTH+ is a truncation candidate.
TERMINAL_CHARS = (".", "!", "?", '"', "'")

TARGET_KEYS = {"abilities", "rule_text"}


def _walk(obj: Any, path: str = "") -> Iterator[tuple[str, str]]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from _walk(value, f"{path}.{key}" if path else key)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from _walk(value, f"{path}[{index}]")
    elif isinstance(obj, str):
        yield path, obj


def _suspiciously_truncated_fields() -> list[tuple[str, str, str]]:
    hits: list[tuple[str, str, str]] = []
    for file_path in sorted(glob.glob(DATA_GLOB, recursive=True)):
        data = yaml.safe_load(open(file_path, encoding="utf-8"))
        if not data:
            continue
        for field_path, raw_value in _walk(data):
            key = field_path.rsplit(".", 1)[-1].split("[")[0]
            if key not in TARGET_KEYS:
                continue
            value = raw_value.strip()
            if len(value) < MIN_SUSPECT_LENGTH:
                continue
            if value.endswith(TERMINAL_CHARS):
                continue
            hits.append((file_path, field_path, value))
    return hits


def test_no_abilities_or_rule_text_field_is_truncated() -> None:
    """abilities/rule_text fields must be empty, a short tag, or a full sentence.

    Regression guard for the S137 scraper-truncation bug (44 fields cut off
    at exactly 55 characters). Fails loud with file/field/value so any new
    truncated import is caught before it reaches YAML.
    """
    hits = _suspiciously_truncated_fields()
    assert not hits, "Truncated abilities/rule_text fields found:\n" + "\n".join(
        f"  {fp} :: {path} :: {value!r}" for fp, path, value in hits
    )
