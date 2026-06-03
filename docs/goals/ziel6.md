# Ziel 6 — Refactoring & Konsolidierung ⬜

**Voraussetzung:** Ziel 5 vollständig abgeschlossen.

Bevor neue Features (Crusade, Faction Fetcher) kommen, wird die bestehende Grundfunktionalität in einen stabilen, erweiterbaren Stand gebracht. Kein neues Feature — ausschließlich Qualität, Korrektheit und Wartbarkeit.

---

## 6a — Stratagems Verbesserungen

### Bug: CP vom falschen Pool

`player: inactive`-Stratagems (Fire Overwatch, Counter-Offensive, Cut Them Down) werden vom CP-Pool des **aktiven** Spielers abgezogen. Korrekt: immer den Spieler verwenden, dem das Stratagem gehört.

- [ ] `gameProtocoll.py`: spendierenden Spieler anhand `strat.player` bestimmen:
  - `player: active` → aktiver Spieler
  - `player: inactive` → inaktiver Spieler
  - `player: both` → Button pro Spieler oder Spieler-Auswahl

### Condition-Check auf Unit-Ebene

Aktuell: Stratagem sichtbar wenn **irgendeine** Unit im Roster das Keyword hat.
Ziel: Stratagem sichtbar wenn die **selected unit** das Keyword hat (sofern eine Unit ausgewählt ist).

- [ ] `_conditions_met()` um `selected_unit`-Check erweitern:
  - Wenn `st.session_state.selected_unit` gesetzt → nur diese Unit prüfen
  - Wenn keine Unit selected → Armee-Level-Check (Fallback wie bisher)

### Stratagems in der gameActionArea

Beim Auswählen einer Aktion (z.B. Unit schießt) werden relevante Stratagems inline angezeigt:

- [ ] Pro Phasenaktion: passende Stratagems nach Phase + Conditions filtern
- [ ] Aktiver Spieler: Stratagems mit `player: active/both` zeigen
- [ ] Reaktiver Spieler: Stratagems mit `player: inactive/both` separat hervorheben
- [ ] Format: kompakter Hinweis (Name + CP-Kosten + ein Satz Regeltext), kein voller Expander

---

## 6b — Code-Qualität

### Faction-Dir Hardcode entfernen

`gameActionsArea._display_unit_datasheet` prüft `"necrons" in unit.id` — fragil bei neuen Fraktionen.

- [ ] `faction_dir_for(player)` aus `game_state.py` verwenden
- [ ] Unit-ID enthält kein Fraktions-Hardcoding mehr

### `resolve_bracket_stats` verdrahten

`loader.py` implementiert `resolve_bracket_stats(unit, current_wounds) → dict`, aber kein Phase-Handler ruft es auf. Vehicles zeigen immer Basis-Stats, auch wenn stark beschädigt.

- [ ] Fight-Phase + Shooting-Phase: Stats vor Angriffskalkulation auflösen
- [ ] `render_attack_form`: Strength aus aufgelösten Stats (nicht Unit-Default)

### `invuln_save` + FNP via BattleScribe Regex

BattleScribe-Importer extrahiert Invuln und FNP noch nicht aus Ability-Texten.

- [ ] `tools/import_rosz.py`: Regex-Extraktion analog zu Wahapedia-Scraper (`_parse_invuln`, `_parse_fnp`)
- [ ] Felder in importiertem Roster setzen

---

## 6c — Datenqualität

### Command Protocols: Englische Namen

`necrons/command_protocols.yaml` enthält deutsche Bezeichnungen ("Protokoll des Ewigen Wächters"), App-UI ist Englisch.

- [ ] `command_protocols.yaml`: `name_en` auf Englisch nachtragen (Quelle: Wahapedia)
- [ ] `gameProtocoll.py`: auf `name_en` umstellen (statt `name_de`)

### Datasheet Dual-Profile vollständig anzeigen

Setup-Phase zeigt bei Waffen mit mehreren Profilen nur `profiles[0]`.

- [ ] `gameActionsArea._display_unit_datasheet`: alle Profile iterieren und anzeigen

### Wargear im Roster-Format

Roster kennt nur `id` + `models` — Wargear-Selektion (z.B. Overlord mit Voidscythe statt Staff of Light) nicht speicherbar.

- [ ] Roster-Format um optionales `wargear`-Feld erweitern (Liste von Weapon-IDs)
- [ ] `loader.py`: Wargear-Overrides beim Unit-Aufbau anwenden
- [ ] `import_rosz.py`: Wargear aus BattleScribe-XML extrahieren

---

## 6d — Offene Ziel-5-Restpunkte

### Setup-Screen

Aus 5e/5g noch ausstehend:

- [ ] Mission-Auswahl im Setup-Screen (Dropdown je Spielgröße)
- [ ] Attacker/Defender-Button (Roll-off UI)
- [ ] Secondary Objectives Toggle (optional, default off)
- [ ] `unmatched`-Warnungen im Setup-Screen anzeigen
- [ ] Punkte-Validierung: Roster-Summe gegen Spielgröße prüfen

### BattleScribe Importer

- [ ] `invuln_save` + FNP via Regex (→ 6b)
- [ ] Wargear-Extraktion (→ 6c)

---

## Nicht in Ziel 6

- Forge World / Legends Necrons → eigenes Ziel
- Neue Fraktionen → Ziel 8 (Faction Fetcher)
- Crusade-Persistenz → Ziel 7
