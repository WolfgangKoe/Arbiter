# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — Ziel 3 komplett neu (3a / 3b / 3c)
3. `docs/architecture.md` — PhaseHandler, PhaseRunner, combat.py, turn_flags, session_state-Schema
4. `docs/processes.md` — P-08 (AttackSequence, vollständig) + P-09 (PhaseRunner)
5. `src/gameMechanic/commandPhase.py` — Referenz-Pattern für PhaseHandler-Migration
6. `src/gameMechanic/ability_engine.py` — bestehende Timing-Struktur
7. `src/gameObjects/ability.py` — Trigger, Condition, Effect Dataclasses
8. `src/engine.py` — bestehender `_unit_state()`, `resolve_attack()` (wird deprecated)

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.
Starten: `streamlit run src/app.py`
Aktueller Branch: `dev`

```
src/
  app.py              ← Entry Point
  engine.py           ← Game Logic + State Init (resolve_attack wird deprecated)
  constants/colors.py
  uiLayout/
    gameHeader.py / armyList.py / armyCard.py / detachmentCard.py
    unitCard.py / gameActionsArea.py / gameProtocoll.py
  gameObjects/
    ability.py / unit.py / weapon.py / faction_property.py / stratagem.py / loader.py
  gameMechanic/
    __init__.py
    ability_engine.py       ← check_trigger, check_conditions, get_triggered_abilities
    commandPhase.py         ← muss auf PhaseHandler migriert werden (Ziel 3a)

data/wh40k_9e/
  necrons/ (army.yaml, unit_abilities.yaml, faction_abilities.yaml, …)
  orks/
  _shared/

tests/
  — 73 Tests, alle grün (Stand vor dieser Session)
```

---

## Was in der Planungs-Session erarbeitet wurde (kein Code geschrieben)

### Kern-Erkenntnisse

**Action ≠ Phase:**
Die `AttackSequence` ist eine wiederverwendbare Aktion, die von Fernkampf, Nahkampf und später
Overwatch (in der Angriffsphase) aufgerufen wird — mit unterschiedlichen Parametern, aber
identischer Auflösungslogik. Phasen sind Kontexte, die Aktionen mit Bedingungen aufrufen.

**Zwei Ebenen pro Würfelwurf:**
Jeder Schritt (Treffer, Verwundung, Schutzwurf) hat:
1. `raw_roll` + `roll_modifier` → `effective_roll` (Würfelergebnis-Ebene)
2. `threshold` (Vergleichswert-Ebene — aus Einheitenprofil oder S/T-Tabelle abgeleitet)

AP modifiziert den **Würfelwurf** (Ebene 1), NICHT den Threshold (Ebene 2).
Abilities müssen exakt angeben, welche Ebene sie beeinflussen.

**RP ist kein Sonderfall:**
Reanimation Protocols sind eine Necron-spezifische Ability mit Timing `after_unit_attacked`.
Kein Hardcode in `shootingPhase.py` oder `fightPhase.py`. Andere Armeen haben andere Abilities
mit anderen Timings. Das Ability-Hook-System behandelt alle gleich.

---

## Nächste Schritte: Ziel 3 implementieren

### Reihenfolge zwingend: 3a → 3b → 3c

### BLOCK 3a — Phase-Infrastruktur

**Neue Dateien:**
- `src/gameMechanic/phase_handler.py`
- `src/gameMechanic/phase_runner.py`
- `src/gameMechanic/movementPhase.py` (Stub)
- `src/gameMechanic/chargephase.py` (Stub)
- `src/gameMechanic/psychicPhase.py` (Stub)
- `src/gameMechanic/moralePhase.py` (Stub)

**Geänderte Dateien:**
- `src/engine.py` — turn_flags in `_unit_state()`, ad-hoc-Felder ersetzen, `reset_turn_flags()`
- `src/gameMechanic/commandPhase.py` — auf `CommandPhaseHandler` (PhaseHandler) migrieren
- `src/gameMechanic/ability_engine.py` — neue Timing-Konstanten hinzufügen
- `src/uiLayout/gameActionsArea.py` — Routing durch `phase_runner.render_current_phase(state)` ersetzen

**phase_handler.py Inhalt:**
```python
from typing import ClassVar, Protocol

class PhaseHandler(Protocol):
    phase_name: ClassVar[str]
    def render_start(self, state: dict) -> None: ...
    def render_active(self, state: dict) -> None: ...
    def render_end(self, state: dict) -> None: ...
```

**phase_runner.py Inhalt:**
```python
PHASE_REGISTRY: dict[str, PhaseHandler] = {}

def render_current_phase(state: dict) -> None:
    handler = PHASE_REGISTRY[state["phase"]]
    stage   = state.get("phase_stage", "active")
    triggered = get_triggered_abilities(state, state["phase"], f"phase_{stage}")
    getattr(handler, f"render_{stage}")(state)

def advance_stage(state: dict) -> None:
    # start → active → end → next_phase
    # Bei end → next_phase: reset_turn_flags aufrufen
    ...

def _setup_registry() -> None:
    # Alle Handler importieren und registrieren
    from gameMechanic.commandPhase import CommandPhaseHandler
    from gameMechanic.movementPhase import MovementPhaseHandler
    # ...
    for h in [...]:
        PHASE_REGISTRY[h.phase_name] = h

_setup_registry()
```

**turn_flags in engine.py `_unit_state()`:**
```python
"turn_flags": {
    "advanced":  False,
    "retreated": False,
    "charged":   False,
    "shot":      False,
    "fought":    False,
}
```
Alte Felder entfernen: `movement_status`, `charged_this_turn`, `acted_this_phase`.
Alten `resolve_attack()` deprecaten (Kommentar + Hinweis auf combat.py).

**Neue ability_engine.py Timing-Konstanten:**
```python
TIMING_PHASE_START        = "phase_start"
TIMING_PHASE_END          = "phase_end"
TIMING_BEFORE_UNIT_ACTS   = "before_unit_acts"
TIMING_AFTER_UNIT_ATTACKED = "after_unit_attacked"
```

**Stub-Handler (alle identisch strukturiert):**
```python
class MovementPhaseHandler:
    phase_name = "movement"
    def render_start(self, state: dict) -> None: pass
    def render_active(self, state: dict) -> None:
        st.info("**Movement Phase** — select a unit and choose its movement type.")
        st.caption("Turn flags (advanced/retreated) set here in Ziel 4.")
    def render_end(self, state: dict) -> None: pass
```

---

### BLOCK 3b — combat.py — KRITISCHE DATEI

**Neue Datei:** `src/gameMechanic/combat.py`

#### Dataclasses

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class Modifier:
    step: Literal["hit", "wound", "save", "damage"]
    target_type: Literal[
        "roll",             # Würfelergebnis direkt
        "threshold",        # Vergleichswert direkt (selten)
        "source_strength",  # → wound_threshold indirekt
        "source_toughness", # → wound_threshold indirekt
    ]
    operation: Literal["add", "subtract", "reroll_ones", "reroll_all", "mortal_on", "ignore_ap"]
    value: int | None = None
    condition: str | None = None  # "on_unmodified_6" | "if_keyword:CORE" | …

@dataclass
class AttackParams:
    n_attacks:     int
    hit_threshold: int        # z.B. 3 = "benötigt 3+"
    strength:      int        # bereits aufgelöst, kein "User"
    toughness:     int
    ap:            int        # 0 / -1 / -2 … (vom Roll subtrahiert, kein Cap)
    damage:        int        # bereits aufgelöst, kein "D3"
    save:          int        # Rüstungswurf (z.B. 3 = "3+")
    invuln_save:   int | None # Rettungswurf oder None
    modifiers:     list[Modifier] = field(default_factory=list)

@dataclass
class AttackResult:
    wound_threshold:  int
    effective_save:   int      # tatsächlich genutzter Threshold
    hits:             int
    wounds:           int
    failed_saves:     int
    damage_dealt:     int
    mortal_wounds:    int
    log_lines:        list[str]

@dataclass
class AttackDisplay:
    """Was der Spieler vor dem Würfeln sehen muss."""
    n_attacks:          int
    hit_threshold:      int    # nach Modifikatoren
    hit_roll_modifier:  int    # gecappt ±1
    wound_threshold:    int    # nach S/T-Auflösung
    wound_roll_modifier: int   # gecappt ±1
    armor_save:         int    # Threshold unverändert
    armor_effective_roll_modifier: int  # = ap (kein Cap)
    invuln_save:        int | None
    active_modifiers:   list[str]  # human-readable Modifier-Beschreibungen
```

#### Funktionen

```python
def s_vs_t_table(strength: int, toughness: int) -> int:
    """Gibt wound_threshold (2-6) zurück."""
    if strength >= toughness * 2: return 2
    if strength > toughness:      return 3
    if strength == toughness:     return 4
    if strength * 2 <= toughness: return 6
    return 5

def build_attack_display(params: AttackParams) -> AttackDisplay:
    """Aufgelöste Anzeige für den Spieler, VOR dem Würfeln."""
    ...

def resolve_attack_sequence(
    params:         AttackParams,
    save_choice:    Literal["armor", "invuln"],
    n_hits:         int,           # vom Spieler eingegeben
    n_wounds:       int,
    n_failed_saves: int,
) -> AttackResult:
    """Auflösungsreihenfolge STRIKT wie in P-08 dokumentiert."""
    # SCHRITT 1: Quellparameter
    # SCHRITT 2: Threshold bestimmen
    # SCHRITT 3: Roll-Modifier sammeln (Cap ±1 für hit/wound, kein Cap für AP)
    # SCHRITT 4: Sonderregeln (unmod. 1/6)
    # SCHRITT 5: Schaden + Mortal Wounds
    ...
```

#### Tests: `tests/gameMechanic/test_combat.py` — ≥ 40 Tests, VOLLSTÄNDIG

**s_vs_t_table (7 Tests):**
```
test_s_double_t_returns_2          S8  vs T4 → 2
test_s_exact_double_t_returns_2    S8  vs T4 → 2 (Grenze: genau ×2)
test_s_greater_t_returns_3         S5  vs T4 → 3
test_s_equal_t_returns_4           S4  vs T4 → 4
test_s_less_t_returns_5            S3  vs T4 → 5
test_s_exact_half_t_returns_6      S2  vs T4 → 6 (Grenze: genau ½)
test_s_below_half_t_returns_6      S1  vs T4 → 6
```

**Quellparameter (source_strength / source_toughness) (5 Tests):**
```
test_source_strength_add_shifts_wound_threshold_up
    → S+1: S4→S5 vs T4, wound_threshold 4→3
test_source_strength_sub_shifts_wound_threshold_down
    → S-1: S4→S3 vs T4, wound_threshold 4→5
test_source_toughness_add_shifts_wound_threshold_down
    → T+1: S4 vs T4→T5, wound_threshold 4→5
test_source_strength_does_not_affect_hit_threshold
    → S+1 Modifier hat KEINEN Einfluss auf hit_threshold
test_multiple_source_modifiers_accumulate
    → S+1 + S+1 = Σ S+2, Auswirkung auf wound_threshold korrekt
```

**Hit Roll Modifier (6 Tests):**
```
test_hit_roll_modifier_add_applied_to_roll
    → Modifier(hit, roll, add, 1): roll_modifier=+1, hit_threshold UNVERÄNDERT
test_hit_roll_modifier_cap_two_plus_one_gives_net_one
    → zwei Modifier add=1: netto +1 (gecappt)
test_hit_roll_modifier_cap_two_minus_one_gives_net_minus_one
    → zwei Modifier subtract=1: netto -1 (gecappt)
test_unmodified_1_always_misses_with_positive_hit_modifier
    → raw_roll=1, roll_modifier=+1 → immer Fehler (Sonderregel)
test_unmodified_6_always_hits_with_negative_hit_modifier
    → raw_roll=6, roll_modifier=-1 → immer Treffer (Sonderregel)
test_hit_threshold_modifier_separate_code_path_from_roll_modifier
    → Modifier(hit, threshold, subtract, 1) ≠ Modifier(hit, roll, add, 1)
      (gleicher Nettoeffekt, aber verschiedene target_type-Werte)
```

**Wound Roll Modifier (5 Tests):**
```
test_wound_roll_modifier_add_applied_to_roll
    → +1 to wound roll: roll_modifier=+1, wound_threshold UNVERÄNDERT
test_wound_roll_modifier_cap_applied
    → zwei add=1: netto +1
test_unmodified_1_always_fails_wound_with_positive_modifier
    → raw_roll=1, mod=+1 → immer Fehler
test_unmodified_6_always_wounds_with_negative_modifier
    → raw_roll=6, mod=-1 → immer Verwundung
test_wound_roll_modifier_distinct_from_source_strength
    → Modifier(wound, roll, add, 1) ≠ Modifier(wound, source_strength, add, 1)
      (verschiedene Code-Pfade, können unterschiedliche Netto-Effekte haben)
```

**Save Roll + AP (7 Tests):**
```
test_ap_modifies_roll_not_threshold
    → AP-1: save_roll wird um 1 reduziert; unit.save UNVERÄNDERT
test_ap_zero_no_modification
    → AP=0: save_roll unverändernd, effektiv = raw_roll
test_ap_minus_two_reduces_roll_by_two
    → AP-2: effective_save_roll = raw - 2
test_invuln_save_ignores_ap
    → save_choice="invuln": ap_modifier=0, unabhängig vom weapon.ap
test_invuln_save_uses_invuln_threshold_not_armor
    → save_choice="invuln": threshold = unit.invuln_save, nicht unit.save
test_unmodified_1_always_fails_save
    → raw_roll=1, AP=0 → immer Fehler (Sonderregel)
test_additional_save_roll_modifier_from_ability
    → Modifier(save, roll, subtract, 1): weitere Roll-Reduktion auf Schutzwurf
```

**Mortal Wounds (3 Tests):**
```
test_mortal_on_6_generates_separate_mortal_wound_count
    → Modifier(wound, roll, mortal_on, 6): n_wounds auf 6 → mortal_wounds += 1
test_mortal_wounds_bypass_save_roll
    → mortal_wounds in AttackResult sind separate Zählung, kein Schutzwurf
test_mortal_wounds_accumulate_with_normal_damage
    → mortal_wounds + damage_dealt beide im AttackResult korrekt
```

**Integration (7 Tests):**
```
test_resolve_full_sequence_basic
    → n_hits=3, n_wounds=2, n_failed_saves=1, damage=2 → damage_dealt=2, mortal_wounds=0
test_resolve_zero_hits_gives_zero_damage
    → n_hits=0 → damage_dealt=0, mortal_wounds=0
test_resolve_zero_wounds_gives_zero_damage
    → n_wounds=0 → damage_dealt=0
test_resolve_zero_failed_saves_gives_zero_damage
    → n_failed_saves=0 → damage_dealt=0
test_resolve_all_modifiers_combined
    → source_strength+1 + hit_roll+1 + ap-2 + invuln → alle Pfade gleichzeitig korrekt
test_damage_multiplies_correctly
    → n_failed_saves=3, damage=2 → damage_dealt=6
test_log_lines_populated
    → AttackResult.log_lines ist nicht leer und enthält relevante Infos
```

**AttackDisplay (4 Tests):**
```
test_build_attack_display_hit_threshold_with_modifier
    → hit_threshold korrekt angezeigt nach Roll-Modifier-Cap
test_build_attack_display_wound_threshold_after_strength_modifier
    → wound_threshold neu berechnet nach source_strength Modifier
test_build_attack_display_shows_both_save_options
    → armor_save + invuln_save beide im Display vorhanden (auch wenn invuln=None)
test_build_attack_display_armor_effective_roll_modifier_equals_ap
    → armor_effective_roll_modifier = weapon.ap (kein Cap)
```

---

### BLOCK 3c — ShootingPhaseHandler + FightPhaseHandler

**Neue Dateien:** `src/gameMechanic/shootingPhase.py`, `src/gameMechanic/fightPhase.py`
**Geänderte Datei:** `data/wh40k_9e/necrons/unit_abilities.yaml` (RP-Timing)

#### shootingPhase.py

```python
def can_shoot(unit_state: dict) -> bool:
    flags = unit_state["turn_flags"]
    return (
        not flags["advanced"]
        and not flags["retreated"]
        and not unit_state.get("in_melee", False)
    )

def params_from_ranged_attack(
    attacker: Unit, weapon: Weapon, target: Unit, active_buffs: list[str]
) -> AttackParams:
    """Löst 'User'-Stärke, parse_dice-Attacken auf. Baut Modifier-Liste aus active_buffs."""
    n_attacks = parse_dice(weapon.attacks)
    strength  = int(weapon.strength)   # Fernkampfwaffe hat immer feste S
    hit_mod   = Modifier(step="hit", target_type="roll", operation="add", value=1) \
                if "my_will_be_done" in active_buffs else None
    return AttackParams(
        n_attacks=n_attacks,
        hit_threshold=int(attacker.bs.rstrip("+")),
        strength=strength,
        toughness=target.toughness,
        ap=int(weapon.ap),
        damage=parse_dice(weapon.damage),
        save=target.save,
        invuln_save=target.invuln_save,
        modifiers=[m for m in [hit_mod] if m is not None],
    )
```

UI-Struktur in `render_active`:
1. Linke PlayerArea: Angreifer wählen → Waffe wählen → `can_shoot` prüfen
2. Rechte PlayerArea: Ziel wählen → T/Save/Invuln anzeigen
3. DisplayArea: `build_attack_display()` anzeigen (was muss der Spieler würfeln?)
4. Spieler-Input: `n_hits` / `n_wounds` / `save_choice` / `n_failed_saves`
5. "Schaden anwenden" Button → `resolve_attack_sequence()` → `apply_damage()`
6. Ability-Hook: `ability_engine.get_triggered_abilities(state, "shooting", TIMING_AFTER_UNIT_ATTACKED)` → RP-UI falls Necrons

#### fightPhase.py

```python
def can_fight(unit_state: dict) -> bool:
    return unit_state.get("in_melee", False) or unit_state["turn_flags"]["charged"]

def params_from_melee_attack(
    attacker: Unit, weapon: Weapon, target: Unit, active_buffs: list[str]
) -> AttackParams:
    """Nahkampf: n_attacks aus Unit.attacks (A-Stat), Stärke aus Waffe ('User' → unit.strength)."""
    n_attacks = parse_dice(str(attacker.attacks))  # A-Stat
    raw_s = weapon.strength
    strength = attacker.strength if raw_s.lower() == "user" else int(raw_s)
    ...
```

UI-Struktur: identisch zu Shooting, aber:
- Fights-First-Reihenfolge: `turn_flags["charged"]` → zuerst kämpfen
- Keine Reichweitenprüfung (in_melee bereits gesetzt)

#### RP-Ability YAML Update

```yaml
# data/wh40k_9e/necrons/unit_abilities.yaml — Reanimation Protocols Trigger
trigger:
  timing: after_unit_attacked    # NEU (war: phase_any)
  phase:
    - shooting
    - fight
  player: inactive               # feuert für den Spieler, der ANGEGRIFFEN WIRD
  stage: active
```

---

## Tests — Gesamtübersicht nach Ziel 3

| Datei | Neue Tests | Gesamt (inkl. bestehend) |
|---|---|---|
| `test_combat.py` (neu) | ≥ 40 | ≥ 40 |
| `test_shooting_phase.py` (neu) | ~8 | ~8 |
| `test_fight_phase.py` (neu) | ~8 | ~8 |
| `test_command_phase.py` | ~2 angepasst | ~15 |
| alle anderen | unverändert | 73 |
| **Gesamt** | **~58+** | **~131+** |

---

## Offene Designfragen

1. **Damage-Werte als Variable (D3/D6):** `parse_dice()` in `engine.py` würfelt zufällig.
   In `combat.py` brauchen wir `damage: int` (aufgelöst). Wann löst wer auf?
   Vorschlag: `build_attack_display()` zeigt den Würfelausdruck ("D3"), Spieler würfelt physisch,
   klickt den tatsächlichen Wert → `damage = eingegebener_wert` in `AttackParams`.

2. **Multi-Weapon-Shooting:** Eine Einheit kann mehrere Waffen auf verschiedene Ziele richten.
   In Ziel 3: eine Waffe, ein Ziel. Multi-Target folgt in Ziel 4.

3. **FNP (Feel No Pain):** `engine.py` hat bereits FNP-Logik. In `combat.py`:
   FNP ist ein `after_damage` Ability-Hook, kein eigener Schritt in der Sequenz?
   Oder als separater Schritt nach failed_saves? → Entscheid vor Implementierung von 3c.

4. **Überschuss-Schaden normal vs. tödliche Verwundungen:** Normale Attacken → Überschuss verfällt.
   Tödliche Verwundungen → Überschuss geht an nächstes Modell in der Einheit.
   In `apply_damage()` abzubilden — aktuell in `engine.py`, muss mit combat.py abgestimmt werden.

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Grundstruktur & Layout | ✅ fertig |
| Einheitenstatus (Wundverwaltung) | ✅ fertig |
| Durchstich (Phasenstruktur, State, Zentralbereich) | ✅ fertig |
| Ziel 1A — uiLayout/ Struktursplit | ✅ fertig |
| Ziel 1B — gameObjects/ Foundation | ✅ fertig |
| Bug-Fixes + Engine-Tests | ✅ fertig |
| Ziel 2 — commandPhase + Ability-System | ✅ fertig (73 Tests grün) |
| Architektur-Update — UI-Refactoring, Farben, Stratagem-Modell, Prozessdoku | ✅ fertig |
| **Ziel 3a — Phase-Infrastruktur** | ⏳ nächster Schritt |
| **Ziel 3b — combat.py (≥ 40 Tests)** | ⏳ parallel zu 3a |
| **Ziel 3c — Shooting + Fight Phase** | ⏳ nach 3a + 3b |
| Ziel 4 — Phasen ausbauen + Army Builder | ⬜ später |
