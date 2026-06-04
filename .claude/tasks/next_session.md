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
| Ziel 6e — Command Phase generic abilities + Protocols verdrahtet | ✅ committed |
| Ziel 6g — Game Log Archiv + Setup-UI | ✅ committed |
| Ziel 6h — Architektur-Aufräum-Sprint | ✅ committed |
| **6-Batch-Plan (Batches 0–6)** | ✅ **VOLLSTÄNDIG COMMITTED (2026-06-04)** |
| **Datenqualitäts-Review (läuft)** | 🔄 Schema done, bekannte Fehler gefixt, volle Review ausstehend |

---

## Was wurde zuletzt gemacht (2026-06-04 — Session 4: 6-Batch-Plan)

Alle Batches 0–6 implementiert und committed:

- **Batch 0:** `universal/stratagems.yaml` → `_shared/stratagems.yaml`, IDs auf `wh40k_9e.shared.stratagem.*`
- **Batch 1:** Subfaction-Affinitäten korrigiert (4× Necron, 3× Custodes), Ork ObjSec → `unit_abilities.yaml`
- **Batch 2:** `shared_abilities.yaml` +3, `shared_powers.yaml` (NEU), `detachment_types.yaml` +CP-Felder
- **Batch 3:** `orks/powers.yaml` (NEU) — 7 Weirdboy-Kräfte migriert
- **Batch 4:** `load_command_protocols()` Alias entfernt, 5 Caller auf `load_round_choice_abilities()` umgestellt
- **Batch 5:** Spec-Doku aktualisiert, 3 neue Fraktions-Docs in `docs/spec/data/factions/`
- **Batch 6:** 27 neue Tests, Custodes + Loader-Tests erweitert
- **Bonus:** Archive-Log-Crash gefixt (`AttributeError: list has no .get`)

Teststand: **426 Tests grün**

---

## ⬅ NÄCHSTE SESSION: Fachliche Datenqualitäts-Review

### Ziel

Alle YAML-Datendateien fachlich gegen Wahapedia verifizieren und intern auf Konsistenz prüfen. Bekannte Fehlerklassen:

1. **Timing-Modell zu grob** — `phase: "any"` verschleiert wann eine GO wirklich verwendbar ist
2. **`stage` stimmt nicht** mit dem tatsächlichen Aktivierungszeitpunkt überein
3. **`player` falsch** — aktiver vs. inaktiver Spieler nicht korrekt modelliert
4. **Fehlende `trigger`-Semantik** — reaktive Stratagems (z.B. nach einem Würfelwurf) haben keinen eigenen `trigger_type`
5. **Effekte nicht strukturiert** — `rule_text` beschreibt den Effekt, aber kein maschinenlesbares `effect`-Feld
6. **`conditions` unvollständig** — Keyword-Anforderungen fehlen oder sind falsch

---

### Bekannte Einzelfehler (Beispiele, kein vollständiger Katalog)

#### `_shared/stratagems.yaml`

| Stratagem | Problem |
|-----------|---------|
| `command_re_roll` | `phase: any` falsch — GO ist **reaktiv nach einem Würfelwurf**, nicht "in beliebiger Phase" aktiv nutzbar. In der Befehlsphase gibt es keine Hit/Wound/Save-Rolls. Braucht `trigger_type: after_roll` + `applicable_phases: [movement, psychic, shooting, charge, fight]` |
| `emergency_disembarkation` | `phase: any` — tatsächlich nur wenn ein TRANSPORT **zerstört wird** (reaktiv). Braucht `trigger_type: on_destroy`, `conditions: [TRANSPORT]` korrekt? |
| `fire_overwatch` | `stage: active` — tatsächlich **nach** Charge-Deklaration, vor dem Charge-Wurf. Braucht genaueres Timing-Modell. |
| `insane_bravery` | `once_per_phase: true` falsch — Regeltext sagt **once per battle** |

#### Necrons `stratagems.yaml`

| Stratagem | Problem |
|-----------|---------|
| `judgement_of_the_triarch` | `phase: any` falsch — GO gilt für Shooting **oder** Fight, nicht beliebig. Korrekt: `phase: [shooting, fight]` |
| `whirling_onslaught` | `phase: any` + `stage: active` falsch — tatsächlich reaktiv wenn Einheit als Ziel ausgewählt wird; `player: inactive` korrekt |
| `resurrection_protocols` | `stage: end` korrekt, aber `player: both`? Nur eigene Modelle. |
| `rapid_reanimation` | variable CP-Kosten (1 oder 2 CP) — YAML hat nur einen Wert |
| `stellar_alignment_protocol` | variable CP-Kosten (1 CP normal, 2 CP für TITANIC) |
| `efficient_disintegration` | `phase: any` falsch — GO ist Shooting-Phase |
| `curse_of_the_phaeron` | `player: both` falsch — nur aktiver Spieler löst aus |

#### Orks `stratagems.yaml`

| Stratagem | Problem |
|-----------|---------|
| `wreckaz` | `phase: any, stage: start` falsch — tatsächlich `phase: [shooting, fight], stage: start` |
| `careen` | `phase: any` + reaktiv auf Destroy-Event — braucht `trigger_type: on_destroy` |

---

### Scope der Review

**Zu prüfende Dateien (Priorität 1 — haben direkte Spielauswirkung):**
1. `data/wh40k_9e/_shared/stratagems.yaml` — 7 Core GOs
2. `data/wh40k_9e/necrons/stratagems.yaml` — 59 GOs
3. `data/wh40k_9e/orks/stratagems.yaml` — 23 GOs
4. `data/wh40k_9e/necrons/faction_abilities.yaml` — Trigger/Conditions
5. `data/wh40k_9e/orks/faction_abilities.yaml` — Trigger/Conditions

**Zu prüfende Dateien (Priorität 2 — Datenkonsistenz):**
6. `data/wh40k_9e/necrons/unit_abilities.yaml`
7. `data/wh40k_9e/orks/unit_abilities.yaml`
8. `data/wh40k_9e/adeptus_custodes/faction_abilities.yaml`
9. `data/wh40k_9e/_shared/shared_abilities.yaml`

---

### Methodik

**Für jede Gefechtsoption:**
1. `rule_text` lesen
2. Wahapedia-Originaltext prüfen (Quelle: `https://wahapedia.ru/wh40k9ed/factions/<faction>/Stratagems`)
3. Folgende Felder verifizieren:
   - `phase` — in welcher Phase **genau** verwendbar? Liste wenn mehrere.
   - `stage` — `start` / `active` / `end` — stimmt der Zeitpunkt?
   - `player` — active / inactive / both?
   - `once_per_phase` vs. `once_per_battle` — explizit im Regeltext prüfen
   - `conditions` — welche Keywords zwingend erforderlich?
   - variable `cp_cost` — im YAML dokumentieren (entweder Mindestwert + Kommentar, oder neues Feld)
4. Interne Konsistenz: passt das zur Spiellogik? Kann die GO im aktuellen Phasenmodell überhaupt getriggert werden?

**Für reaktive Stratagems** (Reaktion auf Ereignis):
- Klären: brauchen wir ein `trigger_type`-Feld? Optionen: `proactive` | `after_roll` | `on_destroy` | `on_target` | `on_declaration`
- Diese Entscheidung **vor** der Implementierung treffen — betrifft das Datenmodell

---

### Offene Architekturentscheidung (VOR der Implementierung klären)

**Frage:** Wie modellieren wir reaktive Stratagems im `Stratagem`-Dataclass?

**Option A:** Neues Feld `trigger_type: proactive | reactive` + optionales `trigger_event`
```yaml
trigger_type: reactive
trigger_event: after_roll   # after_roll | on_destroy | on_target | on_declaration
applicable_phases: [shooting, fight, charge, psychic, movement]
```

**Option B:** `phase`-Feld bleibt, aber als Liste. `stage: reactive` als neuer Stage-Wert.

**Option C:** Kein Schema-Change — nur `phase: [shooting, fight]` statt `any` korrigieren, reaktive Semantik im `rule_text` belassen (pragmatisch, kein Engine-Aufwand)

→ **Empfehlung für die Review-Session:** Zunächst Option C (Datenkorrekturen ohne Schema-Erweiterung), und parallel dokumentieren welche GOs reaktiv sind. Dann separat entscheiden ob ein neues Feld sinnvoll ist.

---

### Ablauf der Review-Session (Stand 2026-06-04)

1. ✅ **Schema-Entscheidung** → Option A gewählt: `timing`, `event`, `once_per_battle`, `effect: Effect` zu `Stratagem`-Dataclass ergänzt; `phase: str | list[str]`; `stratagem_visibility()` angepasst
2. ✅ **`_shared/stratagems.yaml`** — alle 7 GOs korrigiert (timing/event/phase/once_per_battle/effect)
3. ✅ **Bekannte Fehler `necrons/stratagems.yaml`** — 7 GOs korrigiert (phase, player, timing, event, effect, variable CP-Kommentare)
4. ✅ **Bekannte Fehler `orks/stratagems.yaml`** — wreckaz + careen korrigiert
5. ⬅ **Vollständige Review `necrons/stratagems.yaml`** — 52 verbleibende GOs noch nicht geprüft
6. ⬅ **Vollständige Review `orks/stratagems.yaml`** — 21 verbleibende GOs noch nicht geprüft
7. ⬅ **`faction_abilities.yaml`** (necrons + orks) — Trigger/Conditions spot-check
8. ⬅ Optional: neue Tests für korrekte Phase/Stage-Werte

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

YAML (powers.yaml — NEU)          → load_powers() [noch nicht verdrahtet]
YAML (_shared/shared_powers.yaml) → smite, deny_the_witch, perils — stub
YAML (_shared/shared_abilities.yaml) → load_shared_abilities() [noch nicht verdrahtet]
YAML (_shared/stratagems.yaml)    → load_stratagems() [war universal/, jetzt _shared/]
```

### _shared/-Verzeichnis (aktueller Stand)
| Datei | Inhalt | Loader-Status |
|-------|--------|--------------|
| `_shared/stratagems.yaml` | 7 Core Stratagems | verdrahtet (`load_stratagems()`) |
| `_shared/shared_abilities.yaml` | ObjSec, DS, FNP, Fly + 3 weitere | Stub, nicht verdrahtet |
| `_shared/shared_powers.yaml` | Smite, Deny, Perils | Stub, nicht verdrahtet |
| `_shared/detachment_types.yaml` | Patrol–Air Wing + CP-Felder | verdrahtet (`load_detachment_types()`) |

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

## Mittelfristige Roadmap (nach der Review-Session)

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

### 2026-06-04, Session 4 — 6-Batch-Plan vollständig

Alle Batches 0–6 implementiert: Folder-Merge, YAML-Datenkorrekturen, Shared-Dateien,
Orks powers.yaml, Alias-Entfernung, Spec-Doku, 27 neue Tests.
426 Tests grün. Bugfix: Archive-Log-Crash (list vs. dict).

### 2026-06-04, Session 3 — Planung & Forschung (kein Code)

Subfaction-Affinitäten für Necrons (4 falsch) und Custodes (2 falsch + 1 ID) verifiziert.
Core Rules Inventory via Wahapedia. Vollständiger 6-Batch-Plan formuliert.

### 2026-06-03, Session 2 — Bugfixes

Battle Log TypeError gefixt. Inaktiver Spieler konnte Protokoll aktivieren — gefixt.

### 2026-06-03, Session 1

WAAAGH! Datenfehler korrigiert. Generisches Fähigkeitssystem implementiert.
