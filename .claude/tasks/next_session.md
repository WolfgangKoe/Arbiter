# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)
Remote: GitHub (`origin`)

---

## Was in dieser Session gemacht wurde

### Planungssession — Ziel 5 vorbereitet (keine Codeänderungen)

#### Research (Subagenten)

- **BattleScribe XML-Format** vollständig analysiert:
  - `.rosz` = ZIP mit einer `.ros`-Datei (UTF-8 XML), Python stdlib reicht (`zipfile` + `xml.etree`)
  - XML-Namespace: `http://www.battlescribe.net/schema/rosterSchema`
  - Alle Statlines direkt im XML (M/WS/BS/S/T/W/A/Ld/Save + Waffenprofile)
  - `invuln_save` + FNP nur per Regex aus Ability-Text; `oc` existiert nicht in 9E-Daten
  - Weapon-Attacks stecken im `Type`-String (`"Rapid Fire 2"` → 2 Attacks)

- **Wahapedia Setup-Regeln** via curl erfolgreich gefetcht (Matched + Open Play)

- **Doku-Audit** durchgeführt: 4 Inkonsistenzen in `architecture.md`, fehlende P-13/14/15 in `processes.md`, 2 fehlende Spec-Dateien

#### Architekturentscheidungen für Ziel 5

- **Zwei-Quellen-Strategie**: BattleScribe → Roster (`data/rosters/`), Wahapedia → Katalog (`data/wh40k_9e/<fraktion>/`)
- Roster referenziert nur Katalog-IDs (lightweight), keine Stat-Duplikation
- **Default-Nahkampfwaffe** muss explizit ergänzt werden: `Close Combat Weapon: Melee/Melee/User/0/1`
- Bestehende `army.yaml`-Dateien werden ersetzt (zu fehlerhaft, keine Stratagems)
- BS-Importer: XML → Katalog-Matching → leichtgewichtige `roster.yaml`; `unmatched`-Kategorie für unbekannte Einheiten
- Flacher Roster-Speicher, P1-Wahl sperrt für P2

#### Dokumentation restrukturiert

- `docs/goals.md` → `docs/goals/` (aufgeteilt in Dateien pro Ziel)
  - `index.md`: Übersichtstabelle + Vision
  - `ziel1.md` – `ziel7.md`: je ein Ziel
  - `doku.md`: Doku-Bereinigungsaufgaben

**Teststatus: 300 Tests grün (unverändert — keine Codeänderungen).**

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A–1B — Struktur | ✅ fertig |
| Ziel 2 — Command Phase | ✅ fertig |
| Ziel 3 — Combat Foundation | ✅ fertig |
| Ziel A — Architektur-Review | ✅ fertig |
| Ziel 4a–4h — Alle Phasen | ✅ fertig |
| **Ziel 5 — Setup & Datenlage** | ⬜ nächste Aufgabe |
| Ziel 6 — Crusade-Erweiterung | ⬜ geplant |
| Ziel 7 — Wahapedia Faction Fetcher | ⬜ geplant |

---

## Offene Implementierungsaufgaben

| Aufgabe | Priorität |
|---------|-----------|
| Doku-Bereinigung (`architecture.md`, `processes.md`) | hoch — vor Ziel 5 |
| Ziel 5a — Spec-Dateien anlegen (`army_builder.md`, `setup.md`) | hoch |
| Ziel 5b — Katalog neu aufbauen (Necrons via Wahapedia) | hoch |
| Ziel 5c — Loader-Refactoring | hoch |
| Ziel 5d — BattleScribe Importer | mittel |
| Ziel 5e — Setup-Screen Redesign | mittel |
| Ziel 5f — Stratagems Proof of Concept | niedrig |
| 4f.1.c — Blessing-Flow (befreundetes Ziel) | niedrig |
| 4g.x — Overwatch (Scope offen) | niedrig |

---

## Nächste Session — Einstieg

### Schritt 1: Doku-Bereinigung (klein, sofort)

Details in `docs/goals/doku.md`. Kurzfassung:

`docs/spec/architecture.md`:
- `protocol.py` → `game_log.py`, `state.py` → `game_state.py`
- `"current_phase"` → `"phase"` im session_state-Schema
- Phase-Stubs als fertig markieren; `keyword.py`-TBD entfernen

`docs/spec/processes.md`:
- Stub-Phasen-Notiz entfernen
- P-13 Charge, P-14 Fight, P-15 Morale als Flowcharts ergänzen

### Schritt 2: Ziel 5a — Spec-Dateien anlegen

`docs/spec/army_builder.md`:
- Roster-Format (ID-basiert, kein Stat-Duplizierung)
- Katalog-Schema (`units.yaml`, `weapons.yaml`, `stratagems.yaml`, `abilities.yaml`)
- Loader-Vertrag + Unmatched-Handling

`docs/spec/setup.md`:
- Matched Play: Spielgrößen + CP-Werte + Detachment-Regeln
- Open Play: Power Level, keine Punkte
- Crusade: Setup-Übersicht (Details in Ziel 6)

### Schritt 3: Ziel 5b — Katalog neu aufbauen

Start mit Necrons via Wahapedia (curl funktioniert bereits). Zielstruktur:

```
data/wh40k_9e/necrons/
  units.yaml              ← alle Statlines (vollständig, korrekt)
  weapons.yaml            ← alle Waffenprofile
  stratagems.yaml         ← alle Stratagems (NEU)
  abilities.yaml          ← Faction Abilities (mechanisch verdrahtet)
  command_protocols.yaml  ← bereits vorhanden ✅
```

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
    moralePhase.py | chargephase.py | psychicPhase.py
    fightPhase.py | shootingPhase.py | movementPhase.py
    commandPhase.py | game_state.py | unit_mutations.py
    game_log.py | ability_engine.py | phase_runner.py
    combat.py | scenarios.py
  gameObjects/
    unit.py | weapon.py | loader.py | ability.py
    command_protocol.py | detachment.py | faction_property.py
  uiLayout/
    _common.py | unitCard.py | armyCard.py | armyList.py
    gameActionsArea.py | gameProtocoll.py
data/
  wh40k_9e/
    _shared/detachment_types.yaml
    necrons/army.yaml   ← wird in Ziel 5b ersetzt
    orks/army.yaml      ← wird in Ziel 5b ersetzt
  rosters/              ← NEU in Ziel 5 (BattleScribe-Imports)
  scenarios/
docs/
  goals/                ← NEU: aufgeteilt (index.md, ziel1–7.md, doku.md)
  spec/
    architecture.md | ui_layout.md | unit_states.md | processes.md
    army_builder.md (NEU in 5a) | setup.md (NEU in 5a)
  work/schlachtrunde.md | scenarios.md
tools/
  import_rosz.py        ← NEU in Ziel 5d
tests/
  gameMechanic/ | uiLayout/ | gameObjects/
.github/workflows/deploy.yml
```
