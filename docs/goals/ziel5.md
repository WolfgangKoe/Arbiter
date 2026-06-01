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

## 5e — Setup-Screen Redesign

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

- [ ] **Architektur-Umbau `game_state.py`**: Roster-Globals von Modul-Ebene in `init_state(roster_p1, roster_p2, game_mode, game_size, vp_phase)` verschieben — kritischer erster Schritt
- [ ] Spielmodus-Auswahl: Matched / Open / Crusade
- [ ] Spielgröße-Auswahl: Combat Patrol / Incursion / Strike Force / Onslaught + CP-Initialisierung
- [ ] Roster-Dropdown aus `data/rosters/` — P1-Wahl sperrt für P2 (keine doppelte Armeewahl)
- [ ] Siegpunkt-Zählphase wählen (Dropdown: alle 7 Phasen)
- [ ] Erster Spieler festlegen
- [ ] Start-Button erst aktiv wenn alle Bedingungen erfüllt (Modus, Größe, beide Roster, VP-Phase)
- [ ] `unmatched`-Warnungen im Setup-Screen anzeigen (Einheiten die nicht im Katalog gefunden wurden)
- [ ] gameHeader: VP/CP-Buttons entfernen, nur Anzeige behalten
- [ ] gameActionsArea: DisplayArea nach oben verschieben (vor PlayerAreas rendern)
- [ ] VP-Buttons (+5/−5) in displayArea am Ende der konfigurierten Phase einblenden

**Absehbare Lücken:**
- `game_state.py` hat aktuell **hartcodierte** Roster-Dateipfade (`necrons_alpha.yaml`, `necrons_beta.yaml`) auf Modul-Ebene — muss für dynamische Roster-Auswahl grundlegend umgebaut werden.
- Punkte-Validierung: `load_points()` ist implementiert, aber nichts summiert die Punkte eines Rosters gegen die Spielgröße.

---

## 5f — Stratagems Proof of Concept

- [x] `data/wh40k_9e/necrons/stratagems.yaml` — 59 Stratagems, verifiziert (2026-05-30)
- [ ] `data/wh40k_9e/orks/stratagems.yaml`
- [ ] Loader + `game_state` für Stratagems erweitern
- [ ] Stratagem-Anzeige: zunächst nur lesend (kein automatischer Effekt)

---

## Offene Querschnittslücken

Diese Punkte fallen quer durch mehrere Ziele — explizit festhalten damit sie nicht untergehen:

| Lücke | Beschreibung | Relevant für |
|-------|-------------|--------------|
| `resolve_bracket_stats` unverdrahtet | Implementiert in `loader.py`, aber kein Phase-Handler ruft es auf. Vehicle-Stats (Annihilation Barge, Triarch Stalker etc.) ändern sich nicht live beim Schaden. | 5e oder eigenes Ziel |
| Orks-Fraktion fehlt | Nur Legacy `army.yaml`, kein `units.yaml`. Ziel 5c.6 war geplant aber nicht umgesetzt. Orks können nicht als vollständige zweite Fraktion genutzt werden. | 5e (Roster-Auswahl braucht reale zweite Fraktion) |
| Forge World / Legends Necrons | Nicht im Katalog: Night Shroud, Canoptek Tombstalker, Canoptek Acanthrites, Tesseract Ark, Canoptek Tomb Sentinel, Gauss Pylon, Seraptek Heavy Construct, Sentry Pylon. Müssen nach Datenschema in `units.yaml` + `weapons.yaml` eingetragen werden. | nach 5d/5e, eigenes Ziel |
| Datasheet-Anzeige Dual-Profile | `gameActionsArea.py` zeigt im Setup-Phase nur `profiles[0]` einer Waffe — Staff of Light zeigt nur Shooting-Profil. Kein Bug, aber UX-Lücke. | 5e Setup-Screen |
| Keyword-Checks | Alle zukünftigen Keyword-Checks müssen `UPPERCASE` nutzen (units.yaml-Konvention). Bisher nur MWBD-Bug gefunden — weitere könnten bei neuen Features auftreten. | alle |
