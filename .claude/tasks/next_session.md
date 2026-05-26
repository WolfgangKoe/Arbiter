# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — aktuelle Projektziele
3. `docs/architecture.md` — Zielarchitektur
4. `src/uiLayout/unitCard.py` — neues unitCard-Layout (fertig)
5. `src/gameObjects/loader.py` + `src/gameObjects/unit.py` — fertige gameObjects-Grundlage
6. `src/uiLayout/gameActionsArea.py` — Phase-Renderer (Ziel der nächsten Ziele)

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.
Starten: `streamlit run src/app.py`

```
src/
  app.py              ← Entry Point: init_state + render_game_header + 3-Spalten-Layout
  uiLayout/           ← Alle UI-Komponenten (1A fertig)
    gameHeader.py     ← CSS, VP/CP-Stepper (VP-Step=5, CP-Step=1), Phase-Nav
    armyCard.py       ← Fraktions-Header (hardcoded Nephrekh/Bad Moons)
    unitCard.py       ← Neues Layout: Name-Button (Select-Trigger), Keywords, LP/Model-Bars, Badges, Expander
    detachmentCard.py ← Detachment-Header + Units-Liste (ohne Rollengroupierung)
    armyList.py       ← armyCard + detachmentCard
    gameActionsArea.py ← Phase-Dispatcher (alle phase_* Renderer aus alt-ui.py)
    gameProtocoll.py  ← Setup-Summary (Stub)
  gameObjects/        ← Pure Python, kein Streamlit (1B fertig)
    unit.py           ← Unit Dataclass (neue Felder: id, name_en, keywords, models_min/max, bs, ws, ...)
    weapon.py         ← Weapon Dataclass (alle Werte als str)
    faction_property.py ← FactionProperty Dataclass
    detachment.py     ← Detachment + DetachmentType + SlotConstraint Dataclasses
    loader.py         ← load_army(), load_faction_properties(), load_detachment_types()
  engine.py           ← UNVERÄNDERT (game logic)
  models.py           ← UNVERÄNDERT (alte Unit/Weapon Klassen + hardcodierte Listen)
  ui.py               ← Deprecated (nur Kommentar-Zeile)

data/wh40k_9e/
  necrons/
    army.yaml         ← NEU: 5 Necron-Einheiten im gameObjects-Format
    faction_properties.yaml ← Living Metal, Reanimation Protocols
    subfaction_properties.yaml ← Nephrekh Translocation Beams
  orks/
    army.yaml         ← NEU: 6 Ork-Einheiten im gameObjects-Format
  _shared/
    detachment_types.yaml ← Patrol, Battalion, Brigade, Spearhead, Outrider, Vanguard, Air Wing

tests/
  gameObjects/
    test_loader.py    ← 9 Tests (alle grün)
```

---

## Was in dieser Session erarbeitet wurde

### Ziel 1A — `uiLayout/` Struktursplit ✅

- `src/ui.py` aufgeteilt in 7 `uiLayout/` Module
- `app.py` auf neue Imports umgestellt
- Neues `unitCard`-Layout: Name als Select-Trigger-Button (aktiver Spieler), Keywords als Badges, LP/Model-Fortschrittsbalken, State-Badges, collapsible Phase-Area mit Stats + Damage-Buttons + phasenspezifische Info
- VP-Stepper auf Step=5 geändert

### Ziel 1B — `gameObjects/` Foundation ✅

- Alle 4 Dataclasses erstellt (Unit, Weapon, FactionProperty, Detachment)
- YAML-Loader erstellt (load_army, load_faction_properties, load_detachment_types)
- 5 YAML-Datendateien erstellt (Necrons army, Orks army, Necron faction properties, subfaction properties, shared detachment types)
- 9 Unit-Tests, alle grün
- `models.py` unverändert (Migration auf gameObjects folgt in Ziel 2)

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Grundstruktur & Layout | ✅ fertig |
| Einheitenstatus (Wundverwaltung) | ✅ fertig |
| Durchstich (Phasenstruktur, State, Zentralbereich) | ✅ fertig |
| **Ziel 1A — uiLayout/ Struktursplit** | ✅ fertig |
| **Ziel 1B — gameObjects/ Foundation** | ✅ fertig |
| Ziel 2 — commandPhase | ⏳ bereit zum Starten |
| Ziel 3 — Combat Loop | ⬜ nach 2 |

---

## Nächster konkreter Schritt

**Ziel 2 — `gameMechanic/` Einstieg: Command Phase**

### Was Ziel 2 umfasst (aus docs/goals.md)

- `gameMechanic/state.py` — session_state-Schema, `init_state`, `reset_game`, `next_phase` (aus engine.py herauslösen)
- `gameMechanic/protocol.py` — Log-Append, Unveränderlichkeit nach Zug-Ende
- `gameMechanic/commandPhase.py` — BP-Bonus, Living Metal Trigger (via gameObjects FactionProperty), CP-Verwaltung
- `uiLayout/gameActionsArea.py` — Layout für commandPhase fertigstellen (aktuell hardcoded `_central_command_actions`)
- Select-Logik in `unitCard.py` vollständig verdrahten (aktuell Stub bei Gegner-Einheiten)
- `gameProtocoll.py` — Log-Einträge für commandPhase definieren und anzeigen
- Tests für commandPhase (state transitions, FactionProperty-Trigger)

### Wichtige offene Punkte vor Ziel 2 Start

1. **models.py Migration**: `NECRON_UNITS` und `ORK_UNITS` sollen aus YAML geladen werden (aktuell noch hardcoded). Das passiert am besten parallel zu Ziel 2, wenn `uiLayout/` auf `gameObjects.Unit` umgestellt wird.

2. **gameObjects.Unit ↔ models.Unit Inkompatibilität**: Die alten Felder (`uid`, `count`, `faction_keywords`, `other_keywords`, `skill`) unterscheiden sich von den neuen (`id`, `models_max`, `keywords`, `bs`). Dieser Schnitt muss koordiniert werden (entweder Compat-Properties auf gameObjects.Unit, oder alle uiLayout-Module auf neue Felder umstellen).

3. **Living Metal Trigger**: In commandPhase soll `load_faction_properties("necrons")` die Properties holen und für jede Einheit mit dem Keyword "Living Metal" +1 Wunde vergeben. Die `engine.heal_unit()` Funktion bleibt dabei.

---

## Wichtige Designentscheidungen (aus letzter Session)

1. **Select-Trigger**: Name-Button (aktiver Spieler) togglet `selected_unit`. Target-Button (Gegner) bleibt im Expander.
2. **Select erst nach Setup**: `phase_key != "setup"` ist bereits implementiert.
3. **LP-Bar bleibt sichtbar**: immer, ohne Collapse.
4. **gameActionsArea = aktuell**: alle phase_* Renderer aus alt-ui.py, keine neue Logik.
5. **VP-Step = 5, CP-Step = 1**: implementiert.

---

## Offene Designfragen

Dokumentiert in `docs/architecture.md` — Abschnitt "Open Design Questions".
Kritischste für Ziel 2: Fragen #5 (Log-Schema) und #6 (CP-Startwerte).
