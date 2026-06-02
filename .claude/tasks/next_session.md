# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session passiert ist (2026-06-02)

### Ziel 5g — Setup-Screen vollständig implementiert ✅

**game_state.py:**
- `CP_BY_GAME_SIZE` korrigiert: 3 / 6 / 12 / 18 (vorher falsch: 3/3/6/9 — Quelle: Wahapedia)
- `init_state()` um 6 neue Parameter erweitert (alle optional mit Defaults, bestehende Tests unberührt):
  `game_mode`, `mission`, `attacker`, `use_secondaries`, `secondaries`, `secondary_vp`
- Open Play: CP immer fest 3, unabhängig von `game_size`

**setupScreen.py** — Kompletter Umbau:
- Spielmodus-Selektor oben (Matched / Open / Crusade — Crusade zeigt Info-Banner)
- Game Size + CP-Anzeige (Matched) bzw. fixed 3 CP (Open)
- Mission-Dropdown je Spielgröße (3–6 Missionen, GT-Missionpack)
- Attacker/Defender Roll-off-Button + persistiertes Ergebnis in `setup_attacker_result`
- Secondary Objectives Toggle (default: off) + 3 Kategorie/Objective-Picker pro Spieler
  — Live-Filterung: keine Kategorie doppelt je Spieler

**unit_mutations.py:**
- `adjust_secondary_vp(player_key, obj_idx, delta)` — Cap 0–15 per Objective

**gameActionsArea.py:**
- `_render_secondary_vp_section()` — Objective-Name + aktueller Wert + +/− Buttons
- Erscheint nur wenn `use_secondaries=True` und konfigurierte VP-Phase erreicht

### CSS-Fixes (gameHeader.py)

Gelernte Lektion: Streamlit 1.57 rendert NumberInput mit anderen testids als erwartet.
Korrekte Selektoren (nach JS-Source-Analyse):
- Container: `[data-testid="stNumberInputContainer"]`
- Buttons: `[data-testid="stNumberInputStepUp"]`, `[data-testid="stNumberInputStepDown"]`
- (Falsch war: `[data-testid="stNumberInput"] button` und `[data-baseweb="input"]`)

### Stand nach Session
- 323 Tests grün
- Ziel 5g vollständig abgeschlossen

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
| 5g — Regelkonformer Setup-Flow | ✅ **vollständig** |
| 5d — BattleScribe Importer | ⬜ |
| 5f — Stratagems PoC | ⬜ |

---

## Nächste Schritte (priorisiert)

### Priorität 1 — Ziel 5d: BattleScribe Importer

BattleScribe exportiert `.rosz`-Dateien (ZIP mit einer `.ros`-Datei, UTF-8 XML).
XML-Namespace: `http://www.battlescribe.net/schema/rosterSchema`
Python stdlib reicht (zipfile + xml.etree).

**Ziel:** `.rosz` → `data/rosters/<name>.yaml` (ID-basiertes Roster-Format)

Zu implementieren (in `tools/import_rosz.py`):
1. `.rosz` entpacken + XML parsen (Namespace-Check als Sicherheitsvalidierung)
2. Einheiten aus XML extrahieren → gegen Necron-Katalog matchen (via `load_unit_catalog()`)
3. Unmatched-Einheiten explizit flaggen (nicht crashen)
4. Roster-YAML schreiben: `id` + `models` (Wargear-Auswahl ist noch nicht im Format)
5. Streamlit File-Upload im Setup-Screen integrieren (`.rosz` Upload → sofort im Roster-Dropdown)

**Sicherheit:** Dateiformat-Validierung (`.rosz`/`.ros`), Max-Größe (z.B. 5 MB), XML-Namespace-Check

**Absehbare Lücke — Wargear:**
Das Roster-Format kennt aktuell nur `id` + `models`. BattleScribe enthält Wargear-Auswahl im XML.
Entscheidung nötig: Wargear jetzt mit einbauen (erfordert Loader-Erweiterung) oder erstmal nur matchen.
Empfehlung: zunächst ohne Wargear — sauberer Zwischenschritt.

**Roster-Format (aktuell):**
```yaml
faction_dir: necrons
display_name: Meine Armee
units:
  - id: wh40k_9e.necrons.unit.overlord
    models: 1
  - id: wh40k_9e.necrons.unit.warriors
    models: 10
```

### Priorität 2 — Orks-Fraktion

Orks haben nur eine Legacy `army.yaml` — kein `units.yaml`, `weapons.yaml` etc.
Wahapedia-Scraper liegt in `tools/wahapedia_scraper.py`.
Für echtes Zwei-Fraktionen-Spiel (Necrons vs. Orks) wird der vollständige Ork-Katalog gebraucht.

### Priorität 3 — Ziel 5f: Stratagems PoC

Infrastruktur (GO-Liste, Sichtbarkeitslogik) bereits vorbereitet in `gameProtocoll.py`.
Daten (stratagem_conditions, triggers) fehlen noch.

---

## Bekannte offene Lücken (nicht vergessen)

| Lücke | Beschreibung |
|-------|-------------|
| `resolve_bracket_stats` unverdrahtet | Implementiert in `loader.py`, aber kein UI-Aufruf — Vehicles zeigen immer Basis-Stats |
| Orks-Fraktion fehlt | Nur Legacy `army.yaml`, kein `units.yaml` |
| Forge World / Legends importieren | Noch nicht umgesetzt |
| Wargear im Roster-Format | Aktuell nur `id` + `models` — keine Wargear-Auswahl speicherbar |
| Punkte-Validierung | `load_points()` implementiert, aber Roster-Gesamtpunkte werden nicht gegen Spielgröße geprüft |
| Unmatched-UI | `roster_warnings` in session_state gesetzt, aber kein UI-Feedback im Setup-Screen |
| Dual-Profil Datasheet | Setup-Phase zeigt nur `profiles[0]` einer Waffe im Datasheet-View |
| Faction-Dir Hardcode | `gameActionsArea._display_unit_datasheet` nutzt `"necrons" if "necrons" in unit.id else "orks"` — muss auf `faction_dir_for()` umgestellt werden |
| CP +1/Runde verifizieren | `_common.py` zeigt "+1 CP (Battle-forged)" — Wahapedia Core Rules Command Phase noch nicht abgerufen zur Bestätigung |

---

## Wichtige Constraints

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts (unveränderlich während Spiel)
- dev-Branch — kein direktes Committen auf main
- Keywords immer `UPPERCASE` in units.yaml — Checks entsprechend schreiben
- Weapon-Zugriff: Nie `w.is_melee` für Filter nutzen wenn Dual-Profile möglich — `w.for_phase(use_melee)` verwenden
- Session-State Unit-Keys: `p1_units` / `p2_units` (nie wieder `necron_units`/`ork_units`)
- CP wird nur durch Game Mechanics verändert (Befehlsphase, Stratagems) — kein manueller Header-Stepper mehr

### Streamlit 1.57 — CSS-Selektoren (gelernte Lektionen)

Falsche Selektoren kosten Zeit. Vor dem Schreiben von CSS immer JS-Source prüfen:
`find .venv -name "*.js" | xargs grep -l "<Komponentenname>"` → dann testids aus dem Minified-JS extrahieren.

| Komponente | Korrekte Selektoren |
|---|---|
| NumberInput Container | `[data-testid="stNumberInputContainer"]` |
| NumberInput Step-Buttons | `[data-testid="stNumberInputStepUp"]`, `[data-testid="stNumberInputStepDown"]` |
| Buttons allgemein | `button[data-testid="stBaseButton-{kind}"]` (nicht `baseButton-{kind}`) |
| Container border=True | `.e1rw0b1u3` (Emotion-Klasse — kann sich bei Streamlit-Update ändern!) |
| Selectbox | `.stSelectbox [data-baseweb="select"] > div` |
