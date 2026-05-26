# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — aktuelle Projektziele (komplett neu strukturiert)
3. `docs/architecture.md` — Zielarchitektur inkl. Backend-Erkenntnisse
4. `docs/ui_layout.md` — UI-Wireframes und Komponentenspezifikation
5. `src/models.py`, `src/engine.py`, `src/ui.py` — aktueller Stand des Codes

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.
Starten: `streamlit run src/app.py`

```
src/          ← Streamlit-App (app.py, models.py, engine.py, ui.py)
data/
  wh40k_9e/  ← YAML-Katalog (necrons/, orks/)
  log/        ← game_log.json
docs/
  goals.md              ← Projektziele
  architecture.md       ← Zielarchitektur + Backend-Erkenntnisse
  ui_layout.md          ← UI-Wireframes und Komponentenspezifikation
  rules/
    schlachtrunde.md    ← WH40k 9E Grundregeln (bindend)
```

---

## Was in dieser Session erarbeitet wurde

### Planung & Dokumentation (kein Code geändert)

- **`docs/ui_layout.md`** (neu): Vollständige ASCII-Wireframes für alle 8 UI-Komponenten
  (gameHeader, armyCard, unitCard, detachmentCard, armyList, gameActionsArea, gameProtocoll)
  inkl. Properties, States, Interaktionslogik, TBDs

- **`docs/architecture.md`** (komplett neu): Zielstruktur `uiLayout/` / `gameObjects/` / `gameMechanic/`,
  Dataclass-Skelette (Unit, Weapon, FactionProperty, Detachment, Stratagem),
  session_state-Schema, Interaction-Flow, Phase-Stubs für alle 7 Phasen,
  Refactoring-Plan in 4 Phasen, Backend-Erkenntnisse

- **`docs/goals.md`** (komplett neu): 4 Ziele, Ziel 1A + 1B explizit parallel

- **`backend/`** gelöscht nach Extraktion der nützlichen Konzepte → `architecture.md`
- **`Layout_Print/`** gelöscht — alle Skizzen sind in `ui_layout.md` überführt

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Grundstruktur & Layout | ✅ fertig |
| Einheitenstatus (Wundverwaltung) | ✅ fertig |
| Durchstich (Phasenstruktur, State, Zentralbereich) | ✅ fertig |
| **Ziel 1A — uiLayout/ Struktursplit** | ⏳ bereit zum Starten |
| **Ziel 1B — gameObjects/ Foundation** | ⏳ bereit zum Starten |
| Ziel 2 — commandPhase | ⬜ nach 1B |
| Ziel 3 — Combat Loop | ⬜ nach 2 |

---

## Nächster konkreter Schritt

**Ziel 1A und 1B parallel starten** — zwei unabhängige Subagenten.

### Ziel 1A — `uiLayout/` Struktursplit (kein Behavior-Change)
`src/ui.py` → `src/uiLayout/` aufteilen:
- `gameHeader.py`, `armyCard.py`, `unitCard.py` (neues Layout per `ui_layout.md`),
  `detachmentCard.py`, `armyList.py`, `gameProtocoll.py`, `gameActionsArea.py` (Stub)
- `app.py` auf neue Imports umstellen
- Alle Tests bleiben grün

### Ziel 1B — `gameObjects/` Foundation (pure Python, kein Streamlit)
- Dataclasses: `unit.py`, `weapon.py`, `faction_property.py`, `detachment.py`
- `loader.py`: liest YAML, löst Waffen-Referenzen auf
- `data/wh40k_9e/_shared/detachment_types.yaml`
- `data/wh40k_9e/necrons/faction_properties.yaml`
- Necrons + Orks über Loader laden; hardcodierte Listen aus `models.py` entfernen
- Unit-Tests

---

## Wichtige Designentscheidungen aus dieser Session

1. **Select-Trigger**: Klick auf den Einheitennamen (nicht separater Button) → togglet `selected`-State → befüllt gameActionsArea
2. **Select erst nach Setup**: `setup_complete == True` muss gesetzt sein
3. **LP-Bar bleibt gekoppelt**: wounds + models bleiben zusammen wie jetzt; nur Wound-Change-Buttons wandern in gameActionsArea wenn Einheit selektiert
4. **gameActionsArea = freie Fläche** bis gameMechanic pro Phase konzipiert ist; in 1A nur Stub-Container
5. **VP-Stepper Intervall = 5**, CP-Intervall = 1 (beide Spieler gleich)
6. **gameHeader zeigt zusätzlich**: gameSize (Patrol/Incursion/Strike Force/Onslaught), gameType (matched/open/crusade), initial CP abhängig von gameSize
7. **gameProtocoll**: innerhalb laufenden Zuges zurück navigierbar; nach Zugende frozen
8. **WeaponProfile aus backend/**: alle Werte als `str` (nicht `int`) — korrekt wegen Würfelausdrücken
9. **rule_eligibility-Logik aus backend/** nicht neu schreiben — direkt adaptieren für Keyword-Dispatcher

---

## Offene Designfragen

Dokumentiert in `docs/architecture.md` — Abschnitt "Open Design Questions".
Wichtigste für die nächste Session: keine — 1A und 1B sind vollständig spezifiziert.
