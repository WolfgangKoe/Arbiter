# Ziel 3 — Combat Foundation ✅

**Voraussetzung:** Ziel 2 abgeschlossen ✅

---

## 3a — Phase-Infrastruktur ✅

- [x] `gameMechanic/phase_handler.py` — `PhaseHandler` Protocol
- [x] `gameMechanic/phase_runner.py` — zentraler Dispatcher, `PHASE_REGISTRY`
- [x] `gameMechanic/game_state.py` — `turn_flags` in `_unit_state()`, `reset_turn_flags()`
- [x] `gameMechanic/ability_engine.py` — Timing-Konstanten, Trigger-System
- [x] `gameMechanic/commandPhase.py` — auf `CommandPhaseHandler` migriert
- [x] `uiLayout/gameActionsArea.py` — Routing über `phase_runner.render_current_phase(state)`
- [x] Alle Phase-Handler als vollständige Stubs: `movementPhase.py`, `chargephase.py`, `shootingPhase.py`, `fightPhase.py`, `psychicPhase.py`, `moralePhase.py`
- [x] `engine.py` aufgeteilt in `game_state.py`, `unit_mutations.py`, `game_log.py`, `combat.py`; `engine.py` gelöscht

---

## 3b — Combat-Kernel (`combat.py`) ✅

- [x] `gameMechanic/combat.py` — `AttackParams`, `DefendParams` Dataclasses; neue `resolve_attack(params, defender, hits_rolled, wounds_rolled, saves_failed, fnp_saved) → (damage, log)`
- [x] Player-entered roll counts (kein Auto-Würfeln); AP/Invuln/FNP/MWBD korrekt
- [x] Deprecated `resolve_attack(Unit, Weapon, ...)` entfernt
- [x] `tests/gameMechanic/test_combat.py` — **41 Tests**, alle grün

---

## 3c — Shooting Phase + Fight Phase ✅

**Voraussetzung:** 3b vollständig ✅

### Shooting Phase (`shootingPhase.py`)

- [x] `can_shoot(unit_state) → bool` — pure function; False wenn: `advanced`, `retreated`, `in_melee`, `in_reserve`
- [x] UI-Flow: Angreifer wählt Waffe → gibt `hits_rolled` / `wounds_rolled` / `saves_failed` / `fnp_saved` ein → `resolve_attack()` → Schadensanzeige + Log
- [x] Schadensanwendung via `apply_damage()` aus `unit_mutations.py`
- [x] Variable Schadenswerte (D6, W3 etc.) → Extra-Eingabefeld
- [x] Tests: 18 Tests grün

### Fight Phase (`fightPhase.py`)

- [x] `can_fight(unit_state) → bool` — True wenn `in_melee=True` ODER `charged=True`
- [x] Fights-First-Indikator: `fights_first`-Keyword in `unit.keywords` → Badge/Info
- [x] UI analog Shooting: Waffe → Roll-Eingabe → Schadensanzeige + Apply Damage
- [x] Tests: 15 Tests grün

### Shared

- [x] `render_attack_form()` in `uiLayout/_common.py` — von beiden Phasen genutzt
- [x] `_try_parse_damage()` — erkennt variable Schadenswerte
- [x] `"User"`-Stärke wird zu Einheitenstärke aufgelöst

---

## Ziel A — Architektur-Review & Erweiterungsfähigkeit ✅

**Zweck:** Sicherstellen, dass die Kernlogik korrekt und das Gesamtkonzept tragfähig ist, bevor Ziel 4 beginnt.
Ergebnis: `docs/work/architecture_review_2026-05.md` + bereinigtes Test-Gerüst.

**Leitfrage:** Kann eine neue Armee "angedockt" werden, ohne die Kernlogik anzufassen?
**Antwort:** Noch nicht — 3 Blocker wurden vor Ziel 4 behoben (siehe Review-Dokument).

### A1 — Regelwerk-Review gegen Architektur ✅

- [x] Jede Regelgruppe klassifiziert
- [x] Edge Cases in `resolve_attack()` geprüft (AP-Mechanik korrekt, Spillover fehlt)
- [x] Ergebnis: `docs/work/architecture_review_2026-05.md`

### A2 — YAML-Struktur-Review & Datenqualität ✅

- [x] Necron-YAML-Felder klassifiziert: ~200 Zeilen Curation-Metadaten löschen
- [x] `<Dynasty>` kanonisch; `dynasty_selectable` löschen
- [x] Degradierende Profile: Option A (Dataclass-Erweiterung) empfohlen
- [x] W-Notation vs. D-Notation: Crash-Bug dokumentiert, Fix-Empfehlung (Option B, 1 Zeile)
- [x] Stärke-Relativwerte (`Träger`, `+1`, `x2`): Caller-Kontrakt-Lücke dokumentiert
- [x] Ork-Einheitenliste via Wahapedia beschafft (~80 Einheiten)
- [x] Template-YAML für armeeneutrale Einheiten erstellt
- [x] Ergebnis: `docs/work/architecture_review_2026-05.md`

### A3 — Test-Struktur-Refactoring ✅

**Ergebnis:** 166 Tests grün (177 − 11 Duplikate), `tests/engine/` gelöscht.

- [x] `test_engine.py` aufgeteilt: `apply_damage`/`heal_unit` → `test_unit_mutations.py`; `next_phase` → `test_game_state.py`; 11 Duplikate entfernt
- [x] `test_multi_target.py` → `tests/gameMechanic/test_unit_mutations.py` zusammengeführt
- [x] `test_state_badges.py` → `tests/uiLayout/test_common.py` (neuer Ordner)
- [x] `tests/engine/` gelöscht
- [x] Alle 166 Tests grün
