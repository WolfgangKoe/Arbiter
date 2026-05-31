# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)
Remote: GitHub (`origin`)

---

## Was zuletzt gemacht wurde

### Ziel 5b — Necrons Katalog Fixes ✅
Alle Statline-Fehler, Keyword-Korrekturen, 18 fehlende Waffen, 2 neue Einheiten (Technomancer, Lokhust Heavy Destroyers), stratagems.yaml komplett neu aufgebaut.

### Ability-Architektur vereinheitlicht ✅
- `units.yaml` hat nur noch `rules: [...]` — kein `abilities:` Textfeld mehr
- `faction_abilities.yaml` — 7 Abilities, `unit_abilities.yaml` — 8 Abilities, `wargear_abilities.yaml` — 9 Abilities
- `get_abilities_for_unit()` + `load_wargear_abilities()` in loader.py

### Ziel 5b.5 — Necrons Regeln vervollständigen ✅
- **stratagems.yaml**: 59 Stratagems (37 Core + 6 Dynastic + 8 Cult of Cryptek + 8 Annihilation Legion), vollständig gegen Wahapedia verifiziert. Boarding Actions ausgeschlossen. player-Felder für 4 Stratagems korrigiert (both statt active).
- **units.yaml**: 46 Einheiten — alle Necrons 9E Datasheets außer ForgeWorld. 31 neue Einheiten hinzugefügt (14 HQs inkl. Named Characters + Silent King, 4 Elites, 2 Fast Attack, 4 Heavy Support, 2 Flyer, 5 Lord of War/Titanic).
- **weapons.yaml**: 90 Waffen — 52 neue Waffen für alle neuen Einheiten hinzugefügt (Wahapedia-verifiziert).
- **tools/wahapedia_scraper.py**: Slugs für alle neuen Einheiten ergänzt (inkl. Fix: `Lord` statt `Necron-Lord`, `C-tan-Shard-...` mit Bindestrichen).

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
| Ziel 5b — Katalog Necrons | ✅ fertig |
| Ziel 5b.5 — Necrons Regeln vervollständigen | ✅ fertig |
| **Ziel 5b.6 — Army Building Rules** | 🔄 Konzept-Entscheidung nötig |
| **Ziel 5c — Loader-Refactoring** | ⬜ nächste große Aufgabe |
| Ziel 5d — BattleScribe Importer | ⬜ geplant |
| Ziel 5e — Setup-Screen Redesign | ⬜ geplant |
| Ziel 5f — Stratagems PoC | ⬜ geplant |
| Ziel 6 — Crusade-Erweiterung | ⬜ geplant |

---

## Offene Entscheidung: Army Building Rules (Ziel 5b.6)

**Frage an Nutzer:** Wie tief soll die Armeebau-Validierung werden?
- **a)** Nur Daten-Vollständigkeit: alle Einheiten + Regeln als Text-Beschreibung in YAML (kein Code)
- **b)** Einfache Validierung: Pflicht-Slots, Warlord-Pflicht (NOBLE), Dynastic Advisors (1× CRYPTEK pro Detachment)
- **c)** Vollständige Validierung inkl. CP-Budget, Punkte-Limits, The Silent King Sonderregel

Die Entscheidung bestimmt, ob Ziel 5b.6 vor oder nach Ziel 5c angegangen wird.

**Bekannte Regeln die implementiert werden müssten:**
- Dynastic Advisors: 1× CRYPTEK pro DYNASTY-Detachment (Ausnahme: Exalted Cryptek Stratagem = 2; Cult of the Cryptek = unbegrenzt)
- Noble als Warlord: Warlord muss NOBLE-Keyword haben (Ausnahme: Silent King = automatisch Warlord)
- The Silent King: kein `<DYNASTY>`-Keyword, hat SZAREKHAN fest, muss Warlord sein
- Command Protocols: bereits in `command_protocols.yaml` und `commandPhase.py` — prüfen ob korrekt

---

## Nächste Hauptaufgabe: Ziel 5c — Loader-Refactoring

Ziel: `load_army()` auf `units.yaml` + `weapons.yaml` umstellen (statt `army.yaml`), Roster-System einführen.

**Was das bedeutet:**
- `loader.py` neu schreiben: lädt alle 46 units aus units.yaml, resolved weapon-refs aus weapons.yaml
- Roster-System: Spieler wählt Einheiten + Wargear, Wargear-Abilities werden per Roster angewendet
- `army.yaml` archivieren (aktuell noch aktiv, bleibt bis Ziel 5c als Fallback)
- Neue Datei: `data/rosters/` — persistente Armeelisten

**Achtung:** Ziel 5c ist ein größeres Refactoring. units.yaml hat jetzt 46 Einheiten und 90 Waffen — alle valide und weapon-refs vollständig geprüft. Bereit für Loader.

---

## Wichtige Referenz-Dateien

| Datei | Inhalt |
|-------|--------|
| `data/wh40k_9e/necrons/units.yaml` | **46 Einheiten** — Wahapedia-verifiziert |
| `data/wh40k_9e/necrons/weapons.yaml` | **90 Waffen** — Wahapedia-verifiziert |
| `data/wh40k_9e/necrons/stratagems.yaml` | **59 Stratagems** — vollständig Wahapedia-verifiziert |
| `data/wh40k_9e/necrons/faction_abilities.yaml` | 7 Abilities (faction scope) |
| `data/wh40k_9e/necrons/unit_abilities.yaml` | 8 Abilities (unit scope) |
| `data/wh40k_9e/necrons/wargear_abilities.yaml` | 9 Abilities (wargear scope) |
| `data/wh40k_9e/necrons/wargear.yaml` | 10 Wargear-Items (Display-Daten) |
| `tools/wahapedia_scraper.py` | Scraper mit allen 46 Unit-Slugs — `python3 tools/wahapedia_scraper.py necrons --unit overlord` |

Wahapedia Live-Referenz: https://wahapedia.ru/wh40k9ed/factions/necrons/

---

## Designregeln (fest)

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: `first_player` links, `second_player` rechts
- Aktionen nur kontextuell zur ausgewählten Einheit
- `dev`-Branch — kein direktes Committen auf `main`
- Kein Auto-Würfeln — alle Würfelwürfe gibt der Spieler ein
- Keine eigenständigen Design-/Farbentscheidungen (Nutzer definiert Schema)

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
      army.yaml         ← aktiv bis Ziel 5c
      units.yaml        ← verifiziert, bereit für Ziel 5c
      weapons.yaml      ← verifiziert
      stratagems.yaml   ← Review nötig!
      faction_abilities.yaml | unit_abilities.yaml | wargear_abilities.yaml
      subfaction_abilities.yaml | command_protocols.yaml
      faction_properties.yaml | wargear.yaml | relics.yaml | arkana.yaml
    orks/army.yaml
  rosters/            ← NEU in Ziel 5c
  scenarios/
docs/
  goals/ | spec/ | work/
tools/
  wahapedia_scraper.py
tests/
  gameMechanic/ | uiLayout/ | gameObjects/
```
