# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)
Remote: GitHub (`origin`)

---

## Was in dieser Session gemacht wurde

### Schritt 1: Wahapedia-Verifikation — Necrons Katalog (Ziel 5b) ✅

Vollständige Prüfung aller Necron-Datensheets gegen Wahapedia 9E.

Gebaut: `tools/wahapedia_scraper.py`
- Scrapt Wahapedia-Einheitenseiten (BeautifulSoup)
- Extrahiert Stats, Keywords, Invuln, Waffen, Abilities
- Läuft mit: `python3 tools/wahapedia_scraper.py necrons --all`
- Stratagems: `python3 tools/wahapedia_scraper.py necrons --stratagems`
- Wiederverwendbar für andere Fraktionen (Orks etc.)

Befund abgelegt: `docs/work/necrons_catalog_verification.md`
- Alle offenen Fragen beantwortet (scraper-gesichert)
- Alle Fehler mit Ist/Soll dokumentiert

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
| **Ziel 5b — Katalog Necrons** | 🔄 Verifikation ✅, Fixes ausstehend |
| Ziel 5c — Loader-Refactoring | ⬜ nächste Aufgabe (nach 5b Fixes) |
| Ziel 5d — BattleScribe Importer | ⬜ geplant |
| Ziel 5e — Setup-Screen Redesign | ⬜ geplant |
| Ziel 5f — Stratagems PoC | ⬜ geplant |
| Ziel 6 — Crusade-Erweiterung | ⬜ geplant |
| Ziel 7 — Wahapedia Faction Fetcher | ⬜ geplant |

---

## Nächste Session — Einstieg

### Schritt 1: Ziel 5b abschließen — Alle Fixes umsetzen (Freigabe nötig!)

Vollständiger Befund in: `docs/work/necrons_catalog_verification.md`
Der Nutzer muss Freigabe erteilen, dann alles in dieser Reihenfolge:

**1. Schema erweitern:**
- `docs/spec/army_builder.md` → `attacks`-Feld in units.yaml-Schema ergänzen

**2. units.yaml korrigieren:**
- 13 Statline-Fehler (invuln, ws, s, t, wounds, bs, battlefield_role)
- Keywords aller 13 Einheiten bereinigen (Rules raus, fehlende Keywords rein)
- `attacks`-Werte für alle 13 Einheiten eintragen
- Abilities-Texte: Overlord "My Will Be Done", Plasmancer "Living Lightning"
- 2 fehlende Einheiten ergänzen: Technomancer, Lokhust Heavy Destroyers

**3. weapons.yaml korrigieren:**
- 13 falsche Feldwerte (ap, damage, strength — mit neuer User+X-Notation)
- 18 fehlende Waffendefinitionen eintragen (alle Werte scraper-gesichert)
- Canoptek Spyder: `close_combat_weapon` → `automaton_claws`

**4. stratagems.yaml neu aufbauen:**
- Alle 15 aktuellen Einträge löschen
- 34 Kern-Stratagems + 6 Dynastic-Stratagems aus Verifikationsdokument eintragen
- Supplement-Stratagems (Annihilation Legion, Boarding Actions) weglassen

### Schritt 2: Ziel 5c — Loader-Refactoring

Nach den Data-Fixes: Loader auf neue YAML-Struktur umstellen.
- `load_army(faction_dir)` → liest units.yaml + weapons.yaml (statt army.yaml)
- `attacks`-Feld im Unit-Objekt ergänzen
- Default Close Combat Weapon ergänzen wo fehlend
- Alle Tests auf Kompatibilität prüfen
- `army.yaml` danach archivieren

---

## Wichtige Referenz-Dateien

| Datei | Inhalt |
|-------|--------|
| `docs/work/necrons_catalog_verification.md` | Vollständiger Verifikationsbefund mit Ist/Soll |
| `tools/wahapedia_scraper.py` | Wahapedia-Scraper (wiederverwendbar) |
| `data/wh40k_9e/necrons/units.yaml` | Zu korrigierende Katalogdatei |
| `data/wh40k_9e/necrons/weapons.yaml` | Zu korrigierende Waffendatei |
| `data/wh40k_9e/necrons/stratagems.yaml` | Komplett neu aufzubauende Stratagem-Datei |

Scraper-Befehl zum Nachprüfen:
```
python3 tools/wahapedia_scraper.py necrons --unit overlord
python3 tools/wahapedia_scraper.py necrons --all
python3 tools/wahapedia_scraper.py necrons --stratagems
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
      units.yaml        ← wird in dieser Session korrigiert
      weapons.yaml      ← wird in dieser Session korrigiert
      stratagems.yaml   ← wird in dieser Session neu aufgebaut
      faction_abilities.yaml | subfaction_abilities.yaml | unit_abilities.yaml
      command_protocols.yaml | faction_properties.yaml
    orks/army.yaml
  rosters/              ← NEU in Ziel 5c
  scenarios/
docs/
  goals/
  spec/ army_builder.md | architecture.md | setup.md | ...
  work/ necrons_catalog_verification.md ← Verifikationsbefund
tools/
  wahapedia_scraper.py  ← NEU: Wahapedia-Scraper
  import_rosz.py        ← NEU in Ziel 5d
tests/
  gameMechanic/ | uiLayout/ | gameObjects/
```
