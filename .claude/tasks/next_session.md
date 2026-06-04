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
| Ziel 6a — gameHeader Redesign | ✅ fertig |
| Ziel 6b — armyCard generisches Fähigkeitssystem | ✅ fertig |
| Ziel 6c — Stratagems Default-Tab, Modifier-Export | ✅ fertig |
| Ziel 6e (teilw.) — Command Phase generic abilities | ✅ committed |
| Ziel 6e (teilw.) — Command Protocols verdrahtet | ✅ committed |
| Ziel 6g (teilw.) — Game Log Archiv + Setup-UI | ✅ committed |
| Ziel 6h — Architektur-Aufräum-Sprint | ✅ committed (2026-06-04) |
| **6-Batch-Plan (diese Session geplant)** | ⬅ NÄCHSTER SCHRITT |

---

## Was wurde zuletzt gemacht (2026-06-04 — Session 3: Planung)

Diese Session war reine Forschung und Planung — **kein Code wurde geändert**.

### Forschungsergebnisse

#### Subfaction-Affinitäten — korrigiert durch Wahapedia-Verifikation

**Necrons (4 von 6 waren falsch):**
| Protocol ID | Alt (YAML) | Korrekt (Wahapedia) | Status |
|---|---|---|---|
| eternal_guardian | szarekhan | **nihilakh** | FALSCH |
| hungry_void | mephrit | **novokh** | FALSCH |
| conquering_tyrant | sautekh | sautekh | ✓ |
| sudden_storm | nephrekh | nephrekh | ✓ |
| undying_legions | novokh | **szarekhan** | FALSCH |
| vengeful_stars | nihilakh | **mephrit** | FALSCH |

**Adeptus Custodes (2 vertauscht + 1 ID-Rename):**
| Ka'tah ID | Alt (YAML) | Korrekt (Wahapedia) | Status |
|---|---|---|---|
| calistus | emissaries_imperatus | **solar_watch** | FALSCH (swap) |
| conservai | solar_watch | **emissaries_imperatus** | FALSCH (swap) |
| dacatarai | dread_host | dread_host | ✓ |
| salvus | aquilan_shield | aquilan_shield | ✓ |
| rendax | wardens | **emperors_chosen** | ID-Rename |
| kaptaris | shadowkeepers | shadowkeepers | ✓ |

**Hinweis rendax:** Nur `adeptus_custodes/faction_abilities.yaml:101` enthält `subfaction_affinity: wardens` — das ist die einzige Stelle, die geändert werden muss.

#### Core Rules Inventory (universal/shared)

Bereits vorhanden in `data/wh40k_9e/universal/stratagems.yaml` (7 Core-Stratagems — vollständig):
- command_re_roll, cut_them_down, desperate_breakout, emergency_disembarkation,
  fire_overwatch, counter_offensive, insane_bravery

In `data/wh40k_9e/_shared/shared_abilities.yaml` (4 Stubs — unvollständig):
- objective_secured, deep_strike, fly, feel_no_pain

**Noch fehlende Shared Abilities:**
- big_guns_never_tire (VEHICLE/MONSTER keyword — kann in Engagement Range schießen; -1 to hit bei ER)
- look_out_sir (CHARACTER ≤9W — kann nicht targetiert werden wenn ≥1 nicht-CHARACTER-Einheit in 3")
- heroic_intervention (CHARACTER — kann in gegnerischer Charge Phase bis 3" auf Gegner zu bewegen)

**Noch fehlende Shared Powers (neue Datei `_shared/shared_powers.yaml`):**
- smite (warp charge 5, 18", D3 MW; 11+ → D6 MW; max 1 pro PSYKER + je +1 Warp Charge pro weiterer Smite derselben Armee)
- deny_the_witch (Reaktion; PSYKER in 24"; 2D6 > Manifestierungs-Wert → Macht gescheitert)
- perils_of_the_warp (Auto-Trigger; Doppel-1 oder Doppel-6; D3 MW auf Caster; alle Einheiten in 6" ebenfalls D3 MW)

**Nicht 9E — nicht hinzufügen:** Lethal Hits, Sustained Hits, Devastating Wounds, Anti-[X], Lone Operative, Leader, Deadly Demise (alle 10E)

**Detachment CP-Daten für `_shared/detachment_types.yaml`:**
| Detachment | command_cost | command_benefit |
|---|---|---|
| patrol | 2 | 0 |
| battalion | 0 | 3 |
| brigade | 0 | 12 |
| vanguard | 1 | 0 |
| spearhead | 1 | 0 |
| outrider | 1 | 0 |
| air_wing | 1 | 0 |

### Entscheidungen dieser Session

| Thema | Entscheidung |
|-------|-------------|
| Powers-Datei | `powers.yaml` je Fraktion, `power_type: psychic \| deny \| ctan`, shared in `_shared/shared_powers.yaml` |
| Folder-Merge | `universal/` und `_shared/` → vereinheitlicht in `_shared/` |
| rendax Shield Host | ID `wardens` → `emperors_chosen` |
| Alias | `load_command_protocols()` löschen, alle 4 Aufrufer auf `load_round_choice_abilities()` |
| Ork ObjSec | → `unit_abilities.yaml` mit `not_has_keywords: [GRETCHIN]` |
| Dokumentation | Neue Struktur: `docs/spec/data/` mit `schema.md`, `import_guide.md`, `_shared.md`, `factions/` |

---

## ⬅ VOLLSTÄNDIGER IMPLEMENTIERUNGSPLAN (freigegeben)

### Batch 0 — Folder-Merge `universal/` → `_shared/`
**Dateien:**
- `data/wh40k_9e/universal/stratagems.yaml` → `data/wh40k_9e/_shared/stratagems.yaml` (verschieben)
- IDs in der Datei: `wh40k_9e.universal.stratagem.*` → `wh40k_9e.shared.stratagem.*`
- `src/gameObjects/loader.py:327`: `"universal"` → `"_shared"` (in `load_stratagems()`)
- `data/wh40k_9e/universal/` Verzeichnis löschen
- Tests prüfen ob Stratagem-IDs referenziert sind

### Batch 1 — Datenkorrekturen YAML
**Dateien:**
- `data/wh40k_9e/necrons/faction_abilities.yaml` — 4 subfaction_affinity-Werte
- `data/wh40k_9e/adeptus_custodes/faction_abilities.yaml` — calistus↔conservai swap + rendax `wardens`→`emperors_chosen`
- `data/wh40k_9e/orks/faction_abilities.yaml` — objective_secured entfernen
- `data/wh40k_9e/orks/unit_abilities.yaml` — objective_secured hinzufügen (`not_has_keywords: [GRETCHIN]`, `shared_ref: wh40k_9e.shared.objective_secured`)
- Bei Gelegenheit: FNP/Deep-Strike-Einträge in necrons/unit_abilities.yaml + orks/unit_abilities.yaml um `shared_ref`-Feld ergänzen

### Batch 2 — Shared-Dateien ausbauen
**Dateien:**
- `data/wh40k_9e/_shared/shared_abilities.yaml` — big_guns_never_tire, look_out_sir, heroic_intervention ergänzen
- `data/wh40k_9e/_shared/shared_powers.yaml` (NEU) — smite, deny_the_witch, perils_of_the_warp mit `power_type`-Enum
- `data/wh40k_9e/_shared/detachment_types.yaml` — `command_cost` + `command_benefit` ergänzen (7 Einträge)

Schema für `shared_powers.yaml`:
```yaml
- id: wh40k_9e.shared.power.smite
  name_en: Smite
  power_type: psychic          # psychic | deny | ctan
  warp_charge: 5
  denyable: true
  range_inches: 18
  targeting: closest_visible_enemy
  effect:
    type: mortal_wounds
    amount: D3
    boosted_amount: D6
    boost_threshold: 11
  restriction: once_per_psyker_per_battle_round
  accumulating_charge: true    # +1 WC für jede weitere Smite der Armee
```

### Batch 3 — Orks Powers-YAML
**Dateien:**
- `data/wh40k_9e/orks/powers.yaml` (NEU) — Weirdboy-Kräfte mit `power_type: psychic`
- `data/wh40k_9e/orks/faction_abilities.yaml` — Weirdboy-Kräfte entfernen

Loader noch nicht verdrahten — reine Datenmigration.

### Batch 4 — Code-Refactor (Alias entfernen)
**Dateien (alle callers auf `load_round_choice_abilities()` umstellen):**
- `src/gameObjects/loader.py` — `load_command_protocols()` löschen (Zeile 294–296)
- `src/gameMechanic/commandPhase.py` — Import + Aufruf Zeile 11, 200
- `src/gameMechanic/ability_engine.py` — Import + Aufruf Zeile 10, 83
- `src/uiLayout/_common.py` — Import + Aufruf Zeile 393, 428
- `src/uiLayout/armyCard.py` — Import + 3 Aufrufe Zeile 20, 144, 249
- `tests/test_faction_abilities_custodes.py` — 3 Alias-Tests bereinigen (Zeile 82–91)

### Batch 5 — Spec-Update (3 Unter-Batches)

#### Batch 5a — Outdated refs bereinigen
**Dateien:**
- `docs/spec/architecture.md` — `arkana.yaml` (gelöscht), `command_protocols.yaml` (gemergt), `universal/` → `_shared/`
- `docs/spec/loader_contract.md` — Loader-Ablauf Schritt 4 korrigieren, Arkana-Schema anpassen
- `docs/spec/faction_abilities.md` — Alias-Entfernung eintragen, `powers.yaml`-Sektion ergänzen, `_shared/`-Übersicht

#### Batch 5b — Neue Datendokumentation
**Neue Dateien:**
- `docs/spec/data/schema.md` — vollständige Felddefinitionen für alle YAML-Dateitypen:
  units.yaml, weapons.yaml, faction_abilities.yaml, unit_abilities.yaml,
  subfaction_abilities.yaml, wargear_abilities.yaml, powers.yaml, _shared/*.yaml
- `docs/spec/data/import_guide.md` — Checkliste neue Fraktion: Dateien anlegen → Wahapedia → Tests → Doku; Umgang mit Sonderfällen
- `docs/spec/data/_shared.md` — alle shared abilities, stratagems, powers vollständig dokumentiert

#### Batch 5c — Fraktionsdokumentationen
**Neue Dateien:**
- `docs/spec/data/factions/necrons.md` — alle Protocols + Affinitäten (mit korrigierten Werten!), Abilities nach Datei, Sonderregeln
- `docs/spec/data/factions/orks.md` — WAAAGH!-Varianten, ObjSec-Sonderfall, Weirdboy-Powers
- `docs/spec/data/factions/adeptus_custodes.md` — Ka'tahs + Affinitäten (mit korrigierten Werten!), Shield Hosts

### Batch 6 — Test-Gerüst härten
**Neue Dateien:**
- `tests/test_faction_abilities_necrons.py` — Necron-Protokolle fokussiert: alle 6 Affinitäten korrekt, round_choice loading, subfaction_affinity-Daten-Korrektheit
- `tests/test_faction_abilities_orks.py` — WAAAGH!-Aktivierung, objective_secured-Migration, Weirdboy-Powers

**Updates bestehender Dateien:**
- `tests/test_faction_abilities_custodes.py` — Alias-Tests entfernen; subfaction_affinity-Korrektheit testen (emperors_chosen!)
- `tests/gameObjects/test_loader.py` — `load_round_choice_abilities()` direkt testen; `_shared/stratagems`-Pfad testen
- `tests/gameMechanic/test_command_phase.py` — Lücken füllen (76 Zeilen, wahrscheinlich dünn)

---

## Wichtige Constraints & Architektur (Stand 2026-06-04)

### Generische Fähigkeits-Architektur

```
YAML (faction_abilities.yaml)
  ├─ ability_type: round_choice   → load_round_choice_abilities() → list[CommandProtocol]
  │    subfaction_affinity: id         → UI: armyCard._render_protocol_ui()
  │                                        Modifier: ability_engine.get_active_protocol_modifier()
  ├─ ability_type: activated      → load_faction_abilities() filtert, armyCard._render_waaagh_ui()
  ├─ ability_type: triggered      → load_faction_abilities(), ability_engine.get_triggered_abilities()
  └─ ability_type: auto_progression → (noch nicht implementiert)

YAML (powers.yaml — NEU)          → load_powers() [noch nicht verdrahtet]
  ├─ power_type: psychic           → Psionik-Phase
  ├─ power_type: deny              → Reaktion in Psionik-Phase
  └─ power_type: ctan              → Ende der Bewegungsphase

YAML (_shared/shared_powers.yaml) → smite, deny_the_witch, perils — shared_ref in faction powers
YAML (_shared/shared_abilities.yaml) → load_shared_abilities() [noch nicht verdrahtet]
YAML (_shared/stratagems.yaml)    → load_stratagems() [war universal/, jetzt _shared/]
```

### _shared/-Verzeichnis (nach Batch 0+2)
| Datei | Inhalt | Loader-Status |
|-------|--------|--------------|
| `_shared/stratagems.yaml` | 7 Core Stratagems | verdrahtet (`load_stratagems()`) |
| `_shared/shared_abilities.yaml` | ObjSec, DS, FNP, Fly + 3 neue | Stub, nicht verdrahtet |
| `_shared/shared_powers.yaml` | Smite, Deny, Perils | Stub, nicht verdrahtet |
| `_shared/detachment_types.yaml` | Patrol–Air Wing + CP-Felder | verdrahtet (`load_detachment_types()`) |

### Wired effect types (in combat.py)
`hit_modifier`, `wound_modifier`, `save_modifier`

### Nicht wired (nur Display)
`strength_modifier`, `attacks_modifier`, `ap_bonus`, `move_bonus`,
`advance_and_charge`, `reroll_hit_wound_1`, `reroll_save_1`,
`leadership_bonus`, `rp_reroll`, `rp_bonus`, `toughness_debuff`,
`invuln_save`, `extra_hit_on_6`, `shoot_after_fallback`,
`action_during_advance`, `shoot_during_action`, `enemy_pilein_debuff`,
`range_bonus`, `shoot_twice_stationary`, `extra_wound_on_6`,
`prevent_reroll_hits`, `prevent_fallback`, `stationary_after_move`, `deep_strike`

### Session-State Schlüssel (Command Phase + Protocols + WAAAGH!)

| Key | Typ | Bedeutung |
|-----|-----|-----------|
| `active_protocol_id` | `str \| None` | Aktives Protokoll / Ka'tah dieser Runde |
| `active_directive` | `"primary" \| "secondary" \| None` | Gewählte Direktive / Stance |
| `used_protocol_ids` | `list[str]` | Bereits verwendete Protokoll/Ka'tah-IDs |
| `waaagh_state` | `dict[str, dict]` | `{player: {stage, round_activated}}` |
| `command_ability_state` | `dict[ability_id, {target_uid, active_since_round}]` | Unit-Abilities |

### Wichtige Constraints
- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Niemals nur lokale YAML-Daten für Architektur-Entscheidungen** — immer Wahapedia prüfen
- **subfaction_affinity-Daten NICHT implementieren ohne Wahapedia-Verifikation** (jetzt verifiziert!)
- Seitenleisten IMMER fest: first_player links, second_player rechts
- dev-Branch — kein direktes Committen auf main
- Keywords immer `UPPERCASE` in YAML — Checks via `unit.has_keyword()`
- Weapon strength: `_parse_strength()` in `_common.py`
- Abilities: NIE auf Fraktionsnamen hardcoden — immer generisch via YAML/Keywords
- `round_choice` für alle Fraktionen: `load_round_choice_abilities()` + `_render_protocol_ui()`
- WAAAGH! + T'au: nutzen `_render_waaagh_ui()` — generisch via `faction_abilities`
- `auto_round_1: true` im YAML ersetzt jedes Faction-Hardcoding für automatische Runde-1-Auswahl

### Streamlit 1.57 — CSS-Selektoren

| Komponente | Korrekte Selektoren |
|---|---|
| NumberInput Container | `[data-testid="stNumberInputContainer"]` |
| Buttons allgemein | `button[data-testid="stBaseButton-{kind}"]` |
| Container border=True | `.e1rw0b1u3` (Emotion-Klasse — prüfen bei Streamlit-Update!) |

---

## Mittelfristige Roadmap (nach dem 6-Batch-Plan)

| Schritt | Was | Status |
|---------|-----|--------|
| subfaction_affinity UI | Wenn aktive Subfaction == Affinität → beide Direktiven aktiv | ⬜ |
| AdMech Canticles YAML | `data/wh40k_9e/adeptus_mechanicus/faction_abilities.yaml` | ⬜ |
| Auto-Progression Space Marines | Doctrines, neuer ability_type | ⬜ |
| set_log_players() in init_state() | `game_log.py` — klein, 5 Min | ⬜ |
| Ziel 6d — Attackensequenz simultan | | ⬜ |
| Ziel 6f — Ability-Badges unitCard | | ⬜ |

---

## Historische Session-Notizen

### 2026-06-04, Session 3 — Planung & Forschung (kein Code)

- Subfaction-Affinitäten für Necrons (4 falsch) und Custodes (2 falsch + 1 ID) verifiziert
- Core Rules Inventory via Wahapedia: 7 Core Stratagems (vollständig), fehlende Shared Abilities + neues `powers.yaml`-Konzept
- Entscheidungen getroffen: powers.yaml-Schema, Folder-Merge universal→_shared, emperors_chosen-ID, Alias-Entfernung
- Vollständiger 6-Batch-Plan formuliert und freigegeben
- Neue Dokumentationsstruktur `docs/spec/data/` geplant (schema.md, import_guide.md, _shared.md, factions/)

### 2026-06-03, Session 2 — Bugfixes

**Battle Log TypeError gefixt**
- `gameProtocoll._load_game_log()`: Log-Format-Mismatch nach Ziel-6g-Migration

**Inaktiver Spieler konnte Protokoll aktivieren — gefixt**
- `armyCard._render_protocol_ui()`: `is_active`-Check fehlte

### 2026-06-03, Session 1

**WAAAGH! Datenfehler korrigiert**
- `phase: charge` → `phase: command` (WAAAGH! wird in Befehlsphase ausgerufen)

**Generisches Fähigkeitssystem implementiert**
- `waaagh_state`, `_render_waaagh_ui()`, `_render_protocol_ui()` generisch
