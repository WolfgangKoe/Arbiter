# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session gemacht wurde

**Ziel 4g — Angriffsphase (Charge Phase)** vollständig implementiert.

### Änderungen:

| Datei | Was |
|-------|-----|
| `unit_mutations.py` | `melee_with` auf `[[faction, uid]]`-Format umgestellt; `_unit_key()` Helper; `leave_melee_pair()` neu |
| `game_state.py` | `heroic_intervened: False` in `turn_flags` |
| `chargephase.py` | `in_melee`-Sperre, HI-Renderer, `render_melee_engagements`-Aufruf |
| `shootingPhase.py` | `can_shoot()` mit `unit`-Param für Big Guns Never Tire; `target_in_friendly_melee()` |
| `fightPhase.py` | `_render_melee_pairs()` auf neues Format aktualisiert |
| `uiLayout/_common.py` | `render_melee_engagements()` mit Break-Buttons |
| Tests | `test_unit_mutations.py`, `test_movement_transitions.py` angepasst; `test_charge_phase.py` neu (25 Tests) |

**Teststatus:** 280 Tests grün.

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
| Ziel 4g — Angriffsphase (Charge Phase) | ✅ fertig |
| **Ziel 4h — Moralphase** | ⏳ nächste logische Implementierungsaufgabe |

---

## NÄCHSTE SESSION — Diskussionsthemen

Diese Session ist eine **Planungs- und Konzeptsession**, kein Implementierungsblock.
Der Nutzer bringt eigene Prompts/Recherchen mit (insb. für Punkt 2).

---

### Thema 1: Spec-Dokumentation aktualisieren

Zwei Aufgaben:

**a) Bedeutung des Namens „Arbiter" ergänzen**
In `docs/goals.md` (oder einem neuen `docs/concept.md`) die Bedeutung des Namens dokumentieren.
Der Nutzer möchte den Begriff selbst definieren — Vorschlag einholen und dann aufschreiben.

**b) Aktuellen Stand der App dokumentieren**
`docs/goals.md` → alle abgeschlossenen Ziele sauber als fertig markieren.
Ggf. offene Designfragen (Overwatch-Scope, 4f.1.c Blessing-Flow) aktualisieren.

---

### Thema 2: Deployment auf Hugging Face + CodeBerg-Integration

Der Nutzer hat bereits einen Prompt für dieses Thema.

**Zu klärende Fragen:**
- Wie wird die Streamlit-App als Hugging Face Space deployt?
- Wie wird ein CI/CD-Workflow über CodeBerg (Gitea-basiert) gebaut, der pushes auf `dev` → Test-Space und pushes auf `main` → Prod-Space auslöst?
- Secrets/Config für HF-Token in CodeBerg-Actions einrichten
- Benötigt die App eine `requirements.txt` mit fixierten Versionen? (aktuell: `pyproject.toml`)

**Architekturentscheidung vorab:**
Hugging Face Spaces unterstützen Streamlit nativ — kein Docker erforderlich.
Zwei Spaces: `arbiter-test` (branch: `dev`) und `arbiter-prod` (branch: `main`).

---

### Thema 3: Phase-Testfixtures (Dev-Shortcuts / Test-Stubs)

Ziel: Die App in einem vordefinierten Zustand starten, ohne alle Phasen durchklicken zu müssen.

**Mögliche Ansätze zur Diskussion:**

**Option A — URL-Parameter / Query-String**
`?scenario=charge_phase` → App startet direkt in der Charge Phase mit zwei engaged units.
Streamlit unterstützt `st.query_params` seit v1.30.

**Option B — Dev-Panel (sichtbar nur im Dev-Modus)**
Seitliches Expander-Panel mit Schaltflächen: „Load Charge Scenario", „Load Psychic Scenario" etc.
Aktiviert über Env-Variable `ARBITER_DEV=true`.

**Option C — Fixture-Dateien (`data/scenarios/`)**
JSON-Snapshots des `st.session_state` — App kann diese laden und sich in diesen Zustand versetzen.
Wiederverwendbar für Tests (pytest kann denselben Snapshot laden).

**Empfehlung vorab:** Option C ist am mächtigsten (deckt UI-Tests + manuelle Navigation ab),
Option B ist am schnellsten implementiert.

---

## Offene Implementierungsaufgaben (nach den Diskussionen)

| Aufgabe | Priorität |
|---------|-----------|
| Ziel 4h — Moralphase | hoch |
| 4g.x — Overwatch (Scope noch offen) | mittel |
| 4f.1.c — Blessing-Flow (befreundetes Ziel) | niedrig |
| 4i — Army Builder + YAML-Loader | mittel |

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
    chargephase.py    ← Ziel 4g fertig
    psychicPhase.py   ← Ziel 4f + 4f.1 fertig
    game_state.py
    commandPhase.py | movementPhase.py | shootingPhase.py
    fightPhase.py | moralePhase.py
    unit_mutations.py ← melee_with: [[faction, uid]] (neu!)
    game_log.py | ability_engine.py | phase_runner.py
  gameObjects/
    unit.py | weapon.py | loader.py | ability.py | command_protocol.py
  uiLayout/
    _common.py        ← render_melee_engagements() neu
    unitCard.py | armyCard.py | armyList.py
    gameActionsArea.py | gameProtocoll.py
data/wh40k_9e/
  necrons/army.yaml
  orks/army.yaml
tests/
  gameMechanic/test_charge_phase.py  ← NEU (25 Tests)
  gameMechanic/ | uiLayout/ | gameObjects/
docs/
  goals.md | work/schlachtrunde.md
```
