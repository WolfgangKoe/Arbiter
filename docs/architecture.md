# Arbiter — Architektur

## Aktueller Stand (`src/`)

```
src/
  app.py      ← Entry Point: set_page_config() + main()
  models.py   ← Weapon, Unit, NECRON_UNITS, ORK_UNITS, PHASES
  engine.py   ← Spiellogik (Würfeln, Schaden, State-Management, VP/CP)
  ui.py       ← Alle UI-Komponenten, Header, Phasen-Renderer, CSS-Theme

data/
  wh40k_9e/   ← YAML-Rohdaten (Waffen, Einheiten, Regeln)
```

## Module

| Datei | Inhalt |
|-------|--------|
| `models.py` | `Weapon`, `Unit` Dataclasses; `NECRON_UNITS`, `ORK_UNITS`, `PHASES` (7 Phasen) |
| `engine.py` | `parse_dice`, `wound_threshold`, `resolve_attack`, `apply_damage`, `heal_unit`, `adjust_vp`, `adjust_cp`, `init_state`, `reset_game`, `next_phase` |
| `ui.py` | `CSS_THEME`, `unit_card`, `_score_group`, alle `phase_*`-Funktionen, `PHASE_RENDERERS`, `main` |
| `app.py` | `st.set_page_config()` + `from ui import main; main()` |

## Starten

```bash
streamlit run src/app.py
```

## Phasen

| Anzeigename | Schlüssel |
|-------------|-----------|
| Befehlsphase | `command` |
| Bewegungsphase | `movement` |
| Psiphase | `psychic` |
| Fernkampfphase | `shooting` |
| Angriffsphase | `charge` |
| Nahkampfphase | `fight` |
| Moralphase | `morale` |

## Datenfluss

```
models.py         engine.py                ui.py
──────────        ─────────                ─────
Unit         ──→  resolve_attack    ──→    phase_shooting()
NECRON_UNITS ──→  apply_damage      ──→    unit_card()
PHASES       ──→  next_phase        ──→    main()
                  adjust_vp/cp      ──→    _score_group()
                  st.session_state ←──→   (shared state)
```

## Geplante Zielarchitektur

```
src/
  app.py
  domain/
    models.py       ← Unit, Weapon, PHASES  (pure, kein Streamlit)
    combat.py       ← parse_dice, wound_threshold, resolve_attack
  session/
    state.py        ← init_state, reset_game, apply_damage, heal_unit, next_phase, adjust_vp/cp
  ui/
    theme.py        ← CSS_THEME
    unit_card.py    ← unit_card()
    phases.py       ← PHASE_RENDERERS, phase_*-Funktionen
    layout.py       ← main(), _score_group()

data/
  wh40k_9e/
    necrons/        ← units.yaml  (generischer YAML-Loader)
    orks/           ← units.yaml
```

Armeedaten werden aus `models.py` in YAML migriert, sobald ein generischer
Loader implementiert ist. `engine.py` importiert aktuell Streamlit direkt —
`apply_damage`/`heal_unit` schreiben in `st.session_state`. Für Unit-Tests
müssen diese zu pure functions (`-> dict`) werden.
