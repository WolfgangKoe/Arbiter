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
| **Datenqualitäts-Review** | ✅ Stratagems vollständig (Necrons + Orks); faction_abilities offen |

Teststand: **426 Tests grün**

---

## Was wurde zuletzt gemacht (2026-06-04, Session 6)

- `necrons/stratagems.yaml` — alle 59 GOs vollständig:
  - `effect:` Block zu 53 GOs ergänzt (6 waren bereits gesetzt)
  - `once_per_battle: true` bei 5 GOs: Hand of the Phaeron, Dynastic Heirlooms, Rarefied Nobility, Exalted Cryptek, Canoptek Reinforcement
  - `timing: phase_reactive` + `event:` bei 8 weiteren reaktiven GOs: aetheric_interception (`on_set_up`), reanimation_prioritisation (`on_target`), quantum_deflection (`on_target`), shadows_of_drazak (`on_target`), revenge_of_the_doomstalker (`on_destroy`), canoptek_overdrive (`on_destroy`), murderous_demise (`on_destroy`)
  - `player: both` korrigiert bei quantum_deflection + shadows_of_drazak (Angriffe in beiden Spielerzügen möglich)
  - `rule_text:` bei whirling_onslaught nachgetragen (war leer)
- `orks/stratagems.yaml` — alle 28 GOs vollständig:
  - `effect:` Block zu 26 GOs ergänzt (careen + wreckaz bereits gesetzt)
  - `once_per_battle: true` bei Big Boss + Extra Gubbinz
  - `timing/event` + `player: inactive` bei orks_is_never_beaten + tough_as_squig_hide korrigiert
  - `cp_cost`-Kommentar bei get_stuck_in_ladz ergänzt

---

## ⬅ NÄCHSTE SESSION: Daten-Review Abschluss + Ziel 6g + 6d-Vorbereitung

### 1. Daten-Review Abschluss (klein, ca. 30–45 Min.)

**`necrons/faction_abilities.yaml` — Trigger/Conditions spot-check:**
- Für jede Fähigkeit: `ability_type` korrekt? `trigger.phase/timing/event` vollständig? `conditions` richtig?
- Besonders: Living Metal (Command Phase, Auto), Reanimation Protocols (phase_reactive / on_destroy)
- Quelle: `data/wh40k_9e/necrons/faction_abilities.yaml`

**`orks/faction_abilities.yaml` — Trigger/Conditions spot-check:**
- WAAAGH!-Fähigkeit: `trigger`, `stages`, `once_per_battle` prüfen
- Quelle: `data/wh40k_9e/orks/faction_abilities.yaml`

### 2. Ziel 6g Restpunkt (5 Min.)

- `gameMechanic/game_state.py`: `init_state()` ruft `set_log_players()` auf
- Dann: Checkbox in `ziel6.md` abhaken

### 3. Ziel 6d — Attackensequenz (Hauptaufgabe, mehrstufig)

Vorher Plan zeigen + Freigabe holen. Die Arbeit ist umfangreich:
- `gameMechanic/combat.py`: `resolve_attack_modifiers()`, `resolve_save()`, `resolve_fnp()`
- Angreifer/Verteidiger-Area: simultane Darstellung mit Modifier-Stack
- Stratagem-Buttons direkt beim betreffenden Würfelblock

**Wichtiger Constraint:** Nahkampf/Overwatch — Seiten-Zuweisung nach `attacker_faction`, nicht `active`.

---

## Offene Entscheidungen

| Entscheidung | Optionen |
|---|---|
| **`once_per_battle` enforcement** | Braucht `used_this_battle: set[str]` in Session-State + neuen Parameter in `stratagem_visibility()`. Wann implementieren? |
| **Variable CP-Kosten** | Derzeit nur Kommentar im YAML. Optionen: (a) so lassen, (b) `cp_cost_max: int` Feld, (c) `cp_cost_condition: str` Feld + Logik |
| **Reaktive GO UI** | `timing: phase_reactive` GOs sind korrekt markiert — aber UI zeigt sie gleich wie proaktive. Eigener UI-Bereich? Anderes Styling? |

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

### Stratagem-Effect-Vocabulary (Stand 2026-06-04)
Etablierte `effect.type`-Werte (aus Necrons + Orks Review):
`buff_roll`, `debuff_roll`, `buff_stat`, `buff_count`, `mortal_wounds`, `heal`, `reanimate`, `respawn`, `free_attack`, `auto_pass_morale`, `reroll`, `move`, `teleport`, `deep_strike`, `invuln_save`, `restriction`, `grant_ability`, `grant_keyword`, `grant_relic`, `grant_warlord_trait`, `grant_equipment`, `auto_wound`, `auto_explode`, `swap_ability`, `extra_ability_use`, `wound_track_override`, `deny_psychic`, `buff_weapon_type`

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
| faction_abilities spot-check | Necrons + Orks faction_abilities.yaml | ⬜ |
| 6g Restpunkt | set_log_players() in init_state() | ⬜ |
| 6d — Attackensequenz simultan | combat.py + UI | ⬜ |
| subfaction_affinity UI | Wenn aktive Subfaction == Affinität → beide Direktiven aktiv | ⬜ |
| AdMech Canticles YAML | `data/wh40k_9e/adeptus_mechanicus/faction_abilities.yaml` | ⬜ |
| T'au Mont'ka/Kauyon YAML | Runden-Fenster-Mechanik | ⬜ |
| Auto-Progression Space Marines | Doctrines, neuer ability_type | ⬜ |
| 6f — Ability-Badges unitCard | hängt von 6d ab | ⬜ |
| 6e — CP-Doppelvergabe-Fix | `cp_granted_this_phase`-Flag | ⬜ |
| load_powers() verdrahten | Psychic Phase, Orks Weirdboy | ⬜ |
| load_shared_abilities() verdrahten | Universalregeln im Engine | ⬜ |

---

## Historische Session-Notizen

### 2026-06-04, Session 6 — Datenqualitäts-Review (Teil 2, Abschluss Stratagems)
Alle 59 Necron-GOs + 28 Ork-GOs vollständig: effect, once_per_battle, timing/event für reaktive GOs, player-Korrekturen. whirling_onslaught rule_text nachgetragen. 426 Tests grün.

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
