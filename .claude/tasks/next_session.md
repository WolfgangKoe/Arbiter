# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py`
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session gemacht wurde

- Ziel 4e vollständig implementiert und committed (`291e698`):
  - Bug-Fix: Early-Return in `_active_movement` wenn `already_retreated=True`
  - Button-Labels: "Normal" → "Move", "Stationary" → "Stay Stationary"
  - Buttons vertikal (kein `st.columns(4)` mehr)
  - `_render_reinforcements_step` als eigener, immer sichtbarer Abschnitt
  - Phasennamen im Header auf Englisch: Command, Movement, Psychic, Shooting, Charge, Fight, Morale
  - `docs/spec/unit_states.md` komplett überarbeitet (4 Sektionen inkl. passive Spieler)
  - 15 Integrationstests (`test_movement_transitions.py`), alle grün
- `goals.md` + `next_session.md` aktualisiert: Psiphase vorgezogen (vor Fernkampfphase)

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

## NÄCHSTE AUFGABE: Ziel 4f — Psychic Phase

### Kontext

Die Psiphase kommt in der Spielreihenfolge direkt nach der Bewegungsphase.
Stub existiert bereits: `src/gameMechanic/psychicPhase.py`

**Necrons haben keine Psyker** — die Phase zeigt für Necrons nur eine Info-Caption.
Der volle Flow wird trotzdem generisch gebaut, damit er für Psyker-Armeen (z.B. Orks → Weird Boyz) einsetzbar ist.

### Regelgrundlage (aus `docs/work/schlachtrunde.md`)

- **Manifest:** 2W6 ≥ Warp-Energie-Wert → Psikraft wirkt
- **Bannen:** Gegnerischer Psyker innerhalb 24" → 2W6, bei Ergebnis **höher** als der Manifestwurf: Kraft gebannt
- **Gefahren des Warp:** Doppel-1 oder Doppel-6 beim Manifestversuch → W3 Schaden am Psyker
- **Schmetterschlag (Smite):** Warp-Energie 5 (+1 pro Manifestversuch in der Phase), trifft nächste sichtbare feindliche Einheit innerhalb 18" für W3 tödliche Verwundungen (W6 bei Ergebnis 11+)
- **Kein Auto-Würfeln:** Spieler gibt alle Würfelwürfe manuell ein

### Geplanter UI-Flow

#### Aktiver Spieler — Einheit mit PSYKER-Keyword ausgewählt:

```
Schritt 1: Psikraft auswählen
  [Schmetterschlag (Smite) — WC 5]   ← einzige Kraft in Scope

Schritt 2: Manifestation
  Warp-Energie: 5
  [Eingabe: 2D6 Ergebnis]
  → bei ≥ 5: "Kraft manifestiert" → Schritt 3
  → bei Doppel-1/6: "Gefahren des Warp! W3 Schaden." → Eingabe + apply_damage()
  → bei < 5: "Kraft gescheitert."

Schritt 3: Ziel und Schaden
  Nächste sichtbare feindliche Einheit (Spieler wählt)
  → bei Ergebnis 11+: W6 tödliche Verwundungen, sonst W3
  [Eingabe: Anzahl tödlicher Verwundungen] + "Apply"
```

#### Passiver Spieler — Einheit mit PSYKER-Keyword innerhalb 24":

```
[Bannversuch]
  [Eingabe: 2D6 Ergebnis]
  → wenn Ergebnis > Manifestwurf: "Kraft gebannt."
  → sonst: "Bannversuch gescheitert."
```

#### Kein Psyker in der Armee:

```
Caption: "No PSYKER units — nothing to do in the Psychic Phase."
```

### Empfohlene Reihenfolge

1. `psychicPhase.py` lesen (aktueller Stub)
2. Plan beschreiben + Freigabe einholen
3. Implementieren:
   a. PSYKER-Check + No-Psyker-Caption
   b. Smite-Manifestationsflow (2D6-Eingabe, WC-Vergleich, Perils)
   c. Zielauswahl + Schaden (tödliche Verwundungen via `apply_damage(mortal=True)`)
   d. Bannversuch für passiven Spieler
4. Tests schreiben (`tests/gameMechanic/test_psychic_phase.py`)
5. Commit

### Scope-Grenzen

- **Nur Schmetterschlag** — keine weiteren Psikräfte
- **Kein PSYKER-Flag** im unit_state nötig — PSYKER ist ein Keyword, wird aus `unit.keywords` geprüft
- Die Phase nutzt `apply_damage(mortal=True)` für tödliche Verwundungen (kein Schutzwurf)

---

## Designregeln (fest)

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: `first_player` links, `second_player` rechts
- Aktionen nur kontextuell zur ausgewählten Einheit
- **Kein Design ohne Schema** — Nutzer definiert Farbpalette selbst
- `dev`-Branch — kein direktes Committen auf `main`
- Necron-Spezifika sind **Beispiele** — Hauptlogik und Doku bleiben generisch
- Kein Auto-Würfeln — alle Würfelwürfe gibt der Spieler ein

---

## Architektur (Kurzreferenz)

```
src/
  app.py
  gameMechanic/
    combat.py | commandPhase.py
    psychicPhase.py   ← nächste Hauptdatei (Stub vorhanden)
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
data/wh40k_9e/necrons/
  command_protocols.yaml
tests/
  gameMechanic/ | uiLayout/ | gameObjects/
docs/
  goals.md | spec/unit_states.md
  work/schlachtrunde.md   ← Regelreferenz für Psiphase (Abschnitt 3)
```
