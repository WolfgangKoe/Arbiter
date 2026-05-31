# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session gemacht wurde

- Orphaned Dateien gelöscht: `faction_properties.yaml`, `subfaction_properties.yaml`, `fallback_weapon_profiles.yaml`, `faction_property.py`, Compat-Shim in `loader.py`
- `command_protocols.yaml`: 6. Protokoll hinzugefügt (Vengeful Stars)
- `subfaction_abilities.yaml`: Alle 6 Dynastien mit structured abilities (Mephrit, Nihilakh, Novokh, Sautekh, Szarekhan)
- `relics.yaml`: Schema-Alignment (range_inches, weapon_type, strength als Standardfelder; ability_en ergänzt)

---

## Aktueller Status Necrons-Datensatz

| Datei | Status |
|-------|--------|
| `units.yaml` | ✅ 46 Einheiten, verifiziert |
| `stratagems.yaml` | ✅ 59 Stratagems, verifiziert |
| `faction_abilities.yaml` | ✅ 7 structured abilities |
| `unit_abilities.yaml` | ✅ 8 structured abilities |
| `wargear_abilities.yaml` | ✅ 9 structured abilities — **3 fehlen noch (Relikt-Wargear)** |
| `wargear.yaml` | ✅ 10 items — **3 fehlen noch (Relikt-Wargear)** |
| `subfaction_abilities.yaml` | ✅ Alle 6 Dynastien |
| `command_protocols.yaml` | ✅ Alle 6 Protokolle |
| `warlord_traits.yaml` | ✅ 13 Traits |
| `arkana.yaml` | ✅ 12 Cryptek-Arkana |
| `relics.yaml` | ✅ Schema OK — Regeltexte brauchen Wahapedia-Verifikation (siehe unten) |
| `weapons.yaml` | ⚠️ 90 Waffen — Gauntlet stats falsch, 2 Relic-Waffen fehlen, abilities-Texte teils paraphrasiert statt wörtlich |
| `weapon_abilities.yaml` | ❌ Fehlt komplett (neue Datei) |

---

## Nächste Aufgabe: Necrons-Datensatz abschließen (4 Teile)

**Wichtig:** In dieser Reihenfolge abarbeiten. Kein Loader (Ziel 5c) bis alles abgeschlossen.

---

### Teil A — weapons.yaml: Korrekturen + Relic-Waffen

**Schritt 1:** Einmal komplett `weapons.yaml` lesen.

**Schritt 2:** Gauntlet of the Conflagrator korrigieren (aktuell falsch):

```yaml
# FALSCH (aktuell):
weapon_type: Assault
attacks: "D6"
strength: "5"
ap: "0"
damage: "1"

# RICHTIG (Wahapedia):
weapon_type: Pistol 1
attacks: "1"
strength: "*"      # auto-trifft, Verwundungswurf ersetzt
ap: "*"
damage: "*"
abilities: "Each time an attack is made with this weapon, that attack automatically hits its target. Instead of making a wound roll, roll one D6 for each model in the target unit; that unit suffers 1 mortal wound for each result of 6, and the attack sequence ends."
```

**Schritt 3:** Voltaic Staff hinzufügen (Wahapedia-verifiziert):
```yaml
# Shooting profile
id: wh40k_9e.necrons.weapon.voltaic_staff_shooting
weapon_type: Assault 4 / range_inches: 18 / S:6 / AP:-2 / D:2
abilities: "Each time an attack is made with this weapon, an unmodified hit roll of 6 scores 2 additional hits."
is_relic: true

# Melee profile  
id: wh40k_9e.necrons.weapon.voltaic_staff_melee
weapon_type: Melee / range_inches: 0 / S: User+1 / AP:-2 / D:2
abilities: ""
is_relic: true
```

**Schritt 4:** Voidreaper hinzufügen (Wahapedia-verifiziert):
```yaml
id: wh40k_9e.necrons.weapon.voidreaper
weapon_type: Melee / range_inches: 0 / S: User+2 / AP:-4 / D:3
abilities: "Each time an attack is made with this weapon, rules that ignore wounds cannot be used."
is_relic: true
```

**Schritt 5:** Alle 37 weapons mit nicht-leeren abilities auf Wahapedia-Wortlaut prüfen.
Wichtige Korrekturen (aus Wahapedia-Check dieser Session):
- Synaptic Disintegrator: `"Each time you select a target for this weapon, you can ignore the Look Out, Sir rule. Each time an attack is made with this weapon, an unmodified wound roll of 6 inflicts 1 mortal wound on the target in addition to any normal damage."` (aktueller Text ist kürzer)
- Tesla-Waffen: Wortlaut ✅ bereits korrekt
- Blast: Kein eigener per-Waffe Text — "Blast." genügt als Marker (Core Rule)
- Gauss-Waffen: haben KEIN abilities-Feld (Gauss-Bonus kommt nur via Stratagem Disintegration Capacitors)

---

### Teil B — weapon_abilities.yaml (neue Datei)

Neue Datei: `data/wh40k_9e/necrons/weapon_abilities.yaml`
Schema: identisch mit `wargear_abilities.yaml` (trigger/effect/conditions), aber `source: weapon_ability` und `weapon_id:`.

**Ability-Gruppen** (aus grep-Analyse, 37 Einträge total):

| Ability-Typ | Anzahl Waffen | Beispiel |
|-------------|---------------|---------|
| `tesla` — unmod. 6 → 2 extra hits | 5 | Tesla Carbine |
| `extra_attacks_N` — bearer fights = +N attacks | 6 | verschiedene Nahkampf |
| `blast` | 7 | Particle Whip, Exile Cannon |
| `invuln_bypass` — no invuln saves | 4 | C'tan weapons |
| `auto_hit` | 2 | Heat Ray dispersed, Gauntlet |
| `half_range_bonus` | 1 | Heat Ray focused |
| `unique` (keine Gruppe) | 12 | Tachyon Arrow, Synaptic Dis. etc. |

**Vorgehen:** Datei einmalig komplett schreiben — eine Ability-Gruppe nach der anderen, ohne Zwischenkontrollen.

---

### Teil C — wargear.yaml: 3 Relic-Wargear ergänzen

```yaml
# Orb of Eternity (replaces Resurrection Orb)
id: wh40k_9e.necrons.wargear.orb_of_eternity
is_relic: true
replaces: wh40k_9e.necrons.wargear.resurrection_orb
ability_en: "Once per battle, in your Command phase, the bearer can use its Orb of Eternity. Select one friendly <DYNASTY> unit within 6\" not at Starting Strength and not yet enacted this phase. That unit's reanimation protocols are enacted, and add 1 to each Reanimation Protocol roll."

# Nanoscarab Casket (standalone, TECHNOMANCER only)
id: wh40k_9e.necrons.wargear.nanoscarab_casket
is_relic: true
# Wahapedia-Text (verifiziert): Living Metal +1 wound — ACHTUNG: Wahapedia-Agent meldete
# abweichenden Text (Rites of Reanimation). User soll gegen Codex S.66 prüfen.
# Deutschen Text aus user-Bild: "Jedes Mal, wenn der Träger seine Fähigkeit Lebendes Metall
# einsetzt, erhält er 1 zusätzlichen verlorenen Lebenspunkt zurück."
ability_en: "Each time the bearer uses its Living Metal ability, it regains 1 additional lost wound."

# Veil of Darkness (standalone, NOBLE only)
id: wh40k_9e.necrons.wargear.veil_of_darkness
is_relic: true
ability_en: "Once per battle, in your Movement phase, the bearer can use this Relic. Remove the bearer's unit and up to one friendly <DYNASTY> CORE unit within 3\" and set them up anywhere on the battlefield more than 9\" from any enemy models. If two units are set up, both must be set up wholly within 6\" of each other."
```

---

### Teil D — wargear_abilities.yaml: 3 Relic-Abilities

Für jede der 3 neuen wargear-Einträge einen structured ability-Eintrag nach bestehendem Schema (trigger/effect/conditions). Angelehnt an bestehende `resurrection_orb`-Ability für Orb of Eternity.

---

### Teil E — relics.yaml: Wahapedia-Verifikation

- **Nanoscarab Casket**: Agentur meldete anderen Text als im Codex-Bild. User prüft gegen Codex S.66.
- **Voidreaper abilities text**: Wahapedia sagt `"Each time an attack is made with this weapon, rules that ignore wounds cannot be used."` — aktuell in relics.yaml steht `"Abilities that ignore the loss of wounds cannot be used..."` → anpassen
- **Gauntlet of the Conflagrator**: Stats in `relics.yaml` sind korrekt (Pistol 1, range 12"), aber in `weapons.yaml` noch falsch (Teil A, Schritt 2)

---

## Nächster Schritt nach Abschluss dieser Aufgabe

→ **Ziel 5b.6 — Army Building Rules** (vollständig/Option c)  
→ danach **Ziel 5c — Loader Refactoring**

---

## Architektur-Kurzreferenz

```
src/gameObjects/loader.py     ← aktiv, lädt army.yaml (bis Ziel 5c)
data/wh40k_9e/necrons/        ← alle Necron-Daten
data/wh40k_9e/_shared/        ← detachment_types.yaml
```

## Wichtige Constraints
- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts
- dev-Branch — kein direktes Committen auf main
- **Kein Loader bis Datensatz vollständig korrekt!**
