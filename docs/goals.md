# Projektziele — Arbiter

## Vision

Arbiter ist ein digitaler Spielbegleiter für WH40k 9. Edition (Streamlit).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Zielarchitektur: `app.py` + `uiLayout/` + `gameObjects/` + `gameMechanic/`
Details: `docs/spec/architecture.md` · UI-Spec: `docs/spec/ui_layout.md`

---

## Ziel 1A — `uiLayout/` Struktursplit ✅

Ziel: `src/ui.py` wird ohne Verhaltensänderung in `src/uiLayout/` aufgeteilt.
Alle Sidebar-Komponenten erhalten dabei das neue Layout gemäß `docs/spec/ui_layout.md`.

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

**Zweck:** Sicherstellen, dass die Kernlogik korrekt und das Gesamtkonzept tragfähig ist, bevor Ziel 4 beginnt. Ziel ist nicht, alle Regeln zu implementieren, sondern zu prüfen ob bestehende Abstraktionen ausreichen oder substanzielle Lücken vorhanden sind. Ergebnis: `docs/work/architecture_review_2026-05.md` + bereinigtes Test-Gerüst.

**Leitfrage:** Kann eine neue Armee "angedockt" werden, ohne die Kernlogik anzufassen?
**Antwort:** Noch nicht — 3 Blocker müssen vor Ziel 4 behoben werden (siehe Review-Dokument).

---

### A1 — Regelwerk-Review gegen Architektur ✅

**Ergebnis:** `docs/work/architecture_review_2026-05.md`

- [x] Jede Regelgruppe klassifiziert
- [x] Edge Cases in `resolve_attack()` geprüft (AP-Mechanik korrekt, Spillover fehlt)
- [x] Ergebnis in Review-Dokument

---

### A2 — YAML-Struktur-Review & Datenqualität ✅

**Ergebnis:** `docs/work/architecture_review_2026-05.md`

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

---

### 4a — Einheitenzustand & Badge-System ✅

**Konzept:** Badges sind digitale Spielmarker — wie physische Tokens auf dem Tisch.
Jedes Badge drückt genau einen Regelzustand aus, der taktisch relevant ist.
Zustände lösen sich im Phasenverlauf ab oder ergänzen sich; ephemere Badges werden am Zugwechsel zurückgesetzt.

#### Badge-Vokabular (SOLL)

**Persistente Badges** (rundenübergreifend, nicht im Zugreset):

| Badge | Zustand |
|---|---|
| `IN MELEE` | Einheit ist im Nahkampf gebunden |
| `IN RESERVE` | Einheit in Reserve gehalten |

**Ephemere Bewegungs-Badges** (mutex, Zugstart → reset zu `STATIONARY`):

| Badge | Bedeutung | Einschränkungen |
|---|---|---|
| `STATIONARY` | Hat sich nicht bewegt (Zugstart-Default) | keine |
| `MOVED` | Normal bewegt (war: `"normal"`) | keine |
| `ADVANCED` | Vorgestoßen | ✗ Schuss (außer Assault), ✗ Charge |
| `RETREATED` | Aus Nahkampf zurückgezogen — löscht `IN MELEE` | ✗ Schuss, ✗ Charge |
| `CHARGED` | Angestürmt — ersetzt MOVED/STATIONARY, impliziert `IN MELEE` | kämpft zuerst |

**Aktion-Badges** (additiv, Zugstart → reset):

| Badge | Gesetzt wann | Ersetzt |
|---|---|---|
| `SHOT` | nach Schussauflösung (render_attack_form Shooting) | nichts (additiv) |
| `FOUGHT` | nach Kampfauflösung (render_attack_form Fight) | ersetzt `CHARGED` in Anzeige |

**Spezial-Badges**:

| Badge | Reset-Zeitpunkt |
|---|---|
| `MWBD` | Zugwechsel (`_reset_turn_state`) — aktuell Bug: wird nicht zurückgesetzt |

#### Badge-Priorität (Anzeigelogik)

```
Bewegungsgruppe (mutex):  FOUGHT > CHARGED > MOVED | ADVANCED | RETREATED | STATIONARY
Aktion (additiv):         SHOT zeigt immer neben dem aktuellen Bewegungsbadge
Persistent:               IN MELEE zeigt immer — außer CHARGED aktiv (impliziert IN MELEE)
Kombination:              FOUGHT + IN MELEE zeigen zusammen (kämpfte, noch gebunden)
                          SHOT + CHARGED zeigen zusammen (schoss und chargte)
                          SHOT + FOUGHT + IN MELEE möglich (voll aktiviert, noch gebunden)
```

#### Zustandsübergänge — vollständige Szenarien

| # | Startzustand | Bewegung | Fernkampf | Angriff | Nahkampf | Badge-Verlauf | Zugwechsel |
|---|---|---|---|---|---|---|---|
| 1 | STATIONARY | stationary | schießt | — | — | `STATIONARY` → `STATIONARY+SHOT` | `STATIONARY` |
| 2 | STATIONARY | normal | schießt | — | — | `STATIONARY` → `MOVED` → `MOVED+SHOT` | `STATIONARY` |
| 3 | STATIONARY | advance | — | — | — | `STATIONARY` → `ADVANCED` | `STATIONARY` |
| 4 | STATIONARY | normal | schießt | Charge ✓ | kämpft | `MOVED` → `MOVED+SHOT` → `SHOT+CHARGED` → `SHOT+FOUGHT+IN MELEE` | `IN MELEE` |
| 5 | STATIONARY | normal | — | Charge ✓ | kämpft | `MOVED` → `CHARGED` → `CHARGED+FOUGHT` → `[IN MELEE]` | `IN MELEE` |
| 6 | STATIONARY | normal | — | Charge ✗ | — | `MOVED` → `MOVED` (kein CHARGED) | `STATIONARY` |
| 7 | STATIONARY | normal | — | Charge ✓ | noch nicht | `MOVED` → `CHARGED` (zwischen Angriffs- und Nahkampfphase) | — |
| 8 | IN MELEE | stationary | — | — | kämpft | `IN MELEE` → `IN MELEE+FOUGHT` | `IN MELEE` |
| 9 | IN MELEE | stationary | — | — | Feind vernichtet | `IN MELEE` → `IN MELEE+FOUGHT` → auto-clear → `STATIONARY` | `STATIONARY` |
| 10 | IN MELEE | retreat | — | — | — | `IN MELEE` → `RETREATED` (IN MELEE erlischt) | `STATIONARY` |
| 11 | IN RESERVE | (Runde 1) | — | — | — | `IN RESERVE` bleibt | `IN RESERVE` |
| 12 | IN RESERVE | deploy (Runde ≥ 2) | ✗* | ✗* | — | `IN RESERVE` → `MOVED` (IN RESERVE erlischt) | `STATIONARY` |
| 13 | STATIONARY | (MWBD aktiv) | … | … | … | `STATIONARY+MWBD` → … | `STATIONARY` (MWBD cleared) |

*Reserve-Einschränkung in Ankunftsrunde: kein Charge, kein Shoot (vereinfachte Regel)

#### Dokumentation

- [x] Flussdiagramme + Badge-Vokabular in `docs/spec/unit_states.md` schreiben

#### Implementierungsschritte

- [x] `"normal"` → `"moved"` umbenennen: `unit_mutations`, `movementPhase`, `_common`, Tests
- [x] `turn_flags["shot"] = True` nach Schussauflösung setzen (`render_attack_form`, phase_key="shooting")
- [x] `turn_flags["fought"] = True` nach Kampfauflösung setzen (`render_attack_form`, phase_key="fight")
- [x] `state_badges_html()` — FOUGHT > CHARGED Priorität; SHOT additiv; IN MELEE bei CHARGED unterdrücken
- [x] `_reset_turn_state()` — `my_will_be_done_active` ebenfalls zurücksetzen (Bug)
- [x] `apply_damage()` — bei `destroyed=True` melee-Partner `in_melee` auto-clearen
- [x] Tests für neue Badge-Transitionen (TestStateBadges erweitern)

---

### 4b — armyCard + unitCard Redesign ✅

**Abgeschlossen.**

- [x] `unitCard.py` — neue Layout-Reihenfolge: LP/Modell-Bars → Name-Button → State-Badges → Keywords
- [x] `unitCard.py` — `st.container(border=True)`; Hauptfraktions-Keyword aus Keywords-Anzeige gefiltert
- [x] `unitCard.py` — Keyword-Highlighting via `session_state.highlight_keywords`
- [x] `armyCard.py` — Border, Faction-Badge + Subfaction-Badge
- [x] `armyCard.py` — TriggeredAbility-Buttons (phasenabhängig sichtbar, z.B. Living Metal in Befehlsphase)
- [x] `Ability.ability_type: str` — `"triggered"` | `"activated"` ins Datenmodell
- [x] YAMLs aktualisiert, Loader erweitert
- [x] `apply_living_metal()` von `commandPhase.py` → `unit_mutations.py` verschoben
- [x] Living Metal Button aus `commandPhase.py` entfernt (jetzt in armyCard)
- [x] `armyList.py` lädt und reicht `faction_abilities` weiter
- [x] 9 neue Tests — gesamt 209 grün

---

### 4c — Ability Engine Refactoring ✅

**Abgeschlossen** (commit `a884733`).

- [x] `Condition.needs_healing: bool`, `Effect.revive: bool` ins Datenmodell
- [x] `check_conditions()` + `execute_effect()` Dispatcher in `ability_engine.py`
- [x] `heal_unit(revive=)` — Cap-Logik korrekt
- [x] `apply_living_metal()` gelöscht — ersetzt durch generischen Dispatcher
- [x] Living Metal YAML: `unit_not_destroyed`, `needs_healing`, `revive: false`
- [x] `armyCard.py` vollständig datengetrieben
- [x] 215 Tests grün

---

### 4d — Befehlsphase vollständig ⬜

**Voraussetzung:** 4c abgeschlossen ✅

**Kontext:** Analyse in Session 2026-05-28 ergab drei Lücken in der Befehlsphase.

#### 4d.1 — Living Metal immer sichtbar

- [ ] `armyCard.py._render_triggered_abilities()`: Ability immer in Befehlsphase anzeigen
  — wenn keine Einheit verwundet: Caption "Alle Einheiten unverwundet" statt stilles Überspringen
  — Button bleibt nur aktiv wenn eligible units vorhanden

#### 4d.2 — Kommandoprotokolle (Necrons)

Necron-Armeeregel: In der eigenen Befehlsphase wählt der Nekron-Spieler eines von 5 Protokollen (jedes max. 1× pro Spiel). Runde 1: **Ewiger Wächter** automatisch aktiv (beide Direktiven). Mechanische Effekte werden noch nicht automatisch appliziert — nur Anzeige + Auswahl.

| Protokoll | Primär | Sekundär |
|---|---|---|
| Ewiger Wächter | +1 auf alle Rettungswürfe | WW1 wiederholen |
| Der hungrige Leere | +1 zum Treffen (Schuss) | +1 Stärke (Schuss) |
| Des tyrannischen Herrschers | +1 Führung | WW1 bei Treffen/Wunden (NK) |
| Des plötzlichen Sturms | +1 Bewegung | Vormarsch + Charge erlaubt |
| Unaufhörlicher Legionen | RP neu würfeln | +1 Modell pro RP |

- [ ] `data/wh40k_9e/necrons/command_protocols.yaml` — 5 Protokolle (id, name, primär, sekundär, `auto_round_1`)
- [ ] `src/gameObjects/command_protocol.py` — `CommandProtocol` Dataclass
- [ ] `src/gameObjects/loader.py` — `load_command_protocols(faction_dir)`
- [ ] `src/gameMechanic/game_state.py` — `active_protocol_id`, `used_protocol_ids` in `init_state` + `_reset_turn_state`
- [ ] `src/gameMechanic/commandPhase.py` — `_render_command_protocols()` für Necrons
- [ ] `src/uiLayout/gameProtocoll.py` — "Command Protocol" Tab zeigt Protokoll-Status

#### 4d.3 — RP-Trigger (Reanimationsprotokolle) — VERSCHOBEN

RP-Trigger gehört in Schuss-, Angriffs- und Nahkampfphase (nach Feindangriff). Wird dort implementiert.

---

### 4e — Bewegungsphase vollständig ⬜

- [x] **In-Melee-Lock** — Normal/Advance disabled wenn `in_melee=True`
- [x] **Post-Retreat-Lock** — Normal/Advance disabled nach `retreated=True`
- [ ] Advance-Roll: W6 würfeln, Ergebnis zur Bewegungsreichweite addieren, `advanced` setzen
- [ ] Reserve-Deploy (Zug 2+): `in_reserve=False`, Bewegungseinschränkungen greifen

---

### 4f — Angriffsphase (Charge Phase) ⬜

- [ ] Charge-Würfel: 2W6 — bei Erfolg `set_charged()`, bei Misserfolg bleibt `MOVED`
- [ ] `advanced`-Flag sperrt Charge-Button (Regelkonformität)
- [ ] RP-Trigger nach Feindangriff (Charge) — inaktiver Spieler kann RP auslösen
- [ ] Overwatch: gegnerische Schussreaktion mit `hit_modifier="only_6s"` (Scope: TBD)

---

### 4g — Moralphase ⬜

- [ ] D6 + Verluste vs. Leadership → bei Fehlschlag: Modelle fliehen (models reduzieren)
- [ ] `moralePhase.py` — Render-Logik

---

### 4h — Psychic Phase ⬜

- [ ] Manifest: 2D6 ≥ Warp Charge → Effekt ausführen
- [ ] Deny: gegnerischer Psyker darf versuchen zu unterdrücken
- [ ] Perils of the Warp: Doppel-1/Doppel-6 → Schaden am Psyker
- [ ] Scope: TBD (Necrons haben keine Psyker — für Ork-Phase relevant)

---

### 4i — Army Builder ⬜

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

Dokumentiert in `docs/spec/architecture.md` — Abschnitt "Open Design Questions".
