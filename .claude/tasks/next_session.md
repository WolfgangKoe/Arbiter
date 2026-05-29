# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session gemacht wurde

**Ziel 4f.1 — Psychic Phase Nachbesserungen** vollständig abgeschlossen:

1. **CAST-Badge** (`_common.py`, `game_state.py`, `psychicPhase.py`):
   - Violettes Badge `("#9060d0", "#180a28")`, additiv wie SHOT
   - `turn_flags["cast"] = True` nach Smite-Apply gesetzt
   - `"cast": False` in `_unit_state()` + Reset in `next_phase()`

2. **cast_eligibility(unit_state)** — neue exportierte Pure Function:
   - Retreated → gesperrt (Regel: Zurückgezogene können nicht manifestieren)
   - Already cast → gesperrt (Regel: Einheit max. 1× pro Phase wählbar)
   - Wird in `_render_active_psychic()` geprüft

3. **WC-Eskalation für Smite:**
   - `psi_attempts_this_phase` Counter in `game_state` (init + `next_phase()` Reset)
   - Angezeigter und genutzter WC = `5 + psi_attempts_this_phase`
   - Counter wird bei jedem "Attempt Manifest"-Klick inkrementiert

4. **Smite-Zielhinweis** verbessert → Schritt-für-Schritt-Caption

5. **Port 8501 festgelegt** in `.streamlit/config.toml`

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A–1B — Struktur | ✅ fertig |
| Ziel 2 — Command Phase | ✅ fertig |
| Ziel 3 — Combat Foundation | ✅ fertig |
| Ziel 4a–4e — Badges, UI, Ability Engine, Command, Movement | ✅ fertig |
| Ziel 4f — Psychic Phase (Smite + Deny + Perils) | ✅ fertig |
| Ziel 4f.1 — Psychic Phase Nachbesserungen | ✅ fertig |
| **Ziel 4g — Angriffsphase (Charge Phase)** | ⏳ **nächster Schritt** |

---

## NÄCHSTE AUFGABE: Ziel 4g — Angriffsphase (Charge Phase)

Regelreferenz: `docs/work/schlachtrunde.md`, Abschnitt "5. Angriffsphase"

### Kernregeln

**Infrage kommende Einheiten:**
- Innerhalb von 12 Zoll um feindliche Einheit (Distanz nicht implementiert → UI-Hinweis genügt)
- **Gesperrt wenn:** `advanced=True` ODER `retreated=True`
- **Gesperrt wenn:** bereits `in_melee=True` zu Beginn der Phase (steht schon im Nahkampf)

**Ablauf:**
1. Angreifende Einheit wählen → 2W6 würfeln (Spieler gibt Ergebnis ein)
2. Bei Erfolg: `set_charged()` → `turn_flags["charged"] = True`, `in_melee = True`
3. Bei Misserfolg: kein Badge, Einheit bleibt im bisherigen Bewegungsstatus

**Abwehrfeuer (Overwatch):**
Scope TBD — vorläufig weglassen oder als Info-Caption erwähnen

### Dateien

```
src/gameMechanic/chargephase.py    ← Haupt-Handler (aktuell Stub)
src/gameMechanic/game_state.py     ← kein Änderungsbedarf erwartet
src/gameMechanic/unit_mutations.py ← set_charged() prüfen/ergänzen
tests/gameMechanic/test_charge_phase.py  ← neu anlegen
```

### Hilfsfunktionen (analog Shooting/Fight)

```python
def can_charge(unit_state: dict) -> bool:
    flags = unit_state.get("turn_flags", {})
    return not (
        flags.get("advanced")
        or flags.get("retreated")
        or unit_state.get("in_melee")
    )
```

### UI-Fluss

```
Aktive Spalte:
  Einheit selected → can_charge()? → Nein: Warning-Caption
                                   → Ja: "Charge Roll (2W6)" Number-Input + Button
  Erfolg (Roll ≥ custom threshold oder immer — kein Board): set_charged()
  Misserfolg: Caption "Charge failed."

Inaktive Spalte:
  Zieleinheit (selected_targets) → ggf. Wundanpassung wie in anderen Phasen
```

**Hinweis zur Distanzprüfung:** Da kein physisches Board existiert, ist der 12"-Check
nicht implementierbar. Der Spieler gibt nur den 2W6-Würfelwurf ein; ob der Charge
geometrisch reicht, entscheiden die Spieler selbst. Das ist regelkonform für diesen
App-Kontext.

---

## Weitere offene Ziele

### 4h — Moralphase
- D6 + Verluste vs. Leadership → Modelle fliehen

### 4f.1.c — Blessing-Flow (befreundetes Ziel)
- Braucht neuen Effect-Typ `"blessing"` in der Ability Engine
- Scope: nach 4g/4h

### 4i — Army Builder + Architektur
- `army.yaml` als Roster; Loader löst Werte aus `units.yaml`/`weapons.yaml` auf

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
    chargephase.py    ← Ziel 4g (aktuell Stub)
    psychicPhase.py   ← Ziel 4f + 4f.1 fertig
    game_state.py     ← psi_attempts_this_phase, cast in turn_flags
    commandPhase.py | movementPhase.py | shootingPhase.py
    fightPhase.py | moralePhase.py
    unit_mutations.py | game_log.py | ability_engine.py | phase_runner.py
  gameObjects/
    unit.py | weapon.py | loader.py | ability.py | command_protocol.py
  uiLayout/
    _common.py        ← CAST-Badge, cast_eligibility
    unitCard.py | armyCard.py | armyList.py
    gameActionsArea.py | gameProtocoll.py
data/wh40k_9e/
  necrons/army.yaml   ← Canoptek Spyder (gloom_prism) ✅
  orks/army.yaml      ← Weirdboy + Wurrboy (PSYKER) ✅
tests/
  gameMechanic/ | uiLayout/ | gameObjects/
docs/
  goals.md | spec/unit_states.md | spec/processes.md
  work/schlachtrunde.md  ← Regelreferenz
```

---

## Psychic Phase — vollständiger Stand

- Smite (Witchfire): WC 5 + Eskalation pro Versuch, W3/W6 bei Roll ≥ 11
- Perils of the Warp: W3 tödliche Verwundungen am Psyker
- Deny the Witch: 2W6 > Manifestwurf; 1× pro Phase pro Fraktion
- Gloom Prism: Canoptek Spyder kann bannen ohne PSYKER-Keyword
- CAST-Badge: nach erfolgreichem Smite-Apply
- Retreated-Sperre + Already-cast-Sperre via `cast_eligibility()`
- psi_attempts_this_phase: WC-Eskalation korrekt implementiert

### Bekannte Einschränkungen
- Nur Smite implementiert — keine Blessings/Maledictions (4f.1.c)
- Perils-Explosion (W3 auf Nachbareinheiten bei Psyker-Tod) fehlt — braucht Board-Positionen
- Psibann-Distanz (24 Zoll) nicht geprüft — braucht Board-Positionen
