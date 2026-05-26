# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — aktuelle Projektziele
3. `docs/architecture.md` — Zielarchitektur
4. `src/engine.py` — Game Logic (fixes aus dieser Session beachten)
5. `src/uiLayout/unitCard.py` — neue Bar-Logik
6. `src/uiLayout/gameActionsArea.py` — Phase-Renderer (Ziel der nächsten Schritte)

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.
Starten: `streamlit run src/app.py`

```
src/
  app.py              ← Entry Point: init_state + render_game_header + 3-Spalten-Layout
  engine.py           ← Game Logic (FIXES: CP-Bug behoben, Damage-Cap korrekt)
  models.py           ← UNVERÄNDERT (alte Unit/Weapon Klassen + hardcodierte Listen)
  ui.py               ← Deprecated (nur Kommentar-Zeile)
  uiLayout/
    gameHeader.py     ← CSS, VP/CP-Stepper (VP-Step=5, CP-Step=1), Phase-Nav
    armyCard.py       ← Fraktions-Header (hardcoded Nephrekh/Bad Moons)
    unitCard.py       ← GEFIXT: LP/Modell-Bar-Logik (siehe unten)
    detachmentCard.py ← Detachment-Header + Units-Liste
    armyList.py       ← armyCard + detachmentCard
    gameActionsArea.py ← Phase-Dispatcher (alle phase_* Renderer)
    gameProtocoll.py  ← Setup-Summary (Stub)
  gameObjects/        ← Pure Python, kein Streamlit
    unit.py           ← Unit Dataclass
    weapon.py         ← Weapon Dataclass
    faction_property.py ← FactionProperty Dataclass
    detachment.py     ← Detachment + DetachmentType + SlotConstraint
    loader.py         ← load_army(), load_faction_properties(), load_detachment_types()

data/wh40k_9e/
  necrons/army.yaml + faction_properties.yaml + subfaction_properties.yaml
  orks/army.yaml
  _shared/detachment_types.yaml

tests/
  gameObjects/test_loader.py    ← 9 Tests (alle grün)
  engine/test_engine.py         ← 38 Tests (alle grün) — NEU
```

---

## Was in dieser Session erarbeitet wurde

### Bug-Fixes & Testabdeckung ✅

**Bug 1 — CP-Doppel-Award** (`engine.py:next_phase`):
`next_phase()` vergab am Ende von Orks' Zug automatisch +1 CP an beide Fraktionen,
obwohl der "Grant +1 CP"-Button in `phase_command()` das bereits manuell tut.
→ Die zwei Zeilen `cp[...] += 1` aus `next_phase` entfernt.

**Bug 2 — LP/Modell-Bar falsche Anzeige** (`unitCard.py`):
Die Bar zeigte Gesamt-LP statt Front-Modell-LP. Neue Logik:
- 1 Modell, N LP → LP-Bar nur (für das Modell)
- M Modelle, je 1 LP → Modell-Bar nur
- M Modelle, je N LP → Modell-Bar + LP-Bar (Front-Modell)

**Damage-Cap Semantik** (war in dieser Session kurz falsch, dann korrekt gestellt):
- Normaler Schaden (mortal=False) bei Mehrmodell-Einheit: immer auf Front-Modell begrenzt
  → 3 Schaden auf Warriors = 1 Modell tot (Excess verloren, per 9E-Regel)
  → 3× Schaden separat = 3 Modelle tot (je ein neuer Hit)
- Mortalwunden (mortal=True): kein Cap → können mehrere 1-LP-Modelle töten

**Neue Testdatei** `tests/engine/test_engine.py` mit 38 Tests:
- `parse_dice` (fixed, D6, 2D6, D3)
- `wound_threshold` (alle 5 Fälle)
- `apply_damage` (1-LP-Cap, Multi-LP-Cap, Mortal, Zerstörung, lost_models_tracking)
- `heal_unit` (heilen, Cap, Wiederbelebung, Modellzahl)
- `next_phase` (Phasenindex, Spielerwechsel, Runde, CP-fix, selected_unit reset)

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Grundstruktur & Layout | ✅ fertig |
| Einheitenstatus (Wundverwaltung) | ✅ fertig |
| Durchstich (Phasenstruktur, State, Zentralbereich) | ✅ fertig |
| Ziel 1A — uiLayout/ Struktursplit | ✅ fertig |
| Ziel 1B — gameObjects/ Foundation | ✅ fertig |
| Bug-Fixes + Engine-Tests | ✅ fertig (diese Session) |
| **Ziel 2 — commandPhase** | ⏳ bereit zum Starten |
| Ziel 3 — Combat Loop | ⬜ nach 2 |

---

## Nächster konkreter Schritt

**Ziel 2 — `gameMechanic/` Einstieg: Command Phase**

### Was Ziel 2 umfasst (aus docs/goals.md)

- `gameMechanic/state.py` — session_state-Schema, `init_state`, `reset_game`, `next_phase`
  (aus engine.py herauslösen)
- `gameMechanic/protocol.py` — Log-Append, Unveränderlichkeit nach Zug-Ende
- `gameMechanic/commandPhase.py` — BP-Bonus, Living Metal Trigger (via gameObjects
  FactionProperty), CP-Verwaltung
- `uiLayout/gameActionsArea.py` — Layout für commandPhase fertigstellen
- Select-Logik in `unitCard.py` vollständig verdrahten (aktuell Stub bei Gegner-Einheiten)
- `gameProtocoll.py` — Log-Einträge für commandPhase definieren und anzeigen
- Tests für commandPhase (state transitions, FactionProperty-Trigger)

### Offene Punkte vor / parallel zu Ziel 2

1. **models.py Migration**: `NECRON_UNITS` und `ORK_UNITS` sollen aus YAML geladen werden
   (aktuell noch hardcoded). Koordiniert mit uiLayout-Umstellung auf `gameObjects.Unit`.

2. **gameObjects.Unit ↔ models.Unit Inkompatibilität**: Alte Felder (`uid`, `count`,
   `faction_keywords`, `other_keywords`, `skill`) vs. neue (`id`, `models_max`, `keywords`,
   `bs`). Entweder Compat-Properties auf gameObjects.Unit, oder alle uiLayout-Module
   auf neue Felder umstellen.

3. **Living Metal Trigger**: In commandPhase soll `load_faction_properties("necrons")` die
   Properties holen und für jede Einheit mit Keyword "livingMetal" +1 Wunde vergeben.
   `engine.heal_unit()` bleibt dabei.

---

## Wichtige Designentscheidungen

1. **Damage-Cap**: normaler Schaden bleibt immer am Front-Modell (9E-Regel: Excess lost).
   Mortalwunden (mortal=True) kennen keinen Cap.
2. **CP-Vergabe**: ausschließlich manuell über "Grant +1 CP"-Button in der Befehlsphase.
   `next_phase()` vergibt kein CP.
3. **Bar-Anzeige**: 3 Varianten je nach Einheitstyp (siehe Bug 2 oben).
4. **Select-Trigger**: Name-Button (aktiver Spieler) togglet `selected_unit`.
5. **VP-Step = 5, CP-Step = 1**: implementiert in gameHeader.py.

---

## Offene Designfragen

Dokumentiert in `docs/architecture.md` — Abschnitt "Open Design Questions".
Kritischste für Ziel 2: Fragen #5 (Log-Schema) und #6 (CP-Startwerte).
