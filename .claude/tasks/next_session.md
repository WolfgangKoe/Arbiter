# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py`
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — vollständiger Plan, insbesondere Ziel 4a
3. `src/uiLayout/_common.py` — `state_badges_html()` für Badge-Logik
4. `src/gameMechanic/unit_mutations.py` — `set_movement_status`, `apply_damage`
5. `src/gameMechanic/shootingPhase.py` — `_render_display()` für SHOT-Flag
6. `src/gameMechanic/fightPhase.py` — `_render_display()` für FOUGHT-Flag
7. `src/gameMechanic/game_state.py` — `_reset_turn_state()`
8. `tests/uiLayout/test_common.py` — bestehende Badge-Tests

---

## Was in dieser Session gemacht wurde

### Blocker-Fixes (alle committed)

- **Blocker 1** — `parse_dice()` crasht auf W-Notation: Fix + `+N`-Modifier-Support
- **Blocker 2** — `in_melee`-Check in `can_shoot()`: war bereits implementiert, keine Änderung nötig
- **Blocker 3** — Nahkampfphase startet mit falschem Spieler: `⚔ Fight Priority`-Badge für Nicht-Aktiv-Spieler
- **Neu** — `resolve_weapon_strength()` für Träger/+1/x2-Notation
- **182 Tests, alle grün**

### Konzeptarbeit (nicht committed, nur Doku)

- Vollständiges Badge/State-Modell erarbeitet (siehe `docs/goals.md` → Ziel 4a)
- 13 Szenarien für Zustandsübergänge definiert
- `docs/goals.md` um Ziel 4a–4f erweitert

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A — uiLayout/ Struktursplit | ✅ fertig |
| Ziel 1B — gameObjects/ Foundation | ✅ fertig |
| Ziel 2 — Command Phase | ✅ fertig |
| Ziel 3a — Phase-Infrastruktur | ✅ fertig |
| Ziel 3b — combat.py Kernel | ✅ fertig |
| Ziel 3c — Shooting + Fight Phase | ✅ fertig |
| Ziel A — Architektur-Review | ✅ fertig |
| **Ziel 4a — Badge/State-System** | ⏳ **nächste Session** |
| Ziel 4b–4f | ⬜ geplant |

---

## Nächste Session: Ziel 4a

### Reihenfolge

```
1. Entscheidung: Doku-Ort für unit_states.md (docs/rules/ vs. docs/)
2. docs/rules/unit_states.md schreiben (Flussdiagramme + Badge-Vokabular)
3. "normal" → "moved" umbenennen (unit_mutations, movementPhase, _common, Tests)
4. turn_flags["shot"] = True nach Schussauflösung (shootingPhase._render_display)
5. turn_flags["fought"] = True nach Kampfauflösung (fightPhase._render_display)
6. state_badges_html() — neue Prioritätslogik: FOUGHT > CHARGED; SHOT additiv
7. _reset_turn_state() — my_will_be_done_active ebenfalls zurücksetzen
8. apply_damage() — destroyed=True → melee-Partner auto-clearen
9. Tests für alle Badge-Transitionen
```

### Designentscheidungen aus dieser Session (fest)

- Badges sind digitale Spielmarker — immer den Regelzustand abbilden, nicht technische Felder
- `STATIONARY` als Default am Zugstart ist RICHTIG — Spieler muss immer Zustand sehen
- `FOUGHT` ersetzt `CHARGED` in der Anzeige (nicht additiv)
- `SHOT` ist immer additiv neben dem Bewegungsbadge
- `IN MELEE` wird unterdrückt wenn `CHARGED` aktiv (ist impliziert)
- `FOUGHT + IN MELEE` zeigen zusammen (kämpfte, noch gebunden)
- Spaltenreihenfolge NIEMALS an `active` binden — `first_player`/`second_player` sind unveränderlich

---

## Badge-Vokabular (Kurzreferenz für nächste Session)

```
PERSISTENT:   IN MELEE | IN RESERVE
BEWEGUNG:     STATIONARY | MOVED | ADVANCED | RETREATED | CHARGED
AKTION:       SHOT (additiv) | FOUGHT (ersetzt CHARGED)
SPEZIAL:      MWBD

PRIORITÄT: FOUGHT > CHARGED > MOVED/ADVANCED/RETREATED/STATIONARY
           SHOT immer additiv
           IN MELEE zeigt immer außer bei CHARGED
```

## 13 Szenarien (Kurzreferenz)

| # | Start | Bewegung | FKampf | Angriff | Nahkampf | Zugwechsel |
|---|---|---|---|---|---|---|
| 1 | STAT | stationary | SHOT | — | — | STATIONARY |
| 2 | STAT | MOVED | SHOT | — | — | STATIONARY |
| 3 | STAT | ADVANCED | — | — | — | STATIONARY |
| 4 | STAT | MOVED | SHOT | Charge✓ | FOUGHT | IN MELEE |
| 5 | STAT | MOVED | — | Charge✓ | FOUGHT | IN MELEE |
| 6 | STAT | MOVED | — | Charge✗ | — | STATIONARY |
| 7 | STAT | MOVED | — | Charge✓ | (noch nicht) | — |
| 8 | IN MELEE | stationary | — | — | FOUGHT | IN MELEE |
| 9 | IN MELEE | stationary | — | — | Feind destroyed | STATIONARY |
| 10 | IN MELEE | RETREATED | — | — | — | STATIONARY |
| 11 | IN RESERVE | (Runde 1) | — | — | — | IN RESERVE |
| 12 | IN RESERVE | DEPLOY(R≥2) | — | — | — | STATIONARY |
| 13 | STAT | MWBD aktiv | … | … | … | STATIONARY |

---

## Architektur (Kurzreferenz)

```
src/
  app.py
  gameMechanic/
    combat.py               ← parse_dice (W+D, +N), resolve_weapon_strength, resolve_attack
    commandPhase.py
    shootingPhase.py        ← can_shoot(), _render_display() → SHOT-Flag hier setzen
    fightPhase.py           ← can_fight(), _render_display() → FOUGHT-Flag hier setzen
    movementPhase.py        ← "normal" → "moved" umbenennen
    chargephase.py          ← Stub (4c)
    game_state.py           ← _reset_turn_state() — MWBD-Bug hier
    unit_mutations.py       ← set_movement_status, apply_damage — melee-auto-clear hier
    game_log.py
    ability_engine.py
    phase_runner.py
  gameObjects/
    unit.py | weapon.py | loader.py
  uiLayout/
    _common.py              ← state_badges_html() — Hauptziel 4a
    unitCard.py
    gameActionsArea.py
data/wh40k_9e/necrons/ | orks/
tests/
  gameMechanic/             ← test_combat.py (182 Tests total)
  uiLayout/                 ← test_common.py — Badge-Tests hier erweitern
  gameObjects/
docs/
  goals.md                  ← Ziel 4a vollständig spezifiziert
  rules/schlachtrunde.md
  rules/unit_states.md      ← NOCH ZU ERSTELLEN (Ziel 4a Schritt 1-2)
```

## Wichtige Designregeln (aus CLAUDE.md + Memory)

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: `first_player` links, `second_player` rechts — niemals an `active` binden
- Aktionen nur kontextuell zur ausgewählten Einheit
- Kein Design ohne Schema — Nutzer definiert Farbpalette selbst
- `dev`-Branch — kein direktes Committen auf `main`
