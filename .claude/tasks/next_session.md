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
| **Ziel 6d — Simultane Attackensequenz (alt)** | ✅ committed (wird durch 6d-v2 ersetzt) |
| **Ziel 6d-v2 — Attackensequenz Overhaul** | 🔵 Design fertig, Implementierung ausstehend |
| **Datenqualitäts-Review** | ✅ vollständig (Stratagems + faction_abilities) |

Teststand: **454 Tests grün**

---

## Was wurde zuletzt gemacht (2026-06-04, Session 9)

**P0 — Pistol-in-Melee Bug Fix:**
- `shootingPhase.py`: `can_shoot()` erlaubt Schuss wenn Einheit im Nahkampf UND Pistol-Waffe hat; `_active_shooting()` filtert Waffenliste auf Pistolen + zeigt Info-Badge; `_render_display()` übergibt `in_melee` an `render_attack_form()`
- `_common.py`: `render_attack_form()` — neuer `in_melee: bool = False` Parameter; Waffenfilter auf `weapon_type.startswith("Pistol")` wenn `in_melee=True`

**P1 — Scenario-Mockups:**
- 4 neue JSON-Dateien: `necrons_shoot_orks.json`, `orks_fight_necrons.json`, `orks_shoot_necrons.json`, `necrons_fight_orks.json`
- Alle mit `p1_units`/`p2_units` Keys; Roster `necrons_alpha.yaml` (p1) + `orks.yaml` (p2); active-Keys `"Necrons α"` / `"Orks"`
- `orks_shoot_necrons.json`: Boyz in Melee mit Warriors → demonstriert Pistol-only-Verhalten nach Fix
- `necrons_fight_orks.json`: Skorpekhs CHARGED, Warriors ebenfalls im Nahkampf → RP nach Verlusten relevant

Teststand: **454 Tests grün**

---

## ⬅ NÄCHSTE SESSION: Ziel 6d-v2 — Attackensequenz Overhaul (P2)

Design vollständig abgestimmt (Session 8). P0+P1 abgehakt. Nächster Schritt: Implementierung beginnen.

**Empfohlener Einstieg:** Plan zeigen + Freigabe holen für den ersten 6d-v2 Task:
> `uiLayout/_common.py`: `render_attack_form()` aufteilen in `render_attack_declaration()` + `render_attack_resolution_tab()`

---

## Was wurde zuletzt gemacht (2026-06-04, Session 8 — Design)
- `necrons/faction_abilities.yaml` + `orks/faction_abilities.yaml` — Spot-Check: alle Trigger/Conditions korrekt, keine Korrekturen nötig

**Ziel 6g Restpunkt:**
- `game_state.py`: `init_state()` ruft jetzt `set_log_players(p1_name, p2_name)` auf

**Ziel 6d — Simultane Attackensequenz:**
- `combat.py`: 3 neue Pure-Functions — `resolve_attack_modifiers()` (Hit/Wound-Schwellwerte + Modifier-Stack, Heavy-Penalty, ±1-Cap), `resolve_save()` (Rüstung vs. Invuln, Stack), `resolve_fnp()` (None wenn ignoriert/abwesend)
- `weapon.py` + `loader.py`: `ignores_fnp: bool = False` auf `WeaponProfile`, aus YAML parsbar
- `_common.py`: `render_attack_form()` komplett neu — 2-Spalten-Layout: Angreifer (Treffer/Verwundung-Block mit Modifier-Stack und Quellen) | Verteidiger (Rettungswurf, FNP konditional, Schaden-Input + Mortal-Wounds-Input, ein Apply-Button); altes Resolve→Apply-Zweischritt-System entfernt
- `tests/test_combat_6d.py`: 28 neue Tests (454 gesamt, alle grün)

---

## ⬅ NÄCHSTE SESSION: Ziel 6d-v2 — Attackensequenz Overhaul

Design ist vollständig abgestimmt (Session 8, 2026-06-04). Vor Implementierung: Plan zeigen + Freigabe holen.

### P0 — Bug-Fix (unabhängig, klein)
- **Pistol in Melee** — `can_shoot()` in `shootingPhase.py`: Einheit im Nahkampf darf Pistolen abfeuern. Korrekte Logik: wenn `in_melee` → nur Waffen mit `weapon_type` starting "Pistol" anzeigen + Schuss erlauben; alle anderen Waffen blockiert.

### P1 — Scenario-Mockups für Testhilfe (klein, eigenständig)
Infrastruktur ist fertig (`data/scenarios/`, `?scenario=` URL-Parameter, `scenarios.py`). Neue Szenarien:
- `necrons_shoot_orks.json` — Shooting Phase, Necrons aktiv: Immortals (Tesla Carbines, 5 Modelle, 10 LP) → Ork Boyz (20 Modelle, 20 LP). Tesla-Badge sichtbar.
- `orks_fight_necrons.json` — Fight Phase, Orks aktiv: Boyz (20 Modelle) im Nahkampf mit Warriors (10 Modelle) + Skorpekh Destroyers (3 Modelle, 9 LP). Whirling Onslaught aktivierbar (Necrons reaktiv). RP nach Apply relevant.
- `orks_shoot_necrons.json` — Shooting Phase, Orks aktiv: Boyz mit Sluggas (Pistol 1!) → Warriors (einige in Melee → Pistol-Bug sichtbar).
- `necrons_fight_orks.json` — Fight Phase, Necrons aktiv: Skorpekh Destroyers (3 Modelle, geladen → CHARGED-Badge) → Boyz. Whirling Onslaught ist defensive Necron-GO, hier irrelevant für Angreifer.
- **Achtung:** Bestehende Szenarien nutzen falsche Keys (`necron_units` statt `p1_units`). Alle 4 neuen Szenarien mit `p1_units`/`p2_units` schreiben. Roster-Kombi: `necrons_alpha.yaml` (p1) + `orks.yaml` (p2).

### P2 — Ziel 6d-v2 Kern-Redesign (groß, mehrere Sessions)
Vollständige Spec in `docs/goals/ziel6.md` Abschnitt "6d-v2". Kurzüberblick:

**Phase 1 — Deklaration (gameActionArea übernehmen):**
1. Angreifer ist bereits gewählt (via unitCard-Klick, wie bisher)
2. Ziele wählen (mehrere möglich) + Modelle-Counter pro Ziel
3. Waffe wählen (bei mehreren Waffen; triviale Fälle auto-selektiert)
4. Waffenprofil wählen (bei mehreren Profilen; gesperrte Optionen ausgegraut mit Grund)
5. Bestätigen → Tabs öffnen

**Phase 2 — Auflösung (Tabs):**
Ein Tab pro (Waffe × Zieleinheit). Inhalt: Hit-Block → Wound-Tabelle → Save-Block → Damage-Block.

**Damage-Block:**
- Modelle verloren `[0][−][+]`
- Wunden auf Frontmodell `[0][−][+]` (nur wenn Ziel nLP-Modelle hat)
- Tödliche Verwundungen `[0][−][+]` (immer)
- Apply → Tab lockt; Reset-Button bis Phase-End

**Necron RP-Block** (erscheint nach Apply wenn Necron-Einheit Verluste hatte):
- Würfelanzahl = Summe LP der gefallenen Modelle
- Erfolg 5+ pro Würfel; Modelle zurück `[0][−][+]`

### Verbleibende Optionen aus Session 7 (nachrangig)
- **6e — CP-Doppelvergabe-Fix**: `cp_granted_this_phase`-Flag in `commandPhase.py`
- **Subfaction Affinity UI**: `_render_protocol_ui()` — aktive Subfaction == Affinität → beide Direktiven aktiv
- **AdMech Canticles YAML**: `faction_abilities.yaml` + `secondary` optional

---

## Offene Entscheidungen

| Entscheidung | Optionen |
|---|---|
| **`once_per_battle` enforcement** | Braucht `used_this_battle: set[str]` in Session-State + neuen Parameter in `stratagem_visibility()`. Wann implementieren? |
| **Variable CP-Kosten** | Derzeit nur Kommentar im YAML. Optionen: (a) so lassen, (b) `cp_cost_max: int` Feld, (c) `cp_cost_condition: str` Feld + Logik |
| **Reaktive GO UI** | `timing: phase_reactive` GOs sind korrekt markiert — aber UI zeigt sie gleich wie proaktive. In 6d-v2 erscheinen reaktive GOs des Verteidigers inline im Deklarations-Bereich. |
| **Stratagem Reset-Button** | Aktivierte GOs brauchen einen Reset-Button. Vor Phase-End reversibel; danach fest im Log. Implementierung als Teil von 6d-v2. |
| **Cover-Toggle** | Default "kein Cover". Light Cover (+1 save, Shooting), Dense Cover (−1 hit, Shooting), Heavy Cover (+1 save vs Melee, außer nach Charge). Alle drei als Dropdown im Save-Block. Display-only — App trackt nicht ob Terrain physisch vorliegt. |

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

### Attackensequenz-Design-Constraints (6d-v2, Stand 2026-06-04)
- **Kein Input für Zwischenergebnisse** — keine Treffer-/Verwundungs-Eingabe. App zeigt Info, Spieler würfelt am Tisch.
- **Granularität Fernkampf**: pro Modell-Waffe, nicht pro Waffentyp. 10 Warriors = 10 unabhängige Waffen.
- **Überschuss-Schaden bei normalen Attacken verfällt** — bei nLP-Modellen deshalb getrennte Eingabe: Modelle + Wunden Frontmodell.
- **Tödliche Verwundungen** tragen zwischen Modellen über — separater Counter immer sichtbar.
- **RP-Würfel** = Summe LP-Charakteristik aller gefallenen Modelle (1LP-Warrior = 1 Würfel; 3LP-Skorpekh = 3 Würfel). Erfolg 5+.
- **Pistol in Melee**: Einheiten im Nahkampf dürfen nur Pistolen abfeuern — alle anderen Waffen ausgeblendet.
- **Zielansage vor Auflösung** (Regelkonform, 9E Core): alle Targets + Waffen deklarieren, dann erst Tabs starten.
- **Waffe → Profil**: triviale Fälle (1 Waffe, 1 Profil) auto-selektiert; gesperrte Profile (z.B. Heavy Stationary) ausgegraut mit Grund.
- **Scenario-JSON-Keys**: immer `p1_units` / `p2_units`, nicht fraktionsspezifische Namen.

---

## Mittelfristige Roadmap

| Schritt | Was | Status |
|---------|-----|--------|
| faction_abilities spot-check | Necrons + Orks faction_abilities.yaml | ✅ |
| 6g Restpunkt | set_log_players() in init_state() | ✅ |
| 6d — Attackensequenz simultan (alt) | combat.py + UI | ✅ |
| **Pistol-Bug-Fix** | `can_shoot()` in Melee nur Pistolen erlauben | ✅ |
| **Scenario-Mockups** | 4 neue JSON-Szenarien (Necrons↔Orks, Shooting+Fight) | ✅ |
| **6d-v2 — Attackensequenz Overhaul** | Deklaration + Tabs + neue Blöcke (Wound-Tabelle, RP, Cover) | ⬜ P2 |
| 6e — CP-Doppelvergabe-Fix | `cp_granted_this_phase`-Flag | ⬜ |
| subfaction_affinity UI | Wenn aktive Subfaction == Affinität → beide Direktiven aktiv | ⬜ |
| AdMech Canticles YAML | `data/wh40k_9e/adeptus_mechanicus/faction_abilities.yaml` | ⬜ |
| T'au Mont'ka/Kauyon YAML | Runden-Fenster-Mechanik | ⬜ |
| Auto-Progression Space Marines | Doctrines, neuer ability_type | ⬜ |
| 6f — Ability-Badges unitCard | hängt von 6d-v2 ab | ⬜ |
| load_powers() verdrahten | Psychic Phase, Orks Weirdboy | ⬜ |
| load_shared_abilities() verdrahten | Universalregeln im Engine | ⬜ |

---

## Historische Session-Notizen

### 2026-06-04, Session 8 — Design-Session: Attackensequenz Overhaul
Vollständiges Zielbild für 6d-v2 erarbeitet. Wichtigste Entscheidungen: kein Input für Zwischenergebnisse (nur Modellverluste + Tödliche Verwundungen); Deklarations-Phase (alle Targets + Waffen) vor Tab-Auflösung; Granularität Fernkampf = pro Modell-Waffe; Überschuss-Schaden verfällt bei normalen Attacken; RP-Würfel = Summe LP der gefallenen Modelle; Pistol-Bug identifiziert; Cover-Regeln verifiziert (Light/Dense/Heavy); Whirling Onslaught als Verteidigungs-GO inline im Deklarationsbereich. Bestehende Scenario-JSON-Infrastruktur gefunden und nutzbar.

### 2026-06-04, Session 7 — Ziel 6d + 6g + faction_abilities Review
faction_abilities Necrons + Orks geprüft — OK, keine Korrekturen. set_log_players in init_state. render_attack_form komplett neu: 2-Spalten simultanes Layout, 3 Pure-Functions (resolve_attack_modifiers/save/fnp), ignores_fnp-Feld, 28 neue Tests. 454 Tests grün.

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
