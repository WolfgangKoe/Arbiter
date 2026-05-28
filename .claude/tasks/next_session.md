# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py`
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — alle Ziele, aktueller Status, **Ziel A** ist das neue Schwerpunktziel
3. `docs/rules/schlachtrunde.md` — vollständige WH40k 9E Regelreferenz (Deutsch)
4. `src/gameMechanic/combat.py` — Kernlogik Attackensequenz
5. `src/gameObjects/unit.py` — Unit-Dataclass
6. `data/wh40k_9e/necrons/units.yaml` — Necron-Einheitendaten (Beispielstruktur)
7. `data/wh40k_9e/orks/army.yaml` — Ork-Daten (unvollständig, units.yaml fehlt)
8. `tests/engine/` — veraltete Teststruktur, die refactored werden soll

---

## Was in dieser Session gemacht wurde

### Ziel 3c — Shooting Phase + Fight Phase (fertig)

- `can_shoot()` und `can_fight()` als pure functions
- `render_attack_form()` in `_common.py` — shared UI-Helper für beide Phasen
- Waffe wählen → 4 Dice-Inputs (Hits/Wounds/Failed Saves/FNP) → Resolve → Apply Damage
- Variable Schadenswerte (D6, W3) mit Extra-Eingabe
- `"User"`-Stärke korrekt aufgelöst
- 177 Tests, alle grün

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A — uiLayout/ Struktursplit | ✅ fertig |
| Ziel 1B — gameObjects/ Foundation | ✅ fertig |
| Ziel 2 — Command Phase | ✅ fertig |
| Ziel 3a — Phase-Infrastruktur | ✅ fertig |
| Ziel 3b — combat.py Kernel (41 Tests) | ✅ fertig |
| Ziel 3c — Shooting + Fight Phase (177 Tests) | ✅ fertig |
| **Ziel A — Architektur-Review** | ⏳ **nächste Session** |
| Ziel 4 — Phasen ausbauen + Army Builder | ⬜ wartet auf Ziel A |

---

## Nächste Session: Ziel A

**Leitfrage:** Kann eine neue Armee "angedockt" werden, ohne die Kernlogik anzufassen?

Das Ziel ist nicht, alle Regeln zu implementieren, sondern zu prüfen, ob bestehende Abstraktionen ausreichen oder substanzielle Lücken vorhanden sind.

**Output:** `docs/review/architecture_review_2026-05.md` — Analyse + Entscheidungsvorlagen (keine Implementierung, erst nach User-Review)

### Arbeitsreihenfolge

```
1. A3 — Test-Refactoring tests/engine/ (operativ, parallel-sicher)
2. A2 — YAML-Daten sichten + externe Quellen abfragen
3. A1 — Schlachtrunden-Review
4. Review-Dokument schreiben
5. next_session.md + goals.md aktualisieren
```

---

### A1 — Regelwerk-Review gegen Architektur

**Quelle:** `docs/rules/schlachtrunde.md`

Für jede Regelgruppe klassifizieren:

| Kürzel | Bedeutung |
|--------|-----------|
| ✅ YAML-only | Als Ability/Keyword ausdrückbar, kein Code nötig |
| 🔧 Parameter | Neues Feld in Dataclass oder turn_flags |
| 🏗️ Konzept | Eigene Funktion oder Handler nötig |
| ⚠️ Konflikt | Widerspricht bestehender Designentscheidung |
| ❌ Out of Scope | Bewusst nicht geplant |

Zu prüfende Bereiche:
- Befehlsphase (CP-Bonus, Ability-Timing)
- Bewegungsphase (FLIEGEN als Keyword, Advance-Roll, Reserve, Formation)
- Psiphase (2W6 vs. WC, Deny, Perils — passt in `ability_engine`?)
- Fernkampfphase (Zielbeschränkungen, "Im Nahkampf gebunden"-Schussverbot auf Freunde, Schnelles Würfeln)
- Attackensequenz: **AP-Mechanik prüfen** — Regelwerk sagt "W6 − DS ≥ RW", Implementierung setzt "RW + |AP|". Mathematisch äquivalent, aber unmodifizierte 1 (immer misslingt) hat Edge Case wenn kein AP. Spillover bei tödlichen Verwundungen fehlt aktuell.
- Angriffsphase (Abwehrfeuer `hit_modifier="only_6s"`, Heroische Intervention: eigene Funktion oder Ability?)
- Nahkampfphase (Alternierend beginnend mit Nicht-Aktiv-Spieler, Nachrücken, Neu ordnen)
- Moralphase (W6 + `lost_models_this_turn` vs. Leadership — `lost_models_this_turn` ist vorhanden in `unit_state`)

---

### A2 — YAML-Struktur-Review

#### Necron-YAML bereinigen

Felder die wahrscheinlich weg können (kein Spielwert, nur Build-Metadaten):
```yaml
curation:
  rules_reviewed: true
  wave_completed: 2c
  ...
weapon_source_strategy: catalog_entry
```

Strukturfragen zu klären:
- `faction: [<Dynasty>, Necrons, Canoptek]` — `<Dynasty>` bedeutet "Einheit nimmt Dynastiewert an". Aber `dynasty_selectable: []` scheint dasselbe auszudrücken. Welches Konzept ist kanonisch?
- Canoptek-Einheiten haben `<Dynasty>` in der Faction-Liste — stimmt das mit dem Regelwerk überein?
- Schadenswerte: Necrons nutzen `W3`, `W6`, `W3+3`. Orks nutzen `D6`. `parse_dice()` versteht nur D-Notation — W-Notation crasht. Brauchen wir eine kanonische Notation?
- `"User"`-Stärke: bereits in `render_attack_form` aufgelöst. Sollte das ins YAML-Schema?

Degradierende Profile (Triarch Stalker hat 3 Statzeilen je nach LP-Stand):
- Aktuell nicht abbildbar in `Unit`-Dataclass
- Optionen: (a) `wound_profiles: list[WoundProfile]` in Dataclass, (b) als Ability mit Trigger auf LP-Schwelle
- Entscheidungsvorlage mit Abwägung

#### Ork-Daten beschaffen

`data/wh40k_9e/orks/` hat keine `units.yaml`. Einheiten aus `army.yaml` vorhanden aber unvollständig.

Quellen versuchen (in dieser Reihenfolge):
1. Wahapedia: `https://wahapedia.ru/wh40k9ed/factions/orks/` (WebFetch)
2. BattleScribe-Datenrepo auf GitHub (WebSearch nach "battlescribe data orks 9th edition")

**Achtung:** BattleScribe-Datenstruktur (XML, army builder-spezifisch) nicht 1:1 übernehmen — nur Zahlenwerte und Regeltext extrahieren.

Delta `orks.md` (aktuell vorhanden) vs. tatsächliche Einheiten-Datasheets prüfen.

#### Template

Am Ende ein Muster-YAML für eine Einheit, das auf jede Armee anwendbar ist:
- Alle semantisch sinnvollen Felder
- Keine Build-Metadaten
- Klarer Umgang mit Sonderfällen (W-Notation, User-Stärke, Varianten-Profile)

---

### A3 — Test-Struktur-Refactoring

**Problem:** `engine.py` existiert nicht mehr. `tests/engine/` ist verwaist.

```
tests/engine/test_engine.py        → aufteilen (siehe unten)
tests/engine/test_multi_target.py  → tests/gameMechanic/test_unit_mutations.py
tests/engine/test_state_badges.py  → tests/uiLayout/test_common.py
```

`test_engine.py` enthält Logik aus mehreren Modulen:
- `parse_dice`, `wound_threshold` → bereits in `tests/gameMechanic/test_combat.py` — Duplikate prüfen, fehlende Tests ergänzen
- `apply_damage`, `heal_unit` → `tests/gameMechanic/test_unit_mutations.py` (neu)
- `next_phase`, Phase-Navigation → `tests/gameMechanic/test_game_state.py` (neu)

Nach Migration: `tests/engine/` löschen. Coverage-Report: ≥ 80%.

---

## Architektur (Kurzreferenz)

```
src/
  app.py                    ← Streamlit-Einstieg
  gameMechanic/
    combat.py               ← AttackParams, DefendParams, resolve_attack()
    commandPhase.py         ← Command Phase Handler
    shootingPhase.py        ← can_shoot(), ShootingPhaseHandler
    fightPhase.py           ← can_fight(), FightPhaseHandler
    movementPhase.py        ← MovementPhaseHandler
    chargephase.py          ← Stub
    game_state.py           ← init_state, next_phase, PHASES
    unit_mutations.py       ← apply_damage, heal_unit, enter/leave_melee, set_charged
    game_log.py             ← log_action
    ability_engine.py       ← Timing-Konstanten, Trigger-System
    phase_runner.py         ← PHASE_REGISTRY, render_current_phase()
  gameObjects/
    unit.py                 ← Unit-Dataclass
    weapon.py               ← Weapon-Dataclass
    loader.py               ← YAML → Objekte
  uiLayout/
    _common.py              ← lookup(), render_player_column(), render_attack_form()
    unitCard.py             ← Einheitenkarte inkl. MWBD/ResOrb-Awaiting-Flow
    gameActionsArea.py      ← delegiert an phase_runner
data/
  wh40k_9e/
    necrons/                ← units.yaml, weapons.yaml, army.yaml, ...
    orks/                   ← army.yaml (units.yaml fehlt!)
```

## Designentscheidungen (unveränderlich)

- `turn_flags` = Spielmechanik-Checks only
- `selected_targets: list[tuple[str, str]]` — nie single-target
- `can_fight()` prüft `in_melee` ODER `charged`
- `render_attack_form()` in `_common.py` — shared, kein Duplikat
- Attack-Form immer im unteren `_render_display`-Bereich, nicht in der Spalte
- Aktionen erscheinen NUR kontextabhängig zur ausgewählten Einheit
- Alle Engine-Importe direkt aus `gameMechanic.*` — kein Shim mehr
- Kein direktes Committen auf `main`
