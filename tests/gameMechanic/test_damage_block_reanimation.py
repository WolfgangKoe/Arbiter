"""Tests für Damage-Block und Reanimation Protocols (RP) — P2.

Getestete Produktiv-Funktionen:
  - apply_damage_attacks   (src/gameMechanic/combat.py:264)
  - apply_damage           (src/gameMechanic/unit_mutations.py:166)
  - heal_unit              (src/gameMechanic/unit_mutations.py:259)
  - get_active_rp_modifiers (src/gameMechanic/ability_engine.py:324)

RP-Spielregel (Wahapedia core_rules + Necron-YAML):
  - Gate ist datengetrieben (S128 Option B): _render_rp_block fragt
    get_after_attack_revive_ability (ability_engine) — die YAML-Fähigkeit
    (effect.type reanimate, conditions.has_rules reanimationProtocols)
    entscheidet, welche Einheiten triggern.
  - Würfelanzahl = models_lost × unit.wounds (amount: D6_per_wound aus YAML).
  - Erfolg auf 5+ (effect.success_on aus YAML; User zählt Erfolge, gibt models_back ein).
  - RP wird über heal_unit angewendet: hp = models_back × unit.wounds.
  - Rückkehrende Modelle reduzieren lost_models_this_turn (9E: zählen nicht als
    gefallen für Moraltest).
  - rp_reroll-Flag aus dem aktiven Protokoll wird von get_active_rp_modifiers
    geliefert (ability_engine.py:324).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Streamlit-Mock vor allen src-Imports
# ---------------------------------------------------------------------------
_st_mock = MagicMock()
sys.modules["streamlit"] = _st_mock
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import gameMechanic.game_state as _gs  # noqa: E402
import gameMechanic.unit_mutations as _mut  # noqa: E402
from gameMechanic.combat import apply_damage_attacks  # noqa: E402
from gameMechanic.unit_mutations import apply_damage, heal_unit  # noqa: E402
from gameObjects.unit import Unit  # noqa: E402

# ---------------------------------------------------------------------------
# Test-Infrastruktur (gekürzt aus test_unit_mutations.py-Muster)
# ---------------------------------------------------------------------------

WARRIORS_ID = "wh40k_9e.necrons.unit.warriors"
OVERLORD_ID = "wh40k_9e.necrons.unit.overlord"
BOYZ_ID = "wh40k_9e.orks.unit.boyz"


class _S(dict):
    """Einfaches dict, das auch Attributzugriff erlaubt (Streamlit-Session-Compat)."""

    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: object) -> None:
        self[key] = value


def _make_session(**kwargs) -> _S:
    kwargs.setdefault("first_player", "Necrons")
    kwargs.setdefault("second_player", "Orks")
    s = _S(**kwargs)
    _mut.st.session_state = s
    _gs.st.session_state = s
    return s


def _warriors_unit(models_max: int = 10, wounds: int = 1) -> Unit:
    """Necron Warriors: 1 Wound/Modell, reanimationProtocols in rules."""
    return Unit(
        id=WARRIORS_ID,
        name_en="Necron Warriors",
        name_de="Nekron-Krieger",
        faction="Necrons",
        subfaction=None,
        battlefield_role=["Troops"],
        keywords=["Necrons", "Core"],
        wounds=wounds,
        models_min=10,
        models_max=models_max,
        power_level=8,
        move='5"',
        bs="3+",
        ws="3+",
        strength=4,
        toughness=4,
        attacks=1,
        save=4,
        invuln_save=6,
        leadership=10,
        oc=2,
        fnp=None,
        rules={"reanimationProtocols": True},
    )


def _overlord_unit() -> Unit:
    """Overlord: 5 Wounds, kein RP."""
    return Unit(
        id=OVERLORD_ID,
        name_en="Overlord",
        name_de="Overlord",
        faction="Necrons",
        subfaction=None,
        battlefield_role=["HQ"],
        keywords=["Necrons"],
        wounds=5,
        models_min=1,
        models_max=1,
        power_level=6,
        move='6"',
        bs="3+",
        ws="3+",
        strength=5,
        toughness=5,
        attacks=4,
        save=3,
        invuln_save=4,
        leadership=10,
        oc=1,
        fnp=None,
    )


def _warrior_state(models: int = 10, current_wounds: int | None = None) -> dict:
    return {
        "current_wounds": current_wounds if current_wounds is not None else models,
        "models": models,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "normal",
        "lost_models_this_turn": 0,
        "movement_choice": None,
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
        },
    }


def _overlord_state(current_wounds: int = 5) -> dict:
    return {
        "current_wounds": current_wounds,
        "models": 1,
        "destroyed": False,
        "in_melee": False,
        "in_reserve": False,
        "deployment": "normal",
        "lost_models_this_turn": 0,
        "movement_choice": None,
        "melee_with": [],
        "turn_flags": {
            "advanced": False,
            "retreated": False,
            "charged": False,
            "shot": False,
            "fought": False,
        },
    }


# ---------------------------------------------------------------------------
# (a) Damage-Block: apply_damage_attacks — HP-Berechnung aus Eingaben
# ---------------------------------------------------------------------------


class TestApplyDamageAttacks:
    """apply_damage_attacks (combat.py:264) berechnet Gesamt-HP-Schaden aus den
    6d-v2-Eingaben: models_lost × wounds_per_model + wounds_on_front + mortal_wounds.
    """

    def test_models_lost_only_1wound_models(self):
        """3 gefallene 1-Wunden-Modelle → 3 HP Schaden."""
        assert apply_damage_attacks(3, 0, 0, 1) == 3

    def test_models_lost_multiwound(self):
        """2 gefallene 3-Wunden-Modelle → 6 HP."""
        assert apply_damage_attacks(2, 0, 0, 3) == 6

    def test_wounds_on_front_model_added(self):
        """1 gefallenes Modell + 2 Wunden auf dem Frontmodell (3 HP/Modell) → 5 HP."""
        assert apply_damage_attacks(1, 2, 0, 3) == 5

    def test_mortal_wounds_added_separately(self):
        """Mortalwunden werden direkt addiert, unabhängig von Modellverlusten."""
        assert apply_damage_attacks(0, 0, 4, 1) == 4

    def test_all_three_inputs_combined(self):
        """2 Modelle (3 HP) + 1 Frontwunde + 3 Mortalwunden = 10 HP."""
        assert apply_damage_attacks(2, 1, 3, 3) == 10

    def test_zero_inputs_return_zero(self):
        assert apply_damage_attacks(0, 0, 0, 1) == 0

    def test_wounds_on_front_with_no_models_lost(self):
        """Nur Frontwunden — kein Modell gefallen."""
        assert apply_damage_attacks(0, 3, 0, 5) == 3


# ---------------------------------------------------------------------------
# (b) Damage-Block: apply_damage — Modell-Verlust-Zählung
# ---------------------------------------------------------------------------


class TestApplyDamageModelTracking:
    """apply_damage (unit_mutations.py:166) trägt Modell-Verluste korrekt nach:
    lost_models_this_turn wird inkrementiert.
    """

    def test_3_damage_kills_3_warriors_of_1_wound(self):
        """3 HP Schaden auf 1-Wunden-Krieger tötet 3 Modelle."""
        unit = _warriors_unit()
        session = _make_session(
            p1_units={WARRIORS_ID: _warrior_state(models=10, current_wounds=10)},
            p2_units={},
            phase_idx=5,
            active="Necrons",
            round=1,
            cp={"Necrons": 4, "Orks": 4},
            selected_unit=None,
            selected_targets=[],
        )
        apply_damage(WARRIORS_ID, "Necrons", 3, unit, resolved=True)
        state = session["p1_units"][WARRIORS_ID]
        assert state["current_wounds"] == 7
        assert state["models"] == 7
        assert state["lost_models_this_turn"] == 3

    def test_damage_does_not_exceed_remaining_hp(self):
        """100 HP Schaden auf eine 5-LP-Einheit → zerstört, nicht negative HP."""
        unit = _overlord_unit()
        session = _make_session(
            p1_units={OVERLORD_ID: _overlord_state(current_wounds=5)},
            p2_units={},
            phase_idx=5,
            active="Necrons",
            round=1,
            cp={"Necrons": 4, "Orks": 4},
            selected_unit=None,
            selected_targets=[],
        )
        apply_damage(OVERLORD_ID, "Necrons", 100, unit, resolved=True)
        state = session["p1_units"][OVERLORD_ID]
        assert state["current_wounds"] == 0
        assert state["destroyed"] is True

    def test_partial_damage_kills_no_models_on_multiwound_unit(self):
        """1 HP Schaden auf einen 5-Wunden-Overlord → kein Modell gefallen."""
        unit = _overlord_unit()
        session = _make_session(
            p1_units={OVERLORD_ID: _overlord_state(current_wounds=5)},
            p2_units={},
            phase_idx=5,
            active="Necrons",
            round=1,
            cp={"Necrons": 4, "Orks": 4},
            selected_unit=None,
            selected_targets=[],
        )
        apply_damage(OVERLORD_ID, "Necrons", 1, unit, resolved=True)
        state = session["p1_units"][OVERLORD_ID]
        assert state["current_wounds"] == 4
        assert state["models"] == 1
        assert state["lost_models_this_turn"] == 0

    def test_frontmodel_cap_applies_without_resolved_flag(self):
        """Ohne resolved=True wird Schaden auf das Frontmodell begrenzt (9E-Regel)."""
        unit = _warriors_unit(models_max=10, wounds=1)
        session = _make_session(
            p1_units={WARRIORS_ID: _warrior_state(models=10, current_wounds=10)},
            p2_units={},
            phase_idx=5,
            active="Necrons",
            round=1,
            cp={"Necrons": 4, "Orks": 4},
            selected_unit=None,
            selected_targets=[],
        )
        # Ohne resolved: Einzelschlag kann nur das Frontmodell (1 HP) töten
        apply_damage(WARRIORS_ID, "Necrons", 5, unit, resolved=False)
        state = session["p1_units"][WARRIORS_ID]
        # Nur 1 Modell verloren (Frontmodell-Cap bei 1-Wunden-Modellen)
        assert state["current_wounds"] == 9
        assert state["models"] == 9


# ---------------------------------------------------------------------------
# (c) RP-Regel: heal_unit gibt Modelle zurück, reduziert lost_models_this_turn
# ---------------------------------------------------------------------------


class TestHealUnitReanimationProtocols:
    """heal_unit (unit_mutations.py:259) modelliert den RP-Apply-Schritt.

    In _render_rp_block (_common.py:590):
        heal_unit(def_uid, def_faction, models_back * def_unit.wounds, def_unit)

    Hier wird heal_unit direkt getestet — analog zu dem, was _render_rp_block auslöst.
    """

    def test_rp_restores_models_after_damage(self):
        """Nach RP: 3 Modelle zurück → models und current_wounds erhöht."""
        unit = _warriors_unit()
        session = _make_session(
            p1_units={
                WARRIORS_ID: _warrior_state(models=7, current_wounds=7)
                | {"lost_models_this_turn": 3}
            },
            p2_units={},
            phase_idx=5,
            active="Necrons",
            round=1,
            cp={"Necrons": 4, "Orks": 4},
            selected_unit=None,
            selected_targets=[],
        )
        # models_back=3, wounds=1 → hp = 3×1 = 3
        heal_unit(WARRIORS_ID, "Necrons", 3 * unit.wounds, unit)
        state = session["p1_units"][WARRIORS_ID]
        assert state["models"] == 10
        assert state["current_wounds"] == 10

    def test_rp_reduces_lost_models_this_turn(self):
        """Zurückgekehrte Modelle zählen nicht mehr als gefallen (9E-Moralregel)."""
        unit = _warriors_unit()
        session = _make_session(
            p1_units={
                WARRIORS_ID: _warrior_state(models=7, current_wounds=7)
                | {"lost_models_this_turn": 3}
            },
            p2_units={},
            phase_idx=5,
            active="Necrons",
            round=1,
            cp={"Necrons": 4, "Orks": 4},
            selected_unit=None,
            selected_targets=[],
        )
        heal_unit(WARRIORS_ID, "Necrons", 3 * unit.wounds, unit)
        state = session["p1_units"][WARRIORS_ID]
        # Alle 3 zurückgekehrt → lost_models_this_turn = 0
        assert state["lost_models_this_turn"] == 0

    def test_rp_partial_return_reduces_lost_models_partially(self):
        """Nur 1 von 3 Modellen kehrt zurück → lost_models_this_turn = 2."""
        unit = _warriors_unit()
        session = _make_session(
            p1_units={
                WARRIORS_ID: _warrior_state(models=7, current_wounds=7)
                | {"lost_models_this_turn": 3}
            },
            p2_units={},
            phase_idx=5,
            active="Necrons",
            round=1,
            cp={"Necrons": 4, "Orks": 4},
            selected_unit=None,
            selected_targets=[],
        )
        heal_unit(WARRIORS_ID, "Necrons", 1 * unit.wounds, unit)
        state = session["p1_units"][WARRIORS_ID]
        assert state["models"] == 8
        assert state["lost_models_this_turn"] == 2

    def test_rp_caps_at_unit_max_models(self):
        """RP kann nicht mehr Modelle zurückbringen als das Max (models_max)."""
        unit = _warriors_unit(models_max=10)
        session = _make_session(
            p1_units={
                WARRIORS_ID: _warrior_state(models=9, current_wounds=9)
                | {"lost_models_this_turn": 1}
            },
            p2_units={},
            phase_idx=5,
            active="Necrons",
            round=1,
            cp={"Necrons": 4, "Orks": 4},
            selected_unit=None,
            selected_targets=[],
        )
        # Versuche 5 Modelle zurückzubringen, obwohl nur 1 fehlt
        heal_unit(WARRIORS_ID, "Necrons", 5 * unit.wounds, unit)
        state = session["p1_units"][WARRIORS_ID]
        assert state["models"] == 10
        assert state["current_wounds"] == 10

    def test_rp_dice_count_equals_models_lost_times_wounds(self):
        """RP-Würfelanzahl: models_lost × unit.wounds — die Formel kommt jetzt
        aus revive_dice_count (ability_engine, amount: D6_per_wound aus YAML)."""
        from gameMechanic.ability_engine import revive_dice_count

        assert revive_dice_count("D6_per_wound", 4, 2) == 8  # 4 × 2 = 8 Würfel

    def test_rp_not_triggered_for_unit_without_reanimation_protocols(self):
        """Overlord (kein reanimationProtocols) bekommt keine RP-Auslösung.

        Das Produkt-Gate ist datengetrieben (S128 Option B): _render_rp_block →
        get_after_attack_revive_ability; die YAML-Condition has_rules
        [reanimationProtocols] schlägt für Nicht-RP-Einheiten fehl (Gate-Tests:
        test_ability_engine.py::test_revive_ability_*).
        """
        overlord = _overlord_unit()
        # Overlord hat kein reanimationProtocols in rules
        assert "reanimationProtocols" not in overlord.rules

    def test_warriors_have_reanimation_protocols_rule(self):
        """Warriors tragen reanimationProtocols in ihrer rules-Liste — die
        YAML-Condition des datengetriebenen RP-Gates passiert."""
        warriors = _warriors_unit()
        assert "reanimationProtocols" in warriors.rules

    def test_rp_zero_models_back_leaves_state_unchanged(self):
        """0 Modelle zurück (alle RP-Würfel gescheitert) → kein Zustandswechsel."""
        unit = _warriors_unit()
        session = _make_session(
            p1_units={
                WARRIORS_ID: _warrior_state(models=7, current_wounds=7)
                | {"lost_models_this_turn": 3}
            },
            p2_units={},
            phase_idx=5,
            active="Necrons",
            round=1,
            cp={"Necrons": 4, "Orks": 4},
            selected_unit=None,
            selected_targets=[],
        )
        # heal_unit mit 0 HP → keine Änderung
        heal_unit(WARRIORS_ID, "Necrons", 0, unit)
        state = session["p1_units"][WARRIORS_ID]
        assert state["models"] == 7
        assert state["lost_models_this_turn"] == 3


# ---------------------------------------------------------------------------
# (d) get_active_rp_modifiers — rp_reroll-Flag
# ---------------------------------------------------------------------------


class TestGetActiveRpModifiers:
    """get_active_rp_modifiers (ability_engine.py:324) gibt rp_reroll zurück wenn
    ein entsprechendes Protokoll aktiv ist, sonst leeres dict.
    """

    def test_no_active_directive_returns_empty(self):
        """Ohne aktives Protokoll-Direktiv → leeres dict (kein rp_reroll)."""
        import gameMechanic.ability_engine as _eng

        # Session ohne round_choice-Assignments
        _eng.st.session_state = _S(
            first_player="Necrons",
            second_player="Orks",
        )
        from gameMechanic.ability_engine import get_active_rp_modifiers

        result = get_active_rp_modifiers("Necrons")
        assert result == {}

    def test_rp_reroll_flag_returned_when_protocol_effect_active(self):
        """Mit aktivem rp_reroll-Protokoll-Effekt → {'rp_reroll': True}."""
        import gameMechanic.ability_engine as _eng
        from gameMechanic.ability_engine import get_active_rp_modifiers

        # Patch get_active_protocol_effects direkt, um YAML-Abhängigkeit zu vermeiden
        with patch.object(
            _eng,
            "get_active_protocol_effects",
            return_value=[{"type": "rp_reroll"}],
        ):
            result = get_active_rp_modifiers("Necrons")
        assert result == {"rp_reroll": True}

    def test_rp_reroll_not_set_when_no_matching_effect(self):
        """Ohne rp_reroll-Effekt im Protokoll → leeres dict."""
        import gameMechanic.ability_engine as _eng
        from gameMechanic.ability_engine import get_active_rp_modifiers

        with patch.object(
            _eng,
            "get_active_protocol_effects",
            return_value=[],
        ):
            result = get_active_rp_modifiers("Necrons")
        assert result == {}
