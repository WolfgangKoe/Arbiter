# Army Builder — Spec

> Ziel 5a. Bezieht sich auf BattleScribe-Import (Ziel 5d) und Katalog-Aufbau (Ziel 5b).

---

## Überblick: Zwei-Quellen-Strategie

| Quelle | Inhalt | Speicherort |
|--------|--------|-------------|
| **Wahapedia** | Vollständige Statlines, Waffenprofile, Stratagems, Abilities | `data/wh40k_9e/<fraktion>/` |
| **BattleScribe** (`.rosz`) | Einheitenauswahl + Modellanzahl für ein konkretes Spiel | `data/rosters/` |

Der Roster referenziert nur Katalog-IDs. Statlines werden zur Laufzeit aus dem Katalog geladen — keine Stat-Duplikation im Roster.

---

## Katalog-Schema

### Verzeichnisstruktur pro Fraktion

```
data/wh40k_9e/<fraktion>/
  units.yaml              ← alle Einheiten-Statlines (vollständig)
  weapons.yaml            ← alle Waffenprofile
  stratagems.yaml         ← alle Stratagems (CP-Kosten, Phase, Bedingungen)
  abilities.yaml          ← Faction Abilities (mechanisch verdrahtet)
  command_protocols.yaml  ← nur Necrons: Kommandoprotokolle ✅ vorhanden
```

### `units.yaml` — Einheitenformat

```yaml
- id: wh40k_9e.necrons.unit.warriors
  name_en: Necron Warriors
  name_de: Nekron-Krieger
  battlefield_role: [Troops]
  keywords: [Infantry, Necrons, Core, Living Metal, Warrior]
  wounds: 1
  models_min: 10
  models_max: 20
  move: "6"
  ws: "4+"
  bs: "3+"
  strength: 4
  toughness: 4
  save: "4+"
  invuln_save: null
  leadership: 10
  weapons:
    - ref: wh40k_9e.necrons.weapon.gauss_flayer
    - ref: wh40k_9e.necrons.weapon.gauss_reaper
```

Alle Stat-Werte als `str` für Werte wie `"3+"`, `"*"`, `"N/A"`.
`weapons` enthält nur Referenzen (IDs) — der Loader löst sie auf.

### `weapons.yaml` — Waffenprofil-Format

```yaml
- id: wh40k_9e.necrons.weapon.gauss_flayer
  name_en: Gauss Flayer
  weapon_type: Rapid Fire 1
  range_inches: 24
  attacks: "1"
  strength: 4
  ap: "0"
  damage: "1"
  abilities: []
  is_melee: false

- id: wh40k_9e.necrons.weapon.close_combat_weapon
  name_en: Close Combat Weapon
  weapon_type: Melee
  range_inches: 0
  attacks: "1"
  strength: "User"
  ap: "0"
  damage: "1"
  abilities: []
  is_melee: true
```

**Wichtig:** Jede Einheit, die keine explizite Nahkampfwaffe hat, erhält automatisch `Close Combat Weapon` als Default. Der Loader ergänzt diese Waffe beim Laden.

### `stratagems.yaml` — Stratagem-Format

```yaml
- id: wh40k_9e.necrons.stratagem.disruption_fields
  name_en: Disruption Fields
  cp_cost: 1
  phase: fight
  stage: active
  player: active
  conditions: [Necrons, Core]
  rule_text: "Use when a CORE unit from your army is chosen to fight. Until the end of the phase, each time a model in that unit makes an attack, an unmodified hit roll of 6 scores 1 additional hit."
  once_per_phase: true
```

### `abilities.yaml` — Faction Ability Format

```yaml
- id: wh40k_9e.necrons.ability.living_metal
  name_en: Living Metal
  triggers_phase: command
  triggers_stage: start
  affects_parameter: wounds
  ability_keyword: livingMetal
  rule_text: "At the start of your Command phase, each NECRONS unit with this ability recovers 1 lost wound."
  applies_to_keyword: Living Metal
```

---

## Roster-Format

### Verzeichnis

```
data/rosters/
  <spieler>_<fraktion>_<datum>.yaml   ← z.B. player1_necrons_2026-05-30.yaml
```

### Roster-Datei-Schema

```yaml
roster_id: player1_necrons_2026-05-30
faction: necrons
subfaction: Szarekhan
game_size: strike_force
points_limit: 1000
battle_forged: true
created: 2026-05-30

detachments:
  - detachment_type: patrol
    name: Patrol Detachment
    units:
      - unit_id: wh40k_9e.necrons.unit.overlord
        models: 1
        warlord: true
        wargear: []
      - unit_id: wh40k_9e.necrons.unit.warriors
        models: 10
        wargear:
          - slot: primary_weapon
            weapon_id: wh40k_9e.necrons.weapon.gauss_flayer

unmatched:
  - name: "Doom Scythe"
    source: battlescribe
    note: "Not yet in catalog — add to units.yaml"
```

`unmatched` enthält Einheiten aus dem BattleScribe-Import, die keiner Katalog-ID zugeordnet werden konnten. Sie werden im UI markiert und nicht geladen.

---

## Loader-Vertrag

`gameObjects/loader.py` ist der einzige Zugangspunkt für YAML-Daten. Kein anderes Modul liest YAML direkt.

### Eingabe

```python
load_army(faction: str, roster_path: str | None = None) -> Army
```

- `faction`: Fraktion-Slug (z.B. `"necrons"`)
- `roster_path`: Pfad zur Roster-YAML (optional — ohne Roster werden alle Katalog-Einheiten geladen)

### Ausgabe

```python
@dataclass
class Army:
    faction: str
    subfaction: str | None
    battle_forged: bool
    detachments: list[Detachment]
    faction_properties: list[FactionProperty]
    subfaction_properties: list[FactionProperty]
    stratagems: list[Stratagem]
    unmatched: list[str]            # Namen nicht aufgelöster Einheiten
```

### Auflösungsreihenfolge

1. Lade `units.yaml` und `weapons.yaml` der Fraktion
2. Wenn Roster vorhanden: filtere nach Roster-Einheiten, setze `models`-Wert aus Roster
3. Ergänze fehlende `Close Combat Weapon` bei Einheiten ohne Nahkampfwaffe
4. Löse `weapon_id`-Referenzen auf (keine ID-Strings im Laufzeit-Objekt)
5. Lade `stratagems.yaml` und `abilities.yaml`
6. Sammle nicht auflösbare Einheiten in `unmatched`

### Unmatched-Handling

- Unbekannte Einheiten aus BattleScribe werden **nicht** übersprungen, sondern in `Army.unmatched` gesammelt
- Der Setup-Screen zeigt eine Warnung mit allen unmatched Einheiten
- Die Partie kann trotzdem gestartet werden (unmatched Einheiten fehlen dann im Spiel)

---

## BattleScribe-Import (Ziel 5d)

```
tools/import_rosz.py <pfad>.rosz [--faction necrons] [--output data/rosters/]
```

### Verarbeitungsschritte

1. `.rosz` entpacken (ZIP → `.ros`-Datei)
2. XML parsen (`xml.etree.ElementTree`, Namespace `http://www.battlescribe.net/schema/rosterSchema`)
3. Einheiten + Modellanzahl extrahieren
4. Waffenauswahl aus `selection`-Elementen lesen
5. Faction-Matching: BS-Einheitennamen → Katalog-IDs (fuzzy match + manuelle Mapping-Tabelle)
6. Roster-YAML schreiben; unbekannte Einheiten in `unmatched`

### Waffenprofile aus BattleScribe

BS-Waffendaten (Typ-String `"Rapid Fire 2"` → attacks=2) werden **nicht** direkt übernommen.
Der Importer schreibt nur Weapon-IDs; Statlines kommen aus dem Katalog.
Ausnahme: `wargear`-Slot-Zuordnung wird aus BS übernommen.

---

## Offene Fragen (Ziel 5)

| # | Frage | Impact |
|---|-------|--------|
| 1 | Wie genau ist das BS-Mapping (Name → Katalog-ID)? Gibt es Namensabweichungen? | import_rosz.py |
| 2 | Soll `invuln_save` aus Ability-Text per Regex oder als Pflichtfeld? | units.yaml Schema |
| 3 | Mehrere Detachments pro Roster — UI für Detachment-Auswahl? | setup screen |
| 4 | P1 wählt Roster → Roster für P2 sperren? Oder beide gleichzeitig? | setup flow |
