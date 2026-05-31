# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Aktueller Status Necrons-Datensatz

Der Datensatz ist **NICHT vollständig** — folgende Lücken wurden identifiziert:

| Datei | Status |
|-------|--------|
| `units.yaml` | ⚠️ 46 Einheiten, aber 5 fehlen; Triarch Stalker falsche Role; kein PL; keine Brackets |
| `stratagems.yaml` | ✅ 59 Stratagems |
| `faction_abilities.yaml` | ✅ 7 abilities |
| `unit_abilities.yaml` | ⚠️ 8 abilities — ~10 neue für fehlende Einheiten nötig |
| `wargear_abilities.yaml` | ✅ 12 abilities |
| `wargear.yaml` | ✅ 13 Items |
| `subfaction_abilities.yaml` | ✅ 6 Dynastien |
| `command_protocols.yaml` | ✅ 6 Protokolle |
| `warlord_traits.yaml` | ✅ 13 Traits |
| `arkana.yaml` | ✅ 12 Cryptek-Arkana |
| `relics.yaml` | ✅ 6 Relikte |
| `weapons.yaml` | ⚠️ 93 Waffen — 4 neue nötig für fehlende Einheiten |
| `weapon_abilities.yaml` | ✅ 44 abilities |
| `army_rules.yaml` | ✅ Armeebau-Regeln |
| `points.yaml` | ❌ Fehlt komplett (neue Datei) |

---

## Plan: Was zu tun ist

### Schritt 1 — Datenbeschaffung (Subagent, parallel)
Alle fehlenden Werte von Wahapedia holen:
- PL für alle 46 bestehenden Einheiten
- Punktwerte für alle 46 bestehenden Einheiten
- Fehlende Brackets: Canoptek Doomstalker, Ghost Ark, Night Scythe, Doom Scythe, Tesseract Vault
- Fehlende Daten für neue Einheiten: Canoptek Plasmacyte (PL + Punkte), Hexmark Destroyer (PL)

URL-Pattern: `https://wahapedia.ru/wh40k9ed/factions/necrons/{Unit-Slug}`

---

### Schritt 2 — `weapons.yaml`: 4 neue Waffen

| Waffe | Einheit | Stats |
|-------|---------|-------|
| `transdimensional_abductor` | Convergence of Dominion | Assault D3, 12", S4, AP-3, D3 |
| `monomolecular_proboscis` | Canoptek Plasmacyte | Melee, User, AP-1, D1 |
| `enmitic_disintegrator_pistol` | Hexmark Destroyer | Pistol 1, 18", S6, AP-1, D1 |
| `crackling_tendrils` | Transcendent C'tan | Melee, User, AP-4, D D6 |

`tesla_sphere` existiert bereits (Tesseract Vault) → für Obelisk wiederverwenden.

---

### Schritt 3 — `unit_abilities.yaml`: neue Abilities

Neue Ability-IDs für neue Einheiten:
- **Convergence of Dominion:** `dominionProtocols`, `dynasticCommandNode`, `translocationProtocols`
- **Canoptek Plasmacyte:** `viralConstruct`, `evasionProtocol`, `infusedMadness`
- **Hexmark Destroyer:** `inescapableDeath`, `multiThreatEliminator`
- **Transcendent C'tan:** `enslavedStarGod`, `realityUnravels`, `fracturedPersonality`
- **Obelisk:** `hoveringSentinel`, `gravityPulse`

---

### Schritt 4 — `units.yaml`: vier Änderungsblöcke

#### 4a. `power_level` zu allen 46 Einheiten inline ergänzen
```yaml
power_level: 11   # bei models_min; Loader skaliert proportional
```

#### 4b. Battlefield Role Triarch Stalker korrigieren
```yaml
# ALT:
battlefield_role: [Heavy Support]
# NEU:
battlefield_role: [Elites]
```
Bestätigt durch Wahapedia-Datenblatt und Screenshot.

#### 4c. `damage_bracket` zu 10 Einheiten ergänzen (wounds > 9)

| Einheit | W | Brackets | Degradiert |
|---------|---|----------|------------|
| Triarch Stalker | 12 | 7-12 / 4-6 / 1-3 | M, WS, BS |
| Canoptek Doomstalker | 12 | noch fetchen | — |
| Ghost Ark | 14 | noch fetchen | — |
| Doomsday Ark | 14 | 8-14 / 4-7 / 1-3 | M, BS, A |
| Night Scythe | 12 | noch fetchen | — |
| Doom Scythe | 12 | noch fetchen | — |
| Obelisk | 28 | 15-28 / 8-14 / 1-7 | M, BS, A |
| The Silent King | 16 | 9-16 / 5-8 / 1-4 | M, A |
| Monolith | 24 | 13-24 / 7-12 / 1-6 | M, BS, A |
| Tesseract Vault | 30 | noch fetchen | — |

Format:
```yaml
damage_bracket:
  - wounds_min: 7
    wounds_max: 12
    move: "10\""
    ws: "3+"
    bs: "3+"
    attacks: 3
  - wounds_min: 4
    wounds_max: 6
    move: "8\""
    ws: "4+"
    bs: "4+"
    attacks: 3
  - wounds_min: 1
    wounds_max: 3
    move: "6\""
    ws: "5+"
    bs: "5+"
    attacks: 3
```

#### 4d. 5 neue Einheiten ergänzen

**Canoptek Plasmacyte** (Elites)
```
M 8" / WS 4+ / BS 4+ / S 4 / T 5 / W 1 / A 1 / Ld 10 / Sv 4+
Keywords: BEAST, FLY, CANOPTEK, CANOPTEK PLASMACYTE
models_min: 1, models_max: 1
rules: [livingMetal, viralConstruct, evasionProtocol, infusedMadness, dimensionalTranslocation]
weapons: monomolecular_proboscis
PL: fetchen | Punkte: fetchen
```

**Hexmark Destroyer** (Elites)
```
M 8" / WS 3+ / BS 2+ / S 5 / T 5 / W 5 / A 4 / Ld 10 / Sv 3+
Keywords: INFANTRY, CHARACTER, DESTROYER CULT, HYPERSPACE HUNTER, HEXMARK DESTROYER
models_min: 1, models_max: 1
rules: [livingMetal, dimensionalTranslocation, inescapableDeath, multiThreatEliminator, hardwiredForDestruction]
weapons: enmitic_disintegrator_pistol (×6)
PL: fetchen | Punkte: 65
```

**Transcendent C'tan** (Elites)
```
M 8" / WS 2+ / BS 2+ / S 6 / T 7 / W 9 / A 5 / Ld 10 / Sv 4+ / Invuln 4+
Keywords: MONSTER, CHARACTER, FLY, C'TAN SHARD, TRANSCENDENT C'TAN
models_min: 1, models_max: 1
rules: [livingMetal, necrodermis, enslavedStarGod, realityUnravels, fracturedPersonality, ctanPowers]
weapons: crackling_tendrils
PL: 14 | Punkte: 230
```

**Obelisk** (Lords of War)
```
M 8" / WS 6+ / BS 3+ / S 8 / T 8 / W 28 / A 6 / Ld 10 / Sv 2+
Keywords: VEHICLE, CORE, TITANIC, FLY, OBELISK
models_min: 1, models_max: 1
rules: [livingMetal, deathDescending, hoveringSentinel, gravityPulse]
weapons: tesla_sphere (×4)
PL: 17 | Punkte: 270
Bracket: 15-28 / 8-14 / 1-7 → M, BS, A degradieren
```

**Convergence of Dominion** (Fortification)
```
M – / WS – / BS 3+ / S 6 / T 8 / W 6 / A – / Ld – / Sv 3+
Keywords: BUILDING, CORE, VEHICLE, STARSTELE, CONVERGENCE OF DOMINION
models_min: 3, models_max: 3  (Codex: 3 Starstele; Wahapedia zeigt 1-10 → verifizieren)
rules: [livingMetal, dominionProtocols, dynasticCommandNode, translocationProtocols]
weapons: transdimensional_abductor
PL: 4 | Punkte: 80/Modell
```

---

### Schritt 5 — `points.yaml`: neue Datei

```yaml
# Punktkosten für Matched Play (9E, Codex Necrons)
# Quelle: Wahapedia / Chapter Approved

units:
  wh40k_9e.necrons.unit.warriors:             { per_model: 13 }
  wh40k_9e.necrons.unit.overlord:             { per_unit: 90 }
  wh40k_9e.necrons.unit.triarch_stalker:      { per_unit: 110 }
  wh40k_9e.necrons.unit.doomsday_ark:         { per_unit: 145 }
  wh40k_9e.necrons.unit.the_silent_king:      { per_unit: 400 }
  wh40k_9e.necrons.unit.obelisk:              { per_unit: 270 }
  wh40k_9e.necrons.unit.hexmark_destroyer:    { per_unit: 65 }
  wh40k_9e.necrons.unit.transcendent_ctan:    { per_unit: 230 }
  wh40k_9e.necrons.unit.convergence_of_dominion: { per_model: 80 }
  # ... restliche 42 Einheiten aus Schritt 1 ...

wargear:
  wh40k_9e.necrons.wargear.resurrection_orb: { points: 25 }
  # Alle anderen Wargear-Optionen = 0 (Default)
```

---

### Schritt 6 — `army_builder.md`: neue Felder dokumentieren

- `power_level: int` (bei models_min; Loader skaliert)
- `damage_bracket: list` (nur bei wounds > 9)
- Schema für `points.yaml` (per_model vs per_unit, wargear)

---

## Forge World / Legends (aktuell außer Scope)

Im Wahapedia Army List mit Symbol markiert — nicht im Standardkodex:
Night Shroud, Canoptek Tombstalker, Canoptek Acanthrites,
Tesseract Ark, Canoptek Tomb Sentinel, Gauss Pylon,
Seraptek Heavy Construct, Sentry Pylon.

→ Separater Scope falls gewünscht.

---

## Verifikation nach Abschluss

```bash
grep "power_level" data/wh40k_9e/necrons/units.yaml | wc -l    # → 51
grep "damage_bracket" data/wh40k_9e/necrons/units.yaml | wc -l  # → 10
grep -c "^  - id:" data/wh40k_9e/necrons/units.yaml              # → 51
grep "convergence_of_dominion" data/wh40k_9e/necrons/units.yaml  # → Treffer
grep "Elites" data/wh40k_9e/necrons/units.yaml | grep stalker    # → Triarch korrekt
```

---

## Nach diesem Plan: Ziel 5c — Loader Refactoring

**Betroffene Datei:** `src/gameObjects/loader.py`

Der aktuelle Loader lädt `army.yaml`. Nach dem Datensatz-Abschluss wird er refactored,
um den vollständigen Datensatz (units, weapons, wargear, abilities, points etc.) zu nutzen.

Vor dem Start: `loader.py` vollständig lesen und aktuellen Zustand verstehen, dann Plan zeigen.

---

## Architektur-Kurzreferenz

```
src/gameObjects/loader.py     ← aktiv, lädt army.yaml (bis Ziel 5c)
data/wh40k_9e/necrons/        ← alle Necron-Daten (noch unvollständig)
data/wh40k_9e/_shared/        ← detachment_types.yaml
```

## Wichtige Constraints
- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts
- dev-Branch — kein direktes Committen auf main
