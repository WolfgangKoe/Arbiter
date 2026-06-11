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
