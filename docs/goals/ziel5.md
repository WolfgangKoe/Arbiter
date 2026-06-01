# Ziel 5 — Setup & Datenlage 🔄

**Architektur-Entscheidung (2026-05-30):**

Zwei Quellen mit klar getrennter Verantwortung:

| Quelle | Rolle | Speicherort |
|--------|-------|-------------|
| BattleScribe `.rosz` | Roster — welche Einheiten, Modellzahl, Ausrüstungswahl | `data/rosters/<name>.yaml` |
| Wahapedia | Katalog — Stats, Waffen, Stratagems, Abilities (mechanisch verdrahtet) | `data/wh40k_9e/<fraktion>/` |

Roster referenziert nur Katalog-IDs. Der Loader löst auf. Einheit ohne Katalog-Eintrag → `unmatched`, nicht spielbar.

**Implizite Regel (muss explizit sein):**
Jede Einheit besitzt mindestens eine Nahkampfwaffe. Falls nicht explizit definiert, wird automatisch ergänzt:
`Close Combat Weapon: Range=Melee, Type=Melee, S=User, AP=0, D=1`

**Bestehende `army.yaml`-Dateien werden ersetzt** — zu fehlerhaft und strukturell veraltet (Stat-Duplikate, fehlende Waffen, keine Stratagems).

---

## 5a — Neue Datenstruktur & Spec ✅

- [x] `docs/spec/army_builder.md` — Roster-Format, Katalog-Schema, Loader-Vertrag, Unmatched-Handling
- [x] `docs/spec/setup.md` — Spielmodi-Regeln (Matched/Open/Crusade)
- [x] Roster-Format definiert: `data/rosters/<name>.yaml` (ID-basiert, keine Stat-Duplizierung)
- [x] Katalog-Schema definiert: neues Format in army_builder.md v1

---

## 5b — Katalog Necrons (Grunddaten) ✅

Stand 2026-06-01 — verifiziert gegen Wahapedia:

| Datei | Status | Inhalt |
|-------|--------|--------|
| `units.yaml` | ✅ | 51 Einheiten, power_level, damage_bracket (Vehicles), wargear_options (normiert) |
| `weapons.yaml` | ✅ | Profile-Schema, alle Dual-Profile zusammengeführt |
| `stratagems.yaml` | ✅ | 59 Stratagems |
| `faction_abilities.yaml` | ✅ | 7 Abilities, IDs normiert auf `wh40k_9e.necrons.faction.*` |
| `unit_abilities.yaml` | ✅ | 8 Abilities, IDs normiert auf `wh40k_9e.necrons.unit.*` |
| `wargear_abilities.yaml` | ✅ | 12 Abilities, IDs normiert auf `wh40k_9e.necrons.wargear.*` |
| `wargear.yaml` | ✅ | 10 Items |
| `subfaction_abilities.yaml` | ✅ | 6 Dynastien, IDs normiert auf `wh40k_9e.necrons.dynasty.*` |
| `command_protocols.yaml` | ✅ | 6 Protokolle, Namespace-Prefix gesetzt |
| `warlord_traits.yaml` | ✅ | 13 Traits |
| `arkana.yaml` | ✅ | 12 Cryptek-Arkana |
| `relics.yaml` | ✅ | 6 Relikte |
| `weapon_abilities.yaml` | ✅ | 44 Abilities |
| `army_rules.yaml` | ✅ | Armeebau-Regeln |
| `points.yaml` | ✅ | 51 Einheiten + Wargear + Arkana |
| `army.yaml` | ✅ | **gelöscht** |

Wahapedia-Verifikation aller Statlines und Stratagem-Texte: ✅ abgeschlossen (2026-05-30)

---

## 5b.2 — Datensäuberung vor Loader ✅

### Schritt A — `army.yaml` entfernen + Namespace-Normierung ✅

- [x] `army.yaml` gelöscht
- [x] Alle Ability-IDs auf `wh40k_9e.`-Namespace normiert (faction/unit/wargear/dynasty)
- [x] `loader.py` liest `units.yaml` (Catalog), fällt auf `army.yaml` zurück (Orks-Compat)
- [x] `points.yaml`: Triarch Stalker in Elites-Sektion

### Schritt B — `wargear_options`-Schema vereinheitlichen ✅

- [x] Alle 16 `wargear_options`-Blöcke auf einheitliches `type/with/replaces/item`-Schema
- [x] `replace_all_with` (Monolith) → `type: replace, replaces: gauss_flux_arc`

### Schritt C — `Unit`-Dataclass + Loader vervollständigen ✅

- [x] `WargearOption`, `DamageBracket` Dataclasses in `unit.py`
- [x] `Unit` um `power_level`, `attacks`, `wargear_options`, `damage_bracket` erweitert
- [x] `loader.py`: `_wargear_option_from_dict`, `_damage_bracket_from_dict`, `load_unit_catalog()`
- [x] Orks-legacy `army.yaml` via Defaults kompatibel gehalten
- [x] 306 Tests grün

**Forge World / Legends entsprechend des Datenschemas importieren:** Night Shroud, Canoptek Tombstalker, Canoptek Acanthrites, Tesseract Ark, Canoptek Tomb Sentinel, Gauss Pylon, Seraptek Heavy Construct, Sentry Pylon.

---

## 5c — Loader-Refactoring 🔄

Schritt C hat die Dataclass-Seite abgeschlossen. Noch offen:

- [ ] `damage_bracket` zur Laufzeit auflösen: aktive Stats eines Vehicles abhängig von Woundstand (z.B. Triarch Stalker zeigt aktuell immer Basis-Stats, nicht bracketed Stats)
- [ ] `gameObjects/loader.py` — Roster-Flow: liest `data/rosters/<name>.yaml`, löst IDs gegen Katalog auf
- [ ] `power_level`-Skalierung: PL × (aktuelle_modelle / models_min)
- [ ] `points.yaml` einbinden
- [ ] Default-Nahkampfwaffe-Logik im Loader (immer ergänzen wenn fehlend)
- [ ] Unmatched-Einheiten: Warning im Setup, nicht spielbar

**Hinweis UI:** Die neuen Felder (`power_level`, `attacks`, `wargear_options`, `damage_bracket`) sind reine Datenschicht-Erweiterungen — die bestehende UI nutzt sie noch nicht. `damage_bracket` ist die spielmechanisch dringendste Lücke.

---

## 5d — BattleScribe Importer

BattleScribe-Format (recherchiert 2026-05-30):
- `.rosz` = ZIP mit einer `.ros`-Datei (UTF-8 XML), Python stdlib reicht
- XML-Namespace: `http://www.battlescribe.net/schema/rosterSchema`
- Alle Statlines direkt im XML (M/WS/BS/S/T/W/A/Ld/Save + Waffenprofile)
- `invuln_save` + FNP nur per Regex aus Ability-Text
- `oc` existiert in 9E-Daten nicht (10E-Stat) → Default 0
- Weapon-Attacks stecken im `Type`-String (`"Rapid Fire 2"` → 2 Attacks)

Implementierung:
- [ ] `tools/import_rosz.py` — parst `.rosz` XML → matched gegen Katalog → `data/rosters/<name>.yaml`
- [ ] Streamlit-Upload-UI im Setup-Screen integriert
- [ ] Sicherheit: Dateiformat-Validierung (`.rosz`/`.ros`), Max-Größe, XML-Namespace-Check
- [ ] Unmatched-Kategorie: Einheiten ohne Katalog-Treffer werden explizit geflaggt
- [ ] `invuln_save` + FNP via Regex aus Ability-Text extrahieren

---

## 5e — Setup-Screen Redesign

Matched Play Spielgrößen (aus Wahapedia):

| Spielgröße | Punkte | CP |
|---|---|---|
| Combat Patrol | 500 | 3 |
| Incursion | 1000 | 6 |
| Strike Force | 2000 | 12 |
| Onslaught | 3000 | 18 |

Implementierung:
- [ ] Spielmodus-Auswahl: Matched / Open / Crusade
- [ ] Spielgröße: Combat Patrol (500 Pkt) / Incursion (1000) / Strike Force (2000) / Onslaught (3000)
- [ ] Roster-Dropdown aus `data/rosters/` — P1-Wahl sperrt für P2 (keine doppelte Armeewahl)
- [ ] Erster Spieler festlegen
- [ ] Start-Button erst aktiv wenn alle Bedingungen erfüllt
- [ ] `game_state.init_state()` mit Spielmodus + Spielgröße + Roster-Pfaden erweitern

---

## 5f — Stratagems Proof of Concept

- [x] `data/wh40k_9e/necrons/stratagems.yaml` — 59 Stratagems, verifiziert (2026-05-30)
- [ ] `data/wh40k_9e/orks/stratagems.yaml`
- [ ] Loader + `game_state` für Stratagems erweitern
- [ ] Stratagem-Anzeige: zunächst nur lesend (kein automatischer Effekt)
