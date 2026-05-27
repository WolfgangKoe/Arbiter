# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/architecture.md` — aktualisiert: Colour System, session_state Schema, Stratagem-Modell
3. `docs/ui_layout.md` — aktualisiert: §7 gameActionsArea (3-Section), §8 gameProtocoll (Tabs)
4. `docs/processes.md` — **neu**: P-01…P-07 Mermaid-Prozessdiagramme
5. `src/uiLayout/gameActionsArea.py` — refactored: firstPlayerArea / secondPlayerArea / DisplayArea
6. `src/uiLayout/unitCard.py` — refactored: kein Expander, kein Statsblock, einzelner Selector-Button
7. `src/gameMechanic/commandPhase.py` — Referenz für Ziel 3-Pattern

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.
Starten: `streamlit run src/app.py`
Aktueller Branch: `dev`

```
src/
  app.py              ← Entry Point (unverändert)
  engine.py           ← Game Logic + State Init
  constants/
    colors.py         ← Tailwind v3 Farbkonstanten (neu)
  uiLayout/
    gameHeader.py / armyList.py / armyCard.py / detachmentCard.py
    unitCard.py           ← refactored: kein Expander, ❤-LP-Bar, ⬡-Modell-Bar
    gameActionsArea.py    ← refactored: firstPlayerArea | secondPlayerArea + DisplayArea
    gameProtocoll.py      ← refactored: Tabs CommandProtocol | Stratagems
  gameObjects/
    ability.py            ← Trigger.stage Feld hinzugefügt
    stratagem.py          ← neu: Stratagem + stratagem_visibility()
    unit.py / weapon.py / faction_property.py / loader.py
  gameMechanic/
    __init__.py
    ability_engine.py     ← check_trigger, check_conditions, get_triggered_abilities
    commandPhase.py       ← apply_living_metal, resolve_command_start, render_actions_command

data/wh40k_9e/
  necrons/army.yaml + faction_abilities.yaml + unit_abilities.yaml + subfaction_abilities.yaml
  orks/army.yaml + faction_abilities.yaml
  _shared/detachment_types.yaml

tests/
  gameObjects/test_loader.py / test_ability.py
  engine/test_engine.py
  gameMechanic/test_ability_engine.py / test_command_phase.py
  — Total: 73 Tests, alle grün
```

---

## Was in dieser Session erarbeitet wurde

### Architektur-Update (vollständig umgesetzt)

**UI-Layout:**
- `gameActionsArea` intern: `firstPlayerArea | secondPlayerArea` (50/50) + `gameActionDisplayArea` (full width)
- `gameProtocoll` jetzt Tabs: `CommandProtocol | Stratagems`
- `unitCard`: Expander entfernt, Stats-Tabelle entfernt, Wundbuttons entfernt
  - Einziger Button: Einheitenname (Selektor)
  - Eigene Einheit → `selected_unit`, Gegner → `selected_target`
  - Im Setup: Klick zeigt Datenblatt (Stats + Waffen + Abilities) in DisplayArea
- Wundbuttons jetzt in PlayerArea des betroffenen Spielers (nicht mehr auf unitCard)

**Neue Dateien:**
- `src/constants/colors.py` — Tailwind-v3-Farbpaletten (Emerald/Neutral/Amber/Red/Blue) mit semantischen Aliases
- `src/gameObjects/stratagem.py` — Stratagem-Dataclass + `stratagem_visibility()` (4 Zustände inkl. „bereits eingesetzt")
- `docs/processes.md` — P-01 bis P-07 Mermaid-Prozessdiagramme

**Datenmodell:**
- `Trigger.stage: str = "active"` — Phasenstadium für Ability-Trigger
- YAML-Dateien aktualisiert mit `stage`-Feld
- `session_state` neue Felder: `phase_stage`, `active_effect`, `my_will_be_done_active`, `active_buffs`, `models_lost_since_last_rp`

---

## Nächster konkreter Schritt: Ziel 3 — Shooting + Fight mit Ability-System

### Parallelisierbarkeit

Ziel 3 besteht aus zwei unabhängigen Strängen, die parallel implementiert werden können:

**Strang B — Spiellogik (abhängig von abgeschlossenem Architektur-Refactoring ✅):**

| Feature | Datei | Beschreibung |
|---|---|---|
| `resolve_attack()` mit MWBD | `engine.py` | `active_buffs` prüfen, Trefferwurf +1 wenn MWBD aktiv |
| `shootingPhase.py` (neu) | `gameMechanic/` | Shooting-Logik + RP-Trigger |
| `fightPhase.py` (neu) | `gameMechanic/` | Fight-Logik + RP-Trigger |
| UI Shooting in PlayerArea | `gameActionsArea.py` | Angreifer-Area + Ziel-Area |
| UI Fight in PlayerArea | `gameActionsArea.py` | Nahkampf-Area |
| RP-UI in PlayerArea | `gameActionsArea.py` | D6-Pool + Bestätigung im inactive PlayerArea |

**Strang C — Stratagem-Architektur (unabhängig von B, braucht YAML-Daten):**

| Feature | Datei | Beschreibung |
|---|---|---|
| `necrons/stratagems.yaml` | `data/` | Skeleton mit 2–3 Necron-Stratagems |
| YAML-Loader für Stratagems | `gameObjects/loader.py` | `load_stratagems()` |
| Stratagems-Tab füllen | `gameProtocoll.py` | Echte GO-Liste statt Placeholder |

### Reanimation Protocols Mechanik (Strang B, detailliert)

Trigger: Nach jedem feindlichen Angriff (Shooting / Fight), wenn Modelle zerstört
wurden aber die Einheit nicht vollständig vernichtet ist.

```
Ablauf:
1. models_lost_since_last_rp → Anzahl LP der zerstörten Modelle = RP-Pool
2. Für jedes LP im Pool: W6 würfeln → bei 5+ wird 1 LP in den "healed pool"
3. Wenn healed_pool ≥ wounds_per_model: Modell zurückgekehrt, models +1,
   current_wounds += wounds_per_model, healed_pool -= wounds_per_model
4. Their Number Is Legion: RP-Würfe von 1 wiederholen (für Warriors)
```

**UI-Entscheidung (aus Session-Diskussion):**
Option B (Halbmanuell): App zeigt wie viele Würfel, Nutzer klickt "X LP gerettet".

### My Will Be Done Effekt (Strang B)

```python
# In resolve_attack() — wenn Angreifer my_will_be_done_active:
if atk_state.get("my_will_be_done_active") and not weapon.is_melee:
    hits = sum(1 for r in hit_rolls if r >= skill - 1)  # +1 zum Trefferwurf
```

Oder sauberer: `active_buffs: list[str]` in unit_state → `resolve_attack()` liest diese.

### Neue Dateien für Ziel 3

| Datei | Inhalt |
|---|---|
| `src/gameMechanic/shootingPhase.py` | `resolve_shooting()` + `render_actions_shooting()` |
| `src/gameMechanic/fightPhase.py` | `resolve_fight()` + `render_actions_fight()` |
| `tests/gameMechanic/test_shooting_phase.py` | Unit-Tests Shooting |
| `tests/gameMechanic/test_fight_phase.py` | Unit-Tests Fight |
| `data/wh40k_9e/necrons/stratagems.yaml` | Skeleton (Strang C) |

---

## Offene Designfragen

1. **RP-UI** (Ziel 3): Bestätigt: Option B — App zeigt Würfelanzahl, Nutzer bestätigt X gerettete LP.

2. **My Will Be Done Reset**: Am Start der nächsten Command Phase zurücksetzen
   → in `resolve_command_start()` oder `_reset_turn_state()`.

3. **Command Protocols** (Ziel 4): 5 Protokolle, 2 Direktiven je, 1 pro Runde aktiv.
   Benötigt eigene YAML + UI.

4. **Stratagem-System** (Ziel 4 / Strang C): CP-Kosten, Timing-Bedingungen.
   Datenmodell `gameObjects/stratagem.py` ist fertig. YAML + Loader fehlen noch.

5. **Phase-Stage-Logik** (Ziel 3+): `phase_stage` ist im session_state vorhanden.
   Die tatsächliche Weiter-Button-Logik (Start → Active → End) ist noch nicht implementiert.
   Wird in Ziel 3 benötigt (RP triggert am Ende der Shooting/Fight-Phase).

6. **Setup-Screen** (mittelfristig): Formales Setup mit Spielgröße, Missionstyp, OVP/OCP.
   Aktuell: einfacher Setup-Screen mit First-Player-Auswahl + Deployment.

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
| **Architektur-Update** — UI-Refactoring, Farben, Stratagem-Modell, Prozessdoku | ✅ fertig |
| **Ziel 3 — Shooting + Fight (RP, MWBD-Effekt)** | ⏳ nächster Schritt |
| Ziel 4 — Command Protocols + Stratagems | ⬜ später |
