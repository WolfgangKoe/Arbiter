# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session passiert ist (2026-06-03 — vierte Session)

### Fix: Melee-Waffen zeigen Unit-A-Stat statt "AMelee" ✅

`attacks: Melee` in `weapons.yaml` ist semantisch korrekt (= "nutze Unit-A-Wert").
Fix in `fightPhase.py`, `_common.py`, `gameActionsArea.py`: wenn `p.attacks in ("Melee", None)` → `str(unit.attacks)` anzeigen.

### Ziel 5f — Stratagems PoC ✅

- `data/wh40k_9e/universal/stratagems.yaml` — 7 Core-Stratagems von Wahapedia core-rules-Seite
- `loader.py`: `load_stratagems(faction_dir)` — lädt universal + Fraktion
- `stratagem.py`: `phase: any` Support in `stratagem_visibility()`
- `game_state.py`: `used_stratagem_ids` in Init + `_reset_phase_state()`
- `gameProtocoll.py`: `_render_stratagems()` — Phase-Filter, Conditions-Check, CP-Buttons, "*(used)*"-Markierung

**Verifikation (Playwright):**
- Command Phase: nur Command Re-Roll (phase:any) sichtbar ✅
- Charge Phase: Command Re-Roll + Fire Overwatch sichtbar ✅
- Conditions-Filter: Ork-Stratagems mit [FLASH GITZ] etc. korrekt versteckt (nicht im Testspiel-Roster) ✅
- Use-Klick: CP 6→5, Stratagem als *(used)* markiert ✅

**Bekannte offene Punkte (→ Ziel 6a):**
- Bug: `player: inactive`-Stratagems ziehen CP vom falschen Pool (aktiver statt inaktiver Spieler)
- Condition-Check nur auf Armee-Ebene, nicht auf selected-Unit-Ebene
- Stratagems fehlen noch in der gameActionArea als Inline-Hinweis

### Zielstruktur bereinigt ✅

- `ziel5.md`: 5e/5f Checkboxen nachgetragen; neuer Abschlussabschnitt **5i** mit allen offenen Punkten aus 5d/5e/5f/5g
- `ziel6.md`: Platzhalter — wird nach Abschluss von Ziel 5 definiert
- `ziel7.md` (ex-6): Crusade · `ziel8.md` (ex-7): Faction Fetcher

---

## Was in dieser Session passiert ist (2026-06-03 — dritte Session)

### Ork-Roster für Testspiel ✅

`data/rosters/orks_test.yaml` angelegt (297 Punkte):
- Warboss in Mega Armour (115 pts)
- Boyz × 10 (70 pts)
- Gretchin × 10 (40 pts)
- Warbikers × 3 (72 pts)

### E2E-Testspiel — Playwright-Verifikation aller Phasen ✅

Alle 7 Phasen (Command → Movement → Psychic → Shooting → Charge → Fight → Morale) durchgespielt, kein einziger Crash.

**Ergebnisse je Phase:**
- **Command:** +1 CP korrekt, Necron Command Protocols (5 Stück) als "available" gelistet
- **Movement:** Normal / Advance / Stationary / Retreat — alle 4 Optionen mit Regeltext korrekt
- **Psychic:** App erkennt "No PSYKER units — skip this phase." automatisch; Gegner: "No PSYKER or Gloom Prism — cannot deny."
- **Shooting:** Unit-Auswahl → Waffenstatistiken korrekt (`Gauss Flayer · A1 · BS3+ · S4 · AP-1 · D1`); "Designate a target (▷)" Prompt erscheint; Attack-Sequenz sichtbar
- **Charge:** Regeltext korrekt (2D6 ≥ Distanz); **Heroic Intervention-Buttons** erscheinen für alle gegnerischen Einheiten
- **Fight:** "Not in melee — no fight action possible." bei Einheiten ohne Charge — regelkonforme Blockierung; kein Crash (der frühere `User×2`-Bug tritt nicht mehr auf)
- **Morale:** Phase erreichbar

**Offene Beobachtungen aus dem Test:**
- Command Protocol-Namen sind auf Deutsch (`"Protokoll des Ewigen Wächters"`) obwohl App-UI auf Englisch ist — Datenproblem oder gewollt?
- Melee-Attack-Form (Warboss vs. Necrons) nicht automatisch testbar, da Units vorher chargen müssen — manuell im nächsten Testspiel verifizieren

---

## Was in früheren Sessions passiert ist (2026-06-03 — zweite Session)

### Bug 2 — Kampfphase: Gegner-Armeeliste verschwindet ✅

**Root Cause:** `render_attack_form` in `_common.py` rief `int("User×2")` auf (für killsaw/power_klaw des Big Mek in Mega Armour) → `ValueError`. Dieser Crash im Center-Column-Render verhinderte das Rendern der rechten Spalte (Necrons-Armeeliste). Warboss funktionierte weil `int("+3") = 3` in Python gültig ist.

**Fix:** Neue `_parse_strength(raw, unit_strength)` Hilfsfunktion in `_common.py`:
- `"User"` → `unit_strength`
- `"User×2"` → `unit_strength * 2`
- `"User+2"` → `unit_strength + 2`
- `"+3"` → `unit_strength + 3`
- Plain integers → `int(raw)`
- Fallback → `unit_strength`

**Wichtig:** Nie direkt `int(profile.strength)` aufrufen — immer `_parse_strength()` verwenden.

**Hinweis Datenproblem:** `attacks: Melee` für killsaw/power_klaw/uge_choppa in `orks/weapons.yaml` ist ein Scraper-Artefakt (kein Crash, zeigt `AMelee`). Korrekte Werte aus Kodex nachtragen.

### Bug 3 — Setup-Buttons tauschen Position ✅

**Root Cause:** `_render_setup()` las Button-Labels aus `first_player`/`second_player`, die nach `swap_players()` getauscht wurden → Buttons wechselten ihre Labels und Positionen.

**Fix:** `player_slots = (p1_name, p2_name)` wird einmalig in `init_state` gesetzt und NIE getauscht. Setup-Buttons lesen aus `player_slots` statt aus `first_player`/`second_player`.

**Constraint:** Setup-Buttons immer über `player_slots` — nicht über `first_player`/`second_player`.

**Betroffene Dateien:** `src/gameMechanic/game_state.py`, `src/uiLayout/gameActionsArea.py`

### BattleScribe Importer — Orks-Support ✅ (vor Session gefixt, in dieser Session committed)

- `_FACTION_CATALOGUE_MAP` um `"orks"` und `"ork"` erweitert
- Prefix-Stripping generisch (nicht mehr Necron-hardcoded): nutzt `faction_dir` + Singular-Form
- Fallback `"necrons"` → `ValueError` mit klarer Fehlermeldung wenn Fraktion unbekannt
- Tests in `test_rosz_importer.py` erweitert

### Bug 1 — Setup-Phase swap_players() ✅ (vor Session gefixt)

Setup-Buttons rufen `swap_players()` auf, das alle p1/p2-State-Keys korrekt tauscht (units, unit_keys, faction_dir, units_list).

### Weitere Fixes (committed)

- `Effect.target` optional (`None` default) — erlaubt Abilities ohne `target`-Feld
- `armyList.py`: `try/except` um `load_faction_abilities` — verhindert Crash bei fehlerhafter YAML
- `data/rosters/zarekhan_sol_kampf_2.yaml`: neues Necron-Roster

---

## Was in früheren Sessions passiert ist

### Data-driven Keyword-Matching ✅ (2026-06-03, erste Session)

- `Unit.has_keyword(kw: str) -> bool` — case-insensitive Vergleich direkt am Unit-Objekt
- Alle Frontend-Checks nutzen jetzt `unit.has_keyword()` statt literaler String-Vergleiche
- **Constraint:** Keywords IMMER `UPPERCASE` in allen YAML-Dateien

### Orks-Katalog vollständig ✅ (Ziel 5h)

51 Einheiten, 82 Waffen, faction/army/subfaction/stratagem/warlord/relics/unit_abilities/wargear/points — alle Dateien vorhanden. Punktekosten aus MFM 2023 — bei Spielbetrieb verifizieren.

---

## Aktueller Status

| Ziel | Status |
|------|--------|
| 5a — Spec | ✅ |
| 5b — Necron-Katalog | ✅ |
| 5c — Loader-Refactoring | ✅ |
| 5d — BattleScribe Importer | ✅ 2026-06-03 |
| 5e — Setup-Screen Redesign | ✅ |
| 5f — Stratagems PoC | ✅ 2026-06-03 |
| 5g — Regelkonformer Setup-Flow | ✅ |
| 5h — Orks-Katalog | ✅ |
| **5i — Abschluss & Qualitätssicherung** | ✅ 2026-06-03 |
| 6 — [wird nach Ziel 5 definiert] | ⬜ |
| 7 — Crusade-Erweiterung | ⬜ |
| 8 — Wahapedia Faction Fetcher | ⬜ |

---

## Nächste Schritte — Ziel 5i (restliche Punkte) → dann Ziel 6

Vollständige Checkliste: `docs/goals/ziel5.md` → Abschnitt 5i

### Stratagems ✅ erledigt (2026-06-03)

- CP-Bug (player: inactive) — `gameProtocoll.py` ✅
- Condition-Check auf Unit-Ebene — `_conditions_met()` ✅
- Stratagems-Hinweis in gameActionArea (Expander) ✅

### Setup-Screen ✅ erledigt

- Mission-Auswahl, Attacker/Defender, Secondary Objectives, unmatched-Warnungen, Punkte-Validierung ✅

### Code-Qualität ✅ (2026-06-03)

- ✅ **Faction-Dir Hardcode** — `unit.id.split(".")[1]` in `gameActionsArea.py`
- ✅ **`resolve_bracket_stats` verdrahten** — `fightPhase.py` + `shootingPhase.py` nutzen live WS/BS/attacks
- ✅ **`invuln_save` Orks** — Mega Armour-Einheiten (Warboss, Big Mek, Meganobz) auf 4++ korrigiert

### Datenqualität ✅ (2026-06-03)

- ✅ **Command Protocols Englisch** — `primary`/`secondary` + UI (`name_en`) auf Englisch
- ✅ **Datasheet Dual-Profile** — Setup-Anzeige iteriert alle `w.profiles`
- ✅ **Wargear im Roster-Format** — `wargear`-Feld in Roster; `_apply_wargear()` im Loader; BattleScribe-Importer extrahiert Upgrade-Selections

---

## Bekannte offene Lücken

| Lücke | Beschreibung |
|-------|-------------|
| Ork-Waffen `attacks: Melee` | Scraper-Artefakt: killsaw/power_klaw/uge_choppa zeigen `AMelee` — Kodex-Werte nachtragen |
| Melee-Attack-Form Orks unverifiziert | Warboss-Angriff (inkl. `User×2`-Fix) noch nicht im echten Testspiel mit Charge bestätigt |
| Forge World / Legends Necrons | Night Shroud, Canoptek Tombstalker, Acanthrites etc. — kein spielbarer Katalog |
| Ork `power_level: 0` | Codex-Werte nicht eingetragen (kein Blocker) |
| Waffen-Duplikate Orks | Kombi-Waffen teilen einen Eintrag (kein Blocker) |
| Adeptus Custodes | Nur Placeholder-Dateien — kein spielbarer Katalog |

---

## Wichtige Constraints

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts
- Setup-Buttons: `player_slots` verwenden, NICHT `first_player`/`second_player`
- dev-Branch — kein direktes Committen auf main
- **Keywords immer `UPPERCASE` in YAML** — Checks via `unit.has_keyword()`
- Weapon-Zugriff mit Dual-Profile: `w.for_phase(use_melee)` — nicht `w.is_melee`
- Session-State Unit-Keys: `p1_units` / `p2_units` mit `#N`-Suffix für Duplikate
- Weapon strength: `_parse_strength()` in `_common.py` — nie direkt `int(profile.strength)`

### State-Key System

Mehrfach-Units gleichen Typs werden mit `#N`-Suffix disambiguiert:
- Erstes Vorkommen: `wh40k_9e.necrons.unit.warriors`
- Zweites Vorkommen: `wh40k_9e.necrons.unit.warriors#1`

`unit_id_from_state_key(key)` → echte `unit.id`.
`lookup(faction, uid)` in `_common.py` versteht State-Keys.

### Streamlit 1.57 — CSS-Selektoren

| Komponente | Korrekte Selektoren |
|---|---|
| NumberInput Container | `[data-testid="stNumberInputContainer"]` |
| NumberInput Step-Buttons | `[data-testid="stNumberInputStepUp"]`, `[data-testid="stNumberInputStepDown"]` |
| Buttons allgemein | `button[data-testid="stBaseButton-{kind}"]` |
| Container border=True | `.e1rw0b1u3` (Emotion-Klasse — prüfen bei Streamlit-Update!) |
| Selectbox | `.stSelectbox [data-baseweb="select"] > div` |
