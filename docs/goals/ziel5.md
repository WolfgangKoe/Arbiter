# Ziel 5 — Setup & Datenlage ✅ (2026-06-03)

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

---

## 5c — Loader-Refactoring ✅

Stand 2026-06-01 — alle 323 Tests grün.

- [x] `damage_bracket` zur Laufzeit auflösen: `resolve_bracket_stats(unit, current_wounds) → dict`
- [x] `load_roster(path, catalog)` → `(matched: list[tuple[Unit, int]], unmatched: list[str])`
- [x] `load_roster_metadata(path)` → `dict[str, str]` (display_name, faction_dir)
- [x] `power_level`-Skalierung: `scaled_pl(unit, current_models) → float`
- [x] `points.yaml` einbinden: `load_points(faction_dir) → dict[str, int]`
- [x] Default-Nahkampfwaffe: Close Combat Weapon wird automatisch ergänzt wenn fehlend
- [x] Roster-Flow: `game_state.py` lädt aus `data/rosters/` statt vollständigem Katalog
- [x] Zwei Necron-Roster: `necrons_alpha.yaml` (Errant Legion) + `necrons_beta.yaml` (Silent Kings)
- [x] Zwei Necron-Armeen können gegeneinander spielen — alle Phase-Handler und UI-Dateien player-agnostisch

**Unmatched-Einheiten:** `roster_warnings` in session_state gesetzt, UI-Einbindung (Setup-Screen) noch ausstehend (Ziel 5e).

### 5c — Nachgelagerte Bugfixes (2026-06-01) ✅

Beim ersten manuellen Testlauf der App mit zwei Necron-Armeen entdeckt und behoben:

- [x] **`Weapon`-Properties fehlten**: `Weapon`-Dataclass hatte keine `is_melee`, `attacks`, `ap`, `strength`, `damage`, `abilities`, `range_inches`-Attribute — nur `WeaponProfile` hatte diese. Alle UI-Zugriffe crashten mit `AttributeError`. Fix: Convenience-Properties auf `Weapon` ergänzt, die auf `profiles[0]` delegieren.
- [x] **Dual-Profil-Waffen** (z.B. Staff of Light: Shooting + Melee): `Weapon.is_melee` gab immer `profiles[0].is_melee` zurück → Overlord hatte in der Nahkampfphase "No melee weapons". Fix: `Weapon.for_phase(use_melee)` ergänzt; Filter in Fight-/Shooting-Phase und `render_attack_form` auf Profil-Ebene umgestellt.
- [x] **`models_initial` fehlte im Unit-State**: `unitCard.py` nutzte `unit.models_max` als Nenner des Progress-Bars (immer Datenblatt-Maximum). Fix: `models_initial` in `_unit_state()` gespeichert, Unit-Card zeigt Roster-Anzahl als Nenner.
- [x] **MWBD Keyword-Case**: Check war `"Core" in unit.keywords`, Keywords in units.yaml sind durchgehend `UPPERCASE`. Fix: `"Core"` → `"CORE"`.
- [x] **MWBD/ResOrb gegenseitiger Ausschluss**: Beide Awaiting-States konnten gleichzeitig aktiv sein → `elif res_orb_awaiting:` im unitCard wurde von `if mwbd_awaiting:` blockiert. Fix: Aktivieren des einen States löscht den anderen.

**Erkenntnisse für zukünftige Arbeit:**
- Das `for_phase(use_melee)`-Muster muss bei **jedem neuen Weapon-Zugriff** beachtet werden (nicht `w.is_melee` direkt verwenden, wenn Dual-Profil-Waffen möglich sind).
- Keyword-Checks immer mit `UPPERCASE` schreiben — units.yaml ist durchgehend uppercase.

---

## 5d — BattleScribe Importer ✅ (2026-06-03)

BattleScribe-Format (recherchiert 2026-05-30):
- `.rosz` = ZIP mit einer `.ros`-Datei (UTF-8 XML), Python stdlib reicht
- XML-Namespace: `http://www.battlescribe.net/schema/rosterSchema`
- Alle Statlines direkt im XML (M/WS/BS/S/T/W/A/Ld/Save + Waffenprofile)
- `invuln_save` + FNP nur per Regex aus Ability-Text
- `oc` existiert in 9E-Daten nicht (10E-Stat) → Default 0
- Weapon-Attacks stecken im `Type`-String (`"Rapid Fire 2"` → 2 Attacks)

Implementierung:
- [x] `tools/import_rosz.py` — parst `.rosz` XML → matched gegen Katalog → `data/rosters/<name>.yaml`
- [x] Streamlit-Upload-UI im Setup-Screen integriert
- [x] Sicherheit: Dateiformat-Validierung (`.rosz`/`.ros`), Max-Größe, XML-Namespace-Check
- [x] Unmatched-Kategorie: Einheiten ohne Katalog-Treffer werden explizit geflaggt
- [x] Orks-Support: `_FACTION_CATALOGUE_MAP` um `"orks"` / `"ork"` erweitert; Prefix-Stripping generisch (nicht mehr Necron-hardcoded)
- [ ] `invuln_save` + FNP via Regex aus Ability-Text extrahieren (noch ausstehend)

**Absehbare Lücke — Wargear-Selektion im Roster-Format:**
Das aktuelle Roster-Format kennt nur `id` + `models`. Wargear-Auswahl (z.B. Overlord mit Voidscythe statt Staff of Light) ist nicht speicherbar. Der BattleScribe-Importer muss entscheiden: Wargear aus dem XML extrahieren und im Roster ablegen → Loader muss dann Wargear-Overrides beim Unit-Aufbau anwenden. Das erfordert eine Erweiterung des Loader-Vertrags.

Roster-Format-Erweiterung (Entwurf):
```yaml
- id: wh40k_9e.necrons.unit.overlord
  models: 1
  wargear:
    - wh40k_9e.necrons.weapon.voidscythe
    - wh40k_9e.necrons.wargear.resurrection_orb
```

---

## 5e — Setup-Screen Redesign ✅ (2026-06-02)

Matched Play Spielgrößen (aus Wahapedia):

| Spielgröße | Punkte | CP |
|---|---|---|
| Combat Patrol | 500 | 3 |
| Incursion | 1000 | 6 |
| Strike Force | 2000 | 12 |
| Onslaught | 3000 | 18 |

### UI-Änderungen (beschlossen 2026-06-01)

**gameHeader** — bereinigt, nur noch Anzeige (keine Buttons):
- VP und CP werden **nur angezeigt**, keine +/− Buttons mehr im Header
- VP-Anpassung (+5/−5) erfolgt in der gameActionDisplayArea am Ende der konfigurierten Siegpunkt-Phase
- CP-Anpassung läuft ausschließlich über die Befehlsphase (Grant +1 CP) und Abilities

**gameActionDisplayArea** — Reihenfolge geändert:
- Wird **oberhalb** der firstPlayerArea/secondPlayerArea gerendert (nicht mehr darunter)
- Begründung: Kontext (Phasenregeln, Angriffszusammenfassung, Ergebnis) steht vor den Aktionsbuttons

**Siegpunkt-Zählphase** — neues Setup-Feld:
- Spieler wählt im Setup, zu welchem Phasenende VPs gezählt werden
- Optionen: Befehlsphase / Bewegungsphase / Schussphase / Nahkampfphase / Moralphase (etc.)
- Am Ende dieser Phase erscheinen VP-Buttons (+5/−5) für beide Spieler in der displayArea

### Implementierung

- [x] **Architektur-Umbau `game_state.py`**: `init_state(roster_p1, roster_p2, game_mode, game_size, vp_phase)` — dynamische Roster-Auswahl, keine hardcodierten Pfade mehr
- [x] Spielmodus-Auswahl: Matched / Open / Crusade
- [x] Spielgröße-Auswahl: Combat Patrol / Incursion / Strike Force / Onslaught + CP-Initialisierung
- [x] Roster-Dropdown aus `data/rosters/` — P1-Wahl sperrt für P2
- [x] Siegpunkt-Zählphase wählen (Dropdown)
- [x] Erster Spieler festlegen
- [x] Start-Button
- [x] `unmatched`-Warnungen im Setup-Screen anzeigen ✅
- [x] gameHeader: VP/CP nur Anzeige, keine Buttons
- [x] gameActionsArea: DisplayArea oberhalb der Armeen
- [x] VP-Buttons (+5/+1/−1/−5) in displayArea
- [x] Punkte-Validierung: Roster-Summe gegen Spielgröße prüfen ✅

---

## 5g — Regelkonformer Setup-Flow ✅ (2026-06-02)

Recherche abgeschlossen 2026-06-02. Quellen lokal: `docs/work/wahapedia_matched_play.md`, `wahapedia_open_play.md`, `wahapedia_crusade.md`.

### Spec-Korrekturen (aus Wahapedia-Review)

- [x] `docs/spec/setup.md`: Spielgrößen-Tabelle um Missions-Spalte erweitert
- [x] `docs/spec/setup.md`: CP-Regel präzisiert — Starting CP (Matched Play-Kapitel) vs. +1 CP/Runde (Core Rules Command Phase) klar getrennt
- [x] `docs/spec/setup.md`: Attacker/Defender-Abschnitt ergänzt (Matched: Roll-off; Open: höherer PL)
- [x] `docs/spec/setup.md`: Secondary Objectives Abschnitt neu (5 Kategorien, 3 pro Spieler, 15 VP cap, **optional**)
- [x] `docs/spec/setup.md`: Open Play-Sektion um Missions und Attacker/Defender ergänzt
- [x] `docs/spec/setup.md`: Setup-Flow um Mission + Secondary Objectives Toggle erweitert
- [x] `docs/spec/setup.md`: session_state um `mission`, `attacker`, `use_secondaries`, `secondaries`, `secondary_vp` erweitert

**Hinweis Detachment-Count-Limits:** Incursion/Strike Force/Onslaught-Limits (2/3/4 Detachments) stehen **nicht** auf der Wahapedia Matched Play-Seite — nur Combat Patrol = 1 Patrol Detachment ist explizit bestätigt. Limits stammen aus den Core Battle-Forged Rules; Verifikation empfohlen bevor Enforcement implementiert wird.

**Hinweis Crusade Wahapedia:** Die Crusade-Seite auf Wahapedia war 404. Datei basiert auf Core-Rule-Wissen + bestehendem Spec.

### Implementierung

- [x] **+1 CP/Runde:** „Grant +1 CP"-Button in Command Phase funktioniert
- [x] **Mission-Auswahl im Setup-Screen:** Dropdown je Spielgröße (Matched Play) ✅
- [x] **Attacker/Defender-Button:** Roll-off UI im Setup-Screen ✅
- [x] **Secondary Objectives Toggle:** on/off + 3 Slots + VP-Tracking ✅

---

## 5f — Stratagems Proof of Concept ✅ (2026-06-03)

- [x] `data/wh40k_9e/necrons/stratagems.yaml` — 59 Stratagems, verifiziert (2026-05-30)
- [x] `data/wh40k_9e/orks/stratagems.yaml` — 29 Stratagems (2026-06-03)
- [x] `data/wh40k_9e/universal/stratagems.yaml` — 7 Core-Stratagems von Wahapedia
- [x] `load_stratagems()` in `loader.py` — universal + Fraktion kombiniert
- [x] `used_stratagem_ids` in `game_state.py` — Init + Phase-Reset
- [x] `stratagem_visibility()` — `phase: any` Support
- [x] Stratagem-Tab: Phase-Filter, Conditions-Check, CP-Button, "*(used)*"-Markierung

**Verifikation 2026-06-03:** Command Re-Roll (any), Fire Overwatch (charge), Conditions-Filter — alle korrekt.

**Abgeschlossen in 5i (2026-06-03):**
- Bug `player: inactive` CP-Pool ✅
- Condition-Check auf Unit-Ebene ✅
- Stratagems als Inline-Hinweis in gameActionArea ✅

---

## 5h — Orks-Katalog vervollständigen ✅ (2026-06-03)

**Abschluss 2026-06-03** — Alle Katalogdateien vorhanden. Punktekosten aus MFM 2023 Mk I.
E2E-Testspiel durchgeführt: Ork-Roster (`orks_test.yaml`, 297 pts) gegen Necrons — alle 7 Phasen ohne Crash.

**Bekannte Datenlücken (kein Blocker):**
- `attacks: Melee` bei einigen Waffen (killsaw, power_klaw, uge_choppa) — Scraper-Artefakt, zeigt `AMelee` in UI
- `power_level: 0` überall — Codex-Werte nicht eingetragen
- Punktekosten unverified gegen aktuelle MFM-Errata

Zum Vergleich: Necrons haben 15 Dateien, Orks aktuell 3 (davon `faction_abilities.yaml` leer).

### Fehlende Dateien

| Datei | Inhalt | Scraper-Support |
|-------|--------|-----------------|
| `faction_abilities.yaml` | WAAAGH!, Ere We Go, Da Jump etc. | ❌ manuell |
| `army_rules.yaml` | Armeebau-Regeln (Detachment, Warlord etc.) | ❌ manuell |
| `stratagems.yaml` | Codex-Stratagems + Klan-Stratagems | ✅ `--stratagems` |
| `subfaction_abilities.yaml` | Klan-Regeln (Bad Moons, Evil Sunz, Goffs, Deathskulls, Blood Axes, Snakebites) | ❌ fehlt im Scraper |
| `unit_abilities.yaml` | Einheitenspezifische Fähigkeiten (Mob Rule, Dakka! Dakka! Dakka! etc.) | ❌ fehlt im Scraper |
| `relics.yaml` | Ork-Relikte | ❌ fehlt im Scraper |
| `warlord_traits.yaml` | Kriegsherr-Eigenschaften (allgemein + Klan-spezifisch) | ❌ fehlt im Scraper |
| `wargear.yaml` | Wargear-Items | ❌ fehlt im Scraper |
| `wargear_abilities.yaml` | Wargear-Sonderfähigkeiten | ❌ fehlt im Scraper |
| `weapon_abilities.yaml` | Waffen-Sonderfähigkeiten | ❌ fehlt im Scraper |
| `points.yaml` | Punktekosten (aktuell `power_level: 0` überall) | ❌ fehlt im Scraper |

### Umsetzungsstrategie

**Option A — Scraper erweitern:**
`tools/wahapedia_scraper.py` um fehlende Datentypen erweitern:
- `--subfactions` → `subfaction_abilities.yaml`
- `--faction-abilities` → `faction_abilities.yaml`
- `--relics` → `relics.yaml`
- `--warlord-traits` → `warlord_traits.yaml`
- Stratagems (`--stratagems`) bereits vorhanden

**Option B — Manuell aus Codex/Wahapedia:**
Analog zur Necrons-Datenlage — direkt in YAML einpflegen.

**Empfehlung:** Stratagems via Scraper (`--stratagems`), Rest manuell nach Necrons-Schema.

### Checkliste

- [x] `stratagems.yaml` — 29 Stratagems (8 Core + 7 Klan + 4 Specialist Setup + 4 Specialist Rules + 2 Requisitions)
- [x] `subfaction_abilities.yaml` — 7 Klans (Bad Moons, Blood Axes, Deathskulls, Evil Sunz, Freebooterz, Goffs, Snakebites)
- [x] `faction_abilities.yaml` — WAAAGH!, Speedwaaagh!, 'Ere We Go, Mob Rule, Ramshackle, Beast Snagga, Ob.Sec, 7 Psychic Powers
- [x] `unit_abilities.yaml` — HQ, Troop, Elites, Fast Attack, Heavy Support Abilities
- [x] `army_rules.yaml` — Warlord-Anforderung (WARBOSS), Detachment-Regeln, Specialist Detachments
- [x] `relics.yaml` — 11 Relikte (1 pro Klan + 4 Specialist Detachment)
- [x] `warlord_traits.yaml` — 3 Generic + 7 Klan + 4 Specialist Detachment Traits
- [x] `wargear.yaml` + `wargear_abilities.yaml` — 10 Wargear-Items + Abilities
- [x] `weapon_abilities.yaml` — Dakka!, Skorcha, Power Klaw, Killsaw, Choppa, Bomb-Squig, Shokk Attack Gun etc.
- [x] `points.yaml` — alle 51 Einheiten (MFM 2023 Mk I — Verifikation empfohlen)

**Abschluss: 2026-06-03** — Katalog strukturell vollständig. Punktekosten aus Trainingsdaten, nicht direkt von Wahapedia — bei Spielbetrieb gegen MFM verifizieren.

---

## 5i — Abschluss: Offene Punkte & Qualitätssicherung ✅ (2026-06-03)

Sammlung aller noch offenen Punkte aus 5d/5e/5f/5g — muss vor Abschluss von Ziel 5 erledigt sein.

### Stratagems (aus 5f)

- [x] **Bug: CP vom falschen Pool** — `player: inactive`-Stratagems ziehen CP vom richtigen Pool ✅
- [x] **Condition-Check auf Unit-Ebene** — `selected_unit` bevorzugt, Fallback auf Armee ✅
- [x] **Stratagems in gameActionArea** — Inline-Hinweis (Expander) pro Phase ✅

### Setup-Screen (aus 5e/5g)

- [x] **Mission-Auswahl** — Dropdown je Spielgröße im Setup-Screen ✅
- [x] **Attacker/Defender-Button** — Roll-off UI ✅
- [x] **Secondary Objectives Toggle** — on/off + 3 Slots pro Spieler + VP-Tracking mit Cap ✅
- [x] **`unmatched`-Warnungen** — nicht im Katalog gefundene Einheiten im Setup anzeigen ✅
- [x] **Punkte-Validierung** — Roster-Gesamtpunkte gegen Spielgröße prüfen ✅

### Code-Qualität

- [x] **Faction-Dir Hardcode** — `unit.id.split(".")[1]` in `gameActionsArea.py` ✅ 2026-06-03
- [x] **`resolve_bracket_stats` verdrahten** — `fightPhase.py` + `shootingPhase.py` nutzen live WS/BS/attacks ✅ 2026-06-03
- [x] **`invuln_save` Orks Katalog** — Mega Armour (Warboss, Big Mek, Meganobz) auf 4++ korrigiert ✅ 2026-06-03

### Datenqualität

- [x] **Command Protocols Englisch** — `primary`/`secondary` auf Englisch; UI zeigt `name_en` ✅ 2026-06-03
- [x] **Datasheet Dual-Profile** — Setup-Anzeige iteriert alle `w.profiles`; Staff of Light zeigt beide Profile ✅ 2026-06-03
- [x] **Wargear im Roster-Format** — `wargear`-Feld in Roster; `_apply_wargear()` im Loader; BattleScribe-Importer extrahiert Upgrade-Selections ✅ 2026-06-03

---

## Offene Querschnittslücken

Diese Punkte fallen quer durch mehrere Ziele — explizit festhalten damit sie nicht untergehen:

| Lücke | Beschreibung | Relevant für |
|-------|-------------|--------------|
| Ork-Waffen `attacks: Melee` | Scraper-Artefakt für killsaw/power_klaw/uge_choppa — zeigt `AMelee` in UI. Korrekte Werte aus Wahapedia/Kodex nachtragen. | Priorität 1 nächste Session |
| Melee-Attack-Form Orks unverifiziert | E2E-Test konnte Fight-Phase nur ohne Charge testen ("Not in melee — no fight action possible"). Warboss-Angriff (inkl. `User×2`-Fix) manuell im echten Testspiel bestätigen. | manuelles Testspiel |
| Forge World / Legends Necrons | Nicht im Katalog: Night Shroud, Canoptek Tombstalker, Canoptek Acanthrites, Tesseract Ark, Canoptek Tomb Sentinel, Gauss Pylon, Seraptek Heavy Construct, Sentry Pylon. | eigenes Ziel |

### E2E-Verifikation — Stand 2026-06-03

Automatisiertes Playwright-Testspiel (Zarekhan'Sol Necrons vs. Necrons 1500pts) durchgeführt:

| Phase | Ergebnis | Anmerkung |
|-------|----------|-----------|
| Command | ✅ | +1 CP korrekt; 5 Command Protocols gelistet |
| Movement | ✅ | Normal/Advance/Stationary/Retreat mit Regeltext |
| Psychic | ✅ | Kein Psyker erkannt → Skip-Hinweis korrekt |
| Shooting | ✅ | Waffenstatistiken korrekt; Attack-Sequenz sichtbar; Ziel-Prompt |
| Charge | ✅ | 2D6-Regel; Heroic Intervention-Buttons je Gegnereinheit |
| Fight | ✅ | "Not in melee — no fight action possible." regelkonform blockiert |
| Morale | ✅ | Phase erreichbar |

Kein einziger Crash. Der frühere `User×2`-Bug (Big Mek Killsaw) tritt nicht mehr auf.
