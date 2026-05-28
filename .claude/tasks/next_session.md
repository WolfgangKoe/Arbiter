# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py`
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session gemacht wurde

- Psiphase vollständig geplant (kein Code geschrieben — nur Analyse + Dokumentation)
- BSData (`Orks.cat`, `Necrons.cat`) ausgewertet:
  - Weirdboy (p.85) und Wurrboy (p.92) als Ork-PSYKERs identifiziert
  - Canoptek Spyder + Gloom Prism als Necron-Deny-Einheit identifiziert
- Architektur-Problem erkannt: `army.yaml` dupliziert Daten aus `units.yaml`/`weapons.yaml`
  → Notiz in `goals.md` Ziel 4i; für jetzt: neue Einheiten weiterhin in `army.yaml` direkt
- Generalisierter Psi-Flow dokumentiert: `selectPsyker → selectTarget → resolve → handle_effects`
- Bannversuch-Konzept geklärt: unabhängig vom Ziel der Kraft; Canoptek Spinne kann bannen
- `docs/goals.md` Ziel 4f vollständig überarbeitet (Ziel 4i Architektur-Notiz ergänzt)

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A–1B — Struktur | ✅ fertig |
| Ziel 2 — Command Phase | ✅ fertig (Basis) |
| Ziel 3 — Combat Foundation | ✅ fertig |
| Ziel A — Architektur-Review | ✅ fertig |
| Ziel 4a — Badge/State-System | ✅ fertig |
| Ziel 4b — armyCard + unitCard Redesign | ✅ fertig |
| Ziel 4c — Ability Engine Refactoring | ✅ fertig |
| Ziel 4d — Befehlsphase vollständig | ✅ fertig (commit `b734f97`) |
| Ziel 4e — Bewegungsphase vollständig | ✅ fertig (commit `291e698`) |
| **Ziel 4f — Psychic Phase** | ⏳ **nächster Schritt** |

---

## NÄCHSTE AUFGABE: Ziel 4f — Psychic Phase implementieren

### Kontext

Alles ist geplant und dokumentiert. Die nächste Session beginnt direkt mit Implementierung —
kein weiteres Planen nötig. Freigabe liegt vor.

### Schritt 1: YAML-Einträge (vor dem Code)

**`data/wh40k_9e/orks/army.yaml`** — zwei Einheiten hinzufügen:

**Weirdboy** (BSData Orks.cat p.85):
- M5"/WS3+/BS5+/S5/T5/W5/A3/Ld6/Sv6+, kein Invuln, kein FNP
- Keywords: Orks, Bad Moons, Infantry, Character, **PSYKER**, Weirdboy
- Psyker: Cast 1, Deny 1, Powers: Smite + 2 PotW
- Waffe: Weirdboy Staff — Melee, S+3 (= 8 bei S5), AP-1, D3

**Wurrboy** (BSData Orks.cat p.92):
- M5"/WS3+/BS5+/S5/T5/W5/A3/Ld6/Sv6+, kein Invuln, kein FNP
- Keywords: Orks, Bad Moons, Infantry, Character, **PSYKER**, Beast Snagga, Wurrboy
- Psyker: Cast 1, Deny 1, Powers: Smite + 2 Beasthead
- Waffe: Eyez of Mork — 12", Assault 2, S6, AP-3, D3 (einzigartige Fernkampf-Psikraft)

**`data/wh40k_9e/necrons/army.yaml`** — eine Einheit hinzufügen:

**Canoptek Spyder (Gloom Prism)** (BSData Necrons.cat p.101):
- M6"/WS4+/BS4+/S6/T6/W6/A5/Ld10/Sv3+, kein Invuln, kein FNP
- Keywords: Necrons, Nephrekh, Vehicle, Fly, Canoptek, Canoptek Spyder
- `rules: [gloom_prism]` ← Schlüsselfeld für can_deny()-Check
- Waffe: 2× Particle Beamer — 18", Assault 6, S5, AP0, D1
- Abilities: "Gloom Prism: In der Psi-Phase des Gegners kann diese Einheit eine Psikraft bannen als wäre sie ein PSIONIKER | Fabricator Claw Array: Repariert DYNASTY VEHICLE um W3 LP/Zug"

### Schritt 2: Hilfsfunktionen in `psychicPhase.py`

```python
def has_psyker(units: list[Unit]) -> bool:
    return any("PSYKER" in {kw.upper() for kw in u.keywords} for u in units)

def can_deny(units: list[Unit]) -> bool:
    return any(
        "PSYKER" in {kw.upper() for kw in u.keywords} or "gloom_prism" in u.rules
        for u in units
    )

def is_perils(roll: int) -> bool:
    return roll in (2, 12)

def smite_damage_die(roll: int) -> str:
    return "W6" if roll >= 11 else "W3"

def deny_succeeds(manifest_roll: int, deny_roll: int) -> bool:
    return deny_roll > manifest_roll
```

### Schritt 3: UI-Flow

**Generalisierter Psi-Flow:**
```
selectPsyker → selectTarget (friendly ODER enemy) → resolve_psi_power → handle_effects
```
Zielrichtung ist Teil der Kraft, nicht des Bannvorgangs. Für Smite: feindliches Ziel.

**Session-State:**
```python
psi_result: dict | None = {
    "faction": str, "uid": str,
    "roll": int,
    "manifested": bool,      # roll >= 5
    "perils": bool,          # roll in (2, 12)
    "perils_applied": bool,  # W3-Schaden am Psyker angewendet
    "denied": bool,
    "deny_roll": int | None,
}
```

**Aktive Spalte:**
```
Keine PSYKER in Armee     → Caption "No PSYKER units — skip this phase."
Keine Einheit gewählt     → Caption "← Select a PSYKER from your army list."
Nicht-PSYKER gewählt      → Caption "Not a PSYKER — select a PSYKER unit."
PSYKER gewählt (Weirdboy) →
  "Smite — Warp Charge 5"
  [2D6 input]  [Attempt Manifest]
  → Roll < 5 (kein Perils):  "Failed." + [Reset]
  → Roll == 2 (Perils+fail): "Perils! Power failed." → W3 input → [Apply to Weirdboy]
  → Roll == 12 (Perils+ok):  "Perils! Manifested." → W3 input → [Apply] + Smite bereit
  → Roll 5–11:               "Manifested! Roll: N." → Smite bereit
```

**Inaktive Spalte:**
```
can_deny(enemy_units) == True + Manifest läuft + nicht gebannt:
  "Deny: 2D6 > {manifest_roll}"
  [2D6 input]  [Attempt Deny]
  → > manifest_roll: "Denied!"
  → ≤ manifest_roll: "Deny failed."

can_deny == False:
  Caption "No PSYKER or Gloom Prism — cannot deny."

(Zielstats wenn via ▷ markiert: T / Sv / ++)
```

**Unterer Bereich:**
```
Manifested + nicht gebannt + (kein Perils ODER Perils bereits angewendet):
  "Smite → {Zieleinheit}" | W3 (W6 bei Roll ≥ 11)
  [Schadenseingabe]  [Apply mortal wounds]

Sonst: PHASE_RULES["psychic"] Info-Text
```

### Schritt 4: Tests (`tests/gameMechanic/test_psychic_phase.py`)

```python
test_has_psyker_true()            # Unit mit PSYKER-Keyword
test_has_psyker_false()           # Units ohne PSYKER
test_can_deny_via_psyker_keyword()
test_can_deny_via_gloom_prism()   # rules: [gloom_prism], kein PSYKER
test_can_deny_neither()
test_is_perils_true()             # 2 und 12
test_is_perils_false()            # 5, 10, 11
test_smite_damage_die_w3()        # 5–10 → "W3"
test_smite_damage_die_w6()        # 11, 12 → "W6"
test_deny_succeeds_greater()
test_deny_fails_equal()           # strikt größer nötig
test_deny_fails_lower()
```

### Implementierungsreihenfolge

1. YAML-Einträge (Weirdboy, Wurrboy, Canoptek Spyder)
2. Tests schreiben (rot)
3. Hilfsfunktionen implementieren (grün)
4. UI-Flow implementieren
5. Manuell im Browser testen (Testszenario: Orks aktiv, Weirdboy manifestiert → Necrons denyen via Spinne)
6. Commit

---

## Scope-Grenzen

- **Nur Smite** — keine weiteren Psikräfte
- **Kein Blessing-Flow** — Zielauswahl nur feindlich (friendly target: spätere Session)
- **Gloom Prism** — direkt via `unit.rules`, kein Ability-Engine-Dispatch
- Ability Engine braucht neuen Effect-Typ `"deny_psychic"` für vollständige Abstraktion — nicht jetzt

---

## Designregeln (fest)

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: `first_player` links, `second_player` rechts
- Aktionen nur kontextuell zur ausgewählten Einheit
- **Kein Design ohne Schema** — Nutzer definiert Farbpalette selbst
- `dev`-Branch — kein direktes Committen auf `main`
- Kein Auto-Würfeln — alle Würfelwürfe gibt der Spieler ein

---

## Architektur (Kurzreferenz)

```
src/
  app.py
  gameMechanic/
    combat.py | commandPhase.py
    psychicPhase.py   ← NÄCHSTE Hauptdatei (Stub vorhanden)
    shootingPhase.py | fightPhase.py
    movementPhase.py   ← Ziel 4e fertig
    chargephase.py | game_state.py
    unit_mutations.py
    game_log.py | ability_engine.py
    phase_runner.py
  gameObjects/
    ability.py | command_protocol.py
    unit.py | weapon.py | loader.py
  uiLayout/
    _common.py
    unitCard.py | armyCard.py
    armyList.py | gameActionsArea.py
    gameProtocoll.py
data/wh40k_9e/
  necrons/army.yaml   ← Canoptek Spyder hinzufügen
  orks/army.yaml      ← Weirdboy + Wurrboy hinzufügen
tests/
  gameMechanic/ | uiLayout/ | gameObjects/
docs/
  goals.md | spec/unit_states.md
```
