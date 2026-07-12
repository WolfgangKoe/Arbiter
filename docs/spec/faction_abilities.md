# Faction Abilities — Generisches Abstraktionsmodell

> Erstellt: 2026-06-03  
> Aktualisiert: 2026-06-04 — Architektur-Aufräum-Sprint (Ziel 6h)
> Basis: Wahapedia-Recherche aller 10 Hauptfraktionen (WH40k 9E)

---

## Datei-Scope-Regeln (verbindlich)

| Datei | Scope | Wann geladen |
|-------|-------|-------------|
| `faction_abilities.yaml` | Gilt ohne Bedingung für JEDE Armee dieser Fraktion; `ability_type` unterscheidet die Kategorien | Sobald Fraktion geladen |
| `unit_abilities.yaml` | Gebunden an unit- oder keyword-spezifische Regeln (WRAITH, VEHICLE, CRYPTEK) | Wenn Einheit/Keyword in Armee |
| `subfaction_abilities.yaml` | Gebunden an Subfaction-Keyword (Dynasty, Clan, Shield Host, Supplement) | Wenn Subfaction aktiv |
| `wargear_abilities.yaml` | Gebunden an Ausrüstungsgegenstand; enthält auch `arkana:`-Block für Cryptek-Arkana | Wenn Ausrüstung ausgewählt |
| `powers.yaml` | Psionische Kräfte (je Fraktion); `power_type: psychic \| deny \| ctan` | Stub; noch nicht verdrahtet |
| `_shared/shared_abilities.yaml` | ObjSec, Deep Strike, FNP, Fly + BigGuns, LookOut, HeroicIntervention | Stub; noch nicht verdrahtet |
| `_shared/shared_powers.yaml` | Smite, Deny the Witch, Perils of the Warp | Stub; noch nicht verdrahtet |
| `_shared/stratagems.yaml` | 7 Core Stratagems (war `universal/stratagems.yaml`) | verdrahtet: `load_stratagems()` |

**Regel:** Neue Fraktion = nur YAML in `faction_abilities.yaml`. Kein Code-Change nötig, solange der `ability_type` bereits unterstützt ist.

---

## Übersicht

Fraktionsfähigkeiten in WH40k 9E fallen in **6 Kategorien**. Jede hat ein eigenes `ability_type`-Feld und ein eigenes UI-/State-Pattern.

---

## Kategorie 1 — Runden-Wahl (`round_choice`)

**Mechanik:** In der Befehlsphase wählt der Spieler eine Fähigkeit aus einer begrenzten Liste. Jede Option ist nur einmal pro Partie verwendbar. Die Wahl kann eine oder zwei Stances/Direktiven haben.

**Subfaction-Affinität:** Jede `round_choice`-Option kann ein `subfaction_affinity`-Feld haben.
Wenn die aktive Subfaction des Spielers mit dieser Affinität übereinstimmt, aktivieren sich
**beide** Direktiven gleichzeitig (statt einer) — beim permanenten 6. Protokoll wie beim
rundenzugewiesenen (Engine: `_active_directive_effects`/`_extra_directive_effects`;
UI: „… BONUS (BOTH)"-Badge ohne Wahlzwang, S140).

**Fraktionen:**

| Fraktion | Mechanik-Name | Optionen | Stances | Affinität-Feld | Anmerkungen |
|----------|---------------|----------|---------|----------------|-------------|
| Necrons | Command Protocols | 6 | Primary + Secondary | Dynasty (szarekhan, mephrit, …) | Runde 1: Eternal Guardian auto-aktiv (`auto_round_1: true`) |
| Adeptus Custodes | Ka'tahs of the Broadsword | 6 | Aggressive + Stoic Stance | Shield Host (solar_watch, …) | Kein auto_round_1 |
| Adeptus Mechanicus | Canticles of the Omnissiah | 6 | Keine (nur 1 Effekt) | — | `secondary` optional |
| Tyranids | Synaptic Imperatives | bis 10 | Keine | — | Pool dynamisch: schrumpft wenn Synapse-Einheiten sterben |

**YAML-Ort:** `data/wh40k_9e/<faction>/faction_abilities.yaml` als `ability_type: round_choice`  
**Loader:** `load_round_choice_abilities(faction_dir)` in `loader.py` — liest aus `faction_abilities.yaml`, filtert auf `ability_type == "round_choice"`, gibt `list[CommandProtocol]` zurück.

**YAML-Schema:**
```yaml
- id: wh40k_9e.<faction>.faction.<ability_id>
  name_en: "Protocol / Ka'tah / Canticle Name"
  name_de: "Deutsch"
  ability_type: round_choice
  source: faction_rule
  auto_round_1: false        # true nur wenn Runde-1-Pflicht
  subfaction_affinity: <id>  # optional; ID des Subfaction-Eintrags
  round_choice_label: "..."  # top-level im YAML (nicht per Eintrag)
  primary: "Effektbeschreibung Primary/Aggressive"
  secondary: "Effektbeschreibung Secondary/Stoic"  # optional
  directives:
    primary:
      effect:
        type: hit_modifier   # oder anderer wired/display-only Typ
        value: 1
        phase: shooting
    secondary:               # optional
      effect:
        type: strength_modifier
        value: 1
        phase: shooting
```

**Session-State:** `active_protocol_id`, `active_directive`, `used_protocol_ids`  
**UI:** `armyCard._render_protocol_ui()` — generisch; `round_choice_label` aus YAML für Überschrift; kein Faction-Hardcoding

**Tests erforderlich:**
- `test_load_protocols_<faction>()` — YAML korrekt geladen
- `test_protocol_used_ids_prevents_reuse()` — Keine Wiederholung
- `test_protocol_no_stance_canticle_style()` — Optional secondary

---

### Direktiv-Wiring-Status (Plan 024, S86 — Steps 1–4)

Die aktive `round_choice`-Direktive liefert ihren Effekt **nicht** mehr direkt an
die Konsumenten; alle lesen über drei kanonische Abfrage-Funktionen in
`abilityEngine.py` (nie direkt aus `session_state`):

| Funktion | Rückgabe | deckt ab |
|----------|----------|----------|
| `get_active_round_choice_modifier(faction_dir, phase, use_melee)` | `dict[str,int]` (Keys `hit`/`wound`/`save`/`strength`/`ap`/`move`/`leadership`) | numerische Direktiven |
| `get_active_round_choice_rerolls(faction_dir, phase, use_melee)` | `set[str]` (`reroll_save_1`/`reroll_hit_1`/`reroll_wound_1`) | Reroll-Direktiven |
| `get_active_rp_modifiers(faction_dir)` | `dict[str,int\|bool]` (`rp_reroll`/`rp_bonus`) | Undying Legions P/S |

`_WIRED_EFFECT_TYPES` ist die autoritative Liste der numerischen Effekttypen
(`hit_modifier`, `wound_modifier`, `save_modifier`, `strength_modifier`,
`ap_bonus`, `move_bonus`, `leadership_bonus`). Ein neuer Eintrag dort wirkt
automatisch für **jede** Fraktion mit `round_choice`-Direktiven — kein
fraktionsspezifischer Code. `charge_after_advance_allowed` prüft zusätzlich die
aktive Direktive auf `type: advance_and_charge` (Sudden Storm S).

Damit sind alle 12 Necron-Direktiv-Effekte engine-seitig verdrahtet (vorher nur
3 von 12). Status der **Anzeige**-Verbindung je Effekt: Backlog #2 (Protokoll-Buff-Audit).
Hinweise ohne UI-Konsument heute: `leadership` (Morale-Phase nicht voll verdrahtet,
`# TODO` im Code).

### Arkana — Dispatch- vs. Display-Status (Plan 024, S87 — Steps 5–6)

12 Cryptek-Arkana liegen in `data/wh40k_9e/necrons/faction_abilities.yaml`
(`category: arkana`). Alle haben strukturiertes `trigger`/`conditions`/`effect`
+ englischen `rule_text` (Schema = Doku/Display, **keine** Dispatch-Pflicht). Die
Einstufung „dispatchbar" folgt aus dem Regeltext × vorhandenen Engine-Handlern,
NICHT aus der YAML.

- **1 dispatchbar** (`ability_type: activated`): **Failsafe Overcharger** — „+1
  Attacks auf eine CANOPTEK-Einheit" mappt auf das vorhandene `buff_stat`-Muster
  (`buff_stat_bonus`). Aktivierbar in der Command-Phase über `_render_activated_wargear`.
- **11 bleiben `descriptive`** — jeweils, weil ein Engine-Subsystem **fehlt**:

  | Arkanum | fehlendes Subsystem |
  |---------|---------------------|
  | Atavindicator, Metalodermal Tesla Weave, Quantum Orb | Mortal-Wound-Handler |
  | Hypermaterial Ablator, Prismatic Obfuscatron | räumliches Proximity-Tracking |
  | Photonic Transubjector | Damage-Nullify-Hook im Save-Loop |
  | Dimensional Sanctum | Ability-Grant-Dispatch |
  | Phylacterine Hive | Meta-Ability-Targeting |
  | Countertemporal Nanomines | Halve-Movement-Modifier |
  | Cryptogeometric Adjuster | Enemy-Direction-Hit-Debuff |
  | Cortical Subjugator Scarabs | HI-Eligibility-Grant + Unit-Auswahl |

  Sobald eines dieser Subsysteme existiert (eigener Plan), kann der betreffende
  Eintrag aufgewertet werden — **ohne** `src/` anzufassen (alles aus YAML-Feldern).

Punktkosten gegen `wahapedia_necrons/faction_overview.txt` korrigiert (alle 12 −5).

---

### Effekttyp `attrition_modifier` (Combat Attrition, Plan 018 Task 18.3, S128)

**Mechanik:** Modifiziert den Combat-Attrition-Schwellwert einer Einheit (App zeigt den
Schwellwert an, die W6-Würfe selbst bleiben Tisch-Verantwortung — Klasse C). Beispiel:
Gretchin „Cowardly" (`orks/unit_abilities.yaml`) — ohne RUNTHERD in 6" ein zusätzlicher
Modifier auf jeden Attrition-Wurf.

```yaml
effect:
  type: attrition_modifier
  modifier: -1
  target: self
  effects:
    - condition_prompt: "Friendly RUNTHERD within 6\"?"
      applies_when: false
```

**Konvention `condition_prompt`/`applies_when`:** Ein roher Sub-Eintrag in `effects` statt
eines First-Class-Felds auf `Ability`/`Effect` (Schema-Follow-up, s. Backlog-Task
„`condition_prompt`/`applies_when` als First-Class-Felder"). `condition_prompt` ist der
Wortlaut der Nutzer-Checkbox (Tisch-Bedingung, die die App nicht selbst prüfen kann —
gleiches Muster wie Cover); `applies_when` legt fest, bei welchem Checkbox-Zustand der
Modifier aktiv ist (`false` = aktiv, solange die Checkbox NICHT gesetzt ist, wie bei
Cowardly Grots).

**Engine:** `moralePhase.attrition_modifier_abilities()` filtert die passenden Fähigkeiten;
`moralePhase._attrition_threshold(unit, unit_state, active_modifiers)` errechnet den
W6-Schwellwert (Basis 1, +1 wenn die Einheit unter halber Stärke ist, +1 je aktivem
Modifier). Reine Funktion, direkt getestet (`TestAttritionThreshold`,
`tests/gameMechanic/test_morale_phase.py`).

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

**Stufen-Anker + Stufen-Ende:** Stufenwechsel und Ende sind an den **Start der Command-Phase
des Besitzers** geankert — nicht an Zug- oder Rundenwechsel (`gameState.py:_reset_turn_state()`:
nur wenn der Besitzer der neue aktive Spieler ist UND `round_activated < round`; beim Stufenwechsel
wird `round_activated` fortgeschrieben). Stufe 2 hält also die komplette Runde inkl. gegnerischem
Zug. Erreicht der Eintrag dabei eine Stage ohne `next_stage_id` (z.B. `waaagh_stage2`), erlischt
die Ability generisch — der Eintrag wird aus `activated_abilities[player]` entfernt.
Regelbeleg: `docs/work/wahapedia_orks/faction_overview.txt` — Stage 1 „lasts until the start of
your next Command phase", Stage 2 „until the start of your subsequent Command phase. After this
point, the Waaagh! ... is no longer active, and has no further effect." Gilt für jede gestufte
Ability ohne Folgestufe, nicht nur WAAAGH!.

**Once per battle:** unabhängig vom Aktiv-Status im Ledger
`used_once_per_battle_abilities: {player: set[ability_id]}` getrackt
(`gameState.py: mark_once_per_battle_used() / is_once_per_battle_used()`, gesetzt beim
Aktivieren in `armyCard._render_once_per_battle_ability_ui()`). Das Stufen-Expiry leert den
Ledger NICHT — sonst wäre die Fähigkeit nach Ablauf erneut aufrufbar (S138-Befund).

**Session-State:** `waaagh_state: {player_name: {stage, round_activated}}`  
**UI:** `armyCard._render_waaagh_ui()` — generisch über `command_activated`-Filter auf `faction_abilities`

**Tests erforderlich:**
- `test_waaagh_activation_sets_stage_1()`
- `test_waaagh_stage2_transition_on_new_round()`
- `test_waaagh_once_per_battle()`
- `test_staged_ability_without_next_stage_expires_at_owner_command_phase()` (generisch, `test_game_state.py`)
- `test_staged_ability_stage2_survives_opponents_turn()` (`test_game_state.py`)
- `test_once_per_battle_ledger_survives_staged_ability_expiry()` (`test_game_state.py`)
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

### Phase 1 ✅ (2026-06-03)
- Necrons Command Protocols: vollständig (`armyCard._render_protocol_ui()`)
- Orks WAAAGH!: Badge + Aktivierung + Stage-2-Transition (`armyCard._render_waaagh_ui()`)
- Protokoll-Badge: HTML-Badge nach Direktiven-Wahl
- Sourced Modifier-Labels in `_common.py`

### Phase 2 ✅ (2026-06-04 — Architektur-Aufräum-Sprint + 6-Batch-Plan)
- `command_protocols.yaml` → in `faction_abilities.yaml` als `ability_type: round_choice` (Necrons)
- `load_round_choice_abilities()` ersetzt `load_command_protocols()` (Alias entfernt — Batch 4)
- `_ETERNAL_GUARDIAN_ID` Hardcoding → generische `auto_round_1`-Suche
- `commandPhase.py`: `"eternal_guardian"` Hardcoding → `auto_round_1`-Suche
- `round_choice_label` im YAML → dynamische Überschrift statt "Command Protocols" Hardcoding
- `subfaction_affinity` Feld in `CommandProtocol` + Loader (UI erledigt S140)
- Custodes Ka'tahs: `data/wh40k_9e/adeptus_custodes/faction_abilities.yaml` ✅
- Necron `faction_abilities.yaml` aufgeräumt: 5 Fehlplatzierte entfernt
- Necron `unit_abilities.yaml`: quantum_shielding, phase_shifter, wraith_form, dimensional_translocation
- Necron `subfaction_abilities.yaml`: Destroyer Cult + hardwired_for_destruction
- Necron `wargear_abilities.yaml`: 13 Arkana migriert; `arkana.yaml` gelöscht
- Ork `faction_abilities.yaml`: mob_rule, ramshackle, beast_snagga → unit_abilities.yaml
- Ork `faction_abilities.yaml`: objective_secured → `unit_abilities.yaml` (Batch 1)
- Ork `faction_abilities.yaml`: psychic powers → `powers.yaml` (Batch 3)
- `_shared/shared_abilities.yaml`: ObjSec, Deep Strike, Fly, FNP + 3 weitere (Batch 2)
- `_shared/shared_powers.yaml`: Smite, Deny, Perils (Batch 2, NEU)
- `_shared/stratagems.yaml`: migriert aus `universal/` (Batch 0); IDs auf `shared`-Namespace
- `_shared/detachment_types.yaml`: CP-Felder `command_cost` + `command_benefit` ergänzt (Batch 2)
- Subfaction-Affinitäten korrigiert: Necrons 4 Werte, Custodes 2 Werte + rendax-ID (Batch 1)

### Phase 3 (nächste Priorität)
1. ✅ **subfaction_affinity UI** (S140): aktive Subfaction == `subfaction_affinity` →
   beide Direktiven aktiv, Round- wie 6.-Protokoll-Zweig
2. **AdMech Canticles YAML** (`data/wh40k_9e/adeptus_mechanicus/faction_abilities.yaml`)
   - `secondary` bereits optional (Loader gibt leeres dict zurück)
3. **Tests für Custodes und AdMech** schreiben
4. **Auto-Progression: Space Marines Doctrines**

### Phase 4 (mittelfristig)
5. **T'au Mont'ka/Kauyon** — in `_render_waaagh_ui()` integrieren
6. **Tyranid Synaptic Imperatives** — dynamischer Pool-Check
7. **load_shared_abilities()** verdrahten

### Phase 5 (langfristig)
8. Chaos SM Let the Galaxy Burn (Hybrid)
9. Thousand Sons Cabal Points
10. Astra Militarum Orders
11. Aeldari Strands of Fate

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

Coverage-Ziel: 80% auf allen `abilityEngine.py`-Funktionen.
