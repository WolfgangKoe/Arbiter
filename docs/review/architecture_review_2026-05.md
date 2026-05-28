# Architektur-Review — Arbiter 2026-05

**Leitfrage:** Kann eine neue Armee "angedockt" werden, ohne die Kernlogik anzufassen?

**Ergebnis kurz:** Nein — noch nicht. Drei klare Blocker müssen vor Ziel 4 behoben werden.
Die übrigen Lücken sind erwartet oder scope-bedingt; die Kernabstraktionen sind solide.

---

## Klassifikations-Legende

| Kürzel | Bedeutung |
|--------|-----------|
| ✅ OK | Implementiert / YAML-only ausdrückbar |
| 🔧 Parameter | Neues Feld in Dataclass oder `turn_flags` |
| 🏗️ Konzept | Eigene Funktion/Handler nötig |
| ⚠️ Konflikt | Widerspricht bestehender Designentscheidung oder crash-würdig |
| ❌ Out of Scope | Bewusst nicht geplant |

---

## A1 — Regelwerk-Klassifikation

### Befehlsphase

| Regelaspekt | Klassifikation | Notiz |
|-------------|----------------|-------|
| BP-Bonus (1×/Phase) | ✅ OK | `commandPhase.py` implementiert |
| Phasenspezifische Fähigkeiten | ✅ OK | `abilities` mit `phase: command` ausdrückbar |
| Schlachtordnungs-Bedingung | 🏗️ Konzept | `army_in_formation()`-Check fehlt |

### Bewegungsphase

| Regelaspekt | Klassifikation | Notiz |
|-------------|----------------|-------|
| Normale Bewegung / Stationär | ✅ OK | `move`-Wert in Profil; `movement_choice` vorhanden |
| Vorrücken (W6-Roll) | 🏗️ Konzept | Roll-Logik fehlt; `turn_flags["advanced"]` vorhanden, sperrt korrekt |
| Zurückziehen | 🏗️ Konzept | `turn_flags["fell_back"]` fehlt komplett |
| FLIEGEN-Keyword | ✅ OK | Als `keywords`-Eintrag ausdrückbar (`Fly` bereits in Necron-Daten) |
| Reserven | 🏗️ Konzept | Kein Reserve-Handler; `in_reserve` vorhanden aber passiv |
| Geländeregeln / Tischphysik | ❌ Out of Scope | Kein Tischmodell geplant |

### Psiphase

| Regelaspekt | Klassifikation | Notiz |
|-------------|----------------|-------|
| PSIONIKER-Keyword | ✅ OK | Als `keywords`-Eintrag |
| Schmetterschlag-Psikraft | 🔧 Parameter | Passt in Weapon-Profil-Schema (damage: W3) |
| Psitest (2W6 ≥ Warpenergiewert) | 🏗️ Konzept | Kein Psikraft-Handler, kein Warpenergiewert-Feld |
| Deny (Psibanntest) | 🏗️ Konzept | Gegner-Reaktionsmechanik fehlt |
| Gefahren des Warp | 🏗️ Konzept | Sonderfall im Psikraft-Handler |
| Ausgeschlossene Einheiten | 🔧 Parameter | `turn_flags["fell_back"]`-Check |

### Fernkampfphase

| Regelaspekt | Klassifikation | Notiz |
|-------------|----------------|-------|
| Schieß-Einschränkungen (Advance/Fell Back) | 🔧 Parameter | `turn_flags["advanced"]`/`["fell_back"]`-Checks |
| Zielwahl (Sichtlinie, Reichweite) | ❌ Out of Scope | Tischmodell nötig |
| Im Nahkampf gebunden — Schießen verboten | ⚠️ Konflikt | App erlaubt Schießen ohne `in_melee`-Check; **Regelbruch** |
| Auf gebundene Freunde schießen verboten | ⚠️ Konflikt | Gleiche Lücke |
| Schnelles Würfeln | ❌ Out of Scope | UI-Optimierung, kein Gamestate |

### Attackensequenz

| Regelaspekt | Klassifikation | Notiz |
|-------------|----------------|-------|
| Trefferwurf (±1-Cap) | ✅ OK | `hit_modifier` cap in `resolve_attack()` Z.86 |
| Verwundungswurf (S vs. T-Tabelle) | ✅ OK | `wound_threshold()` korrekt |
| Schutzwurf (RW − AP) | ✅ OK | Z.105: `armour_effective = save + abs(ap)` |
| Invuln-Save | ✅ OK | Z.106–111 |
| FNP | ✅ OK | Z.126–129 |
| Tödliche Verwundungen (Mortal Wounds) | ❌ fehlend | Kein separater `mortal_wounds`-Pfad in `resolve_attack()` |
| **Spillover tödliche Verwundungen** | **⚠️ Konflikt** | **Regelwerk: Überschuss geht auf nächstes Modell über — fehlt komplett** |
| Unmodifizierte 1 misslingt immer | ✅ OK (by design) | Player-entered-System: Spieler validiert selbst |
| Überschüssiger Normalschaden verfällt | ✅ OK | Pro-Modell-Cap in `apply_damage()` korrekt |

### Angriffsphase

| Regelaspekt | Klassifikation | Notiz |
|-------------|----------------|-------|
| Angriffswurf (2W6-Bewegung) | 🏗️ Konzept | Roll-Handler fehlt; `charged`-Flag vorhanden |
| Zielwahl (12-Zoll) | ❌ Out of Scope | |
| Abwehrfeuer | ⚠️ Konflikt | `only_6s` in Beschreibungen erwähnt, aber `hit_modifier: int` — Typ-Konflikt |
| Heroische Intervention | 🏗️ Konzept | CHARAKTERMODELL-Check + 3-Zoll-Bewegung fehlt |

### Nahkampfphase

| Regelaspekt | Klassifikation | Notiz |
|-------------|----------------|-------|
| **Alternierend — Nicht-Aktiv-Spieler zuerst** | **⚠️ Konflikt** | **Regelwerk: Nicht-aktiver Spieler beginnt. App startet mit aktivem Spieler.** |
| Angreifer zuerst (`fights_first`) | 🏗️ Konzept | Keyword vorhanden, Sortierlogik fehlt |
| Nachrücken (Consolidation, 3") | 🏗️ Konzept | Kein Handler |
| Reach-Keyword (2"-Reichweite) | 🔧 Parameter | Als YAML-Parameter ausdrückbar |
| Neu ordnen | ❌ Out of Scope | |

### Moralphase

| Regelaspekt | Klassifikation | Notiz |
|-------------|----------------|-------|
| Moraltest (W6 + Verluste > Leadership) | 🏗️ Konzept | `Unit.leadership` vorhanden, kein Moraltest-Handler |
| Modelle entfernen bei Misserfolg | 🏗️ Konzept | Kein Modell-Tracking pro Würfelwurf |
| Einzelmodell-Einheit: kein Test | 🔧 Parameter | `models_max == 1`-Check |

---

## A2 — YAML-Struktur-Analyse

### Necron-YAML: Felder zum Löschen

Folgende Felder in `data/wh40k_9e/necrons/units.yaml` sind Curation-Metadaten ohne Spielwert:

| Feld | Empfehlung |
|------|------------|
| `source_catalog_file` | Löschen |
| `curated_status` | Löschen |
| `curation` (ganzer Block) | Löschen — enthält `rules_reviewed`, `wave_completed`, `review_method`, etc. |
| `notes` | Löschen — enthält Sprint-Kommentare (NX-2c), keine Spieldaten |
| `weapon_source_strategy` | Löschen |

**Umfang:** ~5 Felder × ~40 Einheiten = ~200 Zeilen entfernbar.

### faction / dynasty_selectable: Empfehlung

**`<Dynasty>` in `faction`:** Kanonisch korrekt. Einheiten mit `<Dynasty>` erhalten zur Armeebuilding-Zeit das Dynastiekeyword der Armee. Canoptek-Einheiten mit `<Dynasty>` ist regelkonform — sie sind keine eigenständige Unterfraktion. Beibehalten.

**`dynasty_selectable: []`:** Immer leer, nirgends im Code konsumiert (`unit.py`, `combat.py`, `loader.py` alle ohne Referenz). Semantisch unklar. **Löschen.**

### Schadenswert-Notation — Kritischer Crash-Bug

`parse_dice()` in `combat.py` kennt nur **D-Notation** (D6, 2D6, D3). Die Necron-YAML verwendet durchgängig **W-Notation** (deutsches Kürzel).

| Notation | Einheit/Waffe | `parse_dice()` | Status |
|----------|---------------|----------------|--------|
| `"W3"` | Staff of Tomorrow damage | `int("W3")` | **CRASH** |
| `"W6"` | Eldritch Lance | `int("W6")` | **CRASH** |
| `"W3+3"` | Entropic Lance, Death Ray | `int("W3+3")` | **CRASH** |
| `"3W3"` | Gauss Destructor | `int("3W3")` | **CRASH** |
| `"D6"` | Ork weapons | split at `D` → 1,6 | OK |
| `"D3"` | Ork weapons | split at `D` → 1,3 | OK |
| `"+1"` als Stärke | Staff of the Destroyer | `wound_threshold("+1", T)` | **CRASH** |
| `"x2"` als Stärke | Voidscythe | analog | **CRASH** |
| `"Träger"` als Stärke | Sehr viele Waffen | analog | **CRASH** (Caller) |

**Entscheidungsvorlage:**

**Option A — W→D-Normierung in YAML:** Alle `W3`→`D3`, `W6`→`D6`, `W3+3`→`D3+3` in der YAML umschreiben. `parse_dice()` bleibt unverändert. Vorteil: einheitliche Notation. Nachteil: Einmalaufwand beim Umschreiben.

**Option B — `parse_dice()` erkennt W-Alias:** `s = s.upper().replace("W", "D")` vor dem bestehenden Parse-Code. Vorteil: Necron-YAML bleibt lesbar für Deutsch-Nutzer. Nachteil: Zwei Notationen im System (Orks nutzen D, Necrons W).

**Empfehlung: Option B** — eine Zeile Code, keine YAML-Migration, beide Notationen co-existieren sauber. `+N`-Stärken (`+1`, `x2`) sind ein separates Problem im Caller-Kontrakt (kein `parse_dice()`-Issue).

### Stärke-Relativwerte (Caller-Kontrakt-Lücke)

`wound_threshold(strength: int, toughness: int)` erwartet Integer. Viele Waffen haben:
- `"Träger"` / `"User"` → muss auf Einheitenstärke aufgelöst werden
- `"+1"`, `"+2"` → relativer Bonus auf Trägerstärke
- `"x2"` → doppelte Trägerstärke

Diese Auflösung fehlt als explizite Funktion. Wenn kein Caller sie macht, crasht `wound_threshold()`. `render_attack_form()` löst `"User"` auf (`_common.py`), aber `"+1"` und `"x2"` werden dort nicht behandelt.

**Empfehlung:** `resolve_weapon_strength(weapon_strength: str, unit_strength: int) -> int` in `combat.py` oder `gameObjects/weapon.py` als eigenständige Funktion.

### Degradierende Profile

Nur **Monolith** hat `profile_brackets` in `units.yaml`. Die `Unit`-Dataclass hat kein entsprechendes Feld — das YAML ist aktuell nicht vollständig ladbar.

**Entscheidungsvorlage:**

**Option A — `wound_profiles: list[WoundProfile]` in `Unit`-Dataclass:** Saubere Typsicherheit, aber erfordert neue Dataclass + Loader-Logik. Profile-Wechsel muss im Spielzustand getrackt werden.

**Option B — Als Ability mit LP-Schwellen-Trigger:** Z.B. `trigger: {"wounds_below": 13}` in `abilities`. Flexibel, kein Schema-Breaking-Change. Nachteil: Stat-Ablesbarkeit schlechter; Ability-Engine muss Stat-Overrides unterstützen.

**Empfehlung: Option A** — Degradierende Profile sind ein fundamentales Spielmechanik-Konzept, das sauber in der Dataclass abgebildet sein sollte. Option B ist zu flexibel für etwas Vorhersehbares.

### Ork-Daten: Stand

`data/wh40k_9e/orks/army.yaml` enthält 6 Einheiten: Big Mek in Mega Armour, Warboss in Mega Armour, Boyz ×10, Gretchin ×10, Warbikers ×3, Mek Gun. Keine `units.yaml`.

Wahapedia liefert ~80 Ork-Einheiten (HQ-LoW). Für eine erste spielbare Ork-Armee wären mindestens nötig:
- **Troops:** Boyz (vorhanden), Beast Snagga Boyz
- **HQ:** Warboss (vorhanden), Weirdboy (für Psiphase-Tests)
- **Elites:** Meganobz, Tankbustas
- **Fast Attack:** Deffkoptas, Stormboyz
- **Heavy Support:** Lootas, Battlewagon
- **Transport:** Trukk

**Strukturelle Lücken in `army.yaml`** vs. Necron `units.yaml`:
- `abilities` ist Freitext-String statt strukturierter Liste (beide Armeen gleiches Problem)
- Kein `wargear`-Block
- Ork-Waffen nutzen `D`-Notation (kompatibel mit `parse_dice()`) — konsistent anders als Necrons

---

## Zusammenfassung: Blocker vor Ziel 4

### Blocker 1 — `parse_dice()` crasht auf W-Notation (P1)

Alle Necron-Waffen mit `W3`/`W6`/`W3+3`/`3W3` crashen. Fix: eine Zeile in `parse_dice()`.

### Blocker 2 — `in_melee`-Check fehlt in Fernkampfphase (P2)

Regelbruch: Gebundene Einheiten können schießen. Fix: `can_shoot()` um `in_melee`-Check erweitern (bereits in `can_fight()` vorhanden).

### Blocker 3 — Nahkampfphase startet mit falschem Spieler (P3)

Regelbruch: App startet Nahkampfrunde beim aktiven Spieler. Korrekt wäre der Nicht-aktive Spieler. Fix: `fightPhase.py` Turn-Order-Logik.

### Nicht-Blocker (für Ziel 4 akzeptabel)

- `resolve_weapon_strength()` fehlt (⚠️) — beim ersten Kampf mit Relativstärken-Waffe auffindbar
- Spillover tödliche Verwundungen (⚠️) — kein eigener Pfad, aber selten relevant bei derzeitigem Umfang
- Degradierende Profile (`Unit`-Dataclass) — Monolith nicht spielbar, aber kein anderes Scope-Ziel betroffen
- `dynasty_selectable` / Curation-Metadaten — nur YAML-Bereinigung, kein Code-Impact
- Psiphase / Moralphase-Handler — als Stubs akzeptabel bis Ziel 4

---

## Template-YAML für Einheiten (armeeneutral)

```yaml
# Kanonische Felder — keine Curation-Metadaten, keine Build-Artefakte
id: wh40k_9e.<faction>.<slot>.<name>
name_en: "Unit Name"
name_de: "Einheitenname"
faction:
  - "<Dynasty>"      # Platzhalter, wird zur Armeebuilding-Zeit ersetzt
  - Necrons
  - Canoptek          # falls zutreffend
keywords:
  core: [CORE]        # Mechanik-relevante Keywords
  other: [FLY, INFANTRY, VEHICLE]

battlefield_role: [Troops]

# Statzeile
move: '6"'
ws: "3+"
bs: "3+"
strength: 5
toughness: 5
wounds: 5
save: 3
invuln_save: 4         # null wenn keiner
leadership: 10
oc: 1
fnp: null              # Wert als Integer (5 = 5+) oder null

# Modellanzahl
models_min: 1
models_max: 1

# Waffen — Referenz auf weapons.yaml (kein Inline-Duplikat)
weapons:
  - ref: <faction>.weapons.<weapon_id>
    count: 1

# Degradierende Profile (nur wenn regelwerksgemäß vorhanden)
profile_brackets:
  - min_wounds: 7
    max_wounds: 12
    m: '6"'
    bs: "4+"
    # nur Felder die sich ändern

# Fähigkeiten — strukturiert, nicht Freitext
abilities:
  - id: living_metal
    name_de: Lebendes Metall
    phase: command
    trigger: start_of_phase
    effect: "heal:1"

# Keine der folgenden Felder:
# source_catalog_file, curated_status, curation, notes, weapon_source_strategy, dynasty_selectable
```

---

*Erstellt: 2026-05-28 | Session: Ziel A*
