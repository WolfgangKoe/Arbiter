# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py`
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session gemacht wurde

- `docs/spec/processes.md` ergänzt: P-10 (Bewegungsphase), P-11 (Kommandoprotokolle), P-12 (Psychic Phase)
- Ziel 4f vollständig implementiert (commit `625a0ff`):
  - `orks/army.yaml`: Weirdboy + Wurrboy (PSYKER, korrekte BSData-Werte)
  - `necrons/army.yaml`: Canoptek Spyder mit `rules: [gloom_prism]`
  - `psychicPhase.py`: vollständiger Smite-Flow inkl. Perils, Bannversuch, Schadensanwendung
  - `test_psychic_phase.py`: 22 Tests, alle grün (252 gesamt)
  - Gloom Prism: einmal-pro-Phase-Tracking via `psychic_denies_used` in session_state

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
| Ziel 4f — Psychic Phase | ✅ fertig (commit `625a0ff`) |
| **Ziel 4f-Nachbesserungen** | ⏳ **nächster Schritt** |

---

## NÄCHSTE AUFGABE: Ziel 4f — Nachbesserungen

Drei offene Punkte aus der Review-Session:

---

### 4f.1 — Smite-Schadensbutton klar machen

**Status:** Der Code ist korrekt — der Schadensbutton erscheint sobald eine feindliche Einheit via
`selected_targets` ausgewählt ist (gleicher Mechanismus wie in der Schussphase: Spieler klickt auf
gegnerische Einheit in deren Armeeliste).

**Problem:** In der UI ist nicht klar genug, wie der Spieler das Ziel auswählt.
Die Caption `"▷ Select an enemy unit from their army list as Smite target."` reicht offenbar nicht.

**Fix:** Im Smite-Bereich explizit erklären, dass das Ziel via Klick auf die gegnerische Armeeliste
gewählt wird (wie in Schuss-/Kampfphase). Optional: Die Zielauswahl-Logik testen.

**Zu bearbeiten in:** `src/gameMechanic/psychicPhase.py: _render_psi_result()`

---

### 4f.2 — PSYKER-Badge

**Beschreibung:** Es fehlt ein Badge für den PSYKER-Zustand (analog zu MWBD, IN MELEE etc.).

Konkret: Wenn ein Psyker in dieser Phase bereits eine Kraft manifestiert hat, sollte er ein
`CAST` (oder ähnlich) Badge erhalten, damit Spieler wissen, welche Einheit schon gecastet hat.
(Optional: für Ziel 4f ausreichend — ist kein harter Bug.)

**Design:** Badge setzt sich nach Phasenwechsel zurück (ephemer, analog zu SHOT).
Name: `CAST` — Farbe: passend zu Psi-Thema (lila/violett, ähnlich `CHARGED`).

**Zu bearbeiten in:**
- `src/uiLayout/_common.py: _BADGE_COLORS` + `state_badges_html()`
- `src/gameMechanic/psychicPhase.py`: `turn_flags["cast"] = True` nach erfolgreichem Manifest
- `src/gameMechanic/game_state.py: reset_turn_flags()`: `"cast": False` ergänzen
- Tests: `tests/uiLayout/test_common.py`

---

### 4f.3 — Buff-Flow (Blessing) für spätere Session (Ziel 4g oder 4f.3)

**Beschreibung:** Psikräfte vom Typ Blessing betreffen eine befreundete Einheit (kein feindliches Ziel).
Wenn der Psyker einen Buff manifestiert, muss:
1. Eine **befreundete** Einheit als Ziel gewählt werden (aus der eigenen Armeeliste)
2. Der Buff-Effekt angewendet werden (z.B. +1 Bewegung, +1 Attacke)
3. Ein neues Badge erscheinen (z.B. `BLESSED` oder der Buff-Name als Micro-Badge)

**Scope-Grenze jetzt:** Ziel 4f deckt nur Smite (Witchfire). Blessings kommen in 4f.3 oder 4g.

**Wichtig für die Planung:** Zum Zeitpunkt der Blessing-Implementierung braucht die Ability Engine
einen neuen Effect-Typ `"blessing"` mit Zieltyp `"friendly"` — bis dahin reicht direkter Code.

---

## Weitere offene Punkte aus Ziel 4

### 4g — Angriffsphase (Charge Phase)

- [ ] Charge-Würfel: 2W6 — bei Erfolg `set_charged()`, bei Misserfolg bleibt `MOVED`
- [ ] `advanced`-Flag sperrt Charge-Button
- [ ] RP-Trigger nach Feindangriff
- [ ] Overwatch (Scope: TBD)

### 4h — Moralphase

- [ ] D6 + Verluste vs. Leadership → bei Fehlschlag: Modelle fliehen

### 4i — Army Builder + Architektur

- [ ] `army.yaml` als Roster; Loader löst Werte aus `units.yaml`/`weapons.yaml` auf
- [ ] Ability Engine: Effect-Typ `"deny_psychic"` für Gloom Prism (aktuell: direkter rules-Check)

---

## Implementierungsreihenfolge (nächste Session)

1. **4f.1** — Smite-Zielauswahl-Hinweis verbessern + ggf. manuell testen
2. **4f.2** — CAST-Badge (ephemer, nach Manifest gesetzt, Reset bei Phasenwechsel)
3. Dann: Entscheidung ob 4g (Charge) oder 4f.3 (Blessing) als nächstes

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
    psychicPhase.py   ← Ziel 4f fertig (commit 625a0ff)
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
  necrons/army.yaml   ← Canoptek Spyder (gloom_prism) ✅
  orks/army.yaml      ← Weirdboy + Wurrboy (PSYKER) ✅
tests/
  gameMechanic/ | uiLayout/ | gameObjects/
docs/
  goals.md | spec/unit_states.md | spec/processes.md
```

---

## Psychic Phase — Implementierungsdetails (für nächste Session)

### Wie Smite-Schaden funktioniert (wichtig für Testing)

Der Schadensbutton erscheint **nur wenn eine feindliche Einheit ausgewählt ist**:
1. Psyker-Spieler wählt seinen PSYKER (aktive Spalte)
2. Psyker-Spieler klickt auf eine gegnerische Einheit in der **gegnerischen Armeeliste** → `selected_targets`
3. Danach erscheint in der aktiven Spalte: Zielname + Schadenseingabe + Apply-Button

Gleicher Mechanismus wie in Schuss-/Kampfphase. Kein separater Zielauswahl-Dialog.

### Perils-Schaden — Kein Auto-Apply

Perils verursacht W3 tödliche Verwundungen am Psyker selbst.
Der Spieler gibt das W3-Ergebnis (1–3) ein und klickt **[Apply to {unit}]**.
Kein automatisches Apply — konsistent mit "kein Auto-Würfeln".

### Deny — Gloom Prism (einmal pro Phase)

`psychic_denies_used` in `session_state` ist ein Dict `{faction: bool}`.
Reset erfolgt in `render_end` (wenn Spieler → klickt) und beim nächsten Phasen-Init.
