# Faction Abilities — Generisches Abstraktionsmodell

> Erstellt: 2026-06-03  
> Basis: Wahapedia-Recherche aller 10 Hauptfraktionen (WH40k 9E)

---

## Übersicht

Fraktionsfähigkeiten in WH40k 9E fallen in **6 Kategorien**. Jede hat ein eigenes YAML-Schema und ein eigenes UI-/State-Pattern. Die App muss alle 6 Kategorien unterstützen — nicht nur die zwei ursprünglich implementierten.

---

## Kategorie 1 — Runden-Wahl (`round_choice`)

**Mechanik:** In der Befehlsphase wählt der Spieler eine Fähigkeit aus einer begrenzten Liste. Jede Option ist nur einmal pro Partie verwendbar. Die Wahl kann eine oder zwei Stances/Direktiven haben.

**Fraktionen:**

| Fraktion | Mechanik-Name | Optionen | Stances | Anmerkungen |
|----------|---------------|----------|---------|-------------|
| Necrons | Command Protocols | 6 | Primary + Secondary | Runde 1: Eternal Guardian auto-aktiv |
| Adeptus Custodes | Martial Ka'tah | 6 | Aggressive + Stoic Stance | Reihenfolge im Spiel geordnet |
| Adeptus Mechanicus | Canticles of the Omnissiah | 6 | Keine (nur 1 Effekt) | Freie Reihenfolge |
| Tyranids | Synaptic Imperatives | bis 10 | Keine | Pool dynamisch: schrumpft wenn Synapse-Einheiten sterben |

**YAML-Schema:** `data/wh40k_9e/<faction>/command_protocols.yaml`  
Alle vier Fraktionen benutzen **dasselbe Schema** — `secondary` und `secondary_effect` sind optional.

**Session-State:** `active_protocol_id`, `active_directive`, `used_protocol_ids`  
**UI:** `armyCard._render_protocol_ui()` — bereits generisch (no-op wenn keine Protokoll-YAML vorhanden)

**Tests erforderlich:**
- `test_load_protocols_<faction>()` — YAML korrekt geladen
- `test_protocol_used_ids_prevents_reuse()` — Keine Wiederholung
- `test_protocol_no_stance_canticle_style()` — Optional secondary

---

## Kategorie 2 — Einmalig-Deklariert (`one_time`)

**Mechanik:** Einmal pro Partie in der Befehlsphase aktiviert. Mehrere Stages möglich (Stage 1 diese Runde, Stage 2 folgerundeAuto-Übergang).

**Fraktionen:**

| Fraktion | Mechanik-Name | Varianten | Stages | Aktiv-Runden |
|----------|---------------|-----------|--------|--------------|
| Orks | WAAAGH! | 3 (Standard/Speed/Great Waaagh!) | 2 | Stage 1: Aktivierungsrunde; Stage 2: nächste Runde |
| T'au Empire | Philosophies of War | 2 (Mont'ka/Kauyon) | 1 (kein Stage-Übergang) | Mont'ka: R1–3; Kauyon: R3–5 |

**YAML-Schema:** In `faction_abilities.yaml` als `ability_type: activated` + `trigger.phase: command`  
Stages werden in `faction_abilities.yaml` als separate Ability-Einträge modelliert (waaagh_stage1, waaagh_stage2).

**Session-State:** `waaagh_state: {player_name: {stage, round_activated}}`  
**UI:** `armyCard._render_waaagh_ui()` — generisch über `command_activated`-Filter auf `faction_abilities`

**Tests erforderlich:**
- `test_waaagh_activation_sets_stage_1()`
- `test_waaagh_stage2_transition_on_new_round()`
- `test_waaagh_once_per_battle()`
- `test_tau_montka_active_rounds_1_to_3()`
- `test_tau_kauyon_active_rounds_3_to_5()`

---

## Kategorie 3 — Auto-Progression (`auto_progression`)

**Mechanik:** Kein Spieler-Input. Die Fähigkeit wechselt automatisch nach Rundenfortschritt. Kein UI-Aktivierungsbutton. UI zeigt nur den aktuellen Effekt als Info-Badge.

**Fraktionen:**

| Fraktion | Mechanik-Name | Regel |
|----------|---------------|-------|
| Space Marines | Combat Doctrines | R1: +1 AP Heavy / R2: +1 AP Assault+RF / R3+: +1 AP Pistol+Melee |
| Death Guard | Contagions of Nurgle | Passiv, Reichweite wächst: R1=1" / R2=3" / R3=6" / R4+=9" |
| Chaos SM | Let the Galaxy Burn | R1+R2: auto; R3: Spieler wählt zwischen 2 Optionen (Hybrid) |

**YAML-Schema:** `faction_abilities.yaml` als `ability_type: auto_progression`  
```yaml
- id: example.faction.combat_doctrines
  ability_type: auto_progression
  progression:
    - round: 1
      effect: {type: ap_modifier, value: -1, weapon_types: [Heavy]}
    - round: 2
      effect: {type: ap_modifier, value: -1, weapon_types: [Assault, Rapid Fire]}
    - round: 3
      effect: {type: ap_modifier, value: -1, weapon_types: [Pistol, Melee]}
```

**Session-State:** Kein separater State — Effekt wird direkt aus `current_round` + YAML berechnet  
**UI:** Nur Info-Badge in armyCard; kein Aktivierungsbutton  
**Engine:** `get_auto_progression_modifier(faction_dir, phase, round)` → `dict[str, int]`

**Tests erforderlich:**
- `test_doctrine_modifier_round_1()` — korrekte Phase/Effekt-Kombination
- `test_doctrine_modifier_round_3_plus()` — Round >= 3 gleich wie Round 3
- `test_auto_progression_no_player_input_needed()`

---

## Kategorie 4 — Ressourcen-basiert (`resource_based`)

**Mechanik:** Spieler akkumuliert Ressourcen-Punkte (Cabal Points, Fate Dice) und gibt sie für Effekte aus. Separat von den anderen Kategorien — eigenes UI-System.

**Fraktionen:**

| Fraktion | Mechanik-Name | Ressource | Phase |
|----------|---------------|-----------|-------|
| Thousand Sons | Cabbalistic Rituals | Cabal Points | Psionik-Phase |
| Aeldari | Strands of Fate | Fate Dice (6W6) | Rundenbeginn |

**Status:** Noch nicht geplant. Separat zu implementieren wenn diese Fraktionen hinzukommen.

---

## Kategorie 5 — Verteilungs-System (`distribution`)

**Mechanik:** Ein Officer/HQ gibt Buffs an einzelne Einheiten aus. Kein globaler Toggle — unit-level Buffing.

**Fraktionen:**

| Fraktion | Mechanik-Name | Anmerkungen |
|----------|---------------|-------------|
| Astra Militarum | Voice of Command (Orders) | 18 Orders in 3 Kategorien; jeder Officer gibt 1–2 Orders pro Runde |

**Status:** Noch nicht geplant. Näher am `commandPhase`-Ability-System als am Protokoll-System.

---

## Kategorie 6 — Passive / Persistent (`passive`)

**Mechanik:** Kein Aktivierungsschritt. Immer aktiv. Wird über Keyword-/Regel-Checks ausgelöst.

**Fraktionen:** Alle Klan-Kulturen (Orks), alle Dynastien (Necrons), Ramshackle, Living Metal, etc.

**Status:** Größtenteils abgedeckt durch `triggered`-Abilities in `faction_abilities.yaml`.

---

## Implementierungsplan

### Phase 1 (aktuell implementiert) ✅
- Necrons Command Protocols: vollständig (`armyCard._render_protocol_ui()`)
- Orks WAAAGH!: Badge + Aktivierung + Stage-2-Transition (`armyCard._render_waaagh_ui()`)
- Protokoll-Badge: HTML-Badge nach Direktiven-Wahl
- Sourced Modifier-Labels in `_common.py`

### Phase 2 (nächste Priorität)
1. **Custodes Ka'tah YAML anlegen** (`data/wh40k_9e/adeptus_custodes/command_protocols.yaml`)
   - Format identisch zu Necrons; `secondary` = Stoic Stance; alle 6 Ka'tahs
   - Kein Code-Änderung nötig — `_render_protocol_ui()` funktioniert bereits
2. **Loader: `secondary` optional machen** für AdMech Canticles (kein secondary_effect)
3. **AdMech Canticles YAML anlegen** (`data/wh40k_9e/adeptus_mechanicus/command_protocols.yaml`)
4. **Tests für Custodes und AdMech** schreiben

### Phase 3 (mittelfristig)
5. **Auto-Progression: Space Marines Doctrines**
   - `ability_type: auto_progression` YAML-Schema einführen
   - `get_auto_progression_modifier()` in `ability_engine.py`
   - Info-Badge in armyCard (kein Button)
6. **T'au Mont'ka/Kauyon** — in `_render_waaagh_ui()` integrieren (gleiche Logik)
7. **Tyranid Synaptic Imperatives** — dynamischer Pool-Check (welche Synapse-Units noch leben)

### Phase 4 (langfristig)
8. Chaos SM Let the Galaxy Burn (Hybrid: Auto + 1 Wahl in R3)
9. Thousand Sons Cabal Points (eigenes Ressourcen-UI, Psionik-Phase)
10. Astra Militarum Orders (unit-level Distribution)
11. Aeldari Strands of Fate (Würfelpool-Management)

---

## Test-Coverage-Anforderungen

Jede neue Fraktion die hinzukommt, braucht **mindestens** diese Tests:

```
tests/
  test_faction_abilities_<faction>.py
    test_load_<ability_type>_<faction>()         — YAML-Loading
    test_<ability>_modifier_<phase>()            — Modifier-Berechnung je Phase
    test_<ability>_used_tracking()               — Verwendungs-Tracking
    test_<ability>_no_player_input_needed()      — Auto-Progression: kein State
    test_<ability>_badge_label()                 — Badge-Text korrekt
```

Coverage-Ziel: 80% auf allen `ability_engine.py`-Funktionen.
