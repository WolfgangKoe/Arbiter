# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session passiert ist

### Ziel 5g — Wahapedia-Recherche Spielaufbau-Regeln (2026-06-02)

Regeln für alle drei Spieltypen (Matched / Open / Crusade) von Wahapedia abgerufen und lokal gespeichert:
- `docs/work/wahapedia_matched_play.md` — 16-Schritt-Sequenz, Spielgrößen, Secondaries, VP-System
- `docs/work/wahapedia_open_play.md` — 12 Schritte, 3 Missionen (Annihilation / Hold at All Costs / Death or Glory)
- `docs/work/wahapedia_crusade.md` — Crusade-Überblick (Wahapedia-Seite war 404; aus Core-Rule-Wissen)

`docs/spec/setup.md` korrigiert und erweitert:
- Secondary Objectives neu in Spec (5 Kategorien, 3 pro Spieler, 15 VP cap, **optional via Toggle**)
- Attacker/Defender-Mechanik ergänzt (Matched: Roll-off; Open: höherer PL)
- Mission-Dropdown je Spielgröße ergänzt
- session_state um `mission`, `attacker`, `use_secondaries`, `secondaries`, `secondary_vp` erweitert
- `docs/goals/ziel5.md`: Abschnitt 5g mit allen offenen Implementierungsaufgaben

### UI-Bugfixes (2026-06-02)

1. **CSS-Injection in `app.py` ganz nach oben verschoben** — vorher nur in `render_game_header()`, was
   den Setup-Screen ohne Dark-Theme ließ. Jetzt gilt das Theme für alle Screens.

2. **Borders auf armyCard / unitCard** — `[data-testid="stVerticalBlockBorderWrapper"]` existiert in
   Streamlit 1.57 nicht. Korrekte Lösung: `.e1rw0b1u3` (Emotion-Zielklasse für flex container).
   `border-color` override wirkt nur wo `border-style: solid` bereits gesetzt ist (border=True) —
   nicht-bordered Container bleiben unverändert.

3. **Button-Farben in der Movement-Phase** — data-testid änderte sich in Streamlit 1.57:
   `baseButton-primary` → `stBaseButton-primary`. CSS-Selektoren angepasst.

4. **gameActionDisplayArea jetzt oben** — alle Phase-Handler umgebaut:
   - Movement, Command, Charge: `PHASE_RULES`-Text vor die Columns verschoben
   - Shooting, Fight: `_render_display()` (Angriffs-Form oder Regeltext) vor die Columns
   - In `gameActionsArea.py`: `_render_vp_scoring()` läuft vor `render_current_phase()`
   - In `_render_setup()`: Datasheet/Instructions zuerst, First-Player-Auswahl darunter

### Stand nach Session
- 323 Tests grün
- CSS-Theme gilt für Setup-Screen und Spiel-Screen
- Layout laut Spec: displayArea oben, PlayerAreas unten

---

## Aktueller Status

| Ziel | Status |
|------|--------|
| 5a — Spec | ✅ |
| 5b — Necron-Katalog | ✅ |
| 5b.2 — Datensäuberung | ✅ |
| 5c — Loader-Refactoring | ✅ |
| 5c — Bugfixes (Weapon, MWBD, ResOrb) | ✅ |
| 5e — Setup-Screen Redesign + VP-Config + Header | ✅ |
| 5g — Spec-Erweiterung (Wahapedia-Review) | ✅ Spec fertig, Implementierung offen |
| 5d — BattleScribe Importer | ⬜ |
| 5f — Stratagems PoC | ⬜ |

---

## Nächste Schritte (priorisiert)

### Priorität 1 — Ziel 5g: Setup-Screen erweitern (Spec ist fertig, jetzt implementieren)

Alle nötigen Felder sind in `docs/spec/setup.md` und `docs/goals/ziel5.md § 5g` beschrieben.
Reihenfolge:

1. **Spielmodus-Auswahl** (Matched / Open / Crusade) — aktuell fehlt die Modus-Dropdown komplett im Setup-Screen
2. **Mission-Dropdown** je Spielgröße (Matched Play: 3–6 Missionen, in `wahapedia_matched_play.md`)
3. **Attacker/Defender Roll-off-Button** im Setup-Screen
4. **Secondary Objectives Toggle** + Picker (3 Slots pro Spieler, 1 pro Kategorie erzwungen)
5. **VP-Tracking für Secondaries** (je Objective 0–15 VP, Cap-Enforcement)
6. **Architektur-Voraussetzung**: `game_state.py` muss `game_mode` (matched/open/crusade) als Parameter in `init_state()` aufnehmen

**Kritischer erster Schritt**: `init_state()` um `game_mode`-Parameter erweitern, danach der Rest.

### Priorität 2 — Ziel 5d: BattleScribe Importer

Jetzt sinnvoll, da 5e die Roster-Auswahl abgeschlossen hat. BattleScribe exportiert `.rosz`-Dateien (ZIP mit XML). Ein Importer konvertiert diese in das `data/rosters/*.yaml`-Format.

Erweiterung Roster-Format um Wargear (Entwurf):
```yaml
- id: wh40k_9e.necrons.unit.overlord
  models: 1
  wargear:
    - wh40k_9e.necrons.weapon.voidscythe
    - wh40k_9e.necrons.wargear.resurrection_orb
```

### Priorität 3 — Orks-Fraktion

Orks haben nur eine Legacy `army.yaml` — kein `units.yaml`. Für echtes Zwei-Fraktionen-Spiel wird eine zweite vollständige Fraktion gebraucht (Wahapedia-Scraper in `tools/wahapedia_scraper.py`).

### Priorität 4 — Ziel 5f: Stratagems PoC

Infrastruktur (GO-Liste, Sichtbarkeitslogik) bereits vorbereitet in `gameProtocoll.py`. Daten fehlen noch.

---

## Bekannte offene Lücken (nicht vergessen)

| Lücke | Beschreibung |
|-------|-------------|
| `game_mode` fehlt in `init_state()` | Setup-Screen hat noch keine Modus-Auswahl — `init_state()` kennt kein matched/open/crusade |
| `resolve_bracket_stats` unverdrahtet | Implementiert, aber kein UI-Aufruf — Vehicles zeigen immer Basis-Stats |
| Orks-Fraktion fehlt | Nur Legacy `army.yaml`, kein `units.yaml` |
| Forge World / Legends importieren | Noch nicht umgesetzt |
| Wargear im Roster-Format | Aktuell nur `id` + `models` — keine Wargear-Auswahl speicherbar |
| Punkte-Validierung | `load_points()` implementiert, aber Roster-Gesamtpunkte werden nicht geprüft |
| Unmatched-UI | `roster_warnings` in session_state, aber kein UI-Feedback im Setup-Screen |
| Dual-Profil Datasheet | Setup-Phase zeigt nur `profiles[0]` einer Waffe im Datasheet-View |
| Faction-Dir Hardcode | `gameActionsArea._display_unit_datasheet` nutzt `"necrons" if "necrons" in unit.id else "orks"` — muss auf `faction_dir_for()` umgestellt werden |
| CP +1/Runde verifizieren | Wahapedia Core Rules Command Phase noch nicht abgerufen — in `_common.py` steht "+1 CP (Battle-forged)" aber Quelle nicht bestätigt |

---

## Wichtige Constraints

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts (unveränderlich während Spiel)
- dev-Branch — kein direktes Committen auf main
- Keywords immer `UPPERCASE` in units.yaml — Checks entsprechend schreiben
- Weapon-Zugriff: Nie `w.is_melee` für Filter nutzen wenn Dual-Profile möglich — `w.for_phase(use_melee)` verwenden
- Session-State Unit-Keys: `p1_units` / `p2_units` (nie wieder `necron_units`/`ork_units`)
- CP wird nur durch Game Mechanics verändert (Befehlsphase, Stratagems) — kein manueller Header-Stepper mehr
- Streamlit 1.57: Button-testid ist `stBaseButton-{kind}` (nicht `baseButton-{kind}`)
- Streamlit 1.57: Borders auf `st.container(border=True)` via `.e1rw0b1u3` CSS-Zielklasse stylen
