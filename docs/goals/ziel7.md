# Ziel 7 — Gefechtsoptionen + subfaction-Mechanik ⬜

**Voraussetzung:** Ziel 6 abgeschlossen (inkl. 6e Execute-Logik-Grundlage).

Bündelt zwei eng verwandte Bereiche aus Ziel 6, die blockiert oder bewusst ausgelagert wurden:
(1) die vollständige **subfaction Execute-Logik** (`collect_modifiers_for_phase` + Ability.modifier + Phase-Handler-Verdrahtung) und
(2) die **generischen Fraktionsfähigkeiten** für weitere Armeen (alle aktuell blocked-by-YAML).

**Crusade-Erweiterung ist jetzt Ziel 8.**

---

## Status

⬜ Noch nicht aktiv. Vorbedingung: Ziel 6 muss vollständig abgeschlossen sein.

---

## Backlog — eingehende Punkte (aus Ziel 6 ausgelagert)

### 6e — subfaction Execute-Logik

- [ ] `gameMechanic/ability_engine.py`: `collect_modifiers_for_phase(phase, attacker_unit, weapon, target_unit)` — sammelt alle aktiven Modifier aus allen Quellen
- [ ] `gameObjects/ability.py`: Ability-Schema um `modifier`-Felder erweitern (analog zu Stratagem in 6c)
- [ ] `data/wh40k_9e/*/unit_abilities.yaml` + `faction_abilities.yaml`: Modifier-Felder für relevante Fähigkeiten nachtragen (Pilot: Necrons + Orks)
- [ ] Phase-Handler (Shooting, Fight, Charge): rufen `collect_modifiers_for_phase()` auf und übergeben Ergebnis an Attackensequenz-Renderer

### 6f — Ability-Badges + Keyword-Highlighting

Abhängig von `collect_modifiers_for_phase` (6e Execute-Logik):

- [ ] `uiLayout/unitCard.py`: `active_modifiers` aus Session-State lesen, Badges für betroffene Einheit rendern
- [ ] `uiLayout/unitCard.py`: Keyword-Highlighting wenn `active_modifiers` ein Keyword-Condition-Modifier betrifft
- [ ] `gameMechanic/game_state.py`: `active_modifiers` Datenstruktur definieren: `{unit_key, source, effect, expires_at_phase, expires_at_round}`

### 6h — Kat1–3 neue Fraktionen (alle blocked-by-YAML)

**Kategorie 1 — Runden-Wahl:**

- [ ] AdMech: `data/wh40k_9e/adeptus_mechanicus/faction_abilities.yaml` + `CommandProtocol.secondary` optional + `armyCard._render_protocol_ui()` anpassen
- [ ] Tyranids: `data/wh40k_9e/tyranids/faction_abilities.yaml` + Pool-Check ob Synapse-Unit noch lebt
- [ ] `tests/test_faction_abilities_admech.py`, `tests/test_faction_abilities_tyranids.py`

**Kategorie 2 — Einmalig-Deklariert:**

- [ ] T'au: `data/wh40k_9e/tau_empire/faction_abilities.yaml` (`montka` + `kauyon` mit `active_rounds`)
- [ ] `armyCard._render_waaagh_ui()`: `active_rounds`-Feld aus YAML auslesen
- [ ] `tests/test_faction_abilities_tau.py`

**Kategorie 3 — Auto-Progression (kein Player-Input):**

- [ ] `ability_engine.py`: `get_auto_progression_modifier(faction_dir, phase, round)`
- [ ] `armyCard.py`: `_render_auto_progression_badge(faction)` — Info-Badge ohne Button
- [ ] YAML-Schema `ability_type: auto_progression` + YAML für Space Marines, Death Guard, Chaos SM
- [ ] `tests/test_auto_progression.py`

**Fix B — WAAAGH! generisch:**

- [x] `armyCard.py:_render_waaagh_ui`: Ability-Suche, WARBOSS-Keyword und Effekttexte vollständig generisch (via YAML `active_text`-Feld) (S113, e031616 — Drift-Nachzug S119)
- [x] `gameObjects/ability.py`: optionales `active_text: str | None` (S113, e031616 — Drift-Nachzug S119)
- [x] `data/wh40k_9e/orks/faction_abilities.yaml`: `active_text` ergänzen (S113, e031616 — Drift-Nachzug S119)
