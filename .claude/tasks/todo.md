# Todo — Arbiter

## Modulstruktur

`engine.py` importiert Streamlit direkt — `apply_damage`/`heal_unit` schreiben in
`st.session_state`. Pure functions nötig für Unit-Tests.

```
src/
  domain/
    models.py   ← Unit, Weapon, PHASES  (pure, kein Streamlit)
    combat.py   ← parse_dice, wound_threshold, resolve_attack
  session/
    state.py    ← init_state, reset_game, apply_damage, heal_unit, next_phase, adjust_vp/cp
  ui/
    theme.py    ← CSS_THEME
    unit_card.py
    phases.py   ← PHASE_RENDERERS, phase_*
    layout.py   ← main(), _score_group()
```

- [ ] `src/domain/combat.py` extrahieren
- [ ] `src/session/state.py` extrahieren
- [ ] `src/ui/` aufteilen
- [ ] `engine.py` und `ui.py` entfernen

---

## YAML-Datenquellen

- [ ] `data/wh40k_9e/necrons/units.yaml` — Kampfstats (M/T/Sv/W/Ld/OC/Invuln)
- [ ] `data/wh40k_9e/orks/units.yaml` — Kampfstats
- [ ] `src/session/army_loader.py`: generischer YAML-Loader → `list[Unit]`
- [ ] `NECRON_UNITS`/`ORK_UNITS` aus `models.py` entfernen

---

## HP-Anzeige Multi-Modell-Einheiten

Offene Designfrage: Wunden bei Einheiten mit mehreren Modellen und mehreren Wunden pro Modell.

- Option A: `Warriors: 8/10 Modelle` (Balken = Modelle)
- Option B: `Skorpekh: 5/9 W` (Balken = Gesamtwunden)
- Option C: `2 Modelle · letztes: 2/3 W` (kombiniert)

→ Entscheidung offen.

---

## Phasen-Logik

- [ ] Fernkampfphase: vollständiger Angriffs-Flow (Einheit → Waffe → Ziel → Würfeln)
- [ ] Nahkampfphase: Nahkampf-Sequenz
- [ ] Moralphase: Leadership-Test mit Modell-Verlust
- [ ] Befehlsphase: CP-Ausgabe für Strategeme
