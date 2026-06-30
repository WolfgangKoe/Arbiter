# Ziel 6 — UI-Overhaul, ArmyCard, Attackensequenz, Fähigkeiten-Integration 🔄

**Voraussetzung:** Ziel 5 (inkl. 5i) abgeschlossen. ✅

---

## Übersicht

Ziel 6 besteht aus sieben Teilzielen, die unabhängig voneinander implementiert werden können:

| Teilziel | Thema | Abhängigkeiten |
|----------|-------|----------------|
| **6a** ✅ | gameHeader Redesign | – |
| **6b** ✅ | armyCard — generisches Fähigkeitssystem | – |
| **6c** ✅ | gameProtocoll — Stratagems als Default, Modifier-Export | 6b |
| **6d** ✅ | Attackensequenz — simultane Darstellung (Basis-Implementation) | 6b, 6c |
| **6d-v2** 🔵 | Attackensequenz — vollständiges UI-Redesign (Design abgestimmt) | 6d |
| **6e** ✅ | Fähigkeiten-Integration — Command Protocols regelkonform + Stratagem-Visibility-Fix | 6b |
| **6f** → Ziel7 | Ability-Badges und Keyword-Highlighting auf unitCard (→ Ziel7, abhängig von 6e Execute-Logik) | 6e |
| **6g** ✅ (teilw.) | Game Log — Archiv + Setup-UI | – |
| **6h** ✅ (teilw.) | Generisches Fraktion-Fähigkeits-System | 6b |
| **Daten-Review** 🔄 | YAML-Vollständigkeit (Silent King ✅, weitere Einheiten offen) | – |

---

> **Teilziele 6a–6d** (inkl. 6d-v2, 6d-v3, Testsession-Fixes) sind ausgelagert nach
> [archive/ziel6_6a_6e.md](archive/ziel6_6a_6e.md) — der Großteil ist ✅; die wenigen offenen
> Einzelpunkte dort werden über aktive Pläne/Backlog weiterverfolgt (s. Liste unten).

### Offene Restpunkte aus 6a–6d (weiterverfolgt — nicht nur im Archiv)

Damit kein offener Punkt ausschließlich im Archiv existiert, hier der Verbleib der noch offenen
6a–6d-Tasks. Acht sind durch aktive Artefakte gedeckt, zwei werden hier aktiv weitergeführt:

- [ ] **Attacken-Auflösung in allen drei Kontexten verifizieren** (Shooting / Fight / Overwatch
  in Charge) — Overwatch-Teil → Plan 015; der generische Kontext-Check bleibt hier offen.
- [ ] **Tests für Damage-Block + RP-Würfellogik** (aus 6d-v2) — noch kein eigener Plan; hier offen.

Durch aktive Artefakte gedeckt (im Archiv belassen):
- `render_attack_form()` ersetzen → obsolet durch Plan 013 (einheitlicher Gruppen-Flow, DONE).
- Fähigkeit + AP kombinierte Badge → Plan 017 (backlog 🟡).
- Counterattack-GO / Overwatch-GO / Non-CHARACTER-HI → Plan 015.
- GO-Buttons kontextuell → backlog 🟡. Regelkasten immer oben → backlog 🟡.
- Gretchin Cowardly → Plan 018 (backlog 🟢).

---

## 6e — Fähigkeiten-Integration in alle Phasen

**Ziel:** Fähigkeiten aus Armee, Einheit, Ausrüstung und Stratagems greifen in den richtigen Phasen. CP-Doppelvergabe-Bug gefixt.

### ⚠️ Command Protocol Bugs (Session 2026-06-04)

Die aktuelle Implementierung weicht in drei Punkten von der Regelregel ab:

**Bug 1 — `auto_round_1` existiert nicht in den Regeln:**
Die Regeln erlauben, alle 5 Protokolle frei auf Runden 1–5 zu verteilen. `auto_round_1: true` für Eternal Guardian ist eine erfundene Einschränkung. Das Setup zeigt nur Runden 2–5 (`range(2,6)`) — muss `range(1,6)` sein. Das Flag muss aus YAML, Dataclass, Setup-UI und commandPhase.py entfernt werden.

**Bug 2 — 6. Protokoll fehlt komplett:**
Es gibt 6 Protokolle; 5 werden Runden zugewiesen, das 6. (übrige) ist **jede Runde zusätzlich aktiv**. Die Spielerin wählt dessen Direktive am Rundenanfang. Die App kennt dieses Konzept nicht.

**Bug 3 — Dynastiebonus fehlt:**
Falls das 6. Protokoll das Dynastieprotokoll ist (z.B. Eternal Guardian für Nihilakh), gelten **beide Direktiven** gleichzeitig. Erfordert Dynast-Info im Roster/Unit-Daten — noch nicht vorhanden.

Betroffene Dateien: `faction_abilities.yaml` (Flag weg), `command_protocol.py` (Feld weg), `gameActionsArea.py` (Setup-UI), `commandPhase.py` (Render-Logik), `game_state.py` (`active_protocol_id = "eternal_guardian"` weg).

### ⚠️ Stratagems und Phasenbedingungen (Session 2026-06-04)

Stratagems sind daten-seitig vollständig (`phase`, `timing`, `event`, `once_per_battle` gesetzt), aber die **Anbindung in den Phase-Handlern ist unvollständig**:
- `timing: phase_reactive` GOs werden wie proaktive behandelt (UI-Unterschied fehlt)
- Keine Phase-Handler rufen `stratagem_visibility()` mit korrektem `stage` auf
- Effekte aktiver GOs (`modifier`-Feld) werden in der Attackensequenz nicht ausgewertet
- `once_per_battle` wird nicht enforced

### Tasks

- [x] `gameMechanic/commandPhase.py`: CP-Vergabe als einmaligen Phase-Grant implementieren (Flag `cp_granted_this_phase` im Session-State, Reset beim Phasenwechsel) ✅ (S55 verifiziert; Befund: kein Battle-forged-Gating → backlog R-CMD-03)
- [ ] `gameMechanic/commandPhase.py`: Einheiten mit Befehlsphase-Fähigkeiten anzeigen (ähnlich Psiphase-Hinweise)
- [ ] `gameMechanic/ability_engine.py`: `collect_modifiers_for_phase(phase, attacker_unit, weapon, target_unit)` — sammelt alle aktiven Modifier aus allen Quellen → **Ziel7 (subfaction Execute-Logik)**
- [ ] `gameObjects/ability.py`: Ability-Schema um `modifier`-Felder erweitern (analog zu Stratagem in 6c) → **Ziel7**
- [ ] `data/wh40k_9e/*/unit_abilities.yaml` + `faction_abilities.yaml`: Modifier-Felder für relevante Fähigkeiten nachtragen (Pilot: Necrons + Orks) → **Ziel7**
- [ ] Phase-Handler (Shooting, Fight, Charge): rufen `collect_modifiers_for_phase()` auf und übergeben Ergebnis an Attackensequenz-Renderer → **Ziel7**
- [x] Command Protocol Bug 1 — `auto_round_1` komplett entfernen ✅ (2026-06-05)
- [x] Command Protocol Bug 2 — 6. Protokoll (immer aktiv) + eigene Direktiven-Wahl ✅ (2026-06-05)
- [x] Command Protocol Bug 3 — Dynastiebonus; `dynasty`-Feld in Roster-YAML ✅ (2026-06-05)

---

## 6f — Ability-Badges und Keyword-Highlighting auf unitCard → **Ziel7**

**Ziel:** Aktive Buffs auf einer Einheit sind auf der unitCard sofort sichtbar.

> **Ausgelagert nach Ziel7:** Abhängig von `collect_modifiers_for_phase` (6e Execute-Logik),
> die ebenfalls nach Ziel7 wandert. Spec bleibt hier als Referenz.

### Spec

- Badge pro aktivem Buff (Stratagem, Fähigkeit, Protokoll) auf der unitCard
- Badge zeigt: Name der Quelle + Ablauf (z.B. "bis Phasenende")
- Ablauf-Logik kommt aus `active_modifiers` (6c) — Badge verschwindet wenn Modifier abläuft
- Betroffene Keywords visuell hervorgehoben wenn eine Fähigkeit auf sie zutrifft

### Tasks → Ziel7

- [ ] `uiLayout/unitCard.py`: `active_modifiers` aus Session-State lesen, Badges für betroffene Einheit rendern
- [ ] `uiLayout/unitCard.py`: Keyword-Highlighting wenn `active_modifiers` ein Keyword-Condition-Modifier betrifft
- [ ] `gameMechanic/game_state.py`: `active_modifiers` Datenstruktur definieren: `{unit_key, source, effect, expires_at_phase, expires_at_round}`

---

## 6g — Game Log — Archiv, strukturiertes Format, Setup-UI

**Ziel:** Reset archiviert das Log. Das Format ist für Crusade-Vorbereitung (Ziel 8) geeignet. Setup-Screen hat eine Log-Verwaltungs-UI.

### Log-Format (JSON)

```json
{
  "game_id": "2026-06-03T14:22:00",
  "players": {"first": "Necrons", "second": "Orks"},
  "rounds": [
    {
      "round": 1,
      "phases": [
        {
          "phase": "shooting",
          "active": "Necrons",
          "events": [
            {
              "type": "attack",
              "attacker_unit": "wh40k_9e.necrons.unit.warriors",
              "attacker_unit_name": "Warriors",
              "target_unit": "wh40k_9e.orks.unit.boyz",
              "target_unit_name": "Boyz",
              "weapon": "gauss_flayer",
              "damage_dealt": 2,
              "mortal_wounds": 0,
              "target_destroyed": false
            }
          ]
        }
      ]
    }
  ],
  "result": {"winner": "Necrons", "vp": {"Necrons": 75, "Orks": 42}}
}
```

### Tasks

- [x] `gameMechanic/game_log.py`: Log-Format auf strukturiertes JSON (game_id/players/rounds/phases/events)
- [x] `gameMechanic/game_log.py`: `archive_and_reset_log()` — verschiebt aktuelles Log nach `data/log/archive/<game_id>.json`
- [x] `gameMechanic/game_state.py`: `reset_game()` ruft `archive_and_reset_log()` auf
- [x] `uiLayout/setupScreen.py`: Archiv-Verwaltungs-Sektion (Liste, Download, Löschen mit Bestätigung)
- [x] `gameMechanic/game_state.py`: `init_state()` ruft `set_log_players()` auf (Spielernamen im Log-Header)
- [ ] Prüfen: Nach Reset keine alten Einträge im Battle Log sichtbar

---

## 6h — Generisches Fraktion-Fähigkeits-System (alle Fraktionen)

**Ziel:** Die App funktioniert korrekt für ALLE Fraktionen, nicht nur für Necrons und Orks. Das Fähigkeitssystem ist vollständig generisch — neue Fraktionen erfordern nur YAML-Daten, keinen Code-Änderungen.

**Hintergrund:** Wahapedia-Recherche (2026-06-03) ergab 6 Fähigkeitskategorien über alle 10 Hauptfraktionen.
Vollständige Spec: `docs/spec/faction_abilities.md`. Schema-Beispiele: `data/wh40k_9e/_schema/`.

### Kategorie 1 — Runden-Wahl (identisch zu Command Protocols)

| Fraktion | Mechanik | Status |
|----------|----------|--------|
| Necrons | Command Protocols (6 Optionen, Primary/Secondary) | ✅ implementiert |
| **Adeptus Custodes** | **Martial Ka'tah (6 Ka'tahs, Aggressive/Stoic Stance)** | ✅ YAML vorhanden; Custodes Rendax Ka'tah Secondary → Backlog (toter strength_modifier-Pfad) |
| **Adeptus Mechanicus** | **Canticles of the Omnissiah (6, kein Secondary)** | ⬜ **blocked-by-YAML** — kein `adeptus_mechanicus/`-Verzeichnis; daten-first → **Ziel7** |
| **Tyranids** | **Synaptic Imperatives (bis 10, dynamischer Pool)** | ⬜ **blocked-by-YAML + Pool-Logik** — kein `tyranids/`-Verzeichnis → **Ziel7** |

**Code-Änderungen nötig:**
- [ ] `gameObjects/loader.py`: `CommandProtocol.secondary` + `secondary_effect` optional machen (Voraussetzung für AdMech) → **Ziel7**
- [ ] `armyCard._render_protocol_ui()`: Falls kein secondary: Directive-Wahl überspringen, direkt auto-apply → **Ziel7**
- [ ] Tyranids: Pool-Check ob Synapse-Unit noch lebt (Unit-Keyword-Check in UI) → **Ziel7**

**YAML nötig:**
- [x] `data/wh40k_9e/adeptus_custodes/faction_abilities.yaml` — alle 6 Ka'tahs ✅ (Batch 1+)
- [ ] `data/wh40k_9e/adeptus_mechanicus/faction_abilities.yaml` — alle 6 Canticles → **Ziel7**
- [ ] `data/wh40k_9e/tyranids/faction_abilities.yaml` — alle Synaptic Imperatives → **Ziel7**

**Tests nötig:**
- [x] `tests/test_faction_abilities_custodes.py` — ✅ (Batch 6)
- [ ] `tests/test_faction_abilities_admech.py` — load, no-secondary auto-apply → **Ziel7**
- [ ] `tests/test_faction_abilities_tyranids.py` — dynamic pool when synapse units die → **Ziel7**

### ⚠️ Hardcoded Fraktionslogik — Inventar (Stand 2026-06-08)

Keine Fraktion darf namentlich in gameMechanics/uiLayout hardcoded sein.

| Datei | Problem | Status |
|---|---|---|
| `commandPhase.py` | `_OVERLORD_ID = "wh40k_9e.necrons.unit.overlord"` | ✅ entfernt (6k) |
| `unitCard.py` | `_overlord_id` (doppelt) | ✅ entfernt (6k) |
| `game_state.py` | `is_necron_faction()` | ✅ entfernt (6e) |
| `game_state.py` | `active_protocol_id = "eternal_guardian"` | ✅ entfernt (6e Bug 1) |
| `faction_abilities.yaml` | `auto_round_1: true/false` | ✅ entfernt (6e Bug 1) |
| `psychicPhase.py` | `"gloom_prism" in u.rules` in `can_deny()` | ✅ generisch via `load_deny_wargear_names` (6j) |
| `unitCard.py:248` | `"wh40k_9e.necrons.wargear.resurrection_orb" in unit.wargear_ids` | ✅ erledigt (6k) → **Fix A** |
| `game_state.py` | `resurrection_orb_used = False` in globalem `init_state` | ✅ erledigt (S72) → **Fix D** |
| `armyCard.py:_render_waaagh_ui` | `"WARBOSS"` Keyword + `"waaagh" in a.id` + Effekttexte hardcoded | 🟡 offen → **Fix B** |
| `armyCard.py:_render_protocol_ui` | `active_protocol_id` / `active_directive` nicht per-Fraktion | ✅ erledigt (S52/S72) → **Fix C** |
| `_common.py` | `waaagh_state` im Attacken-Resolver (Stärke/Attacken-Modifier) | ✅ erledigt (S41 — `activated_abilities` ersetzt `waaagh_state`) |

---

### 6h — Generifizierungs-Plan (Audit 2026-06-08)

#### Fix A — unitCard: Resurrection Orb Bearer-Ausschluss ohne Wargear-ID ✅ (6k, 2026-06-07)

**Problem:** `unitCard.py:248` prüfte eine konkrete Necron-Wargear-ID.

**Gelöst (6k):** `unit.wargear_ids` enthält jetzt die IDs; `unitCard.py` prüft
`"resurrection_orb" in unit.wargear_ids`-Logik ist vollständig generisch über den Loader abgebildet.
Kein hardcodierter Wargear-ID-String mehr in `src/` (grep liefert 0 Treffer).

**Dateien:** `commandPhase.py`, `unitCard.py` — erledigt

---

#### Fix B — armyCard: WAAAGH!-UI vollständig generisch (🟡 mittel)

**Problem:** `_render_waaagh_ui` hat drei hardcoded Stellen:

1. **Ability-Suche per ID-String:** `"waaagh" in a.id.lower()` → Ersetzen durch generische Bedingung: alle `activated` Command-Phase-Abilities, deren `conditions[0].once_per_battle == True`. Das YAML hat das bereits als `once_per_battle: true` in den Conditions.

2. **WARBOSS-Keyword:** `has_warboss = any(u.has_keyword("WARBOSS") ...)` → Ersetzen durch `any(check_conditions(ability, u, {}) for u in units)` — die Ability-Conditions enthalten bereits `has_keywords: [WARBOSS]`.

3. **Effekttexte:** Stage-1- und Stage-2-Texte hardcoded → YAML-Feld `active_text` in `faction_abilities.yaml` ergänzen; `Ability`-Dataclass um optionales `active_text: str | None` erweitern.

```yaml
# faction_abilities.yaml (Orks) — Ergänzung:
- id: wh40k_9e.orks.faction.waaagh_stage1
  active_text: "+1 Strength · +1 Attacks · 5+ invuln · Advance & Charge"
  ...
- id: wh40k_9e.orks.faction.waaagh_stage2
  active_text: "+1 Strength · +1 Attacks · 6+ invuln"
  ...
```

**Dateien:** `gameObjects/ability.py`, `gameObjects/loader.py`, `data/wh40k_9e/orks/faction_abilities.yaml`, `armyCard.py`

---

#### Fix C — armyCard/ability_engine: Protokoll-Session-Keys per Fraktion ✅ (S52/S72)

**Problem:** Globale Session-State-Keys konnten bei zwei Round-Choice-Fraktionen kollidiern.

**Gelöst:** `round_choice_state_key(player, kind)` aus `game_state.py` setzt Keys auf den
**Player-Slot** (`first_player` / `second_player`), nicht auf die Fraktion. Jeder Spieler hat
damit isolierte Keys — Necrons vs. Custodes spielen gleichzeitig korrekt.
Belegt via `grep "round_choice_state_key" src/` → alle Reads in `armyCard.py` + `ability_engine.py`
nutzen diesen Key.

**Dateien:** erledigt (S52 Umbenennung + S72 Verifikation)

---

#### Fix D — game_state: `resurrection_orb_used` aus globalem Init herauslösen ✅ (2026-06-20)

**Problem:** `game_state.py init_state()` initialisierte `resurrection_orb_used = False`.

**Gelöst:** `init_state()` setzt jetzt `wargear_used: dict[str, bool] = {}` — vollständig generisch.
`commandPhase.py` schreibt per Wargear-ID. Kein Fraktions-String in `game_state.py` mehr.

**Dateien:** `gameMechanic/game_state.py`, `gameMechanic/commandPhase.py` — erledigt

---

#### Reihenfolge

| Priorität | Fix | Status | Abhängigkeit |
|---|---|---|---|
| 1 | **A** — unitCard Orb-Bearer | ✅ erledigt (6k) | — |
| 2 | **D** — wargear_used generic | ✅ erledigt (S72) | — |
| 3 | **B** — WAAAGH! generisch | 🟡 offen (YAML-Erweiterung nötig) | — |
| 4 | **C** — Protokoll-Keys per Fraktion | ✅ erledigt (S52/S72) | — |

### Kategorie 2 — Einmalig-Deklariert (wie WAAAGH!)

| Fraktion | Mechanik | Status |
|----------|----------|--------|
| Orks | WAAAGH! (2 Stages) | ✅ implementiert |
| **T'au Empire** | **Mont'ka / Kauyon (Runden-Fenster)** | ⬜ **blocked-by-YAML** — kein `tau_empire/`-Verzeichnis → **Ziel7** |

**Code-Änderungen nötig:**
- [ ] `armyCard._render_waaagh_ui()`: `active_rounds`-Feld aus YAML auslesen; Badge nur zeigen wenn aktuelle Runde im Fenster liegt → **Ziel7**
- [ ] `game_state._reset_turn_state()`: Runden-Fenster-Prüfung für T'au ergänzen → **Ziel7**

**YAML nötig:**
- [ ] T'au `faction_abilities.yaml`: `montka` + `kauyon` mit `active_rounds` Feld → **Ziel7**

**Tests nötig:**
- [ ] `tests/test_faction_abilities_tau.py` — montka_active_rounds, kauyon_active_rounds → **Ziel7**

### Kategorie 3 — Auto-Progression (kein Player-Input) → **Ziel7**

> Alle drei Fraktionen fehlen als Datensatz — kein Verzeichnis unter `data/wh40k_9e/`.
> Komplette Kategorie ist **blocked-by-YAML** und wird nach **Ziel7** ausgelagert.

| Fraktion | Mechanik | Status |
|----------|----------|--------|
| Space Marines | Combat Doctrines (R1 Heavy / R2 Assault / R3+ Melee) | ⬜ blocked-by-YAML → Ziel7 |
| Death Guard | Contagions of Nurgle (Reichweite skaliert) | ⬜ blocked-by-YAML → Ziel7 |
| Chaos SM | Let the Galaxy Burn (R1+R2 auto, R3 Wahl) | ⬜ blocked-by-YAML → Ziel7 |

**Code-Änderungen nötig → Ziel7:**
- [ ] `ability_engine.py`: `get_auto_progression_modifier(faction_dir, phase, round)` → `dict[str, int]`
- [ ] `armyCard.py`: `_render_auto_progression_badge(faction)` — Info-Badge ohne Button
- [ ] `_common.py`: Auto-Progression-Modifier in `render_attack_form()` einbinden

**YAML nötig → Ziel7:**
- [ ] `ability_type: auto_progression` + `progression: [{round, effects}]` Schema (Beispiel: `_schema/auto_progression.example.yaml`)
- [ ] YAML für Space Marines, Death Guard, Chaos SM

**Tests nötig → Ziel7:**
- [ ] `tests/test_auto_progression.py` — round→modifier Mapping, round_max, kein Player-Input

---

## Daten-Review — Stratagem-Schema + fachliche Korrekturen

**Ziel:** Alle YAML-Datendateien fachlich gegen Wahapedia verifizieren. Jede GO erhält korrekte `phase`, `stage`, `player`, `timing`, `event` und ein maschinenlesbares `effect`-Feld.

### Schema-Erweiterung `Stratagem`-Dataclass (2026-06-04)

Neue Felder (konsistent mit `Ability.Trigger` / `Ability.Effect`):

| Feld | Typ | Bedeutung |
|------|-----|-----------|
| `phase` | `str \| list[str]` | Einzelphase oder Liste; `"any"` nur wenn wirklich jede Phase gilt |
| `timing` | `str \| None` | `None` = proaktiv; `"phase_reactive"` = reaktiv auf Ereignis |
| `event` | `str \| None` | `"after_roll"` / `"on_destroy"` / `"on_target"` / `"on_declaration"` |
| `once_per_battle` | `bool` | `True` wenn rule_text "once per battle" sagt |
| `effect` | `Effect \| None` | Maschinenlesbarer Effekt — reuse aus `ability.py` |

Effect-Typen (Vocabulary aus `ability.py`): `buff_roll`, `debuff_roll`, `mortal_wounds`, `heal`, `reanimate`, `free_attack`, `auto_pass_morale`, `reroll`, `move`, `disembark`, `shoot_reaction`, `auto_explode`, `teleport`, `invuln_save`, `restriction`, `mark_target`

### Offene Entscheidungen

| Entscheidung | Status |
|---|---|
| `once_per_battle` enforcement | Datenfeld gesetzt; Enforcement braucht `used_this_battle` in Session-State + neuen Parameter in `stratagem_visibility()` — noch nicht implementiert |
| Variable CP-Kosten | Derzeit Kommentar im YAML (`# variable: 1CP / 2CP`). Ggf. `cp_cost_max`-Feld ergänzen. |
| Reaktive GO UI | `timing: phase_reactive` korrekt in Dataclass; UI behandelt diese GOs noch wie proaktive |

### ⚠️ Daten-Lücken — Truncated Scraper (Session 2026-06-04)

Der Wahapedia-Scraper hat bei allen drei implementierten Fraktionen **substantiell unvollständige Daten** geliefert. Betroffen sind insbesondere:
- Einheiten-Profile (fehlende Stats, fehlende Keywords, unvollständige Waffenprofile)
- Fähigkeiten (Abilities/Rules nicht vollständig — z.B. Dynastiebonus-Mechanik bei Command Protocols komplett fehlend)
- Stratagems bereits manuell nachgearbeitet ✅ — Units/Weapons noch offen

**Vorgehen:** Vor jedem weiteren Feature-Build für eine Fraktion zuerst Daten gegen Wahapedia verifizieren.

### Tasks

- [x] `gameObjects/stratagem.py`: `phase: str | list[str]`, `timing`, `event`, `once_per_battle`, `effect: Effect`
- [x] `gameObjects/loader.py`: neue Felder parsen
- [x] `gameObjects/stratagem.py`: `stratagem_visibility()` list-phase-fähig
- [x] `_shared/stratagems.yaml`: alle 7 GOs vollständig
- [x] `necrons/stratagems.yaml`: 7 bekannte Fehler behoben
- [x] `orks/stratagems.yaml`: wreckaz + careen behoben
- [x] `necrons/stratagems.yaml`: alle 59 GOs vollständig — `effect`, `once_per_battle`, `timing/event` für reaktive GOs; `player` korrigiert bei quantum_deflection + shadows_of_drazak; `rule_text` bei whirling_onslaught nachgetragen
- [x] `orks/stratagems.yaml`: alle 28 GOs vollständig — `effect`, `once_per_battle`, `timing/event`, `player` bei tough_as_squig_hide + orks_is_never_beaten korrigiert
- [x] `necrons/faction_abilities.yaml`: Trigger/Conditions spot-check — alle Trigger korrekt, keine Korrekturen nötig
- [x] `orks/faction_abilities.yaml`: Trigger/Conditions spot-check — alle Trigger korrekt, keine Korrekturen nötig
- [x] `once_per_battle` enforcement in Session-State + `stratagem_visibility()` — ✅ S113: `used_stratagem_battle_ids` battle-scoped; überlebt Phasen-/Spielerwechsel
- [ ] Optional: Tests für korrekte Phase/Stage-Werte

---

## 6i — Auto-Advance: Abgehandelte Einheiten ans Listenende

**Ziel:** Nach dem Abhandeln einer Einheit in einer Phase wandert ihre unitCard ans Ende der Armeeliste. So ist die nächste unbehandelte Einheit immer oben — kein Zurückscrollen nötig. Phase-Reset stellt Standardreihenfolge wieder her.

### Handled-Kriterien pro Phase

| Phase | Kriterium |
|---|---|
| movement | `state["movement_choice"] is not None` |
| shooting | `turn_flags["shot"] == True` |
| psychic | `turn_flags["cast"] == True` |
| charge | `turn_flags["charged"] == True` |
| fight | `turn_flags["fought"] == True` |
| command / morale / setup | keine Sortierung |

### Tasks

- [x] `uiLayout/detachmentCard.py`: `(unit, state_key)`-Paare vor dem Rendern sortieren — unbehandelte zuerst, behandelte zuletzt (stabile Sortierung)

---

## 6j — YAML-Konsolidierung: Doppel-Dateien zusammenführen

**Ziel:** Jede Fraktion hat pro Datentyp genau eine YAML-Datei. Die aktuell parallelen `*_abilities.yaml`-Dateien (redundante Maschinen-Repräsentation) werden in die jeweilige Stammdatei integriert. Alle Listen-Dateien bekommen eine einheitliche Top-Level-Struktur (direkte Liste).

### Hintergrund (Session 22, 2026-06-07)

Vollständiger Audit über alle Fraktionen ergab drei Redundanz-Muster:

1. **Doppel-Datei-Paare**: `weapons.yaml + weapon_abilities.yaml` und `wargear.yaml + wargear_abilities.yaml` — je zwei Dateien für dasselbe Objekt (Stammdaten + Maschinen-Repräsentation)
2. **Header-Inkonsistenz**: Fünf verschiedene Top-Level-Formate für dieselbe Grundstruktur „Liste von Objekten"
3. **Lokalisierung inkonsistent**: Mal `name_en/de`, mal nur `text_de`, mal `rule_text` ohne Übersetzung

`faction_abilities.yaml` vs. `unit_abilities.yaml` sind **kein** Redundanzproblem — verschiedene Konzepte, kein Merge.

### Schritt 1 — `weapon_abilities.yaml` in `weapons.yaml` integrieren

Betrifft: Necrons, Orks (je eine Datei entfällt)

Neue Struktur: Ability als optionales `effect`-Feld im Waffen-Eintrag:
```yaml
- id: wh40k_9e.necrons.weapon.tesla_carbine
  name_en: Tesla Carbine
  profiles: [...]
  effect:          # optional — nur wenn Waffe Sonderregel hat
    type: extra_hits
    trigger_value: 6
    unmodified: true
    hits: 2
```

**Dateien:**
- [x] `data/wh40k_9e/necrons/weapons.yaml` — `effect`-Felder aus `weapon_abilities.yaml` einpflegen ✅ (2026-06-07)
- [x] `data/wh40k_9e/orks/weapons.yaml` — dto. ✅ (2026-06-07)
- [x] `data/wh40k_9e/necrons/weapon_abilities.yaml` — **gelöscht** ✅ (2026-06-07)
- [x] `data/wh40k_9e/orks/weapon_abilities.yaml` — **gelöscht** ✅ (2026-06-07)
- [x] `src/gameObjects/loader.py` — `load_weapon_abilities()` liest aus `weapons.yaml` ✅ (2026-06-07)
- [x] Tests anpassen — 470 Tests grün, keine Änderungen nötig ✅ (2026-06-07)

### Schritt 2 — `wargear_abilities.yaml` in `wargear.yaml` integrieren ✅ (2026-06-07)

Betrifft: Necrons, Orks

Neue Struktur: direkte Liste (kein `schema/faction/entries:` Header), Ability inline:
```yaml
- id: wh40k_9e.necrons.wargear.gloom_prism
  name_en: Gloom Prism
  rule_text: "In your opponent's Psychic phase, the bearer's unit can attempt to deny one psychic power as if it were a PSYKER."
  effect:
    type: deny_psychic
    target: self
  trigger:
    timing: phase_reactive
    phase: psychic
    player: inactive
  source: { publication: Codex Necrons 9e }
```

`deny: true` Flag entfällt — `can_deny()` prüft `effect.type == "deny_psychic"` direkt.

**Dateien:**
- [x] `data/wh40k_9e/necrons/wargear.yaml` — Header entfernen, direkte Liste, Ability-Felder einpflegen ✅
- [x] `data/wh40k_9e/orks/wargear.yaml` — dto. ✅
- [x] `data/wh40k_9e/necrons/wargear_abilities.yaml` — **gelöscht** ✅
- [x] `data/wh40k_9e/orks/wargear_abilities.yaml` — **gelöscht** ✅
- [x] `data/wh40k_9e/necrons/arkana.yaml` — **neu** (Arkana-Block ausgelagert) ✅
- [x] `src/gameObjects/loader.py` — `load_wargear_abilities()` und `load_deny_wargear_names()` auf neue Struktur umgestellt ✅

### Schritt 3 — Header vereinheitlichen (restliche Dateien)

Betrifft: `warlord_traits.yaml`, `relics.yaml` in Necrons + Orks

Aktuell mit `schema:` + `entries:`-Header → direkte Liste wie `weapons.yaml` und `stratagems.yaml`.

**Dateien:**
- [x] `data/wh40k_9e/necrons/warlord_traits.yaml` — `schema/entries:` entfernen → direkte Liste ✅ (2026-06-07)
- [x] `data/wh40k_9e/orks/warlord_traits.yaml` — dto. ✅ (2026-06-07)
- [x] `data/wh40k_9e/necrons/relics.yaml` — `schema/relics:` entfernen → direkte Liste ✅ (2026-06-07)
- [x] `data/wh40k_9e/orks/relics.yaml` — dto. ✅ (2026-06-07)
- [x] `src/gameObjects/loader.py` — kein Loader für diese Dateien vorhanden; Format jetzt konsistent ✅ (2026-06-07)

### Reihenfolge

~~Schritt 2 zuerst~~ ✅ → dann Schritt 1, dann Schritt 3.

---

## 6k — Wargear-Effekt-Interpreter

**Ziel:** Persistente Wargear-Effekte (Stat-Änderungen, Keyword-Grants, Saves, FNP) werden beim Roster-Laden auf die Unit-Instanz angewendet und in der App überall dort sichtbar, wo der Originalwert stünde. Kein `type: complex`-Platzhalter mehr für einfache Effekte.

**Voraussetzung:** 6j Schritt 2 abgeschlossen ✅

### Schema-Erweiterung (`wargear.yaml`)

Neues optionales Feld `persistent_effects:` neben dem bestehenden `effect:`-Feld:

```yaml
- id: wh40k_9e.necrons.wargear.canoptek_cloak
  ...
  persistent_effects:
    - type: set_stat
      stat: move
      value: "10\""
    - type: grant_keyword
      keyword: FLY
  # triggered heal bleibt als effect: {type: heal, ...} (Ziel-Auswahl → complex)
```

**Persistente Effekt-Typen (80%):**

| Typ | Felder | Beispiel |
|---|---|---|
| `set_stat` | `stat`, `value` | Move = 10" (absolut) |
| `buff_stat` | `stat`, `modifier` | Move +2 (relativ) |
| `grant_keyword` | `keyword` | FLY, INFANTRY |
| `set_invuln` | `value` | Invuln = 4+ |
| `buff_save` | `modifier` | Save +1 |
| `set_fnp` | `value` | FNP = 6+ |

**Komplex-Liste (20% — nicht implementiert, hardcoded oder display-only):**

| Wargear | Warum komplex | Status |
|---|---|---|
| `canoptek_cloak` heal D3 | Triggered, Ziel-Auswahl innerhalb 3", ein Modell | display-only |
| `canoptek_control_node` Aura | Echtzeit-Reichweiten-Check auf Nachbareinheiten | display-only |
| `resurrection_orb` | Functionally implemented, aber hardcoded auf OVERLORD keyword statt Wargear-ID | 6h-Migration |
| `phylactery` | Modifiziert Living-Metal-Effekt dynamisch (konditionell) | display-only |
| `fabricator_claw_array` | Triggered, Ziel-Auswahl VEHICLE innerhalb 3" | display-only |
| Ork: `grot_oiler` | Modifiziert Mekaniak-Ergebnis konditionell | display-only |
| Ork: `ammo_runt` | Triggered, once-per-battle | display-only |
| Ork: `bomb_squig`, `ramming_spur`, `squig_bomb` | Komplexe Bedingungen + Ziel-Auswahl | display-only |

### Betroffene Dateien

- [x] `gameObjects/unit.py` — `wargear_ids: list[str]` Feld hinzufügen ✅ (2026-06-07)
- [x] `gameObjects/loader.py`: `load_wargear_catalog()`, `_apply_persistent_effect()`, `_apply_wargear()` erweitert ✅ (2026-06-07)
- [x] `data/wh40k_9e/necrons/wargear.yaml` — `persistent_effects:` für canoptek_cloak, dispersion_shield, shieldvanes, shadowloom ✅ (2026-06-07)
- [x] `data/wh40k_9e/orks/wargear.yaml` — `persistent_effects:` für cybork_body, kustom_job_souped_up_driveshaft, kustom_job_extra_armour_platez ✅ (2026-06-07)
- [x] `uiLayout/unitCard.py` — wargear-granted Keywords in Keyword-Zeile anzeigen ✅ (2026-06-07)
- [x] Tests — 14 neue Tests ✅ (2026-06-07)

### Hinweis: `resurrection_orb` bereits funktional

Die Resurrection-Orb-UI ist funktional und nutzt seit 6k `"resurrection_orb" in unit.wargear_ids` statt OVERLORD-Keyword-Check. ✅ (2026-06-07)

### Tasks

- [x] Schema + YAML-Felder für persistente Effekte (Necrons + Orks) ✅ (2026-06-07)
- [x] `_apply_persistent_effect()` Interpreter in loader.py ✅ (2026-06-07)
- [x] `_apply_wargear()` erweiterung ✅ (2026-06-07)
- [x] unitCard: granted Keywords anzeigen (blau markiert) ✅ (2026-06-07)
- [x] resurrection_orb: Wargear-ID-Check statt OVERLORD-Keyword ✅ (2026-06-07)
- [x] Tests (14 neue Tests) ✅ (2026-06-07)

---

## 6l — Relic-Effekt-Interpreter 🔄

**Ziel:** Relics mit Conditions und Effekten werden maschinenlesbar — analog zu 6k (Wargear).

**Phase 1 ✅ (2026-06-09):** Passive Relic-Effekte + Waffenersatz
- [x] `gameObjects/unit.py`: `Unit.relic_id: str | None = None`
- [x] `gameObjects/loader.py`: `load_relic_catalog(faction_dir)` — lädt `relics.yaml` als ID-Index
- [x] `gameObjects/loader.py`: `_attacks_from_weapon_type()` — extrahiert Attacks-Zahl aus Weapon-Type-String
- [x] `gameObjects/loader.py`: `_relic_weapon_from_entry()` — konvertiert Relic-Profiles in Weapon-Objekt
- [x] `gameObjects/loader.py`: `_apply_relic()` — Waffenersatz (replaces.any_of) + persistent_effects + relic_id
- [x] `gameObjects/loader.py`: `_apply_persistent_effect()` — `buff_stat: toughness/strength` ergänzt
- [x] `gameObjects/loader.py`: `load_roster()` — `relic: <id>` Schlüssel in Roster-Einträgen unterstützt
- [x] `data/wh40k_9e/orks/relics.yaml`: `persistent_effects` für Rezmekka's Redder Paint (+2 Move), Skargrim's Snazztrike (+1T + 5+ Invuln), Tezdrek's Power Field (5+ Invuln)
- [x] `uiLayout/unitCard.py`: Relic-Badge (gold) wenn `unit.relic_id` gesetzt — kurzer Name aus ID-Suffix
- [x] 9 neue Tests → 519 grün

**Phase 2 — Triggered Relic-Effekte (offen):**
- [ ] `data/wh40k_9e/orks/relics.yaml`: Morgog's Finkin' Cap — `trigger/effect: gain_cp_roll` (Command Phase, D6 ≥ 4)
- [ ] `data/wh40k_9e/orks/relics.yaml`: Da Irongob — `trigger/effect: mortal_after_melee` (Fight Phase, nach Attacken, D6 ≥ 2 → D3 Mortals)
- [ ] `data/wh40k_9e/necrons/relics.yaml`: Veil of Darkness — `trigger/effect: teleport` (Movement Phase, 1×/Battle)
- [ ] UI: Button pro triggered Relic in der richtigen Phase (analog Resurrection Orb)

**Schema (Phase 2):**

```yaml
- id: wh40k_9e.orks.relic.morgogs_finkin_cap
  ability_type: triggered
  trigger:
    timing: phase_start
    phase: command
    player: active
  effect:
    type: gain_cp_roll
    dice: D6
    threshold: 4
    amount: 1
```

---

## Ork Waffen-Audit — Befunde (Session 29, 2026-06-08)

> Vollständiger manueller Abgleich aller Ork-Einheiten gegen Wahapedia-Quelldaten.

### Befund 1: Stärke-Werte — korrekt ✅

`_parse_strength()` in `_common.py` verarbeitet alle Notationen korrekt: `User` → `unit_strength`, `+2` → `unit_strength + 2`, `User×2` → `unit_strength * 2`. Kein Handlungsbedarf.

### Befund 2: Boss-Nob-Waffen fälschlicherweise für alle Modelle sichtbar ❌

In multi-Modell-Einheiten sind Waffen, die nur der Boss Nob tragen darf, flach in `weapons[]` gelistet — ohne Einschränkung. Die App erlaubt damit jedem Modell, diese Waffen im Nahkampf zu wählen.

| Einheit | Waffe | Tatsächliche Einschränkung |
|---|---|---|
| `boyz` | big_choppa, killsaw, power_klaw, power_stabba | Boss Nob only |
| `boyz` | big_shoota, rokkit_launcha | 1 pro 10 Modelle |
| `beast_snagga_boyz` | thump_gun | 1 pro 10 Modelle |
| `kommandos` | big_choppa, power_klaw | Boss Nob only |
| `kommandos` | big_shoota, breacha_ram, burna, kustom_shoota, rokkit_launcha, shokka_pistol | 1 pro 10 Modelle |
| `tankbustas` | tankhammer (**Nahkampfwaffe!**), pair_of_rokkit_pistols | 1 pro 5 Modelle |
| `warbikers` | big_choppa, power_klaw | Boss Nob only |
| `stormboyz` | power_klaw | Boss Nob only |
| `nobz`, `meganobz`, `flash_gitz`, `squighog_boyz` | alle | jedes Modell ✅ |

**Geplante Lösung (Option A):** Optionales `model_restriction`-Feld in `weapons[]`-Einträgen der Units:

```yaml
# units.yaml — Beispiel Boyz
weapons:
  - ref: wh40k_9e.orks.weapon.choppa          # alle Modelle (kein Feld = keine Einschränkung)
  - ref: wh40k_9e.orks.weapon.power_klaw
    model_restriction: boss_nob_only
  - ref: wh40k_9e.orks.weapon.big_shoota
    model_restriction: "1_per_10"
```

**Betroffene Dateien:** `data/wh40k_9e/orks/units.yaml`, `gameObjects/unit.py` (WeaponRef-Dataclass), `gameObjects/loader.py` (Parsing), `uiLayout/_common.py` (Deklarations-Filter)

### Befund 3: `extra_attacks`-Waffeneffekt nie ausgewertet ❌ (kritisch)

`_compute_attacks()` (`_common.py:358`) ignoriert den `effect`-Block aus `weapons.yaml` vollständig. Bei `weapon_type: Melee` wird immer `models × unit.attacks` berechnet — ohne Bonus für Waffen mit `extra_attacks`-Effekt.

Zwei Unterklassen:

**3a — „+N additional attacks" ohne Cap** (bearer kämpft mit `unit.attacks + N`):

| Waffe | Effekt | Ist | Soll (Beispiel S:4, 3 attacks) |
|---|---|---|---|
| choppa | +1 additional attack | 3 | 4 |
| beastchoppa | +1 additional attack | 3 | 4 |
| 'urty syringe | +1 additional attack | 3 | 4 |
| grabba stikk | +1 additional attack | 3 | 4 |
| dread klaw | +1 additional attack | 3 | 4 |

**3b — „+N additional attacks, no more than N" (fester Cap)** (immer genau N Attacken, unabhängig von `unit.attacks`):

| Waffe | Cap | Ist (Warboss A:5) | Soll |
|---|---|---|---|
| attack squig | max 2 | 5 | 2 |
| squighog jaws | max 2 | 3 | 2 |
| squigosaur's jaws | max 3 | 5 | 3 |
| smasha squig jaws | max 2 | 4 | 2 |
| grabbin' klaw | max 1 | 6 | 1 |
| wreckin' ball | max 1 | 6 | 1 |
| butcha boyz | max 4 | 6 | 4 |
| savage horns and hooves | max 4 | 6 | 4 |

**Geplante Lösung:** `effect`-Block in `weapons.yaml` um `max_attacks`-Feld erweitern; `_compute_attacks()` und `_total_attacks_int()` auslesen:

```yaml
# weapons.yaml — attack_squig (Klasse 3b)
effect:
  type: extra_attacks
  amount: 2
  max_attacks: 2   # neu — "no more than N" Cap

# choppa (Klasse 3a)
effect:
  type: extra_attacks
  amount: 1
  # kein max_attacks → unit.attacks + 1
```

**Betroffene Dateien:** `data/wh40k_9e/orks/weapons.yaml` (max_attacks-Felder ergänzen), `gameObjects/weapon.py` (WeaponProfile-Dataclass), `gameObjects/loader.py`, `uiLayout/_common.py` (`_compute_attacks`, `_total_attacks_int`)

### Befund 4: Optional-Wargear-Attachments nicht in YAML ⚠️ (display-only)

Folgende Attachment-Wargear-Einträge fehlen vollständig in `wargear_options` aller Ork-Einheiten. Sie sind als `display-only` in der 6k-Komplex-Liste bereits dokumentiert (kein neuer Handlungsbedarf):

| Wargear | Trägereinheit(en) | Effekt |
|---|---|---|
| grot oiler | Big Mek-Varianten | +D3 bei Mekaniak-Reparatur |
| ammo runt | Nobz (1/5), Flash Gitz, Kaptin Badrukk | Re-roll 1 Treffer/Runde |
| grot orderly | Painboy, Painboss | Verbessert Sawbonez |
| gitfinda squig | Flash Gitz Kaptin | +1 Hit mit Snazzgun |
| squig hound / grot-lash | Runtherd | Gretchin-Moral-Modifikator |
| bomb squig | Kommandos (1/10), Squighog Boyz (1/3), Tankbustas (2/5) | Mortal Wounds bei Charge |
| distraction grot | Kommandos (1/10) | −1 Hit auf Feind |

### Priorisierung der Fixes

| Priorität | Fix | Aufwand | Kritikalität |
|---|---|---|---|
| **1** | extra_attacks Klasse 3b (Cap-Waffen: feste Attackenzahl) | klein | hoch — falsche Attackanzahl |
| **2** | extra_attacks Klasse 3a (Choppa etc.: +N) | mittel | hoch — betrifft fast alle Ork-Nahkämpfer |
| **3** | model_restriction in YAML + Filter in UI | groß | mittel — regelwidrig, aber Spieler bemerkt es |
| **4** | Optional-Wargear-Attachments | sehr groß | niedrig — display-only akzeptiert |

### Tasks

- [x] `data/wh40k_9e/orks/weapons.yaml`: `max_attacks`-Feld für alle Klasse-3b-Waffen ergänzen ✅ (2026-06-08)
- [x] `gameObjects/weapon.py`: `WeaponProfile.max_attacks: int | None = None` ✅ (2026-06-08)
- [x] `gameObjects/loader.py`: `max_attacks` aus YAML parsen ✅ (2026-06-08)
- [x] `uiLayout/_common.py`: `_compute_attacks()` + `_total_attacks_int()` — Klasse 3b (max_attacks) + Klasse 3a (+N) auswerten ✅ (2026-06-08)
- [x] `data/wh40k_9e/orks/units.yaml`: `model_restriction`-Felder für alle Boss-Nob-Waffen ✅ (2026-06-08)
- [x] `gameObjects/unit.py`: `Unit.weapon_restrictions: dict[str, str]` — Badge-Lookup ✅ (2026-06-08)
- [x] `gameObjects/loader.py`: `model_restriction` aus YAML parsen ✅ (2026-06-08)
- [x] `uiLayout/_common.py`: `render_attack_declaration()` — Boss-Nob-Badge in Melee+Shooting ✅ (2026-06-08)
- [x] Tests für neue extra_attacks-Logik (25 Tests) ✅ (2026-06-08)
- [x] `data/wh40k_9e/orks/units.yaml`: `model_restriction: "1_per_10"` für Boyz (big_shoota, rokkit_launcha) + Kommandos (6 Waffen) ✅ (2026-06-09)
- [x] Tests für 1_per_10-Restrictions (2 Tests → 535 grün) ✅ (2026-06-09)
- [x] Bugfix Cover-Würfelpaare: Dense Cover grau=from_thresh−1/rot=from_thresh; Light/Heavy Cover beide Würfel=from_thresh−1; Effective Save zeigt Rüstungsweg ✅ (2026-06-09)
- Note: grot_prod hat laut Wahapedia kein extra_attacks (Ability-Text: `-`) — war in Session-29-Notizen falsch

---

## 6m — Modellgruppen-Datenmodell + neue Deklarations-UI

**Ziel:** Einheitenkonfiguration regelkonform in YAML abbilden. Deklarations-UI folgt dem regeltreuen Ablauf: Gruppe → Ziel → Attacken → Waffe.

**Status:** 🟢 Implementiert (2026-06-10, Session 38+39) — Review-Befunde in §6n

---

### Hintergrund

Die bisherigen `model_restriction`-Flags sind ein Workaround. Einheiten wie Boyz (9 Boys + 1 Boss Nob) haben strukturell verschiedene Modellgruppen mit unterschiedlichen Waffenoptionen — das ist im YAML nicht sauber abgebildet. Folge: Die UI zeigt alle Waffen allen Modellen, was regelwidrig ist.

**Drei Gruppen-Typen (decken alle 40k-Fälle ab):**

| Typ | Beispiel | Schema |
|---|---|---|
| **Homogen** | Gretchin, Warriors (default) | kein `model_groups` nötig |
| **Strukturell gemischt** | Boyz (9 Boys + 1 Boss Nob), Kommandos | `model_groups` mit `count: remainder` + `count: 1` |
| **Individuell gewählt** | Nobz, Killa Kans, Lychguard gemischt | `model_groups` mit `optional_mode: per_model` |

Character-Units (1 Modell vollständig individuell) brauchen kein `model_groups`.

---

### YAML Schema (units.yaml — neue Felder)

#### Strukturell gemischt (z.B. Boyz):

```yaml
model_groups:
  - id: ork_boy
    name_en: Ork Boy
    count: remainder        # = models_alive minus alle fixed-count Gruppen
    weapons:
      - ref: wh40k_9e.orks.weapon.slugga
      - ref: wh40k_9e.orks.weapon.choppa
      - ref: wh40k_9e.orks.weapon.stikkbombz
    optional_per_10:        # 1 Modell pro 10 wählt genau eine (im Roster aufgelöst)
      - wh40k_9e.orks.weapon.big_shoota
      - wh40k_9e.orks.weapon.rokkit_launcha
    priority: 1             # stirbt zuerst (1 = erster Verlust)
  - id: boss_nob
    name_en: Boss Nob
    count: 1                # immer genau 1
    weapons:
      - ref: wh40k_9e.orks.weapon.slugga
      - ref: wh40k_9e.orks.weapon.stikkbombz
    optional_one_of:        # die ganze Gruppe wählt genau eine (im Roster aufgelöst)
      - wh40k_9e.orks.weapon.choppa
      - wh40k_9e.orks.weapon.big_choppa
      - wh40k_9e.orks.weapon.power_klaw
      - wh40k_9e.orks.weapon.killsaw
    priority: 2             # stirbt zuletzt
```

#### Per-Model (z.B. Nobz, Killa Kans):

```yaml
model_groups:
  - id: nob
    name_en: Nob
    count: models_max       # alle Modelle in dieser Gruppe (zählt gegen models_alive)
    weapons:
      - ref: wh40k_9e.orks.weapon.slugga
      - ref: wh40k_9e.orks.weapon.stikkbombz
    optional_one_of:
      - wh40k_9e.orks.weapon.choppa
      - wh40k_9e.orks.weapon.big_choppa
      - wh40k_9e.orks.weapon.power_klaw
      - wh40k_9e.orks.weapon.killsaw
    optional_mode: per_model  # jedes Modell wählt individuell → Loader splittet in Sub-Gruppen
    priority: 1
```

**`count`-Werte:**
- `1`, `2`, … : feste Anzahl
- `remainder`: `models_alive` minus alle anderen `count`-Gruppen
- `models_max`: alle Modelle (für per_model-Gruppen ohne feste Sondermodelle)

---

### Roster Schema (Erweiterung)

```yaml
# Strukturell gemischt (Boss Nob + 1_per_10):
group_loadouts:
  boss_nob:
    optional_weapon: wh40k_9e.orks.weapon.power_klaw
  ork_boy:
    optional_per_10_weapon: wh40k_9e.orks.weapon.big_shoota  # null = kein Sonderträger

# Per-Model (Nobz):
group_loadouts:
  nob:
    per_model_weapon_counts:
      wh40k_9e.orks.weapon.power_klaw: 2
      wh40k_9e.orks.weapon.big_choppa: 2
      wh40k_9e.orks.weapon.choppa: 1
      # Summe muss models-Anzahl ergeben
```

Der Loader löst `per_model_weapon_counts` in effektive Sub-Gruppen auf:
- `nob_power_klaw` (count=2, weapons=[slugga, power_klaw, stikkbombz])
- `nob_big_choppa` (count=2, …)
- `nob_choppa` (count=1, …)

Dadurch arbeitet die gesamte Laufzeit-Logik immer mit **einfachen Gruppen mit fixen Waffen** — keine Sonderfälle in UI oder Combat.

---

### Betroffene Einheiten

**Orks (model_groups nötig):**

| Einheit | Typ | Gruppen |
|---|---|---|
| boyz | strukturell gemischt | ork_boy (remainder, optional_per_10) + boss_nob (1, optional_one_of) |
| beast_snagga_boyz | strukturell gemischt | beast_snagga (remainder) + boss_nob (1) — Wahapedia prüfen |
| kommandos | strukturell gemischt | kommando (remainder, optional_per_10) + boss_nob (1) |
| stormboyz | strukturell gemischt | stormboy (remainder) + boss_nob (1) |
| warbikers | strukturell gemischt | warbiker (remainder) + boss_nob (1) |
| nobz | per_model | nob (alle, optional_one_of) |
| tankbustas | strukturell gemischt | tankbusta (remainder) + nob_with_tankhammer (1_per_5) — Wahapedia prüfen |
| meganobz | per_model | meganob (alle) — Wahapedia prüfen |
| squighog_boyz | per_model | squighog_boy (alle) — Wahapedia prüfen |

**Orks (homogen, kein model_groups):** flash_gitz, burna_boyz, gretchin, deffkoptas, alle Fahrzeuge/Monster-Einzelmodelle

**Necrons:** Lychguard kann gemischt sein — durch bestehendes `weapon_loadout`-Schema im Roster bereits abbildbar; kein `model_groups` nötig bis UI-Redesign fertig. Warriors homogen by default.

**Custodes:** kein Handlungsbedarf (alle relevanten Einheiten homogen oder Einzelmodelle).

---

### Datenmodell (gameObjects/unit.py)

```python
@dataclass
class ModelGroup:
    id: str
    name_en: str
    count: int          # aufgelöste Anzahl (nach Roster-Auflösung)
    weapons: list[WeaponRef]   # finale Waffen inkl. gewählte Optionals
    priority: int       # Todesreihenfolge (1 = stirbt zuerst)
```

- `Unit.model_groups: list[ModelGroup]` — leer wenn Einheit homogen
- `Unit.weapons` bleibt als flattened Union aller Gruppen-Waffen (Rückwärtskompatibilität)
- Rückwärts: Einheiten ohne `model_groups` in YAML → `unit.model_groups = []`, altes Verhalten aktiv

---

### State-Erweiterung (game_state.py)

```python
unit_state["group_models"]: dict[str, int]
# Init: {group.id: group.count for group in unit.model_groups}
# unit_state["models"] = sum(group_models.values())  — abgeleitet, bleibt kompatibel
```

`apply_damage()`: reduziert nach `priority` (niedrigste zuerst = Standardmodelle sterben vor Sondermodellen). Default-Sortierung spiegelt Spieler-Praxis wider; Spieler kann bei Bedarf manuell abweichen (spätere Erweiterung).

---

### UI-Flow (neue Deklaration)

**Fernkampf:**
- firstPlayerArea: subUnitCard pro Gruppe (Name + lebend-count + Waffensummary + Select-Button)
- Gruppe wählen → zeigt Waffen + Ziel-Zuweisung; count=1 → max 1 Ziel
- secondPlayerArea: Übersicht zugewiesener Attacken / verbleibende Modelle
- Fertige Gruppe: kollabiert zur Zusammenfassung (nicht verschwinden)

**Nahkampf:**
1. Gruppe wählen (firstPlayerArea subUnitCard)
2. Ziel(e) wählen; count=1 → max 1 Ziel
3. Attacken auf Ziele aufteilen
4. Waffe deklarieren pro Ziel
5. Fertige Gruppe: kollabiert zur Zusammenfassung

**Rückwärtskompatibilität:** Einheiten ohne `model_groups` behalten bisherigen Flow.

---

### Tasks (Implementierungsreihenfolge)

- [x] **A — YAML-Datenpflege:** `model_groups` in `orks/units.yaml` für alle betroffenen Einheiten; `model_restriction`-Flags entfernen (werden durch Gruppen ersetzt)
- [x] **B — Roster-Schema:** `group_loadouts` in bestehende `data/rosters/*.yaml` ergänzen (loader_contract.md → Task J)
- [x] **C — `gameObjects/unit.py`:** `ModelGroup` dataclass; `Unit.model_groups: list[ModelGroup]`
- [x] **D — `gameObjects/loader.py`:** `model_groups` parsen, count auflösen, `optional_one_of`/`optional_per_10`/`optional_per_5` gegen Roster auflösen, `per_model`→Sub-Gruppen splitten
- [x] **E — `game_state.py`:** `group_models` initialisieren; `apply_damage()` nach priority; `models` als Summe ableiten
- [x] **F — subUnitCards:** in den PlayerAreas der gameActionsArea (`render_group_cards` in `_common.py`), NICHT in der Armeeliste (Nutzer-Entscheidung Session 39); Gruppe-für-Gruppe-Flow mit `selected_model_group`/`group_targets`/`group_decl`
- [x] **G — `src/uiLayout/_common.py`:** neue Deklaration Schussphase (Gruppe → Waffe → Ziel)
- [x] **H — `src/uiLayout/_common.py`:** neue Deklaration Nahkampf (Gruppe → Ziel → Attacken → Waffe)
- [x] **I — Tests:** ModelGroup-Laden, count-Auflösung, apply_damage nach priority, Rückwärtskompatibilität
- [x] **J — `docs/spec/loader_contract.md` + `unit_states.md`:** aktualisiert (group_loadouts + group_models + Gruppen-Flow)

**Abhängigkeit:** A+B → C → D → E → F → G/H (parallel) → I → J

---

## 6n — Review-Befunde Session 39 (13 Punkte, freigegeben 2026-06-10)

**Ziel:** Regelbugs aus dem 6m-Umbau beheben + UX der Deklaration/Resolution überarbeiten.
**Reihenfolge: Block A → B → C → D → E** (Nutzer-Freigabe Session 39).

### Regelgrundlage (core_rules.txt Z. 1941–1974)

> "Starting with the player whose turn is not taking place, the players must alternate
> selecting an eligible unit … An eligible unit is one that is **within Engagement Range**
> of an enemy unit and/or made a charge move … Units that did not make a charge move this
> turn **cannot be selected to fight until after all units that did make a charge move have
> fought**. If all of one player's eligible units have fought, the opposing player can then
> fight with their remaining eligible units, one at a time."

### Block A — Regelbugs Fight Phase (HOCH)

- [x] **A1 (P10):** ✅ (2026-06-10) Gruppen-Flow-Zielauswahl in der Fight Phase auf engaged Ziele (`melee_with`) beschränken — `toggle_group_target` umgeht aktuell den `_is_target_engaged`-Check der Legacy-Deklaration. ▷ für nicht-engaged Ziele wirkungslos. (`_common.py`, `unitCard.py`, Tests)
- [x] **A2 (P9):** ✅ Root Cause: fought-Flag wird beim ERSTEN Apply gesetzt → Wechsel lief mitten in der Resolution; Fix: kein Advance solange attack_declaration aktiv. Kampfreihenfolge gegen RAW verifizieren/reparieren: charged zuerst (alternierend, Start inaktiver Spieler), danach Alternation; Session-39-Rerun-Änderung kritisch prüfen. Testmatrix für alle Übergänge. (`fightPhase.py`, Tests)
- [x] **A3 (P11):** ✅ Root Cause bestätigt: res_*-Keys überlebten; Fix: seq-Namespacing pro Deklaration. Resolution-Tabs starten fälschlich „✓ 0 models · 0 MW · 0 damage" — vermutlich persistierende Widget-Keys aus früherer Deklaration; Keys pro Deklaration namespacen oder beim Start zurücksetzen. (`_common.py`)
- [x] **A4 (P8):** ✅ render_player_column(show_wound_buttons=False) in der Charge Phase. Wound-Buttons (−3…+3) aus der Charge-Phase-Zielspalte entfernen — kommen aus `render_player_column` (hängt nach `inactive_content` immer `wound_adjustment_buttons` an). Nur zeigen, wenn datengetriebener Charge-Trigger existiert. (`chargephase.py` / `_common.py`)

### Block B — UX Gruppen-Zuweisung (HOCH)

- [x] **B1 (P1):** ✅ Waffen-Zeilen mit Modell-Counter pro Waffe; Grenade-Cap 1. Waffen-Multiselect ersetzen durch feste Waffen-Zeilen mit Modell-Counter pro Waffe (kein Dropdown → kein „No results"). Grenade-Regel: max. 1 Modell pro Einheit wirft Stikkbombz pro Phase. (`_common.py`)
- [x] **B2 (P4):** ✅ dynamische max_value = Restbudget; Budget-Übersicht oben. Überbuchung unmöglich machen: Counter-`max_value` dynamisch = Restbudget; Budget/Rest prominent OBEN im Zuweisungspanel statt Fehlermeldung unten. (`_common.py`)

### Block C — Daten/YAML (MITTEL)

- [x] **C1 (P2):** ✅ _group_weapon_ref_union() im Loader; weapons: bei allen 8 Gruppen-Einheiten entfernt. `weapons:` bei Einheiten mit `model_groups` aus `units.yaml` entfernen; Loader bildet Union aus Gruppen-Waffen. (`loader.py`, `orks/units.yaml`, `loader_contract.md`, Tests)
- [x] **C2 (P1b):** ✅ GENERISCHES weapon_swaps-Schema ersetzt optional_one_of/per_10/per_5 komplett (scope group|per_model, pick N, limit any|per_10|per_5, replaces als echte Ersetzung). Alle 8 Einheiten migriert; Test-Roster: Shoota-Mix 3, Big-Shoota-Träger 1, Boss Nob PK+BC, Nobz 2×(PK+BC)+2×(2 Killsaws). Spec: loader_contract.md. Schema sauber erweitern (Nutzer-Entscheidung: generisch, kein Pragmatismus):
  - Shoota-Mix für Ork Boys: „Any Ork Boy's slugga and choppa can be replaced with 1 shoota" → per-model
  - `optional_two_of` für Boss Nob: slugga+choppa → ZWEI aus [big choppa, choppa, killsaw, power klaw, power stabba, slugga]
  - Orks-Test-Roster deckt ab: Slugga/Shoota-Mix, Big-Shoota-Träger, Boss Nob mit 2 Waffen

### Block D — displayArea-Anzeige (MITTEL)

- [x] **D1 (P13):** ✅ Regelkasten zentral oben in gameActionsArea (alle 7 Phasen); VP unten; Inline-Duplikate entfernt. Blauer Phasen-Regelkasten in JEDER Phase ganz oben (fehlt in Fight + Morale); VP-Scoring ans ENDE der displayArea. (`gameActionsArea.py`, `fightPhase.py`, `moralePhase.py`)
- [x] **D2 (P6):** ✅ halbe Breite, Damage/HP-Werte hervorgehoben. Damage-Panel halbe Breite; „Damage/HP"-Info deutlich lesbar. (`_common.py`)
- [x] **D3 (P12):** ✅ RP-Block halbe Breite. RP-Panel kompakter. (`commandPhase.py` o.ä.)
- [x] **D4 (P7):** ✅ CSS: Trennlinien zwischen stTab-Buttons, schlankeres Padding. Resolution-Tabs trennen/verschlanken (CSS). (`_common.py` / CSS)
- [x] **D5 (P5):** ✅ (2026-06-10) Spaltenraster (Schwellen bündig über Würfeln, 15px hell), Badge-Spalte 96px in allen Zeilen, Trennlücke+Linie an Erfolgsgrenze (würfelbreit), S/T hervorgehoben ohne „→N+", Sv neben SAVE, Eff.-Reihen als Würfelzeilen, Profilzeile verschlankt (nur Attackenzahl), P16-Randfall (×-Marker >6+). Ursprünglich: Würfel-Sequenz: Trennlinien + Luft zwischen HIT/WOUND/SAVE; Würfel spaltenbündig; Schwellenzahlen (2+, 3+ …) in Würfelgröße + voller Helligkeit; Sv-Wert neben SAVE konsistent zu WS/BS (Profilzeile oben entfällt); S-vs-T-Vergleich deutlich markiert. **ERST HTML-Mockup/Schema dem Nutzer vorlegen, dann implementieren.**

### Bugfixes nach Review-Runde 2 (Nutzer-Meldungen 2026-06-10, gefixt)

- [x] **Boss-Nob-Budget unter WAAAGH (4 statt 3):** Gruppen-Melee-Budget basierte nur auf der ERSTEN Waffe — `_group_melee_budget()` = models × eff_attacks + Σ extra_attacks-Boni der getragenen Waffen (Choppa +1; max_attacks-Waffen addieren ihren Cap). 3 Tests.
- [x] **Reanimierte Modelle zählten weiter als Moral-Verluste:** `heal_unit()` reduziert jetzt generisch `lost_models_this_turn` um zurückgekehrte Modelle (JEDE Revive-Mechanik, kein Fraktions-Check) und füllt `group_models` in Priority-Reihenfolge wieder auf (`_restore_group_models`). 3 Tests.
- [x] **„WAAAGH wirkt nicht auf die Modelle":** Wirkung in Zahlen war korrekt (28 Boyz-Attacken = 7×(2+1)+7); die per-Unit-Badge wurde per Farbkonzept-Beschluss bewusst entfernt (Army-Ability nur in armyCard). Der Boss-Nob-Budget-Bug (oben) war der reale Zahlenfehler.

### Block E — Farbkonzept (P3)

- [x] **E1:** ✅ WAAAGH!-Badge aus unitCard entfernt; armyCard zeigt EINE Buff-grüne Army-Ability-Badge (Label aus YAML name_en); waaagh_1/waaagh_2-Farbschlüssel (Fraktionslogik!) entfernt. Ursprünglich: `"WAAAGH!"` aus `_BADGE_COLORS` in `unitCard.py` entfernen (Fraktionslogik in src/ = Bug). Badge-Label aus Army-Ability-YAML; EINE generische Army-Ability-Farbe.
- [x] **E2:** ✅ Entwurf liegt vor — `docs/spec/design_colors.md`; Entscheidungen siehe Review-Runde 2 unten.

### Review-Runde 2 (Session 39, nach Block A–D — GESAMMELT, noch nicht freigegeben)

- [x] **P14:** ✅ (2026-06-10) show_wound_buttons=False in Schussphase; ▷-Sperre via _in_friendly_melee in group_target_selectable (gilt auch für Legacy-Einheiten; nur Schussphase, nicht Fight). Schussphase: eigene Einheiten in-melee sind wählbar → Ziel-Spalte zeigt dann wieder Wound-Buttons; auch beim beschossenen Ziel nach Resolution. Wound-Buttons dort raus. Außerdem: feindliche Einheiten in-melee mit Freunden dürfen NICHT als Ziel wählbar sein (▷ sperren, nicht nur Warnung).
- [x] **P15:** ✅ (2026-06-10) Skorpekh (per_3-Swap, NEU im Schema), Ophydian (per_3), Lokhust Heavy (Exterminator-Swap per_model), Lychguard (group-Swap Schwert, Schild=Wargear — all-or-nothing per RAW), Lokhust Destroyers (falsche Exterminator-Option entfernt). Plasmacyte/Cryptothralls: keine Waffenoptionen → nichts nötig; Plasmacyte-Begleitmodell + „bis zu 2 Heavy in Lokhust-Einheit" (andere Statline!) NICHT abbildbar — Limitation. Necron-Modellgruppen — ALLE Sonderfälle (Wahapedia/offizielle Datasheets prüfen, ⚠ Wargear-Zeilen fehlen teils in `docs/work/wahapedia_necrons/units_all.txt` — Scraper-Lücke!):
  - **Skorpekh Destroyers:** 1 pro 3 Modelle: Threshers → Reap-Blade → neues `limit: per_3` im weapon_swaps-Schema
  - **Ophydian Destroyers:** Besonderheiten der Zerstörer-Einheit prüfen (Waffenwahl)
  - **Lokhust Destroyers / Lokhust Heavy Destroyers:** Besonderheiten prüfen; Heavy: gauss destructor → enmitic exterminator; gemischte Einheit (Lokhust + Heavy in einer Einheit)?
  - **Plasmacyte:** Begleitmodell für Skorpekh/Ophydian — wie abbilden (eigene Gruppe? Sondermodell)?
  - **Cryptothralls:** mögliche Sonderrolle (Bodyguard-Mechanik für Crypteks) prüfen
  - **Lychguard:** Schwert+Schild vs. Warscythe → model_groups statt weapon_loadout?
  - Sonst laut Nutzer keine Necron-Besonderheiten.
- [x] **P16:** ✅ (verifiziert 2026-06-12) Bereits im Zuge von D5 implementiert: `dice_html.py:98-106` (Threshold > 6 → 6 Miss-Würfel + rotes ×) und `dice_html.py:193-213` (Save-Modifier-Reihe: × statt geklemmtem Würfel, Tooltip „exceeds 6 — save impossible"). Ursprünglich: Save-Anzeige Randfall: Sv 6+ mit AP-4 → effektiv unmöglich (10+). Anker „von 6 ausgehend" + Ausnahmeregel für Schwellen > 6+ definieren (vs. Normalfall AP-1 auf 3+).
- [ ] **P17 (nachgeschärft 2026-06-10):** Zielauswahl bleibt auf Einheiten-Ebene (Untergruppen des Verteidigers für den Angreifer unsichtbar — regelkonform). ABER: **Verteidiger bekommt Korrekturmöglichkeit bei der Schadenszuweisung** — nach „Apply Damage" gegen eine Gruppen-Einheit: ±-Counter pro Gruppe (Summe = Verluste), Default bleibt `priority`-Reihenfolge. Kritischer Fall: Nobz mit gemischter Bewaffnung — welcher Nob fällt, ändert die verfügbaren Waffen der Folgerunden („bricht die Logik"). **Danach muss klar erkennbar sein, welche Waffen nicht mehr zur Verfügung stehen** (Gruppe auf 0 → Waffen weg; subUnitCard/Deklaration zeigen nur lebende Gruppen). Folgefrage bei Umsetzung: Tracking, in welcher Gruppe das verwundete Frontmodell steht (Mehrwunden-Einheiten).
- [ ] **P18:** UX Nahkampf: neben den Untergruppen in der gegnerischen PlayerArea die infrage kommenden Ziele anzeigen (App kennt `melee_with`). Einheiten OHNE Untergruppen genauso behandeln (= eine einzige Gruppe) → EIN einheitlicher Deklarations-Flow für alle Einheiten.
- [x] **P19:** ✅ Root Cause: Cover-Checkboxen waren pro TAB gekeyt statt pro ZIEL — im zweiten Waffen-Tab desselben Ziels war die Checkbox separat/nicht gesetzt. Fix: cover_key pro Ziel; Checkbox nur im ersten Tab des Ziels (DuplicateWidgetID). Regel bestätigt: Heavy Cover entfällt NUR wenn der Verteidiger selbst gecharged hat (in-melee allein blockt nicht). Ursprünglich: Warum erscheint Heavy Cover beim Power-Klaw-Tab nicht? (Prüfen: Heavy-Cover-Checkbox-Bedingung pro Tab — Defender-charged-Regel oder Bug?)
- [x] **P20:** ✅ Logik-Ebene verifiziert KORREKT (Regressionstest test_advanced_unit_in_melee_is_eligible_and_receives_turn): ADVANCED+IN MELEE ist kampfberechtigt, Wechsel funktioniert. Der beobachtete Block muss im UI-Pfad liegen — Verdacht: pending_irongob-Dialog des Big Mek (rendert Fight Phase exklusiv) oder unfertige charged-Einheit. Falls erneut beobachtet: genaue Repro-Schritte notieren! Ursprung: Heroic Intervention: Scarabs intervenieren → IN MELEE korrekt, aber ADVANCED-Badge bleibt; Einheit darf danach wohl nicht kämpfen und **blockiert den Kämpfer-Wechsel** in der Fight Phase. HI muss den Bewegungszustand regelkonform behandeln + Regressionstest.

**D5 — verbindliche Detail-Spezifikation (Nutzer, anhand Referenz-Screenshot, 2026-06-10):**
1. Schwellenzahlen (2+, 3+ …) stehen **bündig über dem Würfel der jeweiligen Augenzahl**.
2. KEIN „→ 3+" hinter dem S/T-Vergleich — das Ergebnis steht farblich hervorgehoben in der Schwellenreihe darunter.
3. **Trennlinie an der Erfolgsgrenze** (zwischen letztem Fail- und erstem Erfolgs-Würfel); der Zwischenraum so breit wie ein Würfel-Icon („Luft").
4. Sv-Wert neben SAVE (wie WS/BS bei HIT).
5. **Erste Spalte = Badge-Spalte** (Platz vor jeder Würfelreihe): AP-X, Heavy Cover, MWBD, Eff. … Hinter der Badge die Modifier-Notation zwischen Würfeln: Buff `2→3`, Debuff `3←4`, Buff-Reroll = Reroll-Symbol, Debuff-Miss = „✗" (z.B. Quantenschilde).
6. Randfall P16 (Schwellen > 6+) in der Darstellung abfangen.

**Farbkonzept — Entscheidungen (Nutzer, 2026-06-10):**
- **Buff = GRÜN `#4a9a5a`** (das bisherige MOVED-Grün); **MOVED = BLAU `#60a5fa`** (das bisherige MWBD-Blau) — FESTGELEGT.
- **Cover ist ein Buff** → Cover-Würfel/-Badges im SAVE-Block in Buff-Grün (vormals blau).
- SHOT (cyan) und CHARGED/FOUGHT (violett) bleiben unverändert (bestätigt).
- **Army-Ability (4a) = Buff-Grün** — WAAAGH!, aktive Command Protocols etc. SIND Buffs; eine konsistente, schlanke Kategorie. Badge erscheint in der armyCard (z.B. „WAAAGH!" grün).
- **RESERVE** = Farbe von **HEROIC INT.** (`#ff9060`, warmes Lachs-Orange) — beides temporäre Sonderzustände.
- **Relic-Badge ENTFÄLLT** — nur wenn das Relic einen Effekt bringt, erscheint die Buff-/Debuff-Badge des Effekts.
- **Wargear-Keyword-Blau entfällt analog** — Wargear/Weapon-Abilities zeigen sich als Buff/Debuff.
- **4c Fraktionsfarben: NEIN** — einheitliches Theme.
- 4b (Würfel-Farben) = durch D5-Spezifikation + Referenz-Screenshot definiert; offener Punkt: Buff-Würfel im SAVE-Block war blau → nach neuem Konzept grün? Bei Umsetzung vorlegen.

---

## Akzeptanzkriterien (Ziel 6 komplett)

- [ ] Header: VP/CP inline, alle Steuerelemente auf einer Zeile, Badges doppelt so groß
- [ ] armyCard: Korrekte Fähigkeiten für jede Fraktion, kein Necron-Fallback-Bug
- [ ] WAAAGH aktivierbar, Command Protocol wechselbar — beide über armyCard
- [ ] **Ka'tah (Custodes) + Canticles (AdMech) funktionieren ohne Code-Änderung** (nur YAML)
- [ ] **Auto-Progression-Badge zeigt korrekte Doctrine für Space Marines**
- [ ] Stratagems sind Default-Tab in gameProtocoll
- [ ] Attackensequenz: simultan, Modifier transparent, kein Zwischenwert-Klicken
- [ ] CP-Doppelvergabe unmöglich
- [ ] Ability-Badges auf unitCard sichtbar und korrekt ablaufend
- [ ] Reset archiviert Log; neues Spiel startet sauber
- [ ] Archiv-UI im Setup-Screen: Liste, Download, Löschen

---

## Session-Historie (Changelog)

> Aus `next_session.md` übertragen (2026-06-13), damit der Startprompt schlank bleibt.
> Eine Zeile pro Session — Details stehen in den Teilziel-Abschnitten oben und im Git-Log.

### Feature-Sessions (Ziel 6)

- **S28** WAAAGH! Advance+Charge, +1 Attacks Melee, per-weapon `atk_counter`.
- **S29** Ork-Waffen-Audit — Befunde 1/2/3 (s. „Ork Waffen-Audit").
- **S30** `extra_attacks` + `model_restriction`: `WeaponProfile.max_attacks`, Klasse 3a/3b, Boss-Nob-Badges; +25 Tests.
- **S31** Weapon-Strength-Bugfix: `_parse_strength` akzeptiert `int|str` nativ; `WeaponProfile.ap:int`; 510 Tests.
- **S32** 6l Relic-Interpreter Phase 1 (`Unit.relic_id`, `load_relic_catalog`, `_apply_relic`, `buff_stat`, Relic-Badge); Heavy-Cover-Charged-Check `atk_state`→`def_state`; 519 Tests.
- **S33** `_parse_strength` `User×N`-Notation (power_klaw etc.); +14 Regressionstests; 533 Tests.
- **S34** `1_per_10`-Restrictions (Boyz/Kommandos); Cover-Würfelpaar-Bugfix in `_common.py`; 535 Tests.
- **S35** 6l Phase 2 datengetrieben: `TriggeredEffect`, alle hardcodierten Fraktions-IDs raus, Veil of Darkness (`movement_locked`), Da Irongob 2-stufig; 547 Tests.
- **S36** Da-Irongob-Zielfilter, Dakka-`"5/3"`-Parsing, Boss-Nob-Limit pro Ziel, Save-Modifier-AP-Farben; Cover-Farben offen.
- **S37** Save-Modifier relativ zu `armour` (`save_modifier_die_pair_html`); Shooting-`model_restriction` im Schusspfad; 6m geplant.
- **S38** 6m Modellgruppen implementiert (Tasks A–E,G/H,I): `model_groups` YAML, `ModelGroup(Spec)`, `_resolve_model_groups`, `group_models`-State, `_apply_group_losses`, `_render_group_declaration`; +13 Tests, 559.
- **S39** 6m F+J final (subUnitCards in PlayerAreas, Gruppe-für-Gruppe-Flow), Doppelklick-Fix Fight Phase, `reset_group_declaration_state`; 6n A–D+E2 (Engagement-Check, `seq`-Namespacing, `weapon_swaps`-Schema ersetzt `optional_*`, Regelkasten oben/VP unten); 583 Tests. 13 Review-Befunde → 6n.
- **Coverage-Session (2026-06-11)** 80%-Gate aktiv (`pyproject.toml` omit + `fail_under=80`), `deploy.yml` Dev-Deps; +166 Tests, 760 grün/90%. Audit-Bericht + Pläne 001–005.

### Audit-/Executor-Sessions

- **2026-06-11 (Pläne 001–005 + Findings #8/#9/#10)** CI-Gates (ruff/black/isort/mypy/Coverage), `defusedxml`, `waaagh_attack_bonus()` zentralisiert, `lookup()` KeyError, Loader-Cache; `.woodpecker.yml`/`Makefile`/`.env.example` bereinigt; 767 Tests.
- **2026-06-11 (Pläne 009/010/006/007)** Roster-Group-Validation, 5 tote Vars + F841-Gate, `load_yaml`-Helper, Scenario-Namen-Allowlist; +9 Tests, 776.
- **2026-06-11 (Re-Audit)** Bericht `docs/audit/2026-06-11-reaudit.md` (R1–R8) + Pläne 006–012; Token-in-URL widerrufen.
- **S40 (2026-06-12, Plan 008)** `gameMechanic/attack_math.py` (NEU, gemessen) + `uiLayout/dice_html.py` (NEU); `_common.py` 2084→1594 Zeilen, Re-Exports stabil.
- **S41 (2026-06-12, Plan 011 + Fraktions-Bereinigung)** `activated_abilities` ersetzt `waaagh_state`; `buff_stat_bonus`/`ability_invuln_save`/`ability_badge_label` generisch; RP-Gate über `keywords`; Resurrection Orb via `handler`; `grep waaagh|necron|_RES_ORB_ID src/` = 0; 783 Tests.
- **S42 (2026-06-12)** Pläne 012 (Loader-Cache) abgeschlossen; Feature-Plan-Queue auf `docs/audit/plans/013–018` umgestellt.
- **S43 (2026-06-12, Plan 013)** Einheitlicher Gruppen-Flow: synthetische Einzelgruppe im Loader, Legacy-`render_attack_declaration` entfernt, Ziele neben Gruppen; 788 Tests. Commit `e6fcdb3`.
- **S44 (2026-06-13)** 5 post-013-Bugs B1–B5 behoben (Ziel-Buttons, `str_bonus`-Reihenfolge, Cover-Position, RP-Gate `rules`, stale `attack_declaration`); 790 Tests. Commit `46e03f8`. + 7 neue Findings F1–F7 dokumentiert.
- **S45 (2026-06-13)** Ganzheitliche Regelrecherche + Verifikation F1–F8 gegen Code/Daten/Regeln (s. `next_session.md`). Ergebnis: F8 (WAAAGH-Sichtbarkeit) war falsch — Badge/Invuln sind verdrahtet; echter Bug = per-Gruppe-Stats (F2/F4). F6 Skorpekh hat bereits `model_groups` (optionaler statt fester Swap). F7 Flag = `movement_locked` (nicht `veil_moved`); `in_melee` wird nicht gecleart.
- **S46 (2026-06-13, Commit `44a29a5`)** Findings F2/F4/F6/F7 + Cover-Layout (Option B) umgesetzt: `ModelGroup.stats` (attacks/strength/ws/bs, Fallback Unit) durch Deklaration + Resolution (Boss Nob A3/S5/WS2+ → Power Klaw mit WAAAGH = S11); Cover-Checkboxen in HIT-/SAVE-Block per Tab; Veil cleart `in_melee` für Träger+CORE und stellt es im Undo wieder her; Skorpekh-Rosters opten Standard-Build (1 Reap-Blade je 3). Block B (WAAAGH-Persistenz) verifiziert = kein Bug; F5/F8 = nichts zu tun. +7 Tests, 797 grün. Manuelle UI-Verifikation + Roster-Audit offen.
- **S47 (2026-06-13, Commits `e98d89d` + `cb39cdd`)** Manuelle Verifikation → Findings G1–G5 alle umgesetzt. G1 (Granaten-Cap pro Einheit), G5 (RP einmal pro Verteidiger nach voller Abhandlung der angreifenden Einheit, generisch), G4 (Reset löscht stale `decl_*`-Widget-Keys — re-verifizieren), G3 (`necrons_test.yaml`). **G2: per-Gruppe-Wunden-Subsystem** (generisch, gegated) + The Silent King als 3-Modell-Einheit (Szarekh W16 Bracket + 2 Triarchal Menhirs W7, Menhirs sterben zuerst); Menhir-Stats aus Wahapedia-9e-Datasheet (lokale Scraper-Lücke). +7 Tests, 804 grün. Offen: manuelle UI-Verifikation; Bracket-Präzision Szarekh (Mini-Follow-up).
- **S47b (2026-06-14, Commit `446c2b6`)** Bracket-Follow-up: `_group_effective_attacks` — Gruppen mit eigenem `attacks` fix (Menhirs A2), Gruppen ohne (Szarekh) über Bracket anhand der eigenen Gruppen-Wunden (A6→A4→A2); in Deklaration + Owner-Budget genutzt; Menhirs `attacks: 2` korrigiert. +3 Tests, 807 grün. Boss Nob W2 bewusst nicht umgesetzt (UX-Abwägung, s. `next_session.md`).
- **S47c (2026-06-14, Commit `7ad42e6`)** Crash-Fix: Silent-King-Gesundheitsbalken warf `st.progress(-0.125)` (uniforme Frontmodell-Formel bei gemischten Wunden). Neuer Helfer `front_group_hp` (Option B) liest das Frontmodell aus der vordersten überlebenden Gruppe (Menhirs zuerst, dann Szarekh), Balken auf [0,1] geclampt. +3 Tests, 810 grün.
- **S48 (2026-06-14, Commit `3e508bb`)** Findings H1–H7 aus manueller Verifikation. H3 Living-Metal-Bug (gruppen-bewusste `unit_max_hp`); H2 Silent-King-Waffen (Menhirs = Annihilator Beam, Szarekh = Sceptre+Staff of Stars+Scythe of Dust); H1 Big-Mek-MA-Wargear (mega-blasta XOR shoota/killsaw, + tellyport blasta); H4a Szarekhan-Dynastiecode korrigiert zu **Uncanny Artificers** (5+ vs MW, Re-roll 1 Wound — „beide Direktiven" war erfunden; Silent King = DYNASTIC AGENT → kein Code, FAQ); H4b Roster-Standard `dynasty:`+`protocol_order` (SK = szarekhan); H5 MWBD 2× bei PHAERON-Keyword; H7 Badge-Farben `_common.py` ↔ `design_colors.md` (MOVED blau, Buff grün). +5 Tests, 815 grün.
- **S49 (2026-06-15, Commits `bd9cbe7`/`bbf0a61`/`fc1dd74`)** Infrastruktur + Logo, keine Gameplay-Fixes.
  (A) **Architektur-Gate** `tests/architecture/` — 4 messbare Invarianten (gameObjects Streamlit-frei,
  YAML nur über Loader, Layer-Richtung, Generic-src mit Schulden-Ledger); Doku in
  `docs/spec/architecture_invariants.md`; `architecture.md` an Realität angeglichen (gameMechanic
  rendert). (B) **Artefakt-Konsolidierung** — `docs/goals/backlog.md` als zentraler Index;
  CLAUDE.md Artefakt-Landkarte + Definition-of-Done-Review-Schritt + Arch-Gate; Doku-Drift-Befunde
  notiert (backlog §4b). (C) **Logo** Soft-Gold integriert (page_icon + Setup-Screen), reproduzierbar
  via `tools/process_logo.py`. +4 Tests (Arch-Gate), 819 grün. Manuelle UI-Verifikation → neue
  Findings 1–9 (s. `next_session.md`); neues GPT-Logo bereit, Integration ausstehend.
- **S50 (2026-06-16)** Freier Lauf durch die S49-Findings (Commits `79e96ee` Logo / `1544ecc` F5 /
  `a989b1c` H2 / `59dda19` H4a / `4f8089f` F7 / `6eb26dd` F8). Neues Crest-Logo freigestellt
  (Flood-Fill + 1px-Erosion, kein Re-Grade) → `assets/`. **Finding 5** Nahkampf-Header zeigte
  „0 assigned" (Pre-Widget-Read) → Placeholder mit echtem `attacks_assigned`. **H2** Scythe of Dust /
  Staff of Stars (melee) als „N additional AND no more than N" → `max_attacks` 4/3 (vorher 10/9).
  **H4a** generisches `dynasty_for()` → Dynastie-Badge auf der armyCard. **Finding 7** generisches
  `active_protocol_buff_labels()` → grüne Protokoll-Buff-Badge auf jeder unitCard + im
  Resolution-Block; `short_protocol_label()` entfernt „Protocol of the "-Präfix überall.
  **Finding 8** explizites 6.-Protokoll-Dropdown + **volle Tausch-Logik über alle Slots**
  (Runde 1–5 + 6.): jeder Slot bietet alle Protokolle, Auswahl tauscht mit dem haltenden Slot
  (Bijektion via `on_change`-Callback + reine, getestete `_protocol_slots_after_swap`; Folge-
  änderung nach Nutzer-Feedback). **Verifiziert ohne Änderung:** F1 (Choppa-Extra schon
  choppa-gebunden), F2 (S=User×2+1=11 regelkonform, generisch), H1 (Loader add/replace korrekt,
  keine Wargear-Picker-UI). +Tests (loader/game_state). **Offen: Finding 9** (Würfel-Alignment) —
  Root Cause notiert, wartet auf Layout-Abstimmung. Regel-Recherche: Veil ⇒ **nicht** „Retreated"
  (kein Fall Back); 6.-Protokoll-Identität fix im Setup, Mid-Game-Wechsel nur per Silent King
  „Voice of the Triarch" (1×/Spiel).
- **S51 (2026-06-16, Commits `3af9a7a`/`c31e73e`)** Finding #1 Faktion-/Subfaction-Badge (generisch,
  immer sichtbar); `dynasty`-Vokabular aus `src/` raus → generisches `subfaction`. Datengetriebenes
  Generic-src-Vokabular-Gate (`test_generic_src_vocab.py` + `_vocab.py`, Ledger = Schuld, Ratchet) +
  Doku-/Akzeptanz-Gate (INV-5); Schulden-Scoreboard nach jedem `pytest`. Baseline in
  `architecture_invariants.md`.
- **S52 (2026-06-17)** INV-4b: `protocol`/`protocols`-Vokabular aus `src/` entfernt — reine,
  verifizierte Umbenennung auf `round_choice` (Klasse `CommandProtocol`→`RoundChoiceAbility`, Datei
  `round_choice_ability.py`, Session-Keys `round_choice_*`, Roster-Feld `round_choice_order`,
  UI-Strings via `load_round_choice_label()`); `gameProtocoll`-Tab/Funktion korrekt zu „Battle Log".
  Ledger-Einträge entfernt (Ratchet); Reste LEGIT (`typing.Protocol`) bzw. `reanimation`-Schuld.
  852 Tests grün, 88.45 %. Manuell verifiziert. **Neuer Befund:** Direktivenwahl im Setup regelwidrig
  + blockiert Rundenzuweisung → Root-Cause + Fix in `backlog.md` §0 #2b / `next_session.md` notiert.
- **S53 (2026-06-17)** Regel-Abdeckung (Akzeptanz-Katalog): neuer Nenner `docs/spec/acceptance/rules.md`
  — Combat-Katalog als verbindliche Vorlage (34 Regeln, Klasse A/B/C, stabile `datei:funktion`-Refs +
  Testnamen). Arbeitsweise in `CLAUDE.md` verankert (Token-Korridor <150k, Subagent-für-Fleißarbeit).
- **S54 (2026-06-17)** Regel-Katalog Phase-1-Gate (read-only): `rules.md` ins Schulden-Scoreboard —
  Abdeckung % je Klasse (A 16/29 · B 0/4 · C 1/1), Ledger (2) + Konsistenz-Check (`getestet: ja`-
  Testname existiert). Parser `tests/acceptance/_rules.py` (regex/disk). 852 Tests grün, 88.45 %.
- **S55 (2026-06-17)** Regel-Katalog: Bereich Command Phase ausgerollt (14 Einträge `R-CMD-01..14`,
  Sonnet-Subagent + Opus-Review). Nenner 48 (34 Combat + 14 Command); Ledger 7. 852 Tests, 88.45 %.
- **S56 (2026-06-18)** Operating Model etabliert: `docs/governance/operating_model.md` (Rollen, Model-
  Tier, 7 Events, 4 Modi), `LEITSTAND.md` als Einstiegstür, ADR-Log + ADR-0001, `docs/inbox/`. Doku-only.
- **S57 (2026-06-18)** Token-Report v1+v2 (`tools/token_report.py` → `docs/metrics/overview.md`):
  Haupt vs. Subagent getrennt je Tier/Session, leser-orientiert (ADR-0002). 12 Tool-Tests.
- **S58 (2026-06-18)** Token-Report v3 (Effizienz statt Menge, ADR-0002): Fokus-Block letzte Session
  + Verlauf 6 Sessions (theme-sichere Balken Peak-Kontext/Subagent/Modell-Mix + Trend) + auto-Hinweise
  + Subagenten-Tabelle (Modell) + Aufgabe aus 1. User-Nachricht; All-Time-Torte raus. 23 Tool-Tests,
  875 gesamt grün, 88.45 %. Bewusster Test-Vertragswechsel (`SessionSummary`) per freigegebener Spec.
- **S59 (2026-06-19)** Regel-Katalog: Bereich Movement Phase ausgerollt (13 Einträge `R-MOVE-01..13`,
  Sonnet-Subagent erfasst aus `core_rules.txt`, Opus reviewt gegen Code/Regeln). Nenner 61 (34 Combat
  + 14 Command + 13 Movement); alle 6 implementierten Movement-Regeln getestet → kein neuer Ledger
  (bleibt 7). Scoreboard C 6/6 (100%). FLY/Transport als Klasse B. Doku-only, 875 Tests, 88.45 %.
- **S60 (2026-06-19)** Regel-Katalog: Bereiche Charge + Morale ausgerollt (`R-CHARGE-01..13` +
  `R-MORALE-01..13`). Nenner 87. Ledger 7→10 (3 Render-Schuld-Einträge). Befund R-COMBAT-32
  (impl.+getestet, aber `offen` → backlog §0). Doku-only, 875 Tests, 88.45 %.
- **S61 (2026-06-19)** Session-Hygiene maschinell verankert: Token-Report-Hook in `settings.json`
  (bei `pytest` läuft `token_report.py --write`); next_session-Gate auf Hysterese (Decke 120 /
  Trim-Ziel 70, `test_doc_health.py` + `conftest.py`); Doku-Schulden reduziert — Referenz aus
  next_session in kanonische Häuser geroutet (Architektur-Muster → `architecture.md`, Regel-Gotchas
  → neue `docs/spec/rules_insights.md`, Constraints → `CLAUDE.md`). next_session 159→62 Zeilen.
- **S62 (2026-06-19)** Doku-Drift R-COMBAT-32 geschlossen („Charging Units Fight First"). Bei der
  Verifikation zeigte sich: nur die *Berechtigung* war getestet, der *Reihenfolge*-Zweig
  (`can_fight_now`/`_any_charged_remain` — Nicht-Gecharger wartet) war ungedeckt → Regressionstest
  `test_non_charged_waits_while_charged_pending` ergänzt, dann R-COMBAT-32 auf `implementiert` +
  `getestet: ja` + `code: fightPhase.py:can_fight_now`. Klasse-A-Abdeckung 28→29 (50 %), Ledger
  unberührt (war `offen`). 876 Tests grün, 88.45 %. Token-Report-Hook empirisch als scharf bestätigt.
  Danach **Regel-Katalog: Bereich Psychic Phase** ausgerollt (`R-PSYCHIC-01..24`, Sonnet-Subagent
  erfasst aus `core_rules.txt`, Opus reviewt gegen `psychicPhase.py`/Tests). Nenner 87→111. Review-
  Korrekturen: R-PSYCHIC-23 (Perils⇒Power-fail) auf `offen` (App revidiert `manifested` nicht);
  R-PSYCHIC-05-Quelle gefixt; Komma→`/`-Testnamen-Trenner. Ledger 10→15 (5 Render-Schuld:
  R-PSYCHIC-11/16/17/18/22 — Smite-Manifest-Logik im Render-Code, policy-ungetestet).
- **S63 (2026-06-19)** Permission-Prompts reduziert (`/fewer-permission-prompts`, 50 jüngste
  Sessions): häufige Read-Befehle (`grep`/`sed`/`find`/`ls`/`git diff/status/log`) auto-erlaubt
  → prompten ohnehin nicht; einzige sichere Ergänzung `Bash(ruff check *)` in
  `.claude/settings.json`. Doku-only, Tests unverändert (892 grün, 88.45 %).
- **S64 (2026-06-19)** Token-Messung prompt-frei: `python3`-Reads verbannt, `jq` nicht
  installiert → `grep`/`tail`-Kanonik in `CLAUDE.md`. Psychic-Render-Schuld Ledger 15→10:
  fünf reine Helfer aus `_render_*`-Funktionen extrahiert (`smite_warp_charge`, `is_manifested`,
  `perils_pending`, `faction_deny_used`, `can_attempt_deny`; R-PSYCHIC-17/18/11/22/16); +16
  Tests (892→908… Befund: nach S63-Meldung tatsächlich 892 grün). Test-Roster: Weirdboy
  (PSYKER Orks) + Canoptek Spyder (deny via `gloom_prism` Basis-rule). **Nutzer-Befund:**
  Deny nicht resettbar (asymmetrischer Reset) → backlog §0 #PSI → S65 gelöst.
- **S65 (2026-06-19)** #PSI implementiert + Token-Gauge-Hook. `refund_deny`/`cleared_deny`
  als reine Helfer in `psychicPhase.py`; einheitlicher `_reset_active_power()` refundiert
  Deny-Budget der inaktiven Fraktion (fixt: denied+reset = permanent verbranntes Budget);
  symmetrisches „Undo deny"-Button; „Skip Deny" verbraucht kein Budget; `deny_faction`-Feld
  in `psi_result`. +8 Tests (`TestRefundDeny`/`TestClearedDeny`), **900 grün**, 88.45 %.
  `tools/session_context.py` (`UserPromptSubmit`-Hook) meldet Live-Kontext je Prompt;
  in `.claude/settings.json` verdrahtet. **Follow-up:** CLAUDE.md `Messen:`-Absatz auf
  Hook umzeigen (verschachtelte `usage`-Objekte brechen den alten `[^}]*`-Regex).
  Noch kein Commit (wartet auf manuelle UI-Verifikation #PSI).
- **S66 (2026-06-19)** Operating-Model-Events Hook-vollzogen (Wurzel: Events waren Prosa,
  „feuerten nicht von selbst"). `tools/session_context.py` eskaliert gestuft (≥120k ⚠️ +
  Retro-Vorankündigung, ≥135k ⛔ Stopp). Hartes Freigabe-Gate `tools/freigabe_gate.py`
  (PreToolUse Edit/Write/NotebookEdit, Exit 2) blockt bis Marker `.claude/.freigabe`;
  SessionStart löscht ihn → jede Session neu scharf. `tools/test_report_reminder.py`
  (PostToolUse pytest) injiziert Token-Report-Teilen-Pflicht. Subagent-Routing bewusst
  NICHT automatisiert (Urteil, kein Konditionalprogramm). ADR-0003 + operating_model.md
  (🔧-Marker). +11 Tests, **911 grün**, 88.45 %. Lücke: Bash-Writes (`>`, `sed -i`) nicht gegated.
- **S67 (2026-06-20)** #PSI verifiziert + abgeschlossen: `TestDenyRefundFlow` (3 Regressions-
  tests) nageln die S65-Fix-End-Zustände fest. Neuer Katalog-Bereich **Battle-Round-Struktur**
  R-ROUND-01..10 (Sonnet-Subagent + Opus-Review). Doku-Drift `init_game_state`→`init_state`
  (3×); R-ROUND-06 gedeckt → Ledger zurück auf 10. CLAUDE.md Token-Messung zeigt auf den
  `session_context.py`-Hook (statt rohem Regex). **915 grün, 91.88 %**, Nenner=121.
  Commits 61d6811, 1b264a4, c9504a4.
- **S68 (2026-06-20)** Vier S67-Nutzerwünsche (Operating-Model/Tooling/Doku): (1) **Voraus-
  schauender Review/Retro-Fragenkatalog** in `operating_model.md` Event 5 (Retro) — Qualität ·
  Operating-Model · Hooks/Gates · blinde Flecken · Automatisierung · Doku/Backlog · Skalierung
  (kleine Experimente, kein Umbau) · Kontext-Versorgung · Priorität · Engpass. (2) CLAUDE.md
  neue Subsection **„Haltung"** (ganzheitlich · konstruktiv-kritisch · lösungsorientiert ·
  vorausschauend · stakeholder-verständlich) für Planning + Abschluss. (3) **Composition-Bar-
  Legende + Zielwerte** in `token_report.py` (input/cache_creation/cache_read/output; cache_read
  hoch = gut, Output gegen Qualität gewichtet, nicht maximieren). (4) **Model-Mix-Zeichen**
  getauscht für Opus/Sonnet-Kontrast: `█` Opus · `·` Sonnet · `▒` Haiku · `▓` sonstige
  (Test mitgezogen — bewusster Verhaltenswechsel). **915 grün, 91.88 %**.
- **S69 (2026-06-20)** ADR-0004 (Skill-Fetch nur per Subagent, ~300k-Befund) + History-Rotation-Tool `tools/rotate_history.py` (Stand→ziel6, next_session schlank; +9 Tests). Ledger 10→8 via Sonnet-Subagent: R-CMD-04/12 ehrlich getestet; R-COMBAT-09 code-Ref auf `ability_invuln_save` korrigiert (Test offen), R-COMBAT-17 auf Klasse C reklassifiziert (App zeigt nur Hinweis, rechnet nicht). R-CMD-03 Befund: CP-Grant ungated — risikoarmer Bug, Fix offen. 952 grün, 91.88 %.
- **S70 (2026-06-20)** Ledger 8→1: R-COMBAT-09-Test + Render-Ledger (R-CMD-03 Battle-forged-Gate, R-CMD-10/11, R-CHARGE-09/10, R-MORALE-02) als verdrahtete, getestete Helfer extrahiert; Opus-Review fing 3 verwaiste Subagent-Helfer (grün, aber nie aufgerufen) ab und verdrahtete sie. Overview um Subagent-Peak-Korridor (150k) erweitert. 985 grün, Cov 92.25 %.
- **S71 (2026-06-20)** Subagent-Selbstprüf-Checkliste kanonisch im Operating Model (Event 3 „Sprint") + CLAUDE.md-Querverweis verankert (dogfooded: beide Subagenten lieferten grep-Belege + Ratchet-/LEGIT-Warnungen). Coverage-Floor 88→90 % (`pyproject.toml`) + CLAUDE.md-Drift 80→90 gefixt. Ziel-Fortschritt-Zeile im Review-Event (Event 5). Regel-Katalog +2 Bereiche via Sonnet-Subagent: Deployment (R-DEPLOY-01..09) + Mission-Scoring (R-SCORE-01..13); 3 implementiert-Fälle (`adjust_vp`/`adjust_secondary_vp`/VP-Render) mit 5 neuen VP-Tests → keine neue Schuld. INV-4b-Migrationsinventar via Subagent reviewt (Verdrahtung offen). 995 grün, Cov 92.40 %, Floor 90.
- **S72 (2026-06-20)** (1) Setup-Bug: Protokoll-Direktiven + WAAAGH im Setup sichtbar via `_ability_section_visible` + früher `return` in `armyCard`; Test `test_ability_sections_hidden_in_setup_only`. (2) INV-4b Quick-Wins: Player 1/2-Labels + setupScreen-Caption generisch. (3) Renames: `pending_irongob`→`pending_triggered_relic`, `res_orb_*`→`revive_wargear_*`. (4) Subagent-Peak-Archiv: `token_report.py` akkumuliert idempotent in `subagent_archive.json`. INV-4 Allowlist 10→5, INV-4b 20→19. 1004 grün, Cov 92.40 %, Floor 90. Setup-Fix manuell verifiziert ✅.
- **S73 (2026-06-20)** Refinement-Session: Pläne 019–022 angelegt (UI-Target-Consolidation, Generic-Activated-Wargear, Arkana, Dice-Display-Rework) + `docs/spec/dice_display.md`. Plan 019 vollständig analysiert (alle 6 Quelldateien gelesen), kein Code wegen Kontext-Limit. Arrow-Direction-Bug `dice_html.py:200` dokumentiert (`rightward = value < 0` FALSCH). INV-4b Cluster 4/5 XS-Fix vorgemerkt.
- **S74 (2026-06-20)** Plan 019 via Sonnet-Subagent: `TargetSelectionRequest`-Dataclass + `pending_target_request` ersetzt `cmd_awaiting_ability_id`/`cmd_awaiting_required_kw`/`wargear_awaiting_bearer_uid`; `render_unit_selectbox`-Helper für Veil-of-Darkness + Mortal-Target; 3 neue Tests in `test_game_state.py`. 1007 Tests grün, Cov 92.40 %, Floor 90.
- **S107 (2026-06-27)** Plan 025 DONE (Conquering Tyrant 9E) + D2 Fall-Back-Schuss-Bugfix; Retro M1/M2/M3/M4
- **S109 (2026-06-28)** Conquering Tyrant: Bug2 Zielwahl-Hang + Dense-Cover-Anzeige (Hit) gefixt; Bug1 verifiziert ok
- **S112 (2026-06-30)** Plan 031 Protokoll-Direktiven-Timing gefixt (is_active entkoppelt, unabhaengige Haupt/Extra-Wahl, Runde-1-Fenster); Ziel6 konsolidiert + Ziel7 (Gefechtsoptionen+subfaction) ausgelagert, Renumbering Crusade->8/Fetcher->9; Doku-Drift 92->99%
