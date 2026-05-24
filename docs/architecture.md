# Arbiter — Architektur

## Struktur

```
prototype/
  app.py      ← Entry Point: set_page_config() + main()
  models.py   ← Weapon, UnitData, NECRON_UNITS, ORK_UNITS, PHASES
  engine.py   ← Spiellogik (Würfeln, Schaden, State-Management)
  ui.py       ← Alle UI-Komponenten und Phasen-Renderer

data/
  wh40k_9e/   ← YAML-Rohdaten (für Ziel 4)
```

## Module

| Datei | Inhalt |
|-------|--------|
| `models.py` | `Weapon`, `UnitData` Dataclasses; `NECRON_UNITS`, `ORK_UNITS`, `PHASES` |
| `engine.py` | `parse_dice`, `wound_threshold`, `resolve_attack`, `apply_damage`, `heal_unit`, `add_log`, `init_state`, `reset_game`, `next_phase` |
| `ui.py` | `unit_card`, `_shooting_ui`, alle `phase_*`-Funktionen, `PHASE_RENDERERS`, `main` |
| `app.py` | `st.set_page_config()` + `from ui import main; main()` |

## Starten

```bash
streamlit run prototype/app.py
```

## Datenfluss

```
models.py          engine.py               ui.py
──────────         ─────────               ─────
UnitData    ──→    resolve_attack   ──→    phase_shooting()
NECRON_UNITS ──→   apply_damage     ──→    unit_card()
PHASES       ──→   next_phase       ──→    main()
                   st.session_state ←──→   (shared state)
```
