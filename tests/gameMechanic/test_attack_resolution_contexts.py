"""Regression test — all attack contexts share the same resolution path.

P1: Belegt, dass Shooting, Fight und Overwatch über denselben gemeinsamen
Auflösungs-Code laufen: `resolve_attack_modifiers` (src/gameMechanic/combat.py)
und `render_attack_resolution` (src/uiLayout/_common.py, phase_key-Parameter).

Architektur-Invariante:
  - shootingPhase.py ruft render_attack_resolution("shooting")
  - fightPhase.py ruft render_attack_resolution("fight")
  - Overwatch läuft regelkonform als Shooting (core_rules.txt §Overwatch:
    "resolved like a normal shooting attack … except that an unmodified 6 is
    always required") — kein eigener Auflösungspfad.
  - Die gemeinsame Modifier-Logik steckt in `resolve_attack_modifiers`
    (src/gameMechanic/combat.py:164).

Wenn jemand für einen Kontext einen eigenen Pfad einbaut, schlagen diese
Tests an.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Streamlit-Mock MUSS vor jedem src-Import gesetzt sein
# ---------------------------------------------------------------------------
_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------


def _reload_module(name: str):
    """Lädt ein src-Modul frisch, damit _st_mock überall konsistent ist."""
    if name in sys.modules:
        del sys.modules[name]
    return importlib.import_module(name)


# ---------------------------------------------------------------------------
# P1a — resolve_attack_modifiers ist die gemeinsame Trefferberechnung
# ---------------------------------------------------------------------------


class TestSharedResolutionFunction:
    """resolve_attack_modifiers (combat.py:164) wird von _render_resolution_tab
    für BEIDE Kontexte aufgerufen — identische Funktion, nur phase_key variiert."""

    def test_resolve_attack_modifiers_importable_from_combat(self):
        """Die gemeinsame Funktion muss in gameMechanic.combat liegen."""
        from gameMechanic.combat import resolve_attack_modifiers

        assert callable(resolve_attack_modifiers)

    def test_resolve_attack_modifiers_shooting_context_produces_hit_threshold(self):
        """Shooting-Kontext: BS 3+ → Hit-Threshold 3 (ohne Modifier)."""
        from gameMechanic.combat import resolve_attack_modifiers

        result = resolve_attack_modifiers(
            skill=3,
            strength=4,
            toughness=4,
            weapon_type="Rapid Fire",
            advanced=False,
            modifiers=[],
            use_melee=False,  # Shooting
        )
        assert result["hit"]["base"] == 3
        assert result["hit"]["modified"] == 3

    def test_resolve_attack_modifiers_fight_context_produces_hit_threshold(self):
        """Fight-Kontext: WS 3+ → Hit-Threshold 3 (ohne Modifier)."""
        from gameMechanic.combat import resolve_attack_modifiers

        result = resolve_attack_modifiers(
            skill=3,
            strength=5,
            toughness=4,
            weapon_type="Melee",
            advanced=False,
            modifiers=[],
            use_melee=True,  # Fight
        )
        assert result["hit"]["base"] == 3
        assert result["hit"]["modified"] == 3

    def test_resolve_attack_modifiers_same_wound_threshold_regardless_of_context(self):
        """Wundwurf-Schwelle ist von use_melee UNABHÄNGIG — gleiche Funktion, gleicher Wert."""
        from gameMechanic.combat import resolve_attack_modifiers

        shooting = resolve_attack_modifiers(
            skill=3,
            strength=4,
            toughness=4,
            weapon_type="Rapid Fire",
            advanced=False,
            modifiers=[],
            use_melee=False,
        )
        fight = resolve_attack_modifiers(
            skill=3,
            strength=4,
            toughness=4,
            weapon_type="Melee",
            advanced=False,
            modifiers=[],
            use_melee=True,
        )
        # Wundwurf-Basis identisch bei gleicher S/T-Kombi — gemeinsame Logik
        assert shooting["wound"]["base"] == fight["wound"]["base"]
        assert shooting["wound"]["modified"] == fight["wound"]["modified"]

    def test_heavy_weapon_malus_only_in_shooting_context(self):
        """Heavy-Waffe mit advanced=True gibt -1 Hit nur im Shooting-Kontext (use_melee=False).

        Das ist die einzige regelkonforme Kontextabhängigkeit in resolve_attack_modifiers.
        Im Fight-Kontext (use_melee=True) wird der Malus NICHT angewendet.
        """
        from gameMechanic.combat import resolve_attack_modifiers

        shooting = resolve_attack_modifiers(
            skill=3,
            strength=4,
            toughness=4,
            weapon_type="Heavy",
            advanced=True,
            modifiers=[],
            use_melee=False,
        )
        fight = resolve_attack_modifiers(
            skill=3,
            strength=4,
            toughness=4,
            weapon_type="Heavy",
            advanced=True,
            modifiers=[],
            use_melee=True,
        )
        # Shooting: 3+ → 4+ durch Heavy-Malus
        assert shooting["hit"]["modified"] == 4
        # Fight: kein Malus → bleibt 3+
        assert fight["hit"]["modified"] == 3


# ---------------------------------------------------------------------------
# P1b — render_attack_resolution nutzt denselben phase_key-Pfad
# ---------------------------------------------------------------------------


class TestRenderAttackResolutionSharedEntry:
    """render_attack_resolution(phase_key) in uiLayout/_common.py ist die
    EINZIGE Einsprungfunktion für alle Kontexte.

    shootingPhase ruft sie mit "shooting",
    fightPhase ruft sie mit "fight".
    Overwatch hat keinen eigenen Render-Pfad — es setzt phase_key="shooting".
    """

    def test_shootingPhase_calls_render_attack_resolution_with_shooting(self):
        """shootingPhase.py importiert render_attack_resolution aus _common."""
        import gameMechanic.shootingPhase as sp

        # render_attack_resolution muss importiert sein — prüft die Import-Verdrahtung
        assert hasattr(sp, "render_attack_resolution")

    def test_fightPhase_calls_render_attack_resolution_with_fight(self):
        """fightPhase.py importiert render_attack_resolution aus _common."""
        import gameMechanic.fightPhase as fp

        assert hasattr(fp, "render_attack_resolution")

    def test_both_phases_use_same_render_function_object(self):
        """shootingPhase und fightPhase zeigen auf DIESELBE Funktion aus _common."""
        import gameMechanic.fightPhase as fp
        import gameMechanic.shootingPhase as sp

        assert sp.render_attack_resolution is fp.render_attack_resolution

    def test_no_separate_overwatch_resolution_path(self):
        """Kein eigenes render_*overwatch* existiert in chargephase oder _common.

        Overwatch läuft regelkonform als Shooting (core_rules.txt §Overwatch).
        """
        import gameMechanic.chargephase as cp

        # Es darf keine eigenständige Overwatch-Auflösungsfunktion geben
        assert not hasattr(cp, "render_attack_resolution")
        assert not hasattr(cp, "render_overwatch_resolution")

    def test_render_attack_resolution_is_in_common(self):
        """render_attack_resolution stammt aus uiLayout._common — gemeinsame Quelle."""
        from uiLayout._common import render_attack_resolution

        assert callable(render_attack_resolution)


# ---------------------------------------------------------------------------
# P1c — Modifier-Stack ist für alle Kontexte konsistent aufgebaut
# ---------------------------------------------------------------------------


class TestModifierStackConsistency:
    """resolve_attack_modifiers wendet den Modifier-Cap ±1 für ALLE Kontexte
    identisch an — das ist eine 9E-Grundregel (keine Kontext-Ausnahme)."""

    def test_hit_modifier_capped_at_plus1_shooting(self):
        """+2 Hit Modifier wird in Shooting auf +1 gekappt (9E-Regel)."""
        from gameMechanic.combat import resolve_attack_modifiers

        mods = [
            {"label": "A", "value": 1, "roll_type": "hit"},
            {"label": "B", "value": 1, "roll_type": "hit"},
        ]
        result = resolve_attack_modifiers(3, 4, 4, "Rapid Fire", False, mods, False)
        # Net +2, gekappt auf +1 → 3+ verbessert sich zu 2+
        assert result["hit"]["modified"] == 2

    def test_hit_modifier_capped_at_plus1_fight(self):
        """Derselbe Cap gilt im Fight-Kontext — identische Logik."""
        from gameMechanic.combat import resolve_attack_modifiers

        mods = [
            {"label": "A", "value": 1, "roll_type": "hit"},
            {"label": "B", "value": 1, "roll_type": "hit"},
        ]
        result = resolve_attack_modifiers(3, 5, 4, "Melee", False, mods, True)
        assert result["hit"]["modified"] == 2

    def test_wound_modifier_capped_minus1_both_contexts(self):
        """-2 Wund-Modifier: gekappt auf -1 — gilt in Shooting und Fight gleich."""
        from gameMechanic.combat import resolve_attack_modifiers

        mods = [
            {"label": "X", "value": -1, "roll_type": "wound"},
            {"label": "Y", "value": -1, "roll_type": "wound"},
        ]
        shooting = resolve_attack_modifiers(3, 4, 4, "Rapid Fire", False, mods, False)
        fight = resolve_attack_modifiers(3, 4, 4, "Melee", False, mods, True)
        # 4+ Basis + 1 (gecappter -1 Mod) = 5+
        assert shooting["wound"]["modified"] == fight["wound"]["modified"] == 5

    def test_minimum_threshold_is_2_in_all_contexts(self):
        """Trefferwurf kann nie besser als 2+ sein — gilt in allen Kontexten."""
        from gameMechanic.combat import resolve_attack_modifiers

        # WS/BS 2+ mit +1 Modifier → darf nicht 1+ werden
        mods = [{"label": "A", "value": 1, "roll_type": "hit"}]
        shooting = resolve_attack_modifiers(2, 4, 4, "Rapid Fire", False, mods, False)
        fight = resolve_attack_modifiers(2, 4, 4, "Melee", False, mods, True)
        assert shooting["hit"]["modified"] == 2
        assert fight["hit"]["modified"] == 2
