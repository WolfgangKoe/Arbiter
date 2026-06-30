"""Tests — YAML-Stratagems tragen gültige phase/stage-Werte (P4).

Prüft, dass alle Stratagems in den YAML-Dateien für Necrons, Orks und
Adeptus Custodes nur erlaubte Werte in den Feldern `phase`, `stage` und
`player` tragen.

Erlaubte Werte (aus gameObjects/stratagem.py + game_state.py):
  phase:  "command" | "movement" | "psychic" | "shooting" | "charge" |
          "fight" | "morale" | "before_battle" | "any" | list[str] (Kombination)
  stage:  "start" | "active" | "end"
  player: "active" | "inactive" | "both"

Getestete Produktiv-Funktion:
  - load_stratagems (src/gameObjects/loader.py:590) — lädt und parst die YAML-Daten.

Wenn ein Redakteur einen unbekannten phase-Wert einträgt (Tipp-Fehler, neue Phase
ohne Rücksprache), schlägt dieser Test an, bevor der Fehler im Spiel sichtbar wird.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# ---------------------------------------------------------------------------
# Streamlit-Mock vor allen src-Imports
# ---------------------------------------------------------------------------
_st_mock = MagicMock()
sys.modules.setdefault("streamlit", _st_mock)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gameObjects.loader import load_stratagems  # noqa: E402

# ---------------------------------------------------------------------------
# Erlaubte Werte (kanonisch — aus game_state.PHASES + stratagem.py Literals)
# ---------------------------------------------------------------------------

VALID_PHASES = frozenset(
    {
        "command",
        "movement",
        "psychic",
        "shooting",
        "charge",
        "fight",
        "morale",
        "before_battle",
        "any",
        "setup",  # im PHASES-Register vorhanden, Vollständigkeit
    }
)

VALID_STAGES = frozenset({"start", "active", "end"})
VALID_PLAYERS = frozenset({"active", "inactive", "both"})

FACTIONS = ["necrons", "orks", "adeptus_custodes", "_shared"]


# ---------------------------------------------------------------------------
# Hilfsfunktion: alle Stratagems aus allen Fraktionen laden
# ---------------------------------------------------------------------------


def _all_stratagems():
    seen_ids: set[str] = set()
    result = []
    for faction in FACTIONS:
        for s in load_stratagems(faction):
            if s.id not in seen_ids:
                seen_ids.add(s.id)
                result.append(s)
    return result


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestStratagemsHaveValidPhase:
    """Alle phase-Werte in den YAML-Stratagems müssen in VALID_PHASES liegen."""

    def test_no_stratagem_has_unknown_phase(self):
        """Kein Stratagem trägt einen unbekannten phase-Wert.

        list-Werte (z.B. [shooting, fight]) werden elementweise geprüft.
        """
        bad: list[tuple[str, object]] = []
        for s in _all_stratagems():
            phases = s.phase if isinstance(s.phase, list) else [s.phase]
            for ph in phases:
                # YAML-Kommentare landen nicht im geparsten Wert — nur den reinen String prüfen
                ph_clean = str(ph).split()[0].strip()
                if ph_clean not in VALID_PHASES:
                    bad.append((s.id, ph_clean))
        assert bad == [], f"Ungültige phase-Werte gefunden: {bad}"

    def test_stratagem_phase_is_string_or_list(self):
        """phase muss str oder list[str] sein — kein int, kein None."""
        bad: list[tuple[str, object]] = []
        for s in _all_stratagems():
            if not isinstance(s.phase, str | list):
                bad.append((s.id, type(s.phase).__name__))
        assert bad == [], f"Falscher Typ für phase: {bad}"

    @pytest.mark.parametrize("faction", FACTIONS)
    def test_faction_stratagems_have_valid_phases(self, faction: str):
        """Jede Fraktion einzeln: alle phase-Werte valide."""
        bad: list[tuple[str, str]] = []
        for s in load_stratagems(faction):
            phases = s.phase if isinstance(s.phase, list) else [s.phase]
            for ph in phases:
                ph_clean = str(ph).split()[0].strip()
                if ph_clean not in VALID_PHASES:
                    bad.append((s.id, ph_clean))
        assert bad == [], f"Ungültige phase-Werte in {faction}: {bad}"


class TestStratagemsHaveValidStage:
    """Alle stage-Werte in den YAML-Stratagems müssen 'start', 'active' oder 'end' sein."""

    def test_no_stratagem_has_unknown_stage(self):
        """Kein Stratagem trägt einen unbekannten stage-Wert."""
        bad: list[tuple[str, str]] = []
        for s in _all_stratagems():
            stage_clean = str(s.stage).split()[0].strip()
            if stage_clean not in VALID_STAGES:
                bad.append((s.id, stage_clean))
        assert bad == [], f"Ungültige stage-Werte gefunden: {bad}"

    @pytest.mark.parametrize("faction", FACTIONS)
    def test_faction_stratagems_have_valid_stages(self, faction: str):
        """Jede Fraktion einzeln: alle stage-Werte valide."""
        bad: list[tuple[str, str]] = []
        for s in load_stratagems(faction):
            stage_clean = str(s.stage).split()[0].strip()
            if stage_clean not in VALID_STAGES:
                bad.append((s.id, stage_clean))
        assert bad == [], f"Ungültige stage-Werte in {faction}: {bad}"


class TestStratagemsHaveValidPlayer:
    """Alle player-Werte in den YAML-Stratagems müssen 'active', 'inactive' oder 'both' sein."""

    def test_no_stratagem_has_unknown_player(self):
        """Kein Stratagem trägt einen unbekannten player-Wert."""
        bad: list[tuple[str, str]] = []
        for s in _all_stratagems():
            if s.player not in VALID_PLAYERS:
                bad.append((s.id, s.player))
        assert bad == [], f"Ungültige player-Werte gefunden: {bad}"


class TestStratagems_PhaseStage_Kombinations_Plausibility:
    """Plausibilitäts-Checks für phase/stage-Kombinationen.

    Nicht alle Kombinationen sind regelkonform — diese Tests prüfen die
    häufigsten Unplausibilitäten, ohne alle 9E-Regeln erschöpfend zu kodieren.
    """

    def test_before_battle_stratagems_have_no_end_stage(self):
        """Vor-dem-Spiel-Stratagems (before_battle) sollten nicht stage=end tragen.

        Diese Phase hat kein 'end'-Fenster im regulären Spielablauf.
        """
        suspect: list[str] = []
        for s in _all_stratagems():
            phases = s.phase if isinstance(s.phase, list) else [s.phase]
            if "before_battle" in phases and s.stage == "end":
                suspect.append(s.id)
        assert suspect == [], f"before_battle + stage=end ist unplausibel: {suspect}"

    def test_all_stratagems_have_nonempty_id(self):
        """Alle Stratagems haben eine nicht-leere ID (Lade-Sanity-Check)."""
        bad = [s.id for s in _all_stratagems() if not s.id or not s.id.strip()]
        assert bad == [], f"Stratagems ohne ID: {bad}"

    def test_all_stratagems_have_cp_cost_zero_or_positive(self):
        """CP-Kosten sind niemals negativ."""
        bad = [(s.id, s.cp_cost) for s in _all_stratagems() if s.cp_cost < 0]
        assert bad == [], f"Stratagems mit negativen CP-Kosten: {bad}"
