# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)
Remote: GitHub (`origin`) — kein CodeBerg mehr.

---

## Was in dieser Session gemacht wurde

### GitHub-Integration abgeschlossen
- GitHub als einziges Remote (`origin`), CodeBerg entfernt
- GitHub Actions Workflow (`.github/workflows/deploy.yml`) läuft: Test → Deploy auf HF Space `arbiter-test`

### Bugfix: Fight Phase — Melee-Engagement-Prüfung
- `fightPhase.py`: Angriff nur möglich wenn Ziel in `melee_with` des Angreifers steht
- Neue Hilfsfunktion `_is_target_engaged()` (testbar, pure function)
- 7 neue Tests in `test_fight.py`

### Scenario-Fixtures für alle Phasen
- `data/scenarios/`: command, movement, shooting, morale neu hinzugefügt
- `docs/scenarios.md`: Übersicht mit vollständigen URLs
- `morale_phase.json`: Warriors (3 Verluste) + Boyz (5 Verluste) für echten Moraltest

### Ziel 4h — Moralphase ✅
- `moralePhase.py`: vollständige UI — alle Einheiten mit Verlusten werden angezeigt
- Schwellenwertanzeige mit Rechenweg (z.B. „schlägt fehl ab W6 ≥ 5")
- Bestanden/Fehlgeschlagen-Buttons; bei Fehlschlag: Modellzahl-Eingabe
- `flee_models()` in `unit_mutations.py` — semantisch getrennt von `apply_damage()`
- `fled_models_this_turn` + `morale_tested` im Unit-State
- Protokolleintrag: „X Modelle geflohen" (eigener Log-Eintrag)
- 13 neue Tests (`test_morale_phase.py`)

**Teststatus: 300 Tests grün.**

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
| Ziel 4h — Moralphase | ✅ fertig |
| **Ziel 4i — Army Builder** | ⏳ nächste Aufgabe (Diskussion offen) |

---

## Offene Implementierungsaufgaben

| Aufgabe | Priorität |
|---------|-----------|
| Ziel 4i — Army Builder + YAML-Loader | mittel |
| 4g.x — Overwatch (Scope noch offen) | mittel |
| 4f.1.c — Blessing-Flow (befreundetes Ziel) | niedrig |

---

## Nächste Session — Themen

### Thema 1: Ziel 4i — Army Builder

Architektur-Entscheidung aus `docs/goals.md`:
- Aktuell: `army.yaml` selbstenthalten (Daten dupliziert zum Katalog)
- Ziel: `army.yaml` wird Roster; Loader löst Werte aus `units.yaml`/`weapons.yaml` auf
- Bis dahin: neue Einheiten weiterhin direkt in `army.yaml` pflegen

Offene Frage: Datei-Import vs. In-App-Builder vs. hardcodierte Presets?

### Thema 2: PR auf main

Alle Ziele 4a–4h sind fertig. Wäre ein guter Zeitpunkt für einen PR `dev` → `main`.
Voraussetzung: GitHub Actions läuft grün auf `dev`.

### Thema 3: UI-Theme (Design-Block)

Laut `docs/goals.md` noch offen:
- Farbpalette überarbeiten (Goldtöne, Primärfarbe, Kontraste)
- Badge-Optik und Spacing prüfen
- Einheitenkarten-Layout verfeinern
Nutzer definiert Farbschema selbst (kein Design ohne Schema).

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
  app.py                          ← ?scenario= Query-Param
  gameMechanic/
    moralePhase.py                ← Ziel 4h fertig
    chargephase.py                ← Ziel 4g fertig
    psychicPhase.py               ← Ziel 4f + 4f.1 fertig
    fightPhase.py                 ← _is_target_engaged() neu
    game_state.py                 ← fled_models_this_turn, morale_tested
    unit_mutations.py             ← flee_models() neu
    scenarios.py                  ← load/apply/save Fixtures
    commandPhase.py | movementPhase.py | shootingPhase.py
    game_log.py | ability_engine.py | phase_runner.py
  gameObjects/
    unit.py | weapon.py | loader.py | ability.py | command_protocol.py
  uiLayout/
    _common.py | unitCard.py | armyCard.py | armyList.py
    gameActionsArea.py | gameProtocoll.py
data/
  scenarios/                      ← alle 7 Phasen als Fixtures (docs/scenarios.md)
  wh40k_9e/necrons/army.yaml
  wh40k_9e/orks/army.yaml
tests/
  gameMechanic/test_morale_phase.py  ← NEU (13 Tests)
  gameMechanic/test_fight.py         ← _is_target_engaged (7 neue Tests)
  gameMechanic/ | uiLayout/ | gameObjects/
docs/
  scenarios.md                    ← NEU: Übersicht aller Scenario-URLs
  goals.md | concept.md | work/schlachtrunde.md
.github/workflows/deploy.yml      ← GitHub Actions: Test + HF Deploy
```
