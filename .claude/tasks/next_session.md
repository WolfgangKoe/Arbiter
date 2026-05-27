# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/architecture.md` — Zielarchitektur (Abschnitt "Component Responsibilities" + "session_state Schema")
3. `src/gameMechanic/ability_engine.py` + `src/gameMechanic/commandPhase.py`
4. `src/engine.py` — aktueller Stand (vollständig auf gameObjects migriert)
5. `src/uiLayout/gameActionsArea.py` — für den Einstieg in Ziel 3

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.
Starten: `streamlit run src/app.py`
Aktueller Branch: `dev`

```
src/
  app.py              ← Entry Point
  engine.py           ← Game Logic (gameObjects-native, models.py deprecated)
  models.py           ← Deprecated (nur noch als Referenz, nicht mehr importiert)
  uiLayout/
    gameHeader.py / armyCard.py / unitCard.py / detachmentCard.py / armyList.py
    gameActionsArea.py  ← Phase-Dispatcher (alle Phasen hier)
    gameProtocoll.py
  gameObjects/
    ability.py / unit.py / weapon.py / faction_property.py / detachment.py / loader.py
  gameMechanic/
    __init__.py
    ability_engine.py   ← check_trigger, check_conditions, get_triggered_abilities
    commandPhase.py     ← apply_living_metal, render_actions_command

data/wh40k_9e/
  necrons/army.yaml + faction_abilities.yaml + unit_abilities.yaml
         + subfaction_abilities.yaml
  orks/army.yaml + faction_abilities.yaml
  _shared/detachment_types.yaml

tests/
  gameObjects/test_loader.py    ← 10 Tests (grün)
  gameObjects/test_ability.py   ← 12 Tests (grün)
  engine/test_engine.py         ← 31 Tests (grün)
  gameMechanic/test_ability_engine.py  ← 14 Tests (grün)
  gameMechanic/test_command_phase.py   ←  8 Tests (grün)
  — Total: 73 Tests, alle grün
```

---

## Was bisher erarbeitet wurde

### Ziel 2 — commandPhase ✅ (diese Session)

**Ability-System vollständig implementiert:**

- `gameObjects/ability.py` — Datenmodell: `Ability`, `Trigger`, `Condition`, `Effect`
- `gameObjects/unit.py` — `rules: list[str]` Feld hinzugefügt
- `gameObjects/faction_property.py` — `FactionProperty = Ability` (Alias)
- `gameObjects/loader.py` — `load_faction_abilities()`, `load_unit_abilities()`,
  `load_subfaction_abilities()`, `_ability_from_dict()`, `rules`-Feld beim Unit-Loading

**YAML-Dateien neu/umgebaut:**
- `necrons/faction_abilities.yaml` — Living Metal + Reanimation Protocols
- `necrons/unit_abilities.yaml` — My Will Be Done + Resurrection Orb
- `necrons/subfaction_abilities.yaml` — Nephrekh Translocation Beams
- `orks/faction_abilities.yaml` — leer (keine Faction Abilities im Scope)
- `necrons/army.yaml` — `rules`-Felder zu allen 5 Einheiten

**gameMechanic-Modul:**
- `ability_engine.py` — `check_trigger()`, `check_conditions()`, `get_triggered_abilities()`
- `commandPhase.py` — `apply_living_metal()`, `resolve_command_start()`,
  `render_actions_command()` (Streamlit-UI)

**Living Metal Semantik (wichtig!):**
```python
max_alive = unit_state["models"] * unit.wounds  # models_remaining, NICHT models_max
# Verhindert, dass zerstörte Modelle zurückgezählt werden
```

**Vollständige Migration von `models.py` → `gameObjects`:**
- `engine.py` — PHASES jetzt dort definiert; `_NECRON_UNITS`/`_ORK_UNITS` via `load_army()`
- Session-State-Keys jetzt volle IDs: `"wh40k_9e.necrons.unit.overlord"` statt `"overlord"`
- Alle 5 UI-Dateien migriert: `gameActionsArea`, `armyList`, `detachmentCard`, `unitCard`, `gameHeader`
- Feldnamen: `unit.id`, `unit.name_en`, `unit.models_max`, `unit.invuln_save`, `w.name_en`
- `weapon.skill` gibt es nicht mehr → `int(unit.bs.rstrip('+'))` / `int(unit.ws.rstrip('+'))`

---

## Nächster konkreter Schritt: Ziel 3 — Shooting + Fight mit Ability-System

**Scope Ziel 3:**

| Feature | Beschreibung |
|---|---|
| Reanimation Protocols | Phase-reaktiv (nach feindlichem Angriff) — D6-Pool, Model-Rückholung |
| My Will Be Done Effekt | `unit_state["my_will_be_done_active"]` → +1 hit_roll in `resolve_attack()` |
| Resurrection Orb Auflösung | RP für Ziel-Einheit manuell triggern (1×/Spiel) |
| `active_buffs` im unit_state | Feld für laufende Buffs: `list[str]` |
| RP-UI | D6-Würfel pro LP zerstörter Modelle, Pool ≥ wounds → Modell zurück |

**Reanimation Protocols Mechanik (detailliert):**

Trigger: Nach jedem feindlichen Angriff (Shooting / Fight), wenn Modelle zerstört
wurden aber die Einheit nicht vollständig vernichtet ist.

```
Ablauf:
1. Zerstörte Modelle seit letztem RP → Anzahl LP der zerstörten Modelle = RP-Pool
2. Für jedes LP im Pool: W6 würfeln → bei 5+ wird 1 LP in den "healed pool"
3. Wenn healed_pool ≥ wounds_per_model: Modell zurückkehren, models_remaining +1,
   current_wounds += wounds_per_model, healed_pool -= wounds_per_model
4. Their Number Is Legion: RP-Würfe von 1 wiederholen (für Warriors)
```

Feld `models_lost_since_last_rp` im unit_state erforderlich.

**My Will Be Done Effekt:**

```python
# In resolve_attack() — wenn Angreifer my_will_be_done_active:
if atk_state.get("my_will_be_done_active") and not weapon.is_melee:
    hits = sum(1 for r in hit_rolls if r >= skill - 1)  # +1 zum Trefferwurf
```

Oder sauberer: `active_buffs: list[str]` in unit_state, den resolve_attack() liest.

**`_unit_state()` in engine.py erweitern:**
```python
"my_will_be_done_active": False,
"active_buffs": [],
"models_lost_since_last_rp": 0,
```

---

## Betroffene Dateien Ziel 3 (vorläufig)

| Datei | Änderung |
|---|---|
| `src/engine.py` | `_unit_state()` um neue Felder erweitern; `resolve_attack()` liest `active_buffs` |
| `src/gameMechanic/commandPhase.py` | My Will Be Done reset am Rundenanfang |
| `src/gameMechanic/shootingPhase.py` | neu — RP-Trigger nach Schuss |
| `src/gameMechanic/fightPhase.py` | neu — RP-Trigger nach Nahkampf |
| `src/uiLayout/gameActionsArea.py` | `phase_shooting()` + `phase_fight()` delegieren |
| `data/wh40k_9e/necrons/army.yaml` | `models_lost_since_last_rp` kein YAML-Feld (nur state) |
| Tests: 3–4 neue Dateien | |

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
| **Ziel 2 — commandPhase + Ability-System** | ✅ fertig (73 Tests grün) |
| **Ziel 3 — Shooting + Fight (RP, MWBD-Effekt)** | ⏳ nächster Schritt |
| Ziel 4 — Command Protocols + Stratagems | ⬜ später |

---

## Offene Designfragen

1. **RP-UI** (Ziel 3): Wie viel automatisieren? Optionen:
   - A) Vollautomatisch: App würfelt, zeigt Ergebnis, updated state
   - B) Halbmanuell: App zeigt wie viele Würfel, Nutzer klickt "X LP gerettet"
   - C) Nur Logging: Nutzer macht alles manuell, App trackt nur model count
   → Empfehlung: B (Kompromiss, funktioniert auch ohne exakte Würfelanzahl)

2. **My Will Be Done Reset**: Am Ende jeder Command Phase zurücksetzen, oder am Ende
   des Turns? → Regeltext: "bis zum Start der nächsten Befehlsphase" → Reset in
   `_reset_turn_state()` ODER am Start der nächsten Command Phase.

3. **Command Protocols** (Ziel 4): 5 Protokolle, 2 Direktiven je, 1 pro Runde aktiv.
   Benötigt eigene YAML + UI.

4. **Stratagem-System** (Ziel 4): CP-Kosten, Timing-Bedingungen, `gameObjects/stratagem.py`.
