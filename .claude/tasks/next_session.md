# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## ⚠️ Session-Regeln (immer beachten)

**Zu Beginn jeder Session lesen:**
- `CLAUDE.md` — Workflow, Freigabe-Pflicht, **Unklarheiten IMMER zuerst fragen**, Branch-Strategie
- `docs/goals/ziel6.md` — aktueller Ziel-6-Stand

**Am Ende jeder Session:**
- `docs/goals/ziel6.md` aktualisieren: Checkboxen abhaken, neue Erkenntnisse ergänzen

---

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Aktueller Status

| Ziel | Status |
|------|--------|
| Ziel 1–5 — Grundgerüst, Phasen, Setup, Daten | ✅ fertig |
| Ziel 6a–6c, 6e, 6g, 6h | ✅ committed |
| Ziel 6h — Custodes Ka'tah YAML + Tests | ✅ committed |
| **Datenqualitäts-Review** | 🔄 Schema + _shared + bekannte Fehler done; volle Review offen |

Teststand: **426 Tests grün**

---

## Was wurde zuletzt gemacht (2026-06-04)

- `Stratagem`-Dataclass erweitert: `phase: str | list[str]`, `timing`, `event`, `once_per_battle`, `effect: Effect` (reuse aus `ability.py`); `stratagem_visibility()` list-phase-fähig
- `loader.py`: neue Felder werden geparst
- `_shared/stratagems.yaml`: alle 7 GOs vollständig (phase, timing, event, effect, once_per_battle)
- `necrons/stratagems.yaml`: 7 bekannte Fehler behoben (phase-Listen, player, timing/event, effect, variable CP-Kommentare)
- `orks/stratagems.yaml`: wreckaz + careen korrigiert
- `adeptus_custodes/faction_abilities.yaml`: Datenfehler in Calistus-Eintrag gefixt

---

## ⬅ NÄCHSTE SESSION: Fachliche Datenqualitäts-Review (Fortsetzung)

Für jede GO prüfen und ergänzen:
- `phase` — korrekt als Liste wenn mehrere Phasen möglich
- `stage` — `start` / `active` / `end`
- `player` — `active` / `inactive` / `both`
- `timing` + `event` — wenn reaktiv
- `effect` — maschinenlesbares Feld nachtragen (Typen: `buff_roll`, `debuff_roll`, `mortal_wounds`, `heal`, `reanimate`, `free_attack`, `auto_pass_morale`, `reroll`, `move`, `teleport`, `invuln_save`, `restriction`, `mark_target`, ...)
- `once_per_battle` — wenn rule_text "once per battle" sagt
- variable `cp_cost` — als Kommentar dokumentieren

**Priorität:**
1. ⬅ `necrons/stratagems.yaml` — ~52 GOs noch offen
2. ⬅ `orks/stratagems.yaml` — ~21 GOs noch offen
3. ⬅ `necrons/faction_abilities.yaml` + `orks/faction_abilities.yaml` — Trigger/Conditions spot-check
4. ⬅ Optional: Tests für korrekte Phase/Stage-Werte

**Wahapedia-Quellen:**
- `https://wahapedia.ru/wh40k9ed/factions/necrons/Stratagems`
- `https://wahapedia.ru/wh40k9ed/factions/orks/Stratagems`

---

## Offene Entscheidungen (für Folgeschritte)

| Entscheidung | Optionen |
|---|---|
| **`once_per_battle` enforcement** | Braucht `used_this_battle: set[str]` in Session-State + neuen Parameter in `stratagem_visibility()`. Wann implementieren? |
| **Variable CP-Kosten** | Derzeit nur Kommentar im YAML. Optionen: (a) so lassen, (b) `cp_cost_max: int` Feld, (c) `cp_cost_condition: str` Feld + Logik |
| **Reaktive GO UI** | `timing: phase_reactive` GOs sind jetzt korrekt in der Dataclass markiert — aber die UI zeigt sie gleich wie proaktive. Eigener UI-Bereich? Anderes Styling? Spätere Entscheidung. |

---

## Wichtige Constraints & Architektur (Stand 2026-06-04)

### Generische Fähigkeits-Architektur

```
YAML (faction_abilities.yaml)
  ├─ ability_type: round_choice   → load_round_choice_abilities() → list[CommandProtocol]
  │    subfaction_affinity: id         → UI: armyCard._render_protocol_ui()
  ├─ ability_type: activated      → load_faction_abilities() filtert, armyCard._render_waaagh_ui()
  ├─ ability_type: triggered      → load_faction_abilities(), ability_engine.get_triggered_abilities()
  └─ ability_type: auto_progression → (noch nicht implementiert)

YAML (powers.yaml)               → load_powers() [noch nicht verdrahtet]
YAML (_shared/shared_powers.yaml) → smite, deny_the_witch, perils — stub
YAML (_shared/shared_abilities.yaml) → load_shared_abilities() [noch nicht verdrahtet]
YAML (_shared/stratagems.yaml)   → load_stratagems() [verdrahtet]
```

### _shared/-Verzeichnis
| Datei | Inhalt | Loader-Status |
|-------|--------|--------------|
| `_shared/stratagems.yaml` | 7 Core Stratagems (vollständig) | verdrahtet |
| `_shared/shared_abilities.yaml` | ObjSec, DS, FNP, Fly + 3 weitere | Stub, nicht verdrahtet |
| `_shared/shared_powers.yaml` | Smite, Deny, Perils | Stub, nicht verdrahtet |
| `_shared/detachment_types.yaml` | Patrol–Air Wing + CP-Felder | verdrahtet |

### Nicht wired (nur Display)
`strength_modifier`, `attacks_modifier`, `ap_bonus`, `move_bonus`, `advance_and_charge`,
`reroll_hit_wound_1`, `reroll_save_1`, `leadership_bonus`, `rp_reroll`, `rp_bonus`,
`toughness_debuff`, `invuln_save`, `extra_hit_on_6`, `shoot_after_fallback`,
`action_during_advance`, `shoot_during_action`, `enemy_pilein_debuff`, `range_bonus`,
`shoot_twice_stationary`, `extra_wound_on_6`, `prevent_reroll_hits`, `prevent_fallback`,
`stationary_after_move`, `deep_strike`

### Session-State Schlüssel
| Key | Typ | Bedeutung |
|-----|-----|-----------|
| `active_protocol_id` | `str \| None` | Aktives Protokoll / Ka'tah dieser Runde |
| `active_directive` | `"primary" \| "secondary" \| None` | Gewählte Direktive / Stance |
| `used_protocol_ids` | `list[str]` | Bereits verwendete Protokoll/Ka'tah-IDs |
| `waaagh_state` | `dict[str, dict]` | `{player: {stage, round_activated}}` |
| `command_ability_state` | `dict[ability_id, {target_uid, active_since_round}]` | Unit-Abilities |

### Wichtige Constraints
- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Niemals nur lokale YAML-Daten für Architekturentscheidungen** — immer Wahapedia prüfen
- Seitenleisten IMMER fest: first_player links, second_player rechts
- dev-Branch — kein direktes Committen auf main
- Keywords immer `UPPERCASE` in YAML
- Weapon strength: `_parse_strength()` in `_common.py`
- Abilities: NIE auf Fraktionsnamen hardcoden — immer generisch via YAML/Keywords
- `round_choice` für alle Fraktionen: `load_round_choice_abilities()` + `_render_protocol_ui()`

---

## Mittelfristige Roadmap (nach der Review)

| Schritt | Was | Status |
|---------|-----|--------|
| subfaction_affinity UI | Wenn aktive Subfaction == Affinität → beide Direktiven aktiv | ⬜ |
| AdMech Canticles YAML | `data/wh40k_9e/adeptus_mechanicus/faction_abilities.yaml` | ⬜ |
| Auto-Progression Space Marines | Doctrines, neuer ability_type | ⬜ |
| set_log_players() in init_state() | `game_log.py` — klein, 5 Min | ⬜ |
| Ziel 6d — Attackensequenz simultan | | ⬜ |
| Ziel 6f — Ability-Badges unitCard | | ⬜ |
| load_powers() verdrahten | Psychic Phase, Orks Weirdboy | ⬜ |
| load_shared_abilities() verdrahten | Universalregeln im Engine | ⬜ |

---

## Historische Session-Notizen

### 2026-06-04, Session 5 — Datenqualitäts-Review (Teil 1)
Schema-Erweiterung Stratagem-Dataclass. Alle _shared GOs vollständig. 7 bekannte Necron-Fehler + Orks wreckaz/careen behoben. Custodes faction_abilities.yaml Datenfehler gefixt.

### 2026-06-04, Session 4 — 6-Batch-Plan vollständig
Batches 0–6: Folder-Merge, YAML-Datenkorrekturen, Shared-Dateien, Orks powers.yaml, Alias-Entfernung, Spec-Doku, 27 Tests. 426 Tests grün. Bugfix: Archive-Log-Crash.

### 2026-06-04, Session 3 — Planung & Forschung
Subfaction-Affinitäten verifiziert. Core Rules Inventory. 6-Batch-Plan formuliert.

### 2026-06-03, Session 2 — Bugfixes
Battle Log TypeError + Protokoll-Aktivierung durch inaktiven Spieler gefixt.

### 2026-06-03, Session 1
WAAAGH! Datenfehler korrigiert. Generisches Fähigkeitssystem implementiert.
