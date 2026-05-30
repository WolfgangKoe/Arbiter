# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)
Remote: GitHub (`origin`)

---

## Was in dieser Session gemacht wurde

### Schritt 1: Doku-Bereinigung ✅

- `docs/spec/architecture.md`:
  - `protocol.py` → `game_log.py`, `state.py` → `game_state.py`
  - `"current_phase"` → `"phase"` im session_state-Schema
  - Phase-Stubs als fertig markiert; `keyword.py`-TBD entfernt
  - Heading "Phase Stubs" → "Phase Reference"
- `docs/spec/processes.md`:
  - Stub-Phasen-Notiz entfernt
  - P-13 (Charge), P-14 (Fight), P-15 (Morale) Flowcharts ergänzt
  - Index um P-10 bis P-15 erweitert
- `docs/goals/doku.md`: alle Punkte abgehakt
- `docs/work/necrons.md`, `orks.md`: als veraltet markiert

### Schritt 2: Ziel 5a — Spec-Dateien ✅

- `docs/spec/army_builder.md` neu angelegt:
  - Zwei-Quellen-Strategie (Wahapedia + BattleScribe)
  - Katalog-Schema: `units.yaml`, `weapons.yaml`, `stratagems.yaml`, `abilities.yaml`
  - Roster-Format (ID-basiert, kein Stat-Duplizierung)
  - Loader-Vertrag + Unmatched-Handling
  - BattleScribe-Import-Ablauf
- `docs/spec/setup.md` neu angelegt:
  - Spielmodi: Matched / Open / Crusade
  - Spielgrößen + CP-Werte
  - Detachment-Tabelle (alle 8 Typen)
  - Setup-Flow + session_state-Felder

### Schritt 3: Ziel 5b — Necrons-Katalog (teilweise) 🔄

- `data/wh40k_9e/necrons/units.yaml` **neu aufgebaut**:
  - 11 Einheiten (vorher: alter tabletop.units.v1-Schema ohne Statlines)
  - Format: army_builder.md v1 (Weapon-Refs, kein Subfaction-Bonus in Statlines)
  - Einheiten: Overlord, Royal Warden, Plasmancer, Warriors, Immortals, Skorpekh Destroyers, Lychguard, Deathmarks, Canoptek Scarabs, Canoptek Wraiths, Triarch Stalker, Annihilation Barge, Canoptek Spyder
- `data/wh40k_9e/necrons/weapons.yaml` **neu aufgebaut**:
  - 20 Waffenprofile (vorher: alter Multi-Profil-Schema mit deutschen Feldern)
  - Format: army_builder.md v1
- `data/wh40k_9e/necrons/stratagems.yaml` **neu angelegt**:
  - 15 Stratagems (Dynastic: 8, Destroyer Cult: 2, Canoptek: 2, Vehicle: 2, Psychic: 1)
  - Basiert auf Codex-Trainingswissen — **Wahapedia-Verifikation ausstehend**

**Wichtig:** `army.yaml` (der aktive Loader-Datensatz) bleibt unverändert.
Die neuen `units.yaml`/`weapons.yaml`/`stratagems.yaml` werden erst in Ziel 5c vom Loader gelesen.
**300 Tests grün** (unverändert).

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A–1B — Struktur | ✅ fertig |
| Ziel 2 — Command Phase | ✅ fertig |
| Ziel 3 — Combat Foundation | ✅ fertig |
| Ziel A — Architektur-Review | ✅ fertig |
| Ziel 4a–4h — Alle Phasen | ✅ fertig |
| Ziel 5a — Spec-Dateien | ✅ fertig |
| **Ziel 5b — Katalog Necrons** | 🔄 teilweise (units/weapons/stratagems angelegt, Verifikation fehlt) |
| Ziel 5c — Loader-Refactoring | ⬜ nächste Aufgabe |
| Ziel 5d — BattleScribe Importer | ⬜ geplant |
| Ziel 5e — Setup-Screen Redesign | ⬜ geplant |
| Ziel 5f — Stratagems PoC | 🔄 teilweise (YAML vorhanden, Loader fehlt) |
| Ziel 6 — Crusade-Erweiterung | ⬜ geplant |
| Ziel 7 — Wahapedia Faction Fetcher | ⬜ geplant |

---

## Offene Implementierungsaufgaben

| Aufgabe | Priorität |
|---------|-----------|
| Ziel 5b — Wahapedia-Verifikation (curl) der Necron-Statlines + Stratagems | hoch |
| Ziel 5b — Fehlende Necron-Einheiten ergänzen (Lokhust Destroyers, Triarch Praetorians, etc.) | mittel |
| Ziel 5b — Orks: `units.yaml`, `weapons.yaml`, `stratagems.yaml` | mittel |
| Ziel 5c — Loader-Refactoring: liest units.yaml + weapons.yaml + stratagems.yaml | hoch |
| Ziel 5c — Roster-Unterstützung im Loader | mittel |
| Ziel 5c — Unmatched-Handling + Setup-Screen-Warnung | mittel |
| Ziel 5d — BattleScribe Importer (`tools/import_rosz.py`) | niedrig |
| Ziel 5e — Setup-Screen Redesign (Spielmodus, Roster-Auswahl) | mittel |
| 4f.1.c — Blessing-Flow (befreundetes Ziel) | niedrig |

---

## Nächste Session — Einstieg

### Schritt 1: Wahapedia-Verifikation (Ziel 5b abschließen)

Die neuen YAML-Dateien basieren auf Trainingswissen und benötigen Verifikation via Wahapedia-curl.
Priorität: Warriors, Overlord, Skorpekh (da im aktiven Spielszenario genutzt).

```
data/wh40k_9e/necrons/units.yaml   ← Statlines prüfen (M/WS/BS/S/T/W/A/Ld/Save)
data/wh40k_9e/necrons/weapons.yaml ← Waffenprofile prüfen
data/wh40k_9e/necrons/stratagems.yaml ← Texte + CP-Kosten prüfen
```

### Schritt 2: Ziel 5c — Loader-Refactoring

Neuer Loader liest `units.yaml` + `weapons.yaml` (statt `army.yaml`).
Kernänderungen in `src/gameObjects/loader.py`:

- `load_army(faction_dir)` → liest `units.yaml`, löst `ref`-Weapons aus `weapons.yaml` auf
- Default Close Combat Weapon ergänzen wo fehlend
- Roster-Unterstützung: `load_army(faction_dir, roster_path)` optional
- `load_stratagems(faction_dir)` → neu

Nach Loader-Update:
- Alle Tests auf Kompatibilität prüfen
- `army.yaml` archivieren oder löschen

### Schritt 3: Ziel 5c — Roster-Support

- `data/rosters/`-Verzeichnis anlegen
- Einen Testrost schreiben (z.B. `player1_necrons_2026-05-30.yaml`)
- Loader auf Roster-Pfad-Parameter erweitern

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
    unit.py | weapon.py | loader.py | ability.py | stratagem.py
    command_protocol.py | detachment.py | faction_property.py
  uiLayout/
    _common.py | unitCard.py | armyCard.py | armyList.py
    gameActionsArea.py | gameProtocoll.py
data/
  wh40k_9e/
    _shared/detachment_types.yaml
    necrons/
      army.yaml         ← aktiv (Loader-Quelle bis Ziel 5c)
      units.yaml        ← NEU: army_builder.md v1 (für Ziel 5c)
      weapons.yaml      ← NEU: army_builder.md v1 (für Ziel 5c)
      stratagems.yaml   ← NEU: 15 Stratagems (Verifikation ausstehend)
      faction_abilities.yaml | subfaction_abilities.yaml | unit_abilities.yaml
      command_protocols.yaml | faction_properties.yaml
    orks/army.yaml
  rosters/              ← NEU in Ziel 5c (BattleScribe-Imports)
  scenarios/
docs/
  goals/                index.md | ziel1–7.md | doku.md
  spec/
    architecture.md | ui_layout.md | unit_states.md | processes.md
    army_builder.md ✅ | setup.md ✅
  work/schlachtrunde.md | scenarios.md
tools/
  import_rosz.py        ← NEU in Ziel 5d
tests/
  gameMechanic/ | uiLayout/ | gameObjects/
.github/workflows/deploy.yml
```
