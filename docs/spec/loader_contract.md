# Loader Contract — Spec
<!-- Ergebnis der Architektur-Session 2026-05-31. Grundlage für Ziel 5c (Loader) und Schritt 2 (Schema-Bereinigung). -->

> Verwandte Dokumente: `docs/spec/army_builder.md` (bestehende Spec, wird danach aktualisiert),
> `docs/spec/architecture.md`, `data/wh40k_9e/_shared/detachment_types.yaml`,
> `data/wh40k_9e/necrons/army_rules.yaml`

---

## 1. Datenmodell — `Weapon`

Das `Weapon`-Dataclass bekommt eine `profiles`-Liste. Auch Single-Profile-Waffen haben eine
Liste mit einem Eintrag. Damit ist das Modell einheitlich und der Combat-Code braucht keinen
Sonderfall für Dual-Profile-Waffen.

```python
@dataclass
class WeaponProfile:
    name: str           # "" für Single-Profile; "Shooting" / "Melee" für Dual-Profile
    weapon_type: str    # "Rapid Fire 1", "Melee", "Assault 3", …
    range_inches: int   # 0 für Nahkampf
    attacks: str        # "1", "D6", "*" (= Einheits-A-Wert, nur Nahkampf)
    strength: str       # "4", "User", "User+2", "User×2"
    ap: str             # "0", "-1", "-3"
    damage: str         # "1", "D3", "2"
    abilities: str      # Freitext-Sonderregel
    is_melee: bool

@dataclass
class Weapon:
    id: str
    name_en: str
    profiles: list[WeaponProfile]
```

### Combat-System-Integration

| Phase | Profil-Auswahl |
|-------|---------------|
| Fernkampfphase | `[p for p in weapon.profiles if not p.is_melee]` |
| Nahkampfphase | `[p for p in weapon.profiles if p.is_melee]` |

`"*"` in `attacks` bedeutet: verwende `unit.attacks` (A-Charakteristik). Auflösung geschieht
**vor** `resolve_attack_sequence()` (wie bisher bei `"User"`).

### `grantsKeyword` (S148 Brief 4 — bewusster camelCase-Ausnahmefall)

`WeaponProfile` trägt ein optionales `grants_keyword: str | None` (YAML: `grantsKeyword`,
z. B. `GAUSS`/`TESLA` auf 21 Necron-Waffenprofilen in `weapons.yaml` + der Voltaic-Staff-
Ausnahme in `relics.yaml`). Generischer Loader-Mechanismus (`_apply_weapon_granted_keywords`,
`src/gameObjects/loader.py`): jede Waffe mit `grantsKeyword: X` im Loadout gibt der Einheit
Keyword X — unabhängig vom konkreten X, kein Fraktionsstring in `src/`. Landet in **zwei**
Sets: `unit.keywords` (funktional — das ist dieselbe Menge, die `has_keywords`-Bedingungen in
`abilityEngine.py`/`stratagem.py` bereits ungeändert lesen) und `unit.derived_keywords`
(Anzeige, analog `wargear_keywords`). Ist das erste bewusst camelCase benannte YAML-Feld in
diesem Bereich — Einordnung in die Migrationsgrundlage: Abschnitt 8.

---

## 2. Roster-Format

Das Roster ist die Single Source of Truth für eine konkrete Armeeauswahl. Der Loader liest
Catalog-Daten (YAML-Datenbank) + Roster → gibt ein vollständig aufgelöstes `Army`-Objekt zurück.

```yaml
roster_id: player1_necrons_2026-xx-xx
faction: necrons
subfaction: Szarekhan          # null = keine Dynasty
game_size: strike_force        # patrol | incursion | strike_force | onslaught
battle_forged: true

# Necrons: 5 von 6 Protokollen, Reihenfolge = Runden-Zuweisung (Runde 1 immer eternal_guardian)
command_protocols:
  - wh40k_9e.necrons.protocol.eternal_guardian
  - wh40k_9e.necrons.protocol.hungry_void
  - wh40k_9e.necrons.protocol.conquering_tyrant
  - wh40k_9e.necrons.protocol.undying_legions
  - wh40k_9e.necrons.protocol.vengeful_stars

detachments:
  - detachment_type: patrol
    name: Patrol Detachment     # optional, Default = detachment_type
    units:

      # HQ mit Warlord-Trait und Relic
      - unit_id: wh40k_9e.necrons.unit.overlord
        models: 1
        warlord: true
        warlord_trait: wh40k_9e.necrons.warlord_trait.enduring_will
        relic: wh40k_9e.necrons.relic.sphaere_der_ewigkeit   # ersetzt resurrection_orb
        wargear:
          - wh40k_9e.necrons.wargear.phylactery
        # weapon_loadout weggelassen → Default aus units.yaml (Staff of Light)

      # Cryptek mit Arkana
      - unit_id: wh40k_9e.necrons.unit.technomancer
        models: 1
        warlord: false
        warlord_trait: null
        relic: null
        wargear:
          - wh40k_9e.necrons.wargear.canoptek_cloak
        arkana:
          - wh40k_9e.necrons.arkana.failsafe_overcharger

      # Troops: alle Modelle tragen dieselbe Wahl (kein model_count nötig)
      - unit_id: wh40k_9e.necrons.unit.warriors
        models: 10
        warlord: false
        warlord_trait: null
        relic: null
        wargear: []
        arkana: []
        weapon_loadout:
          - weapons: [wh40k_9e.necrons.weapon.gauss_flayer]

      # Elites mit gemischter Bewaffnung (7 Schwert+Schild, 3 Kriegssense)
      - unit_id: wh40k_9e.necrons.unit.lychguard
        models: 10
        warlord: false
        warlord_trait: null
        relic: null
        wargear: []
        arkana: []
        weapon_loadout:
          - weapons:
              - wh40k_9e.necrons.weapon.hyperphase_sword
              - wh40k_9e.necrons.weapon.dispersion_shield
            model_count: 7
          - weapons:
              - wh40k_9e.necrons.weapon.warscythe
            model_count: 3

unmatched: []     # Einheiten, die keiner Katalog-ID zugeordnet werden konnten
```

### `weapon_loadout`-Feld

Ersetzt `weapon_choices` und modelliert die tatsächliche Bewaffnung pro Einheit:

| Fall | Roster-Eintrag |
|------|---------------|
| Default beibehalten (alle Modelle tragen `units.yaml`-Waffen) | `weapon_loadout` weglassen |
| Alle Modelle tragen dieselbe Non-Default-Waffe | Ein Eintrag ohne `model_count` |
| Gemischte Bewaffnung | Mehrere Einträge mit `model_count`; Summe muss `models` ergeben |

`weapons` ist immer eine Liste — ein Modell kann mehrere Waffen gleichzeitig tragen
(z.B. Schwert + Schild als separate Objekte).

Der Loader überprüft beim Auflösen, ob die gewählte Kombination in den `wargear_options`
der Einheit zulässig ist. Ungültige Auswahlen → `Army.warnings`.

### `weapon_swaps` + `group_loadouts` (6m/6n — Modellgruppen)

Einheiten mit `model_groups` in `units.yaml` beschreiben ihre Datasheet-Wargear-Optionen
als **`weapon_swaps`** (Ersetzungen, nicht Additionen — RAW-Wortlaut „can be replaced").
Einheiten mit `model_groups` haben **kein** unit-level `weapons:`-Feld mehr — der Loader
bildet die flache Union aus allen Gruppen-Waffen + Swap-Optionen (`_group_weapon_ref_union`).

**Swap-Schema (`units.yaml`):**

```yaml
model_groups:
  - id: ork_boy
    count: remainder
    weapons: [slugga, choppa, stikkbombz]          # Default-Bewaffnung
    weapon_swaps:
      - id: shoota_swap
        scope: per_model      # einzelne Modelle tauschen (→ Sub-Gruppen-Split)
        limit: any            # any | per_10 | per_5 | per_3 (pro volle 10/5/3 Modelle der EINHEIT)
        replaces: [slugga, choppa]
        options: [shoota]
  - id: boss_nob
    count: 1
    weapons: [slugga, choppa, stikkbombz]
    weapon_swaps:
      - id: nob_weapons
        scope: group          # die ganze Gruppe tauscht gemeinsam
        pick: 2               # „two of the following" (Wiederholung erlaubt: 2× killsaw)
        replaces: [slugga, choppa]
        options: [big_choppa, choppa, killsaw, power_klaw, power_stabba, slugga]
```

`replaces: []` modelliert reine Additionen („can be equipped with", z.B. Warbikers-Slugga).

**Roster-Auflösung (`group_loadouts` → `swaps`):**

```yaml
group_loadouts:
  boss_nob:                       # scope group: EIN Mapping mit weapons-Liste (pick Stück)
    swaps:
      nob_weapons:
        weapons: [power_klaw, big_choppa]
  ork_boy:                        # scope per_model: LISTE von {weapons, count}-Einträgen
    swaps:
      shoota_swap:
        - weapons: [shoota]
          count: 3
      special_weapon:
        - weapons: [big_shoota]
          count: 1
```

Auflösung durch `_resolve_model_groups()` (`gameObjects/loader.py`):

- **group-Scope:** Gruppen-Waffen = Basis − `replaces` + gewählte `weapons`
- **per_model-Scope:** pro Eintrag entsteht eine **Sub-Gruppe mit fixen Waffen**
  (`ork_boy_shoota`, count=3); der Rest behält die Basis-Bewaffnung. Die gesamte
  Laufzeit-Logik (UI, Combat, group_models) arbeitet nur mit einfachen Gruppen.
- Fehlt `group_loadouts`/ein Swap-Eintrag → Default-Bewaffnung bleibt.
- Sub-Gruppen-IDs: `<gruppe>_<pick-shortnames>`; Anzeigename: `Ork Boy (Shoota)`.

Einheiten ohne `model_groups` ignorieren `group_loadouts`; `weapon_loadout` (oben) bleibt
der Mechanismus für homogene Einheiten mit Non-Default-Bewaffnung.

**Plan 013:** Einheiten ohne YAML-`model_groups` erhalten nach dem Roster-Load automatisch
eine synthetische Gruppe `ModelGroup(id="models", name_en=unit.name_en, count=models,
weapons=unit.weapons, priority=1)`. Damit läuft die gesamte Deklarations-UI über den
Gruppen-Flow — es gibt keinen Legacy-Pfad mehr. Die synthetische Gruppe darf NIE in YAML
auftauchen; `model_groups` mit nur einem Eintrag in `units.yaml` ablehnen.

---

## 3. Loader-Ablauf (Ziel 5c)

`load_army(faction_dir: str, roster_path: str | None = None) -> Army`

Roster-first: Das Roster wird zuerst geparst und validiert. Danach werden **nur** die im
Roster referenzierten Catalog-Einträge geladen — kein Full-Table-Scan.

```
1. Roster parsen (nur YAML-Load, kein Catalog-Zugriff)
   → Sammle alle referenzierten IDs:
     unit_ids, weapon_ids, wargear_ids, relic_ids, trait_ids, arkana_ids

2. Roster validieren (gegen army_rules.yaml + detachment_types.yaml)
   - Warlord hat NOBLE-Keyword?
   - Max. 1 Cryptek pro Dynasty-Detachment?
   - Protocol-Anzahl korrekt (5 von 6; 4 bei Szarekhan-Warlord-Trait)?
   - Slot-Constraints des Detachment-Typs eingehalten?
   - weapon_loadout-Auswahl in wargear_options der Einheit zulässig?
   → Fehler → Army.warnings (Liste sprechender Fehlermeldungen, kein hartes Sperren)
   → Unerwartete Fehler (z.B. fehlende Datei, ungültiges YAML) → LoaderError mit Debug-Info

3. Benötigten Catalog laden (nur referenzierte Einträge)
   ├── units.yaml          → nur unit_ids aus Roster
   └── weapons.yaml        → nur weapon_ids der geladenen Units + Roster-Auswahlen

4. Abilities laden
   ├── faction_abilities.yaml
   ├── unit_abilities.yaml
   ├── subfaction_abilities.yaml   (nur wenn subfaction gesetzt)
   ├── wargear_abilities.yaml      (nur für wargear_ids aus Roster)
   ├── powers.yaml                 (nur wenn Fraktion Psioniker hat; noch nicht verdrahtet)
   ├── _shared/stratagems.yaml     (immer; 7 Core Stratagems)
   └── <faction>/stratagems.yaml   (falls vorhanden)

5. Roster auf Units anwenden
   a. Modellanzahl aus Roster setzen
   b. weapon_loadout anwenden → Default-Waffen aus units.yaml ersetzen
   c. Weapon-Relic → Waffe in unit.weapons ersetzen (ersetzte Waffe wird entfernt)
   d. Wargear-Relic + Warlord Trait + Arkana → als Ability-Objekte laden,
      an unit.abilities hängen
   e. Warlord-Einheit markieren
   f. Command Protocols zuweisen (Necrons)

6. Nicht auflösbare Einheiten → Army.unmatched
7. Army-Objekt zurückgeben (keine ID-Referenzen, vollständig aufgelöst)
```

### Was der Loader **nicht** lädt

| Datei | Grund |
|-------|-------|
| `points.yaml` | Nur im Setup-Screen für Punkte-Validierung, nicht im Spiel |
| `power_level` (in units.yaml) | Nur im Setup-Screen (Open Play Balancing) |
| `relics.yaml` (komplett) | Nur der im Roster referenzierte Relic wird geladen |
| `warlord_traits.yaml` (komplett) | Nur der im Roster referenzierte Trait wird geladen |
| `arkana.yaml` (komplett) | Nur die im Roster referenzierten Arkana werden geladen |

---

## 4. YAML-Schema-Änderungen (Schritt 2)

### 4a. `weapons.yaml`

Alle Waffen auf `profiles:`-Liste umstellen:

```yaml
# Vorher (flach, zwei Objekte):
- id: wh40k_9e.necrons.weapon.staff_of_light_shooting
  weapon_type: Assault
  range_inches: 18
  attacks: "3"
  ...
- id: wh40k_9e.necrons.weapon.staff_of_light_melee
  weapon_type: Melee
  ...

# Nachher (ein Objekt, profiles-Liste):
- id: wh40k_9e.necrons.weapon.staff_of_light
  name_en: Staff of Light
  profiles:
    - name: Shooting
      weapon_type: Assault
      range_inches: 18
      attacks: "3"
      strength: "5"
      ap: "-2"
      damage: "1"
      abilities: ""
      is_melee: false
    - name: Melee
      weapon_type: Melee
      range_inches: 0
      attacks: "*"
      strength: "User"
      ap: "-2"
      damage: "1"
      abilities: ""
      is_melee: true
```

Single-Profile-Waffe (unveränderter Inhalt, nur in Liste verpackt):
```yaml
- id: wh40k_9e.necrons.weapon.gauss_flayer
  name_en: Gauss Flayer
  profiles:
    - name: ""
      weapon_type: Rapid Fire 1
      range_inches: 24
      attacks: "1"
      strength: "4"
      ap: "0"
      damage: "1"
      abilities: ""
      is_melee: false
```

`resurrection_orb` wird aus `weapons.yaml` entfernt (ist Wargear, kein Weapon).

### 4b. `units.yaml`

- `staff_of_light_shooting` / `staff_of_light_melee` → `staff_of_light`
- `wargear_options.add: wh40k_9e.necrons.weapon.resurrection_orb`
  → `wh40k_9e.necrons.wargear.resurrection_orb`

### 4c. `command_protocols.yaml`

IDs bekommen volles Namespace-Präfix:

```yaml
# Vorher:
- id: eternal_guardian

# Nachher:
- id: wh40k_9e.necrons.protocol.eternal_guardian
```

### 4d. `points.yaml`

Neuer Abschnitt für Arkana-Kosten (12 Einträge):

```yaml
arkana:
  wh40k_9e.necrons.arkana.failsafe_overcharger:        { points: 30 }
  wh40k_9e.necrons.arkana.countertemporal_nanomines:   { points: 30 }
  wh40k_9e.necrons.arkana.atavindicator:               { points: 25 }
  wh40k_9e.necrons.arkana.dimensional_sanctum:         { points: 15 }
  wh40k_9e.necrons.arkana.hypermaterial_ablator:       { points: 25 }
  wh40k_9e.necrons.arkana.cortical_subjugator_scarabs: { points: 15 }
  wh40k_9e.necrons.arkana.cryptogeometric_adjuster:    { points: 15 }
  wh40k_9e.necrons.arkana.metalodermal_tesla_weave:    { points: 20 }
  wh40k_9e.necrons.arkana.photonic_transubjector:      { points: 20 }
  wh40k_9e.necrons.arkana.phylacterine_hive:           { points: 20 }
  wh40k_9e.necrons.arkana.prismatic_obfuscatron:       { points: 20 }
  wh40k_9e.necrons.arkana.quantum_orb:                 { points: 20 }
```

`points_cost`-Felder aus `arkana.yaml` werden danach entfernt (Single Source of Truth).

### 4e. `wargear.yaml`

3 Einträge mit `is_relic: true` entfernen (Duplikation — Relics gehören nur in `relics.yaml`):
- `wh40k_9e.necrons.wargear.orb_of_eternity`
- `wh40k_9e.necrons.wargear.nanoscarab_casket`
- `wh40k_9e.necrons.wargear.veil_of_darkness`

### 4f. `wargear_abilities.yaml`

3 Relic-Ability-Einträge entfernen (aus der Duplikation entstanden):
- `necrons.wargear.orb_of_eternity.ability`
- `necrons.wargear.nanoscarab_casket.ability`
- `necrons.wargear.veil_of_darkness.ability`

---

## 5. Betroffene Dateien (Zusammenfassung)

| Datei | Aktion |
|-------|--------|
| `docs/spec/loader_contract.md` | Diese Datei (neu) |
| `docs/spec/army_builder.md` | Weapon-Schema, Roster-Format, Loader-Ablauf aktualisieren |
| `data/wh40k_9e/necrons/weapons.yaml` | Alle Waffen → `profiles:`-Liste; `resurrection_orb` entfernen |
| `data/wh40k_9e/necrons/units.yaml` | Waffen-Refs anpassen; resurrection_orb → wargear-Namespace |
| `data/wh40k_9e/necrons/command_protocols.yaml` | IDs → volles Namespace-Präfix |
| `data/wh40k_9e/necrons/points.yaml` | `arkana:`-Abschnitt ergänzen |
| `data/wh40k_9e/necrons/arkana.yaml` | `points_cost`-Felder entfernen |
| `data/wh40k_9e/necrons/wargear.yaml` | 3 Relic-Einträge entfernen |
| `data/wh40k_9e/necrons/wargear_abilities.yaml` | 3 Relic-Ability-Einträge entfernen |
| `src/gameObjects/weapon.py` | Dataclass auf `profiles: list[WeaponProfile]` umstellen |
| `src/gameObjects/loader.py` | `_weapon_from_dict` → Profile-Parsing; neue load-Funktionen |

---

## 6. Offene Fragen

| # | Frage | Impact |
|---|-------|--------|
| 1 | `Unit`-Dataclass: Braucht es ein `weapon_groups: list[WeaponGroup]`-Feld für gemischte Einheiten-Bewaffnung, oder reicht die flache `weapons: list[Weapon]`-Liste mit Combat-System-seitiger Auswahl? | `unit.py`, `fightPhase.py`, `shootingPhase.py` |
| 2 | Roster ohne Catalog (`roster_path` gesetzt, aber unit_id nicht in units.yaml): `Army.unmatched` + Warnung oder `LoaderError`? | `load_army()` API |

---

## 7. Verbindung zum Army Builder (Ziel 5d)

Dieser Loader-Vertrag ist die Grundlage für den Army Builder (Ziel 5d):

- Der Army Builder erzeugt ein regelkonformes Roster (YAML) und übergibt es an `load_army()`
- Alternativ: BattleScribe-Import (`tools/import_rosz.py`) erzeugt ein Roster, `load_army()` lädt es
- Roster-Validierung (Schritt 2 oben) ist damit auch die Validierung des Army Builders

Der Loader selbst kennt keinen Army-Builder-Kontext — er nimmt ein Roster und gibt ein `Army`-Objekt zurück. Ob das Roster vom Builder, vom Import oder manuell erstellt wurde, ist irrelevant.

---

## 8. camelCase-Migration (Grundlage, S148 Brief 7)

<!-- Reine Migrationsgrundlage — kein Code-/YAML-Change. Quellen: S147-Audits
     `docs/handoff/S147_go_audit_stratagems.md` §3, `S147_go_audit_necron_abilities.md` §5,
     `S147_go_audit_ork_abilities.md` (snake_case-Inventar). Die eigentliche Feld-Umbenennung
     ist ein eigener S149+-Task (s. `docs/goals/backlog.md` §2), nicht Teil dieses Abschnitts. -->

Alle drei GO-Audit-Kataloge aus S147 haben unabhängig voneinander bestätigt: die Effect-/
Ability-/Stratagem-YAMLs sind **durchgängig snake_case**. `grantsKeyword` (S148 Brief 4,
`weapons.yaml`/`relics.yaml`) ist das **erste real existierende camelCase-Feld** in diesem
Bereich — ein bewusster, vom Stakeholder freigegebener Bruch mit der sonst einheitlichen
Konvention. Bevor ein automatisiertes Such-&-Ersetzen auf camelCase umstellt, müssen drei
Namenskollisionen aufgelöst werden — ein naives Rename würde die Mehrdeutigkeit sonst 1:1
ins neue Schema übertragen.

### 8.1 Kollisionsauflösung

**(a) `modifier` — überladenster Einzelbefund.** Der Key `modifier` wird für zwei völlig
verschiedene Dinge verwendet, ausschließlich in `stratagems.yaml` (`_shared`/`necrons`/`orks`,
20 Fundstellen: 13 Necrons + 7 Orks; Verifikation `grep -n "modifier:" data/wh40k_9e/{necrons,orks,_shared}/stratagems.yaml`
bestätigt 13 int-Leaf- und 7 Block-Vorkommen):

- **int-Leaf unter `effect:`** (z. B. `effect.modifier: 6` bei Disintegration Capacitors) —
  ein einzelner Zahlenwert, Teil des Effekt-Payloads. → **`effectModifierValue`**
  (Audit-Vorschlag übernommen).
- **eigener Mapping-Block auf Top-Level** (`modifier: {roll_type, value, target, expires_at,
  source_label}`, das `StratagemModifier`-Schema, das über `spend_stratagem` in
  `active_modifiers` landet). → **`attackModifier`** (Audit-Vorschlag übernommen).

  In `unit_abilities.yaml`/`faction_abilities.yaml`/`subfaction_abilities.yaml`/`wargear.yaml`
  (Necron-Ability-Scope, 22 Fundstellen) kommt `modifier` **nur** als int-Leaf unter `effect:`
  vor — der Top-Level-Block existiert dort nicht (Abilities nutzen `active_modifiers`/
  `StratagemModifier` nicht). Dort gilt daher einheitlich `effectModifierValue`, ohne
  Block-Gegenstück.

**(b) `target` — Rollenkollision, nur in `stratagems.yaml`.** `effect.target` (10
Fundstellen) beschreibt **wen** der Effekt grob betrifft (Werte u. a. `selected_unit`,
`self`, `friendly_core_aura`, `enemy`, aber auch `attacker`/`defender`, verifiziert per
`grep -n "target:" data/wh40k_9e/{necrons,orks,_shared}/stratagems.yaml`); `modifier.target`
(dieselbe Fundstellenzahl, da 1:1 mit dem `modifier`-Block) beschreibt ausschließlich die
Rolle in der Roll-Pipeline (`_collect_atk_modifiers`, nur `attacker`/`defender`). Da (a) den
Top-Level-Block bereits auf `attackModifier` umbenennt, ist `attackModifier.target` durch den
Elternpfad bereits eindeutig — eine reine Struktur-Trennung reicht dafür. Damit die beiden
Felder aber auch **flach** (bare key, z. B. bei generischen Lookup-Helfern oder
Dokumentations-Greps) nie verwechselt werden, wird zusätzlich `effect.target` auf
**`effectTarget`** umbenannt. Ergebnis nach Migration: `effectTarget` (Effekt-Empfänger,
mehrwertig) vs. `attackModifier.target` (Roll-Pipeline-Rolle, nur `attacker`/`defender`) —
strukturell UND namentlich getrennt.

  Im Necron-Ability-Scope kommt `target` (69 Fundstellen) ausschließlich unter `effect:` vor
  (kein Top-Level-`modifier`-Block, s. (a)) — dort ist `target` kein Kollisionsfall, sondern
  einheitlich `effectTarget` wie oben.

**(c) `target_keyword` (Singular) vs. `target_keywords` (Plural) — Inkonsistenz, unabhängig
von camelCase.** Mehrheitsform ist Plural (`target_keywords`, u. a. 7× Necron-Ability-Scope,
weitere Treffer `necrons/faction_abilities.yaml`, `orks/faction_abilities.yaml`). Singular
kommt **zweimal** vor — verifiziert per `grep -rn "target_keyword:" data/wh40k_9e/`:
`orks/unit_abilities.yaml:622` (`target_keyword: [VEHICLE, MONSTER]`, Beast Snagga) **und**
zusätzlich `adeptus_custodes/faction_abilities.yaml:96` (nicht Teil der 3 S147-Audits, beim
Verifizieren dieses Briefs mitgefunden — reine Bestandsaufnahme, kein Custodes-Scope-Wechsel).
Beide Singular-Stellen tragen bereits eine **Liste** als Wert — der Feldname ist der einzige
Fehler, kein Schemafehler. Auflösung: künftig einheitlich `targetKeywords` (Plural-Form,
camelCase), Singular-Stellen bekommen bei der eigentlichen Migration denselben Key.

### 8.2 Vollständige Mapping-Tabelle

Union aller Feldnamen aus den 3 Inventaren (Stratagems `_shared`+`necrons`+`orks`,
Necron-Ability-Scope 6 Dateien, Ork-Ability-Scope 5 Dateien), ohne die drei oben aufgelösten
Kollisionsfelder (separat behandelt) und ohne `id` (Dotted-Namespace-Identifier, kein
Feldname i. e. S., kein Rename-Kandidat — 64/91/… Fundstellen, konsistent in allen 3 Audits
als Ausnahme markiert). **107 verbleibende Felder**, mechanische snake_case→camelCase-Regel
(erstes Wort klein, jedes weitere Wort groß, Unterstriche entfernt):

| alt (snake_case) | neu (camelCase) |
|---|---|
| `abilities` | `abilities` |
| `abilities_en` | `abilitiesEn` |
| `ability_en` | `abilityEn` |
| `ability_id` | `abilityId` |
| `ability_type` | `abilityType` |
| `active_text` | `activeText` |
| `affects` | `affects` |
| `amount` | `amount` |
| `any_of` | `anyOf` |
| `aoe_radius_inches` | `aoeRadiusInches` |
| `applies_to` | `appliesTo` |
| `applies_when` | `appliesWhen` |
| `arkana` | `arkana` |
| `badge_label` | `badgeLabel` |
| `bonus` | `bonus` |
| `bonus_amount` | `bonusAmount` |
| `bonus_vs_character` | `bonusVsCharacter` |
| `category` | `category` |
| `condition` | `condition` |
| `condition_prompt` | `conditionPrompt` |
| `conditions` | `conditions` |
| `cost_pts` | `costPts` |
| `cover_type` | `coverType` |
| `cp_cost` | `cpCost` |
| `damage` | `damage` |
| `detachment` | `detachment` |
| `did_not_move` | `didNotMove` |
| `directives` | `directives` |
| `effect` | `effect` |
| `effects` | `effects` |
| `enforcement` | `enforcement` |
| `event` | `event` |
| `except_strength_ge` | `exceptStrengthGe` |
| `expires_at` | `expiresAt` |
| `extra_uses` | `extraUses` |
| `faction` | `faction` |
| `grants_ability` | `grantsAbility` |
| `handler` | `handler` |
| `hit_modifier` | `hitModifier` |
| `invuln_save` | `invulnSave` |
| `is_relic` | `isRelic` |
| `keyword` | `keyword` |
| `keywords` | `keywords` |
| `klan_keyword` | `klanKeyword` |
| `max` | `max` |
| `min_distance_from_enemy` | `minDistanceFromEnemy` |
| `min_range_from_enemy` | `minRangeFromEnemy` |
| `modifies_ability` | `modifiesAbility` |
| `mortal_dice` | `mortalDice` |
| `name_en` | `nameEn` |
| `nearby_friendly_above_half` | `nearbyFriendlyAboveHalf` |
| `needs_healing` | `needsHealing` |
| `once_per_battle` | `oncePerBattle` |
| `once_per_phase` | `oncePerPhase` |
| `persistent_effects` | `persistentEffects` |
| `phase` | `phase` |
| `player` | `player` |
| `power_delta` | `powerDelta` |
| `power_list` | `powerList` |
| `powers_per_turn` | `powersPerTurn` |
| `primary` | `primary` |
| `profiles` | `profiles` |
| `prompt_text` | `promptText` |
| `range_inches` | `rangeInches` |
| `ranged_only` | `rangedOnly` |
| `remove` | `remove` |
| `replaces` | `replaces` |
| `reroll` | `reroll` |
| `restriction` | `restriction` |
| `revive` | `revive` |
| `roll` | `roll` |
| `roll_threshold` | `rollThreshold` |
| `roll_type` | `rollType` |
| `round_choice_label` | `roundChoiceLabel` |
| `rule_text` | `ruleText` |
| `secondary` | `secondary` |
| `selector_label` | `selectorLabel` |
| `set_damage_to` | `setDamageTo` |
| `shared_ref` | `sharedRef` |
| `source` | `source` |
| `source_label` | `sourceLabel` |
| `stage` | `stage` |
| `stat` | `stat` |
| `strength` | `strength` |
| `subfaction_affinity` | `subfactionAffinity` |
| `subfaction_field` | `subfactionField` |
| `subfaction_label` | `subfactionLabel` |
| `subfactions` | `subfactions` |
| `success_on` | `successOn` |
| `target_keywords` | `targetKeywords` |
| `target_keywords_any` | `targetKeywordsAny` |
| `target_rule` | `targetRule` |
| `text_de` | `textDe` |
| `threshold` | `threshold` |
| `timing` | `timing` |
| `trigger` | `trigger` |
| `triggered_effects` | `triggeredEffects` |
| `type` | `type` |
| `unit_id` | `unitId` |
| `unit_not_destroyed` | `unitNotDestroyed` |
| `value` | `value` |
| `waaagh_called_this_turn` | `waaaghCalledThisTurn` |
| `weapon` | `weapon` |
| `weapon_type` | `weaponType` |
| `weapon_types` | `weaponTypes` |
| `within_inches` | `withinInches` |
| `wounds` | `wounds` |

Die drei Kollisionsfelder aus 8.1 ergänzen die Tabelle:

| alt (snake_case) | neu (camelCase) | Kontext |
|---|---|---|
| `effect.modifier` (int-Leaf) | `effectModifierValue` | Stratagems + Abilities |
| `modifier` (Top-Level-Block) | `attackModifier` | nur Stratagems |
| `effect.target` | `effectTarget` | Stratagems + Abilities |
| `modifier.target` | `attackModifier.target` (unverändert, durch Elternpfad disambiguiert) | nur Stratagems |
| `target_keyword` (Singular) | `targetKeywords` (vereinheitlicht mit Plural) | Ork-Ability-Scope + Custodes (Zusatzfund) |

`grantsKeyword` selbst braucht keine Migration — es ist bereits camelCase (S148 Brief 4).

### 8.3 Nicht Teil dieses Abschnitts

Die eigentliche Feld-Umbenennung in YAML + Loader-Code ist **kein** S148-Scope (Aufwand
größer als Effort M — drei Dateien-Cluster, Kollisionsauflösung zuerst nötig). Sie ist als
eigener, in Teil-Briefs ≤ M geschnittener Task für S149+ vorgesehen, s.
`docs/goals/backlog.md` §2. Ein sinnvoller Schnitt entlang der Cluster: (1) Stratagems
`modifier`/`target`-Kollision zuerst (höchstes Risiko bei naivem Rename), (2) restliche
Stratagem-Felder, (3) Necron-Ability-Scope (6 Dateien), (4) Ork-Ability-Scope (5 Dateien)
inklusive `target_keyword`-Bereinigung und Custodes-Zusatzfund.
