# Projektziele — Arbiter

## Vision

Arbiter ist ein digitaler Spielbegleiter für WH40k 9. Edition (Streamlit).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Zielarchitektur: `app.py` + `uiLayout/` + `gameObjects/` + `gameMechanic/`
Details: `docs/architecture.md` · UI-Spec: `docs/ui_layout.md`

---

## Ziel 1A — `uiLayout/` Struktursplit ✅

Ziel: `src/ui.py` wird ohne Verhaltensänderung in `src/uiLayout/` aufgeteilt.
Alle Sidebar-Komponenten erhalten dabei das neue Layout gemäß `docs/ui_layout.md`.

**Abgeschlossen.** `ui.py` gelöscht. Alle Komponenten in `uiLayout/` aktiv.

- [x] `uiLayout/gameHeader.py` — VP/CP-Stepper, Phase-Navigation, Theme-CSS
- [x] `uiLayout/armyCard.py` — Fraktion/Subfraktion-Anzeige
- [x] `uiLayout/unitCard.py` — Name als Selector, Keywords, LP/Modell-Bar, State-Badges
- [x] `uiLayout/detachmentCard.py` — Detachment-Header + unitCards gruppiert nach Schlachtfeldrolle
- [x] `uiLayout/armyList.py` — Container: armyCard + 1–n detachmentCards
- [x] `uiLayout/gameProtocoll.py` — Battle-Log aus game_log.json + Deployment-Snapshot
- [x] `uiLayout/gameActionsArea.py` — Container; delegiert an phase_runner
- [x] `app.py` auf neue Imports umgestellt
- [x] Alle Tests grün

---

## Ziel 1B — `gameObjects/` Foundation ✅

Ziel: Reine Python-Grundlage für alle Spieldaten. Kein Streamlit, kein session_state.
Armeedaten fließen ausschließlich durch den Loader — keine hardcodierten Listen mehr.

**Abgeschlossen.** `models.py` gelöscht. Alles über YAML-Loader.

- [x] `gameObjects/unit.py` — `Unit` Dataclass
- [x] `gameObjects/weapon.py` — `Weapon` Dataclass
- [x] `gameObjects/faction_property.py` — `FactionProperty` Dataclass
- [x] `gameObjects/detachment.py` — `DetachmentType`, `SlotConstraint`
- [x] `gameObjects/loader.py` — liest YAML, löst Waffen-Referenzen auf
- [x] `data/wh40k_9e/_shared/detachment_types.yaml` — Patrol usw. mit Slot-Constraints
- [x] YAML-Daten für Necrons + Orks vollständig kuratiert
- [x] `models.py` (hardcodierte Dicts) entfernt
- [x] Unit-Tests für Loader und State-Funktionen

---

## Ziel 2 — `gameMechanic/` Einstieg: Command Phase ✅

Ziel: Erste vollständige Phase als Blaupause für alle weiteren.

**Abgeschlossen.** Dateinamen weichen leicht vom Plan ab (state.py → game_state.py, protocol.py → game_log.py).

- [x] `gameMechanic/game_state.py` — `init_state`, `reset_game`, `next_phase`, `PHASES`, Unit-Loader
- [x] `gameMechanic/game_log.py` — `log_action`, `clear_game_log`
- [x] `gameMechanic/unit_mutations.py` — alle Unit/VP/CP-Mutations
- [x] `gameMechanic/commandPhase.py` — CP-Grant (1×/Phase), Living Metal, MWBD (CORE-Unit-Auswahl), Resurrection Orb (Unit-Auswahl + Heal-Buttons)
- [x] `uiLayout/gameActionsArea.py` — Layout vollständig, "Start Game"-Button in Setup
- [x] Select-Logik in `unitCard.py` vollständig verdrahtet
- [x] `gameProtocoll` — Battle-Log mit Expander nach Round/Phase
- [x] Tests für commandPhase

---

## Ziel 3 — Combat Foundation: Phase-Infrastruktur + Attack Sequence ⏳

**Voraussetzung:** Ziel 2 abgeschlossen ✅

---

### 3a — Phase-Infrastruktur ✅

- [x] `gameMechanic/phase_handler.py` — `PhaseHandler` Protocol
- [x] `gameMechanic/phase_runner.py` — zentraler Dispatcher, `PHASE_REGISTRY`
- [x] `gameMechanic/game_state.py` — `turn_flags` in `_unit_state()`, `reset_turn_flags()`
- [x] `gameMechanic/ability_engine.py` — Timing-Konstanten, Trigger-System
- [x] `gameMechanic/commandPhase.py` — auf `CommandPhaseHandler` migriert
- [x] `uiLayout/gameActionsArea.py` — Routing über `phase_runner.render_current_phase(state)`
- [x] Alle Phase-Handler als vollständige Stubs: `movementPhase.py`, `chargephase.py`, `shootingPhase.py`, `fightPhase.py`, `psychicPhase.py`, `moralePhase.py`
- [x] `engine.py` aufgeteilt in `game_state.py`, `unit_mutations.py`, `game_log.py`, `combat.py`; `engine.py` gelöscht

---

### 3b — Combat-Kernel (`combat.py`) ✅

- [x] `gameMechanic/combat.py` — `AttackParams`, `DefendParams` Dataclasses; neue `resolve_attack(params, defender, hits_rolled, wounds_rolled, saves_failed, fnp_saved) → (damage, log)`
- [x] Player-entered roll counts (kein Auto-Würfeln); AP/Invuln/FNP/MWBD korrekt
- [x] Deprecated `resolve_attack(Unit, Weapon, ...)` entfernt
- [x] `tests/gameMechanic/test_combat.py` — **41 Tests**, alle grün

---

### 3c — Shooting Phase + Fight Phase ✅

**Voraussetzung:** 3b vollständig ✅

#### Shooting Phase (`shootingPhase.py`)

- [x] `can_shoot(unit_state) → bool` — pure function; False wenn: `advanced`, `retreated`, `in_melee`, `in_reserve`
- [x] UI-Flow: Angreifer wählt Waffe → gibt `hits_rolled` / `wounds_rolled` / `saves_failed` / `fnp_saved` ein → `resolve_attack()` → Schadensanzeige + Log
- [x] Schadensanwendung via `apply_damage()` aus `unit_mutations.py`
- [x] Variable Schadenswerte (D6, W3 etc.) → Extra-Eingabefeld
- [x] Tests: 18 Tests grün

#### Fight Phase (`fightPhase.py`)

- [x] `can_fight(unit_state) → bool` — True wenn `in_melee=True` ODER `charged=True`
- [x] Fights-First-Indikator: `fights_first`-Keyword in `unit.keywords` → Badge/Info
- [x] UI analog Shooting: Waffe → Roll-Eingabe → Schadensanzeige + Apply Damage
- [x] Tests: 15 Tests grün

#### Shared

- [x] `render_attack_form()` in `uiLayout/_common.py` — von beiden Phasen genutzt
- [x] `_try_parse_damage()` — erkennt variable Schadenswerte
- [x] `"User"`-Stärke wird zu Einheitenstärke aufgelöst

---

## Ziel A — Architektur-Review & Erweiterungsfähigkeit ✅

**Zweck:** Sicherstellen, dass die Kernlogik korrekt und das Gesamtkonzept tragfähig ist, bevor Ziel 4 beginnt. Ziel ist nicht, alle Regeln zu implementieren, sondern zu prüfen ob bestehende Abstraktionen ausreichen oder substanzielle Lücken vorhanden sind. Ergebnis: `docs/review/architecture_review_2026-05.md` + bereinigtes Test-Gerüst.

**Leitfrage:** Kann eine neue Armee "angedockt" werden, ohne die Kernlogik anzufassen?
**Antwort:** Noch nicht — 3 Blocker müssen vor Ziel 4 behoben werden (siehe Review-Dokument).

---

### A1 — Regelwerk-Review gegen Architektur ✅

**Ergebnis:** `docs/review/architecture_review_2026-05.md`

- [x] Jede Regelgruppe klassifiziert
- [x] Edge Cases in `resolve_attack()` geprüft (AP-Mechanik korrekt, Spillover fehlt)
- [x] Ergebnis in Review-Dokument

---

### A2 — YAML-Struktur-Review & Datenqualität ✅

**Ergebnis:** `docs/review/architecture_review_2026-05.md`

- [x] Necron-YAML-Felder klassifiziert: ~200 Zeilen Curation-Metadaten löschen
- [x] `<Dynasty>` kanonisch; `dynasty_selectable` löschen
- [x] Degradierende Profile: Option A (Dataclass-Erweiterung) empfohlen
- [x] W-Notation vs. D-Notation: Crash-Bug dokumentiert, Fix-Empfehlung (Option B, 1 Zeile)
- [x] Stärke-Relativwerte (`Träger`, `+1`, `x2`): Caller-Kontrakt-Lücke dokumentiert
- [x] Ork-Einheitenliste via Wahapedia beschafft (~80 Einheiten)
- [x] Template-YAML für armeeneutrale Einheiten erstellt
- [x] Ergebnis in Review-Dokument

---

### A3 — Test-Struktur-Refactoring ✅

**Ergebnis:** 166 Tests grün (177 − 11 Duplikate), `tests/engine/` gelöscht.

- [x] `test_engine.py` aufgeteilt: `apply_damage`/`heal_unit` → `tests/gameMechanic/test_unit_mutations.py`; `next_phase` → `tests/gameMechanic/test_game_state.py`; 11 Duplikate entfernt
- [x] `test_multi_target.py` → `tests/gameMechanic/test_unit_mutations.py` zusammengeführt
- [x] `test_state_badges.py` → `tests/uiLayout/test_common.py` (neuer Ordner)
- [x] `tests/engine/` gelöscht
- [x] Alle 166 Tests grün

---

## Ziel 4 — Phasen ausbauen + Army Builder ⬜

**Voraussetzung:** Ziel 3 abgeschlossen. Ziel A liefert die Grundlage für korrekte Implementierung.

### Bekannte Bugs (Bewegungsphase)

- [x] **In-Melee-Lock** — Normal/Advance disabled wenn `in_melee=True` ✅
- [x] **Post-Retreat-Lock** — Normal/Advance disabled nach `retreated=True` ✅

### Phasen (Stubs → vollständige Implementierung)
- [ ] `movementPhase.py` — Advance-Roll, Reserve-Deploy (Zug 2+); Bugs (siehe oben) als Voraussetzung
- [ ] `chargephase.py` — Overwatch via `ShootingAction` mit `hit_modifier="only_6s"`
- [ ] `moralePhase.py` — D6 + Verluste vs. Leadership
- [ ] `psychicPhase.py` — Manifest (2D6 ≥ WC), Deny, Perils (Scope: TBD)

### Army Builder
- [ ] Entscheidung: Datei-Import vs. In-App-Builder vs. hardcodierte Presets (TBD)
- [ ] Setup-Screen: Spielgröße, Spieltyp, Armeeauswahl, Erster Spieler
- [ ] Detachment-Slot-Constraints als Referenz im Setup anzeigen

---

## Design-Block — UI-Theme ⏳ (eigene Session)

- [ ] Farbpalette überarbeiten — Goldtöne, Primärfarbe, Kontraste
- [ ] Badge-Optik und Spacing prüfen
- [ ] Einheitenkarten-Layout verfeinern

---

## Offene Designfragen

Dokumentiert in `docs/architecture.md` — Abschnitt "Open Design Questions".
