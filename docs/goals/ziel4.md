# Ziel 4 — Phasen ausbauen ✅

**Voraussetzung:** Ziel 3 abgeschlossen ✅. Ziel A liefert die Grundlage für korrekte Implementierung.

---

## 4a — Einheitenzustand & Badge-System ✅

**Konzept:** Badges sind digitale Spielmarker — wie physische Tokens auf dem Tisch.
Jedes Badge drückt genau einen Regelzustand aus, der taktisch relevant ist.

### Badge-Vokabular

**Persistente Badges** (rundenübergreifend):

| Badge | Zustand |
|---|---|
| `IN MELEE` | Einheit ist im Nahkampf gebunden |
| `IN RESERVE` | Einheit in Reserve gehalten |

**Ephemere Bewegungs-Badges** (mutex, Zugstart → reset zu `STATIONARY`):

| Badge | Bedeutung | Einschränkungen |
|---|---|---|
| `STATIONARY` | Hat sich nicht bewegt (Zugstart-Default) | keine |
| `MOVED` | Normal bewegt | keine |
| `ADVANCED` | Vorgestoßen | ✗ Schuss (außer Assault), ✗ Charge |
| `RETREATED` | Aus Nahkampf zurückgezogen — löscht `IN MELEE` | ✗ Schuss, ✗ Charge |
| `CHARGED` | Angestürmt — impliziert `IN MELEE` | kämpft zuerst |

**Aktion-Badges** (additiv, Zugstart → reset):

| Badge | Gesetzt wann |
|---|---|
| `SHOT` | nach Schussauflösung |
| `FOUGHT` | nach Kampfauflösung; ersetzt `CHARGED` in Anzeige |

### Implementierungsschritte

- [x] `"normal"` → `"moved"` umbenennen: `unit_mutations`, `movementPhase`, `_common`, Tests
- [x] `turn_flags["shot"]` + `turn_flags["fought"]` nach Auflösung setzen
- [x] `state_badges_html()` — FOUGHT > CHARGED Priorität; SHOT additiv; IN MELEE bei CHARGED unterdrücken
- [x] `_reset_turn_state()` — `my_will_be_done_active` ebenfalls zurücksetzen (Bug)
- [x] `apply_damage()` — bei `destroyed=True` melee-Partner `in_melee` auto-clearen
- [x] `docs/spec/unit_states.md` — Flussdiagramme + Badge-Vokabular

---

## 4b — armyCard + unitCard Redesign ✅

**Abgeschlossen.**

- [x] `unitCard.py` — neue Layout-Reihenfolge: LP/Modell-Bars → Name-Button → State-Badges → Keywords
- [x] `unitCard.py` — `st.container(border=True)`; Hauptfraktions-Keyword gefiltert; Keyword-Highlighting
- [x] `armyCard.py` — Border, Faction-Badge + Subfaction-Badge
- [x] `armyCard.py` — TriggeredAbility-Buttons (phasenabhängig sichtbar)
- [x] `Ability.ability_type: str` — `"triggered"` | `"activated"` ins Datenmodell
- [x] YAMLs aktualisiert, Loader erweitert
- [x] `apply_living_metal()` von `commandPhase.py` → `unit_mutations.py` verschoben
- [x] 9 neue Tests — gesamt 209 grün

---

## 4c — Ability Engine Refactoring ✅

**Abgeschlossen** (commit `a884733`).

- [x] `Condition.needs_healing: bool`, `Effect.revive: bool` ins Datenmodell
- [x] `check_conditions()` + `execute_effect()` Dispatcher in `ability_engine.py`
- [x] `heal_unit(revive=)` — Cap-Logik korrekt
- [x] `apply_living_metal()` gelöscht — ersetzt durch generischen Dispatcher
- [x] Living Metal YAML: `unit_not_destroyed`, `needs_healing`, `revive: false`
- [x] `armyCard.py` vollständig datengetrieben
- [x] 215 Tests grün

---

## 4d — Befehlsphase vollständig ✅

**Abgeschlossen** (commit `b734f97`).

### 4d.1 — Living Metal immer sichtbar

- [x] Ability immer in Befehlsphase anzeigen; Caption wenn keine eligible units

### 4d.2 — Kommandoprotokolle (Necrons)

| Protokoll | Primär | Sekundär |
|---|---|---|
| Ewiger Wächter | +1 auf alle Rettungswürfe | WW1 wiederholen |
| Der hungrige Leere | +1 zum Treffen (Schuss) | +1 Stärke (Schuss) |
| Des tyrannischen Herrschers | +1 Führung | WW1 bei Treffen/Wunden (NK) |
| Des plötzlichen Sturms | +1 Bewegung | Vormarsch + Charge erlaubt |
| Unaufhörlicher Legionen | RP neu würfeln | +1 Modell pro RP |

- [x] `data/wh40k_9e/necrons/command_protocols.yaml` — 5 Protokolle
- [x] `src/gameObjects/command_protocol.py` — `CommandProtocol` Dataclass
- [x] `src/gameMechanic/commandPhase.py` — `_render_command_protocols()` für Necrons
- [x] `src/uiLayout/gameProtocoll.py` — "Command Protocol" Tab

### 4d.3 — RP-Trigger (Reanimationsprotokolle) — VERSCHOBEN

RP-Trigger gehört in Schuss-, Angriffs- und Nahkampfphase. Wird separat implementiert.

---

## 4e — Bewegungsphase vollständig ✅

**Abgeschlossen** (commit `291e698`).

- [x] **In-Melee-Lock** — Move/Advance disabled wenn `in_melee=True`
- [x] **Post-Retreat-Lock** — alle Bewegungsoptionen disabled nach `retreated=True`
- [x] Bug-Fix: Retreat-Override durch nachfolgendes "Stay Stationary" verhindert
- [x] Buttons vertikal, Labels: "Move" / "Advance" / "Stay Stationary" / "Retreat"
- [x] `_render_reinforcements_step` — immer sichtbarer Abschnitt für Reserve-Deploy
- [x] Phasennamen im Header auf Englisch
- [x] `docs/spec/unit_states.md` — 4 Sektionen inkl. passive Spieler-Zustände
- [x] 15 Integrationstests grün (`test_movement_transitions.py`)

---

## 4f — Psychic Phase ✅

**Abgeschlossen** (commit `625a0ff`).

- [x] YAML: Weirdboy + Wurrboy in `orks/army.yaml`; Canoptek Spyder in `necrons/army.yaml`
- [x] Pure functions: `has_psyker()`, `can_deny()`, `is_perils()`, `smite_damage_die()`, `deny_succeeds()`
- [x] Smite-Manifest: 2D6 → Ergebnis prüfen (< 5 fail, ≥ 5 ok, 2/12 Perils)
- [x] Perils: W3-Schadenseingabe + `apply_damage(mortal=True)` am Psyker selbst
- [x] Inaktive Spalte: Bannversuch via `can_deny()` + 2D6 > Manifestwurf
- [x] Gloom Prism: einmal-pro-Phase (`psychic_denies_used`)
- [x] 22 Tests grün (`tests/gameMechanic/test_psychic_phase.py`)
- [x] `docs/spec/processes.md`: P-10 Bewegungsphase, P-11 Kommandoprotokolle, P-12 Psychic Phase

### 4f.1 — Psychic Phase Nachbesserungen ✅

- [x] `_render_psi_result()`: Schritt-für-Schritt-Hinweis bei fehlendem Ziel
- [x] CAST-Badge: `("#9060d0", "#180a28")` (Violett), additiv wie SHOT
- [x] `cast_eligibility(unit_state)` — Retreated-Sperre + Already-cast-Sperre
- [x] WC-Eskalation: `psi_attempts_this_phase` — Smite WC steigt pro Versuch um 1

#### 4f.1.c — Blessing-Flow (befreundetes Ziel) ⬜

Scope für spätere Session (nach Ziel 5):
- Psikräfte vom Typ Blessing benötigen eine **befreundete** Einheit als Ziel
- Buff-Effekt anwenden (z.B. +1 Bewegung, +1 Attacke) + neues Badge
- Braucht neuen Effect-Typ `"blessing"` in der Ability Engine (Thema Ziel 5)

---

## 4g — Angriffsphase (Charge Phase) ✅

**Abgeschlossen** (commit `fa224f3`).

### 4g.1 — Melee-Beziehungsgraph

```python
# Datenformat: list[list[str, str]] — [faction, uid]
"melee_with": [["Orks", "boyz_mob"], ["Orks", "gretchin"]]
```

- [x] `enter_melee()`, `leave_melee()`, `leave_melee_pair()` korrekt implementiert
- [x] `in_melee`-Flag immer aus `len(melee_with) > 0` ableiten

### 4g.2 — Charge-Eligibility

- [x] Sperrung wenn `advanced OR retreated OR in_melee`

### 4g.3 — Charge-Flow + Melee-Engagement-Anzeige

- [x] Charge-UI: Einheit wählen → Target(s) via `▷` → "Charge Successful" / "Charge Failed"
- [x] `render_melee_engagements()` mit Break-Buttons in `uiLayout/_common.py`

### 4g.4 — Heroische Intervention

- [x] HI-Sektion in der **inaktiven** Spielerspalte
- [x] Nur CHARACTER-Einheiten; `turn_flags["heroic_intervened"]`

### 4g.5 — `can_shoot()` für VEHICLE/MONSTER (Big Guns Never Tire)

- [x] VEHICLE/MONSTER im Melee: Sperre aufgehoben, Warnung statt Block

### 4g.6 — "Nicht in befreundeten Nahkampf schießen"

- [x] `target_in_friendly_melee()` — Ausnahme für VEHICLE/MONSTER

### 4g.7 — Tests

- [x] 25 neue Tests `test_charge_phase.py` — 280 gesamt

---

## 4h — Moralphase ✅

- [x] D6 + Verluste vs. Leadership → bei Fehlschlag: Modelle fliehen
- [x] `moralePhase.py` — Render-Logik
- [x] `flee_models()` in `unit_mutations.py` — semantisch getrennt von Kampfverlusten
- [x] `fled_models_this_turn` im Unit-State — separat zu `lost_models_this_turn`
- [x] Schwellenwertanzeige mit Rechenweg (D6 ≥ X → schlägt fehl)
- [x] Bestanden/Fehlgeschlagen-Buttons + Modellzahl-Eingabe bei Fehlschlag
- [x] Protokolleintrag: „X Modelle geflohen" (eigener Log-Typ)
- [x] 13 Tests (`test_morale_phase.py`) — 300 gesamt
